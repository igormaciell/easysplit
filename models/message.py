from datetime import UTC, datetime

from extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    group = db.relationship("Group", back_populates="messages")
    user = db.relationship("User", back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message id={self.id} group_id={self.group_id}>"
