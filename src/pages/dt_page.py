import flet as ft
from icecream import ic
from utils.logger import logger
from components.inputs import InputComponent
from components.buttons import ButtonComponent, ImageButtonComponent
from services.supabase_service import SpendingsSupabaseDatabase
from exceptions import (
	GenericException,
	WrongCredentialsException,
	WrongPasswordException,
	UserAlreadyExistsException,
	EmailNotConfirmedException,
	UserNotAllowedException,
	SupabaseApiException,
	EmailNotValidException,
	InvalidCredentialsException
)
from components.dialogs import (
	sucess_message,
	error_message
)
from components.datatables import DataTableComponent

class NewPage(ft.View):

	def __init__(self, page: ft.Page):
		super().__init__(
			route="/new",
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			scroll=ft.ScrollMode.AUTO
		)

		self.fake_dt = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Store")),
                ft.DataColumn(ft.Text("Product")),
                ft.DataColumn(ft.Text("Amount")),
                ft.DataColumn(ft.Text("Price")),
            ],
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"2025-08-11")),
                        ft.DataCell(ft.Text(f"Store {i}")),
                        ft.DataCell(ft.Text(f"Product {i}")),
                        ft.DataCell(ft.Text(f"{100*i}")),
                        ft.DataCell(ft.Text(f"{100*i}")),
                    ]
                ) for i in range(1, 35)
            ],
            border_radius=10,
            heading_row_color=ft.Colors.BLACK12,
            data_row_color={"hovered": "0x30FF0000"},
            divider_thickness=0,
            show_bottom_border=True,
        )

		self.page = page
		self.table_view = DataTableComponent(
			datatable = self.fake_dt
		)

		# Create floating action button to add new rows
		self.add_row_button = ft.FloatingActionButton(
			icon=ft.Icons.ADD,
			tooltip="Add new row",
			on_click=self.add_new_row
		)

		self.controls = [
			ft.SafeArea(
				content = ft.ResponsiveRow(
					alignment=ft.MainAxisAlignment.CENTER,
					controls = [
						ft.Container(
							col = {"xs": 12, "md": 6, "lg": 4},
							width = 360,
							height = 814,
							content = ft.Column(
								horizontal_alignment = ft.CrossAxisAlignment.CENTER,
								controls=[
									ft.Container(
										content = ft.Row(
											controls = [
												ft.Column(
													controls = [
														self.table_view,
														ft.Container(
															content=self.add_row_button,
															alignment=ft.alignment.center,
															padding=ft.padding.only(top=10)
														),
													],
													scroll = True
												)
											],
											scroll = True,
											expand = 1,
										)
									),
								],
							)
						)
					]
				)
			),
		]

	def add_new_row(self, e):
		"""Add a new row with fake data to the DataTable and refresh the view"""
		# Get the current number of rows to generate unique data
		row_count = len(self.fake_dt.rows) + 1
		
		# Create a new row with fake data
		new_row = ft.DataRow(
			cells=[
				ft.DataCell(ft.Text("2025-08-12")),  # Current date
				ft.DataCell(ft.Text(f"Store {row_count}")),
				ft.DataCell(ft.Text(f"Product {row_count}")),
				ft.DataCell(ft.Text(f"{100 * row_count}")),
				ft.DataCell(ft.Text(f"{100 * row_count}")),
			]
		)
		
		# Add the new row to the DataTable
		self.fake_dt.rows.append(new_row)
		
		# Update the table view component
		self.table_view.datatable = self.fake_dt
		self.table_view.num_rows = len(self.fake_dt.rows)
		
		# Recalculate pagination
		p_int, p_add = divmod(self.table_view.num_rows, self.table_view.rows_per_page)
		self.table_view.num_pages = p_int + (1 if p_add else 0)
		
		# Refresh the data display
		self.table_view.refresh_data()
		
		# Update the page to reflect changes
		self.page.update()