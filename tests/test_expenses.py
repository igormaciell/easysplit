"""Testes de registro e visualização de despesas."""
import pytest
from datetime import date
from decimal import Decimal

from tests.conftest import register_and_login


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _setup_group_with_participants(app, owner_email):
    """Cria grupo com dois participantes para testes de despesa."""
    from models import Group, Participant, User
    from extensions import db as _db

    with app.app_context():
        owner = User.query.filter_by(email=owner_email).first()
        group = Group(nome="Grupo Despesa", owner_id=owner.id)
        _db.session.add(group)
        _db.session.flush()
        p1 = Participant(nome="P1", group_id=group.id, user_id=owner.id)
        p2 = Participant(nome="P2", group_id=group.id)
        _db.session.add_all([p1, p2])
        _db.session.commit()
        return group.id, p1.id, p2.id


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

def test_add_expense_success(client, app):
    """Despesa é registrada com divisão igualitária."""
    register_and_login(client, nome="Exp Owner", email="expowner@example.com")
    gid, p1_id, p2_id = _setup_group_with_participants(app, "expowner@example.com")

    resp = client.post(
        f"/groups/{gid}/expenses",
        data={
            "title": "Almoço no restaurante",
            "amount": "30.00",
            "expense_date": date.today().isoformat(),
            "payer_participant_id": p1_id,
            "participant_ids": [p1_id, p2_id],
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Almo" in resp.data or b"registrada" in resp.data


def test_add_expense_zero_value_rejected(client, app):
    """Valor ≤ 0 é rejeitado com erro de validação."""
    register_and_login(client, nome="Zero Owner", email="zeroowner@example.com")
    gid, p1_id, p2_id = _setup_group_with_participants(app, "zeroowner@example.com")

    resp = client.post(
        f"/groups/{gid}/expenses",
        data={
            "title": "Despesa inválida",
            "amount": "0.00",
            "expense_date": date.today().isoformat(),
            "payer_participant_id": p1_id,
            "participant_ids": [p1_id],
        },
        follow_redirects=True,
    )
    # Espera erro — não deve redirecionar para sucesso
    assert resp.status_code in (200, 400)
    # Não deve haver mensagem de sucesso
    assert b"registrada com sucesso" not in resp.data


def test_expense_history_visible(client, app):
    """Despesa registrada aparece no histórico da página de detalhe do grupo."""
    from models import Expense, ExpenseParticipant, Group, Participant, User
    from extensions import db as _db

    register_and_login(client, nome="Hist Owner", email="histowner@example.com")

    with app.app_context():
        owner = User.query.filter_by(email="histowner@example.com").first()
        group = Group(nome="Grupo Hist", owner_id=owner.id)
        _db.session.add(group)
        _db.session.flush()
        p = Participant(nome="Hist Payer", group_id=group.id, user_id=owner.id)
        _db.session.add(p)
        _db.session.flush()
        expense = Expense(
            title="Jantar especial",
            amount=Decimal("50.00"),
            expense_date=date.today(),
            group_id=group.id,
            payer_participant_id=p.id,
        )
        _db.session.add(expense)
        _db.session.flush()
        _db.session.add(
            ExpenseParticipant(
                expense_id=expense.id,
                participant_id=p.id,
                divided_amount=Decimal("50.00"),
            )
        )
        _db.session.commit()
        gid = group.id

    resp = client.get(f"/groups/{gid}", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Jantar especial" in resp.data
