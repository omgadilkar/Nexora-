from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Shared user properties."""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=64)
    last_name: str = Field(..., min_length=1, max_length=64)
    phone_number: Optional[str] = Field(None, max_length=20)
    is_active: bool = True


class UserCreate(UserBase):
    """Properties required when creating a new user."""
    password: str = Field(..., min_length=6, max_length=128)
    role_id: int


class UserUpdate(BaseModel):
    """Properties for updating user profile."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    """Properties returned over the API (never exposes hashed_password)."""
    id: int
    role_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
