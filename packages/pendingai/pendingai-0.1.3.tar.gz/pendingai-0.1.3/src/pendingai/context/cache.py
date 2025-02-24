#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import typer
from pydantic import BaseModel, ValidationError
from yaml import safe_load

from pendingai import Environment, __appname__
from pendingai.auth.models import AccessToken

logger: logging.Logger = logging.getLogger("root")


class Cache(BaseModel):
    """
    Cache file data model.
    """

    access_token: Optional[AccessToken] = None

    @classmethod
    def load(cls, environment: Environment) -> "Cache":
        """
        Load cache runtime based on a given environment.

        Args:
            environment (Environment): Runtime environment.

        Returns:
            Cache: Loaded class instance.
        """
        try:
            contents: Dict[str, Any] = {}
            file: str = f".{environment.value}.cache"
            path: Path = Path(typer.get_app_dir(__appname__, force_posix=True)) / file
            if not path.parent.exists():
                logger.info(f"Initialising cache directory: {path.parent}")
                path.parent.mkdir()
            if not path.parent.is_dir():
                logger.warning(f"Invalid cache directory: {path.parent}")
                logger.warning("Unable to initialise cache instance, using default.")
                return cls.model_validate(contents)
            if path.exists():
                if path.is_file():
                    return cls.model_validate(safe_load(path.open()))
                logger.warning(f"Invalid cache filepath: {path}")
                logger.warning("Unable to initialise cache instance, using default.")
            return cls.model_validate(contents)

        except ValidationError:
            logger.warning("App cache contains malformed data, clearing invalid data.")
            logger.warning("Unable to initialise cache instance, using default.")
            return cls.model_validate({})

    def save(self, environment: Environment) -> None:
        """
        Save cache contents to file.

        Args:
            environment (Environment): Saved cache environment.
        """
        file: str = f".{environment.value}.cache"
        path: Path = Path(typer.get_app_dir(__appname__, force_posix=True)) / file
        with path.open("w") as fp:
            fp.write(self.model_dump_json())

    def delete(self, environment: Environment) -> None:
        """
        Delete cache content file.

        Args:
            environment (Environment): Cache environment being deleted.
        """
        file: str = f".{environment.value}.cache"
        path: Path = Path(typer.get_app_dir(__appname__, force_posix=True)) / file
        path.unlink(missing_ok=True)
