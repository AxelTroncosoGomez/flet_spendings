from typing import Optional, Callable
import flet as ft


class ResponsiveAppBar(ft.AppBar):
    """
    A responsive AppBar component that adapts to different screen sizes.

    Features:
    - Left side menu button (3 lines) for sidebar navigation
    - Right side popup menu (3 dots) for settings and other options
    - Responsive design that works on mobile and desktop
    - Clean architecture compliant with proper separation of concerns
    """

    def __init__(
        self,
        title: str,
        on_menu_click: Optional[Callable] = None,
        on_settings_click: Optional[Callable] = None
    ):
        """
        Initialize ResponsiveAppBar component

        Args:
            title: The title text to display in the AppBar
            on_menu_click: Callback function for menu button (sidebar toggle)
            on_settings_click: Callback function for settings menu item
        """
        self.on_menu_click = on_menu_click
        self.on_settings_click = on_settings_click

        super().__init__(
            leading=self._create_menu_button(),
            leading_width=56,
            title=ft.Text(
                value=title,
                size=20,
                weight=ft.FontWeight.W_500,
                color=ft.Colors.ON_SURFACE
            ),
            center_title=False,
            bgcolor=ft.Colors.SURFACE,
            elevation=2,
            actions=self._create_actions(),
            automatically_imply_leading=True
        )

    def _create_menu_button(self) -> ft.IconButton:
        """
        Create the menu button for the left side of the AppBar.

        Returns:
            ft.IconButton: Menu button with hamburger icon
        """
        return ft.IconButton(
            icon=ft.Icons.MENU,
            icon_size=24,
            icon_color=ft.Colors.ON_SURFACE,
            tooltip="Open menu",
            on_click=self.on_menu_click
        )

    def _create_actions(self) -> list:
        """
        Create the action buttons for the right side of the AppBar.

        Returns:
            list: List containing popup menu button with options
        """
        return [
            ft.PopupMenuButton(
                icon=ft.Icons.MORE_VERT,
                icon_size=24,
                icon_color=ft.Colors.ON_SURFACE,
                tooltip="More options",
                items=[
                    ft.PopupMenuItem(
                        text="Settings",
                        icon=ft.Icons.SETTINGS,
                        on_click=self.on_settings_click
                    ),
                    ft.PopupMenuItem(
                        text="Refresh",
                        icon=ft.Icons.REFRESH,
                        on_click=self.on_settings_click
                    ),
                    ft.PopupMenuItem(),  # Divider
                    ft.PopupMenuItem(
                        text="About",
                        icon=ft.Icons.INFO,
                        on_click=self._handle_about_click
                    ),
                ]
            )
        ]


    def _handle_about_click(self, e):
        """
        Handle about menu item click.

        Args:
            e: Click event
        """
        # This could be expanded to show app version, credits, etc.
        pass

    def update_title(self, new_title: str):
        """
        Update the AppBar title dynamically.

        Args:
            new_title: New title text to display
        """
        self.title.value = new_title

    def set_settings_callback(self, callback: Optional[Callable]):
        """
        Set or update the settings menu callback.

        Args:
            callback: New callback function for settings menu
        """
        self.on_settings_click = callback
        # Update the settings menu item callback
        for item in self.actions[0].items:
            if hasattr(item, 'text') and item.text == "Settings":
                item.on_click = callback
                break

    def set_menu_callback(self, callback: Optional[Callable]):
        """
        Set or update the menu button callback.

        Args:
            callback: New callback function for menu button
        """
        self.on_menu_click = callback
        self.leading.on_click = callback