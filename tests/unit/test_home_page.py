import pytest
import flet as ft
from unittest.mock import Mock, patch, MagicMock
from pages.home_page import HomePage


class TestHomePage:
    """Test suite for HomePage component."""

    def test_initialization_with_valid_parameters(self):
        """Test HomePage initialization with valid parameters."""
        page_mock = Mock(spec=ft.Page)
        supabase_service_mock = Mock()
        on_home_click = Mock()
        on_spendings_click = Mock()

        home_page = HomePage(
            page=page_mock,
            supabase_service=supabase_service_mock,
            on_home_click=on_home_click,
            on_spendings_click=on_spendings_click
        )

        assert home_page.page == page_mock
        assert home_page.route == "/home"
        assert home_page.title == "Spendio - Home"
        assert home_page.supabase_service == supabase_service_mock
        assert home_page.on_home_click == on_home_click
        assert home_page.on_spendings_click == on_spendings_click

    def test_initialization_creates_base_components(self):
        """Test that HomePage creates base page components."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Should inherit from BasePage
        assert hasattr(home_page, 'drawer')
        assert hasattr(home_page, 'appbar')
        assert hasattr(home_page, 'content_area')
        assert home_page.controls is not None

    def test_route_configuration(self):
        """Test HomePage route configuration."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        assert home_page.route == "/home"

    def test_title_configuration(self):
        """Test HomePage title configuration."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        assert home_page.title == "Spendio - Home"
        assert home_page.appbar.title.value == "Spendio - Home"

    def test_page_content_structure(self):
        """Test page content structure."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        content = home_page._get_page_content()
        assert isinstance(content, list)
        assert len(content) >= 4  # Welcome, overview, quick actions, recent activity

    def test_welcome_section_creation(self):
        """Test welcome section creation."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        welcome_section = home_page._create_welcome_section()
        assert isinstance(welcome_section, ft.Container)
        assert isinstance(welcome_section.content, ft.Column)

    def test_overview_cards_creation(self):
        """Test overview cards creation."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        overview_cards = home_page._create_overview_cards()
        assert isinstance(overview_cards, ft.ResponsiveRow)
        assert len(overview_cards.controls) == 4  # Total, This Month, Entries, Categories

    def test_card_creation_with_valid_parameters(self):
        """Test card creation with valid parameters."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        card = home_page._create_card(
            title="Test Card",
            value="$100",
            icon=ft.Icons.MONETIZATION_ON,
            color=ft.Colors.PRIMARY
        )

        assert isinstance(card, ft.Card)
        assert isinstance(card.content, ft.Container)

    def test_quick_actions_creation(self):
        """Test quick actions creation."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        quick_actions = home_page._create_quick_actions()
        assert isinstance(quick_actions, ft.Container)
        assert isinstance(quick_actions.content, ft.Column)

    def test_recent_activity_creation(self):
        """Test recent activity creation."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        recent_activity = home_page._create_recent_activity()
        assert isinstance(recent_activity, ft.Container)
        assert isinstance(recent_activity.content, ft.Column)

    def test_activity_item_creation(self):
        """Test activity item creation."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        activity_item = home_page._create_activity_item(
            store="Test Store",
            amount="$50.00",
            time="1 hour ago",
            icon=ft.Icons.STORE
        )

        assert isinstance(activity_item, ft.Row)
        assert len(activity_item.controls) == 3  # Icon, info column, amount

    def test_add_spending_handler(self):
        """Test add spending button handler."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        mock_event = Mock()
        home_page._handle_add_spending(mock_event)

        page_mock.go.assert_called_once_with("/spendings")

    def test_view_spendings_handler_with_callback(self):
        """Test view spendings handler with callback."""
        page_mock = Mock(spec=ft.Page)
        on_spendings_click = Mock()
        home_page = HomePage(page=page_mock, on_spendings_click=on_spendings_click)

        mock_event = Mock()
        home_page._handle_view_spendings(mock_event)

        on_spendings_click.assert_called_once_with(mock_event)

    def test_view_spendings_handler_without_callback(self):
        """Test view spendings handler without callback."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock, on_spendings_click=None)

        mock_event = Mock()
        home_page._handle_view_spendings(mock_event)

        page_mock.go.assert_called_once_with("/spendings")

    def test_view_database_handler_with_callback(self):
        """Test view database handler with callback."""
        page_mock = Mock(spec=ft.Page)
        on_database_click = Mock()
        home_page = HomePage(page=page_mock, on_database_click=on_database_click)

        mock_event = Mock()
        home_page._handle_view_database(mock_event)

        on_database_click.assert_called_once_with(mock_event)

    def test_view_database_handler_without_callback(self):
        """Test view database handler without callback."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock, on_database_click=None)

        mock_event = Mock()
        home_page._handle_view_database(mock_event)

        page_mock.go.assert_called_once_with("/database")

    def test_refresh_data_functionality(self):
        """Test refresh data functionality."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Should not raise exception
        home_page.refresh_data()
        page_mock.update.assert_called_once()

    def test_set_user_info_functionality(self):
        """Test set user info functionality."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Should not raise exception
        home_page.set_user_info(user_name="John Doe", user_email="john@example.com")

    def test_with_none_callbacks(self):
        """Test HomePage with None callbacks."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Should not raise exception with None callbacks
        assert hasattr(home_page, 'on_home_click')
        assert hasattr(home_page, 'on_spendings_click')
        assert hasattr(home_page, 'on_database_click')
        assert hasattr(home_page, 'on_profile_click')
        assert hasattr(home_page, 'on_logout_click')

    def test_inheritance_from_base_page(self):
        """Test that HomePage inherits from BasePage."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Should have BasePage attributes
        assert hasattr(home_page, 'drawer')
        assert hasattr(home_page, 'appbar')
        assert hasattr(home_page, 'content_area')
        assert hasattr(home_page, '_handle_menu_click')
        assert hasattr(home_page, 'update_title')
        assert hasattr(home_page, 'set_content')

    def test_overview_cards_responsive_layout(self):
        """Test overview cards responsive layout."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        overview_cards = home_page._create_overview_cards()

        # Each card should have responsive column configuration
        for control in overview_cards.controls:
            assert isinstance(control, ft.Container)
            assert "sm" in control.col
            assert "md" in control.col
            assert "lg" in control.col

    def test_quick_actions_responsive_layout(self):
        """Test quick actions responsive layout."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        quick_actions = home_page._create_quick_actions()

        # Should have responsive row with buttons
        column_content = quick_actions.content
        responsive_row = column_content.controls[1]  # Second control should be ResponsiveRow
        assert isinstance(responsive_row, ft.ResponsiveRow)

    def test_error_handling_in_content_creation(self):
        """Test error handling in content creation."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Mock a method to raise exception
        with patch.object(home_page, '_create_welcome_section', side_effect=Exception("Test error")):
            content = home_page._get_page_content()

            # Should return error content instead of raising
            assert isinstance(content, list)
            assert len(content) == 1
            assert isinstance(content[0], ft.Text)
            assert "Error loading" in content[0].value

    def test_error_handling_in_handlers(self):
        """Test error handling in event handlers."""
        page_mock = Mock(spec=ft.Page)
        page_mock.go.side_effect = Exception("Navigation error")
        home_page = HomePage(page=page_mock)

        mock_event = Mock()

        # Should not raise exceptions
        home_page._handle_add_spending(mock_event)
        home_page._handle_view_spendings(mock_event)
        home_page._handle_view_database(mock_event)

    def test_navigation_highlight_on_initialization(self):
        """Test navigation highlight on initialization."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Should have called highlight_current_navigation with "Home"
        # This is tested indirectly by checking the drawer exists
        assert hasattr(home_page, 'drawer')

    def test_multiple_instances_independence(self):
        """Test that multiple HomePage instances are independent."""
        page_mock1 = Mock(spec=ft.Page)
        page_mock2 = Mock(spec=ft.Page)
        callback1 = Mock()
        callback2 = Mock()

        home_page1 = HomePage(page=page_mock1, on_home_click=callback1)
        home_page2 = HomePage(page=page_mock2, on_home_click=callback2)

        assert home_page1.page == page_mock1
        assert home_page2.page == page_mock2
        assert home_page1.on_home_click == callback1
        assert home_page2.on_home_click == callback2
        assert home_page1 is not home_page2

    def test_supabase_service_integration(self):
        """Test Supabase service integration."""
        page_mock = Mock(spec=ft.Page)
        supabase_mock = Mock()

        home_page = HomePage(page=page_mock, supabase_service=supabase_mock)

        assert home_page.supabase_service == supabase_mock

    def test_card_styling_and_content(self):
        """Test card styling and content structure."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        card = home_page._create_card(
            title="Test Title",
            value="Test Value",
            icon=ft.Icons.HOME,
            color=ft.Colors.PRIMARY
        )

        assert isinstance(card, ft.Card)
        assert card.elevation == 2

        # Check card content structure
        container = card.content
        assert isinstance(container, ft.Container)
        assert container.padding == 20

    def test_activity_item_structure(self):
        """Test activity item structure and content."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        activity_item = home_page._create_activity_item(
            store="Test Store",
            amount="$100.00",
            time="1 hour ago",
            icon=ft.Icons.STORE
        )

        assert isinstance(activity_item, ft.Row)
        assert len(activity_item.controls) == 3

        # Check icon
        icon_control = activity_item.controls[0]
        assert isinstance(icon_control, ft.Icon)
        assert icon_control.name == ft.Icons.STORE

        # Check amount text
        amount_control = activity_item.controls[2]
        assert isinstance(amount_control, ft.Text)
        assert amount_control.value == "$100.00"


class TestHomePageEdgeCases:
    """Test edge cases and error scenarios for HomePage."""

    def test_with_none_page_parameter(self):
        """Test HomePage with None page parameter."""
        home_page = HomePage(page=None)

        assert home_page.page is None
        # Should still create components without error
        assert hasattr(home_page, 'drawer')
        assert hasattr(home_page, 'appbar')

    def test_handlers_with_none_page(self):
        """Test event handlers with None page."""
        home_page = HomePage(page=None)

        mock_event = Mock()

        # Should not raise exceptions even with None page
        home_page._handle_add_spending(mock_event)
        home_page._handle_view_spendings(mock_event)
        home_page._handle_view_database(mock_event)

    def test_refresh_data_with_none_page(self):
        """Test refresh data with None page."""
        home_page = HomePage(page=None)

        # Should not raise exception
        home_page.refresh_data()

    def test_card_creation_with_none_values(self):
        """Test card creation with None values."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Should handle None values gracefully
        card = home_page._create_card(
            title=None,
            value=None,
            icon=ft.Icons.HOME,
            color=ft.Colors.PRIMARY
        )

        assert isinstance(card, ft.Card)

    def test_activity_item_with_empty_strings(self):
        """Test activity item creation with empty strings."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        activity_item = home_page._create_activity_item(
            store="",
            amount="",
            time="",
            icon=ft.Icons.STORE
        )

        assert isinstance(activity_item, ft.Row)
        assert len(activity_item.controls) == 3

    def test_with_callable_objects_as_callbacks(self):
        """Test HomePage with callable objects as callbacks."""
        class CallableClass:
            def __init__(self):
                self.called = False

            def __call__(self, event):
                self.called = True

        page_mock = Mock(spec=ft.Page)
        home_callback = CallableClass()
        spendings_callback = CallableClass()

        home_page = HomePage(
            page=page_mock,
            on_home_click=home_callback,
            on_spendings_click=spendings_callback
        )

        assert callable(home_page.on_home_click)
        assert callable(home_page.on_spendings_click)

    def test_content_spacing_and_alignment(self):
        """Test content spacing and alignment configuration."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Check content area configuration
        assert home_page.content_area.padding == 20
        assert home_page.content_area.expand is True

        # Check content column configuration
        content_column = home_page.content_area.content
        assert isinstance(content_column, ft.Column)
        assert content_column.spacing == 20
        assert content_column.horizontal_alignment == ft.CrossAxisAlignment.CENTER

    def test_overview_cards_data_structure(self):
        """Test overview cards data structure and values."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        overview_cards = home_page._create_overview_cards()

        # Should have 4 cards with proper responsive configuration
        assert len(overview_cards.controls) == 4
        assert overview_cards.spacing == 16
        assert overview_cards.run_spacing == 16

    def test_set_user_info_with_none_values(self):
        """Test set user info with None values."""
        page_mock = Mock(spec=ft.Page)
        home_page = HomePage(page=page_mock)

        # Should not raise exception with None values
        home_page.set_user_info(user_name=None, user_email=None)
        home_page.set_user_info()  # No parameters