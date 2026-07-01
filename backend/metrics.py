"""
Prometheus Metrics Endpoint - Production-Grade Observability
Exposes platform metrics in Prometheus format for monitoring and alerting
"""

import time
from datetime import datetime
from typing import Dict, Any
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collects and exposes platform metrics in Prometheus format"""
    
    def __init__(self):
        """Initialize metrics collector"""
        self.request_count = defaultdict(int)  # endpoint -> count
        self.request_duration = defaultdict(list)  # endpoint -> [durations]
        self.error_count = defaultdict(int)  # error_type -> count
        self.cache_hits = 0
        self.cache_misses = 0
        self.start_time = time.time()
        self.requests_total = 0
        self.errors_total = 0
    
    def record_request(self, endpoint: str, duration_ms: float, status_code: int):
        """Record an API request"""
        self.request_count[endpoint] += 1
        self.request_duration[endpoint].append(duration_ms)
        self.requests_total += 1
        
        if status_code >= 400:
            self.errors_total += 1
    
    def record_error(self, error_type: str):
        """Record an error"""
        self.error_count[error_type] += 1
    
    def record_cache_hit(self):
        """Record cache hit"""
        self.cache_hits += 1
    
    def record_cache_miss(self):
        """Record cache miss"""
        self.cache_misses += 1
    
    def get_metrics_prometheus(self) -> str:
        """
        Export metrics in Prometheus text format
        
        Returns:
            String in Prometheus exposition format
        """
        uptime_seconds = time.time() - self.start_time
        
        lines = []
        
        # HELP and TYPE metadata
        lines.append("# HELP ev_platform_uptime_seconds Platform uptime in seconds")
        lines.append("# TYPE ev_platform_uptime_seconds gauge")
        lines.append(f"ev_platform_uptime_seconds {uptime_seconds}")
        lines.append("")
        
        lines.append("# HELP ev_requests_total Total API requests processed")
        lines.append("# TYPE ev_requests_total counter")
        lines.append(f"ev_requests_total {self.requests_total}")
        lines.append("")
        
        lines.append("# HELP ev_errors_total Total errors encountered")
        lines.append("# TYPE ev_errors_total counter")
        lines.append(f"ev_errors_total {self.errors_total}")
        lines.append("")
        
        lines.append("# HELP ev_cache_hits_total Total cache hits")
        lines.append("# TYPE ev_cache_hits_total counter")
        lines.append(f"ev_cache_hits_total {self.cache_hits}")
        lines.append("")
        
        lines.append("# HELP ev_cache_misses_total Total cache misses")
        lines.append("# TYPE ev_cache_misses_total counter")
        lines.append(f"ev_cache_misses_total {self.cache_misses}")
        lines.append("")
        
        # Cache hit rate
        total_cache = self.cache_hits + self.cache_misses
        if total_cache > 0:
            hit_rate = (self.cache_hits / total_cache) * 100
        else:
            hit_rate = 0
        
        lines.append("# HELP ev_cache_hit_rate Cache hit rate percentage")
        lines.append("# TYPE ev_cache_hit_rate gauge")
        lines.append(f"ev_cache_hit_rate {hit_rate}")
        lines.append("")
        
        # Per-endpoint request counts
        lines.append("# HELP ev_requests_by_endpoint Request count by endpoint")
        lines.append("# TYPE ev_requests_by_endpoint counter")
        for endpoint, count in sorted(self.request_count.items()):
            lines.append(f'ev_requests_by_endpoint{{endpoint="{endpoint}"}} {count}')
        lines.append("")
        
        # Per-endpoint average response time
        lines.append("# HELP ev_response_time_ms Average response time by endpoint (milliseconds)")
        lines.append("# TYPE ev_response_time_ms gauge")
        for endpoint, durations in sorted(self.request_duration.items()):
            if durations:
                avg_duration = sum(durations) / len(durations)
                lines.append(f'ev_response_time_ms{{endpoint="{endpoint}"}} {avg_duration:.2f}')
        lines.append("")
        
        # Error counts by type
        lines.append("# HELP ev_errors_by_type Error count by type")
        lines.append("# TYPE ev_errors_by_type counter")
        for error_type, count in sorted(self.error_count.items()):
            lines.append(f'ev_errors_by_type{{error_type="{error_type}"}} {count}')
        lines.append("")
        
        # Platform health status (1 = healthy, 0 = degraded)
        health_score = 1.0 if self.errors_total < (self.requests_total * 0.05) else 0.5
        lines.append("# HELP ev_platform_health Platform health score (0-1)")
        lines.append("# TYPE ev_platform_health gauge")
        lines.append(f"ev_platform_health {health_score}")
        
        return "\n".join(lines)
    
    def get_metrics_json(self) -> Dict[str, Any]:
        """Export metrics as JSON"""
        uptime_seconds = time.time() - self.start_time
        total_cache = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_cache * 100) if total_cache > 0 else 0
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": uptime_seconds,
            "requests": {
                "total": self.requests_total,
                "by_endpoint": dict(self.request_count)
            },
            "errors": {
                "total": self.errors_total,
                "by_type": dict(self.error_count)
            },
            "cache": {
                "hits": self.cache_hits,
                "misses": self.cache_misses,
                "hit_rate_percent": round(hit_rate, 2)
            },
            "response_times_ms": {
                endpoint: {
                    "average": round(sum(durations) / len(durations), 2) if durations else 0,
                    "min": round(min(durations), 2) if durations else 0,
                    "max": round(max(durations), 2) if durations else 0,
                    "count": len(durations)
                }
                for endpoint, durations in self.request_duration.items()
            },
            "health": {
                "status": "healthy" if self.errors_total < (self.requests_total * 0.05) else "degraded",
                "error_rate_percent": round((self.errors_total / self.requests_total * 100) if self.requests_total > 0 else 0, 2)
            }
        }


# Global metrics instance
_metrics_collector = None


def get_metrics_collector() -> MetricsCollector:
    """Get or create global metrics collector instance"""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


# ============================================================================
# PROMETHEUS QUERY EXAMPLES
# ============================================================================
"""
Common Prometheus queries for monitoring this platform:

1. Current Request Rate (requests per second):
   rate(ev_requests_total[1m])

2. Error Rate:
   rate(ev_errors_total[1m]) / rate(ev_requests_total[1m])

3. Cache Hit Rate:
   ev_cache_hit_rate

4. API Response Time by Endpoint:
   ev_response_time_ms

5. Platform Uptime:
   ev_platform_uptime_seconds / 86400 (in days)

6. Platform Health Alert:
   ev_platform_health < 1

7. High Error Rate Alert:
   rate(ev_errors_total[5m]) > 0.05

8. Slow API Response Alert:
   ev_response_time_ms{endpoint="/api/v1/battery"} > 500
"""
