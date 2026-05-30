"""Testes unitários dos serviços de cálculo financeiro."""
import pytest
from decimal import Decimal
from unittest.mock import MagicMock

from services.expense_split_service import split_amount_equally
from services.settlement_service import calculate_group_summary


# ---------------------------------------------------------------------------
# split_amount_equally
# ---------------------------------------------------------------------------

def test_split_equally_exact():
    """R$ 30,00 ÷ 3 = R$ 10,00 cada."""
    shares = split_amount_equally(Decimal("30.00"), 3)
    assert len(shares) == 3
    assert all(share == Decimal("10.00") for share in shares)
    assert sum(shares) == Decimal("30.00")


def test_split_equally_with_remainder():
    """R$ 10,00 ÷ 3 = R$ 3,34 + R$ 3,33 + R$ 3,33 (centavos corretos)."""
    shares = split_amount_equally(Decimal("10.00"), 3)
    assert len(shares) == 3
    assert sum(shares) == Decimal("10.00")
    # O primeiro recebe 1 centavo a mais por causa do arredondamento
    assert shares[0] == Decimal("3.34")
    assert shares[1] == Decimal("3.33")
    assert shares[2] == Decimal("3.33")


def test_split_equally_zero_participants_raises():
    """participant_count <= 0 deve lançar ValueError."""
    with pytest.raises(ValueError):
        split_amount_equally(Decimal("10.00"), 0)


def test_split_equally_single_participant():
    """R$ 15,00 ÷ 1 = R$ 15,00."""
    shares = split_amount_equally(Decimal("15.00"), 1)
    assert shares == [Decimal("15.00")]


# ---------------------------------------------------------------------------
# Helpers para build de participantes e despesas com mocks leves
# ---------------------------------------------------------------------------

def _make_participant(pid, nome="P"):
    p = MagicMock()
    p.id = pid
    p.nome = nome
    return p


def _make_expense(eid, payer_id, amount, shares):
    """
    shares: lista de (participant_id, divided_amount)
    """
    expense = MagicMock()
    expense.id = eid
    expense.payer_participant_id = payer_id
    expense.amount = amount

    share_mocks = []
    for part_id, divided in shares:
        s = MagicMock()
        s.participant_id = part_id
        s.divided_amount = divided
        share_mocks.append(s)

    expense.participant_shares = share_mocks
    return expense


# ---------------------------------------------------------------------------
# calculate_group_summary — saldos
# ---------------------------------------------------------------------------

def test_calculate_summary_balance():
    """Saldo = total_pago - total_devido."""
    p1 = _make_participant(1, "Alice")
    p2 = _make_participant(2, "Bob")

    # Alice paga R$ 30, dividido igualmente entre os dois (R$ 15 cada)
    expense = _make_expense(
        eid=1,
        payer_id=1,
        amount=Decimal("30.00"),
        shares=[(1, Decimal("15.00")), (2, Decimal("15.00"))],
    )

    summary = calculate_group_summary([p1, p2], [expense])

    balance_alice = next(b for b in summary.balances if b.participant.id == 1)
    balance_bob = next(b for b in summary.balances if b.participant.id == 2)

    assert balance_alice.total_paid == Decimal("30.00")
    assert balance_alice.total_due == Decimal("15.00")
    assert balance_alice.balance == Decimal("15.00")  # a receber

    assert balance_bob.total_paid == Decimal("0.00")
    assert balance_bob.total_due == Decimal("15.00")
    assert balance_bob.balance == Decimal("-15.00")  # a pagar


def test_calculate_summary_settlement_suggestion():
    """Sugestão de acerto é gerada quando há devedor e credor."""
    p1 = _make_participant(1, "Credor")
    p2 = _make_participant(2, "Devedor")

    expense = _make_expense(
        eid=1,
        payer_id=1,
        amount=Decimal("20.00"),
        shares=[(1, Decimal("10.00")), (2, Decimal("10.00"))],
    )

    summary = calculate_group_summary([p1, p2], [expense])

    assert len(summary.settlements) == 1
    suggestion = summary.settlements[0]
    assert suggestion.payer.id == 2  # devedor paga
    assert suggestion.receiver.id == 1  # credor recebe
    assert suggestion.amount == Decimal("10.00")


def test_calculate_summary_empty():
    """Sem despesas, todos os saldos são zero e não há sugestões."""
    p1 = _make_participant(1, "A")
    p2 = _make_participant(2, "B")

    summary = calculate_group_summary([p1, p2], [])

    assert summary.total_spent == Decimal("0.00")
    assert all(b.balance == Decimal("0.00") for b in summary.balances)
    assert summary.settlements == []
