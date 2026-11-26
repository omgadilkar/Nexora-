from datetime import timedelta
import time
import pytest
from app.core.security import create_access_token, decode_access_token
from app.schemas.token import TokenPayload


def test_create_and_decode_valid_access_token():
    """Verify generating and decoding a valid JWT access token."""
    user_id = 42
    role = "ADMIN"
    token = create_access_token(subject=user_id, role=role)

    assert isinstance(token, str)
    assert len(token) > 20

    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == str(user_id)
    assert payload["role"] == role
    assert "exp" in payload
    assert "iat" in payload

    # Verify against TokenPayload schema
    token_dto = TokenPayload(**payload)
    assert token_dto.sub == str(user_id)
    assert token_dto.role == role


def test_tampered_token_rejection():
    """Verify that modified or forged tokens fail verification."""
    token = create_access_token(subject=99, role="STUDENT")
    # Tamper with the token string
    tampered_token = token[:-4] + "abcd"

    payload = decode_access_token(tampered_token)
    assert payload is None


def test_expired_token_rejection():
    """Verify that expired tokens fail verification."""
    # Create token expired 5 seconds ago
    expired_delta = timedelta(seconds=-5)
    token = create_access_token(subject=100, role="TEACHER", expires_delta=expired_delta)

    payload = decode_access_token(token)
    assert payload is None
