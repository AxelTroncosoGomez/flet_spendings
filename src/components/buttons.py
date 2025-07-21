import flet as ft
from utils.logger import logger

class ImageButtonComponent(ft.Container):
	def __init__(self, color, text, src_image, trigger):
		super().__init__()

		self.color = color
		self.text = text
		self.src_image = src_image
		self.trigger = trigger

		self.content = ft.ElevatedButton(
			style = ft.ButtonStyle(
				shape = {
					"": ft.RoundedRectangleBorder(radius=20),
				},
				bgcolor = {
					"": self.color
				}
			),
			height = 40,
			width = 350,
			content=ft.Row(
				[
					ft.VerticalDivider(width=1, color="transparent"),
					ft.Image(
						src=self.src_image,
						width=24,
						height=24,
						# border_radius=ft.border_radius.all(10),
					),
					ft.Text(self.text, size=15, color="black"),
				],
				spacing=15,
				alignment=ft.MainAxisAlignment.START,
			),
			on_click = self.trigger
		)


class ButtonComponent(ft.Container):
	def __init__(self, text: str, trigger, color):
		super().__init__()

		self.text = text
		self.trigger = trigger
		self.color = color

		self.content = ft.ElevatedButton(
			content = ft.Text(self.text, size=16),
			style = ft.ButtonStyle(
				shape = {
					"": ft.RoundedRectangleBorder(radius=20),
				},
				color = {
					"": "black"
				},
				bgcolor = {
					"": self.color
				}
			),
			height = 40,
			width = 350,
			on_click = self.trigger
		)