from typing import Any

from pydantic import Field

from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.frinx_rest import X_FROM
from frinx.common.worker.service import ServiceWorkersImpl
from frinx.common.worker.task import Task
from frinx.common.worker.task_def import DefaultTaskDefinition
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.worker.worker import WorkerImpl


class TestTaskGenerator:
    def test_create_task_def(self) -> None:
        class Http(ServiceWorkersImpl):
            class HttpTask1(WorkerImpl):
                class WorkerDefinition(TaskDefinition):
                    name = 'HTTP_task_1'
                    description = 'Generic http task'
                    labels = ['BASIC', 'HTTP']
                    timeout_seconds = 360
                    response_timeout_seconds = 360
                    execution_name_space = 'execution_namespace'
                    retry_count = 10
                    concurrent_exec_limit = 5

                class WorkerInput(TaskInput):
                    http_request: str | dict[str, Any] | None

                class WorkerOutput(TaskOutput):
                    response: Any
                    body: Any
                    status_code: int = Field(..., alias='statusCode')
                    cookies: dict[str, Any]

                def execute(self, task_def: Task) -> TaskResult:
                    return TaskResult(status=TaskResultStatus.COMPLETED)

            class HttpTask2(WorkerImpl):
                class WorkerDefinition(TaskDefinition):
                    name = 'HTTP_task'
                    description = 'Generic http task'
                    labels = ['BASIC', 'HTTP']
                    timeout_seconds = 360
                    response_timeout_seconds = 360

                class WorkerInput(TaskInput):
                    http_request: str | dict[str, Any] | None

                class WorkerOutput(TaskOutput):
                    response: Any
                    body: Any
                    status_code: int = Field(..., alias='statusCode')
                    cookies: dict[str, Any]

                def execute(self, task_def: Task) -> TaskResult:
                    return TaskResult(status=TaskResultStatus.COMPLETED)

        tasks = Http().tasks()
        test_task = []
        for task in tasks:
            test_task.append(task.task_def.dict(exclude_none=True, by_alias=True))

        test_mock = [
            {
                'name': 'HTTP_task_1',
                'description': '{"description": "Generic http task", "labels": ["BASIC", "HTTP"]}',
                'retryCount': 10,
                'timeoutSeconds': 360,
                'inputKeys': ['http_request'],
                'outputKeys': ['response', 'body', 'statusCode', 'cookies'],
                'timeoutPolicy': 'ALERT_ONLY',
                'retryLogic': 'FIXED',
                'retryDelaySeconds': 0,
                'responseTimeoutSeconds': 360,
                'concurrentExecLimit': 5,
                'rateLimitPerFrequency': 0,
                'rateLimitFrequencyInSeconds': 5,
                'executionNameSpace': 'execution_namespace',
                'ownerEmail': 'fm-base-workers',
            },
            {
                'name': 'HTTP_task',
                'description': '{"description": "Generic http task", "labels": ["BASIC", "HTTP"]}',
                'retryCount': 0,
                'timeoutSeconds': 360,
                'inputKeys': ['http_request'],
                'outputKeys': ['response', 'body', 'statusCode', 'cookies'],
                'timeoutPolicy': 'ALERT_ONLY',
                'retryLogic': 'FIXED',
                'retryDelaySeconds': 0,
                'responseTimeoutSeconds': 360,
                'rateLimitPerFrequency': 0,
                'rateLimitFrequencyInSeconds': 5,
                'ownerEmail': 'fm-base-workers',
            },
        ]

        assert test_mock == test_task

    def test_create_task_def_with_custom_default(self) -> None:
        class HttpTask(WorkerImpl):
            class WorkerDefinition(TaskDefinition):
                name = 'HTTP_task'
                description = 'Generic http task'
                labels = ['BASIC', 'HTTP']
                timeout_seconds = 360
                response_timeout_seconds = 360

            class WorkerInput(TaskInput):
                http_request: str | dict[str, Any] | None

            class WorkerOutput(TaskOutput):
                response: Any
                body: Any
                status_code: int = Field(..., alias='statusCode')
                cookies: dict[str, Any]

            def execute(self, task: Task) -> TaskResult:
                return TaskResult(status=TaskResultStatus.COMPLETED)

        class DefaultCustomTaskDefinition(DefaultTaskDefinition):
            limit_to_thread_count: int = 10

        test_task = HttpTask(task_def_template=DefaultCustomTaskDefinition).task_def.dict(
            exclude_none=True
        )
        test_mock = {
            'name': 'HTTP_task',
            'description': '{"description": "Generic http task", "labels": ["BASIC", "HTTP"]}',
            'retry_count': 0,
            'timeout_seconds': 360,
            'input_keys': ['http_request'],
            'output_keys': ['response', 'body', 'statusCode', 'cookies'],
            'timeout_policy': 'ALERT_ONLY',
            'retry_logic': 'FIXED',
            'retry_delay_seconds': 0,
            'response_timeout_seconds': 360,
            'rate_limit_per_frequency': 0,
            'rate_limit_frequency_in_seconds': 5,
            'owner_email': X_FROM,
            'limit_to_thread_count': 10,
        }

        assert test_mock == test_task