#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from rich import print
from typer import Context, Exit

from pendingai.client import Client
from pendingai.context import Namespace

namespace: Namespace = Namespace.load()


def append_client_context(ctx: Context) -> None:
    """
    Update the app runtime context with an initialised client. Required
    context fields are validated and the command `/alive` endpoint is
    hit to confirm the service is available.

    Args:
        ctx (Context): App runtime context.
        command (str): Command with matching client domain.
    """

    # Check profile session token exists
    if ctx.obj.session_token is None:
        print("[yellow]! No authenticated session found, try logging in.")
        raise Exit(0)

    # Check session token is not expired
    if ctx.obj.api_key is None and ctx.obj.cache.access_token.is_expired():
        print("[yellow]! Authenticated session has expired, try logging in.")
        raise Exit(0)

    # Initialise only the retrosynthesis command
    ctx.obj.client = Client(
        domain=ctx.obj.config.api.domain,
        subdomain=namespace.commands.retrosynthesis.api_domain,
        token=ctx.obj.session_token,
    )

    # Check client is reachable
    if ctx.obj.client.get("/alive").status_code != 200:
        print(
            f"[red]\u2717 Pending AI's <{ctx.command.name}> Service is currently",
            "[red]unavailable, try again shortly or contact support with",
            "[red][b]<pendingai support>[/].",
        )
        raise Exit(1)
