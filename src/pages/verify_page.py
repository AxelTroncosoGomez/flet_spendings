import jwt
import flet as ft
import flet_webview as fwv
from utils.logger import logger
from components.inputs import InputComponent
from components.buttons import ButtonComponent, ImageButtonComponent
from services.supabase_service import SpendingsSupabaseDatabase
from icecream import ic

class VerifyEmailPage(ft.View):

	def __init__(self, page: ft.Page):
		super().__init__(
			route="/verify",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		)

		self.page = page
		self.supabase_service = SpendingsSupabaseDatabase()

		# self.current_register_email = self.page.session.get("current_register_email")
		# self.current_register_username = self.page.session.get("current_register_username")
		# self.current_register_password = self.page.session.get("current_register_password")
		# self.current_register_user_id = self.page.session.get("current_register_user_id")

		# self.webview = fwv.WebView(
		# 	url="https://axeltroncosogomez.github.io/verify",
		# 	expand=True,
		# 	on_page_started=self._handle_token_from_url
		# )

		self.resend_email_button = ButtonComponent(
			text = "Resend verification email",
			trigger = self.resend_verification,
			color = "#8db2dd",
		)

		self.email_verifying_text = """
Welcome to DummyDev, we sent you and email to verify your account. 
Please check your inbox to be able to Log-in in our App.
If you don't receive any email, you can resend another one by clickin the button below
"""

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
											# ft.Text(f"{self.current_register_user_id}", size=18),
											ft.Text(self.email_verifying_text, size=15),
											ft.Divider(height=10,color="transparent"),
											self.resend_email_button,
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

	# def _handle_token_from_url(self, e):
	# 	logger.debug("Calling _handle_token_from_url() ...")
	# 	if "#access_token=" in e.url:
	# 		try:
	# 			token = e.url.split("#access_token=")[1].split("&")[0]
	# 			logger.debug(f"token: {token}")

	# 			# Optionally decode token (you can use PyJWT for this)
	# 			decoded = jwt.decode(token, options={"verify_signature": False})
	# 			logger.info(f"User email verified: {decoded['email']}")

	# 			# Save token or mark session
	# 			self.page.session.set("email_verify_access_token", token)
	# 			self.page.email_verify_snack_bar = ft.SnackBar(ft.Text("✅ Email verified."))
	# 			self.page.email_verify_snack_bar.open = True

	# 			# Redirect to login
	# 			self.page.go("/login")

	# 		except Exception as err:
	# 			logger.error(f"Invalid token: {err}")
	# 			self.page.invalid_token_snack_bar = ft.SnackBar(ft.Text("❌ Invalid token."))
	# 			self.page.invalid_token_snack_bar.open = True
	# 			self.page.go("/register")

	# 	self.page.update()

	# def did_mount(self):
	# 	logger.debug("Starting timer ...")
	# 	self.timer.start()

	# def check_verification(self, e):
	# 	# session = self.supabase_service.supabase_client.auth.get_session()
	# 	# if session.user.email_confirmed_at:
	# 	#     self.page.go("/login")
	# 	logger.debug("Dummy callback")

	def resend_verification(self, e):
		logger.debug("resending email...")

		try:
			response = self.supabase_service.supabase_client.auth.resend({
				"type": "signup",
				"email": self.current_register_email,
				"options": {
					"email_redirect_to": "https://axeltroncosogomez.github.io/api/flet_spendings/supabase/verify/"
				}
			})
			ic(response)

		except Exception as e:
			raise

	def go_to_login(self, e):
		self.page.go("/login")
