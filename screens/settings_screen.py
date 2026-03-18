import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations

PROVIDERS = ["anthropic", "openai", "gemini"]
LANGUAGES = ["english", "french"]


def build_settings_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)

    # --- Provider selection ---
    # Use a mutable container so the closure in save() can read the current value.
    selected_provider = [session.provider]

    def _make_provider_btn(p: str) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            p.capitalize(),
            data=p,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PRIMARY if p == session.provider else None,
            ),
            on_click=lambda _, prov=p: _select_provider(prov),
        )

    provider_row = ft.Row(
        controls=[_make_provider_btn(p) for p in PROVIDERS],
        spacing=8,
    )

    def _select_provider(prov: str) -> None:
        selected_provider[0] = prov
        for btn in provider_row.controls:
            btn.style = ft.ButtonStyle(
                bgcolor=ft.Colors.PRIMARY if btn.data == prov else None,
            )
        page.update()

    # --- API key ---
    api_key_field = ft.TextField(
        label=t["api_key"],
        value=session.api_key,
        password=True,
        can_reveal_password=True,
        width=340,
    )

    # --- Interface language ---
    interface_lang_dropdown = ft.Dropdown(
        label=t["interface_language"],
        value=session.interface_language,
        options=[ft.dropdown.Option(lang) for lang in LANGUAGES],
        width=240,
    )

    # --- Exercise language ---
    exercise_lang_dropdown = ft.Dropdown(
        label=t["exercise_language"],
        value=session.exercise_language,
        options=[ft.dropdown.Option(lang) for lang in LANGUAGES],
        width=240,
    )

    feedback = ft.Text("", color=ft.Colors.GREEN_400)

    def save(_) -> None:
        session.api_key = api_key_field.value.strip()
        session.provider = selected_provider[0]          # read from closure, always correct
        session.interface_language = interface_lang_dropdown.value
        session.exercise_language = exercise_lang_dropdown.value
        session.save_settings()
        feedback.value = t["settings_saved"]
        page.update()

    return ft.View(
        route="/settings",
        controls=[
            ft.AppBar(
                title=ft.Text(t["settings"]),
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/home"),
                    tooltip=t["back"],
                ),
            ),
            ft.Column(
                controls=[
                    ft.Text(t["provider"], size=16, weight=ft.FontWeight.W_500),
                    provider_row,
                    ft.Divider(),
                    api_key_field,
                    ft.Divider(),
                    interface_lang_dropdown,
                    exercise_lang_dropdown,
                    ft.Divider(),
                    ft.ElevatedButton(
                        t["save"],
                        on_click=save,
                        width=200,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    ),
                    feedback,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=16,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
