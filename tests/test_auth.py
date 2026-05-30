"""Testes de autenticação — registro, login, logout e proteção de rotas."""
import pytest


# ---------------------------------------------------------------------------
# Registro
# ---------------------------------------------------------------------------

def test_register_success(client):
    """POST /register cria conta e redireciona para login."""
    resp = client.post(
        "/register",
        data={
            "nome": "Ana Souza",
            "email": "ana@example.com",
            "password": "senha1234",
            "confirm_password": "senha1234",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Conta criada com sucesso" in resp.data


def test_register_duplicate_email(client):
    """Segundo cadastro com o mesmo e-mail retorna erro."""
    payload = {
        "nome": "Carlos",
        "email": "carlos@example.com",
        "password": "senha1234",
        "confirm_password": "senha1234",
    }
    client.post("/register", data=payload, follow_redirects=True)
    resp = client.post("/register", data=payload, follow_redirects=True)
    assert resp.status_code == 200
    assert b"j\xc3\xa1 est\xc3\xa1 cadastrado" in resp.data or b"cadastrado" in resp.data


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def test_login_success(client):
    """Login com credenciais corretas redireciona para página principal."""
    client.post(
        "/register",
        data={
            "nome": "Maria",
            "email": "maria@example.com",
            "password": "senha1234",
            "confirm_password": "senha1234",
        },
        follow_redirects=True,
    )
    resp = client.post(
        "/login",
        data={"email": "maria@example.com", "password": "senha1234"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    # Redireciona para a home — não deve mostrar "login" na URL
    assert b"Login realizado com sucesso" in resp.data


def test_login_wrong_password(client):
    """Login com senha errada retorna 200 com mensagem de erro."""
    client.post(
        "/register",
        data={
            "nome": "Pedro",
            "email": "pedro@example.com",
            "password": "senha1234",
            "confirm_password": "senha1234",
        },
        follow_redirects=True,
    )
    resp = client.post(
        "/login",
        data={"email": "pedro@example.com", "password": "senhaerrada"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"E-mail ou senha" in resp.data or b"inv\xc3\xa1lidos" in resp.data


# ---------------------------------------------------------------------------
# Logout
# ---------------------------------------------------------------------------

def test_logout(client):
    """Logout redireciona para login."""
    client.post(
        "/register",
        data={
            "nome": "Julia",
            "email": "julia@example.com",
            "password": "senha1234",
            "confirm_password": "senha1234",
        },
        follow_redirects=True,
    )
    client.post(
        "/login",
        data={"email": "julia@example.com", "password": "senha1234"},
        follow_redirects=True,
    )
    resp = client.post("/logout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"saiu" in resp.data or b"login" in resp.data.lower()


# ---------------------------------------------------------------------------
# Proteção de rotas
# ---------------------------------------------------------------------------

def test_protected_route_redirects_unauthenticated(client):
    """GET /groups/ sem login redireciona para /login."""
    resp = client.get("/groups/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]
