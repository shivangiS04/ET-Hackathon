"""
Response Optimization & Formatting Utilities
Provides consistent response structures and data compression
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import json


class ResponseStatus(str, Enum):
    """Standard response statuses"""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"
    PROCESSING = "processing"


class APIResponse:
    """Standard API response wrapper"""
    
    def __init__(
        self,
        status: ResponseStatus = ResponseStatus.SUCCESS,
        data: Optional[Any] = None,
        message: str = "",
        error: Optional[str] = None,
        metadata: Optional[Dict] = None,
        timestamp: Optional[str] = None
    ):
        self.status = status
        self.data = data
        self.message = message
        self.error = error
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert response to dictionary"""
        response = {
            "status": self.status.value,
            "timestamp": self.timestamp,
            "message": self.message,
        }
        
        if self.data is not None:
            response["data"] = self.data
        
        if self.error:
            response["error"] = self.error
        
        if self.metadata:
            response["metadata"] = self.metadata
        
        return response


class DataCompressionUtils:
    """Utilities for data compression and optimization"""
    
    @staticmethod
    def filter_fields(data: Dict, fields: List[str]) -> Dict:
        """
        Filter dictionary to only include specified fields.
        Reduces response payload size.
        
        Args:
            data: Input dictionary
            fields: List of field names to include
        
        Returns:
            Filtered dictionary
        """
        return {k: v for k, v in data.items() if k in fields}
    
    @staticmethod
    def truncate_decimals(data: Any, decimal_places: int = 2) -> Any:
        """
        Truncate all float values to specified decimal places.
        Reduces response size while maintaining precision.
        """
        if isinstance(data, float):
            return round(data, decimal_places)
        elif isinstance(data, dict):
            return {k: DataCompressionUtils.truncate_decimals(v, decimal_places) 
                    for k, v in data.items()}
        elif isinstance(data, list):
            return [DataCompressionUtils.truncate_decimals(item, decimal_places) 
                    for item in data]
        else:
            return data
    
    @staticmethod
    def compress_response(data: Dict, max_keys: int = 100) -> Dict:
        """
        Compress response by removing low-value fields and truncating lists.
        
        Args:
            data: Response data
            max_keys: Maximum number of items in lists
        
        Returns:
            Compressed response
        """
        compressed = {}
        
        for key, value in data.items():
            if isinstance(value, list) and len(value) > max_keys:
                # Truncate list and add metadata
                compressed[key] = value[:max_keys]
                compressed[f"{key}_count"] = len(value)
                compressed[f"{key}_truncated"] = True
            elif isinstance(value, dict):
                compressed[key] = DataCompressionUtils.compress_response(value, max_keys)
            else:
                compressed[key] = value
        
        return compressed


class PaginationUtils:
    """Utilities for response pagination"""
    
    @staticmethod
    def paginate(
        items: List[Any],
        page: int = 1,
        page_size: int = 20
    ) -> Dict:
        """
        Paginate list of items.
        
        Args:
            items: List of items to paginate
            page: Page number (1-indexed)
            page_size: Number of items per page
        
        Returns:
            Paginated result with metadata
        """
        total = len(items)
        total_pages = (total + page_size - 1) // page_size
        
        # Validate page number
        page = max(1, min(page, total_pages)) if total_pages > 0 else 1
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_items = items[start_idx:end_idx]
        
        return {
            "items": paginated_items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        }


class PerformanceMetrics:
    """Track API performance metrics"""
    
    def __init__(self):
        self.endpoint_times = {}
        self.error_counts = {}
        self.request_counts = {}
    
    def record_endpoint_call(self, endpoint: str, duration_ms: float):
        """Record endpoint call duration"""
        if endpoint not in self.endpoint_times:
            self.endpoint_times[endpoint] = []
        self.endpoint_times[endpoint].append(duration_ms)
    
    def record_error(self, endpoint: str, error_type: str):
        """Record error occurrence"""
        key = f"{endpoint}:{error_type}"
        self.error_counts[key] = self.error_counts.get(key, 0) + 1
    
    def record_request(self, endpoint: str):
        """Record request"""
        self.request_counts[endpoint] = self.request_counts.get(endpoint, 0) + 1
    
    def get_stats(self, endpoint: str) -> Dict:
        """Get statistics for an endpoint"""
        times = self.endpoint_times.get(endpoint, [])
        
        if not times:
            return {
                "endpoint": endpoint,
                "requests": 0,
                "avg_time_ms": 0,
                "max_time_ms": 0,
                "min_time_ms": 0
            }
        
        return {
            "endpoint": endpoint,
            "requests": self.request_counts.get(endpoint, 0),
            "avg_time_ms": round(sum(times) / len(times), 2),
            "max_time_ms": max(times),
            "min_time_ms": min(times),
            "p95_time_ms": sorted(times)[int(len(times) * 0.95)] if len(times) > 20 else max(times),
            "errors": sum(1 for k in self.error_counts.keys() if k.startswith(endpoint))
        }
    
    def get_all_stats(self) -> Dict:
        """Get statistics for all endpoints"""
        stats = {}
        for endpoint in self.endpoint_times.keys():
            stats[endpoint] = self.get_stats(endpoint)
        return stats


# Global performance metrics instance
_perf_metrics = PerformanceMetrics()


def get_performance_metrics() -> PerformanceMetrics:
    """Get global performance metrics instance"""
    return _perf_metrics
