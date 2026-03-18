import flet as ft
from utils.session_state import SessionState
from utils.theme import apply_theme

session = SessionState()


def main(page: ft.Page):
    page.title = "FORPY"
    page.padding = 10
    apply_theme(page, session.theme)

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

        route = page.route
        page.views.clear()

        # Layer 1 — always present
        page.views.append(build_home_screen(page, session))

        if route == "/settings":
            page.views.append(build_settings_screen(page, session))

        elif route in ("/level", "/sublevel", "/exercise"):
            page.views.append(build_level_screen(page, session))

            if route in ("/sublevel", "/exercise"):
                page.views.append(build_sublevel_screen(page, session))

                if route == "/exercise":
                    page.views.append(build_exercise_screen(page, session))

        page.update()

    def view_pop(e):
        """Handle physical back button (Android / desktop window close gesture)."""
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.go("/home")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/home")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
