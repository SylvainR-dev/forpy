import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from utils.theme import get_colors

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
    c = get_colors(session.theme)

    items: list[ft.Control] = []
    for level in LEVELS:
        n = len(level["sublevels"])
        badge = ft.Container(
            content=ft.Text(
                str(n),
                size=11,
                color="#ffffff",
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=c["accent"],
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=8, vertical=3),
        )
        btn = ft.ElevatedButton(
            content=level["name"],
            bgcolor=c["btn_bg"],
            color=c["btn_text"],
            on_click=lambda _, lvl=level: _select_level(page, session, lvl),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )
        row = ft.Container(
            content=ft.Row(
                controls=[btn, badge],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
        route="/level",
        bgcolor=c["bg"],
        controls=[
            ft.AppBar(
                title=ft.Text("Python", color=c["text"]),
                bgcolor=c["bg"],
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/home"),
                    tooltip=t["back"],
                    icon_color=c["accent"],
                ),
            ),
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            t["choose_level"],
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


def _select_level(page: ft.Page, session: SessionState, level: dict) -> None:
    session.current_level = level["name"]
    session._current_sublevels = level["sublevels"]
    page.go("/sublevel")
