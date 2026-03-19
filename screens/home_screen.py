import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from utils.theme import get_colors


def build_home_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    c = get_colors(session.theme)

    return ft.View(
        route="/home",
        bgcolor=c["bg"],
        controls=[
            ft.AppBar(
                bgcolor=c["bg"],
                actions=[
                    ft.IconButton(
                        ft.Icons.SETTINGS_OUTLINED,
                        on_click=lambda _: page.go("/settings"),
                        tooltip=t["settings"],
                        icon_color=c["accent"],
                    )
                ],
            ),
            ft.Column(
                controls=[
                    # Hero logo
                    ft.Image(
                        src="logo-forpy.png",
                        width=300,
                        height=300,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    ft.Text(
                        "For Python — Learn by doing",
                        size=27,
                        color=c["text"],
                        font_family="Nunito",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=32),
                    # Python — active
                    ft.ElevatedButton(
                        content=t["chapter_python"],
                        on_click=lambda _: _select_chapter(page, session, "python"),
                        width=240,
                        height=50,
                        bgcolor=c["btn_bg"],
                        color=c["btn_text"],
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )


def _select_chapter(page: ft.Page, session: SessionState, chapter: str) -> None:
    session.current_chapter = chapter
    page.go("/level")
