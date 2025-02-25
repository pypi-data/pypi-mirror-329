from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import TYPE_CHECKING, Any, TypedDict

from temporalio import workflow as temporal_workflow
from temporalio.common import RetryPolicy
from typing_extensions import NotRequired, Unpack

if TYPE_CHECKING:
    from collections.abc import Callable
from temporalio.workflow import (
    ChildWorkflowCancellationType,
    ParentClosePolicy,
)

from .workflow import WorkflowLogger

log = WorkflowLogger()

get_external_agent_handle = (
    temporal_workflow.get_external_workflow_handle
)
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


class Agent:
    def defn(self) -> Any:
        """Mark a class with a decorator as an agent definition.

        Use this decorator on a class that implements your agent's logic.

        Returns:
            Any: The decorated class, registered as a Restack agent.

        Example:
        .. code-block:: python
            with import_functions():
                from src.functions.llm_chat import llm_chat, LlmChatInput

            @agent.defn()
            class MyAgent:
                def __init__(self) -> None:
                    self.end = False
                    self.messages = []

                @agent.event
                async def message(self, message: MessageEvent) -> list[Message]:
                    \"\"\"Adds a message to the agent's state.\"\"\"
                    self.messages.append(message)
                    \"\"\"Process the message.\"\"\"
                    assistant_message = await agent.step(
                        function=llm_chat,
                        function_input=LlmChatInput(messages=self.messages),
                    )
                    \"\"\"Add the assistant's message to the agent's state.\"\"\"
                    self.messages.append(assistant_message)
                    \"\"\"Return the updated chat.\"\"\"
                    return self.messages

                @agent.run
                async def run(self) -> None:
                    await agent.condition(lambda: self.end)

        """
        return temporal_workflow.defn(sandboxed=False)

    def state(
        self,
        fn: Any,
        name: str | None = None,
        description: str | None = None,
    ) -> Any:
        return temporal_workflow.query(
            fn,
            name=name,
            description=description,
        )

    def event(
        self,
        function: RestackFunction,
    ) -> Any:
        """Mark a method with a decorator as an event handler in an agent.

        An event handler is a function that is invoked to update
        the agent's state or respond to external events. The function
        typically receives a payload that describes the event.

        Parameters
        ----------
        function : RestackFunction
            The function to register as an event handler. This should be an asynchronous
            method that updates the agent's state or responds to external events.

        Example:
        .. code-block:: python
            with import_functions():
                from src.functions.llm_chat import llm_chat, LlmChatInput
            @agent.event
            async def message(self, message: MessageEvent) -> list[Message]:
                \"\"\"Adds a message to the agent's state.\"\"\"
                self.messages.append(message)
                \"\"\"Process the message.\"\"\"
                assistant_message = await agent.step(
                    function=llm_chat,
                    function_input=LlmChatInput(messages=self.messages),
                )
                \"\"\"Add the assistant's message to the agent's state.\"\"\"
                self.messages.append(assistant_message)
                \"\"\"Return the updated chat.\"\"\"
                return self.messages

        """
        name = function.__name__
        return temporal_workflow.update(function, name=name)

    def run(self, function: RestackFunction) -> Any:
        """Mark a method as the main run method for an agent.

        This decorator marks a method as the primary run method for an agent.

        Parameters
        ----------
        function : RestackFunction
            The function to register as the agent's run method. This should be an asynchronous
            method that serves as the run point of the agent.

        Returns
        -------
            Any: The decorated function, registered as the agent's run method.

        Example:
        .. code-block:: python
            @agent.run
            async def run(self) -> None:
                await agent.condition(lambda: self.end)

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

    def condition(
        self,
        fn: Callable[[], bool],
        timeout: timedelta | None = None,
    ) -> None:
        return temporal_workflow.wait_condition(
            fn,
            timeout=timeout,
        )

    async def step(
        self,
        **kwargs: Unpack[StepKwargs],
    ) -> Any:
        """Register and execute an agent step.

        This method registers a step for the agent. The step is then executed asynchronously,
        and the result of the step is returned.

        Parameters
        ----------
        **kwargs: Unpack[StepKwargs]
            Keyword arguments with the following keys:

            - function (RestackFunction):
            The function to execute. This function implements the specific logic to be performed
            as a step of the agent's flow.

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
                from src.functions.my_function import (
                    my_function,
                    MyFunctionInput,
                )

            from pydantic import BaseModel


            class MyFunctionInput(BaseModel):
                data: str


            result = await agent.step(
                function=my_function,
                function_input=MyFunctionInput(data="example"),
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
        """Register and start either a child workflow or a child agent as part of the current agent.

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


            workflow_result = await agent.child_start(
                workflow=MyChildWorkflow,
                workflow_id="child-workflow-123",
                workflow_input=WorkflowInput(data="example"),
                task_queue="workflow-queue",
                execution_timeout=timedelta(minutes=5),
            )
            agent_result = await agent.child_start(
                agent=MyChildAgent,
                agent_id="child-agent-123",
                agent_input=AgentInput(data="example"),
                task_queue="agent-queue",
                execution_timeout=timedelta(minutes=5),
            )

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

        As part of the current agent's process, this method starts a child unit and waits for its execution to complete,
        returning its result. You must provide parameters for either a child workflow or a child agent (but not both)
        along with their respective identifiers and input data.

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
        - task_queue (str): The execution queue for the child unit.
        - cancellation_type (ChildWorkflowCancellationType): Specifies how the child unit should handle cancellation.
        - parent_close_policy (ParentClosePolicy): Defines the behavior of the child unit when the parent is closed.
        - execution_timeout (timedelta): The maximum duration allowed for the child unit to complete its work.

        Returns:
            Any: The result returned by the execution of the child unit.

        Example:
        .. code-block:: python
            from .workflow import MyChildWorkflow
            from .agent import MyChildAgent
            from pydantic import BaseModel


            class WorkflowInput(BaseModel):
                data: str


            class AgentInput(BaseModel):
                data: str


            workflow_result = await agent.child_execute(
                workflow=MyChildWorkflow,
                workflow_id="child-workflow-123",
                workflow_input=WorkflowInput(data="example"),
                task_queue="custom-queue",
                execution_timeout=timedelta(minutes=5),
            )
            agent_result = await agent.child_execute(
                agent=MyChildAgent,
                agent_id="child-agent-123",
                agent_input=AgentInput(data="example"),
                task_queue="agent-queue",
                execution_timeout=timedelta(minutes=5),
            )

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

    async def sleep(self, seconds: int) -> Any:
        return await asyncio.sleep(seconds)

    def get_engine_id_from_client(self) -> Any:
        return temporal_workflow.memo_value("engineId", "local")

    def add_engine_id_prefix(
        self,
        engine_id: str,
        agent_id: str,
    ) -> str:
        if agent_id.startswith(f"{engine_id}-"):
            return agent_id
        return f"{engine_id}-{agent_id}"


agent = Agent()
