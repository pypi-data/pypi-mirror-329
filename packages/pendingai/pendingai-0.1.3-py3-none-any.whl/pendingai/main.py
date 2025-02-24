#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import webbrowser
from typing import Optional

import typer
from rich import print
from typer import Exit, Option, Typer, echo
from typing_extensions import Annotated

import pendingai.commands.retrosynthesis.command as retrosynthesis
from pendingai import Environment, __appname__, __version__
from pendingai.commands.auth.command import command as auth_command
from pendingai.context import Context, Namespace

namespace: Namespace = Namespace.load()

logger: logging.Logger = logging.getLogger("root")


app: Typer = Typer(name=__appname__, no_args_is_help=True, add_completion=False)
app.pretty_exceptions_show_locals = False
app.rich_markup_mode = None

app.add_typer(retrosynthesis.app, name=namespace.commands.retrosynthesis.subcommand)
app.add_typer(auth_command)


def _version_callback(value: bool) -> None:
    """Display app version and exit."""
    if value:
        echo(f"{__appname__}/{__version__}")
        raise Exit(0)


@app.callback()
def _callback(
    ctx: typer.Context,
    version: Annotated[
        bool,
        Option(
            "--version",
            is_flag=True,
            is_eager=True,
            callback=_version_callback,
            help="Show the application version and exit.",
        ),
    ] = False,
    verbosity: Annotated[
        int,
        Option(
            "-v",
            "--verbose",
            hidden=True,
            count=True,
            help="Verbose flag for stdout log-level.",
        ),
    ] = 0,
    environment: Annotated[
        Environment,
        Option(
            "--env",
            "-e",
            hidden=True,
            show_default=False,
            envvar="PENDINGAI_ENVIRONMENT",
            help="Selectable runtime deployment server.",
        ),
    ] = Environment.PRODUCTION,
    api_key: Annotated[
        Optional[str],
        Option(
            "--api-key",
            hidden=True,
            envvar="PENDINGAI_API_KEY",
            help="Session token alternative API key.",
        ),
    ] = None,
) -> None:
    """
    Pending AI Command-Line Interface.

    Cheminformatics services offered by this CLI are accessible through an
    API integration with Pending AI servers. An authenticated session is
    required for use; see <pendingai auth>. More information is available
    with <pendingai docs>.
    """
    logger.setLevel(40 - min(verbosity, 4) * 10)
    ctx.obj = Context(
        app_name=__appname__,
        environment=environment,
        api_key=api_key,
        subcommand=ctx.invoked_subcommand,
    )


@app.command("docs")
def docs(ctx: typer.Context) -> None:
    """
    Open the Pending AI documentation page in a web browser.
    """
    prompt: str = "[bold]Press Enter[/] to open %s in your browser. "
    print(prompt % namespace.docs_redirect_url, end="")
    input()
    webbrowser.open_new_tab(namespace.docs_redirect_url)


@app.command("support")
def support(ctx: typer.Context) -> None:
    """
    Open the Pending AI support page in a web browser.
    """
    print("[yellow]! Lodge a ticket via email: [blue underline]support@pending.ai")
    print("[yellow]- Refer to [b]<pendingai docs>[/] for expected errors.")
    print("[yellow]- Provide information such as the command and any output provided.")
    print("[yellow]- Please use the same email address registered with your account.")


if __name__ == "__main__":
    app()
