import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock, AsyncMock, call
import flet as ft

# We need to mock flet app before importing main to prevent actual app launch
with patch('flet.app'), \
     patch('main.ft.app'):
    from main import main, init_async_supabase

from services.supabase_service import SpendingsSupabaseDatabase
from exceptions import GenericException, SupabaseApiException


class TestInitAsyncSupabase:
    """Test suite for init_async_supabase function."""

    @pytest.mark.skip(reason="Async tests require pytest-asyncio")
    async def test_init_async_supabase_success(self):
        """Test successful initialization of async Supabase."""
        with patch('main.SpendingsSupabaseDatabase') as mock_db_class:
            mock_db = AsyncMock()
            mock_db_class.return_value = mock_db

            result = await init_async_supabase()

            mock_db_class.assert_called_once()
            mock_db.async_client.assert_called_once()
            assert result == mock_db

    @pytest.mark.skip(reason="Async tests require pytest-asyncio")
    async def test_init_async_supabase_generic_exception(self):
        """Test init_async_supabase with GenericException."""
        with patch('main.SpendingsSupabaseDatabase') as mock_db_class:
            mock_db = AsyncMock()
            mock_db.async_client.side_effect = GenericException("Generic error")
            mock_db_class.return_value = mock_db

            with patch('main.logger') as mock_logger:
                result = await init_async_supabase()

                assert result is None
                mock_logger.error.assert_called_once()
                assert "Generic Supabase error" in mock_logger.error.call_args[0][0]

    @pytest.mark.skip(reason="Async tests require pytest-asyncio")
    async def test_init_async_supabase_api_exception(self):
        """Test init_async_supabase with SupabaseApiException."""
        with patch('main.SpendingsSupabaseDatabase') as mock_db_class:
            mock_db = AsyncMock()
            mock_db.async_client.side_effect = SupabaseApiException("API error")
            mock_db_class.return_value = mock_db

            with patch('main.logger') as mock_logger:
                result = await init_async_supabase()

                assert result is None
                mock_logger.error.assert_called_once()
                assert "Supabase API error" in mock_logger.error.call_args[0][0]

    @pytest.mark.skip(reason="Async tests require pytest-asyncio")
    async def test_init_async_supabase_unexpected_exception(self):
        """Test init_async_supabase with unexpected exception."""
        with patch('main.SpendingsSupabaseDatabase') as mock_db_class:
            mock_db = AsyncMock()
            mock_db.async_client.side_effect = ValueError("Unexpected error")
            mock_db_class.return_value = mock_db

            with patch('main.logger') as mock_logger:
                result = await init_async_supabase()

                assert result is None
                mock_logger.error.assert_called_once()
                assert "Unexpected error" in mock_logger.error.call_args[0][0]


class TestMainFunction:
    """Test suite for main function."""

    def test_main_page_configuration(self):
        """Test that main function configures page correctly."""
        mock_page = MagicMock()
        mock_page.views = []

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.LoginPage') as mock_login_page, \
             patch('main.RegisterPage') as mock_register_page, \
             patch('main.VerifyEmailPage') as mock_verify_page, \
             patch('main.ForgotPasswordPage') as mock_forgot_page:

            mock_db = MagicMock()
            mock_db_class.return_value = mock_db

            main(mock_page)

            # Check page configuration
            assert mock_page.title == "Spendings"
            assert mock_page.window.width == 390
            assert mock_page.window.height == 844
            assert mock_page.horizontal_alignment == "center"
            assert mock_page.vertical_alignment == "center"
            assert mock_page.theme_mode == ft.ThemeMode.DARK
            assert mock_page.window.prevent_close is True
            assert mock_page.scroll == ft.ScrollMode.AUTO

    def test_main_supabase_initialization_success(self):
        """Test successful Supabase initialization."""
        mock_page = MagicMock()
        mock_page.views = []

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.LoginPage') as mock_login_page, \
             patch('main.RegisterPage') as mock_register_page, \
             patch('main.VerifyEmailPage') as mock_verify_page, \
             patch('main.ForgotPasswordPage') as mock_forgot_page:

            mock_db = MagicMock()
            mock_db_class.return_value = mock_db

            main(mock_page)

            mock_db_class.assert_called_once()
            mock_db.sync_client.assert_called_once()

            # Check that pages are created with supabase instance
            mock_login_page.assert_called_once_with(mock_page, mock_db)
            mock_register_page.assert_called_once_with(mock_page, mock_db)
            mock_verify_page.assert_called_once_with(mock_page, mock_db)
            mock_forgot_page.assert_called_once_with(mock_page, mock_db)

    def test_main_supabase_generic_exception(self):
        """Test main function with Supabase GenericException."""
        mock_page = MagicMock()
        mock_page.views = []

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.CrashPage') as mock_crash_page:

            mock_db = MagicMock()
            mock_db.sync_client.side_effect = GenericException("Generic error")
            mock_db_class.return_value = mock_db

            main(mock_page)

            # Should clear views and show error page
            mock_page.views.clear.assert_called()
            mock_crash_page.assert_called_once()
            mock_page.views.append.assert_called_once()
            mock_page.go.assert_called_once_with("/error")

    def test_main_supabase_api_exception(self):
        """Test main function with Supabase API exception."""
        mock_page = MagicMock()
        mock_page.views = []

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.CrashPage') as mock_crash_page, \
             patch('main.logger') as mock_logger:

            mock_db = MagicMock()
            mock_db.sync_client.side_effect = SupabaseApiException("API error")
            mock_db_class.return_value = mock_db

            main(mock_page)

            # Should log debug message and show error page
            mock_logger.debug.assert_called_once_with("Something wrong happend on server ...")
            mock_crash_page.assert_called_once()
            mock_page.go.assert_called_once_with("/error")

    def test_main_unexpected_exception(self):
        """Test main function with unexpected exception."""
        mock_page = MagicMock()
        mock_page.views = []

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.CrashPage') as mock_crash_page:

            mock_db = MagicMock()
            mock_db.sync_client.side_effect = ValueError("Unexpected error")
            mock_db_class.return_value = mock_db

            main(mock_page)

            # Should show error page
            mock_crash_page.assert_called_once()
            mock_page.go.assert_called_once_with("/error")

    def test_main_window_event_handler_setup(self):
        """Test that window event handler is set up correctly."""
        mock_page = MagicMock()
        mock_page.views = []

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.LoginPage'), \
             patch('main.RegisterPage'), \
             patch('main.VerifyEmailPage'), \
             patch('main.ForgotPasswordPage'):

            mock_db = MagicMock()
            mock_db_class.return_value = mock_db

            main(mock_page)

            # Check that window event handler is set
            assert mock_page.window.on_event is not None
            assert mock_page.on_route_change is not None

    def test_main_initial_route(self):
        """Test that initial route is set to login."""
        mock_page = MagicMock()
        mock_page.views = []

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.LoginPage'), \
             patch('main.RegisterPage'), \
             patch('main.VerifyEmailPage'), \
             patch('main.ForgotPasswordPage'):

            mock_db = MagicMock()
            mock_db_class.return_value = mock_db

            main(mock_page)

            # Check initial route
            mock_page.go.assert_called_with("/login")


class TestRouteChange:
    """Test suite for route change functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_page = MagicMock()
        self.mock_page.views = []
        self.mock_supabase = MagicMock()

        # Create mock page instances
        self.mock_login_page = MagicMock()
        self.mock_register_page = MagicMock()
        self.mock_verify_page = MagicMock()
        self.mock_forgot_page = MagicMock()
        self.mock_spendings_page = MagicMock()

    def get_route_handler(self):
        """Get the route change handler from main function."""
        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.LoginPage') as mock_login_class, \
             patch('main.RegisterPage') as mock_register_class, \
             patch('main.VerifyEmailPage') as mock_verify_class, \
             patch('main.ForgotPasswordPage') as mock_forgot_class:

            mock_db_class.return_value = self.mock_supabase
            mock_login_class.return_value = self.mock_login_page
            mock_register_class.return_value = self.mock_register_page
            mock_verify_class.return_value = self.mock_verify_page
            mock_forgot_class.return_value = self.mock_forgot_page

            main(self.mock_page)

            # Return the route change handler that was set
            return self.mock_page.on_route_change

    def test_route_change_login(self):
        """Test route change to login page."""
        route_handler = self.get_route_handler()
        self.mock_page.route = "/login"

        route_handler(None)

        self.mock_page.views.clear.assert_called_once()
        self.mock_page.views.append.assert_called_once_with(self.mock_login_page)
        self.mock_page.update.assert_called_once()

    def test_route_change_register(self):
        """Test route change to register page."""
        route_handler = self.get_route_handler()
        self.mock_page.route = "/register"

        route_handler(None)

        self.mock_page.views.clear.assert_called_once()
        self.mock_page.views.append.assert_called_once_with(self.mock_register_page)
        self.mock_page.update.assert_called_once()

    def test_route_change_verify(self):
        """Test route change to verify page."""
        route_handler = self.get_route_handler()
        self.mock_page.route = "/verify"

        route_handler(None)

        self.mock_page.views.clear.assert_called_once()
        self.mock_page.views.append.assert_called_once_with(self.mock_verify_page)
        self.mock_page.update.assert_called_once()

    def test_route_change_forgot_password(self):
        """Test route change to forgot password page."""
        route_handler = self.get_route_handler()
        self.mock_page.route = "/forgotpassword"

        route_handler(None)

        self.mock_page.views.clear.assert_called_once()
        self.mock_page.views.append.assert_called_once_with(self.mock_forgot_page)
        self.mock_page.update.assert_called_once()

    def test_route_change_spendings(self):
        """Test route change to spendings page."""
        with patch('main.SpendingsPage') as mock_spendings_class:
            mock_spendings_class.return_value = self.mock_spendings_page

            route_handler = self.get_route_handler()
            self.mock_page.route = "/spendings"

            route_handler(None)

            self.mock_page.views.clear.assert_called_once()
            mock_spendings_class.assert_called_once_with(self.mock_page, self.mock_supabase)
            self.mock_page.views.append.assert_called_once_with(self.mock_spendings_page)
            self.mock_page.update.assert_called_once()

    def test_route_change_unknown_route(self):
        """Test route change to unknown route."""
        route_handler = self.get_route_handler()
        self.mock_page.route = "/unknown"

        route_handler(None)

        # Should still clear views and update, but not append any view
        self.mock_page.views.clear.assert_called_once()
        self.mock_page.update.assert_called_once()
        # views.append should not be called for unknown routes
        self.mock_page.views.append.assert_not_called()


class TestWindowEvents:
    """Test suite for window event handling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_page = MagicMock()
        self.mock_page.views = []

    def get_window_event_handler(self):
        """Get the window event handler from main function."""
        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.LoginPage'), \
             patch('main.RegisterPage'), \
             patch('main.VerifyEmailPage'), \
             patch('main.ForgotPasswordPage'):

            mock_db = MagicMock()
            mock_db_class.return_value = mock_db

            main(self.mock_page)

            # Return the window event handler that was set
            return self.mock_page.window.on_event

    def test_window_close_event(self):
        """Test window close event handling."""
        window_event_handler = self.get_window_event_handler()

        mock_event = MagicMock()
        mock_event.data = "close"

        window_event_handler(mock_event)

        # Should open confirm dialog
        self.mock_page.open.assert_called_once()
        self.mock_page.update.assert_called_once()

    def test_window_other_event(self):
        """Test window event handling for non-close events."""
        window_event_handler = self.get_window_event_handler()

        mock_event = MagicMock()
        mock_event.data = "minimize"

        window_event_handler(mock_event)

        # Should not open dialog for non-close events
        self.mock_page.open.assert_not_called()
        self.mock_page.update.assert_not_called()


class TestConfirmDialog:
    """Test suite for confirm dialog functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_page = MagicMock()
        self.mock_page.views = []

    def get_dialog_handlers(self):
        """Get the dialog handlers from main function."""
        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.LoginPage'), \
             patch('main.RegisterPage'), \
             patch('main.VerifyEmailPage'), \
             patch('main.ForgotPasswordPage'):

            mock_db = MagicMock()
            mock_db_class.return_value = mock_db

            main(self.mock_page)

            # Extract handlers from the confirm dialog actions
            window_handler = self.mock_page.window.on_event
            mock_event = MagicMock()
            mock_event.data = "close"
            window_handler(mock_event)

            # Get the dialog that was passed to page.open
            confirm_dialog = self.mock_page.open.call_args[0][0]

            yes_button = confirm_dialog.actions[0]
            no_button = confirm_dialog.actions[1]

            return yes_button.on_click, no_button.on_click, confirm_dialog

    def test_confirm_dialog_yes_click(self):
        """Test clicking Yes in confirm dialog."""
        yes_handler, no_handler, dialog = self.get_dialog_handlers()

        mock_event = MagicMock()
        yes_handler(mock_event)

        # Should destroy window
        self.mock_page.window.destroy.assert_called_once()

    def test_confirm_dialog_no_click(self):
        """Test clicking No in confirm dialog."""
        yes_handler, no_handler, dialog = self.get_dialog_handlers()

        mock_event = MagicMock()
        no_handler(mock_event)

        # Should close dialog and update page
        self.mock_page.close.assert_called_once_with(dialog)
        self.mock_page.update.assert_called_once()

    def test_confirm_dialog_properties(self):
        """Test confirm dialog has correct properties."""
        yes_handler, no_handler, dialog = self.get_dialog_handlers()

        assert dialog.modal is True
        assert isinstance(dialog.title, ft.Text)
        assert dialog.title.value == "Please confirm"
        assert isinstance(dialog.content, ft.Text)
        assert dialog.content.value == "Do you really want to exit this app?"
        assert len(dialog.actions) == 2
        assert dialog.actions_alignment == ft.MainAxisAlignment.END

        # Check button types and text
        assert isinstance(dialog.actions[0], ft.ElevatedButton)
        assert dialog.actions[0].text == "Yes"
        assert isinstance(dialog.actions[1], ft.OutlinedButton)
        assert dialog.actions[1].text == "No"


class TestEnvironmentVariables:
    """Test suite for environment variable handling."""

    @patch.dict(os.environ, {'FLET_ASSETS_DIR': '/test/assets'})
    def test_app_assets_path_loading(self):
        """Test that APP_ASSETS_PATH is loaded from environment."""
        # Reload the module to test environment variable loading
        import importlib
        import main
        importlib.reload(main)

        # The APP_ASSETS_PATH should be set from environment
        assert main.APP_ASSETS_PATH == '/test/assets'

    @patch.dict(os.environ, {}, clear=True)
    def test_app_assets_path_none(self):
        """Test APP_ASSETS_PATH when environment variable is not set."""
        # Reload the module to test environment variable loading
        import importlib
        import main
        importlib.reload(main)

        # The APP_ASSETS_PATH should be None when env var not set
        assert main.APP_ASSETS_PATH is None


class TestEdgeCases:
    """Test edge cases and error scenarios."""

    def test_main_with_none_page(self):
        """Test main function behavior with None page (should not crash)."""
        with patch('main.SpendingsSupabaseDatabase') as mock_db_class:
            mock_db = MagicMock()
            mock_db_class.return_value = mock_db

            # This should handle gracefully or raise appropriate error
            try:
                main(None)
            except AttributeError:
                # Expected if page is None, as we'll try to set attributes
                pass

    def test_main_with_page_missing_attributes(self):
        """Test main function with page missing some attributes."""
        mock_page = MagicMock()
        # Remove some attributes to test error handling
        del mock_page.views

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.CrashPage'):
            mock_db = MagicMock()
            mock_db.sync_client.side_effect = Exception("Test error")
            mock_db_class.return_value = mock_db

            # Should handle missing attributes gracefully
            try:
                main(mock_page)
            except AttributeError:
                # May raise AttributeError for missing page.views
                pass

    def test_route_change_with_empty_route(self):
        """Test route change with empty route."""
        mock_page = MagicMock()
        mock_page.views = []
        mock_page.route = ""

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.LoginPage'), \
             patch('main.RegisterPage'), \
             patch('main.VerifyEmailPage'), \
             patch('main.ForgotPasswordPage'):

            mock_db = MagicMock()
            mock_db_class.return_value = mock_db

            main(mock_page)
            route_handler = mock_page.on_route_change

            # Call with empty route
            route_handler(None)

            # Should clear views and update but not append anything
            mock_page.views.clear.assert_called()
            mock_page.update.assert_called()

    def test_multiple_main_calls(self):
        """Test calling main function multiple times."""
        mock_page1 = MagicMock()
        mock_page1.views = []
        mock_page2 = MagicMock()
        mock_page2.views = []

        with patch('main.SpendingsSupabaseDatabase') as mock_db_class, \
             patch('main.LoginPage'), \
             patch('main.RegisterPage'), \
             patch('main.VerifyEmailPage'), \
             patch('main.ForgotPasswordPage'):

            mock_db = MagicMock()
            mock_db_class.return_value = mock_db

            # Should be able to call main multiple times
            main(mock_page1)
            main(mock_page2)

            # Both pages should be configured
            assert mock_page1.title == "Spendings"
            assert mock_page2.title == "Spendings"