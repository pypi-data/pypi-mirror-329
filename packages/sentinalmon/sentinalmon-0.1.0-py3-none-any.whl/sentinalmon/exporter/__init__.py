from sentinalmon.models.metrics import (
    CpuMetric,
    NetworkMetric,
    RamMetric,
    StorageMetric,
)

metric_endpoint_map = {
    CpuMetric: "cpu",
    RamMetric: "memory",
    StorageMetric: "storage",
    NetworkMetric: "network",
    "cpu": CpuMetric,
    "memory": RamMetric,
    "storage": StorageMetric,
    "network": NetworkMetric,
}
