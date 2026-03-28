import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from utils.theme import get_colors

# Ordered levels with their sublevels and corresponding prompt file keys
LEVELS = [
    {
        "name": "Noob",
        "name_key": "level_noob",
        "image": "logique_noob.png",
        "sublevels": [
            {"label": "Noob", "label_key": "sub_noob", "key": "noob"},
        ],
    },
    {
        "name": "Débutant",
        "name_key": "level_debutant",
        "image": "logique_debutant.png",
        "sublevels": [
            {"label": "Débutant", "label_key": "sub_debutant", "key": "debutant"},
            {"label": "Débutant ++", "label_key": "sub_debutant_plus", "key": "debutant_plus"},
            {"label": "DEBUG Débutant", "label_key": "sub_debug_debutant", "key": "debug_debutant"},
        ],
    },
    {
        "name": "Intermédiaire",
        "name_key": "level_intermediaire",
        "image": "logique_intermediaire.png",
        "sublevels": [
            {"label": "Intermédiaire", "label_key": "sub_intermediaire", "key": "intermediaire"},
            {"label": "Intermédiaire Avancé", "label_key": "sub_intermediaire_avance", "key": "intermediaire_avance"},
            {"label": "DEBUG Intermédiaire", "label_key": "sub_debug_intermediaire", "key": "debug_intermediaire"},
            {"label": "Pythonique Intermédiaire", "label_key": "sub_pythonique_intermediaire", "key": "pythonique_intermediaire"},
            {"label": "Pattern", "label_key": "sub_pattern", "key": "pattern_intermediaire"},
        ],
    },
    {
        "name": "Intermédiaire ++",
        "name_key": "level_intermediaire_plus",
        "image": "logique_intermediaire_plus.png",
        "sublevels": [
            {"label": "Fonctions avancées", "label_key": "sub_fonctions_avancees", "key": "fonctions_avancees"},
            {"label": "Manipulation structure", "label_key": "sub_manipulation_structure", "key": "manipulation_structure"},
            {"label": "Entrée/Sortie et erreurs", "label_key": "sub_entree_sortie_erreurs", "key": "entree_sortie_erreurs"},
            {"label": "Organisation du code", "label_key": "sub_organisation_code", "key": "organisation_code"},
            {"label": "DEBUG Intermédiaire ++", "label_key": "sub_debug_intermediaire_plus", "key": "debug_intermediaire_plus"},
            {"label": "Pythonique Intermédiaire ++", "label_key": "sub_pythonique_intermediaire_plus", "key": "pythonique_intermediaire_plus"},
            {"label": "Pattern", "label_key": "sub_pattern", "key": "pattern_intermediaire_plus"},
        ],
    },
    {
        "name": "POO",
        "name_key": "level_poo",
        "image": "logique_poo.png",
        "sublevels": [
            {"label": "Intro POO", "label_key": "sub_intro_poo", "key": "intro_poo"},
            {"label": "POO ++", "label_key": "sub_poo_plus", "key": "poo_plus"},
            {"label": "DEBUG POO", "label_key": "sub_debug_poo", "key": "debug_poo"},
            {"label": "POO Pythonique", "label_key": "sub_poo_pythonique", "key": "poo_pythonique"},
            {"label": "Pattern", "label_key": "sub_pattern", "key": "pattern_poo"},
        ],
    },
    {
        "name": "Expert Architecture",
        "name_key": "level_expert",
        "image": "logique_expert.png",
        "sublevels": [
            {"label": "Architecture", "label_key": "sub_architecture", "key": "architecture"},
            {"label": "DEBUG Architecture", "label_key": "sub_debug_architecture", "key": "debug_architecture"},
            {"label": "Architecture Pythonique", "label_key": "sub_architecture_pythonique", "key": "architecture_pythonique"},
            {"label": "Pattern", "label_key": "sub_pattern", "key": "pattern_expert"},
        ],
    },
]


def build_level_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    c = get_colors(session.theme)

    items: list[ft.Control] = []
    for level in LEVELS:
        logic_btn = ft.ElevatedButton(
            content=t["voir_la_logique"],
            bgcolor="#4a9eff",
            color="#ffffff",
            height=48,
            on_click=lambda _, lvl=level: _open_logic(page, session, lvl["image"]),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )
        btn = ft.ElevatedButton(
            content=t.get(level["name_key"], level["name"]),
            bgcolor=c["btn_bg"],
            color=c["btn_text"],
            height=48,
            on_click=lambda _, lvl=level: _select_level(page, session, lvl),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )
        row = ft.Container(
            content=ft.Row(
                controls=[btn, logic_btn],
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

    qcm_btn = ft.ElevatedButton(
        content=t.get("qcm_python", "QCM Python"),
        bgcolor=c["btn_bg"],
        color=c["btn_text"],
        height=48,
        on_click=lambda _: page.go("/qcm"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    items.append(
        ft.Container(
            content=ft.Row(
                controls=[qcm_btn],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(left=30, right=30, top=8, bottom=8),
        )
    )
    items.append(
        ft.Container(
            content=ft.Divider(height=1, color=c["separator"], thickness=1),
            padding=ft.padding.symmetric(horizontal=30),
        )
    )

    qcm_architecture_btn = ft.ElevatedButton(
        content=t.get("qcm_architecture", "Architecture Quiz"),
        bgcolor=c["btn_bg"],
        color=c["btn_text"],
        height=48,
        on_click=lambda _: page.go("/qcm_architecture"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    items.append(
        ft.Container(
            content=ft.Row(
                controls=[qcm_architecture_btn],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(left=30, right=30, top=8, bottom=8),
        )
    )
    items.append(
        ft.Container(
            content=ft.Divider(height=1, color=c["separator"], thickness=1),
            padding=ft.padding.symmetric(horizontal=30),
        )
    )
    items.append(ft.Container(height=60))

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


def _open_logic(page: ft.Page, session: SessionState, image_name: str) -> None:
    session.current_logic_image = image_name
    page.go("/logic")


def _select_level(page: ft.Page, session: SessionState, level: dict) -> None:
    session.current_level = level["name"]
    session._current_level_key = level["name_key"]
    session._current_sublevels = level["sublevels"]
    page.go("/sublevel")
