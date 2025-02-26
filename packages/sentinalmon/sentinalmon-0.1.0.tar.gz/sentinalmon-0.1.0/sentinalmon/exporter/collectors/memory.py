import psutil

from sentinalmon.collectors import BaseMetricCollector
from sentinalmon.models.metrics import RamMetric


class MemoryMetricCollector(BaseMetricCollector[RamMetric]):

    def _collect(self) -> None:
        while not self._stop_event.is_set():
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            mem_metric = RamMetric(
                total_memory=mem.total,
                available_memory=mem.available,
                used_memory=mem.used,
                memory_usage=mem.percent,
                total_swap=swap.total,
                used_swap=swap.used,
                swap_usage=swap.percent,
            )
            with self._thread_lock:
                self.metric = mem_metric
                self._metric_ready.set()
            self._stop_event.wait(timeout=self.interval)
