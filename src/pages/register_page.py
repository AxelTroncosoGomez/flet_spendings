import jwt
import flet as ft
import webbrowser
from utils.logger import logger
from components.inputs import InputComponent
from components.buttons import ButtonComponent, ImageButtonComponent
from services.supabase_service import SpendingsSupabaseDatabase
from icecream import ic

class RegisterPage(ft.View):

	def __init__(self, page: ft.Page):
		super().__init__(
			route="/register",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		)

		self.supabase_service = SpendingsSupabaseDatabase()
		self.page = page

		self.email_input = InputComponent(
			icon = ft.Icons.EMAIL,
			label = "Email",
			password = False
		)

		self.username_input = InputComponent(
			icon = ft.Icons.PERSON_ROUNDED,
			label = "Username",
			password = False
		)

		self.password_input = InputComponent(
			icon = ft.Icons.LOCK,
			label = "Repeat Password",
			password = True
		)

		self.repeat_password_input = InputComponent(
			icon = ft.Icons.LOCK,
			label = "Password",
			password = True
		)

		self.register_button = ButtonComponent(
			text = "Register",
			trigger = self.handle_user_register,
			color = "#8db2dd",
		)

		self.accept_services_checkbox = ft.Checkbox(label="Accept out terms and services")

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
											ft.Text("Create an account", size=20),
											ft.Divider(height=10,color="transparent"),
											self.email_input,
											self.username_input,
											self.password_input,
											self.repeat_password_input,
											ft.Divider(height=15,color="transparent"),
											self.register_button,
											ft.Text(
												spans=[
													ft.TextSpan("Already have an account? "),
													ft.TextSpan(
														"Log in",
														style=ft.TextStyle(
															color="#8db2dd",
															# decoration=ft.TextDecoration.UNDERLINE,
														),
														on_click=self.go_to_login,
													),
												]
											),
											ft.Divider(height=10,color="transparent"),
											# self.accept_services_checkbox,
										]
									)
								)
							)
						),
					]
				)
			)
		]

	def handle_user_register(self, e):
		logger.debug("Register a user !!!")

		email = self.email_input.input_value
		username = self.username_input.input_value
		password = self.password_input.input_value

		self.page.session.set("current_register_email", email)
		self.page.session.set("current_register_username", username)
		self.page.session.set("current_register_password", password)

		self.page.launch_url("https://yourusername.github.io/forgot", web_popup_window=True)

		# try:
		# 	response = self.supabase_service.supabase_client.auth.sign_up({
		# 		"email": email,
		# 		"password": password,
		# 		"options": {
		# 			"email_redirect_to": "https://axeltroncosogomez.github.io/verify",
		# 			"data": {
		# 				"username": username,
		# 				"verified": False
		# 			}
		# 		}
		# 	})

		# 	user_id = response.user.id
		# 	self.page.session.set("current_register_user_id", user_id)

		# 	# Step 1: Prompt user to check their email
		# 	self.page.snack_bar = ft.SnackBar(ft.Text("Check your email to verify account."))
		# 	self.page.snack_bar.open = True
		# 	self.page.update()

		# 	# Step 2: Open verification page in browser
		# 	# webbrowser.open("https://axeltroncosogomez.github.io/verify")

		# 	# Step 3: Go to a verification waiting page inside app
		# 	# self.page.go("/verify")

		# except Exception as e:
		# 	logger.error(f"Error during registration: {e}")
		# 	self.page.snack_bar = ft.SnackBar(ft.Text("Registration failed. Try again."))
		# 	self.page.snack_bar.open = True
		# 	self.page.update()




	def check_username_already_in_use(self):
		...

	def check_both_password_equal(self):
		...

	def go_to_login(self, e):
		logger.debug("Sign up!")
		self.page.go("/login")

	# def go_to_forgot_password(self, e):
	# 	logger.debug("Going to Forgot Password Page ...")