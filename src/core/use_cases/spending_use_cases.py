"""Use cases for spending-related business operations."""

from datetime import datetime
from typing import List, Optional
from core.entities.spending import Spending
from core.repositories.spending_repository import SpendingRepository
from core.exceptions.spending_exceptions import (
    SpendingNotFoundError,
    InvalidSpendingDataError,
    UnauthorizedSpendingAccessError
)


class SpendingUseCases:
    """Business logic for spending operations."""

    def __init__(self, spending_repository: SpendingRepository):
        self._repository = spending_repository

    async def add_spending(
        self,
        user_id: str,
        store: str,
        product: str,
        amount: int,
        price: float,
        date: Optional[datetime] = None,
        category: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Spending:
        """Add a new spending record for a user."""
        spending = Spending.create(
            user_id=user_id,
            store=store,
            product=product,
            amount=amount,
            price=price,
            date=date,
            category=category,
            notes=notes
        )

        if not spending.is_valid():
            raise InvalidSpendingDataError("Invalid spending data provided")

        return await self._repository.save(spending)

    async def get_spending_by_id(self, item_id: str, user_id: str) -> Spending:
        """Get spending record by ID, ensuring user owns the record."""
        spending = await self._repository.find_by_id(item_id)

        if not spending:
            raise SpendingNotFoundError(f"Spending record {item_id} not found")

        if spending.user_id != user_id:
            raise UnauthorizedSpendingAccessError("User does not have access to this spending record")

        return spending

    async def get_user_spendings(
        self,
        user_id: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Get all spending records for a user."""
        return await self._repository.find_by_user_id(user_id, limit, offset)

    async def get_spendings_by_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Get spending records for a user within a date range."""
        return await self._repository.find_by_user_and_date_range(
            user_id, start_date, end_date, limit, offset
        )

    async def get_spendings_by_category(
        self,
        user_id: str,
        category: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Get spending records for a user by category."""
        return await self._repository.find_by_user_and_category(
            user_id, category, limit, offset
        )

    async def update_spending(
        self,
        item_id: str,
        user_id: str,
        store: Optional[str] = None,
        product: Optional[str] = None,
        amount: Optional[int] = None,
        price: Optional[float] = None,
        date: Optional[datetime] = None,
        category: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Spending:
        """Update an existing spending record."""
        spending = await self.get_spending_by_id(item_id, user_id)

        spending.update(
            store=store,
            product=product,
            amount=amount,
            price=price,
            date=date,
            category=category,
            notes=notes
        )

        if not spending.is_valid():
            raise InvalidSpendingDataError("Invalid spending data provided")

        return await self._repository.save(spending)

    async def delete_spending(self, item_id: str, user_id: str) -> bool:
        """Delete a spending record, ensuring user owns the record."""
        # Verify ownership before deletion
        await self.get_spending_by_id(item_id, user_id)
        return await self._repository.delete(item_id)

    async def get_spending_summary(self, user_id: str) -> dict:
        """Get spending summary for a user."""
        total_amount = await self._repository.sum_by_user_id(user_id)
        total_count = await self._repository.count_by_user_id(user_id)
        categories = await self._repository.get_categories_by_user_id(user_id)
        stores = await self._repository.get_stores_by_user_id(user_id)

        return {
            "total_amount": total_amount,
            "total_count": total_count,
            "categories": categories,
            "stores": stores,
            "average_spending": total_amount / total_count if total_count > 0 else 0
        }

    async def get_spending_summary_by_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get spending summary for a user within a date range."""
        total_amount = await self._repository.sum_by_user_and_date_range(
            user_id, start_date, end_date
        )
        spendings = await self._repository.find_by_user_and_date_range(
            user_id, start_date, end_date
        )

        return {
            "total_amount": total_amount,
            "total_count": len(spendings),
            "average_spending": total_amount / len(spendings) if spendings else 0,
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            }
        }

    async def get_category_summary(self, user_id: str) -> dict:
        """Get spending summary grouped by category."""
        categories = await self._repository.get_categories_by_user_id(user_id)

        category_summary = {}
        for category in categories:
            if category:  # Skip None categories
                total = await self._repository.sum_by_user_and_category(user_id, category)
                category_summary[category] = total

        return category_summary