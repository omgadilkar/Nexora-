import pytest
from starlette.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.models.role import Role
from app.models.user import User
from app.core.security import get_password_hash, decode_access_token

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_users():
    """Sets up test roles and users for authentication testing."""
    db = SessionLocal()
    init_db(db)

    # Ensure roles exist
    admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
    if not admin_role:
        admin_role = Role(name="ADMIN", description="Administrator")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    # Create active user
    active_user = db.query(User).filter(User.email == "login.test@nexora.internal").first()
    if not active_user:
        active_user = User(
            email="login.test@nexora.internal",
            hashed_password=get_password_hash("ValidPassword123"),
            first_name="Active",
            last_name="Tester",
            role_id=admin_role.id,
            is_active=True,
        )
        db.add(active_user)
        db.commit()

    # Create inactive user
    inactive_user = db.query(User).filter(User.email == "inactive.test@nexora.internal").first()
    if not inactive_user:
        inactive_user = User(
            email="inactive.test@nexora.internal",
            hashed_password=get_password_hash("ValidPassword123"),
            first_name="Inactive",
            last_name="Tester",
            role_id=admin_role.id,
            is_active=False,
        )
        db.add(inactive_user)
        db.commit()

    db.close()


def test_successful_login(setup_users):
    """Verify that valid credentials return 200 with JWT access token."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "login.test@nexora.internal", "password": "ValidPassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Decode and verify token
    payload = decode_access_token(data["access_token"])
    assert payload is not None
    assert payload["role"] == "ADMIN"


def test_login_incorrect_password(setup_users):
    """Verify that wrong password returns 400 Bad Request."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "login.test@nexora.internal", "password": "WrongPassword999"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_nonexistent_email(setup_users):
    """Verify that non-existent email returns 400 Bad Request."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "doesnotexist@nexora.internal", "password": "SomePassword123"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_inactive_account(setup_users):
    """Verify that inactive accounts cannot log in."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "inactive.test@nexora.internal", "password": "ValidPassword123"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Inactive user account"
