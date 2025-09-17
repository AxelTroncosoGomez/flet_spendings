"""Authentication service implementation using clean architecture."""

from typing import Optional, Tuple
from datetime import datetime
from supabase import Client

from core.entities.user import User
from core.entities.session import Session
from core.use_cases.auth_use_cases import AuthUseCases
from core.repositories.user_repository import UserRepository
from core.repositories.session_repository import SessionRepository
from core.exceptions.auth_exceptions import (
    InvalidCredentialsError,
    EmailNotConfirmedError,
    SessionExpiredError,
    InvalidSessionError
)


class AuthService:
    """High-level authentication service using clean architecture patterns."""

    def __init__(
        self,
        supabase_client: Client,
        auth_use_cases: AuthUseCases
    ):
        self._client = supabase_client
        self._auth_use_cases = auth_use_cases

    async def register(self, email: str, password: str, metadata: Optional[dict] = None) -> User:
        """Register a new user with Supabase authentication."""
        try:
            # Register with Supabase Auth
            auth_response = self._client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": metadata} if metadata else None
            })

            if not auth_response.user:
                raise Exception("Failed to create user account")

            # Create user in our domain
            user = await self._auth_use_cases.register_user(
                email=email,
                metadata=metadata
            )

            return user

        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")

    async def login(self, email: str, password: str) -> Tuple[User, Session]:
        """Login user with email and password."""
        try:
            # Authenticate with Supabase
            auth_response = self._client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not auth_response.user or not auth_response.session:
                raise InvalidCredentialsError("Invalid email or password")

            # Check email confirmation
            if not auth_response.user.email_confirmed_at:
                raise EmailNotConfirmedError("Please confirm your email before logging in")

            # Create domain session
            user, session = await self._auth_use_cases.login_user(
                email=email,
                access_token=auth_response.session.access_token,
                refresh_token=auth_response.session.refresh_token,
                require_email_confirmation=True
            )

            return user, session

        except (InvalidCredentialsError, EmailNotConfirmedError):
            raise
        except Exception as e:
            raise InvalidCredentialsError(f"Login failed: {str(e)}")

    async def logout(self, session_id: str) -> bool:
        """Logout user and invalidate session."""
        try:
            # Invalidate Supabase session
            self._client.auth.sign_out()

            # Invalidate domain session
            return await self._auth_use_cases.logout_user(session_id)

        except Exception:
            return False

    async def refresh_session(self, refresh_token: str) -> Session:
        """Refresh user session with new access token."""
        try:
            # Refresh with Supabase
            auth_response = self._client.auth.refresh_session(refresh_token)

            if not auth_response.session:
                raise InvalidSessionError("Failed to refresh session")

            # Update domain session
            session = await self._auth_use_cases.refresh_session(
                refresh_token=refresh_token,
                new_access_token=auth_response.session.access_token
            )

            return session

        except Exception as e:
            raise SessionExpiredError(f"Session refresh failed: {str(e)}")

    async def get_current_user(self, session_id: str) -> Tuple[User, Session]:
        """Get current user by session."""
        return await self._auth_use_cases.get_user_by_session(session_id)

    async def validate_session(self, access_token: str) -> Tuple[User, Session]:
        """Validate access token and return user."""
        return await self._auth_use_cases.validate_access_token(access_token)

    async def confirm_email(self, token: str) -> bool:
        """Confirm user email with token."""
        try:
            # Verify token with Supabase
            auth_response = self._client.auth.verify_otp({
                "token_hash": token,
                "type": "signup"
            })

            if not auth_response.user:
                return False

            # Confirm in domain
            await self._auth_use_cases.confirm_user_email(auth_response.user.id)
            return True

        except Exception:
            return False

    async def reset_password(self, email: str) -> bool:
        """Send password reset email."""
        try:
            self._client.auth.reset_password_email(email)
            return True
        except Exception:
            return False

    async def update_password(self, new_password: str) -> bool:
        """Update user password."""
        try:
            response = self._client.auth.update_user({
                "password": new_password
            })
            return response.user is not None
        except Exception:
            return False

    async def delete_account(self, user_id: str) -> bool:
        """Delete user account completely."""
        try:
            # Delete from domain first
            domain_deleted = await self._auth_use_cases.delete_user_account(user_id)

            if domain_deleted:
                # Note: Supabase doesn't provide admin API for user deletion in client
                # This would typically be handled by an admin service or webhook
                pass

            return domain_deleted

        except Exception:
            return False