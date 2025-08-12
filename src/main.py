import os
import uuid
import sys
import sqlite3
import flet as ft
import asyncio
import threading
from typing import Optional
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
from pages.error_page import CrashPage
from pages.dt_page import NewPage
from flet.auth.providers import GitHubOAuthProvider
from utils.logger import logger
import urllib.request
from components.dialogs import (
	sucess_message,
	error_message
)
from exceptions import (
	SupabaseApiException,
	GenericException
)

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

async def init_async_supabase() -> Optional[SpendingsSupabaseDatabase]:
	try:
		db = SpendingsSupabaseDatabase()
		await db.async_client()
		return db
	except GenericException as err:
		logger.error(f"Generic Supabase error: {repr(err)}")
		return None
	except SupabaseApiException as err:
		logger.error("Supabase API error: " + str(err))
		return None
	except Exception as err:
		logger.error(f"Unexpected error: {repr(err)}")
		return None

APP_ASSETS_PATH = os.getenv("FLET_ASSETS_DIR")
logger.debug(APP_ASSETS_PATH)

def main(page: ft.Page):
	page.title = "Spendings"
	page.window.width = 390
	page.window.height = 844
	######### To be able to use transparent background, use ft.WindowDragArea() #########
	# page.window.bgcolor = ft.Colors.TRANSPARENT
	# page.bgcolor = ft.Colors.TRANSPARENT
	# page.window.title_bar_hidden = True
	# page.window.frameless = True
	page.horizontal_alignment = "center"
	page.vertical_alignment = "center"
	page.theme_mode = ft.ThemeMode.DARK
	page.window.prevent_close = True
	page.scroll = ft.ScrollMode.AUTO
	supabase = None
	try:
		supabase = SpendingsSupabaseDatabase()
		supabase.sync_client()
		# supabase = asyncio.run(init_async_supabase())
	except GenericException as err:
		error_message = repr(err)
	except SupabaseApiException as err:
		error_message = "Unable to connect to Supabase"
		logger.debug("Something wrong happend on server ...")
	except Exception as err:
		error_message = repr(err)

	if supabase is None:
		page.views.clear()
		# Show error screen and exit early
		page.views.append(CrashPage(page, error_message))
		page.go("/error")
		return
	
	# new_page = NewPage(page)
	login_page = LoginPage(page, supabase)
	register_page = RegisterPage(page, supabase)
	verify_page = VerifyEmailPage(page, supabase)
	forgot_password_page = ForgotPasswordPage(page, supabase)

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
			page.views.append(login_page)
		elif page.route == "/spendings":
			# spendings_page = SpendingsPage(page, supabase)
			# asyncio.run(spendings_page.init_user())
			# threading.Thread(
			# 	target = asyncio.run(spendings_page.init_user())
			# ).start()
			page.views.append(SpendingsPage(page, supabase))
		elif page.route == "/register":
			page.views.append(register_page)
		elif page.route == "/verify":
			page.views.append(verify_page)
		elif page.route == "/forgotpassword":
			page.views.append(forgot_password_page)
		# elif page.route == "/new":
		# 	page.views.append(new_page)
		page.update()

	page.window.on_event = window_event
	page.on_route_change = route_change
	page.go("/login")
	# page.go("/new")

ft.app(
	target=main,
)