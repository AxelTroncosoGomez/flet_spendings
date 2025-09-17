"""Dependency injection container for the application."""

from typing import Optional
from supabase import create_client, Client

from shared.config import get_config
from core.repositories.user_repository import UserRepository
from core.repositories.spending_repository import SpendingRepository
from core.repositories.session_repository import SessionRepository
from core.use_cases.auth_use_cases import AuthUseCases
from core.use_cases.spending_use_cases import SpendingUseCases
from infrastructure.repositories.user_repository_impl import SupabaseUserRepository
from infrastructure.repositories.spending_repository_impl import SupabaseSpendingRepository
from infrastructure.repositories.session_repository_impl import SupabaseSessionRepository
from infrastructure.services.auth_service import AuthService
from infrastructure.services.spending_service import SpendingService


class Container:
    """Dependency injection container for managing application dependencies."""

    def __init__(self):
        self._config = get_config()
        self._supabase_client: Optional[Client] = None
        self._user_repository: Optional[UserRepository] = None
        self._spending_repository: Optional[SpendingRepository] = None
        self._session_repository: Optional[SessionRepository] = None
        self._auth_use_cases: Optional[AuthUseCases] = None
        self._spending_use_cases: Optional[SpendingUseCases] = None
        self._auth_service: Optional[AuthService] = None
        self._spending_service: Optional[SpendingService] = None

    def supabase_client(self) -> Client:
        """Get or create Supabase client instance."""
        if self._supabase_client is None:
            self._supabase_client = create_client(
                self._config.database.url,
                self._config.database.key
            )
        return self._supabase_client

    def user_repository(self) -> UserRepository:
        """Get or create user repository instance."""
        if self._user_repository is None:
            self._user_repository = SupabaseUserRepository(self.supabase_client())
        return self._user_repository

    def spending_repository(self) -> SpendingRepository:
        """Get or create spending repository instance."""
        if self._spending_repository is None:
            self._spending_repository = SupabaseSpendingRepository(self.supabase_client())
        return self._spending_repository

    def session_repository(self) -> SessionRepository:
        """Get or create session repository instance."""
        if self._session_repository is None:
            self._session_repository = SupabaseSessionRepository(self.supabase_client())
        return self._session_repository

    def auth_use_cases(self) -> AuthUseCases:
        """Get or create auth use cases instance."""
        if self._auth_use_cases is None:
            self._auth_use_cases = AuthUseCases(
                user_repository=self.user_repository(),
                session_repository=self.session_repository()
            )
        return self._auth_use_cases

    def spending_use_cases(self) -> SpendingUseCases:
        """Get or create spending use cases instance."""
        if self._spending_use_cases is None:
            self._spending_use_cases = SpendingUseCases(
                spending_repository=self.spending_repository()
            )
        return self._spending_use_cases

    def auth_service(self) -> AuthService:
        """Get or create auth service instance."""
        if self._auth_service is None:
            self._auth_service = AuthService(
                supabase_client=self.supabase_client(),
                auth_use_cases=self.auth_use_cases()
            )
        return self._auth_service

    def spending_service(self) -> SpendingService:
        """Get or create spending service instance."""
        if self._spending_service is None:
            self._spending_service = SpendingService(
                spending_use_cases=self.spending_use_cases()
            )
        return self._spending_service

    def cleanup(self) -> None:
        """Cleanup resources and close connections."""
        if self._supabase_client:
            # Supabase client doesn't need explicit cleanup
            pass

    def reset(self) -> None:
        """Reset all instances (useful for testing)."""
        self._supabase_client = None
        self._user_repository = None
        self._spending_repository = None
        self._session_repository = None
        self._auth_use_cases = None
        self._spending_use_cases = None
        self._auth_service = None
        self._spending_service = None


# Global container instance
_container: Optional[Container] = None


def get_container() -> Container:
    """Get the global container instance."""
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container() -> None:
    """Reset the global container instance."""
    global _container
    if _container:
        _container.cleanup()
    _container = None