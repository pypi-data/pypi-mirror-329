from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Any, TypedDict

from temporalio import workflow as temporal_workflow
from temporalio.common import RetryPolicy
from temporalio.workflow import (
    ChildWorkflowCancellationType,
    ParentClosePolicy,
)
from typing_extensions import NotRequired, Unpack

from .observability import log_with_context, logger

temporal_workflow.logger.logger = logger


class WorkflowLogger:
    """Wrapper for workflow logger that ensures proper context and formatting."""

    def __init__(self) -> None:
        self._logger = temporal_workflow.logger

    def _log(
        self,
        level: str,
        message: str,
        **kwargs: Any,
    ) -> None:
        if temporal_workflow._Runtime.maybe_current():  # noqa: SLF001
            getattr(self._logger, level)(
                message,
                extra={
                    "extra_fields": {
                        **kwargs,
                        "client_log": True,
                    },
                },
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

get_external_workflow_handle = (
    temporal_workflow.get_external_workflow_handle
)
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

RestackFunction = Any
RestackFunctionInput = Any


class StepKwargs(TypedDict):
    function: RestackFunction
    function_input: NotRequired[RestackFunctionInput]
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
    def defn(self) -> Any:
        """Mark a class as a workflow definition.

        Use this decorator on a class that implements your workflow's logic.

        Returns:
            Any: The decorated class, registered as a Restack workflow.

        Example:
        .. code-block:: python
            with import_functions():
                from src.functions.translate import translate, TranslateInput
                from src.functions.transcribe import transcribe, TranscribeInput

            @workflow.defn()
            class MyWorkflow:
                @worfklow.run
                async def run(self, workflow_input: Any):
                    \"\"\"Translate the workflow input.\"\"\"
                    translated_result = await workflow.step(
                        function=translate,
                        function_input=TranslateInput(text=workflow_input),
                    )
                    \"\"\"Transcribe the translated result.\"\"\"
                    transcribed_result = await workflow.step(
                        function=transcribe,
                        function_input=TranscribeInput(text=translated_result),
                    )
                    \"\"\"Return the result.\"\"\"
                    return transcribed_result

        """
        return temporal_workflow.defn(sandboxed=False)

    def run(self, function: RestackFunction) -> Any:
        """Mark a method as the main run method for a workflow.

        This decorator marks a method as the primary entry point for a workflow.

        Parameters
        ----------
        function : RestackFunction
            The function to register as the workflow's run method. This should be an asynchronous
            method that serves as the main entry point of the workflow.

        Returns
        -------
            Any: The decorated function, registered as the workflow's run method.

        Example:
        .. code-block:: python
            with import_functions():
                from src.functions.translate import translate, TranslateInput
                from src.functions.transcribe import transcribe, TranscribeInput

            @workflow.defn()
            class MyWorkflow:
                @workflow.run
                async def run(self, workflow_input: Any):
                \"\"\"Translate the workflow input.\"\"\"
                translated_result = await workflow.step(
                    function=translate,
                    function_input=TranslateInput(text=workflow_input),
                )
                \"\"\"Transcribe the translated result.\"\"\"
                transcribed_result = await workflow.step(
                    function=transcribe,
                    function_input=TranscribeInput(text=translated_result),
                )
                \"\"\"Return the result.\"\"\"
                return transcribed_result

        """
        import inspect
        from functools import wraps

        sig = inspect.signature(function)
        expected_params = len(sig.parameters) - 1

        @wraps(function)
        async def wrapper(*args: Any, **_kwargs: Any) -> Any:
            if expected_params == 0:
                return await function(args[0])
            if expected_params == 1:
                if len(args) > 1:
                    return await function(args[0], args[1])
                return await function(args[0], None)
            message = """
                Invalid run method signature: the run method must be defined as either:
                async def run(self) -> None
                or:
                async def run(self, function_input: dict) -> None
                Please update your run method accordingly.
            """
            raise TypeError(message)

        return temporal_workflow.run(wrapper)

    async def step(
        self,
        **kwargs: Unpack[StepKwargs],
    ) -> Any:
        """Register and execute a workflow step.

        This method registers a step for the workflow. The step is then executed asynchronously,
        and the result of the step is returned.

        Parameters
        ----------
        **kwargs: Unpack[StepKwargs]
            Keyword arguments with the following keys:

            - function (RestackFunction):
            The function to execute. This function implements the specific logic to be performed
            as a step of the workflow's flow.

            - function_input (Optional[RestackFunctionInput]):
            The input data to pass to the function. Typically, this input is validated
            using a Pydantic model. It is recommended to use a Pydantic model for input validation.

            - task_queue (Optional[str]):
            The task queue on which the function is executed.

            - retry_policy (Optional[RetryPolicy]):
            Retry policy governing how the function should be retried upon failure.

            - schedule_to_close_timeout (Optional[timedelta]):
            The maximum duration allowed for the function execution to complete.

        Returns
        -------
            Any: The result of the executed function step.

        Example:
        .. code-block:: python
            with import_functions():
                from src.functions.translate import (
                    translate,
                    TranslateInput,
                )

            from pydantic import BaseModel


            class TranslateInput(BaseModel):
                text: str


            result = await workflow.step(
                function=translate,
                function_input=TranslateInput(
                    text="Hello, world!"
                ),
                task_queue="custom-task-queue",
                schedule_to_close_timeout=timedelta(minutes=3),
            )

        """
        function = kwargs.get("function")
        function_input = kwargs.get("function_input")
        task_queue = kwargs.get("task_queue", "restack")
        retry_policy = kwargs.get("retry_policy")
        schedule_to_close_timeout = kwargs.get(
            "schedule_to_close_timeout",
            timedelta(minutes=2),
        )
        engine_id = self.get_engine_id_from_client()
        return await temporal_workflow.execute_activity(
            activity=function,
            args=(function_input,)
            if function_input is not None
            else (),
            task_queue=f"{engine_id}-{task_queue}",
            schedule_to_close_timeout=schedule_to_close_timeout,
            retry_policy=retry_policy,
        )

    async def child_start(
        self,
        **kwargs: Unpack[ChildKwargs],
    ) -> Any:
        """Register and start either a child workflow or a child agent as part of the current workflow.

        This method schedules a child unit to execute asynchronously. Depending on your use case,
        you must provide either the parameters for a child workflow or for a child agent (but not both).
        Only one child unit can be started at a time.

        Required parameters:
        - For a child workflow:
            - workflow: The child workflow class to start.
            - workflow_id: A unique identifier for the child workflow.
            - workflow_input: The input data for the child workflow. Recommended to use a Pydantic model.
        - For a child agent:
            - agent: The child agent class to start.
            - agent_id: A unique identifier for the child agent.
            - agent_input: The input data for the child agent. Recommended to use a Pydantic model.

        Optional parameters:
        - task_queue (str): The task queue for executing the child unit (default: `"restack"`).
        - cancellation_type (ChildWorkflowCancellationType): Defines how the child unit should handle cancellation.
        - parent_close_policy (ParentClosePolicy): Specifies the behavior when the parent unit is closed.
        - execution_timeout (timedelta): The maximum duration allowed for the child unit to complete.

        Returns:
            Any: The result produced by starting the child unit.

        Example:
        .. code-block:: python
            from .workflow import MyChildWorkflow
            from .agent import MyChildAgent
            from pydantic import BaseModel

            class WorkflowInput(BaseModel):
                data: str

            class AgentInput(BaseModel):
                data: str

            workflow_result = await workflow.child_start(
                workflow=MyChildWorkflow,
                workflow_id="child-workflow-123",
                workflow_input=WorkflowInput(data="example"),
                task_queue="workflow-queue",
                execution_timeout=timedelta(minutes=5)
            )
            agent_result = await workflow.child_start(
                agent=MyChildAgent,
                agent_id="child-agent-123",
                agent_input=AgentInput(data="example"),
                task_queue="agent-queue",
                execution_timeout=timedelta(minutes=5)

        """
        workflow = kwargs.get("workflow")
        workflow_input = kwargs.get("workflow_input")
        workflow_id = kwargs.get("workflow_id")
        agent = kwargs.get("agent")
        agent_input = kwargs.get("agent_input")
        agent_id = kwargs.get("agent_id")
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
            error_message = (
                "Either workflow or agent must be provided."
            )
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
            id=self.add_engine_id_prefix(
                engine_id,
                workflow_id or agent_id,
            ),
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
        """Register and synchronously execute a subordinate unit (either a child workflow or a child agent).

        As part of the current workflow's process, this method starts a child unit and waits for its execution
        to complete, returning its result. You must provide parameters for either a child workflow or a child
        agent (but not both) along with their respective identifiers and input data.

        Required parameters:
        - For a child workflow:
            - workflow: The child workflow class to execute.
            - workflow_id: A unique identifier for the child workflow.
            - workflow_input: The input data for the child workflow. Recommended to use a Pydantic model.
        - For a child agent:
            - agent: The child agent class to execute.
            - agent_id: A unique identifier for the child agent.
            - agent_input: The input data for the child agent. Recommended to use a Pydantic model.

        Optional parameters:
        - task_queue (str): The task queue for executing the child unit (default: `"restack"`).
        - cancellation_type (ChildWorkflowCancellationType): Defines how the child unit should handle cancellation.
        - parent_close_policy (ParentClosePolicy): Specifies the behavior when the parent unit is closed.
        - execution_timeout (timedelta): The maximum duration allowed for the child unit to complete.

        Returns:
            Any: The result produced by executing the child unit.

        Example:
        .. code-block:: python
            from .workflow import MyChildWorkflow
            from .agent import MyChildAgent
            from pydantic import BaseModel


            class WorkflowInput(BaseModel):
                data: str


            class AgentInput(BaseModel):
                data: str


            workflow_result = await workflow.child_execute(
                workflow=MyChildWorkflow,
                workflow_id="child-workflow-123",
                workflow_input=WorkflowInput(data="example"),
                task_queue="workflow-queue",
                execution_timeout=timedelta(minutes=5),
            )
            agent_result = await workflow.child_execute(
                agent=MyChildAgent,
                agent_id="child-agent-123",
                agent_input=AgentInput(data="example"),
                task_queue="agent-queue",
                execution_timeout=timedelta(minutes=5),
            )

        """
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
            error_message = (
                "Either workflow or agent must be provided."
            )
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
            id=self.add_engine_id_prefix(
                engine_id,
                workflow_id or agent_id,
            ),
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

    def add_engine_id_prefix(
        self,
        engine_id: str,
        workflow_id: str,
    ) -> str:
        if workflow_id.startswith(f"{engine_id}-"):
            return workflow_id
        return f"{engine_id}-{workflow_id}"


workflow = Workflow()
