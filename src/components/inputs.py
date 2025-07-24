from typing import Callable, Optional, Tuple
import flet as ft
from utils.logger import logger

class InputComponent(ft.Container):
	def __init__(
		self, 
		icon: ft.Icons, 
		label: str, 
		password: bool = False , 
		value: str = "",
		validator: Optional[Callable[[str], Tuple[bool, str]]] = None
	):
		"""
        Args:
            icon: The icon to display
            label: The label for the input field
            password: Whether this is a password field
            value: Initial value
            validator: A function that takes the current value and returns True if valid
        """
		super().__init__(
			# padding = 5,
			# margin = 2,
		)

		self.icon = icon
		self.label = label
		self.password = password
		self.value = value
		self.validator = validator

		self.input_field = ft.TextField(
			hint_text = self.label,
			border_color = "transparent",
			# bgcolor = "transparent",
			value = self.value,
			content_padding = 3,
			password = self.password,
			expand = True,
			can_reveal_password = True,
			error_style = ft.TextStyle(
				color = "#DC3E42"
			),
			on_blur=self._handle_change,
		)

		self.input_icon = ft.Icon(
			name = self.icon,
			opacity = 0.85,
		)

		self.content = ft.Container(
			padding = 0,
			margin = 0,
			height = 40,
			border = ft.border.only(
				bottom=ft.border.BorderSide(1, "white54")
			),
			content = ft.Column(
				spacing = 0,
				controls = [
					ft.Row(
						spacing=10,
						vertical_alignment=ft.CrossAxisAlignment.CENTER,
						controls=[
							self.input_icon,
							self.input_field,
						]
					)
				]
			)
		)

	def _handle_change(self, e):
		if self.validator is not None:
			is_valid, error_msg = self.validator(self.input_field.value)
			if is_valid:
				self.content = ft.Container(
					padding = 0,
					margin = 0,
					height = 40,
					border = ft.border.only(
						bottom=ft.border.BorderSide(1, "white54")
					),
					content = ft.Column(
						spacing = 0,
						controls = [
							ft.Row(
								spacing=10,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
								controls=[
									self.input_icon,
									self.input_field,
								]
							),
						]
					)
				)
			else:
				self.content = ft.Container(
					padding = 0,
					margin = 0,
					height = 40,
					border = ft.border.only(
						bottom=ft.border.BorderSide(1, "#DC3E42")
					),
					content = ft.Column(
						spacing = 0,
						tight=True,
						controls = [
							ft.Row(
								spacing=10,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
								controls=[
									ft.Icon(
										name = self.icon,
										opacity = 0.85,
										color = "#DC3E42"
									),
									self.input_field,
								]
							),
							ft.Text(
								error_msg,
								color = "#DC3E42",
				                size=14,
				                height=16,
				                offset=ft.Offset(0, -0.3)
							)
						]
					)
				)
			self.update()

	@property
	def input_value(self):
		return self.input_field.value

	def set_value(self, new_value):
		self.input_field.value = new_value

