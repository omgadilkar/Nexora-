from sqlalchemy.orm import Session
from app.db.base_class import Base
from app.db.session import engine


def init_db(db: Session) -> None:
    """
    Initializes tables and seeds initial administrative fixtures.
    In production, tables are created via Alembic migrations.
    This helper is used for automated test suites and local sandboxing.
    """
    Base.metadata.create_all(bind=engine)
