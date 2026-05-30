from decimal import Decimal

from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, Optional


class PaymentForm(FlaskForm):
    payer_participant_id = SelectField(
        "Quem está pagando?",
        coerce=int,
        validate_choice=False,
        validators=[InputRequired(message="Selecione quem está pagando.")],
    )
    receiver_participant_id = SelectField(
        "Quem está recebendo?",
        coerce=int,
        validate_choice=False,
        validators=[InputRequired(message="Selecione quem está recebendo.")],
    )
    amount = DecimalField(
        "Valor",
        places=2,
        validators=[
            InputRequired(message="Informe o valor do pagamento."),
            NumberRange(min=Decimal("0.01"), message="O valor deve ser maior que zero."),
        ],
    )
    note = StringField(
        "Observação (opcional)",
        validators=[
            Optional(),
            Length(max=200, message="Observação deve ter no máximo 200 caracteres."),
        ],
    )
    submit = SubmitField("Registrar pagamento")
