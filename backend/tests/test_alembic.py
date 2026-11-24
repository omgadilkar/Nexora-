import os
from pathlib import Path
from alembic.config import Config
from alembic import command
from app.db.init_db import init_db
from app.db.session import SessionLocal


def test_alembic_config_loading():
    """Verify alembic.ini exists and loads configuration cleanly."""
    ini_path = Path("backend/alembic.ini")
    assert ini_path.exists(), "alembic.ini must exist in backend folder"

    cfg = Config(str(ini_path))
    script_loc = cfg.get_main_option("script_location")
    assert script_loc == "alembic"


def test_init_db_helper():
    """Verify init_db creates all registered tables without error."""
    db = SessionLocal()
    try:
        init_db(db)
        assert True
    finally:
        db.close()
