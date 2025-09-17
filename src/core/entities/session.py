"""Session entity representing user authentication session."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
import uuid


@dataclass
class Session:
    """Session entity representing an authenticated user session."""

    session_id: str
    user_id: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    created_at: datetime
    last_accessed: datetime
    is_active: bool = True

    @classmethod
    def create(
        cls,
        user_id: str,
        access_token: str,
        refresh_token: str,
        expires_in_seconds: int = 3600
    ) -> "Session":
        """Create a new session instance."""
        now = datetime.now()
        expires_at = now + timedelta(seconds=expires_in_seconds)

        return cls(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            created_at=now,
            last_accessed=now,
            is_active=True
        )

    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.now() > self.expires_at

    def is_valid(self) -> bool:
        """Check if session is valid (active and not expired)."""
        return self.is_active and not self.is_expired()

    def refresh_access(self, new_access_token: str, expires_in_seconds: int = 3600) -> None:
        """Refresh the session with new access token."""
        self.access_token = new_access_token
        self.expires_at = datetime.now() + timedelta(seconds=expires_in_seconds)
        self.last_accessed = datetime.now()

    def update_last_accessed(self) -> None:
        """Update last accessed timestamp."""
        self.last_accessed = datetime.now()

    def invalidate(self) -> None:
        """Invalidate the session."""
        self.is_active = False

    def extend_expiration(self, additional_seconds: int) -> None:
        """Extend session expiration time."""
        self.expires_at += timedelta(seconds=additional_seconds)

    def to_dict(self) -> dict:
        """Convert session to dictionary representation."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "is_active": self.is_active,
            "is_expired": self.is_expired(),
            "is_valid": self.is_valid()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        """Create session instance from dictionary."""
        return cls(
            session_id=data["session_id"],
            user_id=data["user_id"],
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=datetime.fromisoformat(data["expires_at"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            last_accessed=datetime.fromisoformat(data["last_accessed"]),
            is_active=data.get("is_active", True)
        )