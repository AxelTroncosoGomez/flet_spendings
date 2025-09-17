import pytest
import flet as ft
from unittest.mock import Mock
from components.dialogs import (
    _get_snackbar_width,
    _get_snackbar_behavior,
    _get_snackbar_margin,
    _get_snackbar_alignment,
    sucess_message,
    error_message,
    LOGIN_CARD_WIDTH,
    BOTTOM_RIGHT_MARGIN
)


class TestSnackbarBasicFunctionality:
    """Test suite for basic snackbar functionality."""

    def test_snackbar_width_is_always_login_card_width(self):
        """Test that snackbar width is always constrained to login card width."""
        # Test with no page
        assert _get_snackbar_width(None) == LOGIN_CARD_WIDTH

        # Test with Android
        mock_page_android = Mock()
        mock_page_android.platform = ft.PagePlatform.ANDROID
        assert _get_snackbar_width(mock_page_android) == LOGIN_CARD_WIDTH

        # Test with Windows
        mock_page_windows = Mock()
        mock_page_windows.platform = ft.PagePlatform.WINDOWS
        assert _get_snackbar_width(mock_page_windows) == LOGIN_CARD_WIDTH

    def test_snackbar_never_full_width(self):
        """Test that snackbars are never allowed to be full width."""
        platforms = [
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
            ft.PagePlatform.WINDOWS,
            ft.PagePlatform.LINUX,
            ft.PagePlatform.MACOS
        ]

        for platform in platforms:
            mock_page = Mock()
            mock_page.platform = platform

            success_snackbar = sucess_message("Test", page=mock_page)
            error_snackbar = error_message("Test", page=mock_page)

            # Width should always be set and never None (which would mean full width)
            assert success_snackbar.width is not None
            assert error_snackbar.width is not None
            assert success_snackbar.width == LOGIN_CARD_WIDTH
            assert error_snackbar.width == LOGIN_CARD_WIDTH

    def test_mobile_platforms_use_symmetric_margin(self):
        """Test that mobile platforms use symmetric margin."""
        mobile_platforms = [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]

        for platform in mobile_platforms:
            mock_page = Mock()
            mock_page.platform = platform

            margin = _get_snackbar_margin(mock_page)
            # Should be symmetric margin for mobile - check that it has left/right properties
            assert hasattr(margin, 'left') and hasattr(margin, 'right') and hasattr(margin, 'top') and hasattr(margin, 'bottom')
            # For mobile, left and right should be equal (symmetric)
            assert margin.left == margin.right

    def test_desktop_platforms_use_bottom_right_margin(self):
        """Test that desktop platforms use bottom-right margin."""
        desktop_platforms = [ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS]

        for platform in desktop_platforms:
            mock_page = Mock()
            mock_page.platform = platform

            margin = _get_snackbar_margin(mock_page)
            # Should be bottom-right margin for desktop - check properties
            assert hasattr(margin, 'left') and hasattr(margin, 'right') and hasattr(margin, 'top') and hasattr(margin, 'bottom')
            # For desktop, should have right and bottom margins but minimal left/top
            assert margin.right > 0
            assert margin.bottom > 0
            assert margin.left == 0
            assert margin.top == 0

    def test_mobile_platforms_use_default_alignment(self):
        """Test that mobile platforms use default alignment."""
        mobile_platforms = [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]

        for platform in mobile_platforms:
            mock_page = Mock()
            mock_page.platform = platform
            alignment = _get_snackbar_alignment(mock_page)
            assert alignment is None  # Default alignment for mobile

    def test_desktop_platforms_use_bottom_right_alignment(self):
        """Test that desktop platforms use bottom-right alignment."""
        desktop_platforms = [ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS]

        for platform in desktop_platforms:
            mock_page = Mock()
            mock_page.platform = platform
            alignment = _get_snackbar_alignment(mock_page)
            assert alignment == ft.alignment.bottom_right

    def test_unknown_platform_defaults_to_bottom_right(self):
        """Test that unknown platforms (like web) default to bottom-right positioning."""
        mock_page = Mock()
        mock_page.platform = None  # Web doesn't have specific platform

        margin = _get_snackbar_margin(mock_page)
        alignment = _get_snackbar_alignment(mock_page)

        # Should default to bottom-right behavior
        assert hasattr(margin, 'left') and hasattr(margin, 'right') and hasattr(margin, 'top') and hasattr(margin, 'bottom')
        assert margin.right > 0
        assert margin.bottom > 0
        assert alignment == ft.alignment.bottom_right


class TestSnackbarCreation:
    """Test suite for snackbar creation."""

    def test_success_message_properties(self):
        """Test success message has correct properties."""
        message = "Test success"
        snackbar = sucess_message(message)

        assert isinstance(snackbar, ft.SnackBar)
        assert snackbar.bgcolor == "#193526"
        assert snackbar.width == LOGIN_CARD_WIDTH
        assert snackbar.duration == 3000
        assert snackbar.show_close_icon == False
        assert snackbar.behavior == ft.SnackBarBehavior.FLOATING

        # Check content structure
        assert isinstance(snackbar.content, ft.Row)
        assert len(snackbar.content.controls) == 2
        assert isinstance(snackbar.content.controls[0], ft.Icon)
        assert isinstance(snackbar.content.controls[1], ft.Text)
        assert snackbar.content.controls[0].name == ft.Icons.CHECK_CIRCLE
        assert snackbar.content.controls[0].color == "#7AF5B7"
        assert snackbar.content.controls[1].value == message
        assert snackbar.content.controls[1].color == "#7AF5B7"

    def test_error_message_properties(self):
        """Test error message has correct properties."""
        message = "Test error"
        snackbar = error_message(message)

        assert isinstance(snackbar, ft.SnackBar)
        assert snackbar.bgcolor == "#2d0607"
        assert snackbar.width == LOGIN_CARD_WIDTH
        assert snackbar.duration == 3000
        assert snackbar.show_close_icon == False
        assert snackbar.behavior == ft.SnackBarBehavior.FLOATING

        # Check content structure
        assert isinstance(snackbar.content, ft.Row)
        assert len(snackbar.content.controls) == 2
        assert isinstance(snackbar.content.controls[0], ft.Icon)
        assert isinstance(snackbar.content.controls[1], ft.Text)
        assert snackbar.content.controls[0].name == ft.Icons.INFO_ROUNDED
        assert snackbar.content.controls[0].color == "#e48c92"
        assert snackbar.content.controls[1].value == message
        assert snackbar.content.controls[1].color == "#e48c92"
        assert snackbar.content.controls[1].weight == ft.FontWeight.BOLD

    def test_custom_duration(self):
        """Test custom duration works."""
        duration = 5000
        success_snackbar = sucess_message("Test", duration=duration)
        error_snackbar = error_message("Test", duration=duration)

        assert success_snackbar.duration == duration
        assert error_snackbar.duration == duration

    def test_empty_message_handling(self):
        """Test handling of empty messages."""
        success_snackbar = sucess_message("")
        error_snackbar = error_message("")

        assert success_snackbar.content.controls[1].value == ""
        assert error_snackbar.content.controls[1].value == ""

    def test_very_long_message_handling(self):
        """Test handling of very long messages."""
        long_message = "This is a very long message " * 20

        success_snackbar = sucess_message(long_message)
        error_snackbar = error_message(long_message)

        assert success_snackbar.content.controls[1].value == long_message
        assert error_snackbar.content.controls[1].value == long_message
        # Width should still be constrained
        assert success_snackbar.width == LOGIN_CARD_WIDTH
        assert error_snackbar.width == LOGIN_CARD_WIDTH


class TestConstants:
    """Test suite for constants."""

    def test_constants_have_reasonable_values(self):
        """Test that constants have reasonable values."""
        assert LOGIN_CARD_WIDTH > 0
        assert LOGIN_CARD_WIDTH == 360  # Should match login card width
        assert BOTTOM_RIGHT_MARGIN > 0
        assert BOTTOM_RIGHT_MARGIN <= 50  # Should be reasonable margin


class TestPlatformSpecificBehavior:
    """Test suite for platform-specific behavior."""

    def test_android_positioning(self):
        """Test Android-specific positioning."""
        mock_page = Mock()
        mock_page.platform = ft.PagePlatform.ANDROID

        # Test all functions return appropriate values for Android
        width = _get_snackbar_width(mock_page)
        behavior = _get_snackbar_behavior(mock_page)
        margin = _get_snackbar_margin(mock_page)
        alignment = _get_snackbar_alignment(mock_page)

        assert width == LOGIN_CARD_WIDTH
        assert behavior == ft.SnackBarBehavior.FLOATING
        assert alignment is None  # Default alignment for mobile

        # Create actual snackbars and test them
        success_snackbar = sucess_message("Test", page=mock_page)
        error_snackbar = error_message("Test", page=mock_page)

        assert success_snackbar.width == LOGIN_CARD_WIDTH
        assert error_snackbar.width == LOGIN_CARD_WIDTH

    def test_windows_positioning(self):
        """Test Windows-specific positioning."""
        mock_page = Mock()
        mock_page.platform = ft.PagePlatform.WINDOWS

        # Test all functions return appropriate values for Windows
        width = _get_snackbar_width(mock_page)
        behavior = _get_snackbar_behavior(mock_page)
        margin = _get_snackbar_margin(mock_page)
        alignment = _get_snackbar_alignment(mock_page)

        assert width == LOGIN_CARD_WIDTH
        assert behavior == ft.SnackBarBehavior.FLOATING
        assert alignment == ft.alignment.bottom_right

        # Create actual snackbars and test them
        success_snackbar = sucess_message("Test", page=mock_page)
        error_snackbar = error_message("Test", page=mock_page)

        assert success_snackbar.width == LOGIN_CARD_WIDTH
        assert error_snackbar.width == LOGIN_CARD_WIDTH