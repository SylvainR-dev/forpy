import flet as ft
from utils.session_state import SessionState
from utils.theme import apply_theme

def main(page: ft.Page):
    try:
        _main(page)
    except Exception as _e:
        import traceback
        _tb = traceback.format_exc()
        try:
            page.bgcolor = "#1a1a2e"
            page.controls.clear()
            page.add(
                ft.Text("FORPY — CRASH AT STARTUP", color="#ff4444", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(str(_e), color="#ff8800", size=13, selectable=True),
                ft.Text(_tb, color="#ffffff", size=11, selectable=True, font_family="monospace"),
            )
            page.update()
        except Exception:
            pass


def _main(page: ft.Page):
    session = SessionState()
    page.title = "FORPY"
    page.padding = 10
    try:
        page.fonts = {
            "Nunito": "https://fonts.gstatic.com/s/nunito/v25/XRXI3I6Li01BKofiOc5wtlZ2di8HDIkhdTQ3j6zbXWjgeg.woff2"
        }
    except Exception:
        pass  # Font URL not available in packaged APK — fallback to system font
    try:
        apply_theme(page, session.theme)
    except Exception:
        try:
            page.bgcolor = "#1a1a2e"
            page.theme_mode = ft.ThemeMode.DARK
        except Exception:
            pass

    def route_change(e):
        """
        Rebuild the full view stack for the current route.

        Stack layout per route:
            /home                   → [home]
            /settings               → [home, settings]
            /level                  → [home, level]
            /sublevel               → [home, level, sublevel]
            /exercise               → [home, level, sublevel, exercise]

        This ensures the physical back button (view_pop) works correctly
        on all platforms, while custom AppBar back buttons also work via page.go().
        """
        from screens.home_screen import build_home_screen
        from screens.level_screen import build_level_screen
        from screens.sublevel_screen import build_sublevel_screen
        from screens.exercise_screen import build_exercise_screen
        from screens.settings_screen import build_settings_screen
        from screens.pattern_screen import build_pattern_screen
        from screens.logic_screen import build_logic_screen

        route = page.route
        page.views.clear()

        # Layer 1 — always present
        try:
            page.views.append(build_home_screen(page, session))
        except Exception as e:
            page.views.append(ft.View(
                route="/home",
                controls=[ft.Text(f"Home screen error: {e}", color="red", selectable=True)],
            ))

        def safe_append(builder, *args):
            try:
                page.views.append(builder(*args))
            except Exception as ex:
                page.views.append(ft.View(
                    route=route,
                    controls=[ft.Text(f"Screen error: {ex}", color="red", selectable=True)],
                ))

        if route == "/settings":
            safe_append(build_settings_screen, page, session)

        elif route == "/logic":
            safe_append(build_level_screen, page, session)
            safe_append(build_logic_screen, page, session)

        elif route in ("/level", "/sublevel", "/pattern", "/exercise"):
            safe_append(build_level_screen, page, session)

            if route in ("/sublevel", "/pattern", "/exercise"):
                safe_append(build_sublevel_screen, page, session)

                if route in ("/pattern", "/exercise") and session.current_sublevel.startswith("pattern_"):
                    safe_append(build_pattern_screen, page, session)

                    if route == "/exercise":
                        safe_append(build_exercise_screen, page, session)

                elif route == "/exercise":
                    safe_append(build_exercise_screen, page, session)

        try:
            page.update()
        except Exception:
            pass

    def view_pop(e):
        """Handle physical back button (Android / desktop window close gesture)."""
        try:
            if len(page.views) > 1:
                page.views.pop()
                top_view = page.views[-1]
                page.go(top_view.route)
            else:
                page.go("/home")
        except Exception:
            try:
                page.go("/home")
            except Exception:
                pass

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    try:
        page.go("/home")
    except Exception as e:
        try:
            page.add(ft.Text(f"Navigation error: {e}", color="red"))
            page.update()
        except Exception:
            pass


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
