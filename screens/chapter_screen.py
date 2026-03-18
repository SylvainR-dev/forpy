"""
Chapter selection screen.
Currently only "Python" is available for the MVP.
This screen is kept for future extensibility (Python ML, Python IA, etc.).
For MVP, the home screen routes directly to the level screen.
"""
import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations

CHAPTERS = [
    {"label": "Python", "key": "python"},
]


def build_chapter_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)

    chapter_buttons = [
        ft.ElevatedButton(
            ch["label"],
            on_click=lambda _, c=ch: _select_chapter(page, session, c),
            width=260,
            height=48,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        )
        for ch in CHAPTERS
    ]

    return ft.View(
        route="/chapter",
        controls=[
            ft.AppBar(
                title=ft.Text("FORPY"),
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/home"),
                    tooltip=t["back"],
                ),
            ),
            ft.Column(
                controls=[
                    *chapter_buttons,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )


def _select_chapter(page: ft.Page, session: SessionState, chapter: dict) -> None:
    session.current_chapter = chapter["key"]
    page.go("/level")
