#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import time
from collections import defaultdict
from typing import Any, Dict, Generator, List, Optional

from httpx import Response
from pendingai.commands.controller import Controller, capture_controller_errors
from pendingai.commands.retrosynthesis.models import (
    Engine,
    Job,
    JobPage,
    Library,
    NewJob,
)
from rich import print
from rich.console import Console
from rich.progress import track
from rich.status import Status
from typer import Exit

_BATCH_SIZE: int = 100


class Retrosynthesis(Controller):
    """
    Retrosynthesis service subcommand controller.
    """

    @capture_controller_errors
    def get_engines(self) -> List[Engine]:
        """
        Get all available retrosynthesis engine instances for a user.

        Returns:
            List[Engine]: Retrosynthesis engines for the user.
        """
        return [
            Engine.model_validate(x) for x in self.ctx.obj.client.get("/engines").json()
        ]

    @capture_controller_errors
    def get_libraries(self) -> List[Library]:
        """
        Get all available retrosynthesis libraries instances for a user.

        Returns:
            List[Library]: Retrosynthesis libraries for the user.
        """
        return [
            Library.model_validate(x)
            for x in self.ctx.obj.client.get("/libraries").json()
        ]

    @capture_controller_errors
    def get_paginated_jobs(
        self,
        *,
        page: int,
        page_size: int,
        status: Optional[str],
        tags: Optional[List[str]],
        console: Console = Console(),
    ) -> JobPage:
        """
        Retrieve a paginated view of retrosynthesis jobs for a set of
        filter arguments.

        Args:
            page (int): Page number to fetch.
            page_size (int): Page size for the response.
            status (str, optional): Filter value for status.
            tags (List[str], optional): Filter value for tags.
            console (Console, optional): Console for user feedback.

        Returns:
            List[Job]: Retrosynthesis job page.
        """
        params: Dict = {
            "page": page,
            "page_size": page_size,
            "tags": tags,
        }
        if status is not None:
            params["status"] = status

        url: str = "/queries"
        res: Response = self.ctx.obj.client.get(url, params=params, skip_errors=True)

        if res.status_code == 200:
            page_data: JobPage = JobPage.model_validate(res.json())
            page_data.results.sort(key=lambda x: x.created)
            return page_data

        elif res.status_code == 404:
            console.print("[yellow]! No results found with the given filter.")
            raise Exit(0)

        else:
            console.print("[red]\u2717 Failed retrieving jobs. Try again shortly.")
            raise Exit(1)

    @capture_controller_errors
    def submit_molecules(
        self,
        targets: List[str],
        *,
        engine: Optional[str],
        libraries: Optional[List[str]],
        number_of_routes: int,
        processing_time: int,
        reaction_limit: int,
        building_block_limit: int,
        tags: List[str],
        console: Console = Console(),
    ) -> Generator[List[NewJob], Any, None]:
        """
        Submit a collection of SMILES molecules with a set of optional
        parameters to an optional retrosynthesis engine.

        Args:
            targets (List[str]): Collection of query structures.
            engine (str, optional): Retrosynthesis engine.
            libraries (List[str], optional): Building block libraries.
            number_of_routes (int): Number of routes parameter.
            processing_time (int): Processing time parameter.
            reaction_limit (int): Reaction limit parameter.
            building_block_limit (int): Building block limit parameter.
            tags (List[str], optional): Up to 5 job tags.
            console (Console, optional): Console for user feedback.

        Raises:
            BadParameter: Invalid number of targets.
            BadParameter: Invalid number of tags.
            NotImplementedError: Unexpected status code.

        Returns:
            List[NewJob]: Submitted molecule queries and created IDs.
        """

        # Build the shared parameter set for submitting the jobs to
        # the retrosynthesis API. Some parameters need to be dynamically
        # added since null fields are not allowed.
        parameters: dict = {
            "tags": tags,
            "parameters": {
                "number_of_routes": number_of_routes,
                "processing_time": processing_time,
                "reaction_limit": reaction_limit,
                "building_block_limit": building_block_limit,
            },
        }

        if engine is not None:
            parameters["parameters"]["retrosynthesis_engine"] = engine
        else:
            console.print("[green]\u2713[/] Added default retrosynthesis engine.")

        if libraries is not None:
            parameters["parameters"]["building_block_libraries"] = libraries
        else:
            console.print("[green]\u2713[/] Added default building block libraries.")

        # Iterate over the targets in mini-capped batches to not over-
        # whelm the API endpoint. A small 0.5 second wait time is also
        # added to reduce load put into the endpoint and other services.
        batches: int = len(targets) // _BATCH_SIZE + 1
        for i in range(0, len(targets), _BATCH_SIZE):
            result: List[NewJob]
            request: Dict = parameters | {"query": targets[i : i + _BATCH_SIZE]}
            batch_size: int = i // _BATCH_SIZE + 1
            with Status(f"Submitting batch {batch_size} of {batches}", console=console):
                response: Response = self.ctx.obj.client.post("/queries", json=request)
                if response.status_code == 200:
                    result = [NewJob.model_validate(x) for x in response.json()]
                elif response.status_code == 202:
                    target_id: str = response.headers.get("Location").split("/")[-2]
                    result = [NewJob(id=target_id, smiles=targets[i])]
                else:
                    print("[red]\u2717[/] Failed to submit jobs, try again shortly.")
                    raise Exit(1)
            console.print(f"[green]\u2713[/] Submitted batch {batch_size} of {batches}")
            yield result
            time.sleep(0.5)

    @capture_controller_errors
    def delete_jobs(
        self,
        ids: List[str],
        *,
        console: Console = Console(),
    ) -> Dict[str, List[str]]:
        """
        Delete a list of input list and file job IDs.

        Args:
            ids (List[str]): Input list with job IDs.
            console (Console, optional): Console for user feedback.

        Returns:
            Tuple[List[str], List[str], List[str]]: Lists of successful,
                missing and failed job ID deletion operations.
        """
        results: Dict[str, List[str]] = defaultdict(list)
        for i in track(ids, "Deleting jobs", transient=True, console=console):
            res: Response = self.ctx.obj.client.delete(f"/queries/{i}", skip_errors=True)
            if res.status_code == 204:
                results["success"].append(i)
            elif res.status_code == 404:
                results["missing"].append(i)
            else:
                results["failure"].append(i)
        return results

    @capture_controller_errors
    def get_job_status(
        self,
        ids: List[str],
        *,
        console: Console = Console(),
    ) -> List[Dict[str, str]]:
        """
        Get the status of a list of input list and file job IDs.

        Args:
            ids (List[str]): Input list with job IDs.
            console (Console, optional): Console for user feedback.

        Returns:
            List[Dict[str, str]]: Status matching the job IDs.
        """
        results: List[Dict] = []
        for i in track(ids, "Check job statuses", transient=True, console=console):
            endpoint: str = f"/queries/{i}/status"
            res: Response = self.ctx.obj.client.get(endpoint, skip_errors=True)
            if res.status_code == 200:
                results.append({"id": i, "status": res.json()["status"]})
            elif res.status_code == 303:
                results.append({"id": i, "status": "completed"})
            elif res.status_code == 404:
                results.append({"id": i, "status": "missing"})
            else:
                results.append({"id": i, "status": "failed"})
        return sorted(results, key=lambda x: x["status"])

    @capture_controller_errors
    def get_jobs_by_id(
        self,
        ids: List[str],
        *,
        console: Console = Console(),
    ) -> Generator[Job | Dict, Any, None]:
        """
        Retrieve jobs by ID.

        Args:
            ids (List[str]): Input list with job IDs.
            console (Console, optional): Console for user feedback.

        Raises:
            BadParameter: Job ID does not exist.

        Returns:
            List[Job]: Job results.
        """
        for i in track(ids, "Retrieving results", transient=True, console=console):
            res: Response = self.ctx.obj.client.get(f"/queries/{i}", skip_errors=True)
            if res.status_code == 200:
                yield Job.model_validate(res.json() | {"id": i})
            else:
                yield {"id": i, "result": None}

    @capture_controller_errors
    def get_job_tags(self) -> list[str]:
        """
        Retrieve all jobs tags.

        Returns:
            list[str]: Sorted list of tags.
        """
        response: Response = self.ctx.obj.client.get("/query_tags")
        if response.status_code == 200:
            return sorted(response.json())
        return []

    @capture_controller_errors
    def get_job_tag_count(self, tag_id: str) -> int:
        """
        Retrieve count of jobs for a tag.

        Args:
            tag_id (str): Tag to count.

        Returns:
            int: Count of jobs for a tag.
        """
        response: Response = self.ctx.obj.client.get(f"/query_tags/{tag_id}/count")
        if response.status_code == 200:
            return response.json().get("count", 0)
        return 0

    @capture_controller_errors
    def delete_job_tag(self, tag_id: str) -> int:
        """
        Delete all jobs for a tag.

        Args:
            tag_id (str): Tag to delete.

        Returns:
            int: Count of deleted jobs for a tag.
        """
        response: Response = self.ctx.obj.client.delete(f"/query_tags/{tag_id}")
        if response.status_code == 200:
            return response.json().get("count", 0)
        return 0
