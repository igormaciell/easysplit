from datetime import UTC, datetime

from extensions import db


class Participant(db.Model):
    __tablename__ = "participants"
    __table_args__ = (
        db.UniqueConstraint("group_id", "nome", name="uq_participants_group_nome"),
    )

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    group = db.relationship("Group", back_populates="participants")
    user = db.relationship("User", back_populates="participants")
    paid_expenses = db.relationship(
        "Expense",
        back_populates="payer",
        foreign_keys="Expense.payer_participant_id",
    )
    expense_shares = db.relationship(
        "ExpenseParticipant",
        back_populates="participant",
        cascade="all, delete-orphan",
    )

    def has_expense_history(self) -> bool:
        return bool(self.paid_expenses or self.expense_shares)

    def __repr__(self) -> str:
        return f"<Participant id={self.id} nome='{self.nome}'>"
