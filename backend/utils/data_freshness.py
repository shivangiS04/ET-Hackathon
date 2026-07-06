"""
Data Freshness Tracking Utility
Tracks when data was last updated and provides freshness metadata
"""

from datetime import datetime
from typing import Dict, Any
import threading


class DataFreshnessTracker:
    """
    Track data freshness across different data sources.
    Provides metadata about data age and freshness status.
    """
    
    # Singleton instance
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._data_sources: Dict[str, Dict[str, Any]] = {}
        self._refresh_intervals = {
            "battery_health": 5,      # 5 minutes
            "supply_chain": 15,       # 15 minutes
            "fleet_data": 10,         # 10 minutes
            "predictions": 30,        # 30 minutes
            "analytics": 60           # 60 minutes
        }
    
    def register_source(self, source_name: str, refresh_interval_minutes: int = 15):
        """Register a data source with its refresh interval"""
        self._data_sources[source_name] = {
            "last_updated": datetime.now(),
            "refresh_interval": refresh_interval_minutes,
            "update_count": 0
        }
    
    def update_source(self, source_name: str):
        """Update the last refresh time for a data source"""
        if source_name not in self._data_sources:
            self.register_source(source_name)
        
        self._data_sources[source_name]["last_updated"] = datetime.now()
        self._data_sources[source_name]["update_count"] += 1
    
    def get_freshness(self, source_name: str) -> Dict[str, Any]:
        """Get freshness metadata for a data source"""
        if source_name not in self._data_sources:
            return {
                "status": "UNKNOWN",
                "age_minutes": None,
                "last_updated": None,
                "within_sla": False,
                "message": "Data source not registered"
            }
        
        source = self._data_sources[source_name]
        last_updated = source["last_updated"]
        age_minutes = (datetime.now() - last_updated).total_seconds() / 60
        refresh_interval = source["refresh_interval"]
        
        if age_minutes < refresh_interval * 0.5:
            status = "FRESH"
        elif age_minutes < refresh_interval:
            status = "STALE"
        else:
            status = "OLD"
        
        return {
            "status": status,
            "age_minutes": int(age_minutes),
            "last_updated": last_updated.isoformat(),
            "within_sla": status in ["FRESH", "STALE"],
            "refresh_interval_minutes": refresh_interval
        }
    
    def get_all_freshness(self) -> Dict[str, Dict[str, Any]]:
        """Get freshness for all registered data sources"""
        return {
            source: self.get_freshness(source)
            for source in self._data_sources.keys()
        }
    
    def get_global_freshness(self) -> Dict[str, Any]:
        """Get overall system freshness status"""
        all_freshness = self.get_all_freshness()
        
        if not all_freshness:
            return {
                "status": "NO_DATA",
                "overall_within_sla": False,
                "sources_tracked": 0
            }
        
        fresh_count = sum(1 for f in all_freshness.values() if f.get("status") == "FRESH")
        stale_count = sum(1 for f in all_freshness.values() if f.get("status") == "STALE")
        old_count = sum(1 for f in all_freshness.values() if f.get("status") == "OLD")
        
        if old_count > 0:
            overall_status = "CRITICAL"
        elif stale_count > 0:
            overall_status = "WARNING"
        else:
            overall_status = "HEALTHY"
        
        return {
            "status": overall_status,
            "overall_within_sla": old_count == 0,
            "sources_tracked": len(all_freshness),
            "fresh_count": fresh_count,
            "stale_count": stale_count,
            "old_count": old_count,
            "timestamp": datetime.now().isoformat()
        }


# Global singleton instance
_freshness_tracker: DataFreshnessTracker = None


def get_freshness_tracker() -> DataFreshnessTracker:
    """Get the global freshness tracker instance"""
    global _freshness_tracker
    if _freshness_tracker is None:
        _freshness_tracker = DataFreshnessTracker()
    return _freshness_tracker


def get_standard_freshness_metadata() -> Dict[str, Any]:
    """
    Get standard freshness metadata for API responses.
    This provides a consistent freshness indicator across all endpoints.
    """
    tracker = get_freshness_tracker()
    global_freshness = tracker.get_global_freshness()
    
    status_to_sla = {
        "HEALTHY": True,
        "WARNING": True,
        "CRITICAL": False,
        "NO_DATA": False
    }
    
    return {
        "status": global_freshness.get("status", "UNKNOWN"),
        "age_minutes": 23,  # Default placeholder
        "last_updated": datetime.now().isoformat(),
        "within_sla": status_to_sla.get(global_freshness.get("status", "UNKNOWN"), True)
    }