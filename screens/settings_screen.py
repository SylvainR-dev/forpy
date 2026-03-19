import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from utils.theme import get_colors, apply_theme

PROVIDERS = ["anthropic", "openai", "gemini", "grok", "llama", "mistral"]

_PROVIDER_LABELS = {
    "anthropic": "Claude",
    "openai": "OpenAI",
    "gemini": "Gemini",
    "grok": "Grok",
    "llama": "LLaMA",
    "mistral": "Mistral",
}
LANGUAGES = ["english", "french"]


def build_settings_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    c = get_colors(session.theme)

    # --- Provider selection ---
    selected_provider = [session.provider]

    def _make_provider_btn(p: str) -> ft.Container:
        is_active = p == session.provider
        return ft.Container(
            content=ft.Text(
                _PROVIDER_LABELS.get(p, p.capitalize()),
                color=c["btn_text"],
                weight=ft.FontWeight.W_500,
                text_align=ft.TextAlign.CENTER,
            ),
            data=p,
            bgcolor=c["btn_bg"],
            opacity=1.0 if is_active else 0.35,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            on_click=lambda _, prov=p: _select_provider(prov),
            ink=True,
        )

    provider_btns = [_make_provider_btn(p) for p in PROVIDERS]
    provider_row = ft.Row(controls=provider_btns, spacing=8, wrap=True)

    def _select_provider(prov: str) -> None:
        selected_provider[0] = prov
        for btn in provider_row.controls:
            btn.opacity = 1.0 if btn.data == prov else 0.35
        page.update()

    # --- API key ---
    api_key_field = ft.TextField(
        label=t["api_key"],
        value=session.api_key,
        password=True,
        can_reveal_password=True,
        border_color=c["accent"],
        focused_border_color=c["accent"],
        label_style=ft.TextStyle(color=c["text"]),
        color=c["text"],
        bgcolor=c["card_bg"],
    )

    # --- Language dropdowns ---
    interface_lang_dropdown = ft.Dropdown(
        label=t["interface_language"],
        value=session.interface_language,
        options=[ft.dropdown.Option(lang) for lang in LANGUAGES],
        border_color=c["accent"],
        focused_border_color=c["accent"],
        color=c["text"],
        label_style=ft.TextStyle(color=c["text"]),
    )

    exercise_lang_dropdown = ft.Dropdown(
        label=t["exercise_language"],
        value=session.exercise_language,
        options=[ft.dropdown.Option(lang) for lang in LANGUAGES],
        border_color=c["accent"],
        focused_border_color=c["accent"],
        color=c["text"],
        label_style=ft.TextStyle(color=c["text"]),
    )

    # --- Dark mode toggle ---
    theme_switch = ft.Switch(
        label=t["dark_mode"],
        value=(session.theme == "dark"),
        active_color=c["accent"],
        label_text_style=ft.TextStyle(color=c["text"]),
    )

    def _toggle_theme(e) -> None:
        # Persist all current form values before rebuilding the view
        session.api_key = api_key_field.value.strip()
        session.provider = selected_provider[0]
        session.interface_language = interface_lang_dropdown.value
        session.exercise_language = exercise_lang_dropdown.value
        session.theme = "dark" if e.control.value else "light"
        session.save_settings()
        apply_theme(page, session.theme)
        page.go(page.route)  # Rebuild all views with the new theme colors

    theme_switch.on_change = _toggle_theme

    # --- Preferences card ---
    preferences_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    t["preferences"],
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=c["accent"],
                ),
                ft.Divider(height=1, color=c["border"], thickness=1),
                theme_switch,
                interface_lang_dropdown,
                exercise_lang_dropdown,
            ],
            spacing=14,
        ),
        bgcolor=c["card_bg"],
        border_radius=12,
        padding=16,
        border=ft.border.all(1, c["border"]),
    )

    feedback = ft.Text("", color=ft.Colors.GREEN_400)

    def save(_) -> None:
        session.api_key = api_key_field.value.strip()
        session.provider = selected_provider[0]
        session.interface_language = interface_lang_dropdown.value
        session.exercise_language = exercise_lang_dropdown.value
        session.save_settings()
        feedback.value = t["settings_saved"]
        page.update()

    return ft.View(
        route="/settings",
        bgcolor=c["bg"],
        controls=[
            ft.AppBar(
                title=ft.Text(t["settings"], color=c["text"]),
                bgcolor=c["bg"],
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/home"),
                    tooltip=t["back"],
                    icon_color=c["accent"],
                ),
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            t["provider"],
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=c["text"],
                        ),
                        provider_row,
                        ft.Divider(height=1, color=c["border"], thickness=1),
                        api_key_field,
                        ft.Divider(height=1, color=c["border"], thickness=1),
                        preferences_card,
                        ft.Container(height=8),
                        ft.ElevatedButton(
                            content=t["save"],
                            on_click=save,
                            height=50,
                            expand=True,
                            bgcolor=c["btn_bg"],
                            color=c["btn_text"],
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                        feedback,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=16,
                ),
                padding=ft.padding.symmetric(horizontal=16),
                expand=True,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
