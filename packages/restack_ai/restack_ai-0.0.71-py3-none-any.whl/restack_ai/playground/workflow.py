# ruff: noqa: ERA001
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from temporalio import workflow

from .function import test_run


@dataclass
class PlaygroundInput:
    content: str = "test"


@workflow.defn(sandboxed=False)
class PlaygroundRun:
    # def __init__(self) -> None:
    #     self.events = []

    @workflow.run
    async def run(self, workflow_input: PlaygroundInput) -> Any:
        await workflow.execute_activity(
            activity=test_run,
            args=[workflow_input.content],
            start_to_close_timeout=timedelta(seconds=120),
        )

        return "done"

    # @workflow.update
    # async def test_event(self, youpi: Any) -> Any:
    #     self.events.append(youpi)
    #     return youpi
