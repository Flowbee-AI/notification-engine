import time
from typing import Dict, List
from dataclasses import dataclass
from collections import defaultdict
import statistics


@dataclass
class Metric:
    count: int = 0
    total_time: float = 0.0
    values: List[float] = None

    def __post_init__(self):
        if self.values is None:
            self.values = []


class Metrics:
    def __init__(self):
        self._counters: Dict[str, int] = defaultdict(int)
        self._metrics: Dict[str, Metric] = defaultdict(Metric)
        self._start_time = time.time()

    def increment(self, name: str, value: int = 1) -> None:
        """Increment a counter metric"""
        self._counters[name] += value

    def record_processing_time(self, duration: float) -> None:
        """Record a processing time metric"""
        metric = self._metrics["processing_time"]
        metric.count += 1
        metric.total_time += duration
        metric.values.append(duration)

    def get_counter(self, name: str) -> int:
        """Get the current value of a counter"""
        return self._counters.get(name, 0)

    def get_metric_stats(self, name: str) -> Dict[str, float]:
        """Get statistics for a metric"""
        metric = self._metrics.get(name)
        if not metric or not metric.values:
            return {
                "count": 0,
                "total": 0.0,
                "mean": 0.0,
                "median": 0.0,
                "p95": 0.0,
                "p99": 0.0,
            }

        return {
            "count": metric.count,
            "total": metric.total_time,
            "mean": statistics.mean(metric.values),
            "median": statistics.median(metric.values),
            "p95": statistics.quantiles(metric.values, n=20)[18],
            "p99": statistics.quantiles(metric.values, n=100)[98],
        }

    def get_uptime(self) -> float:
        """Get the service uptime in seconds"""
        return time.time() - self._start_time

    def reset(self) -> None:
        """Reset all metrics"""
        self._counters.clear()
        self._metrics.clear()
        self._start_time = time.time()


# Global metrics instance
metrics = Metrics()
