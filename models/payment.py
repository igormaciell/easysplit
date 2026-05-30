from datetime import UTC, datetime

from extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False, index=True)
    payer_participant_id = db.Column(
        db.Integer,
        db.ForeignKey("participants.id"),
        nullable=False,
        index=True,
    )
    receiver_participant_id = db.Column(
        db.Integer,
        db.ForeignKey("participants.id"),
        nullable=False,
        index=True,
    )
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    note = db.Column(db.String(200), default="")
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    group = db.relationship("Group", back_populates="payments")
    payer = db.relationship(
        "Participant",
        foreign_keys=[payer_participant_id],
        backref="payments_made",
    )
    receiver = db.relationship(
        "Participant",
        foreign_keys=[receiver_participant_id],
        backref="payments_received",
    )

    def __repr__(self) -> str:
        return f"<Payment id={self.id} amount={self.amount}>"
