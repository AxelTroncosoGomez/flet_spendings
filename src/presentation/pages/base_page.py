from typing import Optional, Callable, List
import flet as ft
from presentation.components.responsive_appbar import ResponsiveAppBar
from presentation.components.sidebar import Sidebar
from utils.logger import logger


class BasePage(ft.View):
    """
    Base page template providing consistent AppBar and Sidebar structure.

    Features:
    - Responsive AppBar with menu toggle and settings
    - Navigation Sidebar with Home, Spendings, Database, Profile, Logout
    - Safe area wrapper for mobile compatibility
    - Extensible content area for page-specific content
    - Clean architecture compliant design
    """

    def __init__(
        self,
        page: ft.Page,
        route: str,
        title: str,
        supabase_service=None,
        on_home_click: Optional[Callable] = None,
        on_spendings_click: Optional[Callable] = None,
        on_database_click: Optional[Callable] = None,
        on_profile_click: Optional[Callable] = None,
        on_logout_click: Optional[Callable] = None,
        on_settings_click: Optional[Callable] = None
    ):
        """
        Initialize BasePage with common structure.

        Args:
            page: Flet page instance
            route: Route path for this page
            title: Page title for AppBar
            supabase_service: Optional Supabase service instance
            on_home_click: Callback for Home navigation
            on_spendings_click: Callback for Spendings navigation
            on_database_click: Callback for Database navigation
            on_profile_click: Callback for Profile navigation
            on_logout_click: Callback for Logout action
            on_settings_click: Callback for Settings action
        """
        super().__init__(
            route=route,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

        self.page = page
        self.title = title
        self.supabase_service = supabase_service

        # Store callbacks for navigation
        self.on_home_click = on_home_click or self._default_home_click
        self.on_spendings_click = on_spendings_click or self._default_spendings_click
        self.on_database_click = on_database_click or self._default_database_click
        self.on_profile_click = on_profile_click or self._default_profile_click
        self.on_logout_click = on_logout_click or self._default_logout_click
        self.on_settings_click = on_settings_click or self._default_settings_click

        # Create responsive AppBar and Sidebar
        self._create_navigation_components()

        # Set up base layout structure (defer content creation)
        self._setup_layout()

    def _create_navigation_components(self):
        """Create the AppBar and Sidebar components."""
        self.drawer = Sidebar(
            on_home_click=self.on_home_click,
            on_spendings_click=self.on_spendings_click,
            on_database_click=self.on_database_click,
            on_profile_click=self.on_profile_click,
            on_logout_click=self.on_logout_click
        )

        self.appbar = ResponsiveAppBar(
            title=self.title,
            on_menu_click=self._handle_menu_click,
            on_settings_click=self.on_settings_click
        )

    def _setup_layout(self):
        """Set up the base layout structure with content area."""
        # Create content area without content initially (avoid calling overridden method during init)
        self.content_area = ft.Container(
            content=ft.Column(
                controls=[],  # Start empty, will be populated later
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            padding=20,
            expand=True
        )

        self.controls = [
            ft.SafeArea(
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=self.content_area,
                            col={"sm": 12, "md": 10, "lg": 8, "xl": 6},
                            alignment=ft.alignment.center
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                expand=True
            )
        ]

    def _get_page_content(self) -> List[ft.Control]:
        """
        Override this method in subclasses to provide page-specific content.

        Returns:
            List of Flet controls for the page content
        """
        return [
            ft.Text(
                f"Welcome to {self.title}",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_SURFACE
            ),
            ft.Text(
                "This is a base page template. Override _get_page_content() to add content.",
                size=16,
                color=ft.Colors.ON_SURFACE_VARIANT,
                text_align=ft.TextAlign.CENTER
            )
        ]

    def _handle_menu_click(self, e):
        """Handle menu button click to toggle sidebar."""
        try:
            current_drawer_state = getattr(self.drawer, 'open', False)
            self.drawer.open = not current_drawer_state
            self.drawer.update()
        except Exception as err:
            logger.error(f"Error toggling sidebar: {err}")
            if self.page:
                self.page.update()

    def _default_home_click(self, e):
        """Default home navigation handler."""
        try:
            if self.page:
                self.page.go("/home")
        except Exception as err:
            logger.error(f"Error navigating to home: {err}")
            if self.page:
                self.page.update()

    def _default_spendings_click(self, e):
        """Default spendings navigation handler."""
        try:
            if self.page:
                self.page.go("/spendings")
        except Exception as err:
            logger.error(f"Error navigating to spendings: {err}")
            if self.page:
                self.page.update()

    def _default_database_click(self, e):
        """Default database navigation handler."""
        try:
            if self.page:
                self.page.go("/database")
        except Exception as err:
            logger.error(f"Error navigating to database: {err}")
            if self.page:
                self.page.update()

    def _default_profile_click(self, e):
        """Default profile navigation handler."""
        try:
            if self.page:
                self.page.go("/profile")
        except Exception as err:
            logger.error(f"Error navigating to profile: {err}")
            if self.page:
                self.page.update()

    def _default_logout_click(self, e):
        """Default logout handler."""
        try:
            # This should be overridden in subclasses to implement actual logout logic
            logger.info("Logout action triggered")
            if self.page:
                self.page.go("/login")
        except Exception as err:
            logger.error(f"Error during logout: {err}")
            if self.page:
                self.page.update()

    def _default_settings_click(self, e):
        """Default settings handler."""
        try:
            # This should be overridden in subclasses to implement settings functionality
            logger.info("Settings action triggered")
        except Exception as err:
            logger.error(f"Error opening settings: {err}")
            if self.page:
                self.page.update()

    def update_title(self, new_title: str):
        """
        Update the page title dynamically.

        Args:
            new_title: New title for the AppBar
        """
        try:
            self.title = new_title
            if hasattr(self, 'appbar'):
                self.appbar.update_title(new_title)
        except Exception as err:
            logger.error(f"Error updating title: {err}")

    def set_content(self, content: List[ft.Control]):
        """
        Set page-specific content after initialization.

        Args:
            content: List of Flet controls for the page content
        """
        try:
            if hasattr(self, 'content_area') and self.content_area.content:
                self.content_area.content.controls = content
                if self.page:
                    self.page.update()
        except Exception as err:
            logger.error(f"Error setting content: {err}")

    def add_content(self, control: ft.Control):
        """
        Add a single control to the page content.

        Args:
            control: Flet control to add to the page
        """
        try:
            if hasattr(self, 'content_area') and self.content_area.content:
                self.content_area.content.controls.append(control)
                if self.page:
                    self.page.update()
        except Exception as err:
            logger.error(f"Error adding content: {err}")

    def highlight_current_navigation(self, page_name: str):
        """
        Highlight the current page in the sidebar navigation.

        Args:
            page_name: Name of the current page to highlight
        """
        try:
            if hasattr(self, 'drawer'):
                self.drawer.highlight_current_page(page_name)
        except Exception as err:
            logger.error(f"Error highlighting navigation: {err}")

    def _populate_content(self):
        """
        Populate the content area with page-specific content.
        Call this method after subclass initialization is complete.
        """
        try:
            if hasattr(self, 'content_area') and self.content_area.content:
                self.content_area.content.controls = self._get_page_content()
        except Exception as err:
            logger.error(f"Error populating content: {err}")
            if hasattr(self, 'content_area') and self.content_area.content:
                self.content_area.content.controls = [
                    ft.Text(
                        "Error loading page content",
                        size=16,
                        color=ft.Colors.ERROR
                    )
                ]