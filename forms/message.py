from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    content = StringField(
        "Mensagem",
        validators=[
            DataRequired(message="Digite uma mensagem."),
            Length(min=1, max=1000, message="Mensagem deve ter entre 1 e 1000 caracteres."),
        ],
    )
    submit = SubmitField("Enviar")
