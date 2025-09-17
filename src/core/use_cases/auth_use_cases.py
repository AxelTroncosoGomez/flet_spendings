"""Use cases for authentication-related business operations."""

from datetime import datetime
from typing import Optional, Tuple
from core.entities.user import User
from core.entities.session import Session
from core.repositories.user_repository import UserRepository
from core.repositories.session_repository import SessionRepository
from core.exceptions.auth_exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    EmailNotConfirmedError,
    SessionExpiredError,
    InvalidSessionError
)


class AuthUseCases:
    """Business logic for authentication operations."""

    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository
    ):
        self._user_repository = user_repository
        self._session_repository = session_repository

    async def register_user(
        self,
        email: str,
        metadata: Optional[dict] = None
    ) -> User:
        """Register a new user."""
        # Check if user already exists
        if await self._user_repository.exists_by_email(email):
            raise UserAlreadyExistsError(f"User with email {email} already exists")

        # Create new user
        user = User.create(email=email, metadata=metadata)
        return await self._user_repository.save(user)

    async def login_user(
        self,
        email: str,
        access_token: str,
        refresh_token: str,
        require_email_confirmation: bool = True
    ) -> Tuple[User, Session]:
        """Login a user and create a session."""
        # Find user by email
        user = await self._user_repository.find_by_email(email)
        if not user:
            raise UserNotFoundError(f"User with email {email} not found")

        # Check email confirmation if required
        if require_email_confirmation and not user.is_email_confirmed:
            raise EmailNotConfirmedError("Email address must be confirmed before login")

        # Record login
        user.record_login()
        await self._user_repository.save(user)

        # Create session
        session = Session.create(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token
        )
        session = await self._session_repository.save(session)

        return user, session

    async def logout_user(self, session_id: str) -> bool:
        """Logout a user by invalidating their session."""
        return await self._session_repository.invalidate(session_id)

    async def logout_all_user_sessions(self, user_id: str) -> int:
        """Logout user from all sessions."""
        return await self._session_repository.invalidate_all_by_user_id(user_id)

    async def get_user_by_session(self, session_id: str) -> Tuple[User, Session]:
        """Get user by session ID, validating session."""
        session = await self._session_repository.find_by_id(session_id)
        if not session:
            raise InvalidSessionError("Session not found")

        if not session.is_valid():
            if session.is_expired():
                raise SessionExpiredError("Session has expired")
            else:
                raise InvalidSessionError("Session is invalid")

        # Update last accessed
        session.update_last_accessed()
        await self._session_repository.save(session)

        # Get user
        user = await self._user_repository.find_by_id(session.user_id)
        if not user:
            raise UserNotFoundError("User not found")

        return user, session

    async def refresh_session(
        self,
        refresh_token: str,
        new_access_token: str,
        expires_in_seconds: int = 3600
    ) -> Session:
        """Refresh a session with a new access token."""
        session = await self._session_repository.find_by_refresh_token(refresh_token)
        if not session:
            raise InvalidSessionError("Invalid refresh token")

        if not session.is_active:
            raise InvalidSessionError("Session is not active")

        # Update session with new access token
        session.refresh_access(new_access_token, expires_in_seconds)
        return await self._session_repository.save(session)

    async def confirm_user_email(self, user_id: str) -> User:
        """Confirm user email address."""
        user = await self._user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")

        user.confirm_email()
        return await self._user_repository.save(user)

    async def update_user_metadata(self, user_id: str, metadata: dict) -> User:
        """Update user metadata."""
        user = await self._user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")

        user.update_metadata(metadata)
        return await self._user_repository.save(user)

    async def delete_user_account(self, user_id: str) -> bool:
        """Delete user account and all associated sessions."""
        # Verify user exists
        user = await self._user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")

        # Delete all user sessions
        await self._session_repository.delete_by_user_id(user_id)

        # Delete user
        return await self._user_repository.delete(user_id)

    async def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions from the system."""
        return await self._session_repository.delete_expired()

    async def validate_access_token(self, access_token: str) -> Tuple[User, Session]:
        """Validate access token and return user and session."""
        session = await self._session_repository.find_by_access_token(access_token)
        if not session:
            raise InvalidSessionError("Invalid access token")

        if not session.is_valid():
            if session.is_expired():
                raise SessionExpiredError("Access token has expired")
            else:
                raise InvalidSessionError("Session is invalid")

        # Update last accessed
        session.update_last_accessed()
        await self._session_repository.save(session)

        # Get user
        user = await self._user_repository.find_by_id(session.user_id)
        if not user:
            raise UserNotFoundError("User not found")

        return user, session