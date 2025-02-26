from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static

from sentinalmon.models import NetworkMetric
from sentinalmon.models.metrics import CpuMetric, NetworkInterfaceMetric
from sentinalmon.models.server import ExporterInstance
from sentinalmon.ui.master_client import MasterClient


class NetworkView(Container):
    def __init__(
        self, instance: ExporterInstance, client: MasterClient, id: str | None = None
    ):
        super().__init__(id=id)
        self.instance = instance
        self.client = client

    def compose(self) -> ComposeResult:
        yield Static(id="network_stats", classes="value centered")
        yield Container(id="nics-container")

    def on_mount(self):
        metric = self.client.get_metrics(self.instance.id)
        if metric is None:
            return
        network_metric = metric.network
        cores_container = self.query_one("#nics-container")
        for nic in network_metric.nics:
            cores_container.mount(
                Vertical(
                    Static(f"{nic.interface_name}", classes="core-title"),
                    Static("IP: ", id=f"ip-{nic.interface_name}", classes="core-usage"),
                    Static(
                        "MAC: ", id=f"mac-{nic.interface_name}", classes="core-usage"
                    ),
                    Static(
                        "Total Recv: ",
                        id=f"total-rx-{nic.interface_name}",
                        classes="core-usage",
                    ),
                    Static(
                        "Total Sent: ",
                        id=f"total-tx-{nic.interface_name}",
                        classes="core-usage",
                    ),
                    Static(
                        "Recv Speed: ",
                        id=f"speed-rx-{nic.interface_name}",
                        classes="core-usage",
                    ),
                    Static(
                        "Sent Speed: ",
                        id=f"speed-tx-{nic.interface_name}",
                        classes="core-usage",
                    ),
                    classes="nic-box",
                )
            )

    def update(self, metric: NetworkMetric):
        self.query_one("#network_stats", Static).update(
            f"[bold]Total Recv:[/bold] {metric.total_rx} "
            f"[bold]Total Sent:[/bold] {metric.total_tx} "
            f"[bold]Recv Speed:[/bold] {metric.rx_speed} "
            f"[bold]Sent Speed:[/bold] {metric.tx_speed}"
        )
        for nic in metric.nics:
            self.update_nic(nic)

    def update_nic(self, metric: NetworkInterfaceMetric):
        self.query_one(f"#ip-{metric.interface_name}", Static).update(
            f"IP: {metric.ip_address}"
        )
        self.query_one(f"#mac-{metric.interface_name}", Static).update(
            f"MAC: {metric.mac_address}"
        )
        self.query_one(f"#total-rx-{metric.interface_name}", Static).update(
            f"Total Recv: {metric.total_rx}"
        )
        self.query_one(f"#total-tx-{metric.interface_name}", Static).update(
            f"Total Recv: {metric.total_tx}"
        )
        self.query_one(f"#speed-rx-{metric.interface_name}", Static).update(
            f"Recv Speed: {metric.rx_speed}"
        )
        self.query_one(f"#speed-tx-{metric.interface_name}", Static).update(
            f"Sent Speed: {metric.tx_speed}"
        )
