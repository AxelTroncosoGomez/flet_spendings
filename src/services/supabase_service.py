import os
import uuid
import sys
import sqlite3
import flet as ft
from typing import Optional
from datetime import datetime
from utils.logger import logger
from dotenv import load_dotenv
from supabase import create_client, Client
from services.crud import LocalSpendingsDatabase

load_dotenv()

class SupabaseCouldNotResetPasswordException(Exception):
	...

class SpendingsSupabaseDatabase():

	def __init__(self, supabase_table_name = "spendings"):
		self.user_id: Optional[str] = None
		self.supabase_key: Optional[str] = None
		self.supabase_url: Optional[str] = None
		self.supabase_client: Optional[Client] = None

		self.supabase_table_name = supabase_table_name
		self.verify_redirect_link = "https://axeltroncosogomez.github.io/api/flet_spendings/supabase/verify/"
		self.reset_password_redirect_link = "https://axeltroncosogomez.github.io/api/flet_spendings/supabase/reset_password"

		self.__get_credentials()
		self.__get_client()

	def __get_credentials(self):
		self.supabase_url = os.environ.get("SUPABASE_URL")
		self.supabase_key = os.environ.get("SUPABASE_KEY")

	def __get_client(self):
		try:
			self.supabase_client: Client = create_client(self.supabase_url, self.supabase_key)
		except Exception as e:
			logger.error(f"Error while getting client: {repr(e)}")

	def handle_login(self, user_email, user_password):
		response = (
			self.supabase_client
			.auth
			.sign_in_with_password({
				"email": user_email, 
				"password": user_password,
			})
		)
		self.user_id = response.user.id
		return response

	def handle_logout(self):
		self.user_id = None
		response = (
			self.supabase_client
			.auth
			.sign_out()
		)
		return response

	def handle_registration(self, username, user_email, user_password):
		response = (
			self.supabase_client
			.auth
			.sign_up({
				"email": user_email,
				"password": user_password,
				"options": {
					"email_redirect_to": self.verify_redirect_link,
					"data": {
						"username": username,
					}
				}
			})
		)
		return response

	def handle_reset_password(self, email):
		response = (
			self.supabase_client
			.auth
			.reset_password_for_email(
				email,
				{
					"redirect_to": self.reset_password_redirect_link
				}
			)
		)
		return response

	def fetch_all_data(self):
		if self.user_id is not None:
			rows = (
				self.supabase_client
				.table(self.supabase_table_name)
				.select("*")
				.eq("user_id", self.user_id)
				.execute()
			)
			return rows.data
		return None

	def delete_row_by_id(self, item_id: str):
		response = (
			self.supabase_client
			.table(self.supabase_table_name)
			.delete()
			.eq("item_id", item_id)
			.execute()
		)

		return response

	def update(self, item_id: str, update_value: dict):
		response = (
			self.supabase_client
			.table(self.supabase_table_name)
			.update(update_value)
			.eq("item_id", item_id)
			.execute()
		)
		return response

	def insert(self, new_value: dict):
		response = (
			self.supabase_client
			.table(self.supabase_table_name)
			.insert(new_value)
			.execute()
		)
		return response