"""
CLI

Main entrypoint to the program.
"""

import click
from pathlib import Path
from slides_xp import make_app


HELP_TEXT = """
sxp

Slides XP CLI
"""


@click.command("sxp", help=HELP_TEXT, options_metavar="<options>")
@click.argument(
    "paths",
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        readable=True,
        path_type=Path,
    ),
    nargs=-1,
    required=True,
)
@click.option(
    "--theme",
    envvar="SXP_THEME",
    help="Theme directory to serve CSS stylesheets from",
)
@click.option(
    "-h",
    "--host",
    default="localhost",
    envvar="HOST",
    help="Port to run server on",
)
@click.option(
    "-p",
    "--port",
    type=int,
    default=3000,
    envvar="PORT",
    help="Port to run server on",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Whether to enable Flask debug mode",
)
def cli(
    paths: tuple[Path, ...],
    *,
    theme: str | None,
    host: str,
    port: int,
    debug: bool,
):
    """
    Entrypoint to CLI.
    """
    app = make_app(list(paths), theme)

    app.run(host, port, debug)
