#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel, ValidationError
from yaml import safe_load

from pendingai import Environment


class _Command(BaseModel):
    """
    Namespace command data model.
    """

    subcommand: str
    api_domain: str


class _CommandMapping(BaseModel):
    """
    Namespace command mapping data model.
    """

    retrosynthesis: _Command


class Namespace(BaseModel):
    """
    Namespace data model.
    """

    commands: _CommandMapping
    support_redirect_url: str
    docs_redirect_url: str
    labs_redirect_url: str

    @classmethod
    def load(cls) -> "Namespace":
        """
        Custom model loader from static file.

        Raises:
            RuntimeError: Invalid configuration file.

        Returns:
            Namespace: Loaded class instance.
        """
        try:
            path: Path = Path(__file__).parent / "globals.yml"
            contents: Dict[str, Any] = safe_load(path.open())
            return cls.model_validate(contents)

        except (ValidationError, FileExistsError, FileNotFoundError) as ex:
            raise RuntimeError("Invalid application state.") from ex


class _ApiEnvironment(BaseModel):
    """
    Config api environment model.
    """

    domain: str


class _AuthEnvironment(BaseModel):
    """
    Config authentication environment data model.
    """

    domain: str
    client_id: str
    audience: str


class Config(BaseModel):
    """
    Config data model.
    """

    api: _ApiEnvironment
    auth: _AuthEnvironment
    environment: Environment

    @classmethod
    def load(cls, environment: Environment = Environment.PRODUCTION) -> "Config":
        """
        Custom model loader from static file for a specific environment.

        Args:
            environment (Environment, optional): Instance environment.

        Raises:
            RuntimeError: Invalid configuration file.

        Returns:
            Namespace: Loaded class instance.
        """
        try:
            path: Path = Path(__file__).parent / f"config.{environment.value}.yml"
            contents: Dict[str, Any] = safe_load(path.open())
            contents["environment"] = environment
            return cls.model_validate(contents)

        except (ValidationError, FileExistsError, FileNotFoundError) as ex:
            raise RuntimeError("Invalid application state.") from ex
