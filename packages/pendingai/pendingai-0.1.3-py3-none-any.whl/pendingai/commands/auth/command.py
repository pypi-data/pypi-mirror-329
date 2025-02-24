#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import Callable, Dict, Optional

from pendingai.auth.flows import DeviceAuthorizationFlow, RefreshTokenFlow
from pendingai.auth.models import AccessToken
from rich.console import Console
from typer import Context, Exit, Typer

command: Typer = Typer(
    name="auth",
    no_args_is_help=True,
    add_completion=False,
    context_settings={"max_content_width": 90},
)

console: Console = Console(width=90)
print: Callable[..., None] = console.print


@command.callback()
def _callback(ctx: Context) -> None:
    """
    Authenticate with the Pending AI platform.
    """


@command.command("login")
def _login(ctx: Context) -> None:
    """
    Login to a Pending AI account. Device authorization will open a
    web browser window.

    For any account problems, contact support via <pendingai support>.
    """
    if ctx.obj.api_key is not None:
        print("[yellow]![/] Optional API key provided.")
        return

    auth_params: Dict[str, str] = ctx.obj.config.auth.model_dump()

    if ctx.obj.cache.access_token is not None:
        access_token: Optional[AccessToken] = ctx.obj.cache.access_token
        if access_token is not None and not access_token.is_expired():
            user_email: str = access_token.get_email()
            print("[yellow]! Authentication already complete.")
            print(f"[green]✓[/] Logged in as [b]{user_email}[/]")
            return
        else:
            refresh_flow: RefreshTokenFlow = RefreshTokenFlow(**auth_params)
            print("[yellow]! Authentication has expired, refreshing access.")
            if access_token is not None:
                access_token = refresh_flow.refresh(access_token.refresh_token)
            if access_token is None:
                print("[yellow]! Failed to refresh access, re-authenticating now.")
            else:
                print(f"[green]✓[/] Logged in as [b]{access_token.get_email()}[/]")
                ctx.obj.cache.access_token = access_token
                ctx.obj.cache.save(ctx.obj.environment)
                return

    device_auth: DeviceAuthorizationFlow = DeviceAuthorizationFlow(**auth_params)
    ctx.obj.cache.access_token = device_auth.authorize()
    ctx.obj.cache.save(ctx.obj.environment)
    print("[green]✓[/] Authentication complete.")
    print(f"[green]✓[/] Logged in as [b]{ctx.obj.cache.access_token.get_email()}[/]")


@command.command("logout")
def _logout(ctx: Context) -> None:
    """
    Logout of a Pending AI account. Removes locally cached
    authentication details.
    """
    if ctx.obj.cache.access_token:
        email: str = ctx.obj.cache.access_token.get_email()
        ctx.obj.cache.delete(ctx.obj.environment)
        print(f"[green]✓[/] Logged out [b]{email}[/]")
    else:
        print("[yellow]! Already logged out.")


@command.command("refresh", hidden=True)
def _refresh(ctx: Context) -> None:
    """
    TODO: Finish documentation.
    """


@command.command("status", hidden=True)
def _status(ctx: Context) -> None:
    """
    TODO: Finish documentation.
    """


@command.command("token")
def _token(ctx: Context) -> None:
    """
    Print the authentication token Pending AI uses for an account.
    """
    if ctx.obj.cache is None or ctx.obj.cache.access_token is None:
        print(
            "[yellow]! Use [b]<pendingai auth login>[/] to generate an authentication token."
        )
        raise Exit(1)
    elif ctx.obj.cache.access_token.access_token is None:
        print(
            "[yellow]! Invalid authentication token; use [b]<pendingai auth logout>[/]."
        )
        raise Exit(1)
    elif ctx.obj.cache.access_token.is_expired():
        print(
            "[yellow]! Authentication token has expired; use [b]<pendingai auth login>[/]."
        )
        raise Exit(1)
    else:
        user_email: str = ctx.obj.cache.access_token.get_email()
        print(f"[green]✓[/] Access token for [b]{user_email}[/]")
        print(f"\b{ctx.obj.cache.access_token.access_token}", soft_wrap=True)
