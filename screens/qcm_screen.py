import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from utils.theme import get_colors
from services.ai_service import get_provider
from services.prompt_builder import PromptBuilder

_builder = PromptBuilder()


def build_qcm_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    c = get_colors(session.theme)

    loading_indicator = ft.Row(
        controls=[
            ft.ProgressRing(width=24, height=24, color=c["accent"]),
            ft.Text(t["generating"], italic=True, color=c["text"]),
        ],
        visible=True,
        spacing=12,
    )
    error_text = ft.Text("", color=ft.Colors.RED_400, visible=False)
    questions_col = ft.Column(controls=[], visible=False, spacing=16)

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
        page, session, t, c,
        loading_indicator, error_text,
        questions_col, another_btn,
    )

    view = ft.View(
        route="/qcm",
        bgcolor=c["bg"],
        controls=[
            ft.AppBar(
                title=ft.Text(t.get("qcm_python", "QCM Python"), color=c["text"]),
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
                    loading_indicator,
                    error_text,
                    questions_col,
                    ft.Container(
                        content=another_btn,
                        padding=ft.padding.only(top=4, bottom=80),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    page.run_task(
        _async_generate,
        page, session, t, c,
        loading_indicator, error_text,
        questions_col, another_btn,
    )

    return view


# ---------------------------------------------------------------------------
# Question card builder
# ---------------------------------------------------------------------------

def _build_question_card(q: dict, index: int, c: dict) -> ft.Container:
    correct_letter = q.get("reponse", "").strip().upper()
    options = q.get("options", [])

    option_widgets = []
    for opt in options:
        opt_letter = opt[0].upper() if opt else ""
        is_correct = opt_letter == correct_letter
        option_widgets.append(
            ft.Text(
                opt,
                color=c["accent"] if is_correct else c["text"],
                weight=ft.FontWeight.BOLD if is_correct else ft.FontWeight.NORMAL,
                size=13,
            )
        )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    q.get("bloc", ""),
                    color=c["accent"],
                    size=11,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Text(
                    f"Q{index}. {q.get('question', '')}",
                    color=c["text"],
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(height=1, color=c["border"], thickness=1),
                *option_widgets,
                ft.Divider(height=1, color=c["border"], thickness=1),
                ft.Text(
                    q.get("explication", ""),
                    color=c["text"],
                    italic=True,
                    size=13,
                ),
            ],
            spacing=6,
        ),
        bgcolor=c["card_bg"],
        border_radius=12,
        padding=16,
        border=ft.border.all(1, c["border"]),
    )


# ---------------------------------------------------------------------------
# QCM generation
# ---------------------------------------------------------------------------

async def _async_generate(
    page, session, t, c,
    loading, error_text,
    questions_col, another_btn,
):
    loading.visible = True
    error_text.visible = False
    questions_col.visible = False
    another_btn.visible = False
    page.update()

    try:
        if not session.api_key:
            raise ValueError("no_api_key")

        prompt = _builder.get_prompt(
            chapter=session.current_chapter,
            sublevel="qcm_python",
            exercise_language=session.exercise_language,
            last_topic=session.last_exercise_topic,
        )

        provider = get_provider(session.provider)
        result = await provider.call_async(prompt, session.api_key, "qcm_python")

        questions = result.get("_qcm_list", [])
        if not questions:
            raise ValueError("json")

        session.update_last_topic("qcm")

        questions_col.controls.clear()
        for i, q in enumerate(questions, start=1):
            questions_col.controls.append(_build_question_card(q, i, c))
        questions_col.visible = True
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
    page, session, t, c,
    loading, error_text,
    questions_col, another_btn,
):
    page.run_task(
        _async_generate,
        page, session, t, c,
        loading, error_text,
        questions_col, another_btn,
    )
