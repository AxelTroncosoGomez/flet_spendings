import flet as ft
from icecream import ic
from utils.logger import logger
from components.inputs import InputComponent
from components.buttons import ButtonComponent, ImageButtonComponent
from services.supabase_service import SpendingsSupabaseDatabase
from exceptions import (
	GenericException,
	WrongCredentialsException,
	WrongPasswordException,
	UserAlreadyExistsException,
	EmailNotConfirmedException,
	UserNotAllowedException,
	SupabaseApiException,
	EmailNotValidException,
	InvalidCredentialsException
)
from components.dialogs import (
	sucess_message,
	error_message
)

class LoginPage(ft.View):

	def __init__(self, page: ft.Page, supabase_service):
		super().__init__(
			route="/login",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			scroll=ft.ScrollMode.AUTO
		)

		self.page = page
		self.supabase_service = supabase_service

		self.email_input = InputComponent(
			icon = ft.Icons.EMAIL,
			label = "Email",
			password = False,
		)

		self.password_input = InputComponent(
			icon = ft.Icons.LOCK,
			label = "Password",
			password = True
		)

		self.login_btn = ButtonComponent(
			text = "Continue",
			trigger = self.handle_user_login,
			color = "#8db2dd",
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

		self.keep_logged_checkbox = ft.Checkbox(
			label="Remember me",
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
											ft.Divider(height = 10, color="transparent"),
											self.email_input,
											self.password_input,
											ft.Container(
												padding = 0,
												margin = 0,												
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
											ft.Container(
												padding = 0,
												margin = 0,												
												content = ft.Row([
													self.keep_logged_checkbox
												], 
												alignment = ft.MainAxisAlignment.START
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
		logger.debug(f"Username: {self.email_input.input_value}")
		logger.debug(f"Password: {self.password_input.input_value}")

		if self.keep_logged_checkbox.value:
			logger.debug("Session will be remembered ...")

		try:
			response = self.supabase_service.handle_login(
				user_email = self.email_input.input_value, 
				user_password = self.password_input.input_value
			)
			ic(response)
			self.page.session.set("current_user_id", response.user.id)
			logger.debug(f"Login with ID: {response.user.id}")

			self.page.session.set("user_access_token", response.session.access_token)
			self.page.session.set("user_refresh_token", response.session.refresh_token)

			self.page.open(sucess_message("Login Sucessfull!", page=self.page))

			self.page.go("/spendings")
			
			self.clear_input_entries()

		except SupabaseApiException as err:
			self.page.open(error_message("Unable to connect to server", page=self.page))
		except WrongCredentialsException as err:
			self.page.open(error_message("Wrong credentials", page=self.page))
		except WrongPasswordException as err:
			self.page.open(error_message("Wrong email or password", page=self.page))
		except EmailNotConfirmedException as err:
			self.page.open(error_message("User email not confirmed", page=self.page))
		except UserNotAllowedException as err:
			self.page.open(error_message("User not allowed", page=self.page))
		except GenericException as err:
			self.page.open(error_message(f"{type(err).__name__}:{err}", page=self.page))
		except InvalidCredentialsException as err:
			self.page.open(error_message("Please provide the email and password", page=self.page))
		except Exception as err:
			self.page.open(error_message(f"{type(err).__name__}:{err}", page=self.page))

	async def async_handle_user_login(self, e):
		logger.debug(f"Username: {self.email_input.input_value}")
		logger.debug(f"Password: {self.password_input.input_value}")

		try:
			response = await self.supabase_service.handle_login(
				user_email = self.email_input.input_value, 
				user_password = self.password_input.input_value
			)
			ic(response)
			self.page.session.set("current_user_id", response.user.id)
			logger.debug(f"Login with ID: {response.user.id}")

			self.page.session.set("user_access_token", response.session.access_token)
			self.page.session.set("user_refresh_token", response.session.refresh_token)

			self.page.open(sucess_message("Login Sucessfull!", page=self.page))

			self.page.go("/spendings")
			
			self.clear_input_entries()

		except SupabaseApiException as err:
			self.page.open(error_message("Unable to connect to server", page=self.page))
		except WrongCredentialsException as err:
			self.page.open(error_message("Wrong credentials", page=self.page))
		except WrongPasswordException as err:
			self.page.open(error_message("Wrong email or password", page=self.page))
		except EmailNotConfirmedException as err:
			self.page.open(error_message("User email not confirmed", page=self.page))
		except UserNotAllowedException as err:
			self.page.open(error_message("User not allowed", page=self.page))
		except GenericException as err:
			self.page.open(error_message(f"{type(err).__name__}:{err}", page=self.page))
		except Exception as err:
			self.page.open(error_message(f"{type(err).__name__}:{err}", page=self.page))

	def go_to_sign_up(self, e):
		logger.debug("Sign up!")
		self.page.go("/register")

	def go_to_forgot_password(self, e):
		logger.debug("Going to Forgot Password Page ...")
		self.page.go("/forgotpassword")

	def handle_google_login(self, e):
		logger.debug("Login with Google")
		self.page.open(
			sucess_message(
				"Sucessfully logged to Google",
				3000,
				page=self.page
			)
		)
		self.password_input.set_error("Wrong password")
		self.page.update()

	def handle_linkedin_login(self, e):
		logger.debug("Login with Linkedin")
		self.page.open(
			sucess_message(
				"Sucessfully logged to Linkedin",
				3000,
				page=self.page
			)
		)

	def handle_microsoft_login(self, e):
		logger.debug("Login with Microsoft")
		self.page.open(
			sucess_message(
				"Sucessfully logged to Microsoft",
				3000,
				page=self.page
			)
		)

	def clear_input_entries(self):
		self.email_input.set_value("")
		self.password_input.set_value("")
