import flet as ft

# Constants for consistent sizing
LOGIN_CARD_WIDTH = 360
SNACKBAR_PADDING = 20
BOTTOM_RIGHT_MARGIN = 20

def _get_snackbar_width(page: ft.Page = None):
	"""Calculate appropriate snackbar width - always constrained, never full width."""
	if page is None:
		return LOGIN_CARD_WIDTH

	# Always use login card width for consistency across platforms
	# Never allow full width behavior
	return LOGIN_CARD_WIDTH

def _get_snackbar_behavior(page: ft.Page = None):
	"""Determine snackbar behavior based on platform."""
	if page is None:
		return ft.SnackBarBehavior.FLOATING

	# For mobile platforms, show below content
	if page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
		return ft.SnackBarBehavior.FLOATING

	# For web/desktop platforms, use floating for bottom-right positioning
	return ft.SnackBarBehavior.FLOATING

def _get_snackbar_margin(page: ft.Page = None):
	"""Calculate appropriate margin for platform-specific positioning."""
	if page is None:
		return BOTTOM_RIGHT_MARGIN

	# For mobile platforms (Android), show below content with standard margin
	if page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
		return ft.margin.symmetric(horizontal=BOTTOM_RIGHT_MARGIN, vertical=30)

	# For desktop platforms, position at bottom-right
	if page.platform in [ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS]:
		return ft.margin.only(
			right=BOTTOM_RIGHT_MARGIN,
			bottom=BOTTOM_RIGHT_MARGIN,
			left=0,
			top=0
		)

	# Default fallback (includes web which doesn't have a specific platform)
	return ft.margin.only(
		right=BOTTOM_RIGHT_MARGIN,
		bottom=BOTTOM_RIGHT_MARGIN,
		left=0,
		top=0
	)

def _get_snackbar_alignment(page: ft.Page = None):
	"""Get snackbar alignment based on platform."""
	if page is None:
		return None

	# For mobile platforms, use default alignment (centered below)
	if page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
		return None

	# For desktop platforms, align to bottom-right
	if page.platform in [ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS]:
		return ft.alignment.bottom_right

	# Default fallback (includes web) - align to bottom-right
	return ft.alignment.bottom_right

def sucess_message(message, duration=3000, page: ft.Page = None):
	"""Create a success snackbar with platform-appropriate positioning and width."""
	return ft.SnackBar(
		behavior=_get_snackbar_behavior(page),
		bgcolor="#193526",
		clip_behavior=ft.ClipBehavior.HARD_EDGE,
		content=ft.Row(
			[
				ft.Icon(
					name=ft.Icons.CHECK_CIRCLE,
					color="#7AF5B7",
					size=22
				),
				ft.Text(
					value=message,
					size=14,
					color="#7AF5B7",
					font_family="Verdana"
				),
			],
			alignment="start",
			spacing=7
		),
		duration=duration,
		margin=_get_snackbar_margin(page),
		width=_get_snackbar_width(page),
		shape=ft.RoundedRectangleBorder(radius=10),
		show_close_icon=False,
	)

def error_message(message, duration=3000, page: ft.Page = None):
	"""Create an error snackbar with platform-appropriate positioning and width."""
	return ft.SnackBar(
		behavior=_get_snackbar_behavior(page),
		bgcolor="#2d0607",
		clip_behavior=ft.ClipBehavior.HARD_EDGE,
		content=ft.Row(
			[
				ft.Icon(
					name=ft.Icons.INFO_ROUNDED,
					color="#e48c92",
					size=22
				),
				ft.Text(
					value=message,
					size=14,
					weight=ft.FontWeight.BOLD,
					color="#e48c92",
					font_family="Verdana"
				),
			],
			alignment="start",
			spacing=7
		),
		duration=duration,
		margin=_get_snackbar_margin(page),
		width=_get_snackbar_width(page),
		shape=ft.RoundedRectangleBorder(radius=10),
		show_close_icon=False,
	)
