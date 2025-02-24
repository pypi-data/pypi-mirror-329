from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import TYPE_CHECKING, Any, TypedDict

from typing_extensions import NotRequired, Unpack

if TYPE_CHECKING:
    from temporalio.types import CallableAsyncType

from temporalio import workflow as temporal_workflow
from temporalio.common import RetryPolicy
from temporalio.workflow import ChildWorkflowCancellationType, ParentClosePolicy

from .observability import log_with_context, logger

temporal_workflow.logger.logger = logger


class WorkflowLogger:
    """Wrapper for workflow logger that ensures proper context and formatting."""

    def __init__(self) -> None:
        self._logger = temporal_workflow.logger

    def _log(self, level: str, message: str, **kwargs: Any) -> None:
        if temporal_workflow._Runtime.maybe_current():  # noqa: SLF001
            getattr(self._logger, level)(
                message,
                extra={"extra_fields": {**kwargs, "client_log": True}},
            )
        else:
            log_with_context(level.upper(), message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        self._log("debug", message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        self._log("info", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._log("warning", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self._log("error", message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        self._log("critical", message, **kwargs)


log = WorkflowLogger()

get_external_workflow_handle = temporal_workflow.get_external_workflow_handle
workflow_info = temporal_workflow.info
continue_as_new = temporal_workflow.continue_as_new
import_functions = temporal_workflow.unsafe.imports_passed_through
uuid = temporal_workflow.uuid4

__all__ = [
    "RetryPolicy",
    "continue_as_new",
    "get_external_workflow_handle",
    "import_functions",
    "log",
    "uuid",
    "workflow_info",
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


class Workflow:
    def defn(self, *args: Any, **kwargs: Any) -> Any:
        return temporal_workflow.defn(*args, **kwargs, sandboxed=False)

    def run(self, fn: CallableAsyncType) -> CallableAsyncType:
        return temporal_workflow.run(fn)

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
        workflow_input = kwargs.get("workflow_input")
        agent = kwargs.get("agent")
        agent_id = kwargs.get("agent_id")
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

    async def sleep(self, seconds: int) -> None:
        return await asyncio.sleep(seconds)

    def get_engine_id_from_client(self) -> str:
        return temporal_workflow.memo_value("engineId", "local")

    def add_engine_id_prefix(self, engine_id: str, workflow_id: str) -> str:
        if workflow_id.startswith(f"{engine_id}-"):
            return workflow_id
        return f"{engine_id}-{workflow_id}"


workflow = Workflow()
