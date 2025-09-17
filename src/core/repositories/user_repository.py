"""User repository interface defining data access operations for users."""

from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.user import User


class UserRepository(ABC):
    """Abstract repository interface for user data operations."""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save or update a user record."""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID."""
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email address."""
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email address."""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Delete user by ID."""
        pass

    @abstractmethod
    async def list_all(self, limit: Optional[int] = None, offset: int = 0) -> List[User]:
        """List all users with optional pagination."""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Count total number of users."""
        pass

    @abstractmethod
    async def update_metadata(self, user_id: str, metadata: dict) -> bool:
        """Update user metadata."""
        pass

    @abstractmethod
    async def confirm_email(self, user_id: str) -> bool:
        """Mark user email as confirmed."""
        pass

    @abstractmethod
    async def record_login(self, user_id: str) -> bool:
        """Record user login timestamp."""
        pass