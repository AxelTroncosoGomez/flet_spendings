"""Concrete implementation of UserRepository using Supabase."""

from typing import List, Optional
from datetime import datetime
from supabase import Client

from core.entities.user import User
from core.repositories.user_repository import UserRepository
from core.exceptions.auth_exceptions import UserNotFoundError


class SupabaseUserRepository(UserRepository):
    """Supabase implementation of the UserRepository interface."""

    def __init__(self, supabase_client: Client):
        self._client = supabase_client

    async def save(self, user: User) -> User:
        """Save or update a user record."""
        user_data = {
            "id": user.id,
            "email": user.email,
            "metadata": user.metadata,
            "is_email_confirmed": user.is_email_confirmed,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "updated_at": datetime.utcnow().isoformat()
        }

        # Try to update first, then insert if not exists
        try:
            result = self._client.table("users").upsert(user_data).execute()
            data = result.data[0] if result.data else user_data
            return self._map_to_entity(data)
        except Exception as e:
            raise Exception(f"Failed to save user: {str(e)}")

    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID."""
        try:
            result = self._client.table("users").select("*").eq("id", user_id).execute()
            if result.data:
                return self._map_to_entity(result.data[0])
            return None
        except Exception:
            return None

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email address."""
        try:
            result = self._client.table("users").select("*").eq("email", email).execute()
            if result.data:
                return self._map_to_entity(result.data[0])
            return None
        except Exception:
            return None

    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email address."""
        try:
            result = self._client.table("users").select("id").eq("email", email).execute()
            return len(result.data) > 0
        except Exception:
            return False

    async def delete(self, user_id: str) -> bool:
        """Delete user by ID."""
        try:
            result = self._client.table("users").delete().eq("id", user_id).execute()
            return len(result.data) > 0
        except Exception:
            return False

    async def list_all(self, limit: Optional[int] = None, offset: int = 0) -> List[User]:
        """List all users with optional pagination."""
        try:
            query = self._client.table("users").select("*")
            if limit:
                query = query.limit(limit).offset(offset)

            result = query.execute()
            return [self._map_to_entity(data) for data in result.data]
        except Exception:
            return []

    async def count(self) -> int:
        """Count total number of users."""
        try:
            result = self._client.table("users").select("id", count="exact").execute()
            return result.count or 0
        except Exception:
            return 0

    async def update_metadata(self, user_id: str, metadata: dict) -> bool:
        """Update user metadata."""
        try:
            result = self._client.table("users").update({
                "metadata": metadata,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", user_id).execute()
            return len(result.data) > 0
        except Exception:
            return False

    async def confirm_email(self, user_id: str) -> bool:
        """Mark user email as confirmed."""
        try:
            result = self._client.table("users").update({
                "is_email_confirmed": True,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", user_id).execute()
            return len(result.data) > 0
        except Exception:
            return False

    async def record_login(self, user_id: str) -> bool:
        """Record user login timestamp."""
        try:
            result = self._client.table("users").update({
                "last_login": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", user_id).execute()
            return len(result.data) > 0
        except Exception:
            return False

    def _map_to_entity(self, data: dict) -> User:
        """Map database record to User entity."""
        return User(
            id=data["id"],
            email=data["email"],
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00")),
            metadata=data.get("metadata"),
            is_email_confirmed=data.get("is_email_confirmed", False),
            last_login=datetime.fromisoformat(data["last_login"].replace("Z", "+00:00")) if data.get("last_login") else None
        )