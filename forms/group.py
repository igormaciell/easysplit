from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class GroupForm(FlaskForm):
    nome = StringField(
        "Nome do grupo",
        validators=[
            DataRequired(message="Informe o nome do grupo."),
            Length(min=2, max=120, message="Nome deve ter entre 2 e 120 caracteres."),
        ],
    )
    submit = SubmitField("Criar grupo")
