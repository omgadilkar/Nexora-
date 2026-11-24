# Central model registry for Alembic and SQLAlchemy
from app.db.base_class import Base
from app.models.role import Role
from app.models.user import User

__all__ = ["Base", "Role", "User"]
