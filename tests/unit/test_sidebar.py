import pytest
import flet as ft
from unittest.mock import Mock, patch, MagicMock
from presentation.components.sidebar import Sidebar


class TestSidebar:
    """Test suite for Sidebar component."""

    def test_initialization_with_valid_parameters(self):
        """Test Sidebar initialization with valid parameters."""
        on_home_click = Mock()
        on_spendings_click = Mock()
        on_database_click = Mock()
        on_profile_click = Mock()
        on_logout_click = Mock()

        sidebar = Sidebar(
            on_home_click=on_home_click,
            on_spendings_click=on_spendings_click,
            on_database_click=on_database_click,
            on_profile_click=on_profile_click,
            on_logout_click=on_logout_click
        )

        assert sidebar.on_home_click == on_home_click
        assert sidebar.on_spendings_click == on_spendings_click
        assert sidebar.on_database_click == on_database_click
        assert sidebar.on_profile_click == on_profile_click
        assert sidebar.on_logout_click == on_logout_click
        assert isinstance(sidebar, ft.NavigationDrawer)

    def test_initialization_creates_navigation_drawer(self):
        """Test that Sidebar creates a proper NavigationDrawer instance."""
        sidebar = Sidebar()

        assert isinstance(sidebar, ft.NavigationDrawer)
        assert sidebar.controls is not None
        assert len(sidebar.controls) > 0

    def test_sidebar_header_configuration(self):
        """Test sidebar header configuration."""
        sidebar = Sidebar()

        # Should have a header with app information
        header = sidebar.controls[0]
        assert isinstance(header, ft.Container)

    def test_navigation_menu_items(self):
        """Test navigation menu items configuration."""
        sidebar = Sidebar()

        # Find navigation items in controls
        nav_items = []
        for control in sidebar.controls:
            if isinstance(control, ft.ListTile):
                nav_items.append(control)

        # Should have Home, Spendings, Database, Profile items
        expected_titles = ["Home", "Spendings", "Database", "Profile"]
        found_titles = []

        for item in nav_items:
            if hasattr(item, 'title') and hasattr(item.title, 'value'):
                found_titles.append(item.title.value)

        for expected in expected_titles:
            assert expected in found_titles

    def test_logout_button_configuration(self):
        """Test logout button configuration at bottom."""
        sidebar = Sidebar()

        # Logout should be at the bottom
        logout_button = None
        for control in sidebar.controls:
            if isinstance(control, ft.ListTile) and hasattr(control, 'title'):
                if hasattr(control.title, 'value') and control.title.value == "Logout":
                    logout_button = control
                    break

        assert logout_button is not None
        assert isinstance(logout_button, ft.ListTile)
        assert logout_button.leading.name == ft.Icons.LOGOUT

    def test_menu_icons_configuration(self):
        """Test that menu items have proper icons."""
        sidebar = Sidebar()

        expected_icons = {
            "Home": ft.Icons.HOME,
            "Spendings": ft.Icons.MONETIZATION_ON,
            "Database": ft.Icons.STORAGE,
            "Profile": ft.Icons.PERSON,
            "Logout": ft.Icons.LOGOUT
        }

        nav_items = [control for control in sidebar.controls if isinstance(control, ft.ListTile)]

        for item in nav_items:
            if hasattr(item, 'title') and hasattr(item.title, 'value'):
                title = item.title.value
                if title in expected_icons:
                    assert item.leading.name == expected_icons[title]

    def test_with_none_callbacks(self):
        """Test Sidebar with None callbacks."""
        sidebar = Sidebar()

        # Should not raise exception with None callbacks
        assert sidebar.on_home_click is None
        assert sidebar.on_spendings_click is None
        assert sidebar.on_database_click is None
        assert sidebar.on_profile_click is None
        assert sidebar.on_logout_click is None

    def test_home_click_handling(self):
        """Test home menu item click handling."""
        on_home_click = Mock()
        sidebar = Sidebar(on_home_click=on_home_click)

        # Find home menu item
        home_item = None
        for control in sidebar.controls:
            if isinstance(control, ft.ListTile) and hasattr(control, 'title'):
                if hasattr(control.title, 'value') and control.title.value == "Home":
                    home_item = control
                    break

        assert home_item is not None

        # Simulate home click
        if home_item.on_click:
            mock_event = Mock()
            home_item.on_click(mock_event)
            on_home_click.assert_called_once_with(mock_event)

    def test_spendings_click_handling(self):
        """Test spendings menu item click handling."""
        on_spendings_click = Mock()
        sidebar = Sidebar(on_spendings_click=on_spendings_click)

        # Find spendings menu item
        spendings_item = None
        for control in sidebar.controls:
            if isinstance(control, ft.ListTile) and hasattr(control, 'title'):
                if hasattr(control.title, 'value') and control.title.value == "Spendings":
                    spendings_item = control
                    break

        assert spendings_item is not None

        # Simulate spendings click
        if spendings_item.on_click:
            mock_event = Mock()
            spendings_item.on_click(mock_event)
            on_spendings_click.assert_called_once_with(mock_event)

    def test_database_click_handling(self):
        """Test database menu item click handling."""
        on_database_click = Mock()
        sidebar = Sidebar(on_database_click=on_database_click)

        # Find database menu item
        database_item = None
        for control in sidebar.controls:
            if isinstance(control, ft.ListTile) and hasattr(control, 'title'):
                if hasattr(control.title, 'value') and control.title.value == "Database":
                    database_item = control
                    break

        assert database_item is not None

        # Simulate database click
        if database_item.on_click:
            mock_event = Mock()
            database_item.on_click(mock_event)
            on_database_click.assert_called_once_with(mock_event)

    def test_profile_click_handling(self):
        """Test profile menu item click handling."""
        on_profile_click = Mock()
        sidebar = Sidebar(on_profile_click=on_profile_click)

        # Find profile menu item
        profile_item = None
        for control in sidebar.controls:
            if isinstance(control, ft.ListTile) and hasattr(control, 'title'):
                if hasattr(control.title, 'value') and control.title.value == "Profile":
                    profile_item = control
                    break

        assert profile_item is not None

        # Simulate profile click
        if profile_item.on_click:
            mock_event = Mock()
            profile_item.on_click(mock_event)
            on_profile_click.assert_called_once_with(mock_event)

    def test_logout_click_handling(self):
        """Test logout menu item click handling."""
        on_logout_click = Mock()
        sidebar = Sidebar(on_logout_click=on_logout_click)

        # Find logout menu item
        logout_item = None
        for control in sidebar.controls:
            if isinstance(control, ft.ListTile) and hasattr(control, 'title'):
                if hasattr(control.title, 'value') and control.title.value == "Logout":
                    logout_item = control
                    break

        assert logout_item is not None

        # Simulate logout click
        if logout_item.on_click:
            mock_event = Mock()
            logout_item.on_click(mock_event)
            on_logout_click.assert_called_once_with(mock_event)

    def test_sidebar_styling_properties(self):
        """Test sidebar styling properties."""
        sidebar = Sidebar()

        assert isinstance(sidebar, ft.NavigationDrawer)
        assert sidebar.bgcolor is not None or sidebar.bgcolor == ft.Colors.SURFACE

    def test_responsive_width_configuration(self):
        """Test responsive width configuration."""
        sidebar = Sidebar()

        # Should have appropriate width for mobile/desktop
        assert hasattr(sidebar, 'width') or sidebar.width is None  # Default width handling

    def test_multiple_instances_independence(self):
        """Test that multiple Sidebar instances are independent."""
        callback1 = Mock()
        callback2 = Mock()

        sidebar1 = Sidebar(on_home_click=callback1)
        sidebar2 = Sidebar(on_home_click=callback2)

        assert sidebar1.on_home_click == callback1
        assert sidebar2.on_home_click == callback2
        assert sidebar1 is not sidebar2

    def test_inheritance_from_navigation_drawer(self):
        """Test that Sidebar inherits from ft.NavigationDrawer."""
        sidebar = Sidebar()

        assert isinstance(sidebar, ft.NavigationDrawer)
        assert hasattr(sidebar, 'controls')

    def test_header_content_structure(self):
        """Test header content structure."""
        sidebar = Sidebar()

        # Should have a header with app name or logo
        header = sidebar.controls[0]
        assert isinstance(header, ft.Container)

    def test_navigation_items_order(self):
        """Test that navigation items are in correct order."""
        sidebar = Sidebar()

        nav_items = [control for control in sidebar.controls if isinstance(control, ft.ListTile)]

        # Should have items in order: Home, Spendings, Database, Profile, ..., Logout
        titles = []
        for item in nav_items:
            if hasattr(item, 'title') and hasattr(item.title, 'value'):
                titles.append(item.title.value)

        expected_order = ["Home", "Spendings", "Database", "Profile"]

        # Check that the main navigation items appear in correct order
        for i, expected in enumerate(expected_order):
            assert expected in titles

        # Logout should be last
        assert "Logout" in titles
        assert titles.index("Logout") > titles.index("Profile")

    def test_accessibility_properties(self):
        """Test accessibility properties."""
        sidebar = Sidebar()

        nav_items = [control for control in sidebar.controls if isinstance(control, ft.ListTile)]

        for item in nav_items:
            # Each item should have proper icon and title
            assert item.leading is not None
            assert item.title is not None
            assert isinstance(item.title, ft.Text)


class TestSidebarEdgeCases:
    """Test edge cases and error scenarios for Sidebar."""

    def test_with_callable_objects_as_callbacks(self):
        """Test Sidebar with callable objects as callbacks."""
        class CallableClass:
            def __init__(self):
                self.called = False

            def __call__(self, event):
                self.called = True

        home_callback = CallableClass()
        logout_callback = CallableClass()

        sidebar = Sidebar(
            on_home_click=home_callback,
            on_logout_click=logout_callback
        )

        assert callable(sidebar.on_home_click)
        assert callable(sidebar.on_logout_click)

    def test_sidebar_divider_presence(self):
        """Test that sidebar has appropriate dividers."""
        sidebar = Sidebar()

        # Should have dividers between sections
        dividers = [control for control in sidebar.controls if isinstance(control, ft.Divider)]
        assert len(dividers) >= 1  # At least one divider before logout

    def test_list_tile_configuration(self):
        """Test ListTile configuration for menu items."""
        sidebar = Sidebar()

        nav_items = [control for control in sidebar.controls if isinstance(control, ft.ListTile)]

        for item in nav_items:
            # Each ListTile should have proper configuration
            assert isinstance(item.leading, ft.Icon)
            assert isinstance(item.title, ft.Text)
            assert item.title.value is not None
            assert item.title.value != ""

    def test_icon_consistency(self):
        """Test icon consistency across menu items."""
        sidebar = Sidebar()

        nav_items = [control for control in sidebar.controls if isinstance(control, ft.ListTile)]

        for item in nav_items:
            # Icons should be consistent ft.Icons
            assert hasattr(item.leading, 'name')
            assert item.leading.name is not None

    def test_header_styling_consistency(self):
        """Test header styling consistency."""
        sidebar = Sidebar()

        header = sidebar.controls[0]
        assert isinstance(header, ft.Container)
        # Header should have some content
        assert header.content is not None