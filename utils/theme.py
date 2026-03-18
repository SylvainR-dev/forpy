import flet as ft

DARK: dict = {
    "bg": "#1a1a2e",
    "card_bg": "#22223a",
    "code_bg": "#1e1e1e",
    "accent": "#4a9eff",
    "text": "#ffffff",
    "code_text": "#d4d4d4",
    "border": "#2a2a4a",
    "separator": "#4a9eff",
    "btn_bg": "#ffffff",
    "btn_text": "#1a1a2e",
}

LIGHT: dict = {
    "bg": "#f5f7fa",
    "card_bg": "#ffffff",
    "code_bg": "#1e1e1e",
    "accent": "#1a6ecc",
    "text": "#1a1a2e",
    "code_text": "#d4d4d4",
    "border": "#e0e4ec",
    "separator": "#1a6ecc",
    "btn_bg": "#1a1a2e",
    "btn_text": "#ffffff",
}


def get_colors(theme: str) -> dict:
    return DARK if theme == "dark" else LIGHT


def apply_theme(page: ft.Page, theme: str) -> None:
    c = get_colors(theme)
    page.bgcolor = c["bg"]
    page.theme_mode = ft.ThemeMode.DARK if theme == "dark" else ft.ThemeMode.LIGHT
