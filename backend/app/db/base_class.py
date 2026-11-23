from datetime import datetime
from typing import Any
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    id: Any
    __name__: str

    # Automatically generate __tablename__ in lowercase pluralized convention
    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__
        # Convert PascalCase to snake_case
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        snake = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        if not snake.endswith('s'):
            return f"{snake}s"
        return snake

    # Common audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
