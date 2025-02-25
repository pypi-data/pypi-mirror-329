from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypedDict

import aiohttp
from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleCalendarSpec,
    ScheduleIntervalSpec,
    ScheduleRange,
    ScheduleSpec,
    WithStartWorkflowOperation,
)
from temporalio.common import (
    SearchAttributeKey,
    SearchAttributePair,
    TypedSearchAttributes,
    WorkflowIDConflictPolicy,
)
from temporalio.worker import Worker
from typing_extensions import Unpack

from .endpoints import explore_class_details
from .observability import log_with_context
from .playground.workflow import PlaygroundRun
from .pydantic import pydantic_data_converter

if TYPE_CHECKING:
    from .event import AgentEvent
    from .security import DataConverter

__all__ = [
    "ScheduleCalendarSpec",
    "ScheduleIntervalSpec",
    "ScheduleRange",
]


@dataclass
class CloudConnectionOptions:
    engine_id: str
    api_key: str
    address: str | None = "localhost:7233"
    api_address: str | None = None
    temporal_namespace: str | None = "default"
    data_converter: DataConverter | None = None


@dataclass
class ServiceOptions:
    rate_limit: int | None = 100000
    max_concurrent_workflow_runs: int | None = 3000
    max_concurrent_function_runs: int | None = 1000
    endpoints: bool | None = True


class Restack:
    api_key: str | None = None
    client: Client | None = None
    options: CloudConnectionOptions | None = None
    functions: list[Any] | None = None

    def __init__(
        self,
        options: CloudConnectionOptions | None = None,
    ) -> None:
        super().__init__()
        self.client = None
        self.options = options

    def get_connection_options(self) -> dict[str, Any]:
        target_host = (
            self.options.address
            if self.options and self.options.address is not None
            else "localhost:7233"
        )
        api_address = (
            f"https://{self.options.api_address}"
            if self.options
            and self.options.api_address is not None
            else "http://localhost:6233"
        )
        engine_id = (
            self.options.engine_id
            if self.options and self.options.engine_id is not None
            else "local"
        )
        options = {
            "target_host": target_host,
            "metadata": {
                "restack-engineId": engine_id,
                "restack-apiAddress": api_address,
            },
        }
        if self.options and self.options.api_key is not None:
            options["tls"] = True
            options["api_key"] = self.options.api_key
        return options

    async def connect(
        self,
        connection_options: CloudConnectionOptions | None = None,
    ) -> None:
        if self.client:
            log_with_context(
                "INFO",
                "Reusing existing client connection",
            )
            return
        try:
            self.client = await self.create_client(
                connection_options,
            )
            log_with_context(
                "INFO",
                "Connected to Restack Engine",
            )
        except Exception as e:
            log_with_context(
                "ERROR",
                "Failed to connect to Restack Engine",
                error=str(e),
            )
            raise

    async def create_client(
        self,
        connection_options: CloudConnectionOptions | None = None,
    ) -> Client:
        connect_options = (
            connection_options or self.get_connection_options()
        )

        target_host = connect_options["target_host"]
        namespace = (
            self.options.temporal_namespace
            if self.options
            and self.options.temporal_namespace is not None
            else "default"
        )
        api_key = (
            self.options.api_key
            if self.options and self.options.api_key is not None
            else None
        )
        tls = bool(self.options and self.options.api_key)
        metadata = connect_options["metadata"]
        data_converter = (
            self.options.data_converter
            if self.options
            and self.options.data_converter is not None
            else pydantic_data_converter
        )
        try:
            client = await Client.connect(
                target_host,
                namespace=namespace,
                api_key=api_key,
                tls=tls,
                rpc_metadata=metadata,
                data_converter=data_converter,
            )
        except Exception as e:
            documentation_url = "https://docs.restack.io/help/troubleshooting#restack-is-not-running"
            log_with_context(
                "ERROR",
                (
                    "Failed to connect, make sure Restack is running: "
                    + documentation_url
                ),
                error=str(e),
            )
            raise
        return client

    async def create_service(
        self,
        workflows: list[Any] | None = None,
        agents: list[Any] | None = None,
        functions: list[Any] | None = None,
        task_queue: str | None = None,
        options: ServiceOptions | None = None,
    ) -> Worker:
        try:
            log_with_context("INFO", "Starting service...")
            client = await self.create_client()
            engine_id = self.get_connection_options()["metadata"][
                "restack-engineId"
            ]
            api_address = self.get_connection_options()[
                "metadata"
            ]["restack-apiAddress"]
            identity = f"{engine_id}-{task_queue or 'restack'}-{os.getpid()}"
            task_queue = f"{engine_id}-{task_queue or 'restack'}"

            all_workflows = (workflows or []) + (agents or [])
            service = Worker(
                identity=identity,
                client=client,
                task_queue=task_queue,
                workflows=all_workflows,
                activities=functions or [],
                max_task_queue_activities_per_second=options.rate_limit,
                max_concurrent_activities=options.max_concurrent_function_runs,
                max_concurrent_workflow_tasks=options.max_concurrent_workflow_runs,
            )
        except Exception as e:
            if (
                e.__cause__
                and "http.client.incompleteread.__mro_entries__".lower()
                in str(e.__cause__).lower()
            ):
                log_with_context(
                    "ERROR",
                    "Failed to start service: Functions in workflow or agents steps need to be imported with import_functions(). See docs at https://docs.restack.io/libraries/python/workflows",
                )
            else:
                log_with_context(
                    "ERROR",
                    "Failed to start service",
                    error=str(e),
                )
            raise
        else:
            log_with_context(
                "INFO",
                "Service created successfully",
            )
            if options.endpoints:
                log_with_context("INFO", "Creating endpoints...")
                async with aiohttp.ClientSession() as session:
                    workflow_details = []
                    for workflow in workflows or []:
                        details = explore_class_details(workflow)
                        details["taskQueue"] = task_queue
                        workflow_details.append(details)

                    agent_details = []
                    for agent in agents or []:
                        details = explore_class_details(agent)
                        details["taskQueue"] = task_queue
                        agent_details.append(details)

                    endpoints_payload = {
                        "identity": identity,
                        "workflows": workflow_details,
                        "agents": agent_details,
                    }

                    try:
                        async with session.post(
                            f"{api_address}/api/engine/endpoints",
                            json=endpoints_payload,
                        ) as response:
                            response_text = await response.text()
                            log_with_context(
                                "INFO",
                                f"{response_text}",
                            )
                    except Exception as e:
                        log_with_context(
                            "WARNING",
                            "Failed to register endpoints",
                            error=str(e),
                        )
                        raise
            return service

    async def run_service(self, service: Worker) -> None:
        try:
            engine_id = self.get_connection_options()["metadata"][
                "restack-engineId"
            ]

            if service.task_queue.endswith("restack"):
                log_with_context(
                    "INFO",
                    "Creating playground service...",
                )

                playground_service = Worker(
                    identity=f"{engine_id}-playground-{os.getpid()}",
                    client=service.client,
                    task_queue=f"{engine_id}-playground",
                    workflows=[PlaygroundRun],
                )

                log_with_context(
                    "INFO",
                    "Services ready to receive workflows and events",
                )
                await asyncio.gather(
                    service.run(),
                    playground_service.run(),
                )
            else:
                log_with_context(
                    "INFO",
                    "Service ready to receive workflows and events",
                )
                await service.run()
        except Exception as e:
            log_with_context(
                "ERROR",
                "Failed to run service",
                error=str(e),
            )
            raise

    class StartServiceKwargs(TypedDict):
        workflows: list[Any]
        agents: list[Any]
        functions: list[Any]
        task_queue: str
        options: ServiceOptions

    async def start_service(
        self,
        **kwargs: Unpack[StartServiceKwargs],
    ) -> None:
        """Start the service with the given workflows, agents, and functions.

        Args:
            **kwargs (StartServiceKwargs): A dictionary containing optional service parameters.
                - workflows (list[Workflow] | None): A list of workflows to start.
                - agents (list[Agent] | None): A list of agents to be used.
                - functions (list[Function] | None): A list of functions to execute.
                - task_queue (str | None): The name of the task queue.
                - options (ServiceOptions | None): Additional service options.

        """
        workflows = kwargs.get("workflows", [])
        agents = kwargs.get("agents", [])
        functions = kwargs.get("functions", [])
        task_queue = kwargs.get("task_queue", "restack")
        options = kwargs.get("options", ServiceOptions())

        if not workflows and not agents and not functions:
            error_message = "At least one workflow, agent, or function must be provided"
            raise ValueError(error_message)

        service = await self.create_service(
            task_queue=task_queue,
            workflows=workflows,
            agents=agents,
            functions=functions or [],
            options=options or ServiceOptions(),
        )
        await self.run_service(service)

    class ScheduleWorkflowKwargs(TypedDict, total=False):
        task_queue: str
        schedule: ScheduleSpec
        event: AgentEvent
        is_agent: bool
        workflow_input: dict[str, Any] | None
        workflow_id: str
        workflow_name: str

    async def schedule_workflow(
        self,
        **kwargs: Unpack[ScheduleWorkflowKwargs],
    ) -> str:
        workflow_input = kwargs.get("workflow_input")
        workflow_id = kwargs.get("workflow_id")
        workflow_name = kwargs.get("workflow_name")
        task_queue = kwargs.get("task_queue", "restack")
        schedule = kwargs.get("schedule")
        event = kwargs.get("event")
        is_agent = kwargs.get("is_agent", False)
        await self.connect()
        if self.client:
            try:
                connection_options = self.get_connection_options()
                engine_id = connection_options["metadata"][
                    "restack-engineId"
                ]

                search_attribute_pairs = [
                    SearchAttributePair(
                        key=SearchAttributeKey.for_text(
                            "engineId",
                        ),
                        value=engine_id,
                    ),
                ]
                search_attributes = TypedSearchAttributes(
                    search_attributes=search_attribute_pairs,
                )

                if not schedule:
                    if event:
                        start_op = WithStartWorkflowOperation(
                            workflow_name,
                            id=f"{engine_id}-{workflow_id}",
                            id_conflict_policy=WorkflowIDConflictPolicy.USE_EXISTING,
                            args=[workflow_input]
                            if workflow_input
                            else [],
                            task_queue=f"{engine_id}-{task_queue}",
                            memo={
                                "engineId": engine_id,
                                "agent": is_agent,
                            },
                            search_attributes=search_attributes,
                        )
                        try:
                            await self.client.execute_update_with_start_workflow(
                                update=event.name,
                                args=[event.input],
                                start_workflow_operation=start_op,
                            )
                            handle = (
                                await start_op.workflow_handle()
                            )
                        except Exception as e:
                            log_with_context(
                                "ERROR",
                                "Failed to start workflow with event",
                                error=str(e),
                            )
                            raise
                        else:
                            log_with_context(
                                "INFO",
                                "Workflow started with event",
                                handle=handle,
                            )
                            return handle.first_execution_run_id

                    else:
                        handle = await self.client.start_workflow(
                            workflow_name,
                            args=[workflow_input]
                            if workflow_input
                            else [],
                            id=f"{engine_id}-{workflow_id}",
                            memo={"engineId": engine_id},
                            search_attributes=search_attributes,
                            task_queue=f"{engine_id}-{task_queue}",
                        )
                    return handle.first_execution_run_id
                schedule_action = ScheduleActionStartWorkflow(
                    workflow=workflow_name,
                    args=[workflow_input]
                    if workflow_input
                    else [],
                    id=f"{engine_id}-{workflow_id}",
                    task_queue=f"{engine_id}-{task_queue}",
                    memo={"engineId": engine_id},
                    typed_search_attributes=search_attributes,
                )
                schedule_obj = Schedule(
                    action=schedule_action,
                    spec=schedule,
                )
                scheduled = await self.client.create_schedule(
                    id=f"{engine_id}-{workflow_id}",
                    schedule=schedule_obj,
                    memo={"engineId": engine_id},
                    search_attributes=search_attributes,
                )

            except Exception as e:
                log_with_context(
                    "ERROR",
                    "Failed to start or schedule workflow",
                    error=str(e),
                )
                raise
            else:
                return scheduled.id

        else:
            error_message = "Workflow result not retrieved due to failed connection."
            log_with_context("ERROR", error_message)
            raise Exception(error_message)

    async def get_workflow_handle(
        self,
        workflow_id: str,
        run_id: str,
    ) -> Any:
        await self.connect()
        if self.client:
            try:
                connection_options = self.get_connection_options()
                engine_id = connection_options["metadata"][
                    "restack-engineId"
                ]
                return self.client.get_workflow_handle(
                    f"{engine_id}-{workflow_id}",
                    run_id=run_id,
                )
            except Exception as e:
                log_with_context(
                    "ERROR",
                    "Failed to get workflow result",
                    error=str(e),
                )
                raise
        else:
            error_message = "Workflow result not retrieved due to failed connection."
            log_with_context("ERROR", error_message)
            raise Exception(error_message)

    async def get_workflow_result(
        self,
        workflow_id: str,
        run_id: str,
    ) -> Any:
        handle = await self.get_workflow_handle(
            workflow_id,
            run_id,
        )
        try:
            return await handle.result()
        except Exception as e:
            log_with_context(
                "ERROR",
                "Failed to get workflow result",
                error=str(e),
            )
            raise

    class ScheduleAgentKwargs(TypedDict, total=False):
        task_queue: str
        schedule: ScheduleSpec
        event: AgentEvent
        agent_input: dict[str, Any] | None
        agent_name: str
        agent_id: str

    async def schedule_agent(
        self,
        **kwargs: Unpack[ScheduleAgentKwargs],
    ) -> str:
        task_queue = kwargs.get("task_queue", "restack")
        schedule = kwargs.get("schedule")
        event = kwargs.get("event")
        agent_input = kwargs.get("agent_input")
        agent_name = kwargs.get("agent_name")
        agent_id = kwargs.get("agent_id")
        return await self.schedule_workflow(
            workflow_name=agent_name,
            workflow_id=agent_id,
            workflow_input=agent_input,
            schedule=schedule,
            task_queue=task_queue,
            event=event,
            is_agent=True,
        )

    async def get_agent_handle(
        self,
        agent_id: str,
        run_id: str,
    ) -> Any:
        return await self.get_workflow_handle(agent_id, run_id)

    async def get_agent_result(
        self,
        agent_id: str,
        run_id: str,
    ) -> Any:
        return await self.get_workflow_result(agent_id, run_id)

    async def get_agent_state(
        self,
        agent_id: str,
        run_id: str,
        state_name: str,
    ) -> Any:
        handle = await self.get_workflow_handle(agent_id, run_id)
        try:
            return await handle.query(state_name)
        except Exception as e:
            log_with_context(
                "ERROR",
                "Failed to get agent state",
                error=str(e),
            )
            raise

    async def send_agent_event(
        self,
        event_name: str,
        agent_id: str,
        run_id: str | None = None,
        event_input: dict[str, Any] | None = None,
    ) -> Any:
        handle = await self.get_workflow_handle(agent_id, run_id)
        try:
            return await handle.execute_update(
                event_name,
                event_input,
            )
        except Exception as e:
            log_with_context(
                "ERROR",
                "Failed to send agent event",
                error=str(e),
            )
            raise
