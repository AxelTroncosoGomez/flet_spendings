import flet as ft
from components.buttons import ButtonComponent, ImageButtonComponent

class CrashPage(ft.View):

	def __init__(self, page: ft.Page, error_message: str):
		super().__init__(
			route="/error",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			scroll=ft.ScrollMode.AUTO
		)

		self.page = page
		self.error_message = error_message

		self.close_app_btn = ButtonComponent(
			text = "Exit App",
			trigger = self.close_app,
			color = "#e48c92"
		)

		self.controls = [
			ft.Container(
		        expand = True,
		        alignment = ft.alignment.center,
				content = ft.SafeArea(
					content = ft.ResponsiveRow(
						vertical_alignment=ft.CrossAxisAlignment.CENTER,
						alignment=ft.MainAxisAlignment.CENTER,
						controls = [
							ft.Container(
								col={"xs": 12, "md": 6, "lg": 4},
								content=ft.Card(
									width=360,
									height=400,
									elevation=10,
									color=ft.Colors.RED_100,
									content=ft.Container(
										padding=20,
										bgcolor=ft.Colors.RED_900,
										border_radius=8,
										content=ft.Column(
											spacing=10,
											horizontal_alignment=ft.CrossAxisAlignment.CENTER,
											alignment=ft.MainAxisAlignment.CENTER,
											controls=[
												ft.Icon(name=ft.Icons.ERROR_OUTLINE, color="white", size=40),
												ft.Text("Oops! Something went wrong.", size=18, color="white", weight="bold"),
												ft.Text(self.error_message, size=14, color="white", text_align="center"),
												ft.Text("Try again or restart the app.", size=12, color=ft.Colors.RED_200),
												self.close_app_btn
											]
										)
									)
								)
							)
						]
					)
				)
			)
		]

	def close_app(self, e):
		self.page.window.destroy() 