import flet as ft
from utils.session_state import SessionState
from utils.translations import get_translations
from utils.theme import get_colors

# ---------------------------------------------------------------------------
# Pattern data per sublevel
# ---------------------------------------------------------------------------

PATTERNS_INTERMEDIAIRE = {
    "Dictionnaires": [
        ".items()", ".values()", ".keys()",
        ".get()", ".setdefault()",
        "defaultdict", "Counter",
        "dict comprehension",
    ],
    "Listes": [
        "enumerate()", "zip()",
        "list comprehension", "* unpacking",
        ".append()/.extend()",
        ".remove()/.pop()", "slice",
    ],
    "Sets": [
        "set()", ".add()", "intersection",
        "union", "difference",
        "symmetric_difference", "in",
    ],
    "Chaînes": [
        ".lower()/.upper()", ".strip()",
        ".split()", ".join()",
        ".startswith()/.endswith()",
        ".isdigit()/.isalpha()", ".replace()",
        "f-strings",
    ],
    "Tri et recherche": [
        "sorted()", ".sort()",
        "max()/min()", "lambda",
        "key=len", ".count()", ".index()",
    ],
    "Comptage et statistiques": [
        "sum()", "len()", "round()",
        "zip_longest", "groupby",
    ],
    "Copie et référence": [
        ".copy()", "deepcopy()",
        "affectation =",
    ],
    "Conditionnels": [
        "ternaire", "any()", "all()",
    ],
    "Déballage (unpacking)": [
        "* pour listes",
        "** pour dictionnaires",
        "*args/**kwargs",
    ],
    "Namedtuple": [
        "namedtuple()",
        "accès par attribut", "_asdict()",
    ],
    "Fichiers": [
        "with open()", ".read()/.readlines()",
        ".write()/.writelines()",
    ],
    "Assertion et validation": [
        "assert", "isinstance()",
    ],
    "Mathématiques": [
        "abs()", "divmod()",
        "enumerate(start=1)",
    ],
    "Itération avancée": [
        "next()", "iter()", "reversed()",
    ],
    "Déballage variable ignorée": [
        "for _, _, var in iterable",
    ],
}

PATTERNS_INTERMEDIAIRE_PLUS = {
    "Organisation du code": [
        "if __name__ == '__main__'",
        "création de modules",
        "création de packages",
        "imports relatifs", "__all__",
        "alias d'import", "sys.path",
    ],
    "Entrée/Sortie et erreurs": [
        "with (context manager)",
        "try/except/else/finally",
        "raise ValueError",
        "exceptions personnalisées",
        "CSV (reader/writer/DictReader)",
        "JSON (json.load/json.dump)",
        "pathlib.Path",
    ],
    "Fonctions avancées": [
        "lambda", "map()", "filter()",
        "reduce()", "*args", "**kwargs",
        "closure", "partial()",
        "décorateurs simples",
    ],
    "Structures avancées": [
        "namedtuple", "defaultdict",
        "Counter", "deque", "OrderedDict",
        "sets avancés", "shallow/deep copy",
        "structures imbriquées",
        "zip() inversé", "enumerate(start=1)",
        "any()/all()",
    ],
    "Itération avancée": [
        "itérateurs", "générateurs (yield)",
        "expressions génératrices",
        "itertools.count()",
        "itertools.cycle()",
        "itertools.chain()",
        "itertools.product()",
        "itertools.permutations()",
        "itertools.groupby()",
    ],
    "Programmation fonctionnelle": [
        "fonctions pures", "immutabilité",
        "composition de fonctions",
        "functools.reduce()",
        "functools.lru_cache", "récursion",
    ],
    "Gestion de contexte avancée": [
        "contextlib", "contextmanager",
        "closing()", "suppress()",
        "context managers imbriqués",
    ],
    "Validation et assertions": [
        "assert", "isinstance()",
        "hasattr()", "callable()",
    ],
    "Chaînes avancées": [
        "f-strings avancées", ".format()",
        ".partition()/.rpartition()",
        ".translate()", ".maketrans()",
    ],
    "Manipulation de dates": [
        "datetime", "timedelta",
        ".strftime()", ".strptime()",
    ],
    "Tests simples": [
        "doctest", "unittest basique",
    ],
}

PATTERNS_POO = {
    "Base de la POO": [
        "class", "__init__", "self",
        "attributs d'instance",
        "attributs de classe",
        "méthodes d'instance",
        "__str__", "__repr__", "__eq__",
        "__lt__/__le__/__gt__/__ge__",
    ],
    "Héritage": [
        "héritage simple", "super()",
        "héritage multiple", "MRO",
        "isinstance()/issubclass()",
        "surcharge de méthode",
        "extension de méthode",
    ],
    "Méthodes spéciales (dunder)": [
        "__len__", "__getitem__/__setitem__",
        "__iter__/__next__", "__call__",
        "__enter__/__exit__",
        "__add__/__sub__/__mul__",
        "__bool__", "__hash__", "__slots__",
    ],
    "Contrôle d'accès": [
        "encapsulation", "_attribut (protected)",
        "__attribut (private)", "@property",
        "@setter", "@deleter",
        "getters/setters",
    ],
    "Méthodes de classe et statiques": [
        "@classmethod", "@staticmethod",
        "constructeurs alternatifs",
        "variables de classe",
    ],
    "Patterns avancés": [
        "composition", "agrégation",
        "classe abstraite (ABC)",
        "@abstractmethod", "polymorphisme",
        "duck typing", "mixin",
        "factory pattern", "singleton",
        "__new__",
    ],
    "Gestion d'erreurs en POO": [
        "exceptions personnalisées",
        "raise dans les méthodes",
        "context managers dans les classes",
    ],
    "Comparaison et représentation": [
        "__eq__ et __hash__", "frozenset",
        "dataclasses", "@dataclass(frozen=True)",
        "__post_init__",
    ],
}

PATTERNS_EXPERT = {
    "Création": [
        "Singleton", "Factory Method",
        "Abstract Factory", "Builder",
        "Prototype",
    ],
    "Structure": [
        "Adapter", "Bridge", "Composite",
        "Decorator", "Facade",
        "Flyweight", "Proxy",
    ],
    "Comportement": [
        "Chain of Responsibility", "Command",
        "Interpreter", "Iterator",
        "Mediator", "Memento", "Observer",
        "State", "Strategy",
        "Template Method", "Visitor",
    ],
}

PATTERNS_BY_SUBLEVEL = {
    "pattern_intermediaire": PATTERNS_INTERMEDIAIRE,
    "pattern_intermediaire_plus": PATTERNS_INTERMEDIAIRE_PLUS,
    "pattern_poo": PATTERNS_POO,
    "pattern_expert": PATTERNS_EXPERT,
}


# ---------------------------------------------------------------------------
# Screen builder
# ---------------------------------------------------------------------------

def build_pattern_screen(page: ft.Page, session: SessionState) -> ft.View:
    t = get_translations(session.interface_language)
    c = get_colors(session.theme)

    patterns_data = PATTERNS_BY_SUBLEVEL.get(session.current_sublevel, {})
    categories = list(patterns_data.keys())
    sublevel_label = getattr(session, "_current_sublevel_label", session.current_sublevel)

    selected = {"category": categories[0] if categories else ""}

    # --- Right column: pattern buttons ---
    patterns_col = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)

    # --- Category button refs for highlight toggling ---
    cat_buttons: dict[str, ft.ElevatedButton] = {}

    def _fill_patterns(category: str) -> None:
        patterns_col.controls.clear()
        for p in patterns_data.get(category, []):
            patterns_col.controls.append(
                ft.ElevatedButton(
                    content=p,
                    bgcolor=c["btn_bg"],
                    color=c["btn_text"],
                    on_click=lambda _, cat=category, pat=p: _select_pattern(cat, pat),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                )
            )

    def _select_category(category: str) -> None:
        selected["category"] = category
        for name, btn in cat_buttons.items():
            if name == category:
                btn.bgcolor = c["accent"]
                btn.color = "#ffffff"
            else:
                btn.bgcolor = c["btn_bg"]
                btn.color = c["btn_text"]
        _fill_patterns(category)
        page.update()

    def _select_pattern(category: str, pattern: str) -> None:
        session.current_pattern_category = category
        session.current_pattern = pattern
        page.go("/exercise")

    # --- Left column: category buttons ---
    cats_col = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)
    for cat in categories:
        is_first = cat == selected["category"]
        btn = ft.ElevatedButton(
            content=cat,
            bgcolor=c["accent"] if is_first else c["btn_bg"],
            color="#ffffff" if is_first else c["btn_text"],
            on_click=lambda _, cat=cat: _select_category(cat),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        )
        cat_buttons[cat] = btn
        cats_col.controls.append(btn)

    # Initialize patterns for first category
    if selected["category"]:
        _fill_patterns(selected["category"])

    return ft.View(
        route="/pattern",
        bgcolor=c["bg"],
        controls=[
            ft.AppBar(
                title=ft.Text(f"Pattern — {sublevel_label}", color=c["text"]),
                bgcolor=c["bg"],
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/sublevel"),
                    tooltip=t["back"],
                    icon_color=c["accent"],
                ),
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        t["choose_category"],
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=c["accent"],
                                    ),
                                    ft.Divider(height=1, color=c["border"], thickness=1),
                                    cats_col,
                                ],
                                spacing=8,
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            width=170,
                            bgcolor=c["card_bg"],
                            border_radius=10,
                            padding=10,
                            border=ft.border.all(1, c["border"]),
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        t["choose_pattern"],
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=c["accent"],
                                    ),
                                    ft.Divider(height=1, color=c["border"], thickness=1),
                                    patterns_col,
                                ],
                                spacing=8,
                                expand=True,
                            ),
                            expand=True,
                            bgcolor=c["card_bg"],
                            border_radius=10,
                            padding=10,
                            border=ft.border.all(1, c["border"]),
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    expand=True,
                ),
                expand=True,
                padding=ft.padding.all(16),
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
