#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from enum import Enum, unique
from io import TextIOWrapper
from pathlib import Path
from typing import Any, List, Optional

from rich.prompt import Confirm
from typer import BadParameter, Context, Exit, FileText, Option
from typing_extensions import Annotated

_JOB_TAG_LIMIT: int = 5
_JOB_TAG_REGEX: str = r"^[\w-]{,16}$"
_TARGET_LIMIT: int = 10_000
_TARGET_REGEX: str = r"^[A-Za-z0-9\(\)+-=#%+@\/\\\[\]]+$"
_IDS_LIMIT: int = 10_000
_IDS_REGEX: str = r"^[a-f\d]{24}$"


@unique
class Status(str, Enum):
    """
    Job status enum value choices.
    """

    SUBMITTED = "submitted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


def _input_targets_list_callback(value: List[str]) -> List[str]:
    """
    Input targets list validation callback. Check the length of the list
    and check the string pattern for each individual target.

    Args:
        value (List[str]): Input target list.

    Raises:
        BadParameter: Targets list exceeds `_TARGET_LIMIT`.
        BadParameter: Targets do not match `_TARGET_REGEX`.

    Returns:
        List[str]: Input target list.
    """
    if len(value) > _TARGET_LIMIT:
        raise BadParameter(f"Exceeded job limit of {_TARGET_LIMIT}.")
    targets: list[str] = []
    for target_value in value:
        if not re.match(_TARGET_REGEX, target_value):
            raise BadParameter("Query structures must be a valid SMILES.")
        if len(target_value) > 512:
            print(
                f"Query structures must be less than 512 chars, skipping: {target_value}"
            )
            continue
        targets.append(target_value)
    return targets


def _input_targets_file_callback(value: Optional[TextIOWrapper]) -> List[str]:
    """
    Input targets file validation callback. Check the length of the file
    and check the string pattern for each individual target.

    Args:
        value (Optional[TextIOWrapper]): Input target file.

    Raises:
        BadParameter: Targets file exceeds `_TARGET_LIMIT`.
        BadParameter: Targets do not match `_TARGET_REGEX`.

    Returns:
        List[str]: Input target file converted to a list.
    """
    line_values: List[str] = []
    if value is not None:
        for line_no, line_value in enumerate(value):
            if line_no > _TARGET_LIMIT:
                raise BadParameter(f"Exceeded job limit of {_TARGET_LIMIT}.")
            line_values.append(line_value.strip())
            if not re.match(_TARGET_REGEX, line_values[-1]):
                raise BadParameter("Query structures must be a valid SMILES.")
            if len(line_values[-1]) > 512:
                print(
                    f"Query structures must be less than 512 chars, skipping: {line_values[-1]}"
                )
                line_values.pop()
    return line_values


def _input_id_list_callback(ctx: Context, value: List[str]) -> List[str]:
    """
    Input IDs list validation callback. Check the length of the list
    and check the string pattern for each individual IDs.

    Args:
        value (List[str]): Input IDs list.

    Raises:
        BadParameter: IDs list exceeds `_IDS_LIMIT`.
        BadParameter: IDs do not match `_IDS_REGEX`.

    Returns:
        List[str]: Input IDs list.
    """
    if len(value) > _IDS_LIMIT:
        raise BadParameter(f"Exceeded request limit of {_IDS_LIMIT}.")
    for id_value in value:
        if not re.match(_IDS_REGEX, id_value):
            raise BadParameter("Requested IDs have invalid format.")
    return value


def _input_id_file_callback(value: Optional[TextIOWrapper]) -> List[str]:
    """
    Input IDs file validation callback. Check the length of the file
    and check the string pattern for each individual ID.

    Args:
        value (Optional[TextIOWrapper]): Input IDs file.

    Raises:
        BadParameter: IDs file exceeds `_IDS_LIMIT`.
        BadParameter: IDs do not match `_IDS_REGEX`.

    Returns:
        List[str]: Input IDs file converted to a list.
    """
    line_values: List[str] = []
    if value is not None:
        for line_no, line_value in enumerate(value):
            if line_no > _IDS_LIMIT:
                raise BadParameter(f"Exceeded request limit of {_IDS_LIMIT}.")
            line_values.append(line_value.strip())
            if not re.match(_IDS_REGEX, line_values[-1]):
                raise BadParameter("Requested IDs have invalid format.")
    return line_values


def _library_callback(ctx: Context, libraries: Any) -> List[str]:
    """
    Check all building block library IDs are valid.

    Args:
        ctx (Context): Runtime app context.
        libraries (Any, optional): Building block library IDs.

    Raises:
        BadParameter: Library ID has invalid format.

    Returns:
        List[str]: Given library ID parameter values.
    """
    if libraries is not None:
        ids: List[str] = [x.id for x in ctx.obj.controller.get_libraries()]
        if isinstance(libraries, str) and libraries in ids:
            return [libraries]
        elif isinstance(libraries, str):
            raise BadParameter(f"Building block library is not available: {libraries}")
        elif isinstance(libraries, list):
            for lib in libraries:
                if not isinstance(lib, str) or lib not in ids:
                    raise BadParameter(f"Building block library is not available: {lib}")
            return libraries
        raise BadParameter("Invalid parameter type.")
    return []


def _engine_callback(ctx: Context, engine: Any) -> Optional[str]:
    """
    Check a retrosynthesis engine ID is valid.

    Args:
        ctx (Context): Runtime app context.
        engine (Any, optional): Retrosynthesis engine ID.

    Raises:
        typer.BadParameter: Engine ID has invalid format.

    Returns:
        Optional[str]: Given engine ID parameter value.
    """
    if engine is not None and isinstance(engine, str):
        ids: List[str] = [x.id for x in ctx.obj.controller.get_engines()]
        if engine not in ids:
            raise BadParameter(f"Retrosynthesis engine is not available: {engine}")
        return engine
    return None


def _eng_id_pagination_callback(ctx: Context, eng_id: Optional[str]) -> Optional[str]:
    """
    Check a retrosynthesis engine ID is valid.

    Args:
        ctx (Context): Runtime app context.
        eng_id (str, optional): Retrosynthesis engine ID.

    Raises:
        BadParameter: Engine ID is invalid.

    Returns:
        Optional[str]: Retrosynthesis engine ID.
    """
    if eng_id:
        ids: List[str] = [x.id for x in ctx.obj.controller.get_engines()]
        if eng_id not in ids:
            raise BadParameter("Retrosynthesis engine is not available.")
    return eng_id


def _lib_id_pagination_callback(ctx: Context, lib_id: Optional[str]) -> Optional[str]:
    """
    Check a building block library ID is valid.

    Args:
        ctx (Context): Runtime app context.
        lib_id (str, optional): Building block library ID.

    Raises:
        BadParameter: Library ID is invalid.

    Returns:
        Optional[str]: Building block library ID.
    """
    if lib_id:
        ids: List[str] = [x.id for x in ctx.obj.controller.get_libraries()]
        if lib_id not in ids:
            raise BadParameter("Building block library is not available.")
    return lib_id


def _tags_callback(value: List[str]) -> List[str]:
    """
    Job tags list validation callback. Check the length of the tags
    and check the string pattern for each individual tag.

    Args:
        value (List[str]): Input job tag list.

    Raises:
        BadParameter: Tags list exceeds `_JOB_TAG_LIMIT`.
        BadParameter: Tags do not match `_JOB_TAG_REGEX`.

    Returns:
        List[str]: Input job tag list.
    """
    if len(value) > _JOB_TAG_LIMIT:
        raise BadParameter(f"Maximum number of tags per job is {_JOB_TAG_LIMIT}.")
    for tag_value in value:
        if not re.match(_JOB_TAG_REGEX, tag_value):
            raise BadParameter("Tags must be alpha-numeric with underscores or dashes.")
    return value


def _job_tags_callback(value: List[str]) -> List[str]:
    """
    Job tags list validation callback. Check the length of the tags
    and check the string pattern for each individual tag.

    Args:
        value (List[str]): Input job tag list.

    Raises:
        BadParameter: Tags list exceeds `_JOB_TAG_LIMIT`.
        BadParameter: Tags do not match `_JOB_TAG_REGEX`.

    Returns:
        List[str]: Input job tag list.
    """
    if len(value) > 3:
        raise BadParameter(f"Maximum number of tags per job is {3}.")
    for tag_value in value:
        if not re.match(_JOB_TAG_REGEX, tag_value):
            raise BadParameter("Tags must be alpha-numeric with underscores or dashes.")
    return value


def _output_ids_filepath_callback(value: Path) -> Path:
    prompt: str = f"[yellow]? Are you sure you want to overwrite the file '{value}'"
    if value.exists() and not Confirm.ask(prompt):
        raise Exit(0)
    return value


def _output_results_filepath_callback(value: Path) -> Path:
    prompt: str = f"[yellow]? Are you sure you want to overwrite the file '{value}'"
    if value is not None and value.exists() and not Confirm.ask(prompt):
        raise Exit(0)
    return value


class Options:
    """
    Namespace for shared command options.
    """

    InputTargetsList = Annotated[
        List[str],
        Option(
            "--smiles",
            "-s",
            help="SMILES of the query structure. SMARTS are unsupported.",
            callback=_input_targets_list_callback,
        ),
    ]
    InputTargetsFile = Annotated[
        FileText,
        Option(
            "--input-file",
            "-i",
            help="Line-delimited file with SMILES of query structures.",
            callback=_input_targets_file_callback,
            exists=True,
        ),
    ]
    InputIdList = Annotated[
        List[str],
        Option(
            "--id",
            help="Retrosynthesis job IDs. An ID becomes available upon submitting a job. IDs can also be retrieved when listing jobs with <pendingai retro list>.",
            callback=_input_id_list_callback,
        ),
    ]
    InputIdFile = Annotated[
        Optional[FileText],
        Option(
            "--input-file",
            "-i",
            help="Line-delimited file with retrosynthesis job IDs.",
            callback=_input_id_file_callback,
            exists=True,
        ),
    ]
    OutputIdFile = Annotated[
        Path,
        Option(
            "--output-file",
            "-o",
            help="Output filepath for writing line-delimited job IDs.",
            callback=_output_ids_filepath_callback,
            exists=False,
            writable=True,
        ),
    ]
    OutputFile = Annotated[
        Optional[Path],
        Option(
            "--output-file",
            "-o",
            help="Output filepath for writing command results.",
            callback=_output_results_filepath_callback,
            exists=False,
            writable=True,
        ),
    ]
    RenderJson = Annotated[
        bool,
        Option(
            "--json",
            help="Render output as JSON.",
            is_flag=True,
        ),
    ]
    RouteNumber = Annotated[
        Optional[int],
        Option(
            "--route-number",
            "-n",
            help="Individual route to display.",
        ),
    ]

    class Pagination:
        """
        Namespace for pagination options.
        """

        PageNumber = Annotated[
            int,
            Option(
                "--page",
                help="Page number being fetched.",
                show_choices=False,
                show_default=False,
                metavar="INTEGER",
                min=1,
            ),
        ]
        PageSize = Annotated[
            int,
            Option(
                "--page-size",
                help="Number of results per page.",
                show_default=False,
                metavar="INTEGER",
                min=1,
                max=25,
            ),
        ]
        Status = Annotated[
            Optional[Status],
            Option(
                "--status",
                help="Optional filter for matching status.",
            ),
        ]
        EngId = Annotated[
            Optional[str],
            Option(
                "--eng-id",
                help="Optional filter for matching retrosynthesis engine.",
                callback=_eng_id_pagination_callback,
            ),
        ]
        LibId = Annotated[
            Optional[str],
            Option(
                "--lib-id",
                help="Optional filter for matching building block library.",
                callback=_lib_id_pagination_callback,
            ),
        ]

    class Parameters:
        """
        Namespace for retrosynthesis parameter options.
        """

        EngineId = Annotated[
            Optional[str],
            Option(
                "--eng-id",
                help="Retrosynthesis engine ID. Defaults to primary engine.",
                callback=_engine_callback,
            ),
        ]
        LibraryIds = Annotated[
            Optional[List[str]],
            Option(
                "--lib-id",
                help="Building block library IDs. Defaults to all available libraries.",
                callback=_library_callback,
            ),
        ]
        NumRoutes = Annotated[
            int,
            Option(
                "--num-routes",
                help="Maximum number of retrosynthetic routes to generate. Defaults to 20.",
                show_default=False,
                metavar="INTEGER",
                min=1,
                max=50,
            ),
        ]
        ProcessingTime = Annotated[
            int,
            Option(
                "--time-limit",
                help="Maximum processing time in seconds. Defaults to 300.",
                show_default=False,
                metavar="INTEGER",
                min=60,
                max=600,
            ),
        ]
        ReactionLimit = Annotated[
            int,
            Option(
                "--reaction-limit",
                help="Maximum number of times a specific reaction can appear in generated retrosynthetic routes.",
                show_default=False,
                metavar="INTEGER",
                min=1,
                max=25,
            ),
        ]
        BlockLimit = Annotated[
            int,
            Option(
                "--block-limit",
                help="Maximum number of times a building block can appear in a single retrosynthetic route.",
                show_default=False,
                metavar="INTEGER",
                min=1,
                max=25,
            ),
        ]
        JobTags = Annotated[
            List[str],
            Option(
                "--tag",
                help="Up to 3 job tags.",
                callback=_job_tags_callback,
            ),
        ]
        Tags = Annotated[
            List[str],
            Option(
                "--tag",
                help=f"Up to {_JOB_TAG_LIMIT} job tags.",
                callback=_tags_callback,
            ),
        ]
