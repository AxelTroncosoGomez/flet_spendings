"""Concrete implementation of SessionRepository using Supabase."""

from typing import List, Optional
from datetime import datetime, timedelta
from supabase import Client

from core.entities.session import Session
from core.repositories.session_repository import SessionRepository


class SupabaseSessionRepository(SessionRepository):
    """Supabase implementation of the SessionRepository interface."""

    def __init__(self, supabase_client: Client):
        self._client = supabase_client

    async def save(self, session: Session) -> Session:
        """Save or update a session record."""
        session_data = {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "expires_at": session.expires_at.isoformat(),
            "is_active": session.is_active,
            "last_accessed": session.last_accessed.isoformat() if session.last_accessed else None,
            "updated_at": datetime.utcnow().isoformat()
        }

        try:
            result = self._client.table("sessions").upsert(session_data).execute()
            data = result.data[0] if result.data else session_data
            return self._map_to_entity(data)
        except Exception as e:
            raise Exception(f"Failed to save session: {str(e)}")

    async def find_by_id(self, session_id: str) -> Optional[Session]:
        """Find session by ID."""
        try:
            result = self._client.table("sessions").select("*").eq("session_id", session_id).execute()
            if result.data:
                return self._map_to_entity(result.data[0])
            return None
        except Exception:
            return None

    async def find_by_user_id(self, user_id: str) -> List[Session]:
        """Find all sessions for a user."""
        try:
            result = (self._client.table("sessions")
                     .select("*")
                     .eq("user_id", user_id)
                     .order("created_at", desc=True)
                     .execute())
            return [self._map_to_entity(data) for data in result.data]
        except Exception:
            return []

    async def find_active_by_user_id(self, user_id: str) -> List[Session]:
        """Find all active sessions for a user."""
        try:
            result = (self._client.table("sessions")
                     .select("*")
                     .eq("user_id", user_id)
                     .eq("is_active", True)
                     .gt("expires_at", datetime.utcnow().isoformat())
                     .order("created_at", desc=True)
                     .execute())
            return [self._map_to_entity(data) for data in result.data]
        except Exception:
            return []

    async def find_by_access_token(self, access_token: str) -> Optional[Session]:
        """Find session by access token."""
        try:
            result = (self._client.table("sessions")
                     .select("*")
                     .eq("access_token", access_token)
                     .execute())
            if result.data:
                return self._map_to_entity(result.data[0])
            return None
        except Exception:
            return None

    async def find_by_refresh_token(self, refresh_token: str) -> Optional[Session]:
        """Find session by refresh token."""
        try:
            result = (self._client.table("sessions")
                     .select("*")
                     .eq("refresh_token", refresh_token)
                     .execute())
            if result.data:
                return self._map_to_entity(result.data[0])
            return None
        except Exception:
            return None

    async def invalidate(self, session_id: str) -> bool:
        """Invalidate a session by ID."""
        try:
            result = (self._client.table("sessions")
                     .update({
                         "is_active": False,
                         "updated_at": datetime.utcnow().isoformat()
                     })
                     .eq("session_id", session_id)
                     .execute())
            return len(result.data) > 0
        except Exception:
            return False

    async def invalidate_all_by_user_id(self, user_id: str) -> int:
        """Invalidate all sessions for a user. Returns count of invalidated sessions."""
        try:
            result = (self._client.table("sessions")
                     .update({
                         "is_active": False,
                         "updated_at": datetime.utcnow().isoformat()
                     })
                     .eq("user_id", user_id)
                     .eq("is_active", True)
                     .execute())
            return len(result.data)
        except Exception:
            return 0

    async def delete_expired(self) -> int:
        """Delete all expired sessions. Returns count of deleted sessions."""
        try:
            result = (self._client.table("sessions")
                     .delete()
                     .lt("expires_at", datetime.utcnow().isoformat())
                     .execute())
            return len(result.data)
        except Exception:
            return 0

    async def delete_by_user_id(self, user_id: str) -> int:
        """Delete all sessions for a user. Returns count of deleted sessions."""
        try:
            result = (self._client.table("sessions")
                     .delete()
                     .eq("user_id", user_id)
                     .execute())
            return len(result.data)
        except Exception:
            return 0

    async def update_last_accessed(self, session_id: str) -> bool:
        """Update last accessed timestamp for a session."""
        try:
            result = (self._client.table("sessions")
                     .update({
                         "last_accessed": datetime.utcnow().isoformat(),
                         "updated_at": datetime.utcnow().isoformat()
                     })
                     .eq("session_id", session_id)
                     .execute())
            return len(result.data) > 0
        except Exception:
            return False

    async def refresh_access_token(
        self,
        session_id: str,
        new_access_token: str,
        expires_in_seconds: int = 3600
    ) -> bool:
        """Refresh session access token and expiration."""
        try:
            new_expiry = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
            result = (self._client.table("sessions")
                     .update({
                         "access_token": new_access_token,
                         "expires_at": new_expiry.isoformat(),
                         "last_accessed": datetime.utcnow().isoformat(),
                         "updated_at": datetime.utcnow().isoformat()
                     })
                     .eq("session_id", session_id)
                     .execute())
            return len(result.data) > 0
        except Exception:
            return False

    def _map_to_entity(self, data: dict) -> Session:
        """Map database record to Session entity."""
        return Session(
            session_id=data["session_id"],
            user_id=data["user_id"],
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00")),
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00")),
            is_active=data.get("is_active", True),
            last_accessed=datetime.fromisoformat(data["last_accessed"].replace("Z", "+00:00")) if data.get("last_accessed") else None
        )