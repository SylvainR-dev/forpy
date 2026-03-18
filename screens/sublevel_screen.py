import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations


def build_sublevel_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    sublevels = getattr(session, "_current_sublevels", [])

    sublevel_buttons = [
        ft.ElevatedButton(
            sub["label"],
            on_click=lambda _, s=sub: _select_sublevel(page, session, s),
            width=280,
            height=48,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        )
        for sub in sublevels
    ]

    return ft.View(
        route="/sublevel",
        controls=[
            ft.AppBar(
                title=ft.Text(session.current_level),
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/level"),
                    tooltip=t["back"],
                ),
            ),
            ft.Column(
                controls=[
                    ft.Text(t["choose_sublevel"], size=20, weight=ft.FontWeight.W_500),
                    ft.Divider(height=20),
                    *sublevel_buttons,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )


def _select_sublevel(page: ft.Page, session: SessionState, sublevel: dict) -> None:
    session.set_sublevel(session.current_level, sublevel["key"])
    session._current_sublevel_label = sublevel["label"]
    page.go("/exercise")
