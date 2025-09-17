import pytest
import flet as ft
from unittest.mock import Mock, MagicMock, patch

from components.buttons import ImageButtonComponent, ButtonComponent


class TestImageButtonComponent:
    """Test suite for ImageButtonComponent class."""

    def test_initialization_with_valid_parameters(self):
        """Test ImageButtonComponent initialization with valid parameters."""
        color = ft.Colors.BLUE
        text = "Test Button"
        src_image = "test_image.png"
        trigger = Mock()

        button = ImageButtonComponent(color, text, src_image, trigger)

        assert button.color == color
        assert button.text == text
        assert button.src_image == src_image
        assert button.trigger == trigger

    def test_initialization_creates_elevated_button(self):
        """Test that initialization creates an ElevatedButton as content."""
        button = ImageButtonComponent(ft.Colors.RED, "Test", "image.png", Mock())

        assert isinstance(button.content, ft.ElevatedButton)

    def test_elevated_button_properties(self):
        """Test that the ElevatedButton has correct properties."""
        color = ft.Colors.GREEN
        text = "Sample Text"
        src_image = "sample.png"
        trigger = Mock()

        button = ImageButtonComponent(color, text, src_image, trigger)
        elevated_button = button.content

        assert elevated_button.height == 40
        assert elevated_button.width == 350
        assert elevated_button.on_click == trigger

    def test_button_style_configuration(self):
        """Test that button style is configured correctly."""
        color = ft.Colors.PURPLE
        button = ImageButtonComponent(color, "Test", "image.png", Mock())

        button_style = button.content.style

        assert button_style is not None
        assert "" in button_style.shape
        assert isinstance(button_style.shape[""], ft.RoundedRectangleBorder)
        assert button_style.shape[""].radius == 20
        assert "" in button_style.bgcolor
        assert button_style.bgcolor[""] == color

    def test_button_content_structure(self):
        """Test that button content has correct structure."""
        text = "Button Text"
        src_image = "button_image.png"

        button = ImageButtonComponent(ft.Colors.BLUE, text, src_image, Mock())
        content = button.content.content

        assert isinstance(content, ft.Row)
        assert len(content.controls) == 2
        assert content.spacing == 15
        assert content.alignment == ft.MainAxisAlignment.CENTER

    def test_image_component_properties(self):
        """Test that image component has correct properties."""
        src_image = "test_icon.png"
        button = ImageButtonComponent(ft.Colors.ORANGE, "Test", src_image, Mock())

        image = button.content.content.controls[0]

        assert isinstance(image, ft.Image)
        assert image.src == src_image
        assert image.width == 24
        assert image.height == 24

    def test_text_component_properties(self):
        """Test that text component has correct properties."""
        text = "Custom Button Text"
        button = ImageButtonComponent(ft.Colors.CYAN, text, "image.png", Mock())

        text_component = button.content.content.controls[1]

        assert isinstance(text_component, ft.Text)
        assert text_component.value == text
        assert text_component.size == 15
        assert text_component.color == "black"

    def test_inheritance_from_container(self):
        """Test that ImageButtonComponent inherits from ft.Container."""
        button = ImageButtonComponent(ft.Colors.YELLOW, "Test", "image.png", Mock())

        assert isinstance(button, ft.Container)

    def test_trigger_function_assignment(self):
        """Test that trigger function is correctly assigned."""
        mock_trigger = Mock()
        button = ImageButtonComponent(ft.Colors.RED, "Test", "image.png", mock_trigger)

        assert button.content.on_click == mock_trigger

    def test_with_none_trigger(self):
        """Test button creation with None trigger."""
        button = ImageButtonComponent(ft.Colors.BLUE, "Test", "image.png", None)

        assert button.content.on_click is None

    def test_with_empty_string_text(self):
        """Test button creation with empty string text."""
        button = ImageButtonComponent(ft.Colors.GREEN, "", "image.png", Mock())

        text_component = button.content.content.controls[1]
        assert text_component.value == ""

    def test_with_empty_string_image_src(self):
        """Test button creation with empty string image source."""
        button = ImageButtonComponent(ft.Colors.PURPLE, "Test", "", Mock())

        image_component = button.content.content.controls[0]
        assert image_component.src == ""

    def test_with_long_text(self):
        """Test button creation with very long text."""
        long_text = "Very long button text that might overflow " * 10
        button = ImageButtonComponent(ft.Colors.ORANGE, long_text, "image.png", Mock())

        text_component = button.content.content.controls[1]
        assert text_component.value == long_text

    def test_with_special_characters_in_text(self):
        """Test button creation with special characters in text."""
        special_text = "Test ñáéíóú 🚀 中文"
        button = ImageButtonComponent(ft.Colors.PINK, special_text, "image.png", Mock())

        text_component = button.content.content.controls[1]
        assert text_component.value == special_text

    def test_with_special_characters_in_image_path(self):
        """Test button creation with special characters in image path."""
        special_path = "path/with spaces/and-special_chars.png"
        button = ImageButtonComponent(ft.Colors.LIME, "Test", special_path, Mock())

        image_component = button.content.content.controls[0]
        assert image_component.src == special_path

    def test_multiple_instances_independence(self):
        """Test that multiple instances are independent."""
        trigger1 = Mock()
        trigger2 = Mock()

        button1 = ImageButtonComponent(ft.Colors.RED, "Button 1", "image1.png", trigger1)
        button2 = ImageButtonComponent(ft.Colors.BLUE, "Button 2", "image2.png", trigger2)

        assert button1.color != button2.color
        assert button1.text != button2.text
        assert button1.src_image != button2.src_image
        assert button1.trigger != button2.trigger

    def test_button_click_simulation(self):
        """Test simulating button click."""
        mock_trigger = Mock()
        button = ImageButtonComponent(ft.Colors.GREEN, "Clickable", "icon.png", mock_trigger)

        # Simulate click by calling the trigger directly
        mock_event = Mock()
        button.content.on_click(mock_event)

        mock_trigger.assert_called_once_with(mock_event)

    def test_color_types_compatibility(self):
        """Test compatibility with different color types."""
        # Test with ft.Colors enum
        button1 = ImageButtonComponent(ft.Colors.AMBER, "Test", "image.png", Mock())
        assert button1.color == ft.Colors.AMBER

        # Test with hex color string
        hex_color = "#FF5722"
        button2 = ImageButtonComponent(hex_color, "Test", "image.png", Mock())
        assert button2.color == hex_color

        # Test with color name string
        color_name = "red"
        button3 = ImageButtonComponent(color_name, "Test", "image.png", Mock())
        assert button3.color == color_name


class TestButtonComponent:
    """Test suite for ButtonComponent class."""

    def test_initialization_with_valid_parameters(self):
        """Test ButtonComponent initialization with valid parameters."""
        text = "Test Button"
        trigger = Mock()
        color = ft.Colors.BLUE

        button = ButtonComponent(text, trigger, color)

        assert button.text == text
        assert button.trigger == trigger
        assert button.color == color

    def test_initialization_creates_elevated_button(self):
        """Test that initialization creates an ElevatedButton as content."""
        button = ButtonComponent("Test", Mock(), ft.Colors.RED)

        assert isinstance(button.content, ft.ElevatedButton)

    def test_elevated_button_properties(self):
        """Test that the ElevatedButton has correct properties."""
        text = "Sample Button"
        trigger = Mock()
        color = ft.Colors.GREEN

        button = ButtonComponent(text, trigger, color)
        elevated_button = button.content

        assert elevated_button.height == 40
        assert elevated_button.width == 350
        assert elevated_button.on_click == trigger

    def test_button_style_configuration(self):
        """Test that button style is configured correctly."""
        color = ft.Colors.PURPLE
        button = ButtonComponent("Test", Mock(), color)

        button_style = button.content.style

        assert button_style is not None
        assert "" in button_style.shape
        assert isinstance(button_style.shape[""], ft.RoundedRectangleBorder)
        assert button_style.shape[""].radius == 20
        assert "" in button_style.color
        assert button_style.color[""] == "black"
        assert "" in button_style.bgcolor
        assert button_style.bgcolor[""] == color

    def test_button_content_structure(self):
        """Test that button content has correct structure."""
        text = "Button Text"
        button = ButtonComponent(text, Mock(), ft.Colors.BLUE)
        content = button.content.content

        assert isinstance(content, ft.Text)
        assert content.value == text
        assert content.size == 16

    def test_inheritance_from_container(self):
        """Test that ButtonComponent inherits from ft.Container."""
        button = ButtonComponent("Test", Mock(), ft.Colors.YELLOW)

        assert isinstance(button, ft.Container)

    def test_trigger_function_assignment(self):
        """Test that trigger function is correctly assigned."""
        mock_trigger = Mock()
        button = ButtonComponent("Test", mock_trigger, ft.Colors.RED)

        assert button.content.on_click == mock_trigger

    def test_with_none_trigger(self):
        """Test button creation with None trigger."""
        button = ButtonComponent("Test", None, ft.Colors.BLUE)

        assert button.content.on_click is None

    def test_with_empty_string_text(self):
        """Test button creation with empty string text."""
        button = ButtonComponent("", Mock(), ft.Colors.GREEN)

        assert button.content.content.value == ""

    def test_with_long_text(self):
        """Test button creation with very long text."""
        long_text = "Very long button text that might overflow " * 10
        button = ButtonComponent(long_text, Mock(), ft.Colors.ORANGE)

        assert button.content.content.value == long_text

    def test_with_special_characters_in_text(self):
        """Test button creation with special characters in text."""
        special_text = "Test ñáéíóú 🚀 中文"
        button = ButtonComponent(special_text, Mock(), ft.Colors.PINK)

        assert button.content.content.value == special_text

    def test_multiple_instances_independence(self):
        """Test that multiple instances are independent."""
        trigger1 = Mock()
        trigger2 = Mock()

        button1 = ButtonComponent("Button 1", trigger1, ft.Colors.RED)
        button2 = ButtonComponent("Button 2", trigger2, ft.Colors.BLUE)

        assert button1.text != button2.text
        assert button1.trigger != button2.trigger
        assert button1.color != button2.color

    def test_button_click_simulation(self):
        """Test simulating button click."""
        mock_trigger = Mock()
        button = ButtonComponent("Clickable", mock_trigger, ft.Colors.GREEN)

        # Simulate click by calling the trigger directly
        mock_event = Mock()
        button.content.on_click(mock_event)

        mock_trigger.assert_called_once_with(mock_event)

    def test_color_types_compatibility(self):
        """Test compatibility with different color types."""
        # Test with ft.Colors enum
        button1 = ButtonComponent("Test", Mock(), ft.Colors.AMBER)
        assert button1.color == ft.Colors.AMBER

        # Test with hex color string
        hex_color = "#FF5722"
        button2 = ButtonComponent("Test", Mock(), hex_color)
        assert button2.color == hex_color

        # Test with color name string
        color_name = "red"
        button3 = ButtonComponent("Test", Mock(), color_name)
        assert button3.color == color_name

    def test_text_parameter_types(self):
        """Test that text parameter accepts different types."""
        # Test with string
        button1 = ButtonComponent("String text", Mock(), ft.Colors.BLUE)
        assert button1.text == "String text"

        # Test with number (should be converted to string by ft.Text)
        button2 = ButtonComponent(123, Mock(), ft.Colors.RED)
        assert button2.text == 123

    def test_button_default_text_color(self):
        """Test that button text color is set to black by default."""
        button = ButtonComponent("Test", Mock(), ft.Colors.WHITE)

        style = button.content.style
        assert style.color[""] == "black"


class TestButtonComponentsComparison:
    """Test suite comparing ImageButtonComponent and ButtonComponent."""

    def test_both_inherit_from_container(self):
        """Test that both components inherit from ft.Container."""
        image_button = ImageButtonComponent(ft.Colors.BLUE, "Test", "icon.png", Mock())
        button = ButtonComponent("Test", Mock(), ft.Colors.BLUE)

        assert isinstance(image_button, ft.Container)
        assert isinstance(button, ft.Container)

    def test_both_create_elevated_button_content(self):
        """Test that both components create ElevatedButton as content."""
        image_button = ImageButtonComponent(ft.Colors.RED, "Test", "icon.png", Mock())
        button = ButtonComponent("Test", Mock(), ft.Colors.RED)

        assert isinstance(image_button.content, ft.ElevatedButton)
        assert isinstance(button.content, ft.ElevatedButton)

    def test_both_have_same_button_dimensions(self):
        """Test that both components create buttons with same dimensions."""
        image_button = ImageButtonComponent(ft.Colors.GREEN, "Test", "icon.png", Mock())
        button = ButtonComponent("Test", Mock(), ft.Colors.GREEN)

        assert image_button.content.height == button.content.height == 40
        assert image_button.content.width == button.content.width == 350

    def test_both_have_same_button_style_properties(self):
        """Test that both components have similar style properties."""
        color = ft.Colors.PURPLE
        image_button = ImageButtonComponent(color, "Test", "icon.png", Mock())
        button = ButtonComponent("Test", Mock(), color)

        # Both should have rounded borders with radius 20
        assert image_button.content.style.shape[""].radius == 20
        assert button.content.style.shape[""].radius == 20

        # Both should use the provided background color
        assert image_button.content.style.bgcolor[""] == color
        assert button.content.style.bgcolor[""] == color

    def test_content_structure_differences(self):
        """Test the differences in content structure."""
        image_button = ImageButtonComponent(ft.Colors.BLUE, "Test", "icon.png", Mock())
        button = ButtonComponent("Test", Mock(), ft.Colors.BLUE)

        # ImageButton has Row content with Image and Text
        assert isinstance(image_button.content.content, ft.Row)
        assert len(image_button.content.content.controls) == 2

        # Regular Button has Text content only
        assert isinstance(button.content.content, ft.Text)


class TestButtonComponentsEdgeCases:
    """Test edge cases for both button components."""

    def test_with_callable_objects_as_triggers(self):
        """Test buttons with different callable objects as triggers."""
        def test_function():
            pass

        class TestClass:
            def __call__(self):
                pass

        callable_obj = TestClass()

        # Test with function
        button1 = ButtonComponent("Test", test_function, ft.Colors.BLUE)
        assert button1.trigger == test_function

        # Test with callable object
        button2 = ImageButtonComponent(ft.Colors.RED, "Test", "icon.png", callable_obj)
        assert button2.trigger == callable_obj

    def test_with_none_color(self):
        """Test buttons with None color."""
        button1 = ButtonComponent("Test", Mock(), None)
        button2 = ImageButtonComponent(None, "Test", "icon.png", Mock())

        assert button1.color is None
        assert button2.color is None

    def test_parameter_mutation_independence(self):
        """Test that modifying parameters after creation doesn't affect button."""
        original_text = "Original"
        original_color = ft.Colors.BLUE

        button = ButtonComponent(original_text, Mock(), original_color)

        # Modify original variables (shouldn't affect button)
        original_text = "Modified"

        # Button should retain original values
        assert button.text == "Original"
        assert button.color == ft.Colors.BLUE

    @patch('components.buttons.logger')
    def test_logger_import(self, mock_logger):
        """Test that logger is imported and accessible."""
        # Create button to ensure module is loaded
        ButtonComponent("Test", Mock(), ft.Colors.BLUE)

        # Logger should be available in the module
        from components.buttons import logger
        assert logger is not None

    def test_image_button_with_relative_path(self):
        """Test ImageButton with relative image path."""
        relative_path = "../assets/icon.png"
        button = ImageButtonComponent(ft.Colors.GREEN, "Test", relative_path, Mock())

        image = button.content.content.controls[0]
        assert image.src == relative_path

    def test_image_button_with_absolute_path(self):
        """Test ImageButton with absolute image path."""
        absolute_path = "/usr/share/icons/test.png"
        button = ImageButtonComponent(ft.Colors.ORANGE, "Test", absolute_path, Mock())

        image = button.content.content.controls[0]
        assert image.src == absolute_path

    def test_image_button_with_url_path(self):
        """Test ImageButton with URL image path."""
        url_path = "https://example.com/icon.png"
        button = ImageButtonComponent(ft.Colors.CYAN, "Test", url_path, Mock())

        image = button.content.content.controls[0]
        assert image.src == url_path