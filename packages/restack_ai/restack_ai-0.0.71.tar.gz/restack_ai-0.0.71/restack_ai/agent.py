from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import TYPE_CHECKING, Any, TypedDict

from temporalio import workflow as temporal_workflow
from temporalio.common import RetryPolicy
from typing_extensions import NotRequired, Unpack

if TYPE_CHECKING:
    from collections.abc import Callable

    from temporalio.types import CallableAsyncType
from temporalio.workflow import ChildWorkflowCancellationType, ParentClosePolicy

from .workflow import WorkflowLogger

log = WorkflowLogger()

get_external_agent_handle = temporal_workflow.get_external_workflow_handle
agent_info = temporal_workflow.info
continue_as_new = temporal_workflow.continue_as_new
condition = temporal_workflow.wait_condition
import_functions = temporal_workflow.unsafe.imports_passed_through
uuid = temporal_workflow.uuid4

__all__ = [
    "RetryPolicy",
    "agent_info",
    "condition",
    "continue_as_new",
    "get_external_agent_handle",
    "import_functions",
    "log",
    "uuid",
]


class StepKwargs(TypedDict):
    function: Any
    function_input: NotRequired[Any]
    task_queue: NotRequired[str]
    retry_policy: NotRequired[RetryPolicy]
    schedule_to_close_timeout: NotRequired[timedelta]


class ChildKwargs(TypedDict, total=False):
    workflow: Any
    workflow_id: str
    workflow_input: Any
    agent: Any
    agent_id: str
    agent_input: Any
    task_queue: str
    cancellation_type: ChildWorkflowCancellationType
    parent_close_policy: ParentClosePolicy
    execution_timeout: timedelta


class Agent:
    def defn(self, *args: Any, **kwargs: Any) -> Any:
        return temporal_workflow.defn(*args, **kwargs, sandboxed=False)

    def state(
        self, fn: Any, name: str | None = None, description: str | None = None
    ) -> Any:
        return temporal_workflow.query(fn, name=name, description=description)

    def event(
        self, fn: Any, name: str | None = None, description: str | None = None
    ) -> Any:
        return temporal_workflow.update(fn, name=name, description=description)

    def run(self, fn: CallableAsyncType) -> CallableAsyncType:
        return temporal_workflow.run(fn)

    def condition(
        self, fn: Callable[[], bool], timeout: timedelta | None = None
    ) -> None:
        return temporal_workflow.wait_condition(fn, timeout=timeout)

    async def step(
        self,
        **kwargs: Unpack[StepKwargs],
    ) -> Any:
        function = kwargs.get("function")
        function_input = kwargs.get("function_input")
        task_queue = kwargs.get("task_queue", "restack")
        retry_policy = kwargs.get("retry_policy")
        schedule_to_close_timeout = kwargs.get(
            "schedule_to_close_timeout", timedelta(minutes=2)
        )
        engine_id = self.get_engine_id_from_client()
        return await temporal_workflow.execute_activity(
            activity=function,
            args=(function_input,) if function_input is not None else (),
            task_queue=f"{engine_id}-{task_queue}",
            schedule_to_close_timeout=schedule_to_close_timeout,
            retry_policy=retry_policy,
        )

    async def child_start(
        self,
        **kwargs: Unpack[ChildKwargs],
    ) -> Any:
        task_queue = kwargs.get("task_queue", "restack")
        cancellation_type = kwargs.get(
            "cancellation_type",
            ChildWorkflowCancellationType.WAIT_CANCELLATION_COMPLETED,
        )
        parent_close_policy = kwargs.get(
            "parent_close_policy",
            ParentClosePolicy.TERMINATE,
        )
        execution_timeout = kwargs.get("execution_timeout")
        workflow = kwargs.get("workflow")
        workflow_id = kwargs.get("workflow_id")
        agent = kwargs.get("agent")
        agent_id = kwargs.get("agent_id")
        workflow_input = kwargs.get("workflow_input")
        agent_input = kwargs.get("agent_input")

        if not workflow and not agent:
            error_message = "Either workflow or agent must be provided."
            log.error(error_message)
            raise ValueError(error_message)

        if workflow and agent:
            error_message = "Either workflow or agent must be provided, but not both."
            log.error(error_message)
            raise ValueError(error_message)

        engine_id = self.get_engine_id_from_client()

        return await temporal_workflow.start_child_workflow(
            workflow=workflow.run or agent.run,
            args=[workflow_input or agent_input]
            if workflow_input or agent_input
            else [],
            id=self.add_engine_id_prefix(engine_id, workflow_id or agent_id),
            task_queue=f"{engine_id}-{task_queue}",
            memo={"engineId": engine_id},
            search_attributes={"engineId": [engine_id]},
            cancellation_type=cancellation_type,
            parent_close_policy=parent_close_policy,
            execution_timeout=execution_timeout,
        )

    async def child_execute(
        self,
        **kwargs: Unpack[ChildKwargs],
    ) -> Any:
        workflow = kwargs.get("workflow")
        workflow_id = kwargs.get("workflow_id")
        agent = kwargs.get("agent")
        agent_id = kwargs.get("agent_id")
        workflow_input = kwargs.get("workflow_input")
        agent_input = kwargs.get("agent_input")
        task_queue = kwargs.get("task_queue", "restack")
        cancellation_type = kwargs.get(
            "cancellation_type",
            ChildWorkflowCancellationType.WAIT_CANCELLATION_COMPLETED,
        )
        parent_close_policy = kwargs.get(
            "parent_close_policy",
            ParentClosePolicy.TERMINATE,
        )
        execution_timeout = kwargs.get("execution_timeout")
        if not workflow and not agent:
            error_message = "Either workflow or agent must be provided."
            log.error(error_message)
            raise ValueError(error_message)

        if workflow and agent:
            error_message = "Either workflow or agent must be provided, but not both."
            log.error(error_message)
            raise ValueError(error_message)

        engine_id = self.get_engine_id_from_client()

        return await temporal_workflow.execute_child_workflow(
            workflow=workflow.run or agent.run,
            args=[workflow_input or agent_input]
            if workflow_input or agent_input
            else [],
            id=self.add_engine_id_prefix(engine_id, workflow_id or agent_id),
            task_queue=f"{engine_id}-{task_queue}",
            memo={"engineId": engine_id},
            search_attributes={"engineId": [engine_id]},
            cancellation_type=cancellation_type,
            parent_close_policy=parent_close_policy,
            execution_timeout=execution_timeout,
        )

    async def sleep(self, seconds: int) -> Any:
        return await asyncio.sleep(seconds)

    def get_engine_id_from_client(self) -> Any:
        return temporal_workflow.memo_value("engineId", "local")

    def add_engine_id_prefix(self, engine_id: str, agent_id: str) -> str:
        if agent_id.startswith(f"{engine_id}-"):
            return agent_id
        return f"{engine_id}-{agent_id}"


agent = Agent()
