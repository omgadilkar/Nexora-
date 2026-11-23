import pytest
from sqlalchemy import text, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import engine, get_db
from app.db.base_class import Base


class SampleItem(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))


def test_database_connection():
    """Verify engine can connect and execute a ping query."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_base_model_tablename_generation():
    """Verify automatic snake_case plural table name generation."""
    assert SampleItem.__tablename__ == "sample_items"
    assert hasattr(SampleItem, "created_at")
    assert hasattr(SampleItem, "updated_at")


def test_get_db_session():
    """Verify get_db generator yields an active session and closes cleanly."""
    gen = get_db()
    db = next(gen)
    assert db.is_active
    try:
        res = db.execute(text("SELECT 1"))
        assert res.scalar() == 1
    finally:
        # Advance generator to trigger 'finally: db.close()'
        try:
            next(gen)
        except StopIteration:
            pass
