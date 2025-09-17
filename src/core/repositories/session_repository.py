"""Session repository interface defining data access operations for user sessions."""

from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.session import Session


class SessionRepository(ABC):
    """Abstract repository interface for session data operations."""

    @abstractmethod
    async def save(self, session: Session) -> Session:
        """Save or update a session record."""
        pass

    @abstractmethod
    async def find_by_id(self, session_id: str) -> Optional[Session]:
        """Find session by ID."""
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Session]:
        """Find all sessions for a user."""
        pass

    @abstractmethod
    async def find_active_by_user_id(self, user_id: str) -> List[Session]:
        """Find all active sessions for a user."""
        pass

    @abstractmethod
    async def find_by_access_token(self, access_token: str) -> Optional[Session]:
        """Find session by access token."""
        pass

    @abstractmethod
    async def find_by_refresh_token(self, refresh_token: str) -> Optional[Session]:
        """Find session by refresh token."""
        pass

    @abstractmethod
    async def invalidate(self, session_id: str) -> bool:
        """Invalidate a session by ID."""
        pass

    @abstractmethod
    async def invalidate_all_by_user_id(self, user_id: str) -> int:
        """Invalidate all sessions for a user. Returns count of invalidated sessions."""
        pass

    @abstractmethod
    async def delete_expired(self) -> int:
        """Delete all expired sessions. Returns count of deleted sessions."""
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: str) -> int:
        """Delete all sessions for a user. Returns count of deleted sessions."""
        pass

    @abstractmethod
    async def update_last_accessed(self, session_id: str) -> bool:
        """Update last accessed timestamp for a session."""
        pass

    @abstractmethod
    async def refresh_access_token(
        self,
        session_id: str,
        new_access_token: str,
        expires_in_seconds: int = 3600
    ) -> bool:
        """Refresh session access token and expiration."""
        pass