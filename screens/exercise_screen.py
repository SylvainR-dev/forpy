import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from services.ai_service import get_provider
from services.prompt_builder import PromptBuilder

_builder = PromptBuilder()


def build_exercise_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    sublevel_label = getattr(session, "_current_sublevel_label", session.current_sublevel)

    # Mutable state for this view
    state = {"exercise": None, "error": None}

    # --- UI refs ---
    loading_indicator = ft.Row(
        controls=[
            ft.ProgressRing(width=24, height=24),
            ft.Text(t["generating"], italic=True),
        ],
        visible=True,
        spacing=12,
    )
    error_text = ft.Text("", color=ft.Colors.RED_400, visible=False)

    enonce_section = _section(t["statement"], "", visible=False)
    correction_section = _section(t["correction"], "", visible=False, monospace=True)
    explication_section = _section(t["explanation"], "", visible=False)
    deroulement_section = _section(t["walkthrough"], "", visible=False)

    another_btn = ft.ElevatedButton(
        t["another_exercise"],
        on_click=lambda _: _generate(page, session, t, state, loading_indicator,
                                     error_text, enonce_section, correction_section,
                                     explication_section, deroulement_section,
                                     another_btn),
        visible=False,
        width=260,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )

    view = ft.View(
        route="/exercise",
        controls=[
            ft.AppBar(
                title=ft.Text(sublevel_label),
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/sublevel"),
                    tooltip=t["back"],
                ),
            ),
            ft.Column(
                controls=[
                    loading_indicator,
                    error_text,
                    enonce_section,
                    correction_section,
                    explication_section,
                    deroulement_section,
                    another_btn,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    # Trigger first exercise generation after the view is rendered
    page.run_task(
        _async_generate, page, session, t, state,
        loading_indicator, error_text,
        enonce_section, correction_section,
        explication_section, deroulement_section,
        another_btn,
    )

    return view


# ---------------------------------------------------------------------------
# Section builder
# ---------------------------------------------------------------------------

def _section(title: str, body: str, visible: bool = True, monospace: bool = False) -> ft.Column:
    font_family = "monospace" if monospace else None
    return ft.Column(
        controls=[
            ft.Text(title, size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(height=4),
            ft.Text(body, selectable=True, font_family=font_family),
        ],
        visible=visible,
        spacing=4,
    )


def _update_section(section: ft.Column, body: str) -> None:
    section.controls[2].value = body
    section.visible = True


# ---------------------------------------------------------------------------
# Exercise generation
# ---------------------------------------------------------------------------

async def _async_generate(page, session, t, state, loading, error_text,
                           enonce_sec, correction_sec, explication_sec,
                           deroulement_sec, another_btn):
    loading.visible = True
    error_text.visible = False
    enonce_sec.visible = False
    correction_sec.visible = False
    explication_sec.visible = False
    deroulement_sec.visible = False
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
        )

        provider = get_provider(session.provider)
        exercise = await provider.call_async(prompt, session.api_key)

        session.update_last_topic(exercise.get("enonce", "")[:80])
        state["exercise"] = exercise

        _update_section(enonce_sec, exercise.get("enonce", ""))
        _update_section(correction_sec, exercise.get("correction", ""))
        _update_section(explication_sec, exercise.get("explication", ""))
        _update_section(deroulement_sec, exercise.get("deroulement", ""))
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


def _generate(page, session, t, state, loading, error_text,
              enonce_sec, correction_sec, explication_sec, deroulement_sec, another_btn):
    page.run_task(
        _async_generate, page, session, t, state,
        loading, error_text,
        enonce_sec, correction_sec, explication_sec, deroulement_sec,
        another_btn,
    )
