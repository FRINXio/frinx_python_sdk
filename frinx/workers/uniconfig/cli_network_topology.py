from typing import Any

from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.worker.service import ServiceWorkersImpl
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.worker.worker import WorkerImpl
from frinx.services.uniconfig.cli_network_topology import execute
from frinx.services.uniconfig.cli_network_topology import execute_and_read


class CliNetworkTopology(ServiceWorkersImpl):
    class ExecuteAndRead(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Execute_and_read_RPC'
            description = 'Run execute and read RPC'

        class WorkerInput(TaskInput):
            node_id: str
            command: str
            transaction_id: str
            uniconfig_server_id: str | None = None
            wait_for_output: int = 0
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, worker_input: WorkerInput) -> TaskResult:
            response = execute_and_read(
                node_id=worker_input.node_id,
                command=worker_input.command,
                transaction_id=worker_input.transaction_id,
                uniconfig_server_id=worker_input.uniconfig_server_id,
                wait_for_output=worker_input.wait_for_output,
                uniconfig_url_base=worker_input.uniconfig_url_base
            )
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())

    class Execute(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = 'Execute_RPC'
            description = 'Run execute RPC'
            labels = ['UNICONFIG']

        class WorkerInput(TaskInput):
            node_id: str
            command: str
            transaction_id: str
            uniconfig_server_id: str | None = None
            uniconfig_url_base: str | None = None

        class WorkerOutput(TaskOutput):
            output: dict[str, Any]

        def execute(self, worker_input: WorkerInput) -> TaskResult:
            response = execute(
                node_id=worker_input.node_id,
                command=worker_input.command,
                transaction_id=worker_input.transaction_id,
                uniconfig_server_id=worker_input.uniconfig_server_id,
                uniconfig_url_base=worker_input.uniconfig_url_base
            )
            return TaskResult(status=TaskResultStatus.COMPLETED, output=response.json())
