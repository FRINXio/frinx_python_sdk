import copy
from typing import Any

from pydantic import Field
from pydantic import error_wrappers
from pytest import raises

from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.frinx_rest import X_FROM
from frinx.common.type_aliases import DictAny
from frinx.common.type_aliases import ListAny
from frinx.common.worker.task_def import DefaultTaskDefinition
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.worker.worker import WorkerImpl
from tests.unit_tests.conftest import MockExecuteProperties


class TestTaskGenerator:
    def test_create_task_def(self) -> None:
        class HttpTask(WorkerImpl):
            class WorkerDefinition(TaskDefinition):
                name: str = 'HTTP_task'
                description: str = 'Generic http task'
                labels: ListAny = ['BASIC', 'HTTP']
                timeout_seconds: int = 360
                response_timeout_seconds: int = 360
                execution_name_space: str = 'execution_namespace'
                retry_count: int = 10
                concurrent_exec_limit: int = 5

            class WorkerInput(TaskInput):
                http_request: str | dict[str, Any] | None

            class WorkerOutput(TaskOutput):
                response: Any
                body: Any
                status_code: int = Field(..., alias='statusCode')
                cookies: dict[str, Any]

            def execute(self, worker_input: WorkerInput) -> TaskResult[WorkerOutput]:
                return TaskResult(status=TaskResultStatus.COMPLETED)

        test_task = HttpTask(task_def_template=DefaultTaskDefinition).task_def.dict(
            exclude_none=True
        )
        test_mock = {
            'name': 'HTTP_task',
            'description': '{"description": "Generic http task", "labels": ["BASIC", "HTTP"]}',
            'retry_count': 10,
            'timeout_seconds': 360,
            'input_keys': ['http_request'],
            'output_keys': ['response', 'body', 'statusCode', 'cookies'],
            'timeout_policy': 'ALERT_ONLY',
            'retry_logic': 'FIXED',
            'retry_delay_seconds': 0,
            'response_timeout_seconds': 360,
            'concurrent_exec_limit': 5,
            'rate_limit_per_frequency': 0,
            'rate_limit_frequency_in_seconds': 5,
            'execution_name_space': 'execution_namespace',
            'owner_email': 'fm-base-workers',
        }

        assert test_mock == test_task

    def test_create_task_def_with_custom_default(self) -> None:
        class HttpTask(WorkerImpl):
            class WorkerDefinition(TaskDefinition):
                name: str = 'HTTP_task'
                description: str = 'Generic http task'
                labels: ListAny = ['BASIC', 'HTTP']
                timeout_seconds: int = 360
                response_timeout_seconds: int = 360

            class WorkerInput(TaskInput):
                http_request: str | dict[str, Any] | None

            class WorkerOutput(TaskOutput):
                response: Any
                body: Any
                status_code: int = Field(..., alias='statusCode')
                cookies: dict[str, Any]

            def execute(self, worker_input: WorkerInput) -> TaskResult[WorkerOutput]:
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

    def test_execute_properties_default(self) -> None:

        task = MockExecuteProperties()
        response: DictAny = DictAny({
            'response': {
                'string_list': ['a', 'b', 'c'],
                'and_dict': {'a': 'a', 'b': {'c': 'c'}},
                'required_string': 'a',
                'optional_string': None
            }
        })

        result = task.__class__._execute_func(task=copy.deepcopy(task.TEST_WORKER_INPUTS))
        assert result.get('output') == response

    def test_execute_properties_exclude_empty_strings_disabled(self) -> None:
        task = MockExecuteProperties()
        response: DictAny = DictAny({
            'response': {
                'string_list': ['a', 'b', 'c'],
                'and_dict': {'a': 'a', 'b': {'c': 'c'}},
                'required_string': 'a',
                'optional_string': ''
            }
        })

        task.ExecutionProperties.__fields__['exclude_empty_inputs'].default = False
        result = task.__class__._execute_func(task=copy.deepcopy(task.TEST_WORKER_INPUTS))
        assert result.get('output') == response

    def test_execute_properties_transform_string_to_json_valid_disabled(self) -> None:
        task = MockExecuteProperties()

        test_worker_inputs: DictAny = DictAny({
            'inputData': {
                'string_list': ['a', 'b', 'c'],
                'and_dict': {'a': 'a', 'b': {'c': 'c'}},
                'required_string': 'a',
                'optional_string': ''
            }
        })

        response: DictAny = DictAny({
            'response': {
                'string_list': ['a', 'b', 'c'],
                'and_dict': {'a': 'a', 'b': {'c': 'c'}},
                'required_string': 'a',
                'optional_string': None
            }
        })

        task.ExecutionProperties.__fields__['exclude_empty_inputs'].default = True
        task.ExecutionProperties.__fields__['transform_string_to_json_valid'].default = False
        result = task.__class__._execute_func(task=copy.deepcopy(test_worker_inputs))
        assert result.get('output') == response

    def test_execute_properties_transform_string_to_json_valid_disabled_exception(self) -> None:

        task = MockExecuteProperties()
        task.ExecutionProperties.__fields__['transform_string_to_json_valid'].default = False
        with raises(error_wrappers.ValidationError):
            task.__class__._execute_func(task=copy.deepcopy(task.TEST_WORKER_INPUTS))
