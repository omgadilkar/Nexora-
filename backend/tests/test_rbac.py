import pytest
from starlette.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.models.role import Role
from app.models.user import User
from app.core.security import get_password_hash, create_access_token

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_rbac_users():
    """Seeds test Admin and Student users for RBAC route protection tests."""
    db = SessionLocal()
    init_db(db)

    # Admin role & user
    admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
    if not admin_role:
        admin_role = Role(name="ADMIN", description="Administrator")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    admin_user = db.query(User).filter(User.email == "admin.rbac@nexora.internal").first()
    if not admin_user:
        admin_user = User(
            email="admin.rbac@nexora.internal",
            hashed_password=get_password_hash("AdminPass123"),
            first_name="Admin",
            last_name="Super",
            role_id=admin_role.id,
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

    # Student role & user
    student_role = db.query(Role).filter(Role.name == "STUDENT").first()
    if not student_role:
        student_role = Role(name="STUDENT", description="Student")
        db.add(student_role)
        db.commit()
        db.refresh(student_role)

    student_user = db.query(User).filter(User.email == "student.rbac@nexora.internal").first()
    if not student_user:
        student_user = User(
            email="student.rbac@nexora.internal",
            hashed_password=get_password_hash("StudentPass123"),
            first_name="Alex",
            last_name="Hayes",
            role_id=student_role.id,
            is_active=True,
        )
        db.add(student_user)
        db.commit()
        db.refresh(student_user)

    admin_token = create_access_token(subject=admin_user.id, role=admin_role.name)
    student_token = create_access_token(subject=student_user.id, role=student_role.name)

    db.close()
    return {
        "admin_token": admin_token,
        "student_token": student_token,
        "admin_user": admin_user,
        "student_user": student_user,
    }


def test_get_current_user_with_valid_token(setup_rbac_users):
    """Verify /me returns current user profile with valid token."""
    token = setup_rbac_users["student_token"]
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "student.rbac@nexora.internal"
    assert data["first_name"] == "Alex"
    assert not hasattr(data, "hashed_password")


def test_get_current_user_unauthorized():
    """Verify /me rejects request without token with 401."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_admin_only_endpoint_permitted(setup_rbac_users):
    """Verify /admin-only allows Admin role with 200."""
    token = setup_rbac_users["admin_token"]
    response = client.get("/api/v1/auth/admin-only", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["role"] == "ADMIN"


def test_admin_only_endpoint_forbidden_for_student(setup_rbac_users):
    """Verify /admin-only blocks Student role with 403 Forbidden."""
    token = setup_rbac_users["student_token"]
    response = client.get("/api/v1/auth/admin-only", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert "Access forbidden" in response.json()["detail"]
