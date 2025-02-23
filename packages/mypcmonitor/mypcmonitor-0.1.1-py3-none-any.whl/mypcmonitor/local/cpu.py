from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static

from mypcmonitor.local import cpu_collector


class CPU(Container):
    def compose(self) -> ComposeResult:
        yield Static(id="cpu_stats", classes="value centered")
        yield Container(id="cores-container")

    def on_mount(self):
        cpu_metric = cpu_collector.get_metrics()
        cores_container = self.query_one("#cores-container")
        for core in range(cpu_metric.num_cores):
            cores_container.mount(
                Vertical(
                    Static(f"Core {core}", classes="core-title"),
                    Static("Core Usage: 0.0%", id=f"core-{core}", classes="core-usage"),
                    Static("Clock: ", id=f"core-clock-{core}", classes="core-usage"),
                    classes="core-box"
                )
            )
        self.set_interval(1, self.update_stats)


    def update_stats(self) -> None:
        cpu_metric = cpu_collector.get_metrics()
        # CPU
        self.query_one("#cpu_stats", Static).update(f"[bold]CPU Name:[/bold] {cpu_metric.cpu_name} "
                                                   f"[bold]Architecture:[/bold] {cpu_metric.architecture} "
                                                   f"[bold]Cores#:[/bold] {cpu_metric.num_cores} "
                                                   f"[bold]CPU Usage:[/bold] {cpu_metric.usage_percent:.2f}% ")
        for core in cpu_metric.cores:
            self.query_one(f"#core-{core.core_id}", Static).update(f"Core Usage: {core.usage_percent:.2f}%")
            self.query_one(f"#core-clock-{core.core_id}", Static).update(f"Clock: {core.clock_speed}")
