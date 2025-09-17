"""Secure configuration management for the application."""

import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    url: str
    key: str
    service_role_key: Optional[str] = None


@dataclass
class AppConfig:
    """Application configuration settings."""
    name: str = "Spendio"
    version: str = "0.3.0"
    debug: bool = False
    environment: str = "production"


@dataclass
class UIConfig:
    """UI configuration settings."""
    theme_mode: str = "dark"
    window_width: int = 390
    window_height: int = 844
    window_resizable: bool = True
    prevent_close: bool = True


@dataclass
class Config:
    """Main configuration class."""
    app: AppConfig
    database: DatabaseConfig
    ui: UIConfig

    @classmethod
    def from_environment(cls) -> "Config":
        """Create configuration from environment variables."""
        # Load environment file if it exists
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        if env_path.exists():
            cls._load_env_file(env_path)

        # Validate required environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")

        if not supabase_url:
            raise ValueError("SUPABASE_URL environment variable is required")
        if not supabase_key:
            raise ValueError("SUPABASE_ANON_KEY environment variable is required")

        return cls(
            app=AppConfig(
                name=os.getenv("APP_NAME", "Spendio"),
                version=os.getenv("APP_VERSION", "0.3.0"),
                debug=os.getenv("DEBUG", "false").lower() == "true",
                environment=os.getenv("ENVIRONMENT", "production")
            ),
            database=DatabaseConfig(
                url=supabase_url,
                key=supabase_key,
                service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            ),
            ui=UIConfig(
                theme_mode=os.getenv("THEME_MODE", "dark"),
                window_width=int(os.getenv("WINDOW_WIDTH", "390")),
                window_height=int(os.getenv("WINDOW_HEIGHT", "844")),
                window_resizable=os.getenv("WINDOW_RESIZABLE", "true").lower() == "true",
                prevent_close=os.getenv("PREVENT_CLOSE", "true").lower() == "true"
            )
        )

    @staticmethod
    def _load_env_file(env_path: Path) -> None:
        """Load environment variables from .env file."""
        try:
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and not os.getenv(key):
                            os.environ[key] = value
        except Exception as e:
            raise ValueError(f"Failed to load .env file: {e}")

    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.database.url.startswith(("http://", "https://")):
            raise ValueError("Database URL must be a valid HTTP/HTTPS URL")

        if len(self.database.key) < 10:
            raise ValueError("Database key appears to be invalid")

        if self.ui.window_width < 320 or self.ui.window_height < 480:
            raise ValueError("Window dimensions must be at least 320x480")

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app.environment.lower() in ("development", "dev", "local")

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app.environment.lower() in ("production", "prod")


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.from_environment()
        _config.validate()
    return _config


def reload_config() -> Config:
    """Reload configuration from environment."""
    global _config
    _config = None
    return get_config()