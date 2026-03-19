import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from utils.theme import get_colors


def build_logic_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    c = get_colors(session.theme)

    return ft.View(
        route="/logic",
        bgcolor=c["bg"],
        controls=[
            ft.AppBar(
                title=ft.Text(t["voir_la_logique"], color=c["text"]),
                bgcolor=c["bg"],
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/level"),
                    tooltip=t["back"],
                    icon_color=c["accent"],
                ),
            ),
            ft.Column(
                controls=[
                    ft.Image(
                        src=session.current_logic_image,
                        fit=ft.BoxFit.CONTAIN,
                        expand=True,
                    ),
                ],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
    )
