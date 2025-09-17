# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendio is a personal finance tracking application built with Flet (Python UI framework) and Supabase as the backend. The app provides cross-platform support for desktop, web, and mobile platforms with user authentication and spending management features.

## Development Commands

### Running the Application

**Desktop (using uv - preferred):**
```bash
uv run flet run
```

**Web application:**
```bash
uv run flet run --web
```

**Using Poetry (alternative):**
```bash
poetry install
poetry run flet run          # Desktop
poetry run flet run --web    # Web
```

### Building for Different Platforms

```bash
# Android
flet build apk -v

# iOS
flet build ipa -v

# macOS
flet build macos -v

# Linux
flet build linux -v

# Windows
flet build windows -v
```

### Testing

```bash
# Run tests with pytest
uv run pytest

# Tests are located in tests/ directory with unit and integration subdirectories
# Test configuration is handled by tests/conftest.py which loads .env variables
```

## Architecture

### Project Structure

- `src/main.py` - Application entry point with routing logic
- `src/pages/` - UI page components (login, register, spendings, etc.)
- `src/components/` - Reusable UI components (buttons, dialogs, datatables, inputs)
- `src/services/` - Business logic layer
  - `crud.py` - Local SQLite database operations
  - `supabase_service.py` - Supabase backend integration
- `src/utils/` - Utility modules (config, logging)
- `src/exceptions.py` - Custom exception definitions
- `storage/` - Local data storage
- `tests/` - Test suite with unit and integration tests

### Key Technologies

- **Flet 0.28.2** - Cross-platform UI framework based on Flutter
- **Supabase** - Backend-as-a-Service for authentication and database
- **Python 3.9+** - Minimum Python version requirement
- **uv** - Primary package manager (with Poetry support)

### Authentication Flow

The application uses Supabase for user authentication with the following pages:
- Login (`/login`) - Default landing page
- Register (`/register`) - User registration
- Verify (`/verify`) - Email verification
- Forgot Password (`/forgotpassword`) - Password reset
- Spendings (`/spendings`) - Main application after login

### Database Layer

Dual database approach:
- **Local**: SQLite through `LocalSpendingsDatabase` class
- **Remote**: Supabase through `SpendingsSupabaseDatabase` class

### Error Handling

Custom exceptions defined in `src/exceptions.py` for specific error scenarios:
- SupabaseApiException
- WrongCredentialsException
- UserAlreadyExistsException
- EmailNotConfirmedException
- And others for various auth/API scenarios

### Configuration

- Environment variables loaded from `.env` file
- Main configuration handled through `utils/config.py`
- Logging configured via `utils/logger.py`

## Development Notes

- The app is configured for mobile-first design (390x844 viewport by default)
- Dark theme is enabled by default
- Window close confirmation dialog is implemented
- The application prevents accidental closure with `page.window.prevent_close = True`
- Assets are handled through the `src/assets/` directory
- The app includes responsive breakpoints for different screen sizes

## Dependencies Management

The project uses both uv.lock and pyproject.toml for dependency management. Key dependencies include Flet, Supabase client, pytest for testing, and various utility libraries like loguru for logging and faker for test data generation.