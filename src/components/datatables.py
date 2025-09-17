from typing import Callable, Optional, Tuple
import flet as ft
from utils.logger import logger


class DataTableComponent(ft.Container):
	DEFAULT_ROW_PER_PAGE = 10

	def __init__(
		self, 
		datatable: ft.DataTable,
		rows_per_page: int = DEFAULT_ROW_PER_PAGE
	):
		super().__init__()

		self.rows_per_page = rows_per_page
		self.datatable = datatable
		self.num_rows = len(self.datatable.rows)
		self.current_page = 1
		self.v_count = ft.Text(weight=ft.FontWeight.BOLD)

		# Calculating the number of pages.
		p_int, p_add = divmod(self.num_rows, self.rows_per_page)
		self.num_pages = p_int + (1 if p_add else 0)

		self.v_current_page = ft.GestureDetector(
			content=ft.Text(
				str(self.current_page),
				tooltip="Double click to set current page.",
				weight=ft.FontWeight.BOLD
			),
			on_double_tap=self.toggle_page_field
		)
		
		self.shown_datatable = ft.DataTable(
			columns = self.datatable.columns,
			rows = self.build_rows(),
			border_radius=10,
			heading_row_color=ft.Colors.BLACK12,
			data_row_color={"hovered": "0x30FF0000"},
			divider_thickness=0,
			show_bottom_border=True,
		)

		self.current_page_changer_field = ft.TextField(
			value=str(self.current_page),
			dense=True,
			filled=False,
			width=40,
			on_submit=self.on_page_field_submit,
			on_blur=self.hide_page_field,
			visible=False,
			keyboard_type=ft.KeyboardType.NUMBER,
			content_padding=2,
			text_align=ft.TextAlign.CENTER
		)

		self.v_num_of_row_changer_field = ft.TextField(
			value = str(self.rows_per_page),
			dense = True,
			filled = False,
			width = 40,
			on_submit = lambda e: self.set_rows_per_page(e.control.value),
			keyboard_type = ft.KeyboardType.NUMBER,
			content_padding = 2,
			text_align = ft.TextAlign.CENTER
		)

		self.content = ft.Container(
			ft.Column(
				controls = [
					self.shown_datatable,
					ft.Row(
						controls=[
							ft.Row(
								controls = [
									ft.IconButton(
										ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT,
										on_click=self.goto_first_page,
										tooltip="First Page"
									),
									ft.IconButton(
										ft.Icons.KEYBOARD_ARROW_LEFT,
										on_click=self.prev_page,
										tooltip="Previous Page"
									),
									ft.IconButton(
										ft.Icons.KEYBOARD_ARROW_RIGHT,
										on_click=self.next_page,
										tooltip="Next Page"
									),
									ft.IconButton(
										ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT,
										on_click=self.goto_last_page,
										tooltip="Last Page"
									),
								]
							),
							ft.Row(
								controls = [
									self.v_num_of_row_changer_field, ft.Text("rows per page")
								]
							),
							ft.Stack(
								controls=[
									self.v_current_page,
									self.current_page_changer_field
								]
							),
							self.v_count,
						],
						alignment=ft.MainAxisAlignment.CENTER
					),
				],
				scroll=ft.ScrollMode.AUTO
			),
			padding=10,
		)

	def set_rows_per_page(self, new_row_per_page: str):
		"""
		Takes a string as an argument, tries converting it to an integer, and sets the number of rows 
		per page to that integer if it is between 1 and the total number of rows, otherwise it sets 
		the number of rows per page to the default value

		:param new_row_per_page: The new number of rows per page
		:type new_row_per_page: str
		:raise ValueError
		"""
		try:
			self.rows_per_page = int(new_row_per_page) \
				if 1 <= int(new_row_per_page) <= self.num_rows \
				else self.DEFAULT_ROW_PER_PAGE
		except ValueError:
			# if an error occurs set to default
			self.rows_per_page = self.DEFAULT_ROW_PER_PAGE
		self.v_num_of_row_changer_field.value = str(self.rows_per_page)

		# Calculating the number of pages.
		p_int, p_add = divmod(self.num_rows, self.rows_per_page)
		self.num_pages = p_int + (1 if p_add else 0)

		self.set_page(page=1)

	def set_page(self, page: [str, int, None] = None, delta: int = 0):
		"""
		Sets the current page using the page parameter if provided. Else if the delta is not 0,
		sets the current page to the current page plus the provided delta.

		:param page: the page number to display
		:param delta: The number of pages to move forward or backward, defaults to 0 (optional)
		:return: The current page number.
		:raise ValueError
		"""
		if page is not None:
			try:
				self.current_page = int(page) if 1 <= int(page) <= self.num_pages else 1
			except ValueError:
				self.current_page = 1
		elif delta:
			self.current_page += delta
		else:
			return
		self.refresh_data()

	def next_page(self, e: ft.ControlEvent):
		"""sets the current page to the next page"""
		if self.current_page < self.num_pages:
			self.set_page(delta=1)

	def prev_page(self, e: ft.ControlEvent):
		"""set the current page to the previous page"""
		if self.current_page > 1:
			self.set_page(delta=-1)

	def goto_first_page(self, e: ft.ControlEvent):
		"""sets the current page to the first page"""
		self.set_page(page=1)

	def goto_last_page(self, e: ft.ControlEvent):
		"""sets the current page to the last page"""
		self.set_page(page=self.num_pages)


	def build_rows(self) -> list:
		"""
		Returns a slice of indexes, using the start and end values returned by the paginate() function
		:return: The rows of data that are being displayed on the page.
		"""
		return self.datatable.rows[slice(*self.paginate())]

	def paginate(self) -> tuple[int, int]:
		"""
		Returns a tuple of two integers, where the first is the index of the first row to be displayed
		on the current page, and `the second the index of the last row to be displayed on the current page
		:return: A tuple of two integers.
		"""
		i1_multiplier = 0 if self.current_page == 1 else self.current_page - 1
		i1 = i1_multiplier * self.rows_per_page
		i2 = self.current_page * self.rows_per_page

		return i1, i2

	def refresh_data(self):
		# Setting the rows of the paginated datatable to the rows returned by the `build_rows()` function.
		self.shown_datatable.rows = self.build_rows()
		# display the total number of rows in the table.
		self.v_count.value = f"Total Rows: {self.num_rows}"
		# the current page number versus the total number of pages.
		self.v_current_page.content.value = f"{self.current_page}/{self.num_pages}"

		# update the visibility of controls in the gesture detector
		self.current_page_changer_field.visible = False
		self.v_current_page.visible = True

		# update the control so the above changes are rendered in the UI
		self._safe_update()

	def _safe_update(self):
		"""Safely update the component if it's attached to a page."""
		try:
			if hasattr(self, '_Control__page') and self._Control__page is not None:
				self.update()
		except (AttributeError, AssertionError):
			# Component not yet added to page, skip update
			pass

	def toggle_page_field(self, e: ft.ControlEvent):
		"""Toggle between current page display and page input field."""
		self.v_current_page.visible = False
		self.current_page_changer_field.visible = True
		self.current_page_changer_field.value = str(self.current_page)
		self._safe_update()

		# Focus on the field if possible
		try:
			self.current_page_changer_field.focus()
		except (AttributeError, AssertionError):
			pass

	def on_page_field_submit(self, e: ft.ControlEvent):
		"""Handle page field submission."""
		self.set_page(page=e.control.value)
		self.hide_page_field(e)

	def hide_page_field(self, e: ft.ControlEvent):
		"""Hide the page input field and show current page display."""
		self.current_page_changer_field.visible = False
		self.v_current_page.visible = True
		self._safe_update()

	def update_data(self, new_datatable: ft.DataTable):
		"""Update the component with new data."""
		self.datatable = new_datatable
		self.num_rows = len(self.datatable.rows)

		# Recalculate number of pages
		p_int, p_add = divmod(self.num_rows, self.rows_per_page)
		self.num_pages = p_int + (1 if p_add else 0)

		# Reset to first page if current page is now invalid
		if self.current_page > self.num_pages and self.num_pages > 0:
			self.current_page = 1
		elif self.num_pages == 0:
			self.current_page = 1

		# Update the shown datatable columns
		self.shown_datatable.columns = self.datatable.columns

		# Refresh the display
		self.refresh_data()