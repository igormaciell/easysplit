from dataclasses import dataclass
from decimal import Decimal

from models import Expense, Participant
from services.expense_split_service import CENTS, to_money


@dataclass(frozen=True)
class ParticipantBalance:
    participant: Participant
    total_paid: Decimal
    total_due: Decimal
    balance: Decimal

    @property
    def status_label(self) -> str:
        if self.balance > 0:
            return "A receber"
        if self.balance < 0:
            return "A pagar"
        return "Quitado"

    @property
    def status_class(self) -> str:
        if self.balance > 0:
            return "success"
        if self.balance < 0:
            return "danger"
        return "secondary"

    @property
    def absolute_balance(self) -> Decimal:
        return abs(self.balance)


@dataclass(frozen=True)
class SettlementSuggestion:
    payer: Participant
    receiver: Participant
    amount: Decimal


@dataclass(frozen=True)
class GroupFinancialSummary:
    total_spent: Decimal
    participant_count: int
    expense_count: int
    largest_expense: Expense | None
    balances: list[ParticipantBalance]
    settlements: list[SettlementSuggestion]


def calculate_group_summary(
    participants: list[Participant],
    expenses: list[Expense],
) -> GroupFinancialSummary:
    totals = {
        participant.id: {
            "participant": participant,
            "paid": Decimal("0.00"),
            "due": Decimal("0.00"),
        }
        for participant in participants
    }

    total_spent = Decimal("0.00")
    largest_expense: Expense | None = None

    for expense in expenses:
        amount = to_money(expense.amount)
        total_spent += amount

        if largest_expense is None or amount > to_money(largest_expense.amount):
            largest_expense = expense

        if expense.payer_participant_id in totals:
            totals[expense.payer_participant_id]["paid"] += amount

        for share in expense.participant_shares:
            if share.participant_id in totals:
                totals[share.participant_id]["due"] += to_money(share.divided_amount)

    balances = [
        ParticipantBalance(
            participant=values["participant"],
            total_paid=to_money(values["paid"]),
            total_due=to_money(values["due"]),
            balance=to_money(values["paid"] - values["due"]),
        )
        for values in totals.values()
    ]
    balances.sort(key=lambda item: item.participant.nome.lower())

    return GroupFinancialSummary(
        total_spent=to_money(total_spent),
        participant_count=len(participants),
        expense_count=len(expenses),
        largest_expense=largest_expense,
        balances=balances,
        settlements=_build_settlement_suggestions(balances),
    )


def _build_settlement_suggestions(
    balances: list[ParticipantBalance],
) -> list[SettlementSuggestion]:
    debtors = [
        {"participant": balance.participant, "amount": to_money(abs(balance.balance))}
        for balance in balances
        if balance.balance < 0
    ]
    receivers = [
        {"participant": balance.participant, "amount": to_money(balance.balance)}
        for balance in balances
        if balance.balance > 0
    ]

    debtors.sort(key=lambda item: item["participant"].nome.lower())
    receivers.sort(key=lambda item: item["participant"].nome.lower())

    suggestions: list[SettlementSuggestion] = []
    debtor_index = 0
    receiver_index = 0

    while debtor_index < len(debtors) and receiver_index < len(receivers):
        debtor = debtors[debtor_index]
        receiver = receivers[receiver_index]
        amount = to_money(min(debtor["amount"], receiver["amount"]))

        if amount >= CENTS:
            suggestions.append(
                SettlementSuggestion(
                    payer=debtor["participant"],
                    receiver=receiver["participant"],
                    amount=amount,
                )
            )

        debtor["amount"] = to_money(debtor["amount"] - amount)
        receiver["amount"] = to_money(receiver["amount"] - amount)

        if debtor["amount"] < CENTS:
            debtor_index += 1
        if receiver["amount"] < CENTS:
            receiver_index += 1

    return suggestions
