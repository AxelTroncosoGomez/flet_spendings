import re
import jwt
import socket
import smtplib
import flet as ft
import webbrowser
from typing import Tuple
from utils.logger import logger
from gotrue.errors import AuthApiError
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

class RegisterPage(ft.View):

	def __init__(self, page: ft.Page, supabase_service):
		super().__init__(
			route="/register",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			scroll=ft.ScrollMode.AUTO
		)

		self.page = page
		self.supabase_service = supabase_service

		# TODO: Add shake when error happend on email field
		self.email_input = InputComponent(
			icon = ft.Icons.EMAIL,
			label = "Email",
			password = False,
			validator = self.check_correct_email
		)

		self.username_input = InputComponent(
			icon = ft.Icons.PERSON_ROUNDED,
			label = "Username",
			password = False
		)

		self.password_input = InputComponent(
			icon = ft.Icons.LOCK,
			label = "Password",
			password = True
		)

		self.repeat_password_input = InputComponent(
			icon = ft.Icons.LOCK_OUTLINED,
			label = "Repeat Password",
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
											ft.Image(
												src="dummy_logo_light.png",
												width=150,
											),										
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

		# self.page.session.set("current_register_email", email)
		# self.page.session.set("current_register_username", username)
		# self.page.session.set("current_register_password", password)

		email = self.email_input.input_value
		username = self.username_input.input_value
		password = self.password_input.input_value
		repeat_password = self.repeat_password_input.input_value

		logger.debug(f"User email: {email}")
		logger.debug(f"User username: {username}")
		logger.debug(f"User password: {password}")

		# self.page.launch_url("https://yourusername.github.io/forgot", web_popup_window=True)
		try:
			if (
				email == ""
				or username == ""
				or password == ""
				or repeat_password == ""
			):
				raise InputNotFilledException("Please fill all the fields")

			if password != repeat_password:
				raise PasswordNotEqualException("Both password does not match")

			response = self.supabase_service.handle_registration(
				username = username,
				user_email = email,
				user_password = password
			)

			if len(response.user.identities) == 0:
				raise UserAlreadyExistsException("Email is already in use")

			ic(response)
			# ic(response.user.identities)
			# ic(response.session)

			self.page.open(sucess_message("Registration Sucessfully!"))

			# webbrowser.open("https://axeltroncosogomez.github.io/verify")
			self.page.go("/verify")

			self.clear_input_entries()

		except UserAlreadyExistsException as err:
			self.page.open(error_message("Email is already in use"))
		except InputNotFilledException as err:
			self.page.open(error_message(err))
		except PasswordNotEqualException as err:
			self.page.open(error_message(err))
		except SupabaseApiException as err:
			self.page.open(error_message("Unable to connect to server"))
		except WrongCredentialsException as err:
			self.page.open(error_message("Wrong credentials"))
		except EmailNotConfirmedException as err:
			self.page.open(error_message("User email not confirmed"))
		except UserNotAllowedException as err:
			self.page.open(error_message("User not allowed"))
		except GenericException as err:
			self.page.open(error_message(err))
		except Exception as err:
			self.page.open(error_message(err))

	@staticmethod
	def check_correct_email(value: str) -> Tuple[bool, str]:
		if len(value) == 0:
			return (True, "")
		email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
		match = re.fullmatch(email_pattern, value)
		logger.debug(re.fullmatch(email_pattern, value))
		if match is None:
			return (False, "Invalid email format")
		if len(value) < 20:
			return (False, "Email must be at least 20 characters long")
		return (True, "")

	def smtp_ping(email: str, timeout: int = 5) -> Tuple[bool, str]:
	    """Verify if mailbox exists via SMTP ping (without sending email)"""
	    if not validate_email_format(email):
	        return False, "Invalid email format"
	    
	    domain = email.split('@')[1]
	    
	    try:
	        # Get MX records
	        records = socket.getaddrinfo(domain, None, socket.AF_INET)
	        mx_servers = [r[4][0] for r in records]
	        
	        if not mx_servers:
	            return False, "No MX records found"
	        
	        # Try each MX server
	        for mx in mx_servers[:3]:  # Limit to 3 servers
	            try:
	                with smtplib.SMTP(mx, timeout=timeout) as server:
	                    server.helo('example.com')
	                    server.mail('test@example.com')
	                    code, _ = server.rcpt(email)
	                    if code == 250:
	                        return True, "Mailbox exists"
	            except (smtplib.SMTPException, socket.timeout, ConnectionError):
	                continue
	                
	        return False, "Mailbox verification failed"
	    except Exception as e:
	        return False, f"SMTP error: {str(e)}"

	def go_to_login(self, e):
		self.page.go("/login")

	def clear_input_entries(self):
		self.email_input.set_value("")
		self.username_input.set_value("")
		self.password_input.set_value("")
		self.repeat_password_input.set_value("")