import pytest
import flet as ft
from unittest.mock import Mock, patch, MagicMock
from pages.database_page import DatabasePage


class TestDatabasePage:
    """Test suite for DatabasePage component."""

    def test_initialization_with_valid_parameters(self):
        """Test DatabasePage initialization with valid parameters."""
        page_mock = Mock(spec=ft.Page)
        supabase_service_mock = Mock()
        on_database_click = Mock()
        on_logout_click = Mock()

        database_page = DatabasePage(
            page=page_mock,
            supabase_service=supabase_service_mock,
            on_database_click=on_database_click,
            on_logout_click=on_logout_click
        )

        assert database_page.page == page_mock
        assert database_page.route == "/database"
        assert database_page.title == "Spendio - Database"
        assert database_page.supabase_service == supabase_service_mock
        assert database_page.on_database_click == on_database_click
        assert database_page.on_logout_click == on_logout_click

    def test_initialization_creates_base_components(self):
        """Test that DatabasePage creates base page components."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        # Should inherit from BasePage
        assert hasattr(database_page, 'drawer')
        assert hasattr(database_page, 'appbar')
        assert hasattr(database_page, 'content_area')
        assert database_page.controls is not None

    def test_route_configuration(self):
        """Test DatabasePage route configuration."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        assert database_page.route == "/database"

    def test_title_configuration(self):
        """Test DatabasePage title configuration."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        assert database_page.title == "Spendio - Database"
        assert database_page.appbar.title.value == "Spendio - Database"

    def test_database_statistics_initialization(self):
        """Test database statistics initialization."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        assert hasattr(database_page, 'db_stats')
        assert isinstance(database_page.db_stats, dict)
        assert 'total_entries' in database_page.db_stats
        assert 'total_amount' in database_page.db_stats
        assert 'unique_stores' in database_page.db_stats
        assert 'date_range' in database_page.db_stats
        assert 'last_backup' in database_page.db_stats
        assert 'database_size' in database_page.db_stats

    def test_page_content_structure(self):
        """Test page content structure."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        content = database_page._get_page_content()
        assert isinstance(content, list)
        assert len(content) >= 4  # Overview, statistics, management, search

    def test_database_overview_creation(self):
        """Test database overview creation."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        overview = database_page._create_database_overview()
        assert isinstance(overview, ft.Container)
        assert isinstance(overview.content, ft.Column)

    def test_statistics_section_creation(self):
        """Test statistics section creation."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        statistics = database_page._create_statistics_section()
        assert isinstance(statistics, ft.Container)
        assert isinstance(statistics.content, ft.Column)

    def test_stat_card_creation(self):
        """Test statistics card creation."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        stat_card = database_page._create_stat_card(
            title="Test Stat",
            value="100",
            icon=ft.Icons.STORAGE,
            color=ft.Colors.PRIMARY
        )

        assert isinstance(stat_card, ft.Card)
        assert isinstance(stat_card.content, ft.Container)

    def test_management_tools_creation(self):
        """Test management tools creation."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        management_tools = database_page._create_management_tools()
        assert isinstance(management_tools, ft.Container)
        assert isinstance(management_tools.content, ft.Column)

    def test_advanced_search_creation(self):
        """Test advanced search creation."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        search_section = database_page._create_advanced_search()
        assert isinstance(search_section, ft.Container)
        assert isinstance(search_section.content, ft.Column)

    def test_backup_data_handler(self):
        """Test backup data handler."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)
        database_page._show_info_message = Mock()

        mock_event = Mock()
        database_page._handle_backup_data(mock_event)

        database_page._show_info_message.assert_called_once()

    def test_export_data_handler(self):
        """Test export data handler."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)
        database_page._show_info_message = Mock()

        mock_event = Mock()
        database_page._handle_export_data(mock_event)

        database_page._show_info_message.assert_called_once()

    def test_import_data_handler(self):
        """Test import data handler."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)
        database_page._show_info_message = Mock()

        mock_event = Mock()
        database_page._handle_import_data(mock_event)

        database_page._show_info_message.assert_called_once()

    def test_optimize_database_handler(self):
        """Test optimize database handler."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)
        database_page._show_info_message = Mock()

        mock_event = Mock()
        database_page._handle_optimize_database(mock_event)

        database_page._show_info_message.assert_called_once()

    def test_clean_data_handler(self):
        """Test clean data handler."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)
        database_page._show_info_message = Mock()

        mock_event = Mock()
        database_page._handle_clean_data(mock_event)

        database_page._show_info_message.assert_called_once()

    def test_refresh_stats_handler(self):
        """Test refresh statistics handler."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)
        database_page.refresh_statistics = Mock()
        database_page._show_success_message = Mock()

        mock_event = Mock()
        database_page._handle_refresh_stats(mock_event)

        database_page.refresh_statistics.assert_called_once()
        database_page._show_success_message.assert_called_once()

    def test_advanced_search_handler(self):
        """Test advanced search handler."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)
        database_page._show_info_message = Mock()

        mock_event = Mock()
        database_page._handle_advanced_search(mock_event)

        database_page._show_info_message.assert_called_once()

    def test_clear_search_handler(self):
        """Test clear search handler."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)
        database_page._show_info_message = Mock()

        mock_event = Mock()
        database_page._handle_clear_search(mock_event)

        database_page._show_info_message.assert_called_once()

    def test_refresh_statistics_functionality(self):
        """Test refresh statistics functionality."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        original_stats = database_page.db_stats.copy()
        database_page.refresh_statistics()

        # Stats should be updated
        assert database_page.db_stats != original_stats
        page_mock.update.assert_called_once()

    def test_update_statistics_functionality(self):
        """Test update statistics functionality."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        new_stats = {
            "total_entries": 100,
            "total_amount": 5000.0
        }

        database_page.update_statistics(new_stats)

        assert database_page.db_stats["total_entries"] == 100
        assert database_page.db_stats["total_amount"] == 5000.0
        page_mock.update.assert_called_once()

    def test_error_handling_in_content_creation(self):
        """Test error handling in content creation."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        # Mock a method to raise exception
        with patch.object(database_page, '_create_database_overview', side_effect=Exception("Test error")):
            content = database_page._get_page_content()

            # Should return error content instead of raising
            assert isinstance(content, list)
            assert len(content) == 1
            assert isinstance(content[0], ft.Text)
            assert "Error loading" in content[0].value

    def test_error_handling_in_handlers(self):
        """Test error handling in event handlers."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        # Mock show_error_message
        database_page._show_error_message = Mock()

        # Mock methods to raise exceptions
        database_page._show_info_message = Mock(side_effect=Exception("Test error"))

        mock_event = Mock()

        # Should not raise exceptions
        database_page._handle_backup_data(mock_event)
        database_page._handle_export_data(mock_event)
        database_page._handle_import_data(mock_event)

        # Should call error message handler
        assert database_page._show_error_message.call_count >= 3

    def test_message_display_methods(self):
        """Test message display methods."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        # Should not raise exceptions
        database_page._show_info_message("Test info")
        database_page._show_error_message("Test error")
        database_page._show_success_message("Test success")

    def test_with_none_callbacks(self):
        """Test DatabasePage with None callbacks."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        # Should not raise exception with None callbacks
        assert hasattr(database_page, 'on_home_click')
        assert hasattr(database_page, 'on_spendings_click')
        assert hasattr(database_page, 'on_database_click')
        assert hasattr(database_page, 'on_profile_click')
        assert hasattr(database_page, 'on_logout_click')

    def test_inheritance_from_base_page(self):
        """Test that DatabasePage inherits from BasePage."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        # Should have BasePage attributes
        assert hasattr(database_page, 'drawer')
        assert hasattr(database_page, 'appbar')
        assert hasattr(database_page, 'content_area')
        assert hasattr(database_page, '_handle_menu_click')
        assert hasattr(database_page, 'update_title')
        assert hasattr(database_page, 'set_content')

    def test_statistics_responsive_layout(self):
        """Test statistics section responsive layout."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        statistics_section = database_page._create_statistics_section()
        column_content = statistics_section.content
        responsive_row = column_content.controls[1]  # Second control should be ResponsiveRow

        assert isinstance(responsive_row, ft.ResponsiveRow)
        assert len(responsive_row.controls) == 6  # 6 stat cards

        # Each card should have responsive column configuration
        for control in responsive_row.controls:
            assert isinstance(control, ft.Container)
            assert "sm" in control.col
            assert "md" in control.col
            assert "lg" in control.col

    def test_management_tools_responsive_layout(self):
        """Test management tools responsive layout."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        management_section = database_page._create_management_tools()
        column_content = management_section.content
        responsive_row = column_content.controls[1]  # Second control should be ResponsiveRow

        assert isinstance(responsive_row, ft.ResponsiveRow)
        assert len(responsive_row.controls) == 6  # 6 management buttons

    def test_multiple_instances_independence(self):
        """Test that multiple DatabasePage instances are independent."""
        page_mock1 = Mock(spec=ft.Page)
        page_mock2 = Mock(spec=ft.Page)
        callback1 = Mock()
        callback2 = Mock()

        database_page1 = DatabasePage(page=page_mock1, on_database_click=callback1)
        database_page2 = DatabasePage(page=page_mock2, on_database_click=callback2)

        assert database_page1.page == page_mock1
        assert database_page2.page == page_mock2
        assert database_page1.on_database_click == callback1
        assert database_page2.on_database_click == callback2
        assert database_page1 is not database_page2

    def test_supabase_service_integration(self):
        """Test Supabase service integration."""
        page_mock = Mock(spec=ft.Page)
        supabase_mock = Mock()

        database_page = DatabasePage(page=page_mock, supabase_service=supabase_mock)

        assert database_page.supabase_service == supabase_mock

    def test_stat_card_styling_and_content(self):
        """Test stat card styling and content structure."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        stat_card = database_page._create_stat_card(
            title="Test Title",
            value="Test Value",
            icon=ft.Icons.STORAGE,
            color=ft.Colors.PRIMARY
        )

        assert isinstance(stat_card, ft.Card)
        assert stat_card.elevation == 1

        # Check card content structure
        container = stat_card.content
        assert isinstance(container, ft.Container)
        assert container.padding == 16

    def test_database_overview_status_display(self):
        """Test database overview status display."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        overview = database_page._create_database_overview()

        # Should contain status information
        assert isinstance(overview, ft.Container)
        column_content = overview.content
        assert isinstance(column_content, ft.Column)
        assert len(column_content.controls) >= 3  # Title, subtitle, status card


class TestDatabasePageEdgeCases:
    """Test edge cases and error scenarios for DatabasePage."""

    def test_with_none_page_parameter(self):
        """Test DatabasePage with None page parameter."""
        database_page = DatabasePage(page=None)

        assert database_page.page is None
        # Should still create components without error
        assert hasattr(database_page, 'drawer')
        assert hasattr(database_page, 'appbar')
        assert hasattr(database_page, 'db_stats')

    def test_handlers_with_none_page(self):
        """Test event handlers with None page."""
        database_page = DatabasePage(page=None)

        mock_event = Mock()

        # Should not raise exceptions even with None page
        database_page._handle_backup_data(mock_event)
        database_page._handle_export_data(mock_event)
        database_page._handle_import_data(mock_event)
        database_page._handle_refresh_stats(mock_event)

    def test_refresh_statistics_with_none_page(self):
        """Test refresh statistics with None page."""
        database_page = DatabasePage(page=None)

        # Should not raise exception
        database_page.refresh_statistics()

    def test_update_statistics_with_none_page(self):
        """Test update statistics with None page."""
        database_page = DatabasePage(page=None)

        new_stats = {"total_entries": 50}

        # Should not raise exception
        database_page.update_statistics(new_stats)
        assert database_page.db_stats["total_entries"] == 50

    def test_stat_card_creation_with_none_values(self):
        """Test stat card creation with None values."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        # Should handle None values gracefully
        stat_card = database_page._create_stat_card(
            title=None,
            value=None,
            icon=ft.Icons.STORAGE,
            color=ft.Colors.PRIMARY
        )

        assert isinstance(stat_card, ft.Card)

    def test_message_methods_with_none_page(self):
        """Test message methods with None page."""
        database_page = DatabasePage(page=None)

        # Should not raise exceptions
        database_page._show_info_message("Test")
        database_page._show_error_message("Test")
        database_page._show_success_message("Test")

    def test_statistics_update_with_partial_data(self):
        """Test statistics update with partial data."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        original_entries = database_page.db_stats["total_entries"]

        # Update only some fields
        partial_stats = {"total_entries": 999}
        database_page.update_statistics(partial_stats)

        assert database_page.db_stats["total_entries"] == 999
        # Other fields should remain unchanged
        assert "total_amount" in database_page.db_stats

    def test_with_callable_objects_as_callbacks(self):
        """Test DatabasePage with callable objects as callbacks."""
        class CallableClass:
            def __init__(self):
                self.called = False

            def __call__(self, event):
                self.called = True

        page_mock = Mock(spec=ft.Page)
        database_callback = CallableClass()
        logout_callback = CallableClass()

        database_page = DatabasePage(
            page=page_mock,
            on_database_click=database_callback,
            on_logout_click=logout_callback
        )

        assert callable(database_page.on_database_click)
        assert callable(database_page.on_logout_click)

    def test_error_handling_in_statistics_methods(self):
        """Test error handling in statistics methods."""
        page_mock = Mock(spec=ft.Page)
        page_mock.update.side_effect = Exception("Update error")

        database_page = DatabasePage(page=page_mock)

        # Should not raise exceptions
        database_page.refresh_statistics()
        database_page.update_statistics({"total_entries": 100})

    def test_advanced_search_form_structure(self):
        """Test advanced search form structure."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        search_section = database_page._create_advanced_search()

        # Should contain search form with multiple fields
        assert isinstance(search_section, ft.Container)
        column_content = search_section.content
        assert isinstance(column_content, ft.Column)

        # Should have search card
        search_card = column_content.controls[1]
        assert isinstance(search_card, ft.Card)

    def test_management_tools_button_configuration(self):
        """Test management tools button configuration."""
        page_mock = Mock(spec=ft.Page)
        database_page = DatabasePage(page=page_mock)

        management_section = database_page._create_management_tools()
        column_content = management_section.content
        responsive_row = column_content.controls[1]

        # Should have 6 management buttons
        assert len(responsive_row.controls) == 6

        # Each should be a container with a button
        for container in responsive_row.controls:
            assert isinstance(container, ft.Container)
            button = container.content
            assert isinstance(button, ft.ElevatedButton)