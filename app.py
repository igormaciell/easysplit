from decimal import Decimal, InvalidOperation
from pathlib import Path

import click
from flask import Flask, render_template

from extensions import db, login_manager
from models import User
from routes import auth_bp, groups_bp


def create_app(config_overrides: dict | None = None) -> Flask:
    app = Flask(__name__)

    base_dir = Path(__file__).resolve().parent
    db_path = base_dir / "easysplit.db"

    app.config.update(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar esta página."
    login_manager.login_message_category = "warning"

    app.register_blueprint(auth_bp)
    app.register_blueprint(groups_bp)

    @app.template_filter("brl")
    def brl(value) -> str:
        try:
            amount = Decimal(value or 0).quantize(Decimal("0.01"))
        except (InvalidOperation, TypeError, ValueError):
            amount = Decimal("0.00")
        formatted = f"{amount:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
        return f"R$ {formatted}"

    @app.template_filter("date_br")
    def date_br(value) -> str:
        if value is None:
            return ""
        return value.strftime("%d/%m/%Y")

    @app.cli.command("init-db")
    def init_db_command() -> None:
        db.create_all()
        click.echo("Banco de dados inicializado.")

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
