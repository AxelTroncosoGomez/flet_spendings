import os
import uuid
import sys
import sqlite3
import asyncio
import flet as ft
import supabase
from typing import Optional, Union
from datetime import datetime
from dotenv import load_dotenv
from gotrue.errors import AuthApiError
from supabase import create_client, Client, AsyncClient, create_async_client
from postgrest.exceptions import APIError
from supabase._sync.client import SupabaseException

from utils.logger import logger
from utils.config import Config
from services.crud import LocalSpendingsDatabase
from exceptions import (
	GenericException,
	WrongCredentialsException,
	WrongPasswordException,
	UserAlreadyExistsException,
	EmailNotConfirmedException,
	UserNotAllowedException,
	SupabaseApiException,
	EmailNotValidException
)

logger.debug(f"Supabase version: {supabase.__version__}")

load_dotenv()

class SupabaseCouldNotResetPasswordException(Exception):
	...

class SpendingsSupabaseDatabase():

	def __init__(self, supabase_table_name = "spendings"):
		self.user_id: Optional[str] = None
		self.supabase_url: str
		self.supabase_key: str
		self.supabase_client: Optional[Union[AsyncClient, Client]] = None

		self.supabase_table_name = supabase_table_name
		self.verify_redirect_link = "https://axeltroncosogomez.github.io/api/flet_spendings/supabase/verify/"
		self.reset_password_redirect_link = "https://axeltroncosogomez.github.io/api/flet_spendings/supabase/reset_password"

	def sync_client(self):
		self.supabase_url = Config.SUPABASE_URL
		logger.debug(f"Supabase URL: {self.supabase_url}")
		self.supabase_key = Config.SUPABASE_KEY
		logger.debug(f"Supabase ANON KEY: {self.supabase_key}")
		try:
			self.supabase_client: Client = create_client(
				self.supabase_url, 
				self.supabase_key,
			)
		except SupabaseException as err:
			if "Invalid URL" in repr(err):
				raise SupabaseApiException(err)
			else:
				raise GenericException(err)
		except Exception as err:
			logger.error(f"Error while getting client: {repr(err)}")
			raise GenericException(err)
		return self

	async def async_client(self):
		self.supabase_url = Config.SUPABASE_URL
		logger.debug(f"Supabase URL: {self.supabase_url}")
		self.supabase_key = Config.SUPABASE_KEY
		logger.debug(f"Supabase ANON KEY: {self.supabase_key}")
		try:
			self.supabase_client: AsyncClient = await create_async_client(
				self.supabase_url, 
				self.supabase_key,
			)
		except SupabaseException as err:
			if "Invalid URL" in repr(err):
				raise SupabaseApiException(err)
			else:
				raise GenericException(err)
		except Exception as err:
			logger.error(f"Error while getting client: {repr(err)}")
			raise GenericException(err)
		return self

	def set_session(self, access_token, refresh_token):
		response = self.supabase_client.auth.set_session(access_token, refresh_token)
		return response

	async def async_set_session(self, access_token, refresh_token):
		response = await self.supabase_client.auth.set_session(access_token, refresh_token)
		return self

	def get_user(self):
		response = self.supabase_client.auth.get_user()
		return response

	def get_session(self):
		response = self.supabase_client.auth.get_session()
		return response

	def handle_login(self, user_email, user_password):
		try:
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
		except AuthApiError as err:
			if "A user with this email address has already been registered" in repr(err):
				raise UserAlreadyExistsException(err)
			elif "Invalid API key" in repr(err):
				raise SupabaseApiException(err)
			elif "Invalid login credentials" in repr(err):
				raise WrongCredentialsException(err)
			elif "User not allowed" in repr(err):
				raise UserNotAllowedException(err)
			elif "Email not confirmed" in repr(err):
				raise EmailNotConfirmedException(err)	
			else:
				logger.error(f"{type(err).__name__}:{err}")
				raise GenericException(f"{type(err).__name__}:{err}")
		except Exception as err:
			logger.error(f"{type(err).__name__}:{err}")
			raise GenericException(f"{type(err).__name__}:{err}")

	async def async_handle_login(self, user_email, user_password):
		try:
			response = await (
				self.supabase_client
				.auth
				.sign_in_with_password({
					"email": user_email, 
					"password": user_password,
				})
			)
			self.user_id = response.user.id
			return response 
		except AuthApiError as err:
			if "A user with this email address has already been registered" in repr(err):
				raise UserAlreadyExistsException(err)
			elif "Invalid API key" in repr(err):
				raise SupabaseApiException(err)
			elif "Invalid login credentials" in repr(err):
				raise WrongCredentialsException(err)
			elif "User not allowed" in repr(err):
				raise UserNotAllowedException(err)
			elif "Email not confirmed" in repr(err):
				raise EmailNotConfirmedException(err)	
			else:
				logger.error(f"{type(err).__name__}:{err}")
				raise GenericException(f"{type(err).__name__}:{err}")
		except Exception as err:
			logger.error(f"{type(err).__name__}:{err}")
			raise GenericException(f"{type(err).__name__}:{err}")

	def handle_logout(self):
		try:
			self.supabase_client.auth.sign_out()
			self.user_id = None
			logger.debug("Logout sucessfully")
			return
		except Exception as err:
			logger.error(err)

	def handle_registration(self, username, user_email, user_password):
		try:
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
		except AuthApiError as err:
			if "A user with this email address has already been registered" in repr(err):
				raise UserAlreadyExistsException(err)
			elif "Unable to validate email address" in repr(err):
				raise EmailNotValidException(err)
			elif "Invalid API key" in repr(err):
				raise SupabaseApiException(err)
			elif "Invalid login credentials" in repr(err):
				raise WrongCredentialsException(err)
			elif "User not allowed" in repr(err):
				raise UserNotAllowedException(err)
			elif "Email not confirmed" in repr(err):
				raise EmailNotConfirmedException(err)	
			else:
				raise GenericException(err)
		except Exception as err:
			raise GenericException(err)


	def handle_resend_verification(self, email):
		try:
			response = (
				self.supabase_client.auth.resend({
					"type": "signup",
					"email": email,
					"options": {
						"email_redirect_to": self.verify_redirect_link,
					}
				})
			)
			return response
		except AuthApiError as err:
			if "A user with this email address has already been registered" in repr(err):
				raise UserAlreadyExistsException(err)
			elif "Unable to validate email address: invalid format" in repr(err):
				raise EmailNotValidException(err)
			elif "Invalid API key" in repr(err):
				raise SupabaseApiException(err)
			elif "Invalid login credentials" in repr(err):
				raise WrongCredentialsException(err)
			elif "User not allowed" in repr(err):
				raise UserNotAllowedException(err)
			elif "Email not confirmed" in repr(err):
				raise EmailNotConfirmedException(err)	
			else:
				raise GenericException(err)

	def handle_reset_password(self, email):
		try:
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
		except AuthApiError as err:
			if "A user with this email address has already been registered" in repr(err):
				raise UserAlreadyExistsException(err)
			elif "Unable to validate email address: invalid format" in repr(err):
				raise EmailNotValidException(err)
			elif "Invalid API key" in repr(err):
				raise SupabaseApiException(err)
			elif "Invalid login credentials" in repr(err):
				raise WrongCredentialsException(err)
			elif "User not allowed" in repr(err):
				raise UserNotAllowedException(err)
			elif "Email not confirmed" in repr(err):
				raise EmailNotConfirmedException(err)	
			else:
				raise GenericException(err)

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
		else:
			raise UserNotLoggedException("User is not logged")
		return None

	async def async_fetch_all_data(self):
		if self.user_id is not None:
			rows = await (
				self.supabase_client
				.table(self.supabase_table_name)
				.select("*")
				.eq("user_id", self.user_id)
				.execute()
			)
			return rows.data
		else:
			raise UserNotLoggedException("User is not logged")
		return None

	def delete(self, item_id: str):
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
			# .eq("user_id", self.user_id)
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