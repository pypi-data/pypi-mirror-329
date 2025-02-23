import platform
import threading
import time
from typing import Optional
import psutil
from mypcmonitor.models.metrics import RamMetric


class MemoryMetricCollector:
    def __init__(self, interval:int = 1):
        self.metric = None
        self.interval = interval
        self._thread: Optional[threading.Thread] = None
        self._thread_lock = threading.Lock()
        self._stop_event = threading.Event()
        self.system = platform.system()

    def _collect_mem(self) -> None:
        while not self._stop_event.is_set():
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            mem_metric = RamMetric(
                total_memory=mem.total,
                available_memory=mem.available,
                used_memory=mem.used,
                memory_usage=mem.percent,
                total_swap=swap.total,
                used_swap=swap.used,
                swap_usage=swap.percent
            )
            with self._thread_lock:
                self.metric = mem_metric
            time.sleep(self.interval)

    def start(self):
        if not self._thread or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._collect_mem, daemon=True)
            self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join()

    def get_metrics(self):
        with self._thread_lock:
            return self.metric





