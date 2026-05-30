---
applyTo: "{models,routes,services,forms}/**/*.py"
---

# Backend Flask — EasySplit

## Models (SQLAlchemy)

- Timestamps usam `datetime.now(UTC)` — nunca `datetime.utcnow()` (deprecated).
- Novos models devem ser importados em `models/__init__.py` e registrados nos imports de `routes/groups.py` ou no blueprint relevante.
- Relações com `cascade="all, delete-orphan"` nos relacionamentos pai → filho.

## Blueprints / Rotas

- Todo blueprint criado precisa ser registrado via `app.register_blueprint(...)` em `create_app()` em `app.py`.
- Rotas privadas: sempre decorar com `@login_required`.
- Acesso a dados: sempre filtrar por `owner_id == current_user.id` ou relação de participante. Usar helpers `_get_group_for_user_or_404` / `_get_owned_group_or_404` como modelo.

## Serviços

- Lógica financeira → `services/settlement_service.py` (`calculate_group_summary()`).
- Divisão de valores → `services/expense_split_service.py` (`split_amount_equally()`).
- `split_amount_equally()` distribui centavos corretamente (sem arredondamento que gere diferença).

## Formulários (WTForms)

- Formulários ficam em `forms/`, um arquivo por domínio.
- Exportar todas as classes via `forms/__init__.py`.
- Validar no formulário **e** confirmar integridade no backend (ex: checar se pagador pertence ao grupo).

## Configuração e Variáveis de Ambiente

- `SECRET_KEY="dev"` — hardcoded para desenvolvimento. Para produção, ler de variável de ambiente:
  ```python
  app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")
  ```
- Usar arquivo `.env` na raiz com `python-dotenv` para carregar variáveis localmente.
- `.env` **nunca** deve ser versionado — garantir que está no `.gitignore`.
- Banco: SQLite em `easysplit.db` na raiz do projeto (criado por `flask --app app init-db`).

## Logging e Tratamento de Erros

- Usar `app.logger` (já disponível no Flask) para registrar erros inesperados — não usar `print()`.
- Erros de acesso não autorizado: usar `abort(403)` ou redirecionar com `flash()`.
- Erros de recurso não encontrado: usar `abort(404)` — os helpers `_get_group_for_user_or_404` já fazem isso.
- Registrar handler de erro 404/500 em `create_app()` quando necessário:
  ```python
  @app.errorhandler(404)
  def not_found(e):
      return render_template("errors/404.html"), 404
  ```
- Em operações de banco que podem falhar, usar `try/except` com `db.session.rollback()` antes de relançar.
