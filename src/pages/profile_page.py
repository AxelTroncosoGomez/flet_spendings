from typing import Optional, Callable, List, Dict, Any
import flet as ft
from presentation.pages.base_page import BasePage
from utils.logger import logger


class ProfilePage(BasePage):
    """
    Profile management page for the Spendio application.

    Features:
    - User profile information display and editing
    - Account settings management
    - Security settings (password change, 2FA)
    - Preferences configuration
    - Account statistics and usage
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
        Initialize ProfilePage with base template structure.

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
            route="/profile",
            title="Spendio - Profile",
            supabase_service=supabase_service,
            on_home_click=on_home_click,
            on_spendings_click=on_spendings_click,
            on_database_click=on_database_click,
            on_profile_click=on_profile_click,
            on_logout_click=on_logout_click,
            on_settings_click=on_settings_click
        )

        # Initialize user profile data first
        self.user_profile = {
            "name": "User",
            "email": "user@example.com",
            "avatar_url": None,
            "created_at": "2024-01-01",
            "last_login": "Today",
            "subscription": "Free",
            "total_spendings": 0.0,
            "entries_count": 0,
            "theme": "Dark",
            "currency": "USD",
            "notifications": True,
            "two_factor": False
        }

        # Create form fields for editing
        self._create_form_fields()

        # Highlight current page in navigation
        self.highlight_current_navigation("Profile")

        # Populate content after initialization is complete
        self._populate_content()

    def _create_form_fields(self):
        """Create form fields for profile editing."""
        try:
            self.name_field = ft.TextField(
                label="Full Name",
                value=self.user_profile["name"],
                prefix_icon=ft.Icons.PERSON,
                border_radius=8,
                expand=True
            )

            self.email_field = ft.TextField(
                label="Email Address",
                value=self.user_profile["email"],
                prefix_icon=ft.Icons.EMAIL,
                border_radius=8,
                expand=True,
                read_only=True  # Email usually can't be changed
            )

            self.current_password_field = ft.TextField(
                label="Current Password",
                password=True,
                can_reveal_password=True,
                prefix_icon=ft.Icons.LOCK,
                border_radius=8,
                expand=True
            )

            self.new_password_field = ft.TextField(
                label="New Password",
                password=True,
                can_reveal_password=True,
                prefix_icon=ft.Icons.LOCK_OUTLINE,
                border_radius=8,
                expand=True
            )

            self.confirm_password_field = ft.TextField(
                label="Confirm New Password",
                password=True,
                can_reveal_password=True,
                prefix_icon=ft.Icons.LOCK_OUTLINE,
                border_radius=8,
                expand=True
            )

        except Exception as err:
            logger.error(f"Error creating form fields: {err}")

    def _get_page_content(self) -> List[ft.Control]:
        """
        Override to provide Profile page specific content.

        Returns:
            List of Flet controls for the Profile page content
        """
        try:
            return [
                self._create_profile_header(),
                self._create_account_info(),
                self._create_security_settings(),
                self._create_preferences_settings(),
                self._create_account_statistics(),
            ]
        except Exception as err:
            logger.error(f"Error creating profile page content: {err}")
            return [
                ft.Text(
                    "Error loading profile page content",
                    size=16,
                    color=ft.Colors.ERROR
                )
            ]

    def _create_profile_header(self) -> ft.Container:
        """
        Create profile header with avatar and basic info.

        Returns:
            ft.Container: Profile header container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.CircleAvatar(
                                    foreground_image_src=self.user_profile.get("avatar_url"),
                                    content=ft.Icon(
                                        name=ft.Icons.PERSON,
                                        size=40,
                                        color=ft.Colors.ON_PRIMARY
                                    ),
                                    radius=40,
                                    bgcolor=ft.Colors.PRIMARY
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        self.user_profile["name"],
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.ON_SURFACE
                                    ),
                                    ft.Text(
                                        self.user_profile["email"],
                                        size=16,
                                        color=ft.Colors.ON_SURFACE_VARIANT
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            f"{self.user_profile['subscription']} Plan",
                                            size=12,
                                            color=ft.Colors.ON_PRIMARY,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        bgcolor=ft.Colors.PRIMARY,
                                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                        border_radius=12
                                    )
                                ],
                                spacing=4,
                                expand=True
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=20
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Change Avatar",
                                icon=ft.Icons.PHOTO_CAMERA,
                                on_click=self._handle_change_avatar,
                                style=ft.ButtonStyle(
                                    padding=ft.padding.symmetric(horizontal=16, vertical=8)
                                )
                            ),
                            ft.OutlinedButton(
                                text="Edit Profile",
                                icon=ft.Icons.EDIT,
                                on_click=self._handle_edit_profile,
                                style=ft.ButtonStyle(
                                    padding=ft.padding.symmetric(horizontal=16, vertical=8)
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=16
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            padding=ft.padding.symmetric(vertical=20),
            alignment=ft.alignment.center
        )

    def _create_account_info(self) -> ft.Container:
        """
        Create account information section.

        Returns:
            ft.Container: Account info container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Account Information",
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
                                                content=self.name_field,
                                                col={"sm": 12, "md": 6}
                                            ),
                                            ft.Container(
                                                content=self.email_field,
                                                col={"sm": 12, "md": 6}
                                            ),
                                        ],
                                        spacing=16,
                                        run_spacing=16
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                text="Save Changes",
                                                icon=ft.Icons.SAVE,
                                                on_click=self._handle_save_profile,
                                                style=ft.ButtonStyle(
                                                    padding=ft.padding.symmetric(
                                                        horizontal=24, vertical=12
                                                    )
                                                )
                                            ),
                                            ft.OutlinedButton(
                                                text="Cancel",
                                                icon=ft.Icons.CANCEL,
                                                on_click=self._handle_cancel_edit,
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

    def _create_security_settings(self) -> ft.Container:
        """
        Create security settings section.

        Returns:
            ft.Container: Security settings container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Security Settings",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Change Password",
                                        size=16,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.ON_SURFACE
                                    ),
                                    ft.ResponsiveRow(
                                        controls=[
                                            ft.Container(
                                                content=self.current_password_field,
                                                col={"sm": 12, "md": 4}
                                            ),
                                            ft.Container(
                                                content=self.new_password_field,
                                                col={"sm": 12, "md": 4}
                                            ),
                                            ft.Container(
                                                content=self.confirm_password_field,
                                                col={"sm": 12, "md": 4}
                                            ),
                                        ],
                                        spacing=16,
                                        run_spacing=16
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                text="Change Password",
                                                icon=ft.Icons.SECURITY,
                                                on_click=self._handle_change_password,
                                                style=ft.ButtonStyle(
                                                    padding=ft.padding.symmetric(
                                                        horizontal=24, vertical=12
                                                    ),
                                                    bgcolor=ft.Colors.ORANGE
                                                )
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.START
                                    ),
                                    ft.Divider(),
                                    ft.Text(
                                        "Two-Factor Authentication",
                                        size=16,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.ON_SURFACE
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Switch(
                                                label="Enable Two-Factor Authentication",
                                                value=self.user_profile["two_factor"],
                                                on_change=self._handle_two_factor_toggle
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.OutlinedButton(
                                                text="Setup 2FA",
                                                icon=ft.Icons.SECURITY,
                                                on_click=self._handle_setup_2fa,
                                                disabled=self.user_profile["two_factor"],
                                                style=ft.ButtonStyle(
                                                    padding=ft.padding.symmetric(
                                                        horizontal=24, vertical=12
                                                    )
                                                )
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.START
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

    def _create_preferences_settings(self) -> ft.Container:
        """
        Create preferences settings section.

        Returns:
            ft.Container: Preferences settings container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Preferences",
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
                                                content=ft.Dropdown(
                                                    label="Theme",
                                                    value=self.user_profile["theme"],
                                                    options=[
                                                        ft.dropdown.Option("Light"),
                                                        ft.dropdown.Option("Dark"),
                                                        ft.dropdown.Option("System"),
                                                    ],
                                                    on_change=self._handle_theme_change,
                                                    border_radius=8,
                                                    expand=True
                                                ),
                                                col={"sm": 12, "md": 6}
                                            ),
                                            ft.Container(
                                                content=ft.Dropdown(
                                                    label="Currency",
                                                    value=self.user_profile["currency"],
                                                    options=[
                                                        ft.dropdown.Option("USD"),
                                                        ft.dropdown.Option("EUR"),
                                                        ft.dropdown.Option("GBP"),
                                                        ft.dropdown.Option("JPY"),
                                                        ft.dropdown.Option("CAD"),
                                                    ],
                                                    on_change=self._handle_currency_change,
                                                    border_radius=8,
                                                    expand=True
                                                ),
                                                col={"sm": 12, "md": 6}
                                            ),
                                        ],
                                        spacing=16,
                                        run_spacing=16
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Switch(
                                                label="Email Notifications",
                                                value=self.user_profile["notifications"],
                                                on_change=self._handle_notifications_toggle
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                text="Save Preferences",
                                                icon=ft.Icons.SAVE,
                                                on_click=self._handle_save_preferences,
                                                style=ft.ButtonStyle(
                                                    padding=ft.padding.symmetric(
                                                        horizontal=24, vertical=12
                                                    )
                                                )
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.START
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

    def _create_account_statistics(self) -> ft.Container:
        """
        Create account statistics section.

        Returns:
            ft.Container: Account statistics container
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Account Statistics",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Total Spendings",
                                    value=f"${self.user_profile['total_spendings']:.2f}",
                                    icon=ft.Icons.MONETIZATION_ON,
                                    color=ft.Colors.PRIMARY
                                ),
                                col={"sm": 12, "md": 6, "lg": 3}
                            ),
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Total Entries",
                                    value=str(self.user_profile["entries_count"]),
                                    icon=ft.Icons.RECEIPT_LONG,
                                    color=ft.Colors.SECONDARY
                                ),
                                col={"sm": 12, "md": 6, "lg": 3}
                            ),
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Member Since",
                                    value=self.user_profile["created_at"],
                                    icon=ft.Icons.CALENDAR_TODAY,
                                    color=ft.Colors.TERTIARY
                                ),
                                col={"sm": 12, "md": 6, "lg": 3}
                            ),
                            ft.Container(
                                content=self._create_stat_card(
                                    title="Last Login",
                                    value=self.user_profile["last_login"],
                                    icon=ft.Icons.LOGIN,
                                    color=ft.Colors.GREEN
                                ),
                                col={"sm": 12, "md": 6, "lg": 3}
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
                content=ft.Row(
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
                                    size=16,
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
                ),
                padding=16,
                alignment=ft.alignment.center_left
            ),
            elevation=1
        )

    # Event Handlers
    def _handle_change_avatar(self, e):
        """Handle change avatar button click."""
        try:
            # TODO: Implement avatar upload functionality
            logger.info("Change avatar requested")
            self._show_info_message("Avatar upload coming soon!")
        except Exception as err:
            logger.error(f"Error handling change avatar: {err}")

    def _handle_edit_profile(self, e):
        """Handle edit profile button click."""
        try:
            # TODO: Enable/disable form fields for editing
            logger.info("Edit profile requested")
            self._show_info_message("Profile editing enabled!")
        except Exception as err:
            logger.error(f"Error handling edit profile: {err}")

    def _handle_save_profile(self, e):
        """Handle save profile changes."""
        try:
            # TODO: Validate and save profile changes
            self.user_profile["name"] = self.name_field.value
            logger.info("Profile saved")
            self._show_success_message("Profile updated successfully!")
        except Exception as err:
            logger.error(f"Error saving profile: {err}")
            self._show_error_message("Error saving profile changes")

    def _handle_cancel_edit(self, e):
        """Handle cancel edit profile."""
        try:
            # Reset form fields to original values
            self.name_field.value = self.user_profile["name"]
            self.email_field.value = self.user_profile["email"]
            if self.page:
                self.page.update()
        except Exception as err:
            logger.error(f"Error canceling edit: {err}")

    def _handle_change_password(self, e):
        """Handle change password."""
        try:
            # TODO: Validate current password and update with new password
            current_password = self.current_password_field.value
            new_password = self.new_password_field.value
            confirm_password = self.confirm_password_field.value

            if not all([current_password, new_password, confirm_password]):
                self._show_error_message("Please fill all password fields")
                return

            if new_password != confirm_password:
                self._show_error_message("New passwords do not match")
                return

            logger.info("Password change requested")
            self._show_success_message("Password changed successfully!")

            # Clear password fields
            self.current_password_field.value = ""
            self.new_password_field.value = ""
            self.confirm_password_field.value = ""
            if self.page:
                self.page.update()

        except Exception as err:
            logger.error(f"Error changing password: {err}")
            self._show_error_message("Error changing password")

    def _handle_two_factor_toggle(self, e):
        """Handle two-factor authentication toggle."""
        try:
            self.user_profile["two_factor"] = e.control.value
            logger.info(f"2FA toggled: {e.control.value}")
            if e.control.value:
                self._show_info_message("Two-factor authentication enabled")
            else:
                self._show_info_message("Two-factor authentication disabled")
        except Exception as err:
            logger.error(f"Error toggling 2FA: {err}")

    def _handle_setup_2fa(self, e):
        """Handle setup 2FA button click."""
        try:
            # TODO: Implement 2FA setup flow
            logger.info("2FA setup requested")
            self._show_info_message("2FA setup coming soon!")
        except Exception as err:
            logger.error(f"Error setting up 2FA: {err}")

    def _handle_theme_change(self, e):
        """Handle theme dropdown change."""
        try:
            self.user_profile["theme"] = e.control.value
            logger.info(f"Theme changed to: {e.control.value}")
            # TODO: Apply theme change to the app
        except Exception as err:
            logger.error(f"Error changing theme: {err}")

    def _handle_currency_change(self, e):
        """Handle currency dropdown change."""
        try:
            self.user_profile["currency"] = e.control.value
            logger.info(f"Currency changed to: {e.control.value}")
        except Exception as err:
            logger.error(f"Error changing currency: {err}")

    def _handle_notifications_toggle(self, e):
        """Handle notifications toggle."""
        try:
            self.user_profile["notifications"] = e.control.value
            logger.info(f"Notifications toggled: {e.control.value}")
        except Exception as err:
            logger.error(f"Error toggling notifications: {err}")

    def _handle_save_preferences(self, e):
        """Handle save preferences."""
        try:
            # TODO: Save preferences to database/settings
            logger.info("Preferences saved")
            self._show_success_message("Preferences saved successfully!")
        except Exception as err:
            logger.error(f"Error saving preferences: {err}")
            self._show_error_message("Error saving preferences")

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

    def load_user_profile(self, user_data: Dict[str, Any]):
        """
        Load user profile data from external source.

        Args:
            user_data: Dictionary containing user profile data
        """
        try:
            self.user_profile.update(user_data)
            self._update_form_fields()
            if self.page:
                self.page.update()
        except Exception as err:
            logger.error(f"Error loading user profile: {err}")

    def _update_form_fields(self):
        """Update form fields with current profile data."""
        try:
            self.name_field.value = self.user_profile["name"]
            self.email_field.value = self.user_profile["email"]
        except Exception as err:
            logger.error(f"Error updating form fields: {err}")

    def get_user_profile(self) -> Dict[str, Any]:
        """
        Get current user profile data.

        Returns:
            Dictionary containing current user profile data
        """
        return self.user_profile.copy()