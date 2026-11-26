from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.token import Token
from app.schemas.user import UserRead
from app.api.deps import get_current_user, require_role

router = APIRouter()


@router.post("/login", response_model=Token, summary="OAuth2 Compatible Login")
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    OAuth2 compatible token login.
    Authenticates user with username (email) and password.
    Returns a cryptographically signed Bearer JWT token upon success.
    """
    email = form_data.username.strip().lower()
    user = db.query(User).filter(User.email == email).first()

    # Validate user existence and password hash
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    # Check if user account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account",
        )

    # Issue signed JWT Access Token
    access_token = create_access_token(
        subject=user.id,
        role=user.role.name if user.role else "USER",
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRead, summary="Get Current Authenticated User")
def read_current_user(current_user: User = Depends(get_current_user)) -> User:
    """Returns the profile information of the currently authenticated user."""
    return current_user


@router.get("/admin-only", summary="Admin Restricted Endpoint")
def admin_only_check(current_user: User = Depends(require_role(["ADMIN"]))):
    """Restricted endpoint accessible exclusively to administrators."""
    return {
        "message": "Welcome to the Administrative Control Console",
        "user_email": current_user.email,
        "role": current_user.role.name,
    }
