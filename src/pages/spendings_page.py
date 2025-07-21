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
from components.inputs import InputComponent
from components.buttons import ButtonComponent, ImageButtonComponent
from utils.logger import logger
import urllib.request

class SpendingsPage(ft.View):
	def __init__(self, page: ft.Page):
		super().__init__(
			route="/spendings",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		)
		self.page = page
		self.user_id = self.page.session.get("user_id")
		logger.debug(f"User ID: {self.user_id}")

		self.database = LocalSpendingsDatabase("spendings.db", self.user_id)
		self.database.connect()
		self.database.create_or_open()

		self.input_date = InputComponent(
			icon = ft.Icons.CALENDAR_MONTH,
			label = "Date",
			value = datetime.now().date().strftime("%d-%m-%Y"),
		)
		self.input_store = InputComponent(
			icon=ft.Icons.STORE,
			label="Store",
		)
		self.input_product = InputComponent(
			icon=ft.Icons.LOCAL_GROCERY_STORE,
			label="Product",
		)
		self.input_amount = InputComponent(
			icon=ft.Icons.NUMBERS,
			label="Amount",
		)
		self.input_price = InputComponent(
			icon=ft.Icons.PRICE_CHANGE,
			label="Price",
		)

		self.table_view = ft.DataTable(
			columns=[
				ft.DataColumn(ft.Text("Date")),
				ft.DataColumn(ft.Text("Store")),
				ft.DataColumn(ft.Text("Product")),
				ft.DataColumn(ft.Text("Amount")),
				ft.DataColumn(ft.Text("Price")),
			],
			rows=[],
			border_radius=10,
			heading_row_color=ft.Colors.BLACK12,
			data_row_color={"hovered": "0x30FF0000"},
			divider_thickness=0,
			show_bottom_border=True,
		)

		# Create dialog (moved before table_view since it's referenced in open_new_entry_dialog)
		self.dlg_modal = ft.AlertDialog(
			modal=True,
			title=ft.Text("Add New Entry"),
			content=ft.Container(
				content=ft.Column(
					controls=[
						self.input_date,
						self.input_store,
						self.input_product,
						self.input_amount,
						self.input_price,
					],
					tight=True,  # Makes column only take needed space
					spacing=10,
					horizontal_alignment=ft.CrossAxisAlignment.START,
				),
				padding=20,
			),
			actions=[
				ft.TextButton("Add", on_click=self.add_new_spending),
				ft.TextButton("Close", on_click=self.close_new_entry_dialog),
			],
			actions_alignment=ft.MainAxisAlignment.END,
		)

		self.dlg_edit_modal = ft.AlertDialog(
			modal=True,
			title=ft.Text("Edit Entry"),
			content=ft.Container(
				content=ft.Column(
					controls=[
						self.input_date,
						self.input_store,
						self.input_product,
						self.input_amount,
						self.input_price,
					],
					tight=True,  # Makes column only take needed space
					spacing=10,
					horizontal_alignment=ft.CrossAxisAlignment.START,
				),
				padding=20,
			),
			actions=[
				ft.TextButton("Edit", on_click=self.edit_spending),
				ft.TextButton("Delete", on_click=self.delete_spending),
				ft.TextButton("Close", on_click=self.close_edit_entry_dialog),
			],
			actions_alignment=ft.MainAxisAlignment.END,
		)

		self.controls = [
			ft.SafeArea(
				content = ft.ResponsiveRow(
					# vertical_alignment=ft.CrossAxisAlignment.CENTER,
					alignment=ft.MainAxisAlignment.CENTER,
					# Each item in controls, will be responsibe, respect to col parameter
					controls = [
						ft.Container(
							# bgcolor="#22CCCC00",
							# blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
							col = {"xs": 12, "md": 6, "lg": 4},
							width = 360,
							height = 814,
							content = ft.Column(
								horizontal_alignment = ft.CrossAxisAlignment.CENTER,
								# alignment = ft.MainAxisAlignment.CENTER,
								controls=[
									ft.Container(
										content = ft.ResponsiveRow(
											alignment=ft.MainAxisAlignment.CENTER,
											controls = [
												ft.TextField(
													prefix_icon = ft.Icons.SEARCH,
													hint_text="Search for entry",
													border_color = "transparent",
													col={"xs": 9,"sm": 9, "md": 8, "lg": 8, "xl": 8, "xxl": 8},
													height=40
												),
												ft.ElevatedButton(
													"Add",
													icon=ft.Icons.ADD,
													col={"xs": 3,"sm": 3, "md": 4, "lg": 4, "xl": 4, "xxl": 4},
													height=40,
													on_click=self.open_new_entry_dialog
												)	
											]
										)
									),
									ft.Divider(height=10,color="transparent"),
									ft.Container(
										content = ft.Row(
											# horizontal_alignment = ft.MainAxisAlignment.CENTER,
											controls = [
												ft.Column(
													controls = [
														self.table_view
													],
													scroll = True
												)
											],
											scroll = True,
											expand = 1,
										)
									)
								],
							)
						)
					]
				)
			)
		]

		self._init_db()

	def _init_db(self):
		# Here the logic should be taake into account the way the user will store its data
		# The user could store its data on cloud (Supabase) or using Local storage (SQlite)

		# For a CRUD environment
		self.current_data = self.database.select_all_data(exclude_id=False)
		# Based on the data inside `self.current_data`, populate the DataTable inmediatly
		for row in self.current_data:
			self.table_view.rows.append(
				self._create_data_row(
					item_id = row[0], 
					date = row[2], 
					store = row[3], 
					product = row[4], 
					amount = row[5], 
					price = row[6],
				)
			)

		# For Cloud Storage
		# self.current_data = 

	def reset_dialog_entries(self):
		self.input_date.set_value(datetime.now().date().strftime("%d-%m-%Y"))
		self.input_store.set_value("")
		self.input_product.set_value("")
		self.input_amount.set_value("")
		self.input_price.set_value("")
		self.current_entry_id = ""

	def _create_data_row(self, item_id, date, store, product, amount, price, selected=False):
		"""Helper method to create a DataRow with default on_select_changed behavior"""
		return ft.DataRow(
			cells=[
				ft.DataCell(ft.Text(date)),
				ft.DataCell(ft.Text(store)),
				ft.DataCell(ft.Text(product)),
				ft.DataCell(ft.Text(amount)),
				ft.DataCell(ft.Text(price)),
			],
			# selected=selected,
			# show_checkbox_column=True,
			on_long_press=self._handle_row_selection,
			data=item_id
		)

	def open_new_entry_dialog(self, e):
		e.control.page.overlay.append(self.dlg_modal)
		self.dlg_modal.open = True
		e.control.page.update()

	def close_new_entry_dialog(self, e):
		self.dlg_modal.open = False
		e.control.page.update()

	def _handle_row_selection(self, e):
		cell_content = [cell.content.value for cell in e.control.cells]
		logger.debug(f"Row selection changed. Selected: {cell_content} with id {e.control.data}")

		self.current_entry_id = e.control.data

		self.input_date.set_value(cell_content[0])
		self.input_store.set_value(cell_content[1])
		self.input_product.set_value(cell_content[2])
		self.input_amount.set_value(cell_content[3])
		self.input_price.set_value(cell_content[4])

		e.control.page.overlay.append(self.dlg_edit_modal)
		self.dlg_edit_modal.open = True
		e.control.page.update()

	def edit_spending(self, e):
		logger.debug(f"Current item ID: {self.current_entry_id}")

		new_date = self.input_date.input_value
		new_store = self.input_store.input_value
		new_product = self.input_product.input_value
		new_amount = int(self.input_amount.input_value)
		new_price = float(self.input_price.input_value)

		new_values = (new_date, new_store, new_product, new_amount, new_price)

		new_rows = []
		for row in self.table_view.rows:
			if row.data == self.current_entry_id:
				row.cells[0].content.value = new_date
				row.cells[1].content.value = new_store
				row.cells[2].content.value = new_product
				row.cells[3].content.value = new_amount
				row.cells[4].content.value = new_price
			new_rows.append(row)

		self.table_view.rows = new_rows
		# After modifying rows, update the UI
		self.table_view.update()		
		self.reset_dialog_entries()
		self.close_edit_entry_dialog(e)

		self.database.update(self.current_entry_id, new_values)

	def delete_spending(self, e):
		logger.debug(f"Current entry ID: {self.current_entry_id}")

		date = self.input_date.input_value
		store = self.input_store.input_value
		product = self.input_product.input_value
		amount = int(self.input_amount.input_value)
		price = float(self.input_price.input_value)

		logger.debug(f"Deliting row {(self.current_entry_id, self.user_id, date, store, product, amount, price)}...")

		filtered_rows = [
			row for row in self.table_view.rows
			if row.data != self.current_entry_id
		]
		self.table_view.rows = filtered_rows
		# After modifying rows, update the UI
		self.table_view.update()

		self.database.delete_row_by_id(self.current_entry_id)

		self.reset_dialog_entries()
		self.close_edit_entry_dialog(e)

	def close_edit_entry_dialog(self, e):
		self.reset_dialog_entries()
		self.dlg_edit_modal.open = False
		e.control.page.update()

	def add_new_spending(self, e):
		logger.debug("Adding new user to Datatable")
		item_id = str(uuid.uuid4())
		logger.debug(f"item ID: {item_id} -> {type(item_id)}")
		# Get the current values
		self.input_date.set_value(datetime.now().date().strftime("%d-%m-%Y"))

		date = self.input_date.input_value
		logger.debug(f"date: {date} -> {type(date)}")
		store = self.input_store.input_value
		logger.debug(f"store: {store} -> {type(store)}")
		product = self.input_product.input_value
		logger.debug(f"product: {product} -> {type(product)}")
		amount = int(self.input_amount.input_value)
		logger.debug(f"amount: {amount} -> {type(amount)}")
		price = float(self.input_price.input_value)
		logger.debug(f"price: {price} -> {type(price)}")

		self.table_view.rows.append(
			self._create_data_row(item_id, date, store, product, amount, price)
		)

		# Close dialog and clear fields
		self.close_new_entry_dialog(e)
		self.reset_dialog_entries()

		logger.debug(f"Inserting data {(item_id, self.user_id, date, store, product, amount, price)} into database ...")

		self.database.insert((item_id, self.user_id, date, store, product, amount, price))