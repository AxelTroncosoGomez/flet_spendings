import flet as ft

def sucess_message(message, duration=3000):
	return ft.SnackBar(
		behavior = ft.SnackBarBehavior.FLOATING,
		bgcolor = "#193526",
		clip_behavior = ft.ClipBehavior.HARD_EDGE,
		content = ft.Row(
            [
            	ft.Icon(
            		name = ft.Icons.CHECK_CIRCLE,
            		color = "#7AF5B7",
            		size = 22
            	),
				ft.Text(
					value = message,
					size = 14,
					# weight = ft.FontWeight.BOLD,
					color = "#7AF5B7",
					font_family = "Verdana"
				),
            ], 
            alignment = "start", 
            spacing = 7
        ),
		duration = duration,
		margin = 30,
		shape = ft.RoundedRectangleBorder(radius=10),
		show_close_icon = False,
	)

def error_message(message, duration=3000):
	return ft.SnackBar(
		behavior = ft.SnackBarBehavior.FLOATING,
		bgcolor = "#2d0607",
		clip_behavior = ft.ClipBehavior.HARD_EDGE,
		content = ft.Row(
            [
            	ft.Icon(
            		name = ft.Icons.INFO_ROUNDED,
            		color = "#e48c92",
            		size = 22
            	),
				ft.Text(
					value = message,
					size = 14,
					weight = ft.FontWeight.BOLD,
					color = "#e48c92",
					font_family = "Verdana"
				),
            ], 
            alignment = "start", 
            spacing = 7
        ),
		duration = duration,
		margin = 30,
		shape = ft.RoundedRectangleBorder(radius=10),
		show_close_icon = False,
	)
