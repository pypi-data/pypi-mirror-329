from textual.app import ComposeResult
from textual.containers import Center, Container, Vertical
from textual.widgets import ProgressBar, Static

from sentinalmon.models.metrics import RamMetric
from sentinalmon.models.server import ExporterInstance


def mem_template(metric: RamMetric) -> str:
    return f"""
    Total: {metric.total_memory}
    Available: {metric.available_memory}
    Used: {metric.used_memory}
    Usage: {metric.memory_usage}%
    """


class RamDisplay(Static):
    def update(self, metric: RamMetric) -> None:
        super().update(
            f"""[bold]Total:[/bold] {metric.total_memory} [bold]Available:[/bold] {metric.available_memory} [bold]Used:[/bold] {metric.used_memory} [bold]Usage:[/bold] {metric.memory_usage}%
        """
        )


class SwapDisplay(Static):
    def update(self, metric: RamMetric) -> None:
        super().update(
            f"""[bold]Total:[/bold] {metric.total_swap} [bold]Used:[/bold] {metric.used_swap} [bold]Usage:[/bold] {metric.swap_usage}%
        """
        )


class MemoryView(Container):
    def __init__(self, instance: ExporterInstance, id: str | None = None):
        super().__init__(id=id)
        self.instance = instance

    def compose(self) -> ComposeResult:
        yield Container(
            Vertical(
                Static("Ram:", classes="core-title"),
                RamDisplay(id="mem-container"),
                Center(ProgressBar(id="mem-bar", total=100, show_eta=False)),
                classes="mem-box",
            ),
            Vertical(
                Static("Swap:", classes="core-title"),
                SwapDisplay(id="swap-container"),
                Center(ProgressBar(id="swap-bar", total=100, show_eta=False)),
                classes="mem-box",
            ),
            id="memory-container",
        )

    def update(self, metric: RamMetric):
        self.query_one("#mem-container", RamDisplay).update(metric)
        self.query_one("#mem-bar", ProgressBar).update(progress=metric.memory_usage)
        self.query_one("#swap-container", SwapDisplay).update(metric)
        self.query_one("#swap-bar", ProgressBar).update(progress=metric.swap_usage)
