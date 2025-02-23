from dataclasses import dataclass
import pyhtml as p


@dataclass
class Choice:
    name: str
    url: str


def picker(root: str, choices: list[Choice], parent: str | None = None):
    choices_html = [
        p.div(class_="picker-item")(
            p.a(href=f"{choice.url}")(choice.name),
        )
        for choice in choices
    ]

    if parent is not None:
        choices_html.insert(
            0, p.div(class_="picker-item")(p.a(href=parent)(".."))
        )

    return p.html(
        p.head(
            p.title("Slides XP"),
            p.script(src="/javascript/navigator.js", defer=True),
            p.link(href="/css/root.css", rel="stylesheet"),
            p.link(href="/theme/main.css", rel="stylesheet"),
            p.link(href="/theme/picker.css", rel="stylesheet"),
        ),
        p.body(
            p.h1(root),
            p.div(class_="picker-box")(choices_html),
        ),
    )
