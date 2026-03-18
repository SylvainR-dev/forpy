import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations

# Ordered levels with their sublevels and corresponding prompt file keys
LEVELS = [
    {
        "name": "Noob",
        "sublevels": [
            {"label": "Noob", "key": "noob"},
        ],
    },
    {
        "name": "Débutant",
        "sublevels": [
            {"label": "Débutant", "key": "debutant"},
            {"label": "Débutant ++", "key": "debutant_plus"},
            {"label": "DEBUG Débutant", "key": "debug_debutant"},
        ],
    },
    {
        "name": "Intermédiaire",
        "sublevels": [
            {"label": "Intermédiaire", "key": "intermediaire"},
            {"label": "Intermédiaire Avancé", "key": "intermediaire_avance"},
            {"label": "DEBUG Intermédiaire", "key": "debug_intermediaire"},
            {"label": "Pythonique Intermédiaire", "key": "pythonique_intermediaire"},
            {"label": "Pattern", "key": "pattern_intermediaire"},
        ],
    },
    {
        "name": "Intermédiaire ++",
        "sublevels": [
            {"label": "Fonctions avancées", "key": "fonctions_avancees"},
            {"label": "Manipulation structure", "key": "manipulation_structure"},
            {"label": "Entrée/Sortie et erreurs", "key": "entree_sortie_erreurs"},
            {"label": "Organisation du code", "key": "organisation_code"},
            {"label": "DEBUG Intermédiaire ++", "key": "debug_intermediaire_plus"},
            {"label": "Pythonique Intermédiaire ++", "key": "pythonique_intermediaire_plus"},
            {"label": "Pattern", "key": "pattern_intermediaire_plus"},
        ],
    },
    {
        "name": "POO",
        "sublevels": [
            {"label": "Intro POO", "key": "intro_poo"},
            {"label": "POO ++", "key": "poo_plus"},
            {"label": "DEBUG POO", "key": "debug_poo"},
            {"label": "POO Pythonique", "key": "poo_pythonique"},
            {"label": "Pattern", "key": "pattern_poo"},
        ],
    },
    {
        "name": "Expert Architecture",
        "sublevels": [
            {"label": "Architecture", "key": "architecture"},
            {"label": "DEBUG Architecture", "key": "debug_architecture"},
            {"label": "Architecture Pythonique", "key": "architecture_pythonique"},
            {"label": "Pattern", "key": "pattern_expert"},
        ],
    },
]


def build_level_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)

    level_buttons = [
        ft.ElevatedButton(
            level["name"],
            on_click=lambda _, lvl=level: _select_level(page, session, lvl),
            width=280,
            height=48,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        )
        for level in LEVELS
    ]

    return ft.View(
        route="/level",
        controls=[
            ft.AppBar(
                title=ft.Text("Python"),
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/home"),
                    tooltip=t["back"],
                ),
            ),
            ft.Column(
                controls=[
                    ft.Text(t["choose_level"], size=20, weight=ft.FontWeight.W_500),
                    ft.Divider(height=20),
                    *level_buttons,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )


def _select_level(page: ft.Page, session: SessionState, level: dict) -> None:
    session.current_level = level["name"]
    # Store sublevels for the sublevel screen
    session._current_sublevels = level["sublevels"]
    page.go("/sublevel")
