"""Spending entity representing the domain model for a spending record."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Spending:
    """Spending entity representing a spending record in the system."""

    item_id: str
    user_id: str
    date: datetime
    store: str
    product: str
    amount: int
    price: float
    created_at: datetime
    updated_at: datetime
    category: Optional[str] = None
    notes: Optional[str] = None

    @classmethod
    def create(
        cls,
        user_id: str,
        store: str,
        product: str,
        amount: int,
        price: float,
        date: Optional[datetime] = None,
        category: Optional[str] = None,
        notes: Optional[str] = None
    ) -> "Spending":
        """Create a new spending instance with generated ID and timestamps."""
        now = datetime.now()
        spending_date = date or now

        return cls(
            item_id=str(uuid.uuid4()),
            user_id=user_id,
            date=spending_date,
            store=store,
            product=product,
            amount=amount,
            price=price,
            category=category,
            notes=notes,
            created_at=now,
            updated_at=now
        )

    @property
    def total_cost(self) -> float:
        """Calculate total cost (amount * price)."""
        return self.amount * self.price

    def update(
        self,
        store: Optional[str] = None,
        product: Optional[str] = None,
        amount: Optional[int] = None,
        price: Optional[float] = None,
        date: Optional[datetime] = None,
        category: Optional[str] = None,
        notes: Optional[str] = None
    ) -> None:
        """Update spending record with new values."""
        if store is not None:
            self.store = store
        if product is not None:
            self.product = product
        if amount is not None:
            self.amount = amount
        if price is not None:
            self.price = price
        if date is not None:
            self.date = date
        if category is not None:
            self.category = category
        if notes is not None:
            self.notes = notes

        self.updated_at = datetime.now()

    def is_valid(self) -> bool:
        """Validate spending record integrity."""
        return (
            self.amount > 0 and
            self.price >= 0 and
            len(self.store.strip()) > 0 and
            len(self.product.strip()) > 0 and
            len(self.user_id.strip()) > 0
        )

    def to_dict(self) -> dict:
        """Convert spending to dictionary representation."""
        return {
            "item_id": self.item_id,
            "user_id": self.user_id,
            "date": self.date.isoformat(),
            "store": self.store,
            "product": self.product,
            "amount": self.amount,
            "price": self.price,
            "category": self.category,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "total_cost": self.total_cost
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Spending":
        """Create spending instance from dictionary."""
        return cls(
            item_id=data["item_id"],
            user_id=data["user_id"],
            date=datetime.fromisoformat(data["date"]),
            store=data["store"],
            product=data["product"],
            amount=data["amount"],
            price=data["price"],
            category=data.get("category"),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )