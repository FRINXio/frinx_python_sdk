from typing import Any

from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.worker.task import Task
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.worker.worker import WorkerImpl
from frinx.common.workflow.workflow import WorkflowImpl
from frinx.common.workflow.workflow import WorkflowInputField


class MockWorker(WorkerImpl):
    class WorkerDefinition(TaskDefinition):
        name = 'MockWorker'
        description = 'Helper class used in tests.'

    class WorkerInput(TaskInput): ...

    class WorkerOutput(TaskOutput): ...

    def execute(self, worker_input: WorkerInput) -> TaskResult:
        return TaskResult(status=TaskResultStatus.COMPLETED)


class MockWorkflow(WorkflowImpl):
    name = 'MockWorkflow'
    version = 1
    description = 'Helper class used in tests.'
    
    class WorkflowInput(WorkflowImpl.WorkflowInput):
        device_name = WorkflowInputField(name='device_name')
        zone = WorkflowInputField(name='zone')

    class WorkflowOutput(WorkflowImpl.WorkflowOutput): ...

    def workflow_builder(self, workflow_inputs: WorkflowInput) -> None: ...
