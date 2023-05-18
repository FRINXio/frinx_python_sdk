from typing import Any

from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.worker.service import ServiceWorkersImpl
from frinx.common.worker.task import Task
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.worker.worker import WorkerImpl
from frinx.services.snapshot_manager import create_snapshot
from frinx.services.snapshot_manager import delete_snapshot
from frinx.services.snapshot_manager import replace_config_with_snapshot


class SnapshotManager(ServiceWorkersImpl):
    class CreateSnapshot(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Create_snapshot_RPC'
            description = 'Create Uniconfig snapshot'

        class WorkerInput(TaskInput):
            node_ids: list[str]
            snapshot_name: str
            transaction_id: str
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, task: Task) -> TaskResult:
            response = create_snapshot(**task.input_data)
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())

    class DeleteSnapshot(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Delete_snapshot_RPC'
            description = 'Delete Uniconfig snapshot'

        class WorkerInput(TaskInput):
            snapshot_name: str
            transaction_id: str
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, task: Task) -> TaskResult:
            response = delete_snapshot(**task.input_data)
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())

    class ReplaceConfigWithSnapshot(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Replace_config_with_snapshot_RPC'
            description = 'Replace Uniconfig CONFIG datastore with a snapshot'

        class WorkerInput(TaskInput):
            snapshot_name: str
            node_ids: list[str]
            transaction_id: str
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, task: Task) -> TaskResult:
            response = replace_config_with_snapshot(**task.input_data)
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())
