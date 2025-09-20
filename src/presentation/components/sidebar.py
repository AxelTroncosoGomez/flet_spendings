from typing import Optional, Callable
import flet as ft


class Sidebar(ft.NavigationDrawer):
    """
    A responsive sidebar navigation component.

    Features:
    - Navigation options: Home, Spendings, Database, Profile
    - Logout button at the bottom
    - Clean architecture compliant design
    - Responsive layout for mobile and desktop
    """

    def __init__(
        self,
        on_home_click: Optional[Callable] = None,
        on_spendings_click: Optional[Callable] = None,
        on_database_click: Optional[Callable] = None,
        on_profile_click: Optional[Callable] = None,
        on_logout_click: Optional[Callable] = None
    ):
        """
        Initialize Sidebar component.

        Args:
            on_home_click: Callback for Home navigation
            on_spendings_click: Callback for Spendings navigation
            on_database_click: Callback for Database navigation
            on_profile_click: Callback for Profile navigation
            on_logout_click: Callback for Logout action
        """
        self.on_home_click = on_home_click
        self.on_spendings_click = on_spendings_click
        self.on_database_click = on_database_click
        self.on_profile_click = on_profile_click
        self.on_logout_click = on_logout_click

        super().__init__(
            elevation=40,
            selected_index=0,
            controls=[
                self._create_header(),
                ft.Divider(thickness=1, color=ft.Colors.OUTLINE),
                self._create_navigation_section(),
                ft.Divider(thickness=1, color=ft.Colors.OUTLINE),
                self._create_logout_section(),
            ],
            bgcolor=ft.Colors.SURFACE,
        )

    def _create_header(self) -> ft.Container:
        """
        Create the sidebar header with app branding.

        Returns:
            ft.Container: Header container with app information
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=20),  # Top spacing
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name=ft.Icons.MONETIZATION_ON,
                                size=32,
                                color=ft.Colors.PRIMARY
                            ),
                            ft.Text(
                                "Spendio",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ON_SURFACE
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=12,
                    ),
                    ft.Text(
                        "Personal Finance Tracker",
                        size=12,
                        color=ft.Colors.ON_SURFACE,
                        italic=True
                    ),
                    ft.Container(height=10),  # Bottom spacing
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
        )

    def _create_navigation_section(self) -> ft.Column:
        """
        Create the main navigation section with menu items.

        Returns:
            ft.Column: Navigation menu items
        """
        return ft.Column(
            controls=[
                self._create_nav_item(
                    icon=ft.Icons.HOME,
                    title="Home",
                    on_click=self._wrap_home_click
                ),
                self._create_nav_item(
                    icon=ft.Icons.MONETIZATION_ON,
                    title="Spendings",
                    on_click=self._wrap_spendings_click
                ),
                self._create_nav_item(
                    icon=ft.Icons.STORAGE,
                    title="Database",
                    on_click=self._wrap_database_click
                ),
                self._create_nav_item(
                    icon=ft.Icons.PERSON,
                    title="Profile",
                    on_click=self._wrap_profile_click
                ),
            ],
            spacing=4,
            tight=True,
        )

    def _create_logout_section(self) -> ft.Column:
        """
        Create the logout section at the bottom.

        Returns:
            ft.Column: Logout button section
        """
        return ft.Column(
            controls=[
                self._create_nav_item(
                    icon=ft.Icons.LOGOUT,
                    title="Logout",
                    on_click=self._wrap_logout_click,
                    is_logout=True
                ),
            ],
            spacing=4,
            tight=True,
        )

    def _create_nav_item(
        self,
        icon: ft.Icons,
        title: str,
        on_click: Optional[Callable] = None,
        is_logout: bool = False
    ) -> ft.ListTile:
        """
        Create a navigation menu item.

        Args:
            icon: Icon for the menu item
            title: Title text for the menu item
            on_click: Click callback for the menu item
            is_logout: Whether this is the logout item (for special styling)

        Returns:
            ft.ListTile: Navigation menu item
        """
        icon_color = ft.Colors.ERROR if is_logout else ft.Colors.ON_SURFACE
        text_color = ft.Colors.ERROR if is_logout else ft.Colors.ON_SURFACE

        return ft.ListTile(
            leading=ft.Icon(
                name=icon,
                size=24,
                color=icon_color
            ),
            title=ft.Text(
                value=title,
                size=16,
                weight=ft.FontWeight.W_400,
                color=text_color
            ),
            on_click=on_click,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=4),
            hover_color=ft.Colors.SURFACE if not is_logout else ft.Colors.RED_100,
        )

    def set_home_callback(self, callback: Optional[Callable]):
        """
        Set or update the home navigation callback.

        Args:
            callback: New callback function for home navigation
        """
        self.on_home_click = callback
        self._update_nav_item_callback("Home", callback)

    def set_spendings_callback(self, callback: Optional[Callable]):
        """
        Set or update the spendings navigation callback.

        Args:
            callback: New callback function for spendings navigation
        """
        self.on_spendings_click = callback
        self._update_nav_item_callback("Spendings", callback)

    def set_database_callback(self, callback: Optional[Callable]):
        """
        Set or update the database navigation callback.

        Args:
            callback: New callback function for database navigation
        """
        self.on_database_click = callback
        self._update_nav_item_callback("Database", callback)

    def set_profile_callback(self, callback: Optional[Callable]):
        """
        Set or update the profile navigation callback.

        Args:
            callback: New callback function for profile navigation
        """
        self.on_profile_click = callback
        self._update_nav_item_callback("Profile", callback)

    def set_logout_callback(self, callback: Optional[Callable]):
        """
        Set or update the logout callback.

        Args:
            callback: New callback function for logout action
        """
        self.on_logout_click = callback
        self._update_nav_item_callback("Logout", callback)

    def _update_nav_item_callback(self, title: str, callback: Optional[Callable]):
        """
        Update a navigation item's callback.

        Args:
            title: Title of the navigation item to update
            callback: New callback function
        """
        for control in self.controls:
            if isinstance(control, ft.Column):
                for item in control.controls:
                    if isinstance(item, ft.ListTile) and hasattr(item, 'title'):
                        if hasattr(item.title, 'value') and item.title.value == title:
                            item.on_click = callback
                            return

    def _wrap_home_click(self, e):
        """Wrap home click to close drawer first."""
        self._close_drawer()
        if self.on_home_click:
            self.on_home_click(e)

    def _wrap_spendings_click(self, e):
        """Wrap spendings click to close drawer first."""
        self._close_drawer()
        if self.on_spendings_click:
            self.on_spendings_click(e)

    def _wrap_database_click(self, e):
        """Wrap database click to close drawer first."""
        self._close_drawer()
        if self.on_database_click:
            self.on_database_click(e)

    def _wrap_profile_click(self, e):
        """Wrap profile click to close drawer first."""
        self._close_drawer()
        if self.on_profile_click:
            self.on_profile_click(e)

    def _wrap_logout_click(self, e):
        """Wrap logout click to close drawer first."""
        self._close_drawer()
        if self.on_logout_click:
            self.on_logout_click(e)

    def _close_drawer(self):
        """Close the drawer if page is available."""
        if self.page and hasattr(self.page, 'drawer'):
            try:
                self.page.drawer.open = False
                self.page.update()
            except Exception:
                pass

    def highlight_current_page(self, page_name: str):
        """
        Highlight the current page in the navigation.

        Args:
            page_name: Name of the current page to highlight
        """
        # This method can be expanded to highlight the current navigation item
        # by changing its background color or adding selection indicator
        pass