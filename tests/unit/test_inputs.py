import pytest
import flet as ft
from unittest.mock import Mock, MagicMock, patch

from components.inputs import InputComponent


class TestInputComponent:
    """Test suite for InputComponent class."""

    def test_initialization_with_required_parameters(self):
        """Test InputComponent initialization with required parameters."""
        icon = ft.Icons.PERSON
        label = "Username"

        input_comp = InputComponent(icon, label)

        assert input_comp.icon == icon
        assert input_comp.label == label
        assert input_comp.password is False
        assert input_comp.value == ""
        assert input_comp.validator is None

    def test_initialization_with_all_parameters(self):
        """Test InputComponent initialization with all parameters."""
        icon = ft.Icons.LOCK
        label = "Password"
        password = True
        value = "initial_value"
        validator = Mock()

        input_comp = InputComponent(icon, label, password, value, validator)

        assert input_comp.icon == icon
        assert input_comp.label == label
        assert input_comp.password == password
        assert input_comp.value == value
        assert input_comp.validator == validator

    def test_inheritance_from_container(self):
        """Test that InputComponent inherits from ft.Container."""
        input_comp = InputComponent(ft.Icons.EMAIL, "Email")

        assert isinstance(input_comp, ft.Container)

    def test_text_field_creation(self):
        """Test that TextField is created with correct properties."""
        label = "Test Input"
        value = "test_value"
        input_comp = InputComponent(ft.Icons.TEXT_FIELDS, label, value=value)

        text_field = input_comp.input_field

        assert isinstance(text_field, ft.TextField)
        assert text_field.hint_text == label
        assert text_field.value == value
        assert text_field.border_color == "transparent"
        assert text_field.content_padding == 3
        assert text_field.expand is True
        assert text_field.can_reveal_password is True

    def test_password_field_configuration(self):
        """Test password field specific configuration."""
        input_comp = InputComponent(ft.Icons.LOCK, "Password", password=True)

        assert input_comp.input_field.password is True

    def test_non_password_field_configuration(self):
        """Test non-password field configuration."""
        input_comp = InputComponent(ft.Icons.PERSON, "Username", password=False)

        assert input_comp.input_field.password is False

    def test_icon_creation(self):
        """Test that icon is created with correct properties."""
        icon = ft.Icons.STAR
        input_comp = InputComponent(icon, "Test")

        input_icon = input_comp.input_icon

        assert isinstance(input_icon, ft.Icon)
        assert input_icon.name == icon
        assert input_icon.opacity == 0.85

    def test_container_structure(self):
        """Test that container has correct structure."""
        input_comp = InputComponent(ft.Icons.HOME, "Test")

        container = input_comp.content

        assert isinstance(container, ft.Container)
        assert container.padding == 0
        assert container.margin == 0
        assert container.height == 40

    def test_container_border_configuration(self):
        """Test that container has correct border configuration."""
        input_comp = InputComponent(ft.Icons.SEARCH, "Search")

        border = input_comp.content.border

        assert border is not None
        assert hasattr(border, 'bottom')
        assert border.bottom.width == 1
        assert border.bottom.color == "white54"

    def test_content_column_structure(self):
        """Test that content column has correct structure."""
        input_comp = InputComponent(ft.Icons.PHONE, "Phone")

        column = input_comp.content.content

        assert isinstance(column, ft.Column)
        assert column.spacing == 0
        assert len(column.controls) == 1

    def test_content_row_structure(self):
        """Test that content row has correct structure."""
        input_comp = InputComponent(ft.Icons.CALENDAR_TODAY, "Date")

        row = input_comp.content.content.controls[0]

        assert isinstance(row, ft.Row)
        assert row.spacing == 10
        assert row.vertical_alignment == ft.CrossAxisAlignment.CENTER
        assert len(row.controls) == 2

    def test_row_controls_content(self):
        """Test that row contains icon and text field."""
        input_comp = InputComponent(ft.Icons.LOCATION_ON, "Location")

        row_controls = input_comp.content.content.controls[0].controls

        assert row_controls[0] == input_comp.input_icon
        assert row_controls[1] == input_comp.input_field

    def test_input_value_property(self):
        """Test input_value property returns correct value."""
        initial_value = "test_value"
        input_comp = InputComponent(ft.Icons.EDIT, "Edit", value=initial_value)

        assert input_comp.input_value == initial_value

    def test_input_value_property_after_change(self):
        """Test input_value property after field value changes."""
        input_comp = InputComponent(ft.Icons.EDIT, "Edit")
        new_value = "new_value"

        input_comp.input_field.value = new_value

        assert input_comp.input_value == new_value

    def test_set_value_method(self):
        """Test set_value method updates field value."""
        input_comp = InputComponent(ft.Icons.EDIT, "Edit")
        new_value = "updated_value"

        input_comp.set_value(new_value)

        assert input_comp.input_field.value == new_value
        assert input_comp.input_value == new_value

    @patch.object(InputComponent, 'update')
    def test_set_error_method(self, mock_update):
        """Test set_error method creates error state."""
        input_comp = InputComponent(ft.Icons.WARNING, "Test")
        error_message = "This field is required"

        input_comp.set_error(error_message)

        # Check that content was updated to error state
        assert isinstance(input_comp.content, ft.Container)
        assert input_comp.content.height == 40

        # Check border color changed to error color
        border = input_comp.content.border
        assert border.bottom.color == "#DC3E42"

        # Check that column has error text
        column = input_comp.content.content
        assert len(column.controls) == 2

        # Check error text properties
        error_text = column.controls[1]
        assert isinstance(error_text, ft.Text)
        assert error_text.value == error_message
        assert error_text.color == "#DC3E42"
        assert error_text.size == 14

        # Check that icon color changed to error color
        error_icon = column.controls[0].controls[0]
        assert error_icon.color == "#DC3E42"

        mock_update.assert_called_once()

    @patch.object(InputComponent, 'update')
    def test_reset_method(self, mock_update):
        """Test reset method restores normal state."""
        input_comp = InputComponent(ft.Icons.REFRESH, "Test")

        # First set error state
        input_comp.set_error("Error message")

        # Then reset
        input_comp.reset()

        # Check that content was reset to normal state
        container = input_comp.content
        assert container.height == 40

        # Check border color reset to normal
        border = container.border
        assert border.bottom.color == "white54"

        # Check that column has only one control (no error text)
        column = container.content
        assert len(column.controls) == 1

        mock_update.assert_called()

    def test_handle_change_with_valid_validator(self):
        """Test _handle_change with validator that returns valid."""
        def valid_validator(value):
            return True, ""

        input_comp = InputComponent(ft.Icons.CHECK, "Test", validator=valid_validator)

        with patch.object(input_comp, 'update') as mock_update:
            mock_event = Mock()
            input_comp._handle_change(mock_event)

            # Should update to normal state
            border = input_comp.content.border
            assert border.bottom.color == "white54"
            mock_update.assert_called_once()

    def test_handle_change_with_invalid_validator(self):
        """Test _handle_change with validator that returns invalid."""
        error_message = "Invalid input"

        def invalid_validator(value):
            return False, error_message

        input_comp = InputComponent(ft.Icons.ERROR, "Test", validator=invalid_validator)

        with patch.object(input_comp, 'update') as mock_update:
            mock_event = Mock()
            input_comp._handle_change(mock_event)

            # Should update to error state
            border = input_comp.content.border
            assert border.bottom.color == "#DC3E42"

            # Should have error text
            column = input_comp.content.content
            assert len(column.controls) == 2
            error_text = column.controls[1]
            assert error_text.value == error_message

            mock_update.assert_called_once()

    def test_handle_change_without_validator(self):
        """Test _handle_change without validator does nothing."""
        input_comp = InputComponent(ft.Icons.PERSON, "Test")

        with patch.object(input_comp, 'update') as mock_update:
            mock_event = Mock()
            input_comp._handle_change(mock_event)

            # Should not call update since no validator
            mock_update.assert_not_called()

    def test_text_field_event_handlers(self):
        """Test that TextField has correct event handlers."""
        input_comp = InputComponent(ft.Icons.EVENT, "Test")

        text_field = input_comp.input_field

        assert text_field.on_blur == input_comp._handle_change

    def test_error_style_configuration(self):
        """Test that TextField has correct error style."""
        input_comp = InputComponent(ft.Icons.STYLE, "Test")

        error_style = input_comp.input_field.error_style

        assert isinstance(error_style, ft.TextStyle)
        assert error_style.color == "#DC3E42"

    def test_with_custom_validator_function(self):
        """Test with custom validator function."""
        def email_validator(value):
            if "@" in value:
                return True, ""
            return False, "Invalid email"

        input_comp = InputComponent(ft.Icons.EMAIL, "Email", validator=email_validator)

        assert input_comp.validator == email_validator

        # Test validation calls
        with patch.object(input_comp, 'update'):
            # Test valid email
            input_comp.input_field.value = "test@example.com"
            mock_event = Mock()
            input_comp._handle_change(mock_event)

            border = input_comp.content.border
            assert border.bottom.color == "white54"

            # Test invalid email
            input_comp.input_field.value = "invalid_email"
            input_comp._handle_change(mock_event)

            border = input_comp.content.border
            assert border.bottom.color == "#DC3E42"

    def test_with_lambda_validator(self):
        """Test with lambda validator."""
        validator = lambda x: (len(x) > 5, "Too short")

        input_comp = InputComponent(ft.Icons.KEY, "Key", validator=validator)

        assert input_comp.validator == validator

    def test_multiple_instances_independence(self):
        """Test that multiple instances are independent."""
        validator1 = Mock(return_value=(True, ""))
        validator2 = Mock(return_value=(False, "Error"))

        input1 = InputComponent(ft.Icons.PERSON, "Input 1", validator=validator1)
        input2 = InputComponent(ft.Icons.LOCK, "Input 2", password=True, validator=validator2)

        assert input1.icon != input2.icon
        assert input1.label != input2.label
        assert input1.password != input2.password
        assert input1.validator != input2.validator

    def test_with_unicode_label(self):
        """Test with unicode characters in label."""
        unicode_label = "用户名 ñáéíóú"
        input_comp = InputComponent(ft.Icons.PERSON, unicode_label)

        assert input_comp.label == unicode_label
        assert input_comp.input_field.hint_text == unicode_label

    def test_with_unicode_value(self):
        """Test with unicode characters in value."""
        unicode_value = "测试值 ñáéíóú"
        input_comp = InputComponent(ft.Icons.TEXT_FIELDS, "Test", value=unicode_value)

        assert input_comp.value == unicode_value
        assert input_comp.input_field.value == unicode_value

    def test_with_very_long_label(self):
        """Test with very long label."""
        long_label = "Very long label " * 50
        input_comp = InputComponent(ft.Icons.DESCRIPTION, long_label)

        assert input_comp.label == long_label
        assert input_comp.input_field.hint_text == long_label

    def test_with_very_long_value(self):
        """Test with very long value."""
        long_value = "Very long value " * 100
        input_comp = InputComponent(ft.Icons.TEXT_FIELDS, "Test", value=long_value)

        assert input_comp.value == long_value
        assert input_comp.input_field.value == long_value

    def test_with_empty_strings(self):
        """Test with empty strings for label and value."""
        input_comp = InputComponent(ft.Icons.CLEAR, "", value="")

        assert input_comp.label == ""
        assert input_comp.value == ""
        assert input_comp.input_field.hint_text == ""
        assert input_comp.input_field.value == ""

    def test_set_error_with_empty_message(self):
        """Test set_error with empty error message."""
        input_comp = InputComponent(ft.Icons.ERROR, "Test")

        with patch.object(input_comp, 'update'):
            input_comp.set_error("")

            # Should still create error state even with empty message
            border = input_comp.content.border
            assert border.bottom.color == "#DC3E42"

            # Error text should be empty
            error_text = input_comp.content.content.controls[1]
            assert error_text.value == ""

    def test_set_error_with_unicode_message(self):
        """Test set_error with unicode error message."""
        unicode_error = "错误信息 ñáéíóú"
        input_comp = InputComponent(ft.Icons.WARNING, "Test")

        with patch.object(input_comp, 'update'):
            input_comp.set_error(unicode_error)

            error_text = input_comp.content.content.controls[1]
            assert error_text.value == unicode_error

    def test_validator_return_value_handling(self):
        """Test handling of different validator return values."""
        def tuple_validator(value):
            return True, "Valid"

        input_comp = InputComponent(ft.Icons.VERIFIED, "Test", validator=tuple_validator)

        with patch.object(input_comp, 'update'):
            mock_event = Mock()
            input_comp._handle_change(mock_event)

            # Should handle tuple return correctly
            border = input_comp.content.border
            assert border.bottom.color == "white54"

    def test_validator_exception_handling(self):
        """Test handling when validator raises exception."""
        def exception_validator(value):
            raise ValueError("Validator error")

        input_comp = InputComponent(ft.Icons.DANGEROUS, "Test", validator=exception_validator)

        with patch.object(input_comp, 'update'):
            mock_event = Mock()
            # The current implementation doesn't handle exceptions, so we expect it to raise
            with pytest.raises(ValueError, match="Validator error"):
                input_comp._handle_change(mock_event)

    def test_container_styling_consistency(self):
        """Test that container styling is consistent across states."""
        input_comp = InputComponent(ft.Icons.STYLE, "Test")

        # Normal state
        normal_container = input_comp.content
        assert normal_container.padding == 0
        assert normal_container.margin == 0
        assert normal_container.height == 40

        # Error state
        with patch.object(input_comp, 'update'):
            input_comp.set_error("Error")

        error_container = input_comp.content
        assert error_container.padding == 0
        assert error_container.margin == 0
        assert error_container.height == 40

        # Reset state
        with patch.object(input_comp, 'update'):
            input_comp.reset()

        reset_container = input_comp.content
        assert reset_container.padding == 0
        assert reset_container.margin == 0
        assert reset_container.height == 40

    def test_icon_consistency_across_states(self):
        """Test that icon remains consistent across states."""
        icon = ft.Icons.STAR
        input_comp = InputComponent(icon, "Test")

        # Normal state icon
        normal_icon = input_comp.content.content.controls[0].controls[0]
        assert normal_icon.name == icon
        assert normal_icon.opacity == 0.85

        # Error state should change icon color but keep same icon
        with patch.object(input_comp, 'update'):
            input_comp.set_error("Error")

        error_icon = input_comp.content.content.controls[0].controls[0]
        assert error_icon.name == icon
        assert error_icon.color == "#DC3E42"

    @patch('components.inputs.logger')
    def test_logger_import(self, mock_logger):
        """Test that logger is imported and accessible."""
        # Create input to ensure module is loaded
        InputComponent(ft.Icons.LABEL, "Test")

        # Logger should be available in the module
        from components.inputs import logger
        assert logger is not None