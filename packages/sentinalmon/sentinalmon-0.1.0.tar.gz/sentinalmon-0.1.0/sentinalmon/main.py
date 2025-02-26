import typer

from sentinalmon.exporter.server import Exporter, ServerConfig
from sentinalmon.master.server import Master
from sentinalmon.ui.main import PcMonitor
from sentinalmon.ui.master_client import MasterClient

app = typer.Typer()


@app.command()
def exporter(
    master_host: str = "0.0.0.0",
    master_port: int = 8001,
    host: str = "0.0.0.0",
    port: int = 8000,
    hostname: str = None,
):
    config = ServerConfig(ip_addr=master_host, port=master_port)
    server = Exporter(config, host, port, hostname)
    server.start()


@app.command(name="client")
def textual_ui(master_host: str = "0.0.0.0", master_port: int = 8001):
    client = MasterClient(host=master_host, port=master_port)
    tui = PcMonitor(client)
    tui.run()


@app.command()
def master(host: str = "0.0.0.0", port: int = 8001):
    server = Master(host, port)
    server.start()


if __name__ == "__main__":
    app()
