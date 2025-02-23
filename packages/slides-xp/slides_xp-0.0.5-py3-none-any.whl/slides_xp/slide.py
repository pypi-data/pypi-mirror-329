import importlib
import importlib.util
import sys
import pyhtml as p
from pathlib import Path, PosixPath

from slides_xp.markdown import render_markdown
from slides_xp.util import slides_list


def python_slide(file: Path) -> p.Tag:
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    module_name = f"slides_xp.temp.{file.name.removesuffix('.py')}"

    # Add rule file's directory to the module search path, so that imports
    # work as-expected
    sys.path.append(str(file.parent.absolute()))
    # Now begin the import
    spec = importlib.util.spec_from_file_location(module_name, file)
    if spec is None:
        raise ImportError(f"Import spec for file '{file}' was None")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    if spec.loader is None:
        raise ImportError(f"Spec loader for file '{file}' was None")

    # Any exceptions this raises get caught by the calling code
    try:
        spec.loader.exec_module(module)
    except BaseException as e:
        e.add_note(
            f"This exception occurred during execution of file "
            f"{file}. It is unlikely to be an issue with Slides-XP."
        )
        raise e

    try:
        render_fn = module.render
    except AttributeError as e:
        raise AttributeError(
            f"Python slide '{file}' does not have a `render` function"
        ) from e
    if not callable(render_fn):
        raise TypeError("Python slide's `render` attribute is not callable")

    return render_fn()  # type: ignore


def markdown_slide(file: Path) -> p.Tag:
    return p.div(class_="slide-content")(
        p.DangerousRawHtml(render_markdown(file.read_text()))
    )


def slide(file_path: Path, file_url: PosixPath) -> p.html:
    slides = list(slides_list(file_path.parent))

    curr_index = slides.index(file_path)

    first = f"'{file_url.parent / slides[0].name}'" if len(slides) else "null"
    prev = (
        f"'{file_url.parent / slides[curr_index - 1].name}'"
        if curr_index > 0
        else "null"
    )
    next = (
        f"'{file_url.parent / slides[curr_index + 1].name}'"
        if curr_index < len(slides) - 1
        else "null"
    )

    if file_path.suffix == ".py":
        rendered = python_slide(file_path)
    elif file_path.suffix == ".md":
        rendered = markdown_slide(file_path)
    else:
        raise ValueError(f"File '{file_path}' cannot be rendered")

    return p.html(
        p.head(
            p.title("Slides XP"),
            p.script(src="/javascript/navigator.js", defer=True),
            p.link(href="/css/root.css", rel="stylesheet"),
            p.link(href="/theme/main.css", rel="stylesheet"),
            p.link(href="/theme/slide.css", rel="stylesheet"),
        ),
        p.body(
            p.script(f"""
                window.sxp = {{
                    first: {first},
                    prev: {prev},
                    next: {next},
                }};
            """),
            rendered,
        ),
    )
