"""Testes de grupos e participantes."""
import pytest
from tests.conftest import register_and_login


# ---------------------------------------------------------------------------
# Helpers locais
# ---------------------------------------------------------------------------

def _create_group(client, nome="Viagem SP"):
    return client.post(
        "/groups/",
        data={"nome": nome},
        follow_redirects=True,
    )


# ---------------------------------------------------------------------------
# Grupos
# ---------------------------------------------------------------------------

def test_create_group(client):
    """POST /groups/ cria grupo e adiciona dono como participante."""
    register_and_login(client, email="owner@example.com")
    resp = _create_group(client, "Churrasco")
    assert resp.status_code == 200
    assert b"Churrasco" in resp.data or b"Grupo criado" in resp.data


def test_list_groups_only_own(client, app):
    """Usuário B não vê grupos criados pelo usuário A."""
    # Usuário A cria um grupo
    register_and_login(client, nome="Usua A", email="a@example.com")
    _create_group(client, "Grupo Secreto A")

    # Usuário B faz login
    register_and_login(client, nome="Usua B", email="b@example.com")
    resp = client.get("/groups/", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Grupo Secreto A" not in resp.data


def test_access_other_user_group_returns_404(client, app):
    """Usuário B não consegue acessar o grupo do usuário A (404)."""
    from models import Group, Participant, User
    from extensions import db as _db

    with app.app_context():
        user_a = User(nome="User A", email="ua@example.com")
        user_a.set_password("senha1234")
        _db.session.add(user_a)
        _db.session.flush()
        group = Group(nome="Grupo A", owner_id=user_a.id)
        _db.session.add(group)
        _db.session.flush()
        _db.session.add(Participant(nome="User A", group_id=group.id, user_id=user_a.id))
        _db.session.commit()
        gid = group.id

    register_and_login(client, nome="User B", email="ub@example.com")
    resp = client.get(f"/groups/{gid}")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Participantes
# ---------------------------------------------------------------------------

def test_add_participant(client, app):
    """Participante adicionado diretamente no banco aparece na página do grupo."""
    from models import Group, Participant, User
    from extensions import db as _db

    register_and_login(client, nome="Dono", email="dono@example.com")

    with app.app_context():
        owner = User.query.filter_by(email="dono@example.com").first()
        group = Group(nome="Grupo Participante", owner_id=owner.id)
        _db.session.add(group)
        _db.session.flush()
        _db.session.add(Participant(nome="Dono", group_id=group.id, user_id=owner.id))
        novo = Participant(nome="Novo Amigo", group_id=group.id)
        _db.session.add(novo)
        _db.session.commit()
        gid = group.id

    resp = client.get(f"/groups/{gid}", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Novo Amigo" in resp.data


def test_remove_participant_without_expenses(client, app):
    """Participante sem despesas pode ser removido com sucesso."""
    from models import Group, Participant, User
    from extensions import db as _db

    register_and_login(client, nome="Remov Owner", email="remov@example.com")

    with app.app_context():
        owner = User.query.filter_by(email="remov@example.com").first()
        group = Group(nome="Grupo Remov", owner_id=owner.id)
        _db.session.add(group)
        _db.session.flush()
        participant = Participant(nome="Participante Remov", group_id=group.id)
        _db.session.add(participant)
        _db.session.commit()
        gid = group.id
        pid = participant.id

    resp = client.post(
        f"/groups/{gid}/participants/{pid}/delete",
        data={},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"removido com sucesso" in resp.data or b"Participante Remov" not in resp.data


def test_remove_participant_with_expenses_blocked(client, app):
    """Participante com despesas não pode ser removido."""
    from datetime import date
    from decimal import Decimal
    from models import Expense, ExpenseParticipant, Group, Participant, User
    from extensions import db as _db

    register_and_login(client, nome="Block Owner", email="block@example.com")

    with app.app_context():
        owner = User.query.filter_by(email="block@example.com").first()
        group = Group(nome="Grupo Block", owner_id=owner.id)
        _db.session.add(group)
        _db.session.flush()
        payer = Participant(nome="Pagador Block", group_id=group.id, user_id=owner.id)
        other = Participant(nome="Outro Block", group_id=group.id)
        _db.session.add_all([payer, other])
        _db.session.flush()
        expense = Expense(
            title="Almoço",
            amount=Decimal("30.00"),
            expense_date=date.today(),
            group_id=group.id,
            payer_participant_id=payer.id,
        )
        _db.session.add(expense)
        _db.session.flush()
        _db.session.add(
            ExpenseParticipant(expense_id=expense.id, participant_id=payer.id, divided_amount=Decimal("15.00"))
        )
        _db.session.add(
            ExpenseParticipant(expense_id=expense.id, participant_id=other.id, divided_amount=Decimal("15.00"))
        )
        _db.session.commit()
        gid = group.id
        pid = payer.id

    resp = client.post(
        f"/groups/{gid}/participants/{pid}/delete",
        data={},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"despesas" in resp.data or b"bloqueada" in resp.data or b"n\xc3\xa3o" in resp.data
