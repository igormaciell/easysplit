from datetime import UTC, datetime

from extensions import db


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    owner = db.relationship("User", back_populates="groups")
    participants = db.relationship(
        "Participant",
        back_populates="group",
        cascade="all, delete-orphan",
        order_by="Participant.nome",
    )
    expenses = db.relationship(
        "Expense",
        back_populates="group",
        cascade="all, delete-orphan",
        order_by="Expense.expense_date.desc(), Expense.created_at.desc()",
    )
    invitations = db.relationship(
        "GroupInvitation",
        back_populates="group",
        cascade="all, delete-orphan",
        order_by="GroupInvitation.created_at.desc()",
    )

    def __repr__(self) -> str:
        return f"<Group id={self.id} nome='{self.nome}'>"
