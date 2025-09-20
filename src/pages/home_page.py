from typing import Optional, Callable, List
import flet as ft
from presentation.pages.base_page import BasePage
from utils.logger import logger


class HomePage(BasePage):
    """
    Home page for the Spendio application.

    Features:
    - Welcome dashboard with overview cards
    - Quick action buttons for common tasks
    - Recent activity summary
    - Uses BasePage template for consistent AppBar and Sidebar
    """

    def __init__(
        self,
        page: ft.Page,
        supabase_service=None,
        on_home_click: Optional[Callable] = None,
        on_spendings_click: Optional[Callable] = None,
        on_database_click: Optional[Callable] = None,
        on_profile_click: Optional[Callable] = None,
        on_logout_click: Optional[Callable] = None,
        on_settings_click: Optional[Callable] = None
    ):
        """
        Initialize HomePage with base template structure.

        Args:
            page: Flet page instance
            supabase_service: Optional Supabase service instance
            on_home_click: Callback for Home navigation
            on_spendings_click: Callback for Spendings navigation
            on_database_click: Callback for Database navigation
            on_profile_click: Callback for Profile navigation
            on_logout_click: Callback for Logout action
            on_settings_click: Callback for Settings action
        """
        super().__init__(
            page=page,
            route="/home",
            title="Spendio - Home",
            supabase_service=supabase_service,
            on_home_click=on_home_click,
            on_spendings_click=on_spendings_click,
            on_database_click=on_database_click,
            on_profile_click=on_profile_click,
            on_logout_click=on_logout_click,
            on_settings_click=on_settings_click
        )

        # Highlight current page in navigation
        self.highlight_current_navigation("Home")

        # Populate content after initialization is complete
        self._populate_content()

    def _get_page_content(self) -> List[ft.Control]:
        """
        Override to provide Home page specific content.

        Returns:
            List of Flet controls for the Home page content
        """
        try:
            return [
                self._create_welcome_section(),
                self._create_overview_cards(),
                self._create_quick_actions(),
                self._create_recent_activity(),
            ]
        except Exception as err:
            logger.error(f"Error creating home page content: {err}")
            return [
                ft.Text(
                    "Error loading home page content",
                    size=16,
                    color=ft.Colors.ERROR
                )
            ]

    def _create_welcome_section(self) -> ft.Container:
        """
        Create welcome section with user greeting.

        Returns:
            ft.Container: Welcome section container
        """
        user_name = "User"  # TODO: Get from supabase_service or session
        current_time = "Good day"  # TODO: Implement time-based greeting

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"{current_time}, {user_name}!",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.Text(
                        "Welcome to your personal finance dashboard",
                        size=16,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                        text_align=ft.TextAlign.CENTER
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
            ),
            padding=ft.padding.symmetric(vertical=20),
            alignment=ft.alignment.center
        )

    def _create_overview_cards(self) -> ft.ResponsiveRow:
        """
        Create overview cards with financial summary.

        Returns:
            ft.ResponsiveRow: Overview cards container
        """
        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self._create_card(
                        title="Total Spendings",
                        value="$1,234.56",  # TODO: Get from database
                        icon=ft.Icons.MONETIZATION_ON,
                        color=ft.Colors.PRIMARY
                    ),
                    col={"sm": 12, "md": 6, "lg": 3}
                ),
                ft.Container(
                    content=self._create_card(
                        title="This Month",
                        value="$345.67",  # TODO: Get from database
                        icon=ft.Icons.CALENDAR_MONTH,
                        color=ft.Colors.SECONDARY
                    ),
                    col={"sm": 12, "md": 6, "lg": 3}
                ),
                ft.Container(
                    content=self._create_card(
                        title="Entries",
                        value="42",  # TODO: Get from database
                        icon=ft.Icons.RECEIPT_LONG,
                        color=ft.Colors.TERTIARY
                    ),
                    col={"sm": 12, "md": 6, "lg": 3}
                ),
                ft.Container(
                    content=self._create_card(
                        title="Categories",
                        value="8",  # TODO: Get from database
                        icon=ft.Icons.CATEGORY,
                        color=ft.Colors.OUTLINE
                    ),
                    col={"sm": 12, "md": 6, "lg": 3}
                ),
            ],
            spacing=16,
            run_spacing=16
        )

    def _create_card(
        self,
        title: str,
        value: str,
        icon: ft.Icons,
        color: ft.Colors
    ) -> ft.Card:
        """
        Create a summary card for the overview section.

        Args:
            title: Card title
            value: Card value to display
            icon: Icon for the card
            color: Theme color for the card

        Returns:
            ft.Card: Summary card
        """
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name=icon,
                                    size=32,
                                    color=color
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            title,
                                            size=14,
                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                            weight=ft.FontWeight.W_400
                                        ),
                                        ft.Text(
                                            value,
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.ON_SURFACE
                                        ),
                                    ],
                                    spacing=4,
                                    expand=True
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=16
                        )
                    ],
                    spacing=8
                ),
                padding=20,
                alignment=ft.alignment.center_left
            ),
            elevation=2
        )

    def _create_quick_actions(self) -> ft.Container:
        """
        Create quick action buttons for common tasks.

        Returns:
            ft.Container: Quick actions container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Quick Actions",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Add Spending",
                                    icon=ft.Icons.ADD_CIRCLE,
                                    on_click=self._handle_add_spending,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(
                                            horizontal=24, vertical=16
                                        )
                                    )
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="View Spendings",
                                    icon=ft.Icons.LIST_ALT,
                                    on_click=self._handle_view_spendings,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(
                                            horizontal=24, vertical=16
                                        )
                                    )
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Database",
                                    icon=ft.Icons.STORAGE,
                                    on_click=self._handle_view_database,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(
                                            horizontal=24, vertical=16
                                        )
                                    )
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                        ],
                        spacing=16,
                        run_spacing=16
                    )
                ],
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            padding=ft.padding.symmetric(vertical=20)
        )

    def _create_recent_activity(self) -> ft.Container:
        """
        Create recent activity section.

        Returns:
            ft.Container: Recent activity container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Recent Activity",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    self._create_activity_item(
                                        "Grocery Store",
                                        "$85.43",
                                        "2 hours ago",
                                        ft.Icons.LOCAL_GROCERY_STORE
                                    ),
                                    ft.Divider(height=1),
                                    self._create_activity_item(
                                        "Gas Station",
                                        "$45.20",
                                        "1 day ago",
                                        ft.Icons.LOCAL_GAS_STATION
                                    ),
                                    ft.Divider(height=1),
                                    self._create_activity_item(
                                        "Restaurant",
                                        "$32.15",
                                        "2 days ago",
                                        ft.Icons.RESTAURANT
                                    ),
                                    ft.Container(
                                        content=ft.TextButton(
                                            text="View All Spendings",
                                            icon=ft.Icons.ARROW_FORWARD,
                                            on_click=self._handle_view_spendings
                                        ),
                                        alignment=ft.alignment.center,
                                        padding=ft.padding.only(top=10)
                                    )
                                ],
                                spacing=8
                            ),
                            padding=20
                        ),
                        elevation=2
                    )
                ],
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            padding=ft.padding.symmetric(vertical=20)
        )

    def _create_activity_item(
        self,
        store: str,
        amount: str,
        time: str,
        icon: ft.Icons
    ) -> ft.Row:
        """
        Create a single activity item.

        Args:
            store: Store name
            amount: Spending amount
            time: Time ago string
            icon: Icon for the activity

        Returns:
            ft.Row: Activity item row
        """
        return ft.Row(
            controls=[
                ft.Icon(
                    name=icon,
                    size=24,
                    color=ft.Colors.PRIMARY
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            store,
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.ON_SURFACE
                        ),
                        ft.Text(
                            time,
                            size=12,
                            color=ft.Colors.ON_SURFACE_VARIANT
                        ),
                    ],
                    spacing=2,
                    expand=True
                ),
                ft.Text(
                    amount,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ON_SURFACE
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=16
        )

    def _handle_add_spending(self, e):
        """Handle add spending button click."""
        try:
            # TODO: Open add spending dialog or navigate to spendings page with dialog
            if self.page:
                self.page.go("/spendings")
                # TODO: Trigger add dialog on spendings page
        except Exception as err:
            logger.error(f"Error handling add spending: {err}")

    def _handle_view_spendings(self, e):
        """Handle view spendings button click."""
        try:
            if self.on_spendings_click:
                self.on_spendings_click(e)
            elif self.page:
                self.page.go("/spendings")
        except Exception as err:
            logger.error(f"Error handling view spendings: {err}")

    def _handle_view_database(self, e):
        """Handle view database button click."""
        try:
            if self.on_database_click:
                self.on_database_click(e)
            elif self.page:
                self.page.go("/database")
        except Exception as err:
            logger.error(f"Error handling view database: {err}")

    def refresh_data(self):
        """
        Refresh home page data from database.
        TODO: Implement actual data fetching and update UI.
        """
        try:
            # TODO: Fetch recent data from supabase_service
            # TODO: Update overview cards with real data
            # TODO: Update recent activity with real data
            if self.page:
                self.page.update()
        except Exception as err:
            logger.error(f"Error refreshing home page data: {err}")

    def set_user_info(self, user_name: str = None, user_email: str = None):
        """
        Set user information for personalized welcome.

        Args:
            user_name: User's display name
            user_email: User's email address
        """
        try:
            # TODO: Update welcome section with user info
            # TODO: Store user info for greeting updates
            pass
        except Exception as err:
            logger.error(f"Error setting user info: {err}")