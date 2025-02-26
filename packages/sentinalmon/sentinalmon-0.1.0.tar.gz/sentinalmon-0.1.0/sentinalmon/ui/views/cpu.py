from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static

from sentinalmon.models.metrics import CpuMetric
from sentinalmon.models.server import ExporterInstance
from sentinalmon.ui.master_client import MasterClient


class CPU(Container):
    def __init__(
        self, instance: ExporterInstance, client: MasterClient, id: str | None = None
    ):
        super().__init__(id=id)
        self.instance = instance
        self.client = client

    def compose(self) -> ComposeResult:
        yield Static(id="cpu_stats", classes="value centered")
        yield Container(id="cores-container")

    def on_mount(self):
        metric = self.client.get_metrics(self.instance.id)
        if metric is None:
            return
        cpu_metric = metric.cpu
        cores_container = self.query_one("#cores-container")
        for core in range(cpu_metric.num_cores):
            cores_container.mount(
                Vertical(
                    Static(f"Core {core}", classes="core-title"),
                    Static("Core Usage: 0.0%", id=f"core-{core}", classes="core-usage"),
                    Static("Clock: ", id=f"core-clock-{core}", classes="core-usage"),
                    classes="core-box",
                )
            )

    def update(self, metric: CpuMetric):
        self.query_one("#cpu_stats", Static).update(
            f"[bold]CPU Name:[/bold] {metric.cpu_name} "
            f"[bold]Architecture:[/bold] {metric.architecture} "
            f"[bold]Cores#:[/bold] {metric.num_cores} "
            f"[bold]CPU Usage:[/bold] {metric.usage_percent:.2f}% "
        )
        for core in metric.cores:
            self.query_one(f"#core-{core.core_id}", Static).update(
                f"Core Usage: {core.usage_percent:.2f}%"
            )
            self.query_one(f"#core-clock-{core.core_id}", Static).update(
                f"Clock: {core.clock_speed}"
            )
