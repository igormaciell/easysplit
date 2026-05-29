from datetime import date
from decimal import Decimal

from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange


class ExpenseForm(FlaskForm):
    title = StringField(
        "Título da despesa",
        validators=[
            DataRequired(message="Informe o título da despesa."),
            Length(min=2, max=160, message="Título deve ter entre 2 e 160 caracteres."),
        ],
    )
    amount = DecimalField(
        "Valor",
        places=2,
        validators=[
            InputRequired(message="Informe o valor da despesa."),
            NumberRange(min=Decimal("0.01"), message="O valor deve ser maior que zero."),
        ],
    )
    expense_date = DateField(
        "Data",
        default=date.today,
        validators=[DataRequired(message="Informe a data da despesa.")],
    )
    payer_participant_id = SelectField(
        "Quem pagou?",
        coerce=int,
        validate_choice=False,
        validators=[DataRequired(message="Selecione quem pagou.")],
    )
    participant_ids = SelectMultipleField(
        "Participantes da divisão",
        coerce=int,
        validate_choice=False,
        validators=[DataRequired(message="Selecione pelo menos um participante.")],
    )
    submit = SubmitField("Salvar despesa")
