import os

from authlib.integrations.flask_client import OAuth
from flask import Blueprint, flash, redirect, session, url_for
from flask_login import login_user

from extensions import db
from models import User


oauth_bp = Blueprint("oauth", __name__, url_prefix="/oauth")
oauth = OAuth()


def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )


@oauth_bp.get("/google/login")
def google_login():
    if not os.environ.get("GOOGLE_CLIENT_ID"):
        flash("Login com Google não está configurado.", "warning")
        return redirect(url_for("auth.login"))
    redirect_uri = url_for("oauth.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@oauth_bp.get("/google/callback")
def google_callback():
    try:
        token = oauth.google.authorize_access_token()
    except Exception:
        flash("Erro na autenticação com Google. Tente novamente.", "danger")
        return redirect(url_for("auth.login"))

    user_info = token.get("userinfo")
    if not user_info:
        user_info = oauth.google.userinfo()

    google_id = user_info.get("sub")
    email = user_info.get("email", "").lower()
    nome = user_info.get("name", email.split("@")[0])

    user = User.query.filter_by(google_id=google_id).first()
    if user is None:
        user = User.query.filter_by(email=email).first()
        if user is not None:
            user.google_id = google_id
            db.session.commit()
        else:
            user = User(
                nome=nome,
                email=email,
                google_id=google_id,
                password_hash="oauth-no-password",
            )
            db.session.add(user)
            db.session.commit()

    login_user(user)
    flash("Login com Google realizado com sucesso.", "success")
    return redirect(url_for("index"))
