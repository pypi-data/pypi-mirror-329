#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class Engine(BaseModel):
    """
    Retrosynthesis engine data model.
    """

    id: str
    name: str
    last_alive: datetime
    default: bool


class Library(BaseModel):
    """
    Retrosynthesis library data model.
    """

    id: str
    name: str
    version: str
    # available_from: datetime # NOTE: Masked from JSON output


class _Parameters(BaseModel):
    """
    Retrosynthesis job parameters data model.
    """

    retrosynthesis_engine: str
    building_block_libraries: List[str]
    number_of_routes: int
    processing_time: int
    reaction_limit: int
    building_block_limit: int


class _Step(BaseModel):
    """
    Retrosynthesis job route step data model.
    """

    order: int
    reaction_smiles: str


class Route(BaseModel):
    """
    Retrosynthesis job route data model.
    """

    summary: str
    building_blocks: List[Dict]
    steps: List[_Step]


class Job(BaseModel):
    """
    Retrosynthesis job data model.
    """

    id: str
    query: str
    status: str
    created: datetime
    updated: datetime
    routes: List[Route]
    parameters: _Parameters
    tags: Optional[List[str]]


class JobPage(BaseModel):
    """
    Retrosynthesis job paginated result data model.
    """

    results: List[Job]
    count: int
    limit: int


class NewJob(BaseModel):
    """
    Retrosynthesis job submission data model.
    """

    id: str
    smiles: str
