from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from extensions import db
from forms import EmptyForm
from models import Notification


notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")


@notifications_bp.get("/")
@login_required
def index():
    notifications = (
        Notification.query.filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )
    return render_template(
        "notifications/index.html",
        notifications=notifications,
        form=EmptyForm(),
        title="Notificações",
    )


@notifications_bp.post("/<int:notification_id>/read")
@login_required
def mark_read(notification_id: int):
    notification = Notification.query.filter_by(
        id=notification_id, user_id=current_user.id
    ).first_or_404()
    notification.is_read = True
    db.session.commit()
    if notification.link:
        return redirect(notification.link)
    return redirect(url_for("notifications.index"))


@notifications_bp.post("/read-all")
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update(
        {"is_read": True}
    )
    db.session.commit()
    flash("Todas as notificações foram marcadas como lidas.", "success")
    return redirect(url_for("notifications.index"))


def create_notification(user_id: int, type: str, title: str, body: str = "", link: str = "") -> Notification:
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        body=body,
        link=link,
    )
    db.session.add(notification)
    return notification
