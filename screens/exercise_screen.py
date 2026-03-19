import asyncio
import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from utils.theme import get_colors
from services.ai_service import get_provider
from services.prompt_builder import PromptBuilder

_builder = PromptBuilder()


def build_exercise_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    c = get_colors(session.theme)
    sublevel_label = getattr(session, "_current_sublevel_label", session.current_sublevel)

    state = {"exercise": None, "error": None}

    # --- Loading indicator ---
    loading_indicator = ft.Row(
        controls=[
            ft.ProgressRing(width=24, height=24, color=c["accent"]),
            ft.Text(t["generating"], italic=True, color=c["text"]),
        ],
        visible=True,
        spacing=12,
    )
    error_text = ft.Text("", color=ft.Colors.RED_400, visible=False)

    # --- Body text widgets (updatable refs) ---
    enonce_text = ft.Text("", selectable=True, color=c["text"], size=14)
    correction_text = ft.Text(
        "", selectable=True, color="#d4d4d4", font_family="monospace", size=14
    )
    explication_text = ft.Text("", selectable=True, color=c["text"], size=14)
    deroulement_text = ft.Text("", selectable=True, color=c["text"], size=14)

    # --- Cards ---
    enonce_card = _card("📝", t["statement"], enonce_text, c)
    correction_card = _card("✅", t["correction"], correction_text, c, is_code=True, page=page)
    explication_card = _card("💡", t["explanation"], explication_text, c)
    deroulement_card = _card("🎙️", t["walkthrough"], deroulement_text, c)

    another_btn = ft.ElevatedButton(
        content=t["another_exercise"],
        visible=False,
        width=300,
        height=50,
        bgcolor=c["btn_bg"],
        color=c["btn_text"],
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )
    another_btn.on_click = lambda _: _generate(
        page, session, t, c, state,
        loading_indicator, error_text,
        enonce_card, enonce_text,
        correction_card, correction_text,
        explication_card, explication_text,
        deroulement_card, deroulement_text,
        another_btn,
    )

    view = ft.View(
        route="/exercise",
        bgcolor=c["bg"],
        controls=[
            ft.AppBar(
                title=ft.Text(sublevel_label, color=c["text"]),
                bgcolor=c["bg"],
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/pattern") if session.current_pattern else page.go("/sublevel"),
                    tooltip=t["back"],
                    icon_color=c["accent"],
                ),
            ),
            ft.Column(
                controls=[
                    loading_indicator,
                    error_text,
                    enonce_card,
                    correction_card,
                    explication_card,
                    deroulement_card,
                    ft.Container(height=4),
                    another_btn,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    page.run_task(
        _async_generate,
        page, session, t, c, state,
        loading_indicator, error_text,
        enonce_card, enonce_text,
        correction_card, correction_text,
        explication_card, explication_text,
        deroulement_card, deroulement_text,
        another_btn,
    )

    return view


# ---------------------------------------------------------------------------
# Card builder
# ---------------------------------------------------------------------------

def _card(
    icon: str,
    title: str,
    body_widget: ft.Text,
    c: dict,
    is_code: bool = False,
    page: ft.Page = None,
) -> ft.Container:
    inner: ft.Control
    if is_code:
        copy_icon = ft.Icon(ft.Icons.CONTENT_COPY, size=16, color="#d4d4d4")
        copy_label = ft.Text("", size=12, color="#d4d4d4")
        copy_btn = ft.TextButton(
            content=ft.Row(
                controls=[copy_icon, copy_label],
                spacing=4,
                tight=True,
            ),
        )

        async def on_copy(_):
            if page:
                page.set_clipboard(body_widget.value or "")
            copy_icon.name = ft.Icons.CHECK
            copy_icon.color = "#4caf50"
            copy_label.value = "Copié !"
            copy_label.color = "#4caf50"
            page.update()
            await asyncio.sleep(2)
            copy_icon.name = ft.Icons.CONTENT_COPY
            copy_icon.color = "#d4d4d4"
            copy_label.value = ""
            copy_label.color = "#d4d4d4"
            page.update()

        copy_btn.on_click = lambda e: page.run_task(on_copy, e) if page else None

        inner = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[ft.Container(expand=True), copy_btn],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    body_widget,
                ],
                spacing=4,
            ),
            bgcolor="#1e1e1e",
            border_radius=8,
            padding=12,
        )
    else:
        inner = body_widget

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    f"{icon}  {title}",
                    color=c["accent"],
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(height=1, color=c["border"], thickness=1),
                inner,
            ],
            spacing=10,
        ),
        bgcolor=c["card_bg"],
        border_radius=12,
        padding=16,
        border=ft.border.all(1, c["border"]),
        visible=False,
    )


# ---------------------------------------------------------------------------
# Exercise generation
# ---------------------------------------------------------------------------

async def _async_generate(
    page, session, t, c, state,
    loading, error_text,
    enonce_card, enonce_text,
    correction_card, correction_text,
    explication_card, explication_text,
    deroulement_card, deroulement_text,
    another_btn,
):
    loading.visible = True
    error_text.visible = False
    enonce_card.visible = False
    correction_card.visible = False
    explication_card.visible = False
    deroulement_card.visible = False
    another_btn.visible = False
    page.update()

    try:
        if not session.api_key:
            raise ValueError("no_api_key")

        prompt = _builder.get_prompt(
            chapter=session.current_chapter,
            sublevel=session.current_sublevel,
            exercise_language=session.exercise_language,
            last_topic=session.last_exercise_topic,
            category=session.current_pattern_category,
            pattern=session.current_pattern,
        )

        provider = get_provider(session.provider)
        exercise = await provider.call_async(prompt, session.api_key)

        session.update_last_topic(exercise.get("enonce", "")[:80])
        state["exercise"] = exercise

        enonce_text.value = exercise.get("enonce", "")
        enonce_card.visible = True

        correction_text.value = exercise.get("correction", "")
        correction_card.visible = True

        explication_text.value = exercise.get("explication", "")
        explication_card.visible = True

        deroulement_text.value = exercise.get("deroulement", "")
        deroulement_card.visible = True

        another_btn.visible = True

    except ValueError as exc:
        key = str(exc)
        error_text.value = t.get(f"error_{key}", t["error_generic"])
        error_text.visible = True
    except Exception as exc:
        error_text.value = f"{t['error_generic']}\n{exc}"
        error_text.visible = True
    finally:
        loading.visible = False
        page.update()


def _generate(
    page, session, t, c, state,
    loading, error_text,
    enonce_card, enonce_text,
    correction_card, correction_text,
    explication_card, explication_text,
    deroulement_card, deroulement_text,
    another_btn,
):
    page.run_task(
        _async_generate,
        page, session, t, c, state,
        loading, error_text,
        enonce_card, enonce_text,
        correction_card, correction_text,
        explication_card, explication_text,
        deroulement_card, deroulement_text,
        another_btn,
    )
