from .auth import auth_bp
from .groups import groups_bp
from .notifications import notifications_bp
from .oauth import oauth_bp

__all__ = ["auth_bp", "groups_bp", "notifications_bp", "oauth_bp"]
