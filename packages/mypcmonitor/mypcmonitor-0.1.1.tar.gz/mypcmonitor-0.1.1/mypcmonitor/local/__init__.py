from mypcmonitor.core.cpu import CpuMetricCollector
from mypcmonitor.core.memory import MemoryMetricCollector
from mypcmonitor.core.storage import StorageMetricCollector

cpu_collector = CpuMetricCollector()
mem_collector = MemoryMetricCollector()
storage_collector = StorageMetricCollector()