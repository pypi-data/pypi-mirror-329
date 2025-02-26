from typing import Iterable

from textual.app import App, ComposeResult, SystemCommand
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Header, OptionList, TabbedContent
from textual.widgets._option_list import Option

from sentinalmon.models.server import ExporterInstance
from sentinalmon.ui.master_client import MasterClient
from sentinalmon.ui.views.cpu import CPU
from sentinalmon.ui.views.memory import MemoryView
from sentinalmon.ui.views.network import NetworkView
from sentinalmon.ui.views.storage import StorageView


class InstanceMonitor(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Exit")]

    def __init__(self, instance: ExporterInstance, client: MasterClient):
        super().__init__()
        self.instance = instance
        self.client = client

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent("CPU", "Memory", "Storage", "Network"):
            yield CPU(
                instance=self.instance, id=f"cpu-{self.instance.id}", client=self.client
            )
            yield MemoryView(instance=self.instance, id=f"memory-{self.instance.id}")
            yield StorageView(
                instance=self.instance,
                id=f"storage-{self.instance.id}",
                client=self.client,
            )
            yield NetworkView(
                instance=self.instance,
                id=f"network-{self.instance.id}",
                client=self.client,
            )
        yield Footer()

    def on_mount(self):
        self.update()
        self.set_interval(1, self.update)

    def update(self):
        metric = self.client.get_metrics(self.instance.id)
        if metric is None:
            return
        self.query_one(f"#cpu-{self.instance.id}", CPU).update(metric.cpu)
        self.query_one(f"#memory-{self.instance.id}", MemoryView).update(metric.memory)
        self.query_one(f"#storage-{self.instance.id}", StorageView).update(
            metric.storage
        )
        self.query_one(f"#network-{self.instance.id}", NetworkView).update(
            metric.network
        )


class InstanceSelector(Screen):
    def __init__(self, client: MasterClient):
        super().__init__()
        self.client = client
        self.instances = None
        self.timer = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield OptionList(id="instance-selector")
        yield Footer()

    def on_mount(self):
        self.instances = self.client.get_instances()
        if self.instances:
            for instance in self.instances:
                option = Option(instance.hostname, id=instance.id)
                self.query_one("#instance-selector", OptionList).add_option(option)
        self.update_options()
        self.timer = self.set_interval(3, self.update_options)

    def update_options(self):
        now_instances = self.client.get_instances()
        if now_instances is None:
            self.notify(
                "Retrying in 3 seconds..", title="Master offline", severity="error"
            )
            self.query_one("#instance-selector", OptionList).clear_options()
            self.instances = None
            return
        if self.instances is None:
            self.instances = now_instances
            for instance in self.instances:
                option = Option(instance.hostname, id=instance.id)
                self.query_one("#instance-selector", OptionList).add_option(option)
            return
        old_ids = {instance.id for instance in self.instances}
        new_ids = {instance.id for instance in now_instances}

        # Remove old instances
        for instance in self.instances:
            if instance.id not in new_ids:
                self.query_one("#instance-selector", OptionList).remove_option(
                    instance.id
                )

        # Add new instances
        for instance in now_instances:
            if instance.id not in old_ids:
                option = Option(instance.hostname, id=instance.id)
                self.query_one("#instance-selector", OptionList).add_option(option)

        self.instances = now_instances

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        instance_id = event.option_id
        instance = self.client.get_instance(instance_id)
        self.app.push_screen(InstanceMonitor(instance, self.client))


class PcMonitor(App):
    CSS_PATH = "main.tcss"
    """An app with a 'bell' command."""
    BINDINGS = [("i", "app.switch_screen('selector')", "InstanceSelector")]

    def __init__(self, client):
        super().__init__()
        self.client = client

    def on_mount(self) -> None:
        self.install_screen(InstanceSelector(self.client), name="selector")
        self.push_screen("selector")

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)
        yield SystemCommand("Bell", "Ring the bell", self.bell)
