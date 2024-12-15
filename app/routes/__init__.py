from app.routes.auth import bp as auth_bp
from app.routes.user import bp as user_bp
from app.routes.admin import bp as admin_bp
from app.routes.job import bp as job_bp

__all__ = ['auth_bp', 'user_bp', 'admin_bp', 'job_bp']
