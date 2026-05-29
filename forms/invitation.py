from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class InvitationForm(FlaskForm):
    email = EmailField(
        "E-mail do participante",
        validators=[
            DataRequired(message="Informe o e-mail da pessoa."),
            Email(message="Informe um e-mail válido."),
            Length(max=255, message="E-mail muito longo."),
        ],
    )
    submit = SubmitField("Enviar convite")
