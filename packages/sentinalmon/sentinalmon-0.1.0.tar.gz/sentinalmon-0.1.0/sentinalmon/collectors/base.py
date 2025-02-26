import platform
import threading
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from sentinalmon.models import CpuMetric, NetworkMetric, RamMetric, StorageMetric

T = TypeVar("T")


class BaseMetricCollector(ABC, Generic[T]):
    def __init__(self, interval: int = 1):
        self.metric: Optional[T] = None
        self.interval = interval
        self._thread: Optional[threading.Thread] = None
        self._thread_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._metric_ready = threading.Event()
        self.system = platform.system()

    @abstractmethod
    def _collect(self) -> None:
        pass

    def start(self) -> None:
        if not self._thread or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._collect, daemon=True)
            self._thread.start()

    def stop(self, wait=False) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive() and wait:
            self._thread.join()

    def is_running(self) -> bool:
        if self._thread:
            return self._thread.is_alive()
        else:
            return False

    def get_metrics(self) -> T:
        self._metric_ready.wait()
        with self._thread_lock:
            return self.metric


class InstanceCollectors:
    def __init__(
        self,
        cpu: BaseMetricCollector[CpuMetric],
        memory: BaseMetricCollector[RamMetric],
        storage: BaseMetricCollector[StorageMetric],
        network: BaseMetricCollector[NetworkMetric],
    ):
        self.cpu: BaseMetricCollector[CpuMetric] = cpu
        self.memory: BaseMetricCollector[RamMetric] = memory
        self.storage: BaseMetricCollector[StorageMetric] = storage
        self.network: BaseMetricCollector[NetworkMetric] = network
        self._collectors = [cpu, memory, storage, network]
        self.started = False

    def start(self) -> None:
        print("Starting collectors")

        for collector in self._collectors:
            collector.start()

        self.started = True
        print("Collectors started successfully")

    def stop(self, wait: bool = False) -> None:
        print("Stopping collectors")

        for collector in self._collectors:
            collector.stop(wait=wait)

        print("Collectors stopped successfully")

    def is_running(self) -> bool:
        if not self.started:
            return False

        return all([collector.is_running() for collector in self._collectors])

    def get_collectors_status(self) -> dict[str, bool]:
        """
        Get the running status of all collectors.
        Returns a dictionary with collector names and their status.
        """
        return {
            "cpu": self.cpu.is_running(),
            "memory": self.memory.is_running(),
            "storage": self.storage.is_running(),
            "network": self.network.is_running(),
        }

    def get_metrics(self):
        if not self.started:
            print("Attempted to get metrics before collectors were started")
            return None

        return {
            "cpu": self.cpu.get_metrics(),
            "memory": self.memory.get_metrics(),
            "storage": self.storage.get_metrics(),
            "network": self.network.get_metrics(),
        }
