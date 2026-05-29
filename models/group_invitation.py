from datetime import UTC, datetime

from extensions import db


class GroupInvitation(db.Model):
    __tablename__ = "group_invitations"
    __table_args__ = (
        db.UniqueConstraint(
            "group_id",
            "invited_user_id",
            name="uq_group_invitation_group_user",
        ),
    )

    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_DECLINED = "declined"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False, index=True)
    invited_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default=STATUS_PENDING)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    responded_at = db.Column(db.DateTime)

    group = db.relationship("Group", back_populates="invitations")
    invited_user = db.relationship("User", foreign_keys=[invited_user_id])
    invited_by_user = db.relationship("User", foreign_keys=[invited_by_user_id])

    def __repr__(self) -> str:
        return (
            "<GroupInvitation "
            f"id={self.id} group_id={self.group_id} invited_user_id={self.invited_user_id} "
            f"status={self.status}>"
        )
