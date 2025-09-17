"""Base component classes for consistent UI architecture."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, Callable
import flet as ft

from shared.config import get_config
from infrastructure.container import get_container


class BaseComponent(ABC):
    """Abstract base class for all UI components."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.config = get_config()
        self.container = get_container()
        self._control: Optional[ft.Control] = None

    @abstractmethod
    def build(self) -> ft.Control:
        """Build and return the UI control."""
        pass

    def get_control(self) -> ft.Control:
        """Get the built control, building it if necessary."""
        if self._control is None:
            self._control = self.build()
        return self._control

    def refresh(self) -> None:
        """Refresh the component by rebuilding it."""
        self._control = None
        if self.page:
            self.page.update()

    def show_error(self, message: str) -> None:
        """Show error message to user."""
        from components.dialogs import error_message
        error_message(self.page, message)

    def show_success(self, message: str) -> None:
        """Show success message to user."""
        from components.dialogs import success_message
        success_message(self.page, message)

    def is_mobile(self) -> bool:
        """Check if running on mobile platform."""
        return self.page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]

    def is_web(self) -> bool:
        """Check if running on web platform."""
        return self.page.platform is None  # Web platform is None in Flet

    def is_desktop(self) -> bool:
        """Check if running on desktop platform."""
        return self.page.platform in [ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS]

    def get_responsive_width(self, mobile: float = 1.0, tablet: float = 0.8, desktop: float = 0.6) -> float:
        """Get responsive width based on platform."""
        if self.is_mobile():
            return mobile
        elif self.page.width and self.page.width > 768:
            return desktop
        else:
            return tablet


class BaseFormComponent(BaseComponent):
    """Base class for form components with validation."""

    def __init__(self, page: ft.Page):
        super().__init__(page)
        self._form_key = ft.Ref[ft.Form]()
        self._errors: Dict[str, str] = {}

    def validate_field(self, field_name: str, value: Any, validator: Callable[[Any], Optional[str]]) -> bool:
        """Validate a single field."""
        error = validator(value)
        if error:
            self._errors[field_name] = error
            return False
        else:
            self._errors.pop(field_name, None)
            return True

    def has_errors(self) -> bool:
        """Check if form has validation errors."""
        return len(self._errors) > 0

    def get_errors(self) -> Dict[str, str]:
        """Get all validation errors."""
        return self._errors.copy()

    def clear_errors(self) -> None:
        """Clear all validation errors."""
        self._errors.clear()

    def show_field_error(self, field_name: str) -> None:
        """Show error for a specific field."""
        if field_name in self._errors:
            self.show_error(self._errors[field_name])


class BasePageComponent(BaseComponent):
    """Base class for page-level components."""

    def __init__(self, page: ft.Page, title: str):
        super().__init__(page)
        self.title = title
        self._app_bar: Optional[ft.AppBar] = None
        self._body: Optional[ft.Control] = None

    @abstractmethod
    def build_body(self) -> ft.Control:
        """Build the page body content."""
        pass

    def build_app_bar(self) -> Optional[ft.AppBar]:
        """Build the app bar (override in subclasses if needed)."""
        return ft.AppBar(
            title=ft.Text(self.title),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

    def build(self) -> ft.Control:
        """Build the complete page structure."""
        self._app_bar = self.build_app_bar()
        self._body = self.build_body()

        # Set page properties
        self.page.title = self.title
        if self._app_bar:
            self.page.appbar = self._app_bar

        # Return the body as the main content
        return self._body

    def navigate_to(self, route: str) -> None:
        """Navigate to a different route."""
        self.page.go(route)

    def navigate_back(self) -> None:
        """Navigate back to previous page."""
        if len(self.page.route.split('/')) > 1:
            self.page.go('/')
        else:
            self.page.window_close()


class BaseDialogComponent(BaseComponent):
    """Base class for dialog components."""

    def __init__(self, page: ft.Page, title: str, modal: bool = True):
        super().__init__(page)
        self.title = title
        self.modal = modal
        self._dialog: Optional[ft.AlertDialog] = None
        self._is_open = False

    @abstractmethod
    def build_content(self) -> ft.Control:
        """Build the dialog content."""
        pass

    def build_actions(self) -> list[ft.Control]:
        """Build dialog action buttons (override in subclasses)."""
        return [
            ft.TextButton("Close", on_click=self.close)
        ]

    def build(self) -> ft.Control:
        """Build the dialog."""
        self._dialog = ft.AlertDialog(
            title=ft.Text(self.title),
            content=self.build_content(),
            actions=self.build_actions(),
            modal=self.modal,
        )
        return self._dialog

    def open(self) -> None:
        """Open the dialog."""
        if not self._is_open:
            dialog = self.get_control()
            self.page.dialog = dialog
            dialog.open = True
            self._is_open = True
            self.page.update()

    def close(self, e: Optional[ft.ControlEvent] = None) -> None:
        """Close the dialog."""
        if self._is_open and self._dialog:
            self._dialog.open = False
            self._is_open = False
            self.page.update()

    def is_open(self) -> bool:
        """Check if dialog is currently open."""
        return self._is_open