from flask import Flask, Blueprint, redirect, send_file, send_from_directory
from pathlib import Path, PosixPath
import pyhtml as p

from slides_xp.picker import Choice, picker
from slides_xp.slide import slide
from slides_xp.util import dir_contains_slides, list_subdirs, slides_list


lib_dir = Path(__file__).parent


def error(code: int, message: str):
    return str(
        p.html(
            p.body(
                p.h1(f"Error {code}"),
                p.p(message),
            )
        )
    ), code


def make_blueprint(name: str, root_dir: Path):
    bp = Blueprint(name, __name__, url_prefix=f"/{name}")

    @bp.get("/", defaults={"path": ""})
    @bp.get("/<path:path>")
    def endpoint(path: str):
        file_path = root_dir / path
        file_url = f"/{name}/{path}".removesuffix("/")
        # Root path must be a parent of `full_path` to prevent escaping the
        # specified directories
        if root_dir not in [file_path, *file_path.parents]:
            return error(403, "Illegal path")
        # 404 if file/dir does not exist
        if not file_path.exists():
            return error(404, "File not found")
        # If file, send it
        if file_path.is_file():
            # Render markdown files as HTML
            if file_path.suffix in [".md", ".py"]:
                return str(slide(file_path, PosixPath(file_url)))
            else:
                return send_file(file_path.absolute())
        elif dir_contains_slides(file_path):
            # Dir with markdown, render a list of slides
            return str(
                picker(
                    str(root_dir),
                    [
                        Choice(p.name, f"{file_url}/{p.name}")
                        for p in slides_list(file_path)
                    ],
                    parent=str(file_path.parent),
                )
            )
        else:
            # Otherwise, dir with no markdown, so render a list of subdirs
            return str(
                picker(
                    str(root_dir),
                    [
                        Choice(p.name, f"{file_url}/{p.name}")
                        for p in list_subdirs(file_path)
                    ],
                    parent=str(file_path.parent),
                )
            )

    return bp


def make_app(paths: list[Path], theme: str | None = None):
    if theme is None:
        theme_dir = lib_dir / "themes" / "default"
    elif Path(theme).is_dir():
        theme_dir = Path(theme)
    elif (lib_dir / "themes" / theme).is_dir():
        theme_dir = lib_dir / "themes" / theme
    else:
        # Invalid theme
        theme_dir = lib_dir / "themes" / "default"

    app = Flask(__name__)

    for path in paths:
        app.register_blueprint(make_blueprint(path.name, path))

    @app.get("/")
    def root():
        """
        Root path.

        If using one path, redirect to it. Otherwise give a choice.
        """
        if len(paths) == 1:
            return redirect(f"/{paths[0].name}/")
        else:
            return str(
                picker(
                    "Slides XP",
                    [Choice(p.name, f"/{p.name}") for p in paths],
                )
            )

    @app.get("/javascript/<path>")
    def scripts(path):
        return send_from_directory(lib_dir / "javascript", path)

    @app.get("/css/<path>")
    def css(path):
        return send_from_directory(lib_dir / "css", path)

    @app.get("/theme/<path>")
    def theme_css(path):
        return send_from_directory(theme_dir, path)

    return app


if __name__ == "__main__":
    app = make_app([Path("temp")])
    app.run(port=3000)
