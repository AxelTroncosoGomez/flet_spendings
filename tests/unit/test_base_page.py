import pytest
import flet as ft
from unittest.mock import Mock, patch, MagicMock
from presentation.pages.base_page import BasePage


class TestBasePage:
    """Test suite for BasePage template."""

    def test_initialization_with_valid_parameters(self):
        """Test BasePage initialization with valid parameters."""
        page_mock = Mock(spec=ft.Page)
        supabase_service_mock = Mock()
        on_home_click = Mock()
        on_logout_click = Mock()

        base_page = BasePage(
            page=page_mock,
            route="/test",
            title="Test Page",
            supabase_service=supabase_service_mock,
            on_home_click=on_home_click,
            on_logout_click=on_logout_click
        )

        assert base_page.page == page_mock
        assert base_page.route == "/test"
        assert base_page.title == "Test Page"
        assert base_page.supabase_service == supabase_service_mock
        assert base_page.on_home_click == on_home_click
        assert base_page.on_logout_click == on_logout_click
        assert isinstance(base_page, ft.View)

    def test_initialization_creates_required_components(self):
        """Test that BasePage creates required components."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        assert hasattr(base_page, 'drawer')
        assert hasattr(base_page, 'appbar')
        assert hasattr(base_page, 'content_area')
        assert base_page.controls is not None
        assert len(base_page.controls) > 0

    def test_navigation_components_configuration(self):
        """Test navigation components configuration."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test Page")

        # Check AppBar configuration
        assert base_page.appbar.title.value == "Test Page"
        assert base_page.appbar.on_menu_click == base_page._handle_menu_click

        # Check Sidebar configuration
        assert base_page.drawer.on_home_click == base_page.on_home_click
        assert base_page.drawer.on_spendings_click == base_page.on_spendings_click
        assert base_page.drawer.on_database_click == base_page.on_database_click
        assert base_page.drawer.on_profile_click == base_page.on_profile_click
        assert base_page.drawer.on_logout_click == base_page.on_logout_click

    def test_content_area_structure(self):
        """Test content area structure."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        assert isinstance(base_page.content_area, ft.Container)
        assert isinstance(base_page.content_area.content, ft.Column)
        assert base_page.content_area.expand is True

    def test_safe_area_layout(self):
        """Test safe area layout structure."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        assert len(base_page.controls) == 1
        assert isinstance(base_page.controls[0], ft.SafeArea)
        safe_area = base_page.controls[0]
        assert isinstance(safe_area.content, ft.ResponsiveRow)

    def test_responsive_layout_configuration(self):
        """Test responsive layout configuration."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        safe_area = base_page.controls[0]
        responsive_row = safe_area.content
        assert responsive_row.alignment == ft.MainAxisAlignment.CENTER
        assert responsive_row.vertical_alignment == ft.CrossAxisAlignment.START

        # Check responsive container
        container = responsive_row.controls[0]
        assert isinstance(container, ft.Container)
        assert container.col == {"sm": 12, "md": 10, "lg": 8, "xl": 6}

    def test_default_page_content(self):
        """Test default page content structure."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test Page")

        content_controls = base_page._get_page_content()
        assert len(content_controls) >= 2
        assert isinstance(content_controls[0], ft.Text)
        assert "Welcome to Test Page" in content_controls[0].value

    def test_with_none_callbacks(self):
        """Test BasePage with None callbacks uses defaults."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        # Should use default callbacks
        assert base_page.on_home_click == base_page._default_home_click
        assert base_page.on_spendings_click == base_page._default_spendings_click
        assert base_page.on_database_click == base_page._default_database_click
        assert base_page.on_profile_click == base_page._default_profile_click
        assert base_page.on_logout_click == base_page._default_logout_click
        assert base_page.on_settings_click == base_page._default_settings_click

    def test_handle_menu_click_toggles_drawer(self):
        """Test menu click handler toggles drawer."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        # Mock drawer with initial state
        base_page.drawer.open = False
        base_page.drawer.update = Mock()

        # Simulate menu click
        mock_event = Mock()
        base_page._handle_menu_click(mock_event)

        assert base_page.drawer.open is True
        base_page.drawer.update.assert_called_once()

    def test_handle_menu_click_with_exception(self):
        """Test menu click handler with exception."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        # Mock drawer to raise exception
        base_page.drawer.update = Mock(side_effect=Exception("Test error"))

        # Should not raise exception
        mock_event = Mock()
        base_page._handle_menu_click(mock_event)

        # Should call page.update as fallback
        page_mock.update.assert_called_once()

    def test_default_navigation_handlers(self):
        """Test default navigation handlers."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        mock_event = Mock()

        # Test home navigation
        base_page._default_home_click(mock_event)
        page_mock.go.assert_called_with("/home")

        # Test spendings navigation
        page_mock.reset_mock()
        base_page._default_spendings_click(mock_event)
        page_mock.go.assert_called_with("/spendings")

        # Test database navigation
        page_mock.reset_mock()
        base_page._default_database_click(mock_event)
        page_mock.go.assert_called_with("/database")

        # Test profile navigation
        page_mock.reset_mock()
        base_page._default_profile_click(mock_event)
        page_mock.go.assert_called_with("/profile")

        # Test logout navigation
        page_mock.reset_mock()
        base_page._default_logout_click(mock_event)
        page_mock.go.assert_called_with("/login")

    def test_update_title_functionality(self):
        """Test update title functionality."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Original")

        # Mock appbar update_title method
        base_page.appbar.update_title = Mock()

        new_title = "Updated Title"
        base_page.update_title(new_title)

        assert base_page.title == new_title
        base_page.appbar.update_title.assert_called_once_with(new_title)

    def test_set_content_functionality(self):
        """Test set content functionality."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        new_content = [
            ft.Text("New content"),
            ft.Button("Test button")
        ]

        base_page.set_content(new_content)

        assert base_page.content_area.content.controls == new_content
        page_mock.update.assert_called_once()

    def test_add_content_functionality(self):
        """Test add content functionality."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        original_count = len(base_page.content_area.content.controls)
        new_control = ft.Text("Added content")

        base_page.add_content(new_control)

        assert len(base_page.content_area.content.controls) == original_count + 1
        assert base_page.content_area.content.controls[-1] == new_control
        page_mock.update.assert_called_once()

    def test_highlight_current_navigation(self):
        """Test highlight current navigation functionality."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        # Mock drawer highlight method
        base_page.drawer.highlight_current_page = Mock()

        base_page.highlight_current_navigation("Home")

        base_page.drawer.highlight_current_page.assert_called_once_with("Home")

    def test_inheritance_from_view(self):
        """Test that BasePage inherits from ft.View."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        assert isinstance(base_page, ft.View)
        assert hasattr(base_page, 'route')
        assert hasattr(base_page, 'controls')
        assert hasattr(base_page, 'horizontal_alignment')
        assert hasattr(base_page, 'scroll')

    def test_view_configuration_properties(self):
        """Test View configuration properties."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        assert base_page.route == "/test"
        assert base_page.horizontal_alignment == ft.CrossAxisAlignment.CENTER
        assert base_page.scroll == ft.ScrollMode.AUTO

    def test_custom_callbacks_override_defaults(self):
        """Test that custom callbacks override default ones."""
        page_mock = Mock(spec=ft.Page)
        custom_home = Mock()
        custom_logout = Mock()

        base_page = BasePage(
            page=page_mock,
            route="/test",
            title="Test",
            on_home_click=custom_home,
            on_logout_click=custom_logout
        )

        assert base_page.on_home_click == custom_home
        assert base_page.on_logout_click == custom_logout
        # Others should use defaults
        assert base_page.on_spendings_click == base_page._default_spendings_click

    def test_with_supabase_service(self):
        """Test BasePage with Supabase service."""
        page_mock = Mock(spec=ft.Page)
        supabase_mock = Mock()

        base_page = BasePage(
            page=page_mock,
            route="/test",
            title="Test",
            supabase_service=supabase_mock
        )

        assert base_page.supabase_service == supabase_mock

    def test_error_handling_in_navigation(self):
        """Test error handling in navigation methods."""
        page_mock = Mock(spec=ft.Page)
        page_mock.go.side_effect = Exception("Navigation error")

        base_page = BasePage(page=page_mock, route="/test", title="Test")

        mock_event = Mock()

        # Should not raise exception
        base_page._default_home_click(mock_event)
        base_page._default_spendings_click(mock_event)
        base_page._default_database_click(mock_event)
        base_page._default_profile_click(mock_event)
        base_page._default_logout_click(mock_event)

        # Should call page.update for error recovery
        assert page_mock.update.call_count == 5

    def test_error_handling_in_content_methods(self):
        """Test error handling in content manipulation methods."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        # Remove content_area to trigger error
        delattr(base_page, 'content_area')

        # Should not raise exception
        base_page.set_content([ft.Text("Test")])
        base_page.add_content(ft.Text("Test"))

    def test_multiple_instances_independence(self):
        """Test that multiple BasePage instances are independent."""
        page_mock1 = Mock(spec=ft.Page)
        page_mock2 = Mock(spec=ft.Page)

        base_page1 = BasePage(page=page_mock1, route="/test1", title="Test 1")
        base_page2 = BasePage(page=page_mock2, route="/test2", title="Test 2")

        assert base_page1.page == page_mock1
        assert base_page2.page == page_mock2
        assert base_page1.route == "/test1"
        assert base_page2.route == "/test2"
        assert base_page1.title == "Test 1"
        assert base_page2.title == "Test 2"
        assert base_page1 is not base_page2


class TestBasePageEdgeCases:
    """Test edge cases and error scenarios for BasePage."""

    def test_with_none_page_parameter(self):
        """Test BasePage with None page parameter."""
        base_page = BasePage(page=None, route="/test", title="Test")

        assert base_page.page is None
        # Should still create components without error
        assert hasattr(base_page, 'drawer')
        assert hasattr(base_page, 'appbar')

    def test_with_empty_title(self):
        """Test BasePage with empty title."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="")

        assert base_page.title == ""
        assert base_page.appbar.title.value == ""

    def test_with_special_characters_in_title(self):
        """Test BasePage with special characters in title."""
        page_mock = Mock(spec=ft.Page)
        special_title = "Test with ñáéíóú & symbols 🚀"
        base_page = BasePage(page=page_mock, route="/test", title=special_title)

        assert base_page.title == special_title
        assert base_page.appbar.title.value == special_title

    def test_with_callable_objects_as_callbacks(self):
        """Test BasePage with callable objects as callbacks."""
        class CallableClass:
            def __init__(self):
                self.called = False

            def __call__(self, event):
                self.called = True

        page_mock = Mock(spec=ft.Page)
        home_callback = CallableClass()
        logout_callback = CallableClass()

        base_page = BasePage(
            page=page_mock,
            route="/test",
            title="Test",
            on_home_click=home_callback,
            on_logout_click=logout_callback
        )

        assert callable(base_page.on_home_click)
        assert callable(base_page.on_logout_click)

    def test_drawer_state_persistence(self):
        """Test drawer state persistence across toggles."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        base_page.drawer.open = False
        base_page.drawer.update = Mock()

        mock_event = Mock()

        # First toggle - should open
        base_page._handle_menu_click(mock_event)
        assert base_page.drawer.open is True

        # Second toggle - should close
        base_page._handle_menu_click(mock_event)
        assert base_page.drawer.open is False

        assert base_page.drawer.update.call_count == 2

    def test_content_area_expansion_properties(self):
        """Test content area expansion properties."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        assert base_page.content_area.expand is True
        assert base_page.content_area.content.expand is True

    def test_responsive_breakpoints_configuration(self):
        """Test responsive breakpoints configuration."""
        page_mock = Mock(spec=ft.Page)
        base_page = BasePage(page=page_mock, route="/test", title="Test")

        safe_area = base_page.controls[0]
        container = safe_area.content.controls[0]

        expected_col = {"sm": 12, "md": 10, "lg": 8, "xl": 6}
        assert container.col == expected_col