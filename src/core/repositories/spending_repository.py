"""Spending repository interface defining data access operations for spending records."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from core.entities.spending import Spending


class SpendingRepository(ABC):
    """Abstract repository interface for spending data operations."""

    @abstractmethod
    async def save(self, spending: Spending) -> Spending:
        """Save or update a spending record."""
        pass

    @abstractmethod
    async def find_by_id(self, item_id: str) -> Optional[Spending]:
        """Find spending record by ID."""
        pass

    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Find all spending records for a user with optional pagination."""
        pass

    @abstractmethod
    async def find_by_user_and_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Find spending records for a user within a date range."""
        pass

    @abstractmethod
    async def find_by_user_and_category(
        self,
        user_id: str,
        category: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Find spending records for a user by category."""
        pass

    @abstractmethod
    async def delete(self, item_id: str) -> bool:
        """Delete spending record by ID."""
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: str) -> int:
        """Delete all spending records for a user. Returns count of deleted records."""
        pass

    @abstractmethod
    async def count_by_user_id(self, user_id: str) -> int:
        """Count total spending records for a user."""
        pass

    @abstractmethod
    async def sum_by_user_id(self, user_id: str) -> float:
        """Calculate total spending amount for a user."""
        pass

    @abstractmethod
    async def sum_by_user_and_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> float:
        """Calculate total spending amount for a user within a date range."""
        pass

    @abstractmethod
    async def sum_by_user_and_category(self, user_id: str, category: str) -> float:
        """Calculate total spending amount for a user by category."""
        pass

    @abstractmethod
    async def get_categories_by_user_id(self, user_id: str) -> List[str]:
        """Get unique categories used by a user."""
        pass

    @abstractmethod
    async def get_stores_by_user_id(self, user_id: str) -> List[str]:
        """Get unique stores used by a user."""
        pass