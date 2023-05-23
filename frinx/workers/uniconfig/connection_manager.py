from typing import Any
from typing import Literal

from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.worker.service import ServiceWorkersImpl
from frinx.common.worker.task import Task
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.worker.worker import WorkerImpl
from frinx.services.uniconfig.connection_manager import install_node
from frinx.services.uniconfig.connection_manager import uninstall_node


class ConnectionManager(ServiceWorkersImpl):
    class InstallNode(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Install_node_RPC'
            description = 'Install node to Uniconfig'

        class WorkerInput(TaskInput):
            node_id: str
            connection_type: Literal['netconf', 'cli']
            install_params: dict[str, Any] | None = None,
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, task: Task) -> TaskResult:
            response = install_node(**task.input_data)
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())

    class UninstallNode(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Uninstall_node_RPC'
            description = 'Uninstall node from Uniconfig'

        class WorkerInput(TaskInput):
            node_id: str
            connection_type: Literal['netconf', 'cli']
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, task: Task) -> TaskResult:
            response = uninstall_node(**task.input_data)
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())
