import os
import uuid
import sys
import sqlite3
import flet as ft
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from services.crud import LocalSpendingsDatabase
from services.supabase_service import SpendingsSupabaseDatabase
from pages.login_page import LoginPage  
from pages.register_page import RegisterPage  
from pages.spendings_page import SpendingsPage
from pages.verify_page import VerifyEmailPage
from pages.forgot_password_page import ForgotPasswordPage
from flet.auth.providers import GitHubOAuthProvider
from utils.logger import logger
import urllib.request

load_dotenv()

# uv export --no-hashes --no-annotate --format requirements.txt > requirements.txt

# Password from Supabase proj
# gCATA6eaPyZs#rEKQ8^WhERQ3zUxGnTeZ61w42PZ

# xs < 576px
# sm ≥ 576px
# md ≥ 768px
# lg ≥ 992px
# xl ≥ 1200px
# xxl ≥ 1400px

# {"xs": 8,"sm": 8, "md": 8, "lg": 8, "xl": 8, "xxl": 8}

# iPhone 13	               390	844
# Samsung Galaxy A53	   393	873
# Samsung Galaxy Tab A9	   800	1340
# Full HD Desktop Browser  1920	1080

APP_ASSETS_PATH = os.getenv("FLET_ASSETS_DIR")
logger.debug(APP_ASSETS_PATH)

def main(page: ft.Page):

	def window_event(e):
		if e.data == "close":
			page.open(confirm_dialog)
			page.update()

	def yes_click(e):
		page.window.destroy()

	def no_click(e):
		page.close(confirm_dialog)
		page.update()

	confirm_dialog = ft.AlertDialog(
		modal=True,
		title=ft.Text("Please confirm"),
		content=ft.Text("Do you really want to exit this app?"),
		actions=[
			ft.ElevatedButton("Yes", on_click=yes_click),
			ft.OutlinedButton("No", on_click=no_click),
		],
		actions_alignment=ft.MainAxisAlignment.END,
	)

	def route_change(e):
		page.views.clear()
		if page.route == "/login":
			login_page = LoginPage(page)
			page.views.append(login_page)
		elif page.route == "/spendings":
			spendings_page = SpendingsPage(page)
			page.views.append(spendings_page)
		elif page.route == "/register":
			spendings_page = RegisterPage(page)
			page.views.append(spendings_page)
		elif page.route == "/verify":
			verify_page = VerifyEmailPage(page)
			page.views.append(verify_page)
		elif page.route == "/forgotpassword":
			forgot_password_page = ForgotPasswordPage(page)
			page.views.append(forgot_password_page)
		page.update()

	page.title = "To-Do App"
	page.window.width = 390
	page.window.height = 844
	page.horizontal_alignment = "center"
	page.vertical_alignment = "center"
	page.theme_mode = ft.ThemeMode.DARK
	page.window.prevent_close = True
	page.window.on_event = window_event
	page.scroll = "auto"
	page.on_route_change = route_change
	page.go("/login")

ft.app(
	target=main,
)