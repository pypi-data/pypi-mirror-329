#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field, model_validator

from pendingai import Environment
from pendingai.client import Client
from pendingai.commands.controller import Controller
from pendingai.context.cache import Cache
from pendingai.context.config import Config


class Context(BaseModel):
    """
    Runtime context data model for typer object state.
    """

    app_name: str
    environment: Environment
    subcommand: str
    api_key: Optional[str] = None
    client: Optional[Client] = None
    cache: Cache = None  # type: ignore
    config: Config = None  # type: ignore
    controller: Controller = None  # type: ignore

    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def init_computed_fields(self) -> "Context":
        """
        Initialise null-defined context fields on startup.
        """
        self.cache = Cache.load(self.environment)
        self.config = Config.load(self.environment)
        return self

    @computed_field  # type: ignore
    @property
    def session_token(self) -> Optional[str]:
        """
        Runtime session token determined by the api key or access token.
        """
        if self.api_key:
            return self.api_key
        if self.cache.access_token:
            return self.cache.access_token.access_token
        return None
