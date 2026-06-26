"""
Data Validation & Sanitization Utilities
Ensures data accuracy and prevents invalid inputs
"""

from typing import Any, Dict, List, Tuple, Optional
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom validation error"""
    pass


class DataValidator:
    """Validates and sanitizes input data"""
    
    # Validation regex patterns
    PATTERNS = {
        "vehicle_id": r"^[A-Za-z0-9_-]{3,20}$",
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "phone": r"^[+]?[0-9]{7,15}$",
        "iso_date": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
    }
    
    @staticmethod
    def validate_range(
        value: float,
        min_val: float = 0,
        max_val: float = 100,
        field_name: str = "value"
    ) -> Tuple[bool, Optional[str]]:
        """Validate numeric value is within range"""
        if not isinstance(value, (int, float)):
            return False, f"{field_name} must be a number"
        
        if value < min_val or value > max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}"
        
        return True, None
    
    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]) -> Tuple[bool, Optional[str]]:
        """Validate required fields are present"""
        missing = [f for f in required_fields if f not in data or data[f] is None]
        
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"
        
        return True, None
    
    @staticmethod
    def validate_pattern(value: str, pattern_name: str) -> Tuple[bool, Optional[str]]:
        """Validate value matches pattern"""
        if pattern_name not in DataValidator.PATTERNS:
            return False, f"Unknown pattern: {pattern_name}"
        
        pattern = DataValidator.PATTERNS[pattern_name]
        if not re.match(pattern, value):
            return False, f"Invalid {pattern_name}: {value}"
        
        return True, None
    
    @staticmethod
    def validate_vehicle_data(vehicle_data: Dict) -> Tuple[bool, Optional[str]]:
        """Validate vehicle operational data"""
        required = ["vehicle_id", "vehicle_type", "daily_distance_km", "dwell_time_hours"]
        is_valid, error = DataValidator.validate_required_fields(vehicle_data, required)
        if not is_valid:
            return is_valid, error
        
        # Validate vehicle type
        valid_types = ["urban", "delivery", "long_haul", "mining", "construction"]
        if vehicle_data.get("vehicle_type") not in valid_types:
            return False, f"Invalid vehicle_type. Must be one of: {', '.join(valid_types)}"
        
        # Validate distances
        is_valid, error = DataValidator.validate_range(
            vehicle_data.get("daily_distance_km", 0),
            min_val=0,
            max_val=1000,
            field_name="daily_distance_km"
        )
        if not is_valid:
            return is_valid, error
        
        # Validate dwell time
        is_valid, error = DataValidator.validate_range(
            vehicle_data.get("dwell_time_hours", 0),
            min_val=0,
            max_val=24,
            field_name="dwell_time_hours"
        )
        if not is_valid:
            return is_valid, error
        
        return True, None
    
    @staticmethod
    def validate_battery_data(battery_data: Dict) -> Tuple[bool, Optional[str]]:
        """Validate battery health data"""
        required = ["vehicle_id", "charge_history", "current_cycles", "ambient_temp_c"]
        is_valid, error = DataValidator.validate_required_fields(battery_data, required)
        if not is_valid:
            return is_valid, error
        
        # Validate charge history is list
        if not isinstance(battery_data.get("charge_history"), list):
            return False, "charge_history must be a list"
        
        # Validate cycles
        is_valid, error = DataValidator.validate_range(
            battery_data.get("current_cycles", 0),
            min_val=0,
            max_val=10000,
            field_name="current_cycles"
        )
        if not is_valid:
            return is_valid, error
        
        # Validate ambient temperature
        is_valid, error = DataValidator.validate_range(
            battery_data.get("ambient_temp_c", 25),
            min_val=-40,
            max_val=60,
            field_name="ambient_temp_c"
        )
        if not is_valid:
            return is_valid, error
        
        return True, None
    
    @staticmethod
    def validate_supply_chain_data(supply_chain_data: Dict) -> Tuple[bool, Optional[str]]:
        """Validate supply chain data"""
        required = ["suppliers", "material"]
        is_valid, error = DataValidator.validate_required_fields(supply_chain_data, required)
        if not is_valid:
            return is_valid, error
        
        if not isinstance(supply_chain_data.get("suppliers"), list):
            return False, "suppliers must be a list"
        
        return True, None


class DataSanitizer:
    """Sanitizes and cleans input data"""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """Sanitize string input"""
        if not isinstance(value, str):
            value = str(value)
        
        # Remove leading/trailing whitespace
        value = value.strip()
        
        # Truncate if too long
        if len(value) > max_length:
            value = value[:max_length]
        
        # Remove potentially dangerous characters
        value = re.sub(r'[<>\"\'`;]', '', value)
        
        return value
    
    @staticmethod
    def sanitize_number(value: Any, min_val: float = None, max_val: float = None) -> float:
        """Sanitize numeric input"""
        try:
            num = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid number: {value}")
        
        if min_val is not None and num < min_val:
            num = min_val
        
        if max_val is not None and num > max_val:
            num = max_val
        
        return num
    
    @staticmethod
    def sanitize_dict(data: Dict, allowed_keys: List[str] = None) -> Dict:
        """
        Sanitize dictionary by removing unknown keys and sanitizing values.
        
        Args:
            data: Input dictionary
            allowed_keys: List of allowed keys. If None, all keys allowed.
        
        Returns:
            Sanitized dictionary
        """
        sanitized = {}
        
        for key, value in data.items():
            # Skip if not in allowed keys
            if allowed_keys and key not in allowed_keys:
                logger.warning(f"Skipping unknown key: {key}")
                continue
            
            # Sanitize based on type
            if isinstance(value, str):
                sanitized[key] = DataSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = DataSanitizer.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    DataSanitizer.sanitize_dict(item) if isinstance(item, dict)
                    else DataSanitizer.sanitize_string(item) if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        
        return sanitized


class RangeValidator:
    """Validates specific range of values for different domains"""
    
    # Valid ranges for different metrics
    RANGES = {
        "soh_percent": (0, 100),
        "risk_score": (0, 1),
        "confidence": (0, 1),
        "daily_distance_km": (0, 1000),
        "cycles": (0, 10000),
        "temperature_c": (-40, 60),
        "current_a": (0, 500),
        "voltage_v": (0, 500),
        "payload_kg": (0, 50000),
    }
    
    @staticmethod
    def validate(metric_name: str, value: float) -> Tuple[bool, Optional[str]]:
        """Validate value is in valid range for metric"""
        if metric_name not in RangeValidator.RANGES:
            return True, None  # No validation rule, assume valid
        
        min_val, max_val = RangeValidator.RANGES[metric_name]
        
        if value < min_val or value > max_val:
            return False, f"{metric_name} must be between {min_val} and {max_val}, got {value}"
        
        return True, None
    
    @staticmethod
    def clamp(metric_name: str, value: float) -> float:
        """Clamp value to valid range"""
        if metric_name not in RangeValidator.RANGES:
            return value
        
        min_val, max_val = RangeValidator.RANGES[metric_name]
        return max(min_val, min(value, max_val))
