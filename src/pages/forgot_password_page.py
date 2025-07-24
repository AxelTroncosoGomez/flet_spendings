import flet as ft
from utils.logger import logger
from components.inputs import InputComponent
from components.buttons import ButtonComponent, ImageButtonComponent
from services.supabase_service import SpendingsSupabaseDatabase
from icecream import ic
from exceptions import (
	GenericException,
	WrongCredentialsException,
	WrongPasswordException,
	UserAlreadyExistsException,
	EmailNotConfirmedException,
	UserNotAllowedException,
	SupabaseApiException,
	PasswordNotEqualException,
	InputNotFilledException,
	EmailNotValidException
)
from components.dialogs import (
	sucess_message,
	error_message
)

class ForgotPasswordPage(ft.View):

	def __init__(self, page: ft.Page, supabase_service):
		super().__init__(
			route="/forgotpassword",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			scroll=ft.ScrollMode.AUTO
		)

		self.page = page
		self.supabase_service = supabase_service

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
											ft.Container(
												content = ft.Row([
													ft.Text(
														spans=[
															ft.TextSpan(
																"← Back to login",
																style=ft.TextStyle(
																	color="#8db2dd",
																	size=15,
																),
																on_click=self.go_to_login
															)
														]
													)
												], 
												alignment = ft.MainAxisAlignment.CENTER
												),
											),
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

		email = self.email_input.input_value

		try:
			if len(email) == 0:
				raise InputNotFilledException("Please provide an email")

			response = self.supabase_service.handle_reset_password(
				email
			)
			ic(response)

			self.page.open(sucess_message("An email was send to you to change your password."))
			self.page.update()

		except InputNotFilledException as err:
			self.page.open(error_message(err))
		except EmailNotValidException as err:
			# logger.error(type(err).__name__)
			# logger.error(err)
			self.page.open(error_message("Invalid email format"))
		except GenericException as err:
			self.page.open(error_message(err))
		except Exception as err:
			self.page.open(error_message(err))

	def go_to_login(self, e):
		self.page.go("/login")
