---
applyTo: "tests/**/*.py"
---

# Testes Automatizados — EasySplit

## Stack de testes

- **pytest** como runner principal.
- **pytest-flask** para fixtures de app e client HTTP.
- Arquivo de configuração: `tests/conftest.py`.

## Configuração obrigatória (`tests/conftest.py`)

```python
import pytest
from app import create_app
from extensions import db as _db

@pytest.fixture(scope="session")
def app():
    return create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test",
    })

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
```

> `WTF_CSRF_ENABLED=False` é obrigatório nos testes para não precisar incluir token CSRF em posts.

## O que testar (mínimo para o MVP)

| Área | Casos obrigatórios |
|------|-------------------|
| Auth | Registro, login com senha correta, login com senha errada, logout |
| Grupos | Criar grupo autenticado, listar apenas grupos do dono |
| Participantes | Adicionar, remover, bloquear remoção com despesa |
| Despesas | Registrar despesa, validar valor ≤ 0 rejeitado |
| Serviços | `split_amount_equally()` — centavos corretos; `calculate_group_summary()` — saldo correto |
| Autorização | Rota privada redireciona não-autenticado; usuário não acessa grupo de outro |

## Convenções

- Um arquivo por módulo: `tests/test_auth.py`, `tests/test_groups.py`, `tests/test_services.py`.
- Nomes de funções: `test_<ação>_<contexto>` (ex: `test_login_wrong_password`).
- Usar `db.session.add()` diretamente nas fixtures de dados — sem factory libraries.
- Helpers de usuário autenticado: criar usuário via model e fazer login via `client.post("/auth/login", ...)`.

## Rodar testes

```bash
pip install pytest pytest-flask
pytest tests/ -v
```
