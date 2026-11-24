import pytest
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserRead
from app.db.session import SessionLocal
from app.db.init_db import init_db


@pytest.fixture(scope="module")
def db():
    """Provides a fresh database session for testing."""
    session = SessionLocal()
    init_db(session)
    yield session
    session.close()


def test_password_hashing():
    """Verify password hashing and verification with bcrypt."""
    password = "SuperSecretPassword123"
    hashed = get_password_hash(password)

    assert hashed != password
    assert hashed.startswith("$2b$")
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_role_and_user_creation(db: Session):
    """Verify creating a Role and User with relationships in database."""
    # Create or fetch role
    role = db.query(Role).filter(Role.name == "ADMIN").first()
    if not role:
        role = Role(name="ADMIN", description="Administrator with full privileges")
        db.add(role)
        db.commit()
        db.refresh(role)

    assert role.id is not None
    assert role.name == "ADMIN"

    # Create user linked to role
    email = "admin.test@nexora.internal"
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            hashed_password=get_password_hash("AdminPass123"),
            first_name="Marcus",
            last_name="Vance",
            phone_number="+1-555-0199",
            role_id=role.id,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    assert user.id is not None
    assert user.email == email
    assert user.role.name == "ADMIN"
    assert verify_password("AdminPass123", user.hashed_password) is True

    # Verify Pydantic UserRead schema serialization
    user_dto = UserRead.model_validate(user)
    assert user_dto.id == user.id
    assert user_dto.email == email
    assert not hasattr(user_dto, "hashed_password")  # Password must never leak
