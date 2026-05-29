from decimal import Decimal, ROUND_HALF_UP


CENTS = Decimal("0.01")


def to_money(value: Decimal) -> Decimal:
    return Decimal(value).quantize(CENTS, rounding=ROUND_HALF_UP)


def split_amount_equally(amount: Decimal, participant_count: int) -> list[Decimal]:
    if participant_count <= 0:
        raise ValueError("participant_count deve ser maior que zero.")

    total_cents = int((to_money(amount) * 100).to_integral_value(rounding=ROUND_HALF_UP))
    base_cents = total_cents // participant_count
    remainder = total_cents % participant_count

    shares: list[Decimal] = []
    for index in range(participant_count):
        cents = base_cents + (1 if index < remainder else 0)
        shares.append(to_money(Decimal(cents) / 100))

    return shares
