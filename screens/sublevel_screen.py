import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from utils.theme import get_colors


def build_sublevel_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    c = get_colors(session.theme)
    sublevels = getattr(session, "_current_sublevels", [])

    items: list[ft.Control] = []
    for sub in sublevels:
        btn = ft.ElevatedButton(
            content=sub["label"],
            bgcolor=c["btn_bg"],
            color=c["btn_text"],
            on_click=lambda _, s=sub: _select_sublevel(page, session, s),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )
        row = ft.Container(
            content=ft.Row(
                controls=[btn],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.only(left=30, right=30, top=8, bottom=8),
        )
        items.append(row)
        items.append(
            ft.Container(
                content=ft.Divider(height=1, color=c["separator"], thickness=1),
                padding=ft.padding.symmetric(horizontal=30),
            )
        )

    return ft.View(
        route="/sublevel",
        bgcolor=c["bg"],
        controls=[
            ft.AppBar(
                title=ft.Text(session.current_level, color=c["text"]),
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
                    ft.Container(
                        content=ft.Text(
                            t["choose_sublevel"],
                            size=18,
                            weight=ft.FontWeight.W_500,
                            color=c["text"],
                        ),
                        padding=ft.padding.only(left=30),
                    ),
                    ft.Container(height=4),
                    *items,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=6,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )


def _select_sublevel(page: ft.Page, session: SessionState, sublevel: dict) -> None:
    session.set_sublevel(session.current_level, sublevel["key"])
    session._current_sublevel_label = sublevel["label"]
    page.go("/exercise")
