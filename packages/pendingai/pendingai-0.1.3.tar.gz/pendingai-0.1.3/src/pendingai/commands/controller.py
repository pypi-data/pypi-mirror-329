#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
from abc import ABC
from typing import Callable

from httpx import RequestError
from pydantic import ValidationError
from rich import print
from typer import BadParameter, Context, Exit


def capture_controller_errors(method: Callable) -> Callable:
    """
    Capture exceptions and errors that occur when interfacing with
    a command controller instance.

    Args:
        method (Callable): Controller method with error handling.

    Returns:
        Callable: Decorator method with controller error handling.
    """

    def controller_method(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except BadParameter as ex:
            raise ex
        except ValidationError:
            print(
                "[red]\u2717",
                "[red]Unexpected response data from the service, contact support",
                "[red]for more information.",
            )
        except RequestError:
            print(
                "[red]\u2717",
                "[red]Service request failed due to network or data transport",
                "[red]errors, try again or see the relevant documentation.",
            )
        except Exit as e:
            raise e
        except Exception:
            print(
                "[red]\u2717",
                "[red]Unexpected error encountered by the service, contact support",
                "[red]for more information.",
            )
        sys.exit(1)

    return controller_method


class Controller(ABC):
    """
    Abstract superclass for interfacing with command-specific logic.

    Attributes:
        ctx (typer.Context): Runtime application context instance.
    """

    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
