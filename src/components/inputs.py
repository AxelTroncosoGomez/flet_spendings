import flet as ft
from utils.logger import logger

class InputComponent(ft.Container):
	def __init__(self, icon: ft.Icons, label: str, password: bool = False , value: str = ""):
		super().__init__(
			height=40,
			border=ft.border.only(
				bottom=ft.border.BorderSide(0.5, "white54")
			)
		)
		self.icon = icon
		self.label = label
		self.password = password
		self.value = value

		self.input_field = ft.TextField(
			label = self.label,
			border_color = "transparent",
			# bgcolor = "transparent",
			value = self.value,
			content_padding = 3,
			# cursor_color = "white",
			password = self.password,
			expand = True
		)

		self.input_icon = ft.Icon(
			name = self.icon,
			opacity = 0.85
		)

		self.content = ft.Row(
			spacing=10,
			vertical_alignment=ft.CrossAxisAlignment.CENTER,
			controls=[
				self.input_icon,
				self.input_field,
			]
		)

	@property
	def input_value(self):
		return self.input_field.value

	def set_value(self, new_value):
		self.input_field.value = new_value