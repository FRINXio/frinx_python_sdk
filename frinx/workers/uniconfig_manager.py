from typing import Any

from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.worker.service import ServiceWorkersImpl
from frinx.common.worker.task import Task
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.worker.worker import WorkerImpl
from frinx.services.uniconfig_manager import close_transaction
from frinx.services.uniconfig_manager import commit_transaction
from frinx.services.uniconfig_manager import create_transaction
from frinx.services.uniconfig_manager import replace_config_with_operational
from frinx.services.uniconfig_manager import sync_from_network


class UniconfigManager(ServiceWorkersImpl):
    class CreateTransaction(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Create_transaction_RPC'
            description = 'Create Uniconfig transaction'

        class WorkerInput(TaskInput):
            transaction_timeout: int | None = None
            use_dedicated_session: bool = False
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            transaction_id: str
            uniconfig_server_id: str | None

        def execute(self, task: Task) -> TaskResult:
            response = create_transaction(**task.input_data)
            cookies = response.cookies.get_dict()
            transaction_id: str = cookies['UNICONFIGTXID']
            uniconfig_server_id: str = cookies.get('uniconfig_server_id')
            return TaskResult(
                status=TaskResultStatus.COMPLETED,
                output={'transaction_id': transaction_id, 'uniconfig_server_id': uniconfig_server_id}
            )

    class CloseTransaction(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Close_transaction_RPC'
            description = 'Close Uniconfig transaction'

        class WorkerInput(TaskInput):
            transaction_id: str
            uniconfig_url_base: str | None = None

        def execute(self, task: Task) -> TaskResult:
            close_transaction(**task.input_data)
            return TaskResult(status=TaskResultStatus.COMPLETED)

    class CommitTransaction(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Commit_transaction_RPC'
            description = 'Commit Uniconfig transaction'

        class WorkerInput(TaskInput):
            transaction_id: str
            confirmed_commit: bool = False
            validate_commit: bool = True
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, task: Task) -> TaskResult:
            response = commit_transaction(**task.input_data)
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())

    class ReplaceConfigWithOperational(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Replace_config_with_operational_RPC'
            description = 'Replace Uniconfig CONFIG datastore with OPER datastore'

        class WorkerInput(TaskInput):
            node_ids: list[str]
            transaction_id: str
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, task: Task) -> TaskResult:
            response = replace_config_with_operational(**task.input_data)
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())

    class SyncFromNetwork(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Sync_from_network_RPC'
            description = 'Synchronize configuration from network and the UniConfig nodes'

        class WorkerInput(TaskInput):
            node_ids: list[str]
            transaction_id: str
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, task: Task) -> TaskResult:
            response = sync_from_network(**task.input_data)
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())
