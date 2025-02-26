import json
import os
import subprocess

import psutil
from psutil._common import sdiskpart

from sentinalmon.collectors import BaseMetricCollector
from sentinalmon.models.metrics import (
    DiskMetric,
    DiskType,
    PartitionMetric,
    StorageMetric,
)
from sentinalmon.utils import load_plist


class StorageMetricCollector(BaseMetricCollector[StorageMetric]):

    @staticmethod
    def _macos_drives() -> str:
        cmd = ["diskutil", "list", "-plist", "physical"]
        result = subprocess.run(cmd, capture_output=True, text=True).stdout
        data = load_plist(result)
        return data.get("WholeDisks")

    @staticmethod
    def _linux_drives():
        cmd = ["lsblk", "--json", "--output", "NAME,TYPE"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse JSON output
        devices = json.loads(result.stdout)

        # Filter only disk type devices
        disks = [
            device["name"]
            for device in devices["blockdevices"]
            if device["type"] == "disk"
        ]

        return disks

    def _get_drives(self):
        if self.system == "Darwin":
            return self._macos_drives()
        elif self.system == "Linux":
            return self._linux_drives()
        elif self.system == "Windows":
            return os.listdrives()

    def _collect(self) -> None:
        drives = self._get_drives()
        drive_collectors = {
            drive: DiskMetricCollector(drive, interval=self.interval)
            for drive in drives
        }
        for collector in drive_collectors.values():
            collector.start()
        partitions = psutil.disk_partitions()
        part_collectors = {
            part.device: PartitionMetricCollector(part.device, interval=self.interval)
            for part in partitions
        }
        for collector in part_collectors.values():
            collector.start()

        while not self._stop_event.is_set():
            storage_metric = StorageMetric(
                disks=[
                    collector.get_metrics() for collector in drive_collectors.values()
                ],
                partitions=[
                    collector.get_metrics() for collector in part_collectors.values()
                ],
            )
            with self._thread_lock:
                self.metric = storage_metric
                self._metric_ready.set()
            self._stop_event.wait(timeout=self.interval)

        for collector in drive_collectors.values():
            collector.stop()
        for collector in part_collectors.values():
            collector.stop()


class DiskMetricCollector(BaseMetricCollector[DiskMetric]):
    def __init__(self, drive: str, interval: int = 1):
        super().__init__(interval)
        self.drive = drive

    def _macos_drive_type(self) -> DiskType:
        cmd = ["diskutil", "info", "-plist", self.drive]
        result = subprocess.run(cmd, capture_output=True, text=True).stdout
        data = load_plist(result)
        return DiskType.SSD if data["SolidState"] else DiskType.HDD

    def _linux_drive_type(self) -> DiskType:
        cmd = ["lsblk", "--json", "--output", "NAME,ROTA"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        devices = json.loads(result.stdout)

        for device in devices["blockdevices"]:
            if device["name"] == self.drive:
                return DiskType.HDD if device["rota"] else DiskType.SSD

        return DiskType.UNKNOWN

    def _get_drive_type(self) -> DiskType:
        if self.system == "Darwin":
            return self._macos_drive_type()
        elif self.system == "Linux":
            return self._linux_drive_type()
        elif self.system == "Windows":
            raise NotImplementedError()
        return DiskType.UNKNOWN

    def _macos_drive_size(self) -> int:
        cmd = ["diskutil", "info", "-plist", self.drive]
        result = subprocess.run(cmd, capture_output=True, text=True).stdout
        data = load_plist(result)
        return data["TotalSize"]

    def _linux_drive_size(self) -> int:
        cmd = ["lsblk", "-b", "--json", "--output", "NAME,SIZE"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        devices = json.loads(result.stdout)

        for device in devices["blockdevices"]:
            if device["name"] == self.drive:
                return device["size"]

        return -1

    def _get_drive_size(self) -> int:
        if self.system == "Darwin":
            return self._macos_drive_size()
        elif self.system == "Linux":
            return self._linux_drive_size()
        elif self.system == "Windows":
            raise NotImplementedError()
        return -1

    def _collect(self) -> None:
        while not self._stop_event.is_set():
            io_start = psutil.disk_io_counters(perdisk=True)[self.drive]
            self._stop_event.wait(timeout=self.interval)
            io_end = psutil.disk_io_counters(perdisk=True)[self.drive]
            disk_metric = DiskMetric(
                disk_name=self.drive,
                disk_type=self._get_drive_type(),
                capacity=self._get_drive_size(),
                read_speed=int(
                    (io_end.read_bytes - io_start.read_bytes) / self.interval
                ),
                write_speed=int(
                    (io_end.write_bytes - io_start.write_bytes) / self.interval
                ),
                iops=int(
                    (
                        (io_end.read_count + io_end.write_count)
                        - (io_start.read_count + io_start.write_count)
                    )
                    / self.interval
                ),
            )

            with self._thread_lock:
                self.metric = disk_metric
                self._metric_ready.set()


class PartitionMetricCollector(BaseMetricCollector[PartitionMetric]):
    def __init__(self, device: str, interval: int = 1):
        super().__init__(interval)
        self.device = device

        partitions = psutil.disk_partitions()
        for part in partitions:
            if part.device == self.device:
                self.info: sdiskpart = part

        if not self.info:
            raise IndexError

    def _collect(self) -> None:
        while not self._stop_event.is_set():
            usage = psutil.disk_usage(self.info.mountpoint)
            part_metric = PartitionMetric(
                capacity=usage.total,
                usage_percent=usage.percent,
                partition_name=self.device.removeprefix("/dev/"),
                free_space=usage.free,
                used_space=usage.used,
                mount_point=self.info.mountpoint,
                filesystem_type=self.info.fstype,
            )

            with self._thread_lock:
                self.metric = part_metric
                self._metric_ready.set()
            self._stop_event.wait(timeout=self.interval)
