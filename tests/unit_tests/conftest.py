from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.worker.worker import WorkerImpl
from frinx.common.workflow.workflow import WorkflowImpl
from frinx.common.workflow.workflow import WorkflowInputField


class MockWorker(WorkerImpl):
    class WorkerDefinition(TaskDefinition):
        name: str = 'MockWorker'
        description: str = 'Helper class used in tests.'

    class WorkerInput(TaskInput):
        ...

    class WorkerOutput(TaskOutput):
        ...

    def execute(self, worker_input: WorkerInput) -> TaskResult[WorkerOutput]:
        return TaskResult(status=TaskResultStatus.COMPLETED)


class MockWorkflow(WorkflowImpl):
    name: str = 'MockWorkflow'
    version: int = 1
    description: str = 'Helper class used in tests.'

    class WorkflowInput(WorkflowImpl.WorkflowInput):
        device_name: WorkflowInputField = WorkflowInputField(name='device_name')
        zone: WorkflowInputField = WorkflowInputField(name='zone')

    class WorkflowOutput(WorkflowImpl.WorkflowOutput): ...

    def workflow_builder(self, workflow_inputs: WorkflowInput) -> None: ...
