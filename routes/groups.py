from datetime import UTC, datetime

from flask import Blueprint, Response, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from extensions import db
from forms import EmptyForm, ExpenseForm, GroupForm, InvitationForm, MessageForm, PaymentForm
from models import Expense, ExpenseParticipant, Group, GroupInvitation, Message, Notification, Participant, Payment, User
from services import calculate_group_summary, split_amount_equally
from routes.notifications import create_notification


groups_bp = Blueprint("groups", __name__, url_prefix="/groups")


def _get_group_for_user_or_404(group_id: int) -> Group:
    group = (
        Group.query.filter(
            Group.id == group_id,
            or_(
                Group.owner_id == current_user.id,
                Group.participants.any(Participant.user_id == current_user.id),
            ),
        ).first()
    )
    if group is None:
        abort(404)
    return group


def _get_owned_group_or_404(group_id: int) -> Group:
    group = Group.query.filter_by(id=group_id, owner_id=current_user.id).first()
    if group is None:
        abort(404)
    return group


def _group_participants(group: Group) -> list[Participant]:
    return (
        Participant.query.filter_by(group_id=group.id)
        .order_by(Participant.nome.asc())
        .all()
    )


def _group_expenses(group: Group) -> list[Expense]:
    return (
        Expense.query.filter_by(group_id=group.id)
        .order_by(Expense.expense_date.desc(), Expense.created_at.desc())
        .all()
    )


def _configure_expense_form(form: ExpenseForm, participants: list[Participant]) -> None:
    choices = [(participant.id, participant.nome) for participant in participants]
    form.payer_participant_id.choices = choices
    form.participant_ids.choices = choices


def _configure_payment_form(form: PaymentForm, participants: list[Participant]) -> None:
    choices = [(participant.id, participant.nome) for participant in participants]
    form.payer_participant_id.choices = choices
    form.receiver_participant_id.choices = choices


def _normalize_name(value: str) -> str:
    return " ".join(value.strip().split())


def _normalize_email(value: str) -> str:
    return value.strip().lower()


def _unique_participant_name(group_id: int, base_name: str) -> str:
    candidate = base_name
    counter = 2
    while Participant.query.filter_by(group_id=group_id, nome=candidate).first():
        candidate = f"{base_name} ({counter})"
        counter += 1
    return candidate


def _ensure_owner_participant(group: Group) -> None:
    if group.owner_id != current_user.id:
        return

    existing = Participant.query.filter_by(
        group_id=group.id,
        user_id=current_user.id,
    ).first()
    if existing is not None:
        return

    base_name = _normalize_name(current_user.nome)
    existing_by_name = Participant.query.filter(
        Participant.group_id == group.id,
        db.func.lower(Participant.nome) == base_name.lower(),
        Participant.user_id.is_(None),
    ).first()
    if existing_by_name is not None:
        existing_by_name.user_id = current_user.id
    else:
        unique_name = _unique_participant_name(group.id, base_name)
        participant = Participant(
            nome=unique_name,
            group_id=group.id,
            user_id=current_user.id,
        )
        db.session.add(participant)

    db.session.commit()


def _render_detail(
    group: Group,
    invite_form: InvitationForm | None = None,
    expense_form: ExpenseForm | None = None,
    payment_form: PaymentForm | None = None,
    message_form: MessageForm | None = None,
    status_code: int = 200,
):
    participants = _group_participants(group)
    expenses = _group_expenses(group)
    payments = (
        Payment.query.filter_by(group_id=group.id)
        .order_by(Payment.created_at.desc())
        .all()
    )
    summary = calculate_group_summary(participants, expenses, payments)
    invite_form = invite_form or InvitationForm()
    expense_form = expense_form or ExpenseForm()
    payment_form = payment_form or PaymentForm()
    message_form = message_form or MessageForm()
    _configure_expense_form(expense_form, participants)
    _configure_payment_form(payment_form, participants)
    is_owner = group.owner_id == current_user.id
    invitations = []
    if is_owner:
        invitations = (
            GroupInvitation.query.filter_by(group_id=group.id)
            .order_by(GroupInvitation.created_at.desc())
            .all()
        )
    messages = (
        Message.query.filter_by(group_id=group.id)
        .order_by(Message.created_at.asc())
        .limit(100)
        .all()
    )

    return (
        render_template(
            "groups/detail.html",
            group=group,
            invite_form=invite_form,
            expense_form=expense_form,
            payment_form=payment_form,
            message_form=message_form,
            delete_form=EmptyForm(),
            participants=participants,
            expenses=expenses,
            payments=payments,
            summary=summary,
            invitations=invitations,
            messages=messages,
            is_owner=is_owner,
            title=group.nome,
        ),
        status_code,
    )


@groups_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = GroupForm()

    if form.validate_on_submit():
        group = Group(nome=form.nome.data.strip(), owner_id=current_user.id)
        db.session.add(group)
        db.session.flush()
        participant = Participant(
            nome=_normalize_name(current_user.nome),
            group_id=group.id,
            user_id=current_user.id,
        )
        db.session.add(participant)
        db.session.commit()
        flash("Grupo criado com sucesso.", "success")
        return redirect(url_for("groups.index"))

    groups = (
        Group.query.filter(
            or_(
                Group.owner_id == current_user.id,
                Group.participants.any(Participant.user_id == current_user.id),
            )
        )
        .order_by(Group.created_at.desc())
        .all()
    )
    pending_invites = (
        GroupInvitation.query.filter_by(
            invited_user_id=current_user.id,
            status=GroupInvitation.STATUS_PENDING,
        )
        .order_by(GroupInvitation.created_at.desc())
        .all()
    )
    return render_template(
        "groups/index.html",
        form=form,
        groups=groups,
        pending_invites=pending_invites,
        invite_action_form=EmptyForm(),
        title="Grupos",
    )


@groups_bp.get("/<int:group_id>")
@login_required
def detail(group_id: int):
    group = _get_group_for_user_or_404(group_id)
    _ensure_owner_participant(group)
    participants = _group_participants(group)
    expense_form = ExpenseForm()
    _configure_expense_form(expense_form, participants)
    expense_form.participant_ids.data = [participant.id for participant in participants]

    return _render_detail(group, expense_form=expense_form)


@groups_bp.post("/<int:group_id>/invitations")
@login_required
def invite_participant(group_id: int):
    group = _get_owned_group_or_404(group_id)
    form = InvitationForm()

    if form.validate_on_submit():
        email = _normalize_email(form.email.data)
        if email == current_user.email:
            form.email.errors.append("Você já participa deste grupo como dono.")
            return _render_detail(group, invite_form=form, status_code=400)

        user = User.query.filter_by(email=email).first()
        if user is None:
            form.email.errors.append("Não existe conta cadastrada com este e-mail.")
            return _render_detail(group, invite_form=form, status_code=400)

        existing_participant = Participant.query.filter_by(
            group_id=group.id,
            user_id=user.id,
        ).first()
        if existing_participant is not None:
            form.email.errors.append("Este usuário já participa do grupo.")
            return _render_detail(group, invite_form=form, status_code=400)

        existing_invite = GroupInvitation.query.filter_by(
            group_id=group.id,
            invited_user_id=user.id,
        ).first()
        if existing_invite is not None:
            if existing_invite.status == GroupInvitation.STATUS_DECLINED:
                form.email.errors.append(
                    "Este convite já foi recusado e não pode ser reenviado."
                )
                return _render_detail(group, invite_form=form, status_code=400)
            if existing_invite.status == GroupInvitation.STATUS_PENDING:
                form.email.errors.append("Convite pendente já enviado para este usuário.")
                return _render_detail(group, invite_form=form, status_code=400)
            form.email.errors.append("Este usuário já participa do grupo.")
            return _render_detail(group, invite_form=form, status_code=400)

        invite = GroupInvitation(
            group_id=group.id,
            invited_user_id=user.id,
            invited_by_user_id=current_user.id,
        )
        db.session.add(invite)

        create_notification(
            user_id=user.id,
            type=Notification.TYPE_INVITE,
            title=f"Convite para o grupo {group.nome}",
            body=f"{current_user.nome} te convidou para participar.",
            link=url_for("groups.index"),
        )

        db.session.commit()

        flash("Convite enviado com sucesso.", "success")
        return redirect(url_for("groups.detail", group_id=group.id))

    return _render_detail(group, invite_form=form, status_code=400)


def _accept_invitation(invite: GroupInvitation) -> None:
    if invite.status != GroupInvitation.STATUS_PENDING:
        return

    invite.status = GroupInvitation.STATUS_ACCEPTED
    invite.responded_at = datetime.now(UTC)

    existing = Participant.query.filter_by(
        group_id=invite.group_id,
        user_id=invite.invited_user_id,
    ).first()
    if existing is None:
        user = invite.invited_user
        base_name = _normalize_name(user.nome)
        existing_by_name = Participant.query.filter(
            Participant.group_id == invite.group_id,
            db.func.lower(Participant.nome) == base_name.lower(),
            Participant.user_id.is_(None),
        ).first()
        if existing_by_name is not None:
            existing_by_name.user_id = invite.invited_user_id
        else:
            unique_name = _unique_participant_name(invite.group_id, base_name)
            participant = Participant(
                nome=unique_name,
                group_id=invite.group_id,
                user_id=invite.invited_user_id,
            )
            db.session.add(participant)

    db.session.commit()


@groups_bp.post("/invitations/<int:invite_id>/accept")
@login_required
def accept_invitation(invite_id: int):
    form = EmptyForm()
    if not form.validate_on_submit():
        flash("Não foi possível validar o convite. Tente novamente.", "danger")
        return redirect(url_for("groups.index"))

    invite = GroupInvitation.query.filter_by(
        id=invite_id,
        invited_user_id=current_user.id,
    ).first()
    if invite is None:
        abort(404)

    if invite.status != GroupInvitation.STATUS_PENDING:
        flash("Este convite já foi respondido.", "info")
        return redirect(url_for("groups.index"))

    _accept_invitation(invite)
    flash("Convite aceito com sucesso.", "success")
    return redirect(url_for("groups.detail", group_id=invite.group_id))


@groups_bp.post("/invitations/<int:invite_id>/decline")
@login_required
def decline_invitation(invite_id: int):
    form = EmptyForm()
    if not form.validate_on_submit():
        flash("Não foi possível validar o convite. Tente novamente.", "danger")
        return redirect(url_for("groups.index"))

    invite = GroupInvitation.query.filter_by(
        id=invite_id,
        invited_user_id=current_user.id,
    ).first()
    if invite is None:
        abort(404)

    if invite.status != GroupInvitation.STATUS_PENDING:
        flash("Este convite já foi respondido.", "info")
        return redirect(url_for("groups.index"))

    invite.status = GroupInvitation.STATUS_DECLINED
    invite.responded_at = datetime.now(UTC)
    db.session.commit()
    flash("Convite recusado.", "info")
    return redirect(url_for("groups.index"))


@groups_bp.post("/<int:group_id>/participants/<int:participant_id>/delete")
@login_required
def delete_participant(group_id: int, participant_id: int):
    group = _get_group_for_user_or_404(group_id)
    form = EmptyForm()
    if not form.validate_on_submit():
        flash("Não foi possível validar a remoção. Tente novamente.", "danger")
        return redirect(url_for("groups.detail", group_id=group.id))

    participant = Participant.query.filter_by(id=participant_id, group_id=group.id).first()
    if participant is None:
        abort(404)

    if participant.has_expense_history():
        flash(
            "Não é possível remover participante com despesas vinculadas ao histórico.",
            "warning",
        )
        return redirect(url_for("groups.detail", group_id=group.id))

    db.session.delete(participant)
    db.session.commit()
    flash("Participante removido com sucesso.", "success")
    return redirect(url_for("groups.detail", group_id=group.id))


@groups_bp.post("/<int:group_id>/expenses")
@login_required
def add_expense(group_id: int):
    group = _get_group_for_user_or_404(group_id)
    participants = _group_participants(group)
    form = ExpenseForm()
    _configure_expense_form(form, participants)

    if not participants:
        flash("Adicione participantes antes de registrar despesas.", "warning")
        return redirect(url_for("groups.detail", group_id=group.id))

    if form.validate_on_submit():
        participant_by_id = {participant.id: participant for participant in participants}
        selected_ids = form.participant_ids.data or []

        if len(selected_ids) != len(set(selected_ids)):
            form.participant_ids.errors.append("Selecione cada participante apenas uma vez.")
            return _render_detail(group, expense_form=form, status_code=400)

        if form.payer_participant_id.data not in participant_by_id:
            form.payer_participant_id.errors.append("Selecione um pagador válido para este grupo.")
            return _render_detail(group, expense_form=form, status_code=400)

        invalid_selected_ids = [
            participant_id
            for participant_id in selected_ids
            if participant_id not in participant_by_id
        ]
        if invalid_selected_ids:
            form.participant_ids.errors.append(
                "Selecione apenas participantes válidos deste grupo."
            )
            return _render_detail(group, expense_form=form, status_code=400)

        amount = form.amount.data
        selected_participants = [participant_by_id[participant_id] for participant_id in selected_ids]
        shares = split_amount_equally(amount, len(selected_participants))

        expense = Expense(
            title=form.title.data.strip(),
            amount=sum(shares),
            expense_date=form.expense_date.data,
            group_id=group.id,
            payer_participant_id=form.payer_participant_id.data,
        )

        for participant, divided_amount in zip(selected_participants, shares, strict=True):
            expense.participant_shares.append(
                ExpenseParticipant(
                    participant=participant,
                    divided_amount=divided_amount,
                )
            )

        db.session.add(expense)
        db.session.commit()

        for p in participants:
            if p.user_id and p.user_id != current_user.id:
                create_notification(
                    user_id=p.user_id,
                    type=Notification.TYPE_EXPENSE,
                    title=f"Nova despesa em {group.nome}",
                    body=f"{current_user.nome} registrou \"{form.title.data.strip()}\".",
                    link=url_for("groups.detail", group_id=group.id),
                )

        db.session.commit()
        flash("Despesa registrada com sucesso.", "success")
        return redirect(url_for("groups.detail", group_id=group.id))

    return _render_detail(group, expense_form=form, status_code=400)


@groups_bp.post("/<int:group_id>/payments")
@login_required
def add_payment(group_id: int):
    group = _get_group_for_user_or_404(group_id)
    participants = _group_participants(group)
    form = PaymentForm()
    _configure_payment_form(form, participants)

    if not participants:
        flash("Adicione participantes antes de registrar pagamentos.", "warning")
        return redirect(url_for("groups.detail", group_id=group.id))

    if form.validate_on_submit():
        participant_by_id = {p.id: p for p in participants}

        payer_id = form.payer_participant_id.data
        receiver_id = form.receiver_participant_id.data

        if payer_id not in participant_by_id:
            form.payer_participant_id.errors.append("Selecione um pagador válido.")
            return _render_detail(group, payment_form=form, status_code=400)

        if receiver_id not in participant_by_id:
            form.receiver_participant_id.errors.append("Selecione um recebedor válido.")
            return _render_detail(group, payment_form=form, status_code=400)

        if payer_id == receiver_id:
            form.receiver_participant_id.errors.append("Pagador e recebedor devem ser diferentes.")
            return _render_detail(group, payment_form=form, status_code=400)

        payment = Payment(
            group_id=group.id,
            payer_participant_id=payer_id,
            receiver_participant_id=receiver_id,
            amount=form.amount.data,
            note=form.note.data.strip() if form.note.data else "",
        )
        db.session.add(payment)

        receiver_participant = participant_by_id[receiver_id]
        if receiver_participant.user_id and receiver_participant.user_id != current_user.id:
            payer_participant = participant_by_id[payer_id]
            create_notification(
                user_id=receiver_participant.user_id,
                type=Notification.TYPE_PAYMENT,
                title=f"Pagamento recebido em {group.nome}",
                body=f"{payer_participant.nome} registrou um pagamento para você.",
                link=url_for("groups.detail", group_id=group.id),
            )

        db.session.commit()
        flash("Pagamento registrado com sucesso.", "success")
        return redirect(url_for("groups.detail", group_id=group.id))

    return _render_detail(group, payment_form=form, status_code=400)


@groups_bp.get("/<int:group_id>/export/csv")
@login_required
def export_csv(group_id: int):
    import csv
    import io

    group = _get_group_for_user_or_404(group_id)
    participants = _group_participants(group)
    expenses = _group_expenses(group)
    payments = (
        Payment.query.filter_by(group_id=group.id)
        .order_by(Payment.created_at.desc())
        .all()
    )
    summary = calculate_group_summary(participants, expenses, payments)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Relatório do grupo", group.nome])
    writer.writerow(["Total gasto", str(summary.total_spent)])
    writer.writerow(["Participantes", str(summary.participant_count)])
    writer.writerow(["Despesas", str(summary.expense_count)])
    writer.writerow([])

    writer.writerow(["DESPESAS"])
    writer.writerow(["Data", "Título", "Valor", "Pagador", "Participantes"])
    for expense in expenses:
        participant_names = ", ".join(
            share.participant.nome for share in expense.participant_shares
        )
        writer.writerow([
            expense.expense_date.strftime("%d/%m/%Y"),
            expense.title,
            f"{expense.amount:.2f}",
            expense.payer.nome,
            participant_names,
        ])

    writer.writerow([])
    writer.writerow(["PAGAMENTOS"])
    writer.writerow(["Data", "Pagador", "Recebedor", "Valor", "Observação"])
    for payment in payments:
        writer.writerow([
            payment.created_at.strftime("%d/%m/%Y"),
            payment.payer.nome,
            payment.receiver.nome,
            f"{payment.amount:.2f}",
            payment.note or "",
        ])

    writer.writerow([])
    writer.writerow(["SALDOS"])
    writer.writerow(["Participante", "Total Pago", "Total Devido", "Saldo", "Status"])
    for balance in summary.balances:
        writer.writerow([
            balance.participant.nome,
            f"{balance.total_paid:.2f}",
            f"{balance.total_due:.2f}",
            f"{balance.balance:.2f}",
            balance.status_label,
        ])

    writer.writerow([])
    writer.writerow(["SUGESTÕES DE ACERTO"])
    writer.writerow(["Pagador", "Recebedor", "Valor"])
    for settlement in summary.settlements:
        writer.writerow([
            settlement.payer.nome,
            settlement.receiver.nome,
            f"{settlement.amount:.2f}",
        ])

    csv_content = output.getvalue()
    output.close()

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=grupo_{group.id}_{group.nome}.csv"},
    )


@groups_bp.post("/<int:group_id>/messages")
@login_required
def send_message(group_id: int):
    group = _get_group_for_user_or_404(group_id)
    form = MessageForm()

    if form.validate_on_submit():
        message = Message(
            group_id=group.id,
            user_id=current_user.id,
            content=form.content.data.strip(),
        )
        db.session.add(message)

        participants = _group_participants(group)
        for p in participants:
            if p.user_id and p.user_id != current_user.id:
                create_notification(
                    user_id=p.user_id,
                    type=Notification.TYPE_MESSAGE,
                    title=f"Nova mensagem em {group.nome}",
                    body=f"{current_user.nome}: {form.content.data.strip()[:80]}",
                    link=url_for("groups.detail", group_id=group.id),
                )

        db.session.commit()
        flash("Mensagem enviada.", "success")
        return redirect(url_for("groups.detail", group_id=group.id))

    return _render_detail(group, message_form=form, status_code=400)
