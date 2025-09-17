"""Concrete implementation of SpendingRepository using Supabase."""

from typing import List, Optional
from datetime import datetime
from supabase import Client

from core.entities.spending import Spending
from core.repositories.spending_repository import SpendingRepository


class SupabaseSpendingRepository(SpendingRepository):
    """Supabase implementation of the SpendingRepository interface."""

    def __init__(self, supabase_client: Client):
        self._client = supabase_client

    async def save(self, spending: Spending) -> Spending:
        """Save or update a spending record."""
        spending_data = {
            "item_id": spending.item_id,
            "user_id": spending.user_id,
            "date": spending.date.isoformat(),
            "store": spending.store,
            "product": spending.product,
            "amount": spending.amount,
            "price": spending.price,
            "category": spending.category,
            "notes": spending.notes,
            "updated_at": datetime.utcnow().isoformat()
        }

        try:
            result = self._client.table("spendings").upsert(spending_data).execute()
            data = result.data[0] if result.data else spending_data
            return self._map_to_entity(data)
        except Exception as e:
            raise Exception(f"Failed to save spending: {str(e)}")

    async def find_by_id(self, item_id: str) -> Optional[Spending]:
        """Find spending record by ID."""
        try:
            result = self._client.table("spendings").select("*").eq("item_id", item_id).execute()
            if result.data:
                return self._map_to_entity(result.data[0])
            return None
        except Exception:
            return None

    async def find_by_user_id(
        self,
        user_id: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Find all spending records for a user with optional pagination."""
        try:
            query = self._client.table("spendings").select("*").eq("user_id", user_id).order("date", desc=True)

            if limit:
                query = query.limit(limit).offset(offset)

            result = query.execute()
            return [self._map_to_entity(data) for data in result.data]
        except Exception:
            return []

    async def find_by_user_and_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Find spending records for a user within a date range."""
        try:
            query = (self._client.table("spendings")
                    .select("*")
                    .eq("user_id", user_id)
                    .gte("date", start_date.isoformat())
                    .lte("date", end_date.isoformat())
                    .order("date", desc=True))

            if limit:
                query = query.limit(limit).offset(offset)

            result = query.execute()
            return [self._map_to_entity(data) for data in result.data]
        except Exception:
            return []

    async def find_by_user_and_category(
        self,
        user_id: str,
        category: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Spending]:
        """Find spending records for a user by category."""
        try:
            query = (self._client.table("spendings")
                    .select("*")
                    .eq("user_id", user_id)
                    .eq("category", category)
                    .order("date", desc=True))

            if limit:
                query = query.limit(limit).offset(offset)

            result = query.execute()
            return [self._map_to_entity(data) for data in result.data]
        except Exception:
            return []

    async def delete(self, item_id: str) -> bool:
        """Delete spending record by ID."""
        try:
            result = self._client.table("spendings").delete().eq("item_id", item_id).execute()
            return len(result.data) > 0
        except Exception:
            return False

    async def delete_by_user_id(self, user_id: str) -> int:
        """Delete all spending records for a user. Returns count of deleted records."""
        try:
            result = self._client.table("spendings").delete().eq("user_id", user_id).execute()
            return len(result.data)
        except Exception:
            return 0

    async def count_by_user_id(self, user_id: str) -> int:
        """Count total spending records for a user."""
        try:
            result = (self._client.table("spendings")
                     .select("item_id", count="exact")
                     .eq("user_id", user_id)
                     .execute())
            return result.count or 0
        except Exception:
            return 0

    async def sum_by_user_id(self, user_id: str) -> float:
        """Calculate total spending amount for a user."""
        try:
            result = self._client.table("spendings").select("price").eq("user_id", user_id).execute()
            return sum(float(record["price"]) for record in result.data)
        except Exception:
            return 0.0

    async def sum_by_user_and_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> float:
        """Calculate total spending amount for a user within a date range."""
        try:
            result = (self._client.table("spendings")
                     .select("price")
                     .eq("user_id", user_id)
                     .gte("date", start_date.isoformat())
                     .lte("date", end_date.isoformat())
                     .execute())
            return sum(float(record["price"]) for record in result.data)
        except Exception:
            return 0.0

    async def sum_by_user_and_category(self, user_id: str, category: str) -> float:
        """Calculate total spending amount for a user by category."""
        try:
            result = (self._client.table("spendings")
                     .select("price")
                     .eq("user_id", user_id)
                     .eq("category", category)
                     .execute())
            return sum(float(record["price"]) for record in result.data)
        except Exception:
            return 0.0

    async def get_categories_by_user_id(self, user_id: str) -> List[str]:
        """Get unique categories used by a user."""
        try:
            result = (self._client.table("spendings")
                     .select("category")
                     .eq("user_id", user_id)
                     .execute())
            categories = list(set(record["category"] for record in result.data if record["category"]))
            return sorted(categories)
        except Exception:
            return []

    async def get_stores_by_user_id(self, user_id: str) -> List[str]:
        """Get unique stores used by a user."""
        try:
            result = (self._client.table("spendings")
                     .select("store")
                     .eq("user_id", user_id)
                     .execute())
            stores = list(set(record["store"] for record in result.data if record["store"]))
            return sorted(stores)
        except Exception:
            return []

    def _map_to_entity(self, data: dict) -> Spending:
        """Map database record to Spending entity."""
        return Spending(
            item_id=data["item_id"],
            user_id=data["user_id"],
            date=datetime.fromisoformat(data["date"].replace("Z", "+00:00")),
            store=data["store"],
            product=data["product"],
            amount=data["amount"],
            price=float(data["price"]),
            category=data.get("category"),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
        )