from typing import Generic, TypeVar

import requests

from sentinalmon.collectors import BaseMetricCollector
from sentinalmon.exporter import metric_endpoint_map
from sentinalmon.models.server import ExporterInstance

T = TypeVar("T")


class RemoteMetricCollector(BaseMetricCollector[T], Generic[T]):
    def __init__(
        self, instance: ExporterInstance, metric_class, endpoint="", interval: int = 1
    ):
        super().__init__(interval=1)
        self.instance = instance
        self.endpoint = metric_endpoint_map[metric_class]
        self.metric_class = metric_class

    def _collect(self) -> None:
        while not self._stop_event.is_set():
            # Get metrics from remote instance
            try:
                metric = self._get_remote_metrics()
            except requests.RequestException as e:
                print(f"Collector {T} of {self.instance.hostname} stop working: \n{e}")
                self._stop_event.wait(timeout=3)
                continue
            with self._thread_lock:
                self.metric = metric
                self._metric_ready.set()
            self._stop_event.wait(timeout=self.interval)

    def _get_remote_metrics(self):
        url = f"http://{self.instance.ip_addr}:{self.instance.port}/metric/{self.endpoint}"
        response = requests.get(url)
        return self.metric_class(**response.json())
