from datetime import UTC, datetime

from extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    TYPE_INVITE = "invite"
    TYPE_EXPENSE = "expense"
    TYPE_PAYMENT = "payment"
    TYPE_MESSAGE = "message"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    type = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(500), default="")
    link = db.Column(db.String(300), default="")
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    user = db.relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<Notification id={self.id} type='{self.type}' user_id={self.user_id}>"
