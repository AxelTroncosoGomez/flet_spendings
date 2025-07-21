import flet as ft
from utils.logger import logger
from components.inputs import InputComponent
from components.buttons import ButtonComponent, ImageButtonComponent
from services.supabase_service import SpendingsSupabaseDatabase
from icecream import ic

class LoginPage(ft.View):

	def __init__(self, page: ft.Page):
		super().__init__(
			route="/login",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		)

		self.page = page
		self.supabase_service = SpendingsSupabaseDatabase()

		self.email_input = InputComponent(
			icon = ft.Icons.EMAIL,
			label = "Email",
			# value = "admin",
			password = False
		)

		self.password_input = InputComponent(
			icon = ft.Icons.LOCK,
			label = "Password",
			# value = "admin",
			password = True
		)

		self.login_btn = ButtonComponent(
			text = "Continue",
			trigger = self.handle_user_login,
			color = "#8db2dd"
		)

		self.google_login_btn = ImageButtonComponent(
			color = "white",
			text = "Continue with Google",
			src_image = "google_logo.svg",
			trigger = self.handle_google_login
		)

		self.linkedin_login_btn = ImageButtonComponent(
			color = "white",
			text = "Continue with Linkedin",
			src_image = "linkedin_logo.svg",
			trigger = self.handle_linkedin_login
		)

		self.microsoft_login_btn = ImageButtonComponent(
			color = "white",
			text = "Continue with Microsoft",
			src_image = "microsoft_logo.svg",
			trigger = self.handle_microsoft_login
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
										spacing = 10,
										controls=[
										    ft.Image(
										        src="dummy_logo_light.png",
										        width=150,
										    ),
											ft.Text("Welcome to DummyDev", size=20),
											ft.Divider(height = 10,color="transparent"),
											self.email_input,
											self.password_input,
											ft.Container(
												content = ft.Row([
													ft.Text(
														spans=[
															ft.TextSpan(
																"Forgot password?",
																style=ft.TextStyle(
																	color="#8db2dd",
																),
																on_click=self.go_to_forgot_password,
															)
														]
													)
												], 
												alignment = ft.MainAxisAlignment.END
												),
											),
											self.login_btn,
											ft.Text(
												spans=[
													ft.TextSpan("Don't have an account? "),
													ft.TextSpan(
														"Sign up",
														style=ft.TextStyle(
															color="#8db2dd",
															# decoration=ft.TextDecoration.UNDERLINE,
														),
														on_click=self.go_to_sign_up,
													),
												]
											),
											ft.Divider(height=5,color="transparent"),
											ft.Divider(height=9, thickness=2),
											ft.Divider(height=5,color="transparent"),
											ft.Text("Or sign up using", size=13),
											self.google_login_btn,
											self.microsoft_login_btn,
											self.linkedin_login_btn,
										]
									)
								)
							)
						),
					]
				)
			)
		]

	def handle_user_login(self, e):
		logger.debug("Logged successfully!!!")
		logger.debug(f"Username: {self.email_input.input_value}")
		logger.debug(f"Password: {self.password_input.input_value}")

		try:
			response = self.supabase_service.handle_login(
				user_email = self.email_input.input_value, 
				user_password = self.password_input.input_value
			)
			ic(response)
			self.page.session.set("current_user_id", response.user.id)
			logger.debug(f"Login with ID: {response.user.id}")

		except Exception as err:
			logger.error(f"Error during registration: {err}")
			self.page.snack_bar = ft.SnackBar(ft.Text("Login failed. Try again."))
			self.page.snack_bar.open = True
			self.page.update()

	def go_to_sign_up(self, e):
		logger.debug("Sign up!")
		self.page.go("/register")

	def go_to_forgot_password(self, e):
		logger.debug("Going to Forgot Password Page ...")
		self.page.go("/forgotpassword")

	def handle_google_login(self, e):
		logger.debug("Login with Google")

	def handle_linkedin_login(self, e):
		logger.debug("Login with Linkedin")

	def handle_microsoft_login(self, e):
		logger.debug("Login with Microsoft")