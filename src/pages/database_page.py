from typing import Optional, Callable, List, Dict, Any
import flet as ft
from presentation.pages.base_page import BasePage
from utils.logger import logger


class DatabasePage(BasePage):
    """
    Database management page for the Spendio application.

    Features:
    - Database statistics and information
    - Data management tools (backup, export, import)
    - Database health monitoring
    - Advanced search and filtering
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
        Initialize DatabasePage with base template structure.

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
            route="/database",
            title="Spendio - Database",
            supabase_service=supabase_service,
            on_home_click=on_home_click,
            on_spendings_click=on_spendings_click,
            on_database_click=on_database_click,
            on_profile_click=on_profile_click,
            on_logout_click=on_logout_click,
            on_settings_click=on_settings_click
        )

        # Initialize database statistics
        self.db_stats = {
            "total_entries": 0,
            "total_amount": 0.0,
            "unique_stores": 0,
            "date_range": "No data",
            "last_backup": "Never",
            "database_size": "0 MB"
        }

        # Highlight current page in navigation
        self.highlight_current_navigation("Database")

        # Populate content after initialization is complete
        self._populate_content()

    def _get_page_content(self) -> List[ft.Control]:
        """
        Override to provide Database page specific content.

        Returns:
            List of Flet controls for the Database page content
        """
        try:
            return [
                self._create_database_overview(),
                self._create_statistics_section(),
                self._create_management_tools(),
                self._create_advanced_search(),
            ]
        except Exception as err:
            logger.error(f"Error creating database page content: {err}")
            return [
                ft.Text(
                    "Error loading database page content",
                    size=16,
                    color=ft.Colors.ERROR
                )
            ]

    def _create_database_overview(self) -> ft.Container:
        """
        Create database overview section.

        Returns:
            ft.Container: Database overview container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Database Management",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.Text(
                        "Monitor and manage your spending data",
                        size=16,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        name=ft.Icons.STORAGE,
                                        size=40,
                                        color=ft.Colors.PRIMARY
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Database Status",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.ON_SURFACE
                                            ),
                                            ft.Text(
                                                "Connected and operational",  # TODO: Get from service
                                                size=14,
                                                color=ft.Colors.GREEN
                                            ),
                                        ],
                                        spacing=4,
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Icon(
                                            name=ft.Icons.CHECK_CIRCLE,
                                            size=32,
                                            color=ft.Colors.GREEN
                                        ),
                                        alignment=ft.alignment.center_right
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=16
                            ),
                            padding=20
                        ),
                        elevation=2
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16
            ),
            padding=ft.padding.symmetric(vertical=20)
        )

    def _create_statistics_section(self) -> ft.Container:
        """
        Create database statistics section.

        Returns:
            ft.Container: Statistics section container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Database Statistics",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Total Entries",
                                    value=str(self.db_stats["total_entries"]),
                                    icon=ft.Icons.RECEIPT_LONG,
                                    color=ft.Colors.PRIMARY
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Total Amount",
                                    value=f"${self.db_stats['total_amount']:.2f}",
                                    icon=ft.Icons.MONETIZATION_ON,
                                    color=ft.Colors.SECONDARY
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Unique Stores",
                                    value=str(self.db_stats["unique_stores"]),
                                    icon=ft.Icons.STORE,
                                    color=ft.Colors.TERTIARY
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Date Range",
                                    value=self.db_stats["date_range"],
                                    icon=ft.Icons.DATE_RANGE,
                                    color=ft.Colors.OUTLINE
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Database Size",
                                    value=self.db_stats["database_size"],
                                    icon=ft.Icons.STORAGE,
                                    color=ft.Colors.PRIMARY
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Last Backup",
                                    value=self.db_stats["last_backup"],
                                    icon=ft.Icons.BACKUP,
                                    color=ft.Colors.ORANGE
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

    def _create_stat_card(
        self,
        title: str,
        value: str,
        icon: ft.Icons,
        color: ft.Colors
    ) -> ft.Card:
        """
        Create a statistics card.

        Args:
            title: Card title
            value: Statistic value to display
            icon: Icon for the card
            color: Theme color for the card

        Returns:
            ft.Card: Statistics card
        """
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name=icon,
                                    size=28,
                                    color=color
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            title,
                                            size=12,
                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                            weight=ft.FontWeight.W_400
                                        ),
                                        ft.Text(
                                            value,
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.ON_SURFACE
                                        ),
                                    ],
                                    spacing=4,
                                    expand=True
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=12
                        )
                    ],
                    spacing=8
                ),
                padding=16,
                alignment=ft.alignment.center_left
            ),
            elevation=1
        )

    def _create_management_tools(self) -> ft.Container:
        """
        Create database management tools section.

        Returns:
            ft.Container: Management tools container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Management Tools",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Backup Data",
                                    icon=ft.Icons.BACKUP,
                                    on_click=self._handle_backup_data,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(
                                            horizontal=24, vertical=16
                                        ),
                                        bgcolor=ft.Colors.PRIMARY
                                    )
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Export Data",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=self._handle_export_data,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(
                                            horizontal=24, vertical=16
                                        ),
                                        bgcolor=ft.Colors.SECONDARY
                                    )
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Import Data",
                                    icon=ft.Icons.UPLOAD,
                                    on_click=self._handle_import_data,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(
                                            horizontal=24, vertical=16
                                        ),
                                        bgcolor=ft.Colors.TERTIARY
                                    )
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Optimize DB",
                                    icon=ft.Icons.TUNE,
                                    on_click=self._handle_optimize_database,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(
                                            horizontal=24, vertical=16
                                        ),
                                        bgcolor=ft.Colors.OUTLINE
                                    )
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Clean Data",
                                    icon=ft.Icons.CLEANING_SERVICES,
                                    on_click=self._handle_clean_data,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(
                                            horizontal=24, vertical=16
                                        ),
                                        bgcolor=ft.Colors.ORANGE
                                    )
                                ),
                                col={"sm": 12, "md": 6, "lg": 4}
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="Refresh Stats",
                                    icon=ft.Icons.REFRESH,
                                    on_click=self._handle_refresh_stats,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(
                                            horizontal=24, vertical=16
                                        ),
                                        bgcolor=ft.Colors.GREEN
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

    def _create_advanced_search(self) -> ft.Container:
        """
        Create advanced search and filtering section.

        Returns:
            ft.Container: Advanced search container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Advanced Search",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.ResponsiveRow(
                                        controls=[
                                            ft.Container(
                                                content=ft.TextField(
                                                    label="Search stores",
                                                    hint_text="Enter store name...",
                                                    border_radius=8
                                                ),
                                                col={"sm": 12, "md": 6, "lg": 4}
                                            ),
                                            ft.Container(
                                                content=ft.TextField(
                                                    label="Search products",
                                                    hint_text="Enter product name...",
                                                    border_radius=8
                                                ),
                                                col={"sm": 12, "md": 6, "lg": 4}
                                            ),
                                            ft.Container(
                                                content=ft.TextField(
                                                    label="Amount range",
                                                    hint_text="e.g., 10-100",
                                                    border_radius=8
                                                ),
                                                col={"sm": 12, "md": 6, "lg": 4}
                                            ),
                                        ],
                                        spacing=16,
                                        run_spacing=16
                                    ),
                                    ft.ResponsiveRow(
                                        controls=[
                                            ft.Container(
                                                content=ft.TextField(
                                                    label="Date from",
                                                    hint_text="DD-MM-YYYY",
                                                    border_radius=8
                                                ),
                                                col={"sm": 12, "md": 6, "lg": 6}
                                            ),
                                            ft.Container(
                                                content=ft.TextField(
                                                    label="Date to",
                                                    hint_text="DD-MM-YYYY",
                                                    border_radius=8
                                                ),
                                                col={"sm": 12, "md": 6, "lg": 6}
                                            ),
                                        ],
                                        spacing=16,
                                        run_spacing=16
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                text="Search",
                                                icon=ft.Icons.SEARCH,
                                                on_click=self._handle_advanced_search,
                                                style=ft.ButtonStyle(
                                                    padding=ft.padding.symmetric(
                                                        horizontal=24, vertical=12
                                                    )
                                                )
                                            ),
                                            ft.OutlinedButton(
                                                text="Clear",
                                                icon=ft.Icons.CLEAR,
                                                on_click=self._handle_clear_search,
                                                style=ft.ButtonStyle(
                                                    padding=ft.padding.symmetric(
                                                        horizontal=24, vertical=12
                                                    )
                                                )
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        spacing=16
                                    )
                                ],
                                spacing=20
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

    def _handle_backup_data(self, e):
        """Handle backup data button click."""
        try:
            # TODO: Implement backup functionality
            logger.info("Backup data requested")
            self._show_info_message("Backup functionality coming soon!")
        except Exception as err:
            logger.error(f"Error handling backup data: {err}")
            self._show_error_message("Error initiating backup")

    def _handle_export_data(self, e):
        """Handle export data button click."""
        try:
            # TODO: Implement export functionality (CSV, JSON, etc.)
            logger.info("Export data requested")
            self._show_info_message("Export functionality coming soon!")
        except Exception as err:
            logger.error(f"Error handling export data: {err}")
            self._show_error_message("Error initiating export")

    def _handle_import_data(self, e):
        """Handle import data button click."""
        try:
            # TODO: Implement import functionality
            logger.info("Import data requested")
            self._show_info_message("Import functionality coming soon!")
        except Exception as err:
            logger.error(f"Error handling import data: {err}")
            self._show_error_message("Error initiating import")

    def _handle_optimize_database(self, e):
        """Handle optimize database button click."""
        try:
            # TODO: Implement database optimization
            logger.info("Database optimization requested")
            self._show_info_message("Database optimization coming soon!")
        except Exception as err:
            logger.error(f"Error handling database optimization: {err}")
            self._show_error_message("Error optimizing database")

    def _handle_clean_data(self, e):
        """Handle clean data button click."""
        try:
            # TODO: Implement data cleaning (duplicates, invalid entries)
            logger.info("Data cleaning requested")
            self._show_info_message("Data cleaning functionality coming soon!")
        except Exception as err:
            logger.error(f"Error handling data cleaning: {err}")
            self._show_error_message("Error cleaning data")

    def _handle_refresh_stats(self, e):
        """Handle refresh statistics button click."""
        try:
            self.refresh_statistics()
            self._show_success_message("Statistics refreshed successfully!")
        except Exception as err:
            logger.error(f"Error handling refresh stats: {err}")
            self._show_error_message("Error refreshing statistics")

    def _handle_advanced_search(self, e):
        """Handle advanced search button click."""
        try:
            # TODO: Implement advanced search functionality
            logger.info("Advanced search requested")
            self._show_info_message("Advanced search functionality coming soon!")
        except Exception as err:
            logger.error(f"Error handling advanced search: {err}")
            self._show_error_message("Error performing search")

    def _handle_clear_search(self, e):
        """Handle clear search button click."""
        try:
            # TODO: Clear all search fields
            logger.info("Clear search requested")
            self._show_info_message("Search fields cleared!")
        except Exception as err:
            logger.error(f"Error handling clear search: {err}")

    def _show_info_message(self, message: str):
        """Show info message to user."""
        try:
            if self.page:
                # TODO: Implement proper dialog or snackbar
                logger.info(f"Info message: {message}")
        except Exception as err:
            logger.error(f"Error showing info message: {err}")

    def _show_error_message(self, message: str):
        """Show error message to user."""
        try:
            if self.page:
                # TODO: Implement proper error dialog or snackbar
                logger.error(f"Error message: {message}")
        except Exception as err:
            logger.error(f"Error showing error message: {err}")

    def _show_success_message(self, message: str):
        """Show success message to user."""
        try:
            if self.page:
                # TODO: Implement proper success dialog or snackbar
                logger.info(f"Success message: {message}")
        except Exception as err:
            logger.error(f"Error showing success message: {err}")

    def refresh_statistics(self):
        """
        Refresh database statistics from the database.
        TODO: Implement actual database queries.
        """
        try:
            # TODO: Fetch actual statistics from supabase_service or local database
            self.db_stats = {
                "total_entries": 42,  # TODO: Get from database
                "total_amount": 1234.56,  # TODO: Get from database
                "unique_stores": 15,  # TODO: Get from database
                "date_range": "Jan 2024 - Now",  # TODO: Get from database
                "last_backup": "3 days ago",  # TODO: Get from backup service
                "database_size": "2.5 MB"  # TODO: Get from database
            }

            # Update the UI content
            if self.page:
                # TODO: Update the statistics section with new data
                self.page.update()

        except Exception as err:
            logger.error(f"Error refreshing statistics: {err}")

    def update_statistics(self, stats: Dict[str, Any]):
        """
        Update statistics with new data.

        Args:
            stats: Dictionary containing database statistics
        """
        try:
            self.db_stats.update(stats)
            if self.page:
                self.page.update()
        except Exception as err:
            logger.error(f"Error updating statistics: {err}")