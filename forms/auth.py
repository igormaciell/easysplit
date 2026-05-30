from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class RegisterForm(FlaskForm):
    nome = StringField(
        "Nome",
        validators=[
            DataRequired(message="Informe seu nome."),
            Length(min=2, max=120, message="Nome deve ter entre 2 e 120 caracteres."),
        ],
    )
    email = EmailField(
        "E-mail",
        validators=[
            DataRequired(message="Informe seu e-mail."),
            Email(message="Informe um e-mail válido."),
            Length(max=255, message="E-mail muito longo."),
        ],
    )
    telefone = StringField(
        "Telefone (opcional)",
        validators=[
            Optional(),
            Length(max=20, message="Telefone deve ter no máximo 20 caracteres."),
        ],
    )
    password = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="Informe uma senha."),
            Length(min=8, message="Senha deve ter pelo menos 8 caracteres."),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(message="Confirme sua senha."),
            EqualTo("password", message="As senhas não coincidem."),
        ],
    )
    submit = SubmitField("Cadastrar")


class LoginForm(FlaskForm):
    email = EmailField(
        "E-mail",
        validators=[
            DataRequired(message="Informe seu e-mail."),
            Email(message="Informe um e-mail válido."),
        ],
    )
    password = PasswordField(
        "Senha",
        validators=[DataRequired(message="Informe sua senha.")],
    )
    submit = SubmitField("Entrar")

