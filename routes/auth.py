from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db
from forms.auth import LoginForm, RegisterForm
from models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Este e-mail já está cadastrado.", "danger")
            return render_template("auth/register.html", form=form)

        user = User(nome=form.nome.data.strip(), email=email, telefone=form.telefone.data.strip() if form.telefone.data else "")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Conta criada com sucesso. Faça login para continuar.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(form.password.data):
            flash("E-mail ou senha inválidos.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user)
        flash("Login realizado com sucesso.", "success")
        return redirect(url_for("index"))

    return render_template("auth/login.html", form=form)


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))

