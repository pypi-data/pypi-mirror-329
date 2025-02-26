import platform
import re
import subprocess

import psutil

from sentinalmon.collectors import BaseMetricCollector
from sentinalmon.models.metrics import CoreMetric, CpuMetric
from sentinalmon.utils import DefaultList


class CpuMetricCollector(BaseMetricCollector[CpuMetric]):
    def _cpu_name(self) -> str:
        cpu_name = platform.processor()
        if self.system == "Darwin":
            cpu_name = (
                subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"])
                .strip()
                .decode()
            )
        elif self.system == "Linux":
            result = subprocess.run(["lscpu"], capture_output=True, text=True)
            pattern = r"Model name:\s*(.*) @"
            match = re.search(pattern, result.stdout)
            cpu_name = match.group(1) if match else None
        return cpu_name

    @staticmethod
    def _cpu_freq() -> list[int]:
        freq_per_cpu = psutil.cpu_freq(percpu=True)
        # According psutil docs, per cpu freq available only in linux and freebsd systems.
        # So all the cores in different os, will have whole cpu freq
        cpu_freqs = DefaultList(default_value=freq_per_cpu[0].current)
        cpu_freqs.extend([cpu.current for cpu in freq_per_cpu])
        return cpu_freqs

    def _cpu_temp(self) -> float:
        # Sensors available only in Linux and FreeBSD
        if self.system == "FreeBSD" or self.system == "Linux":
            return psutil.sensors_temperatures()["coretemp"][0].current
        return 0.0

    def _collect(self) -> None:
        # Without interval, the first call for cpu stats return None according to psutil documentation
        psutil.cpu_percent(interval=None, percpu=True)
        num_cores = psutil.cpu_count()
        while not self._stop_event.is_set():
            cores = list()
            cpu_usage = psutil.cpu_percent(percpu=True)
            cpu_freq = self._cpu_freq()
            for idx in range(num_cores):
                cores.append(
                    CoreMetric(
                        core_id=idx,
                        usage_percent=cpu_usage[idx],
                        clock_speed=cpu_freq[idx],
                    )
                )

            pass
            cpu_metric = CpuMetric(
                cpu_name=self._cpu_name(),
                architecture=platform.machine(),
                num_cores=psutil.cpu_count(),
                usage_percent=sum(cpu_usage) / len(cpu_usage),
                clock_speed=sum(cpu_freq) / len(cpu_freq),
                temperature=self._cpu_temp(),
                cores=cores,
            )
            with self._thread_lock:
                self.metric = cpu_metric
                self._metric_ready.set()
            self._stop_event.wait(timeout=self.interval)
