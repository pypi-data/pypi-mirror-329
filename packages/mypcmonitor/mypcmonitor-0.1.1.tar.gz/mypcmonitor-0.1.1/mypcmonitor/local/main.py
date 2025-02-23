from typing import Iterable

from textual.app import App, SystemCommand, ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, TabbedContent

from mypcmonitor.local import cpu_collector, mem_collector
from mypcmonitor.local.cpu import CPU
from mypcmonitor.local.memory import MemoryView

class PcMonitor(App):
    CSS_PATH = "main.tcss"
    """An app with a 'bell' command."""

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)
        yield SystemCommand("Bell", "Ring the bell", self.bell)

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent("CPU", "Memory", "Storage", "Network"):
            yield CPU()
            yield MemoryView()
            yield Container()
            yield Container()
        yield Footer()

def main():
    app = PcMonitor()
    cpu_collector.start()
    mem_collector.start()
    app.run()
    cpu_collector.stop()
    mem_collector.stop()
