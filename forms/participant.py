from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ParticipantForm(FlaskForm):
    nome = StringField(
        "Nome do participante",
        validators=[
            DataRequired(message="Informe o nome do participante."),
            Length(min=2, max=120, message="Nome deve ter entre 2 e 120 caracteres."),
        ],
    )
    submit = SubmitField("Adicionar participante")
