from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Token response schema returned upon successful authentication."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Internal decoded JWT payload structure."""
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None
