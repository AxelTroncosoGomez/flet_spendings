import flet as ft
from utils.logger import logger
from components.inputs import InputComponent
from components.buttons import ButtonComponent, ImageButtonComponent
from services.supabase_service import SpendingsSupabaseDatabase
from icecream import ic

class ForgotPasswordPage(ft.View):

	def __init__(self, page: ft.Page):
		super().__init__(
			route="/forgotpassword",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		)

		self.page = page
		self.supabase_service = SpendingsSupabaseDatabase()

		self.email_input = InputComponent(
			icon = ft.Icons.EMAIL,
			label = "Email",
			password = False
		)

		self.reset_password_button = ButtonComponent(
			text = "Reset password",
			trigger = self.reset_password,
			color = "#8db2dd",
		)

		self.controls = [
			ft.SafeArea(
				content = ft.ResponsiveRow(
					vertical_alignment=ft.CrossAxisAlignment.CENTER,
					alignment=ft.MainAxisAlignment.CENTER,
					controls = [
						ft.Container(
							col = {"xs": 12, "md": 6, "lg": 4},
							content = ft.Card(
								width=360,
								height=814,
								elevation=10,
								content=ft.Container(
									bgcolor="#23262a",
									border_radius=8,
									padding=40,
									# border=ft.border.all(2, ft.Colors.BLACK),
									content=ft.Column(
										horizontal_alignment=ft.CrossAxisAlignment.CENTER,
										alignment=ft.MainAxisAlignment.CENTER,
										spacing = 15,
										controls=[
											ft.Text(f"Please enter your email to reset your password", size=20),
											self.email_input,
											ft.Divider(height=10,color="transparent"),
											self.reset_password_button,
										]
									)
								)
							)
						),
					]
				)
			)
		]

	def reset_password(self, e):
		logger.debug("Reseting password ...")

		try:
			response = self.supabase_service.supabase_client.auth.reset_password_for_email(self.email_input.input_value)
			ic(response)

		except Exception as e:
			raise

	def go_to_login(self, e):
		self.page.go("/login")
