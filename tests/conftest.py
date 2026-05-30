import pytest
from app import create_app
from extensions import db as _db


@pytest.fixture(scope="session")
def app():
    return create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "test",
        }
    )


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app, db):
    return app.test_client()


# ---------------------------------------------------------------------------
# Helpers reutilizáveis
# ---------------------------------------------------------------------------

def register_and_login(client, nome="Teste", email="teste@example.com", password="senha1234"):
    """Cria usuário via POST /register e faz login, retornando o client.
    
    Faz logout do usuário atual antes de registrar/logar, garantindo isolamento.
    """
    # Garante que não há sessão ativa
    client.post("/logout", follow_redirects=True)
    client.post(
        "/register",
        data={"nome": nome, "email": email, "password": password, "confirm_password": password},
        follow_redirects=True,
    )
    client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )
    return client
