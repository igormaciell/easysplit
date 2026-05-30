"""Testes de convites entre usuários."""
import pytest

from tests.conftest import register_and_login


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _setup_owner_and_group(app, owner_email="owner_inv@example.com"):
    """Cria usuário dono + grupo e retorna (group_id, owner_user_id)."""
    from models import Group, Participant, User
    from extensions import db as _db

    with app.app_context():
        owner = User.query.filter_by(email=owner_email).first()
        group = Group(nome="Grupo Convite", owner_id=owner.id)
        _db.session.add(group)
        _db.session.flush()
        _db.session.add(Participant(nome=owner.nome, group_id=group.id, user_id=owner.id))
        _db.session.commit()
        return group.id, owner.id


def _create_guest_user(app, nome="Convidado", email="guest_inv@example.com"):
    """Cria um usuário convidado diretamente no banco e retorna o id."""
    from models import User
    from extensions import db as _db

    with app.app_context():
        user = User(nome=nome, email=email)
        user.set_password("senha1234")
        _db.session.add(user)
        _db.session.commit()
        return user.id


# ---------------------------------------------------------------------------
# Testes de envio de convite
# ---------------------------------------------------------------------------

def test_invite_by_email_success(client, app):
    """Convite criado com status 'pending'."""
    from models import GroupInvitation
    from extensions import db as _db

    register_and_login(client, nome="Dono Inv", email="owner_inv@example.com")
    gid, _ = _setup_owner_and_group(app, "owner_inv@example.com")
    _create_guest_user(app, nome="Convidado Inv", email="guest_inv@example.com")

    resp = client.post(
        f"/groups/{gid}/invitations",
        data={"email": "guest_inv@example.com"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Convite enviado" in resp.data or b"enviado com sucesso" in resp.data

    with app.app_context():
        invite = GroupInvitation.query.filter_by(group_id=gid).first()
        assert invite is not None
        assert invite.status == GroupInvitation.STATUS_PENDING


def test_invite_nonexistent_email(client, app):
    """E-mail sem conta cadastrada retorna erro."""
    register_and_login(client, nome="Dono NE", email="owner_ne@example.com")
    gid, _ = _setup_owner_and_group(app, "owner_ne@example.com")

    resp = client.post(
        f"/groups/{gid}/invitations",
        data={"email": "naoexiste@example.com"},
        follow_redirects=True,
    )
    assert resp.status_code in (200, 400)
    assert b"Convite enviado" not in resp.data


# ---------------------------------------------------------------------------
# Testes de aceite e recusa
# ---------------------------------------------------------------------------

def test_accept_invitation(client, app):
    """Aceitar convite muda status para 'accepted' e cria participante."""
    from models import GroupInvitation, Participant
    from extensions import db as _db

    # Dono cria grupo e envia convite
    register_and_login(client, nome="Dono Acc", email="owner_acc@example.com")
    gid, owner_id = _setup_owner_and_group(app, "owner_acc@example.com")

    # Criar usuário convidado
    _create_guest_user(app, nome="Guest Acc", email="guest_acc@example.com")

    # Criar convite diretamente no banco
    with app.app_context():
        from models import User
        guest = User.query.filter_by(email="guest_acc@example.com").first()
        invite = GroupInvitation(
            group_id=gid,
            invited_user_id=guest.id,
            invited_by_user_id=owner_id,
        )
        _db.session.add(invite)
        _db.session.commit()
        invite_id = invite.id

    # Login como convidado e aceita
    register_and_login(client, nome="Guest Acc", email="guest_acc@example.com")
    resp = client.post(
        f"/groups/invitations/{invite_id}/accept",
        data={},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"aceito" in resp.data or b"sucesso" in resp.data

    with app.app_context():
        invite = _db.session.get(GroupInvitation, invite_id)
        assert invite.status == GroupInvitation.STATUS_ACCEPTED
        participant = Participant.query.filter_by(group_id=gid, user_id=invite.invited_user_id).first()
        assert participant is not None


def test_decline_invitation(client, app):
    """Recusar convite muda status para 'declined'."""
    from models import GroupInvitation
    from extensions import db as _db

    register_and_login(client, nome="Dono Dec", email="owner_dec@example.com")
    gid, owner_id = _setup_owner_and_group(app, "owner_dec@example.com")

    _create_guest_user(app, nome="Guest Dec", email="guest_dec@example.com")

    with app.app_context():
        from models import User
        guest = User.query.filter_by(email="guest_dec@example.com").first()
        invite = GroupInvitation(
            group_id=gid,
            invited_user_id=guest.id,
            invited_by_user_id=owner_id,
        )
        _db.session.add(invite)
        _db.session.commit()
        invite_id = invite.id

    register_and_login(client, nome="Guest Dec", email="guest_dec@example.com")
    resp = client.post(
        f"/groups/invitations/{invite_id}/decline",
        data={},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    with app.app_context():
        invite = _db.session.get(GroupInvitation, invite_id)
        assert invite.status == GroupInvitation.STATUS_DECLINED
