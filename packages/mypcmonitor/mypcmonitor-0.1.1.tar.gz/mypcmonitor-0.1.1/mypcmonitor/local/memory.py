from rich.console import RenderableType
from textual.app import ComposeResult, RenderResult
from textual.containers import Container, Center, Vertical, Horizontal, Middle
from textual.visual import Visual, visualize, SupportsVisual, VisualType
from textual.widget import Widget
from textual.widgets import Static, Markdown, ProgressBar

from mypcmonitor.local import mem_collector
from mypcmonitor.models.metrics import RamMetric


def mem_template(metric: RamMetric) -> str:
    return f"""
    Total: {metric.total_memory}
    Available: {metric.available_memory}
    Used: {metric.used_memory}
    Usage: {metric.memory_usage}%
    """

class RamDisplay(Static):
    def update(self, metric: RamMetric) -> None:
        super().update(f"""[bold]Total:[/bold] {metric.total_memory} [bold]Available:[/bold] {metric.available_memory} [bold]Used:[/bold] {metric.used_memory} [bold]Usage:[/bold] {metric.memory_usage}%
        """)

class SwapDisplay(Static):
    def update(self, metric: RamMetric) -> None:
        super().update(f"""[bold]Total:[/bold] {metric.total_swap} [bold]Used:[/bold] {metric.used_swap} [bold]Usage:[/bold] {metric.swap_usage}%
        """)

class MemoryView(Container):
    def compose(self) -> ComposeResult:
        yield Container(
            Vertical(
                Static("Ram:", classes="core-title"),
                RamDisplay(id="mem-container"),
                Center(ProgressBar(id="mem-bar", total=100, show_eta=False)),
                classes="mem-box"
            ),
            Vertical(
                Static("Swap:", classes="core-title"),
                SwapDisplay(id="swap-container"),
                Center(ProgressBar(id="swap-bar", total=100, show_eta=False)),
                classes="mem-box"
            ), id="memory-container")

    def on_mount(self):
        self.set_interval(1, self.update_stats)

    def update_stats(self):
        mem_metric = mem_collector.get_metrics()
        self.query_one("#mem-container", RamDisplay).update(mem_metric)
        self.query_one("#mem-bar", ProgressBar).update(progress=mem_metric.memory_usage)
        self.query_one("#swap-container", SwapDisplay).update(mem_metric)
        self.query_one("#swap-bar", ProgressBar).update(progress=mem_metric.swap_usage)