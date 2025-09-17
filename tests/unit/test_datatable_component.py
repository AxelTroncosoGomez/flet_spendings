import pytest
import flet as ft
from unittest.mock import Mock, patch
from components.datatables import DataTableComponent


class TestDataTableComponent:
    """Test suite for DataTableComponent using TDD approach."""

    @pytest.fixture
    def sample_datatable(self):
        """Create a sample datatable with test data."""
        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Amount")),
        ]

        rows = []
        for i in range(25):  # Create 25 rows for testing pagination
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(i + 1))),
                ft.DataCell(ft.Text(f"Item {i + 1}")),
                ft.DataCell(ft.Text(f"${(i + 1) * 10}")),
            ]))

        return ft.DataTable(columns=columns, rows=rows)

    @pytest.fixture
    def datatable_component(self, sample_datatable):
        """Create a DataTableComponent instance for testing."""
        return DataTableComponent(sample_datatable, rows_per_page=10)

    def test_initialization_with_default_values(self, sample_datatable):
        """Test DataTableComponent initialization with default values."""
        component = DataTableComponent(sample_datatable)

        assert component.rows_per_page == DataTableComponent.DEFAULT_ROW_PER_PAGE
        assert component.num_rows == 25
        assert component.current_page == 1
        assert component.num_pages == 3  # 25 rows / 10 per page = 3 pages

    def test_initialization_with_custom_rows_per_page(self, sample_datatable):
        """Test DataTableComponent initialization with custom rows per page."""
        component = DataTableComponent(sample_datatable, rows_per_page=5)

        assert component.rows_per_page == 5
        assert component.num_pages == 5  # 25 rows / 5 per page = 5 pages

    def test_paginate_first_page(self, datatable_component):
        """Test pagination calculation for first page."""
        start, end = datatable_component.paginate()

        assert start == 0
        assert end == 10

    def test_paginate_middle_page(self, datatable_component):
        """Test pagination calculation for middle page."""
        datatable_component.current_page = 2
        start, end = datatable_component.paginate()

        assert start == 10
        assert end == 20

    def test_paginate_last_page(self, datatable_component):
        """Test pagination calculation for last page."""
        datatable_component.current_page = 3
        start, end = datatable_component.paginate()

        assert start == 20
        assert end == 30

    def test_build_rows_first_page(self, datatable_component):
        """Test building rows for first page."""
        rows = datatable_component.build_rows()

        assert len(rows) == 10
        # Check if first row contains correct data
        assert rows[0].cells[0].content.value == "1"

    def test_build_rows_last_page(self, datatable_component):
        """Test building rows for last page."""
        datatable_component.current_page = 3
        rows = datatable_component.build_rows()

        assert len(rows) == 5  # Last page has only 5 rows (25 % 10)
        # Check if first row of last page contains correct data
        assert rows[0].cells[0].content.value == "21"

    def test_set_page_valid_page(self, datatable_component):
        """Test setting a valid page number."""
        datatable_component.set_page(page=2)

        assert datatable_component.current_page == 2

    def test_set_page_invalid_page_too_high(self, datatable_component):
        """Test setting page number higher than available pages."""
        datatable_component.set_page(page=10)

        assert datatable_component.current_page == 1  # Should default to 1

    def test_set_page_invalid_page_zero(self, datatable_component):
        """Test setting page number to zero."""
        datatable_component.set_page(page=0)

        assert datatable_component.current_page == 1  # Should default to 1

    def test_set_page_invalid_string(self, datatable_component):
        """Test setting page with invalid string."""
        datatable_component.set_page(page="invalid")

        assert datatable_component.current_page == 1  # Should default to 1

    def test_set_page_with_delta_positive(self, datatable_component):
        """Test setting page using positive delta."""
        datatable_component.current_page = 2
        datatable_component.set_page(delta=1)

        assert datatable_component.current_page == 3

    def test_set_page_with_delta_negative(self, datatable_component):
        """Test setting page using negative delta."""
        datatable_component.current_page = 2
        datatable_component.set_page(delta=-1)

        assert datatable_component.current_page == 1

    def test_next_page_valid(self, datatable_component):
        """Test going to next page when valid."""
        mock_event = Mock()
        datatable_component.next_page(mock_event)

        assert datatable_component.current_page == 2

    def test_next_page_at_last_page(self, datatable_component):
        """Test going to next page when at last page."""
        datatable_component.current_page = 3  # Last page
        mock_event = Mock()
        datatable_component.next_page(mock_event)

        assert datatable_component.current_page == 3  # Should stay at last page

    def test_prev_page_valid(self, datatable_component):
        """Test going to previous page when valid."""
        datatable_component.current_page = 2
        mock_event = Mock()
        datatable_component.prev_page(mock_event)

        assert datatable_component.current_page == 1

    def test_prev_page_at_first_page(self, datatable_component):
        """Test going to previous page when at first page."""
        mock_event = Mock()
        datatable_component.prev_page(mock_event)

        assert datatable_component.current_page == 1  # Should stay at first page

    def test_goto_first_page(self, datatable_component):
        """Test going to first page."""
        datatable_component.current_page = 3
        mock_event = Mock()
        datatable_component.goto_first_page(mock_event)

        assert datatable_component.current_page == 1

    def test_goto_last_page(self, datatable_component):
        """Test going to last page."""
        mock_event = Mock()
        datatable_component.goto_last_page(mock_event)

        assert datatable_component.current_page == 3

    def test_set_rows_per_page_valid(self, datatable_component):
        """Test setting valid rows per page."""
        datatable_component.set_rows_per_page("5")

        assert datatable_component.rows_per_page == 5
        assert datatable_component.num_pages == 5  # 25 rows / 5 per page
        assert datatable_component.current_page == 1  # Should reset to first page

    def test_set_rows_per_page_invalid_string(self, datatable_component):
        """Test setting invalid rows per page string."""
        original_rows_per_page = datatable_component.rows_per_page
        datatable_component.set_rows_per_page("invalid")

        assert datatable_component.rows_per_page == DataTableComponent.DEFAULT_ROW_PER_PAGE

    def test_set_rows_per_page_zero(self, datatable_component):
        """Test setting rows per page to zero."""
        datatable_component.set_rows_per_page("0")

        assert datatable_component.rows_per_page == DataTableComponent.DEFAULT_ROW_PER_PAGE

    def test_set_rows_per_page_too_high(self, datatable_component):
        """Test setting rows per page higher than total rows."""
        datatable_component.set_rows_per_page("100")

        assert datatable_component.rows_per_page == DataTableComponent.DEFAULT_ROW_PER_PAGE

    @patch.object(DataTableComponent, '_safe_update')
    def test_refresh_data_updates_ui(self, mock_safe_update, datatable_component):
        """Test that refresh_data properly updates UI elements."""
        datatable_component.refresh_data()

        # Check that the count text is updated
        assert "Total Rows: 25" in datatable_component.v_count.value

        # Check that current page text is updated
        assert datatable_component.v_current_page.content.value == "1/3"

        # Check that safe update was called
        mock_safe_update.assert_called_once()

    def test_empty_datatable_handling(self):
        """Test handling of empty datatable."""
        empty_datatable = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("Empty"))],
            rows=[]
        )
        component = DataTableComponent(empty_datatable)

        assert component.num_rows == 0
        assert component.num_pages == 0
        assert component.current_page == 1

    def test_single_row_datatable(self):
        """Test handling of datatable with single row."""
        single_row_datatable = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("Single"))],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("1"))])]
        )
        component = DataTableComponent(single_row_datatable)

        assert component.num_rows == 1
        assert component.num_pages == 1
        assert component.current_page == 1

    def test_ui_component_structure(self, datatable_component):
        """Test that UI components are properly structured."""
        # Check that the component has the expected structure
        assert isinstance(datatable_component.content, ft.Container)
        assert isinstance(datatable_component.content.content, ft.Column)

        # Check that pagination controls exist
        assert datatable_component.shown_datatable is not None
        assert datatable_component.v_count is not None
        assert datatable_component.v_current_page is not None
        assert datatable_component.current_page_changer_field is not None
        assert datatable_component.v_num_of_row_changer_field is not None

    def test_data_table_properties(self, datatable_component):
        """Test that the shown datatable has correct properties."""
        shown_dt = datatable_component.shown_datatable

        assert shown_dt.border_radius == 10
        assert shown_dt.heading_row_color == ft.Colors.BLACK12
        assert shown_dt.data_row_color == {"hovered": "0x30FF0000"}
        assert shown_dt.divider_thickness == 0
        assert shown_dt.show_bottom_border == True

    def test_current_page_field_properties(self, datatable_component):
        """Test current page text field properties."""
        field = datatable_component.current_page_changer_field

        assert field.dense == True
        assert field.filled == False
        assert field.width == 40
        assert field.visible == False
        assert field.keyboard_type == ft.KeyboardType.NUMBER
        assert field.content_padding == 2
        assert field.text_align == ft.TextAlign.CENTER

    def test_rows_per_page_field_properties(self, datatable_component):
        """Test rows per page field properties."""
        field = datatable_component.v_num_of_row_changer_field

        assert field.dense == True
        assert field.filled == False
        assert field.width == 40
        assert field.keyboard_type == ft.KeyboardType.NUMBER
        assert field.content_padding == 2
        assert field.text_align == ft.TextAlign.CENTER

    def test_toggle_page_field(self, datatable_component):
        """Test toggling between page display and input field."""
        mock_event = Mock()

        # Initially, current page should be visible and field hidden
        assert datatable_component.v_current_page.visible == True
        assert datatable_component.current_page_changer_field.visible == False

        # Toggle to show field
        datatable_component.toggle_page_field(mock_event)

        assert datatable_component.v_current_page.visible == False
        assert datatable_component.current_page_changer_field.visible == True
        assert datatable_component.current_page_changer_field.value == "1"

    def test_hide_page_field(self, datatable_component):
        """Test hiding page input field."""
        mock_event = Mock()

        # Setup field as visible
        datatable_component.current_page_changer_field.visible = True
        datatable_component.v_current_page.visible = False

        # Hide the field
        datatable_component.hide_page_field(mock_event)

        assert datatable_component.current_page_changer_field.visible == False
        assert datatable_component.v_current_page.visible == True

    def test_on_page_field_submit(self, datatable_component):
        """Test page field submission."""
        mock_event = Mock()
        mock_event.control.value = "2"

        # Ensure we start on page 1
        assert datatable_component.current_page == 1

        # Submit page change
        datatable_component.on_page_field_submit(mock_event)

        # Should change to page 2 and hide field
        assert datatable_component.current_page == 2
        assert datatable_component.current_page_changer_field.visible == False
        assert datatable_component.v_current_page.visible == True

    def test_update_data_with_new_datatable(self, datatable_component):
        """Test updating component with new datatable data."""
        # Create new datatable with different data
        new_columns = [
            ft.DataColumn(ft.Text("New ID")),
            ft.DataColumn(ft.Text("New Name")),
        ]
        new_rows = []
        for i in range(15):  # Different number of rows
            new_rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(f"N{i + 1}")),
                ft.DataCell(ft.Text(f"New Item {i + 1}")),
            ]))

        new_datatable = ft.DataTable(columns=new_columns, rows=new_rows)

        # Update the component
        datatable_component.update_data(new_datatable)

        # Check that data was updated
        assert datatable_component.num_rows == 15
        assert datatable_component.num_pages == 2  # 15 rows / 10 per page = 2 pages
        assert datatable_component.current_page == 1  # Should reset to first page
        assert datatable_component.shown_datatable.columns == new_columns

    def test_update_data_resets_page_if_current_page_invalid(self, datatable_component):
        """Test that update_data resets current page if it becomes invalid."""
        # Start on page 3
        datatable_component.current_page = 3

        # Create new datatable with only 5 rows (1 page)
        new_columns = [ft.DataColumn(ft.Text("Test"))]
        new_rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(str(i)))]) for i in range(5)]
        new_datatable = ft.DataTable(columns=new_columns, rows=new_rows)

        # Update the component
        datatable_component.update_data(new_datatable)

        # Should reset to page 1 since page 3 no longer exists
        assert datatable_component.current_page == 1
        assert datatable_component.num_pages == 1

    def test_safe_update_without_page(self, datatable_component):
        """Test that _safe_update doesn't crash when component isn't on a page."""
        # This should not raise an exception
        datatable_component._safe_update()

    def test_gesture_detector_structure(self, datatable_component):
        """Test that v_current_page is a GestureDetector with correct structure."""
        assert isinstance(datatable_component.v_current_page, ft.GestureDetector)
        assert isinstance(datatable_component.v_current_page.content, ft.Text)
        assert datatable_component.v_current_page.on_double_tap is not None

    def test_edge_case_zero_pages(self):
        """Test handling when there are no pages (empty data)."""
        empty_datatable = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("Empty"))],
            rows=[]
        )
        component = DataTableComponent(empty_datatable)

        # Should handle gracefully
        assert component.num_pages == 0
        assert component.current_page == 1

        # Pagination should work without errors
        mock_event = Mock()
        component.next_page(mock_event)  # Should not crash
        component.prev_page(mock_event)  # Should not crash

    def test_rows_per_page_field_validation_edge_cases(self, datatable_component):
        """Test edge cases for rows per page validation."""
        # Test negative number
        datatable_component.set_rows_per_page("-5")
        assert datatable_component.rows_per_page == DataTableComponent.DEFAULT_ROW_PER_PAGE

        # Test decimal number
        datatable_component.set_rows_per_page("5.5")
        assert datatable_component.rows_per_page == DataTableComponent.DEFAULT_ROW_PER_PAGE

        # Test empty string
        datatable_component.set_rows_per_page("")
        assert datatable_component.rows_per_page == DataTableComponent.DEFAULT_ROW_PER_PAGE