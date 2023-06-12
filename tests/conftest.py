"""
IMPORTANT !!!
Use only in tests until new features are implemented to replace these code.
"""

from enum import Enum
from typing import Any
from typing import Optional
from pydantic import Field

from frinx.common.worker.service import ServiceWorkersImpl
from frinx.common.worker.task import Task
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.worker.worker import WorkerImpl
from frinx.common.workflow.service import ServiceWorkflowsImpl
from frinx.common.workflow.task import DecisionCaseValueTask
from frinx.common.workflow.task import DecisionCaseValueTaskInputParameters
from frinx.common.workflow.task import SimpleTask
from frinx.common.workflow.task import WorkflowTaskImpl
from frinx.common.workflow.task import TaskType
from frinx.common.workflow.task import SimpleTaskInputParameters
from frinx.common.workflow.task import TerminateTask
from frinx.common.workflow.task import TerminateTaskInputParameters
from frinx.common.conductor_enums import WorkflowStatus
from frinx.common.workflow.workflow import FrontendWFInputFieldType
from frinx.common.workflow.workflow import WorkflowImpl
from frinx.common.workflow.workflow import WorkflowInputField


class Http(ServiceWorkersImpl):
    ###############################################################################

    class HttpTask(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "HTTP_task"
            description = "Generic http task"
            labels = ["BASIC", "HTTP"]
            timeout_seconds = 360
            response_timeout_seconds = 360

        class WorkerInput(TaskInput):
            http_request: Optional[str | dict[str, Any]]

        class WorkerOutput(TaskOutput):
            response: Any
            body: Any
            status_code: int = Field(..., alias="statusCode")
            cookies: dict[str, Any]

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)


class Inventory(ServiceWorkersImpl):
    ###############################################################################

    class InventoryGetDevicesInfo(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_get_device_info"
            description = "get a list of pages cursors from device inventory"
            labels = ["BASIC", "INVENTORY"]

        class WorkerInput(TaskInput):
            device_name: str

        class WorkerOutput(TaskOutput):
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################

    class InventoryInstallDeviceById(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_install_device_by_id"
            description = "Install device by device ID"
            labels = ["BASIC", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            device_id: Optional[str]

        class WorkerOutput(TaskOutput):
            url: str
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################

    class InventoryUninstallDeviceById(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_uninstall_device_by_id"
            description = "Uninstall device by device ID"
            labels = ["BASIC", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            device_id: Optional[str]

        class WorkerOutput(TaskOutput):
            url: str
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################
    class InventoryInstallDeviceByName(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_install_device_by_name"
            description = "Install device by device name"
            labels = ["BASIC", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            device_name: str

        class WorkerOutput(TaskOutput):
            url: str
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################

    class InventoryUninstallDeviceByName(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_uninstall_device_by_name"
            description = "Uninstall device by device name"
            labels = ["BASIC", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            device_name: Optional[str]

        class WorkerOutput(TaskOutput):
            url: str
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################

    class InventoryGetLabels(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_get_labels"
            description = "Get device labels"
            labels = ["BASICS", "MAIN", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            ...

        class WorkerOutput(TaskOutput):
            url: str
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################

    class InventoryCreateLabel(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_create_label"
            description = "Create device labels"
            labels = ["BASICS", "MAIN", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            label: str

        class WorkerOutput(TaskOutput):
            url: str
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################

    class InventoryAddDevice(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_add_device"
            description = "Add device to inventory database"
            labels = ["BASICS", "MAIN", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            device_name: str
            zone: str
            service_state: str
            mount_body: str
            vendor: Optional[str]
            model: Optional[str]
            device_size: Optional[str]
            labels: Optional[str]

        class WorkerOutput(TaskOutput):
            url: str
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################
    class InventoryGetPagesCursors(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_get_pages_cursors"
            description = "Get a list of pages cursors from device inventory"
            labels = ["BASIC", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            labels: Optional[str]

        class WorkerOutput(TaskOutput):
            labels: str
            url: str
            response_code: str
            page_ids_count: str
            page_size: str
            page_ids: str

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################

    class InventoryGetAllDevicesAsDynamicForkTask(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_get_all_devices_as_dynamic_fork_tasks"
            description = "Get all devices as dynamic fork task"
            labels = ["BASIC", "INVENTORY"]

        class WorkerInput(TaskInput):
            labels: Optional[str]
            task: str
            task_params: dict[str, Any]
            optional: bool = False

        class WorkerOutput(TaskOutput):
            url: str
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################
    class InventoryGetPagesCursorsForkTasks(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_get_pages_cursors_fork_tasks"
            description = "Get all pages cursors as dynamic fork tasks"
            labels = ["BASIC", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            task: str
            page_ids: str
            labels: Optional[str]

        class WorkerOutput(TaskOutput):
            url: str
            response_code: int
            response_body: Any

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################

    class InventoryInstallInBatch(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_install_in_batch"
            description = "Install devices in batch started from page cursor"
            labels = ["BASIC", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            page_size: str
            page_id: str
            labels: Optional[str]

        class WorkerOutput(TaskOutput):
            url: str
            dynamic_tasks_i: str
            dynamic_tasks: str

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)

    ###############################################################################

    class InventoryUninstallInBatch(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name = "INVENTORY_uninstall_in_batch"
            description = "Uninstall devices in batch started from page cursor"
            labels = ["BASIC", "INVENTORY"]
            timeout_seconds = 3600
            response_timeout_seconds = 3600

        class WorkerInput(TaskInput):
            page_size: int
            page_id: str
            labels: Optional[str]

        class WorkerOutput(TaskOutput):
            url: str
            dynamic_tasks_i: str
            dynamic_tasks: str

        def execute(self, task: Task) -> TaskResult:
            return TaskResult(status=TaskResultStatus.COMPLETED)


class ServiceState(str, Enum):
    PLANNING = "PLANNING"
    IN_SERVICE = "IN_SERVICE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def list(cls) -> list[str]:
        return [x.value for x in list(cls.__members__.values())]


class DeviceSize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def list(cls) -> list[str]:
        return [x.value for x in list(cls.__members__.values())]


class InventoryWorkflows(ServiceWorkflowsImpl):
    class InstallDeviceByName(WorkflowImpl):
        name = "Install_device_by_name"
        version = 1
        description = "Install device from device inventory by device name"
        restartable = False
        schema_version = 2
        labels = ["BASICS", "INVENTORY"]

        class WorkflowInput(WorkflowImpl.WorkflowInput):
            device_name = WorkflowInputField(
                name="device_name",
                frontend_default_value="IOS01",
                description="Device name from Device Inventory",
                type=FrontendWFInputFieldType.STRING,
            )

        class WorkflowOutput(WorkflowImpl.WorkflowOutput):
            url: str
            response_code: str
            response_body: dict[str, Any]

        def workflow_builder(self, workflow_inputs: WorkflowImpl.WorkflowInput) -> None:
            self.tasks.append(
                SimpleTask(
                    type=TaskType.SIMPLE,
                    name=Inventory.InventoryInstallDeviceByName,
                    task_reference_name="Install_device_by_name",
                    input_parameters=SimpleTaskInputParameters(
                        device_name="${workflow.input.device_name}"
                    ),
                )
            )

    class UninstallDeviceByName(WorkflowImpl):
        name = "Uninstall_device_by_name"
        version = 1
        description = "Uninstall device from device inventory by device name"
        restartable = False
        schema_version = 2
        labels = ["BASICS", "INVENTORY"]

        class WorkflowInput(WorkflowImpl.WorkflowInput):
            device_name = WorkflowInputField(
                name="device_name",
                frontend_default_value="IOS01",
                description="Device name from Device Inventory",
                type=FrontendWFInputFieldType.STRING,
            )

        class WorkflowOutput(WorkflowImpl.WorkflowOutput):
            url: str
            response_code: str
            response_body: dict[str, Any]

        def workflow_builder(self, workflow_inputs: WorkflowImpl.WorkflowInput) -> None:
            self.tasks.append(
                SimpleTask(
                    type=TaskType.SIMPLE,
                    name=Inventory.InventoryUninstallDeviceByName,
                    task_reference_name="Uninstall_device_by_name",
                    input_parameters=SimpleTaskInputParameters(
                        device_name="${workflow.input.device_name}"
                    ),
                )
            )

    class InstallDeviceById(WorkflowImpl):
        name = "Install_device_by_id"
        version = 1
        description = "Install device from device inventory by device id"
        restartable = False
        schema_version = 2
        labels = ["BASICS", "INVENTORY"]

        class WorkflowInput(WorkflowImpl.WorkflowInput):
            device_id = WorkflowInputField(
                name="device_id",
                frontend_default_value="IOS01",
                description="Device name from Device Inventory",
                type=FrontendWFInputFieldType.STRING,
            )

        class WorkflowOutput(WorkflowImpl.WorkflowOutput):
            url: str
            response_code: str
            response_body: dict[str, Any]

        def workflow_builder(self, workflow_inputs: WorkflowImpl.WorkflowInput) -> None:
            self.tasks.append(
                SimpleTask(
                    type=TaskType.SIMPLE,
                    name=Inventory.InventoryUninstallDeviceById,
                    task_reference_name="Install_device_by_id",
                    input_parameters=SimpleTaskInputParameters(
                        device_id="${workflow.input.device_id}"
                    ),
                )
            )

    class UninstallDeviceById(WorkflowImpl):
        name = "Uninstall_device_by_id"
        version = 1
        description = "Uninstall device from device inventory by device id"
        restartable = False
        schema_version = 2
        labels = ["BASICS", "INVENTORY"]

        class WorkflowInput(WorkflowImpl.WorkflowInput):
            device_id = WorkflowInputField(
                name="device_id",
                frontend_default_value="IOS01",
                description="Device name from Device Inventory",
                type=FrontendWFInputFieldType.STRING,
            )

        class WorkflowOutput(WorkflowImpl.WorkflowOutput):
            url: str
            response_code: str
            response_body: dict[str, Any]

        def workflow_builder(self, workflow_inputs: WorkflowImpl.WorkflowInput) -> None:
            self.tasks.append(
                SimpleTask(
                    type=TaskType.SIMPLE,
                    name=Inventory.InventoryUninstallDeviceById,
                    task_reference_name="Uninstall_device_by_id",
                    input_parameters=SimpleTaskInputParameters(
                        device_id="${workflow.input.device_id}"
                    ),
                )
            )

    class AddDeviceToInventory(WorkflowImpl):
        name = "Add_device_to_inventory"
        version = 1
        description = "Add device to inventory"
        restartable = True
        schema_version = 2
        labels = ["BASICS", "INVENTORY"]
        update_time = 2
        workflow_status_listener_enabled = True

        class WorkflowInput(WorkflowImpl.WorkflowInput):
            device_name = WorkflowInputField(
                name="device_name",
                frontend_default_value="IOS01",
                description="Device name",
                type=FrontendWFInputFieldType.STRING,
            )

            zone = WorkflowInputField(
                name="zone",
                frontend_default_value="uniconfig",
                description="Deployment zone",
                type=FrontendWFInputFieldType.STRING,
            )

            service_state = WorkflowInputField(
                name="service_state",
                frontend_default_value=ServiceState.IN_SERVICE,
                description="Device service state",
                type=FrontendWFInputFieldType.SELECT,
                options=ServiceState.list(),
            )

            mount_body = WorkflowInputField(
                name="mount_body",
                frontend_default_value=None,
                description="Device mount body",
                type=FrontendWFInputFieldType.TEXTAREA,
            )

            vendor = WorkflowInputField(
                name="vendor",
                frontend_default_value=None,
                description="Device vendor",
                type=FrontendWFInputFieldType.STRING,
            )

            model = WorkflowInputField(
                name="model",
                frontend_default_value=None,
                description="Device model",
                type=FrontendWFInputFieldType.STRING,
            )

            device_size = WorkflowInputField(
                name="device_size",
                frontend_default_value=DeviceSize.MEDIUM,
                description="Device size",
                type=FrontendWFInputFieldType.SELECT,
                options=DeviceSize.list(),
            )

            labels = WorkflowInputField(
                name="labels",
                frontend_default_value=None,
                description="Device status",
                type=FrontendWFInputFieldType.STRING,
            )

            install = WorkflowInputField(
                name="install",
                frontend_default_value=False,
                description="Install device",
                type=FrontendWFInputFieldType.TOGGLE,
            )

        class WorkflowOutput(WorkflowImpl.WorkflowOutput):
            url: str
            response_code: str
            response_body: dict[str, Any]

        def workflow_builder(self, workflow_inputs: WorkflowImpl.WorkflowInput) -> None:
            add_device = SimpleTask(
                type=TaskType.SIMPLE,
                name=Inventory.InventoryAddDevice,
                task_reference_name="Add_device_to_inventory",
                input_parameters=SimpleTaskInputParameters(
                    device_name="${workflow.input.device_name}",
                    zone="${workflow.input.zone}",
                    service_state="${workflow.input.service_state}",
                    mount_body="${workflow.input.mount_body}",
                    vendor="${workflow.input.vendor}",
                    model="${workflow.input.model}",
                    device_size="${workflow.input.device_size}",
                    labels="${workflow.input.labels}",
                ),
            )

            default_tasks: list[WorkflowTaskImpl] = [
                TerminateTask(
                    type=TaskType.TERMINATE,
                    name="skip_install",
                    task_reference_name="skip_install",
                    input_parameters=TerminateTaskInputParameters(
                        termination_reason=None,
                        termination_status=WorkflowStatus.COMPLETED,
                        workflow_output={"a": "b"},
                    ),
                )
            ]

            true_tasks: list[WorkflowTaskImpl] = [
                SimpleTask(
                    type=TaskType.SIMPLE,
                    name=Inventory.InventoryInstallDeviceById,
                    task_reference_name="Add_device_to_inventory.output.response_body.add_device.device.id",
                    input_parameters=SimpleTaskInputParameters(
                        device_id="${Add_device_to_inventory.output.response_body.addDevice.device.id}"
                    ),
                )
            ]

            self.tasks.append(add_device)

            self.tasks.append(
                (
                    DecisionCaseValueTask(
                        type=TaskType.DECISION,
                        name="decisionTask",
                        task_reference_name="decisionTask",
                        case_value_param="install",
                        decision_cases={"true": true_tasks},
                        default_case=default_tasks,
                        input_parameters=DecisionCaseValueTaskInputParameters(
                            case_value_param="${workflow.input.install}"
                        ),
                    )
                )
            )
