from threading import Lock
from typing import Any

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import start_wsgi_server
from prometheus_client.registry import CollectorRegistry

from frinx.common.telemetry.enums import MetricDocumentation
from frinx.common.telemetry.enums import MetricLabel
from frinx.common.telemetry.enums import MetricName
from frinx.common.telemetry.settings import MetricsSettings


class MetricsSingletonMeta(type):

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Metrics(metaclass=MetricsSingletonMeta):
    counters: dict = {}
    gauges: dict = {}
    registry: CollectorRegistry
    settings: MetricsSettings

    def __init__(self, settings: MetricsSettings = None):

        if settings is not None:
            self.settings = settings
            self.__init_collector()

    def __init_collector(self):
        if self.settings.metrics_enabled:
            self.registry = CollectorRegistry()
            start_wsgi_server(self.settings.port, registry=self.registry)

    def increment_task_poll(self, task_type: str) -> None:
        self.__increment_counter(
            name=MetricName.TASK_POLL,
            documentation=MetricDocumentation.TASK_POLL,
            labels={MetricLabel.TASK_TYPE: task_type},
        )

    def increment_task_execution_queue_full(self, task_type: str) -> None:
        self.__increment_counter(
            name=MetricName.TASK_EXECUTION_QUEUE_FULL,
            documentation=MetricDocumentation.TASK_EXECUTION_QUEUE_FULL,
            labels={MetricLabel.TASK_TYPE: task_type},
        )

    def increment_uncaught_exception(self):
        self.__increment_counter(
            name=MetricName.THREAD_UNCAUGHT_EXCEPTION,
            documentation=MetricDocumentation.THREAD_UNCAUGHT_EXCEPTION,
            labels={},
        )

    def increment_task_poll_error(self, task_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.TASK_POLL_ERROR,
            documentation=MetricDocumentation.TASK_POLL_ERROR,
            labels={MetricLabel.TASK_TYPE: task_type, MetricLabel.EXCEPTION: str(exception)},
        )

    def increment_task_paused(self, task_type: str) -> None:
        self.__increment_counter(
            name=MetricName.TASK_PAUSED,
            documentation=MetricDocumentation.TASK_PAUSED,
            labels={
                MetricLabel.TASK_TYPE: task_type
            }
        )

    def increment_task_execution_error(self, task_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.TASK_EXECUTE_ERROR,
            documentation=MetricDocumentation.TASK_EXECUTE_ERROR,
            labels={MetricLabel.TASK_TYPE: task_type, MetricLabel.EXCEPTION: str(exception)},
        )

    def increment_task_ack_failed(self, task_type: str) -> None:
        self.__increment_counter(
            name=MetricName.TASK_ACK_FAILED,
            documentation=MetricDocumentation.TASK_ACK_FAILED,
            labels={
                MetricLabel.TASK_TYPE: task_type
            }
        )

    def increment_task_ack_error(self, task_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.TASK_ACK_ERROR,
            documentation=MetricDocumentation.TASK_ACK_ERROR,
            labels={
                MetricLabel.TASK_TYPE: task_type,
                MetricLabel.EXCEPTION: str(exception)
            }
        )

    def increment_task_update_error(self, task_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.TASK_UPDATE_ERROR,
            documentation=MetricDocumentation.TASK_UPDATE_ERROR,
            labels={
                MetricLabel.TASK_TYPE: task_type,
                MetricLabel.EXCEPTION: str(exception)
            }
        )

    def increment_external_payload_used(self, entity_name: str, operation: str, payload_type: str) -> None:
        self.__increment_counter(
            name=MetricName.EXTERNAL_PAYLOAD_USED,
            documentation=MetricDocumentation.EXTERNAL_PAYLOAD_USED,
            labels={
                MetricLabel.ENTITY_NAME: entity_name,
                MetricLabel.OPERATION: operation,
                MetricLabel.PAYLOAD_TYPE: payload_type
            }
        )

    def increment_workflow_start_error(self, workflow_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.WORKFLOW_START_ERROR,
            documentation=MetricDocumentation.WORKFLOW_START_ERROR,
            labels={
                MetricLabel.WORKFLOW_TYPE: workflow_type,
                MetricLabel.EXCEPTION: str(exception)
            }
        )

    def record_workflow_input_payload_size(self, workflow_type: str, version: str, payload_size: int) -> None:
        self.__record_gauge(
            name=MetricName.WORKFLOW_INPUT_SIZE,
            documentation=MetricDocumentation.WORKFLOW_INPUT_SIZE,
            labels={
                MetricLabel.WORKFLOW_TYPE: workflow_type,
                MetricLabel.WORKFLOW_VERSION: version
            },
            value=payload_size
        )

    def record_task_result_payload_size(self, task_type: str, payload_size: int) -> None:
        self.__record_gauge(
            name=MetricName.TASK_RESULT_SIZE,
            documentation=MetricDocumentation.TASK_RESULT_SIZE,
            labels={MetricLabel.TASK_TYPE: task_type},
            value=payload_size,
        )

    def record_task_poll_time(self, task_type: str, time_spent: float) -> None:
        self.__record_gauge(
            name=MetricName.TASK_POLL_TIME,
            documentation=MetricDocumentation.TASK_POLL_TIME,
            labels={
                MetricLabel.TASK_TYPE: task_type
            },
            value=time_spent
        )

    def record_task_execute_time(self, task_type: str, time_spent: float) -> None:
        self.__record_gauge(
            name=MetricName.TASK_EXECUTE_TIME,
            documentation=MetricDocumentation.TASK_EXECUTE_TIME,
            labels={MetricLabel.TASK_TYPE: task_type},
            value=time_spent,
        )

    def __increment_counter(
            self, name: MetricName, documentation: MetricDocumentation, labels: dict[MetricLabel, str]
    ) -> None:

        if self.settings.metrics_enabled:
            counter = self.__get_counter(
                name=name, documentation=documentation, label_names=list(labels.keys())
            )
            counter.labels(*labels.values()).inc()

    def __record_gauge(
            self,
            name: MetricName,
            documentation: MetricDocumentation,
            labels: dict[MetricLabel, str],
            value: Any,
    ) -> None:
        if self.settings.metrics_enabled:
            gauge = self.__get_gauge(
                name=name, documentation=documentation, label_names=list(labels.keys())
            )
            gauge.labels(*labels.values()).set(value)

    def __get_counter(
            self, name: MetricName, documentation: MetricDocumentation, label_names: list[MetricLabel]
    ) -> Counter:
        if self.settings.metrics_enabled:
            if name not in self.counters:
                self.counters[name] = self.__generate_counter(name, documentation, label_names)
            return self.counters[name]

    def __get_gauge(
            self, name: MetricName, documentation: MetricDocumentation, label_names: list[MetricLabel]
    ) -> Gauge:
        if self.settings.metrics_enabled:
            if name not in self.gauges:
                self.gauges[name] = self.__generate_gauge(name, documentation, label_names)
            return self.gauges[name]

    def __generate_counter(
            self, name: MetricName, documentation: MetricDocumentation, label_names: list[MetricLabel]
    ) -> Counter:
        if self.settings.metrics_enabled:
            return Counter(
                name=name, documentation=documentation, labelnames=label_names, registry=self.registry
            )

    def __generate_gauge(
            self, name: MetricName, documentation: MetricDocumentation, label_names: list[MetricLabel]
    ) -> Gauge:
        if self.settings.metrics_enabled:
            return Gauge(
                name=name, documentation=documentation, labelnames=label_names, registry=self.registry
            )
