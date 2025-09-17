"""Spending service implementation using clean architecture."""

from typing import List, Optional
from datetime import datetime

from core.entities.spending import Spending
from core.use_cases.spending_use_cases import SpendingUseCases


class SpendingService:
    """High-level spending service using clean architecture patterns."""

    def __init__(self, spending_use_cases: SpendingUseCases):
        self._spending_use_cases = spending_use_cases

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
        """Add a new spending record."""
        return await self._spending_use_cases.add_spending(
            user_id=user_id,
            store=store,
            product=product,
            amount=amount,
            price=price,
            date=date,
            category=category,
            notes=notes
        )

    async def get_spending(self, item_id: str, user_id: str) -> Spending:
        """Get spending record by ID."""
        return await self._spending_use_cases.get_spending_by_id(item_id, user_id)

    async def get_user_spendings(
        self,
        user_id: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Get all spending records for a user."""
        return await self._spending_use_cases.get_user_spendings(
            user_id=user_id,
            limit=limit,
            offset=offset
        )

    async def get_spendings_by_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Get spending records within a date range."""
        return await self._spending_use_cases.get_spendings_by_date_range(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )

    async def get_spendings_by_category(
        self,
        user_id: str,
        category: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Get spending records by category."""
        return await self._spending_use_cases.get_spendings_by_category(
            user_id=user_id,
            category=category,
            limit=limit,
            offset=offset
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
        return await self._spending_use_cases.update_spending(
            item_id=item_id,
            user_id=user_id,
            store=store,
            product=product,
            amount=amount,
            price=price,
            date=date,
            category=category,
            notes=notes
        )

    async def delete_spending(self, item_id: str, user_id: str) -> bool:
        """Delete a spending record."""
        return await self._spending_use_cases.delete_spending(item_id, user_id)

    async def get_spending_summary(self, user_id: str) -> dict:
        """Get spending summary for a user."""
        return await self._spending_use_cases.get_spending_summary(user_id)

    async def get_spending_summary_by_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get spending summary within a date range."""
        return await self._spending_use_cases.get_spending_summary_by_date_range(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

    async def get_category_summary(self, user_id: str) -> dict:
        """Get spending summary grouped by category."""
        return await self._spending_use_cases.get_category_summary(user_id)

    async def get_available_categories(self, user_id: str) -> List[str]:
        """Get all categories used by a user."""
        summary = await self._spending_use_cases.get_spending_summary(user_id)
        return summary.get("categories", [])

    async def get_available_stores(self, user_id: str) -> List[str]:
        """Get all stores used by a user."""
        summary = await self._spending_use_cases.get_spending_summary(user_id)
        return summary.get("stores", [])

    async def get_monthly_spending_trends(self, user_id: str, months: int = 12) -> dict:
        """Get monthly spending trends for visualization."""
        from dateutil.relativedelta import relativedelta

        end_date = datetime.now()
        start_date = end_date - relativedelta(months=months)

        monthly_data = {}
        current_date = start_date

        while current_date <= end_date:
            month_start = current_date.replace(day=1)
            month_end = (month_start + relativedelta(months=1)) - relativedelta(days=1)

            summary = await self._spending_use_cases.get_spending_summary_by_date_range(
                user_id=user_id,
                start_date=month_start,
                end_date=month_end
            )

            month_key = current_date.strftime("%Y-%m")
            monthly_data[month_key] = {
                "total_amount": summary["total_amount"],
                "total_count": summary["total_count"],
                "average_spending": summary["average_spending"]
            }

            current_date += relativedelta(months=1)

        return monthly_data