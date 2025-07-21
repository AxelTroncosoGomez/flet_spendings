import os
import uuid
import sys
import sqlite3
from utils.logger import logger
from datetime import datetime

class LocalSpendingsDatabase():	
	APP_DATA_PATH = os.getenv("FLET_APP_STORAGE_DATA")
	APP_TEMP_PATH = os.getenv("FLET_APP_STORAGE_TEMP")
	
	def __init__(self, db, user):
		self.db = db
		self.user = user
		self.conn = None
		self.db_path = os.path.join(self.APP_DATA_PATH, self.db)
		self._database_name = "spendings"
		logger.debug(f"Database {self.db} on path {self.db_path}")

	def create_or_open(self):
		try:
			self.connect()
		except:
			logger.debug(f"Database {self._database_name} already connected")
		self.pencil.execute(f'''
			CREATE TABLE IF NOT EXISTS {self._database_name}(
			item_id TEXT PRIMARY KEY,
			user_id TEXT NOT NULL,
			date TEXT NOT NULL,
			store TEXT NOT NULL,
			product TEXT NOT NULL,
			amount INTEGER NOT NULL,
			price FLOAT NOT NULL
		)''')
		self.conn.commit()
		logger.debug(f"Database {self._database_name} created on {self.db_path}")

	def connect(self):
		self.conn = sqlite3.connect(self.db_path)
		self.pencil = self.conn.cursor()

	def __reset(self):
		try:
			# Delete all rows from the table
			self.pencil.execute(f"DELETE FROM {self._database_name}")
			self.conn.commit()
		except Exception as e:
			logger.debug(f"Failed to reset database: {e}")

	def custom_query_execution(self, query):
		self.pencil.execute(query)
		self.conn.commit()
		
	def custom_fetch_execution(self, query):
		self.pencil.execute(query)
		records = self.pencil.fetchall()
		return records
	
	def delete_row_by_id(self, item_id):
		query = f"""DELETE FROM {self._database_name} WHERE item_id = ? AND user_id = ?"""
		self.pencil.execute(query, (item_id, self.user))
		self.conn.commit()
	
	def delete_rows_by_ids(self, ids):
		placeholders = ', '.join(['?'] * len(ids))
		query = f"""DELETE FROM {self._database_name} WHERE item_id IN ({placeholders})"""
		self.pencil.execute(query, ids)
		self.conn.commit()

	def update(self, item_id, new_values):
		query = f"""
		UPDATE {self._database_name} 
		SET date = ?, store = ?, product = ?, amount = ?, price = ?
		WHERE item_id = ? AND user_id = ?
		"""
		try:
			self.pencil.execute(query, (*new_values, item_id, self.user))
			self.conn.commit()
		except Exception as e:
			logger.debug(f"Failed to update database: \n{e}")
		
	def get_id_from_row(self, row):
		query = f"""
		SELECT item_id 
		FROM {self._database_name} 
		WHERE date = ? AND store = ? AND product = ? AND amount = ? AND price = ? AND user_id = ?
		"""
		self.pencil.execute(query, row)
		result = self.pencil.fetchone()
		return result[0] if result else None

	def insert(self, row):
		# try:
		self.pencil.execute(f'INSERT INTO {self._database_name} (item_id, user_id, date, store, product, amount, price) VALUES(?, ?, ?, ?, ?, ?, ?)', row)
		self.conn.commit()
		logger.info(f"Row {row} successfully added into {self._database_name}")
		# except Exception as e:
		# 	logger.error(f"Something wrong happend: {str(e)}")

	def select_all_data(self, exclude_id: bool = False):
		self.pencil.execute(f"""SELECT * FROM {self._database_name} WHERE user_id = ?""", (self.user,))
		records = self.pencil.fetchall()
		if exclude_id:
			records = [record[1:] for record in records]
			return records
		return records

	def select_data_from_date(self, date = datetime.now().date().strftime("%d/%m/%Y"), exclude_id: bool = False):
		self.pencil.execute(f"""SELECT * FROM {self._database_name} WHERE date = ? AND user_id = ?""", (date, self.user))
		records = self.pencil.fetchall()
		# Exclude the first 2 values of each tuple
		if exclude_id:
			records = [record[2:] for record in records]
			return records
		return records

	def close(self):
		if self.conn:
			self.conn.close()