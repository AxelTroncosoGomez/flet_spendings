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

class SpendingsSupabaseDatabase():

	def __init__(self):
		self.user_id: str
		self.supabase_key: Optional[str] = None
		self.supabase_url: Optional[str] = None
		self.supabase_client: Optional[Client] = None

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
		response = self.supabase_client.auth.sign_in_with_password({
			"email": user_email, 
			"password": user_password,
		})
		logger.debug("Response ...")
		logger.debug(response)
		self.user_id = response.user.id
		logger.debug(f"Welcome user {self.user_id}")


	def handle_registration(self, user_email, user_password):
		...


	def fetch_all_data(self):
		rows = self.supabase_client.table("spendings").select("*").eq("user_id", self.user_id).execute()
		logger.debug("Current spendings for this user:")
		logger.debug(rows.data)


	def insert(self, new_spending):
		inserted = self.supabase_client.table("spendings").insert(new_spending).execute()
		logger.debug("Inserted new spending row:")
		logger.debug(inserted.data)


	def handle_logout(self):
		...