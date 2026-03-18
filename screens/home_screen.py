import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations


def build_home_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)

    return ft.View(
        route="/home",
        controls=[
            ft.AppBar(
                title=ft.Text("FORPY", weight=ft.FontWeight.BOLD),
                actions=[
                    ft.IconButton(
                        ft.Icons.SETTINGS_OUTLINED,
                        on_click=lambda _: page.go("/settings"),
                        tooltip=t["settings"],
                    )
                ],
            ),
            ft.Column(
                controls=[
                    ft.Text("FORPY", size=40, weight=ft.FontWeight.BOLD),
                    ft.Text(t["welcome"], size=16),
                    ft.Divider(height=30),
                    ft.ElevatedButton(
                        t["chapter_python"],
                        on_click=lambda _: _select_chapter(page, session, "python"),
                        width=220,
                        height=50,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )


def _select_chapter(page: ft.Page, session: SessionState, chapter: str) -> None:
    session.current_chapter = chapter
    page.go("/level")
