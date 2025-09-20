import pytest
import flet as ft
from unittest.mock import Mock, patch, MagicMock
from pages.profile_page import ProfilePage


class TestProfilePage:
    """Test suite for ProfilePage component."""

    def test_initialization_with_valid_parameters(self):
        """Test ProfilePage initialization with valid parameters."""
        page_mock = Mock(spec=ft.Page)
        supabase_service_mock = Mock()
        on_profile_click = Mock()
        on_logout_click = Mock()

        profile_page = ProfilePage(
            page=page_mock,
            supabase_service=supabase_service_mock,
            on_profile_click=on_profile_click,
            on_logout_click=on_logout_click
        )

        assert profile_page.page == page_mock
        assert profile_page.route == "/profile"
        assert profile_page.title == "Spendio - Profile"
        assert profile_page.supabase_service == supabase_service_mock
        assert profile_page.on_profile_click == on_profile_click
        assert profile_page.on_logout_click == on_logout_click

    def test_initialization_creates_base_components(self):
        """Test that ProfilePage creates base page components."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Should inherit from BasePage
        assert hasattr(profile_page, 'drawer')
        assert hasattr(profile_page, 'appbar')
        assert hasattr(profile_page, 'content_area')
        assert profile_page.controls is not None

    def test_route_configuration(self):
        """Test ProfilePage route configuration."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        assert profile_page.route == "/profile"

    def test_title_configuration(self):
        """Test ProfilePage title configuration."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        assert profile_page.title == "Spendio - Profile"
        assert profile_page.appbar.title.value == "Spendio - Profile"

    def test_user_profile_initialization(self):
        """Test user profile initialization."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        assert hasattr(profile_page, 'user_profile')
        assert isinstance(profile_page.user_profile, dict)
        assert 'name' in profile_page.user_profile
        assert 'email' in profile_page.user_profile
        assert 'avatar_url' in profile_page.user_profile
        assert 'created_at' in profile_page.user_profile
        assert 'subscription' in profile_page.user_profile
        assert 'theme' in profile_page.user_profile
        assert 'currency' in profile_page.user_profile
        assert 'notifications' in profile_page.user_profile
        assert 'two_factor' in profile_page.user_profile

    def test_form_fields_creation(self):
        """Test form fields creation."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        assert hasattr(profile_page, 'name_field')
        assert hasattr(profile_page, 'email_field')
        assert hasattr(profile_page, 'current_password_field')
        assert hasattr(profile_page, 'new_password_field')
        assert hasattr(profile_page, 'confirm_password_field')

        assert isinstance(profile_page.name_field, ft.TextField)
        assert isinstance(profile_page.email_field, ft.TextField)
        assert isinstance(profile_page.current_password_field, ft.TextField)
        assert isinstance(profile_page.new_password_field, ft.TextField)
        assert isinstance(profile_page.confirm_password_field, ft.TextField)

    def test_page_content_structure(self):
        """Test page content structure."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        content = profile_page._get_page_content()
        assert isinstance(content, list)
        assert len(content) >= 5  # Header, account info, security, preferences, statistics

    def test_profile_header_creation(self):
        """Test profile header creation."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        header = profile_page._create_profile_header()
        assert isinstance(header, ft.Container)
        assert isinstance(header.content, ft.Column)

    def test_account_info_creation(self):
        """Test account info section creation."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        account_info = profile_page._create_account_info()
        assert isinstance(account_info, ft.Container)
        assert isinstance(account_info.content, ft.Column)

    def test_security_settings_creation(self):
        """Test security settings creation."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        security_settings = profile_page._create_security_settings()
        assert isinstance(security_settings, ft.Container)
        assert isinstance(security_settings.content, ft.Column)

    def test_preferences_settings_creation(self):
        """Test preferences settings creation."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        preferences = profile_page._create_preferences_settings()
        assert isinstance(preferences, ft.Container)
        assert isinstance(preferences.content, ft.Column)

    def test_account_statistics_creation(self):
        """Test account statistics creation."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        statistics = profile_page._create_account_statistics()
        assert isinstance(statistics, ft.Container)
        assert isinstance(statistics.content, ft.Column)

    def test_stat_card_creation(self):
        """Test statistics card creation."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        stat_card = profile_page._create_stat_card(
            title="Test Stat",
            value="100",
            icon=ft.Icons.PERSON,
            color=ft.Colors.PRIMARY
        )

        assert isinstance(stat_card, ft.Card)
        assert isinstance(stat_card.content, ft.Container)

    def test_change_avatar_handler(self):
        """Test change avatar handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_info_message = Mock()

        mock_event = Mock()
        profile_page._handle_change_avatar(mock_event)

        profile_page._show_info_message.assert_called_once()

    def test_edit_profile_handler(self):
        """Test edit profile handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_info_message = Mock()

        mock_event = Mock()
        profile_page._handle_edit_profile(mock_event)

        profile_page._show_info_message.assert_called_once()

    def test_save_profile_handler(self):
        """Test save profile handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_success_message = Mock()

        # Set form field value
        profile_page.name_field.value = "New Name"

        mock_event = Mock()
        profile_page._handle_save_profile(mock_event)

        assert profile_page.user_profile["name"] == "New Name"
        profile_page._show_success_message.assert_called_once()

    def test_cancel_edit_handler(self):
        """Test cancel edit handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Modify form fields
        profile_page.name_field.value = "Modified"
        profile_page.email_field.value = "modified@example.com"

        mock_event = Mock()
        profile_page._handle_cancel_edit(mock_event)

        # Should reset to original values
        assert profile_page.name_field.value == profile_page.user_profile["name"]
        assert profile_page.email_field.value == profile_page.user_profile["email"]
        page_mock.update.assert_called_once()

    def test_change_password_handler_success(self):
        """Test change password handler with valid inputs."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_success_message = Mock()

        # Set password fields
        profile_page.current_password_field.value = "current123"
        profile_page.new_password_field.value = "new123"
        profile_page.confirm_password_field.value = "new123"

        mock_event = Mock()
        profile_page._handle_change_password(mock_event)

        profile_page._show_success_message.assert_called_once()
        # Password fields should be cleared
        assert profile_page.current_password_field.value == ""
        assert profile_page.new_password_field.value == ""
        assert profile_page.confirm_password_field.value == ""

    def test_change_password_handler_mismatch(self):
        """Test change password handler with mismatched passwords."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_error_message = Mock()

        # Set mismatched passwords
        profile_page.current_password_field.value = "current123"
        profile_page.new_password_field.value = "new123"
        profile_page.confirm_password_field.value = "different123"

        mock_event = Mock()
        profile_page._handle_change_password(mock_event)

        profile_page._show_error_message.assert_called_with("New passwords do not match")

    def test_change_password_handler_empty_fields(self):
        """Test change password handler with empty fields."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_error_message = Mock()

        # Leave fields empty
        profile_page.current_password_field.value = ""
        profile_page.new_password_field.value = "new123"
        profile_page.confirm_password_field.value = "new123"

        mock_event = Mock()
        profile_page._handle_change_password(mock_event)

        profile_page._show_error_message.assert_called_with("Please fill all password fields")

    def test_two_factor_toggle_handler(self):
        """Test two-factor authentication toggle handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_info_message = Mock()

        mock_event = Mock()
        mock_event.control.value = True

        profile_page._handle_two_factor_toggle(mock_event)

        assert profile_page.user_profile["two_factor"] is True
        profile_page._show_info_message.assert_called_once()

    def test_setup_2fa_handler(self):
        """Test setup 2FA handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_info_message = Mock()

        mock_event = Mock()
        profile_page._handle_setup_2fa(mock_event)

        profile_page._show_info_message.assert_called_once()

    def test_theme_change_handler(self):
        """Test theme change handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        mock_event = Mock()
        mock_event.control.value = "Light"

        profile_page._handle_theme_change(mock_event)

        assert profile_page.user_profile["theme"] == "Light"

    def test_currency_change_handler(self):
        """Test currency change handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        mock_event = Mock()
        mock_event.control.value = "EUR"

        profile_page._handle_currency_change(mock_event)

        assert profile_page.user_profile["currency"] == "EUR"

    def test_notifications_toggle_handler(self):
        """Test notifications toggle handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        mock_event = Mock()
        mock_event.control.value = False

        profile_page._handle_notifications_toggle(mock_event)

        assert profile_page.user_profile["notifications"] is False

    def test_save_preferences_handler(self):
        """Test save preferences handler."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_success_message = Mock()

        mock_event = Mock()
        profile_page._handle_save_preferences(mock_event)

        profile_page._show_success_message.assert_called_once()

    def test_load_user_profile_functionality(self):
        """Test load user profile functionality."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subscription": "Premium",
            "total_spendings": 1500.75
        }

        profile_page.load_user_profile(user_data)

        assert profile_page.user_profile["name"] == "John Doe"
        assert profile_page.user_profile["email"] == "john@example.com"
        assert profile_page.user_profile["subscription"] == "Premium"
        assert profile_page.user_profile["total_spendings"] == 1500.75
        assert profile_page.name_field.value == "John Doe"
        assert profile_page.email_field.value == "john@example.com"
        page_mock.update.assert_called_once()

    def test_get_user_profile_functionality(self):
        """Test get user profile functionality."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        profile_data = profile_page.get_user_profile()

        assert isinstance(profile_data, dict)
        assert profile_data is not profile_page.user_profile  # Should be a copy
        assert profile_data["name"] == profile_page.user_profile["name"]
        assert profile_data["email"] == profile_page.user_profile["email"]

    def test_message_display_methods(self):
        """Test message display methods."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Should not raise exceptions
        profile_page._show_info_message("Test info")
        profile_page._show_error_message("Test error")
        profile_page._show_success_message("Test success")

    def test_update_form_fields_functionality(self):
        """Test update form fields functionality."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Change profile data
        profile_page.user_profile["name"] = "Updated Name"
        profile_page.user_profile["email"] = "updated@example.com"

        profile_page._update_form_fields()

        assert profile_page.name_field.value == "Updated Name"
        assert profile_page.email_field.value == "updated@example.com"

    def test_error_handling_in_content_creation(self):
        """Test error handling in content creation."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Mock a method to raise exception
        with patch.object(profile_page, '_create_profile_header', side_effect=Exception("Test error")):
            content = profile_page._get_page_content()

            # Should return error content instead of raising
            assert isinstance(content, list)
            assert len(content) == 1
            assert isinstance(content[0], ft.Text)
            assert "Error loading" in content[0].value

    def test_error_handling_in_handlers(self):
        """Test error handling in event handlers."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Mock show_error_message
        profile_page._show_error_message = Mock()

        # Mock methods to raise exceptions
        profile_page._show_info_message = Mock(side_effect=Exception("Test error"))

        mock_event = Mock()

        # Should not raise exceptions
        profile_page._handle_change_avatar(mock_event)
        profile_page._handle_edit_profile(mock_event)

    def test_form_field_properties(self):
        """Test form field properties and configuration."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Name field
        assert profile_page.name_field.label == "Full Name"
        assert profile_page.name_field.prefix_icon == ft.Icons.PERSON

        # Email field
        assert profile_page.email_field.label == "Email Address"
        assert profile_page.email_field.prefix_icon == ft.Icons.EMAIL
        assert profile_page.email_field.read_only is True

        # Password fields
        assert profile_page.current_password_field.password is True
        assert profile_page.new_password_field.password is True
        assert profile_page.confirm_password_field.password is True

    def test_with_none_callbacks(self):
        """Test ProfilePage with None callbacks."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Should not raise exception with None callbacks
        assert hasattr(profile_page, 'on_home_click')
        assert hasattr(profile_page, 'on_spendings_click')
        assert hasattr(profile_page, 'on_database_click')
        assert hasattr(profile_page, 'on_profile_click')
        assert hasattr(profile_page, 'on_logout_click')

    def test_inheritance_from_base_page(self):
        """Test that ProfilePage inherits from BasePage."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Should have BasePage attributes
        assert hasattr(profile_page, 'drawer')
        assert hasattr(profile_page, 'appbar')
        assert hasattr(profile_page, 'content_area')
        assert hasattr(profile_page, '_handle_menu_click')
        assert hasattr(profile_page, 'update_title')
        assert hasattr(profile_page, 'set_content')

    def test_multiple_instances_independence(self):
        """Test that multiple ProfilePage instances are independent."""
        page_mock1 = Mock(spec=ft.Page)
        page_mock2 = Mock(spec=ft.Page)
        callback1 = Mock()
        callback2 = Mock()

        profile_page1 = ProfilePage(page=page_mock1, on_profile_click=callback1)
        profile_page2 = ProfilePage(page=page_mock2, on_profile_click=callback2)

        assert profile_page1.page == page_mock1
        assert profile_page2.page == page_mock2
        assert profile_page1.on_profile_click == callback1
        assert profile_page2.on_profile_click == callback2
        assert profile_page1 is not profile_page2

    def test_supabase_service_integration(self):
        """Test Supabase service integration."""
        page_mock = Mock(spec=ft.Page)
        supabase_mock = Mock()

        profile_page = ProfilePage(page=page_mock, supabase_service=supabase_mock)

        assert profile_page.supabase_service == supabase_mock

    def test_responsive_layout_configuration(self):
        """Test responsive layout configuration."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Check account info responsive layout
        account_info = profile_page._create_account_info()
        column_content = account_info.content
        card_content = column_content.controls[1].content.content
        responsive_row = card_content.controls[0]

        assert isinstance(responsive_row, ft.ResponsiveRow)

        # Check statistics responsive layout
        statistics = profile_page._create_account_statistics()
        stats_column = statistics.content
        stats_responsive_row = stats_column.controls[1]

        assert isinstance(stats_responsive_row, ft.ResponsiveRow)
        assert len(stats_responsive_row.controls) == 4  # 4 stat cards


class TestProfilePageEdgeCases:
    """Test edge cases and error scenarios for ProfilePage."""

    def test_with_none_page_parameter(self):
        """Test ProfilePage with None page parameter."""
        profile_page = ProfilePage(page=None)

        assert profile_page.page is None
        # Should still create components without error
        assert hasattr(profile_page, 'drawer')
        assert hasattr(profile_page, 'appbar')
        assert hasattr(profile_page, 'user_profile')
        assert hasattr(profile_page, 'name_field')

    def test_handlers_with_none_page(self):
        """Test event handlers with None page."""
        profile_page = ProfilePage(page=None)

        mock_event = Mock()

        # Should not raise exceptions even with None page
        profile_page._handle_change_avatar(mock_event)
        profile_page._handle_edit_profile(mock_event)
        profile_page._handle_save_profile(mock_event)
        profile_page._handle_save_preferences(mock_event)

    def test_form_field_creation_with_exception(self):
        """Test form field creation with exception handling."""
        page_mock = Mock(spec=ft.Page)

        # Mock TextField to raise exception
        with patch('flet.TextField', side_effect=Exception("TextField error")):
            # Should not raise exception during initialization
            profile_page = ProfilePage(page=page_mock)
            assert hasattr(profile_page, 'user_profile')

    def test_load_user_profile_with_partial_data(self):
        """Test load user profile with partial data."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        partial_data = {"name": "Partial User"}

        profile_page.load_user_profile(partial_data)

        assert profile_page.user_profile["name"] == "Partial User"
        # Other fields should remain unchanged
        assert "email" in profile_page.user_profile

    def test_load_user_profile_with_none_page(self):
        """Test load user profile with None page."""
        profile_page = ProfilePage(page=None)

        user_data = {"name": "Test User"}

        # Should not raise exception
        profile_page.load_user_profile(user_data)
        assert profile_page.user_profile["name"] == "Test User"

    def test_message_methods_with_none_page(self):
        """Test message methods with None page."""
        profile_page = ProfilePage(page=None)

        # Should not raise exceptions
        profile_page._show_info_message("Test")
        profile_page._show_error_message("Test")
        profile_page._show_success_message("Test")

    def test_stat_card_creation_with_none_values(self):
        """Test stat card creation with None values."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Should handle None values gracefully
        stat_card = profile_page._create_stat_card(
            title=None,
            value=None,
            icon=ft.Icons.PERSON,
            color=ft.Colors.PRIMARY
        )

        assert isinstance(stat_card, ft.Card)

    def test_error_handling_in_update_methods(self):
        """Test error handling in update methods."""
        page_mock = Mock(spec=ft.Page)
        page_mock.update.side_effect = Exception("Update error")

        profile_page = ProfilePage(page=page_mock)

        # Should not raise exceptions
        profile_page.load_user_profile({"name": "Test"})

    def test_with_callable_objects_as_callbacks(self):
        """Test ProfilePage with callable objects as callbacks."""
        class CallableClass:
            def __init__(self):
                self.called = False

            def __call__(self, event):
                self.called = True

        page_mock = Mock(spec=ft.Page)
        profile_callback = CallableClass()
        logout_callback = CallableClass()

        profile_page = ProfilePage(
            page=page_mock,
            on_profile_click=profile_callback,
            on_logout_click=logout_callback
        )

        assert callable(profile_page.on_profile_click)
        assert callable(profile_page.on_logout_click)

    def test_change_password_with_exception_handling(self):
        """Test change password with exception handling."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)
        profile_page._show_error_message = Mock()

        # Mock to raise exception
        profile_page._show_success_message = Mock(side_effect=Exception("Test error"))

        profile_page.current_password_field.value = "current"
        profile_page.new_password_field.value = "new"
        profile_page.confirm_password_field.value = "new"

        mock_event = Mock()
        profile_page._handle_change_password(mock_event)

        profile_page._show_error_message.assert_called_with("Error changing password")

    def test_user_profile_default_values(self):
        """Test user profile default values."""
        page_mock = Mock(spec=ft.Page)
        profile_page = ProfilePage(page=page_mock)

        # Check all expected default values
        assert profile_page.user_profile["name"] == "User"
        assert profile_page.user_profile["email"] == "user@example.com"
        assert profile_page.user_profile["avatar_url"] is None
        assert profile_page.user_profile["subscription"] == "Free"
        assert profile_page.user_profile["theme"] == "Dark"
        assert profile_page.user_profile["currency"] == "USD"
        assert profile_page.user_profile["notifications"] is True
        assert profile_page.user_profile["two_factor"] is False