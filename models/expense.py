from datetime import UTC, datetime

from extensions import db


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False, index=True)
    payer_participant_id = db.Column(
        db.Integer,
        db.ForeignKey("participants.id"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    group = db.relationship("Group", back_populates="expenses")
    payer = db.relationship(
        "Participant",
        back_populates="paid_expenses",
        foreign_keys=[payer_participant_id],
    )
    participant_shares = db.relationship(
        "ExpenseParticipant",
        back_populates="expense",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Expense id={self.id} title='{self.title}'>"


class ExpenseParticipant(db.Model):
    __tablename__ = "expense_participants"
    __table_args__ = (
        db.UniqueConstraint("expense_id", "participant_id", name="uq_expense_participant"),
    )

    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey("expenses.id"), nullable=False, index=True)
    participant_id = db.Column(
        db.Integer,
        db.ForeignKey("participants.id"),
        nullable=False,
        index=True,
    )
    divided_amount = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    expense = db.relationship("Expense", back_populates="participant_shares")
    participant = db.relationship("Participant", back_populates="expense_shares")

    def __repr__(self) -> str:
        return (
            f"<ExpenseParticipant expense_id={self.expense_id} "
            f"participant_id={self.participant_id}>"
        )
