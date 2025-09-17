"""User entity representing the domain model for a user."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    """User entity representing a user in the system."""

    id: str
    email: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[dict] = None
    is_email_confirmed: bool = False
    last_login: Optional[datetime] = None

    @classmethod
    def create(cls, email: str, metadata: Optional[dict] = None) -> "User":
        """Create a new user instance with generated ID and timestamps."""
        now = datetime.now()
        return cls(
            id=str(uuid.uuid4()),
            email=email,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
            is_email_confirmed=False,
            last_login=None
        )

    def update_metadata(self, metadata: dict) -> None:
        """Update user metadata and refresh updated_at timestamp."""
        self.metadata = {**(self.metadata or {}), **metadata}
        self.updated_at = datetime.now()

    def confirm_email(self) -> None:
        """Mark user email as confirmed."""
        self.is_email_confirmed = True
        self.updated_at = datetime.now()

    def record_login(self) -> None:
        """Record user login timestamp."""
        self.last_login = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert user to dictionary representation."""
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
            "is_email_confirmed": self.is_email_confirmed,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create user instance from dictionary."""
        return cls(
            id=data["id"],
            email=data["email"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            metadata=data.get("metadata"),
            is_email_confirmed=data.get("is_email_confirmed", False),
            last_login=datetime.fromisoformat(data["last_login"]) if data.get("last_login") else None
        )