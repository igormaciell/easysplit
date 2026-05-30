import logging
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path

import click
from dotenv import load_dotenv
from flask import Flask, render_template

from extensions import db, login_manager
from models import User
from routes import auth_bp, groups_bp, notifications_bp, oauth_bp
from routes.oauth import init_oauth

load_dotenv()


def create_app(config_overrides: dict | None = None) -> Flask:
    app = Flask(__name__)

    base_dir = Path(__file__).resolve().parent
    db_path = base_dir / "easysplit.db"

    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
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
    app.register_blueprint(notifications_bp)
    app.register_blueprint(oauth_bp)

    init_oauth(app)

    if app.debug:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error("Erro interno: %s", e)
        return render_template("errors/500.html"), 500

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

    @app.context_processor
    def inject_unread_notifications():
        from flask_login import current_user
        from models import Notification

        if current_user.is_authenticated:
            count = Notification.query.filter_by(
                user_id=current_user.id, is_read=False
            ).count()
            return {"unread_notifications_count": count}
        return {"unread_notifications_count": 0}

    @app.get("/")
    def index() -> str:
        from flask_login import current_user
        from models import Group, Participant
        from sqlalchemy import or_

        groups = []
        stats = {"total_groups": 0, "total_expenses": 0, "total_participants": 0}
        if current_user.is_authenticated:
            all_groups = (
                Group.query.filter(
                    or_(
                        Group.owner_id == current_user.id,
                        Group.participants.any(Participant.user_id == current_user.id),
                    )
                )
                .order_by(Group.updated_at.desc())
                .all()
            )
            groups = all_groups[:6]
            stats["total_groups"] = len(all_groups)
            stats["total_expenses"] = sum(len(g.expenses) for g in all_groups)
            stats["total_participants"] = sum(len(g.participants) for g in all_groups)
        return render_template("index.html", groups=groups, stats=stats)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
