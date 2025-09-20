import pytest
import flet as ft
from unittest.mock import Mock, patch, MagicMock
from presentation.components.responsive_appbar import ResponsiveAppBar


class TestResponsiveAppBar:
    """Test suite for ResponsiveAppBar component."""

    def test_initialization_with_valid_parameters(self):
        """Test ResponsiveAppBar initialization with valid parameters."""
        title = "Test App"
        on_menu_click = Mock()
        on_settings_click = Mock()

        appbar = ResponsiveAppBar(
            title=title,
            on_menu_click=on_menu_click,
            on_settings_click=on_settings_click
        )

        assert appbar.title.value == title
        assert appbar.on_menu_click == on_menu_click
        assert appbar.on_settings_click == on_settings_click
        assert isinstance(appbar, ft.AppBar)

    def test_initialization_creates_appbar_instance(self):
        """Test that ResponsiveAppBar creates a proper AppBar instance."""
        appbar = ResponsiveAppBar(title="Test")

        assert isinstance(appbar, ft.AppBar)
        assert appbar.title is not None
        assert appbar.leading is not None
        assert appbar.actions is not None

    def test_appbar_title_configuration(self):
        """Test AppBar title configuration."""
        title_text = "Spendio"
        appbar = ResponsiveAppBar(title=title_text)

        assert isinstance(appbar.title, ft.Text)
        assert appbar.title.value == title_text
        assert appbar.center_title is False

    def test_appbar_leading_menu_button(self):
        """Test AppBar leading menu button configuration."""
        on_menu_click = Mock()
        appbar = ResponsiveAppBar(title="Test", on_menu_click=on_menu_click)

        assert isinstance(appbar.leading, ft.IconButton)
        assert appbar.leading.icon == ft.Icons.MENU
        assert appbar.leading.on_click == on_menu_click

    def test_appbar_actions_configuration(self):
        """Test AppBar actions configuration."""
        appbar = ResponsiveAppBar(title="Test")

        assert isinstance(appbar.actions, list)
        assert len(appbar.actions) == 1
        assert isinstance(appbar.actions[0], ft.PopupMenuButton)

    def test_popup_menu_items_configuration(self):
        """Test popup menu items configuration."""
        appbar = ResponsiveAppBar(title="Test")
        popup_menu = appbar.actions[0]

        assert isinstance(popup_menu.items, list)
        assert len(popup_menu.items) >= 2  # Settings and at least one divider

        # Check for settings item
        settings_item = None
        for item in popup_menu.items:
            if hasattr(item, 'text') and item.text == "Settings":
                settings_item = item
                break

        assert settings_item is not None
        assert isinstance(settings_item, ft.PopupMenuItem)

    def test_appbar_styling_properties(self):
        """Test AppBar styling properties."""
        appbar = ResponsiveAppBar(title="Test")

        assert appbar.bgcolor == ft.Colors.SURFACE
        assert appbar.elevation is not None
        assert appbar.leading_width == 56

    def test_with_none_callbacks(self):
        """Test ResponsiveAppBar with None callbacks."""
        appbar = ResponsiveAppBar(title="Test")

        # Should not raise exception with None callbacks
        assert appbar.on_menu_click is None
        assert appbar.on_settings_click is None

    def test_with_empty_title(self):
        """Test ResponsiveAppBar with empty title."""
        appbar = ResponsiveAppBar(title="")

        assert appbar.title.value == ""
        assert isinstance(appbar.title, ft.Text)

    def test_with_long_title(self):
        """Test ResponsiveAppBar with long title."""
        long_title = "Very Long Application Title That Might Be Truncated"
        appbar = ResponsiveAppBar(title=long_title)

        assert appbar.title.value == long_title
        assert isinstance(appbar.title, ft.Text)

    def test_menu_button_click_simulation(self):
        """Test menu button click simulation."""
        on_menu_click = Mock()
        appbar = ResponsiveAppBar(title="Test", on_menu_click=on_menu_click)

        # Simulate menu button click
        mock_event = Mock()
        appbar.leading.on_click(mock_event)

        on_menu_click.assert_called_once_with(mock_event)

    def test_settings_click_handling(self):
        """Test settings menu item click handling."""
        on_settings_click = Mock()
        appbar = ResponsiveAppBar(title="Test", on_settings_click=on_settings_click)

        # Find settings menu item
        popup_menu = appbar.actions[0]
        settings_item = None
        for item in popup_menu.items:
            if hasattr(item, 'text') and item.text == "Settings":
                settings_item = item
                break

        assert settings_item is not None

        # Simulate settings click
        if settings_item.on_click:
            mock_event = Mock()
            settings_item.on_click(mock_event)
            on_settings_click.assert_called_once_with(mock_event)

    def test_responsive_behavior_configuration(self):
        """Test responsive behavior configuration."""
        appbar = ResponsiveAppBar(title="Test")

        # Should adapt to different screen sizes
        assert appbar.automatically_imply_leading is True
        assert isinstance(appbar.title, ft.Text)

    def test_accessibility_properties(self):
        """Test accessibility properties."""
        appbar = ResponsiveAppBar(title="Test App")

        # Menu button should have proper accessibility
        assert appbar.leading.icon == ft.Icons.MENU
        assert isinstance(appbar.leading, ft.IconButton)

        # Title should be readable
        assert appbar.title.value == "Test App"

    def test_multiple_instances_independence(self):
        """Test that multiple ResponsiveAppBar instances are independent."""
        callback1 = Mock()
        callback2 = Mock()

        appbar1 = ResponsiveAppBar(title="App1", on_menu_click=callback1)
        appbar2 = ResponsiveAppBar(title="App2", on_menu_click=callback2)

        assert appbar1.title.value == "App1"
        assert appbar2.title.value == "App2"
        assert appbar1.on_menu_click == callback1
        assert appbar2.on_menu_click == callback2
        assert appbar1 is not appbar2

    def test_inheritance_from_appbar(self):
        """Test that ResponsiveAppBar inherits from ft.AppBar."""
        appbar = ResponsiveAppBar(title="Test")

        assert isinstance(appbar, ft.AppBar)
        assert hasattr(appbar, 'title')
        assert hasattr(appbar, 'leading')
        assert hasattr(appbar, 'actions')

    def test_default_values_consistency(self):
        """Test consistency of default values."""
        appbar1 = ResponsiveAppBar(title="Test1")
        appbar2 = ResponsiveAppBar(title="Test2")

        # Both should have same default styling
        assert appbar1.bgcolor == appbar2.bgcolor
        assert appbar1.leading_width == appbar2.leading_width
        assert appbar1.center_title == appbar2.center_title

    def test_popup_menu_additional_items(self):
        """Test that popup menu can handle additional items."""
        appbar = ResponsiveAppBar(title="Test")
        popup_menu = appbar.actions[0]

        # Should have at least settings item
        menu_texts = [item.text for item in popup_menu.items if hasattr(item, 'text') and item.text]
        assert "Settings" in menu_texts

    def test_with_special_characters_in_title(self):
        """Test ResponsiveAppBar with special characters in title."""
        special_title = "App with ñáéíóú & symbols 🚀"
        appbar = ResponsiveAppBar(title=special_title)

        assert appbar.title.value == special_title
        assert isinstance(appbar.title, ft.Text)


class TestResponsiveAppBarEdgeCases:
    """Test edge cases and error scenarios for ResponsiveAppBar."""

    def test_with_callable_objects_as_callbacks(self):
        """Test ResponsiveAppBar with callable objects as callbacks."""
        class CallableClass:
            def __init__(self):
                self.called = False

            def __call__(self, event):
                self.called = True

        menu_callback = CallableClass()
        settings_callback = CallableClass()

        appbar = ResponsiveAppBar(
            title="Test",
            on_menu_click=menu_callback,
            on_settings_click=settings_callback
        )

        assert callable(appbar.on_menu_click)
        assert callable(appbar.on_settings_click)

    def test_parameter_mutation_independence(self):
        """Test that parameter mutations don't affect other instances."""
        title = "Original Title"
        appbar = ResponsiveAppBar(title=title)

        # Changing original title shouldn't affect appbar
        title = "Modified Title"
        assert appbar.title.value == "Original Title"

    def test_menu_button_properties(self):
        """Test menu button specific properties."""
        appbar = ResponsiveAppBar(title="Test")
        menu_button = appbar.leading

        assert isinstance(menu_button, ft.IconButton)
        assert menu_button.icon == ft.Icons.MENU
        assert menu_button.icon_size is None or isinstance(menu_button.icon_size, (int, float))

    def test_popup_menu_button_properties(self):
        """Test popup menu button specific properties."""
        appbar = ResponsiveAppBar(title="Test")
        popup_menu = appbar.actions[0]

        assert isinstance(popup_menu, ft.PopupMenuButton)
        assert popup_menu.icon == ft.Icons.MORE_VERT
        assert isinstance(popup_menu.items, list)

    def test_appbar_elevation_and_shadow(self):
        """Test AppBar elevation and shadow properties."""
        appbar = ResponsiveAppBar(title="Test")

        # Should have reasonable elevation for modern design
        assert appbar.elevation is not None
        assert appbar.bgcolor == ft.Colors.SURFACE