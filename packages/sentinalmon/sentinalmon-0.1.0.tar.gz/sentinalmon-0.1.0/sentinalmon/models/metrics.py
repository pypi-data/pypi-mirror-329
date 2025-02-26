"""
This module defines metric models for CPU, RAM, and disk metrics.
"""

from enum import Enum

from pydantic.dataclasses import dataclass


@dataclass
class CoreMetric:
    core_id: int
    usage_percent: float
    clock_speed: float


@dataclass
class CpuMetric:
    cpu_name: str
    architecture: str
    num_cores: int
    usage_percent: float
    clock_speed: float
    temperature: float
    cores: list[CoreMetric]


@dataclass
class RamMetric:
    total_memory: int
    available_memory: int
    used_memory: int
    memory_usage: float
    total_swap: int
    used_swap: int
    swap_usage: float


class DiskType(Enum):
    HDD = "HardDisk"
    SSD = "SolidStateDrive"
    NVME = "NVMe"
    UNKNOWN = "Unknown"


@dataclass
class PartitionMetric:
    partition_name: str
    capacity: int
    used_space: int
    free_space: int
    usage_percent: float
    mount_point: str
    filesystem_type: str


@dataclass
class DiskMetric:
    disk_name: str
    disk_type: DiskType
    read_speed: int
    write_speed: int
    iops: int
    capacity: int


@dataclass
class StorageMetric:
    disks: list[DiskMetric]
    partitions: list[PartitionMetric]


@dataclass
class NetworkInterfaceMetric:
    interface_name: str
    ip_address: str | None
    mac_address: str | None
    total_rx: int
    total_tx: int
    rx_speed: int
    tx_speed: int
    packet_lost_percent: float


@dataclass
class NetworkMetric:
    total_rx: int
    total_tx: int
    rx_speed: int
    tx_speed: int
    nics: list[NetworkInterfaceMetric]


@dataclass
class InstanceMetric:
    cpu: CpuMetric
    memory: RamMetric
    storage: StorageMetric
    network: NetworkMetric
