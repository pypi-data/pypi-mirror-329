from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Label, Static, TabbedContent

from sentinalmon.models.metrics import DiskMetric, PartitionMetric, StorageMetric
from sentinalmon.models.server import ExporterInstance
from sentinalmon.ui.master_client import MasterClient


class DriveDisplay(Static):
    def update(self, metric: DiskMetric) -> None:
        super().update(
            f"[bold]Type:[/bold] {str(metric.disk_type)}\n"
            f"[bold]Size:[/bold] {metric.capacity}\n"
            f"[bold]Read:[/bold] {metric.read_speed}\n"
            f"[bold]Write:[/bold] {metric.write_speed}\n"
            f"[bold]IOPS:[/bold] {metric.iops}"
        )


class PartitionDisplay(Static):
    def update(self, metric: PartitionMetric) -> None:
        super().update(
            f"[bold]Size:[/bold] {metric.capacity}\n"
            f"[bold]Used:[/bold] {metric.used_space}\n"
            f"[bold]Free:[/bold] {metric.free_space}\n"
            f"[bold]Usage:[/bold] {metric.usage_percent}%\n"
            f"[bold]Mount point:[/bold] {metric.mount_point}\n"
            f"[bold]Filesystem:[/bold] {metric.filesystem_type}"
        )


class StorageView(Container):
    def __init__(
        self, instance: ExporterInstance, client: MasterClient, id: str | None = None
    ):
        super().__init__(id=id)
        self.instance = instance
        self.client = client

    def compose(self) -> ComposeResult:
        with TabbedContent("Disks", "Partitions"):
            yield Container(id="disks-container")
            yield Container(id="parts-container")

    def on_mount(self):
        metric = self.client.get_metrics(self.instance.id)
        if metric is None:
            return
        storage_metric = metric.storage
        disks_container = self.query_one("#disks-container")
        parts_container = self.query_one("#parts-container")
        for disk in storage_metric.disks:
            disks_container.mount(
                Vertical(
                    Label(disk.disk_name, classes="core-title"),
                    DriveDisplay(id=disk.disk_name),
                    classes="disk-box",
                )
            )
        for part in storage_metric.partitions:
            parts_container.mount(
                Vertical(
                    Label(part.partition_name, classes="core-title"),
                    PartitionDisplay(id=part.partition_name),
                    classes="part-box",
                )
            )

    def update(self, metric: StorageMetric):
        for disk in metric.disks:
            self.query_one(f"#{disk.disk_name}", DriveDisplay).update(disk)
        for part in metric.partitions:
            self.query_one(f"#{part.partition_name}", PartitionDisplay).update(part)
