"""
Test configuration and fixtures for EV Supply Chain & Asset Intelligence Platform
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)


@pytest.fixture
def sample_vehicle_data():
    """Sample vehicle operational data for testing"""
    return {
        "vehicle_id": "TEST_001",
        "vehicle_type": "urban",
        "current_fuel": "diesel",
        "daily_distance_km": 120,
        "payload_capacity_kg": 3000,
        "dwell_time_hours": 6,
        "annual_utilization_hours": 2200,
        "current_age_years": 5
    }


@pytest.fixture
def sample_charge_history():
    """Sample charge history for battery testing"""
    return [
        {"current_a": 100, "temperature_c": 28, "voltage_v": 3.7, "timestamp": "2024-12-01T10:00:00"},
        {"current_a": 120, "temperature_c": 32, "voltage_v": 3.65, "timestamp": "2024-12-02T10:00:00"},
        {"current_a": 180, "temperature_c": 38, "voltage_v": 3.6, "timestamp": "2024-12-03T10:00:00"},  # Fast charge
        {"current_a": 90, "temperature_c": 25, "voltage_v": 3.72, "timestamp": "2024-12-04T10:00:00"},
        {"current_a": 200, "temperature_c": 42, "voltage_v": 3.55, "timestamp": "2024-12-05T10:00:00"},  # Fast charge + hot
    ]


@pytest.fixture
def sample_supplier_data():
    """Sample supplier data for supply chain testing"""
    return [
        {
            "supplier_id": "LTH_001",
            "supplier_name": "Test Lithium Supplier",
            "country": "China",
            "material": "Lithium",
            "risk_score": 78,
            "concentration_percentage": 45,
            "defect_rate_ppm": 250,
            "on_time_delivery_percent": 94,
            "invoice_accuracy_percent": 99.2
        },
        {
            "supplier_id": "COB_002",
            "supplier_name": "Test Cobalt Supplier",
            "country": "DR Congo",
            "material": "Cobalt",
            "risk_score": 82,
            "concentration_percentage": 60,
            "defect_rate_ppm": 350,
            "on_time_delivery_percent": 88,
            "invoice_accuracy_percent": 97.5
        }
    ]


@pytest.fixture
def sample_geopolitical_event():
    """Sample geopolitical event for testing"""
    return {
        "event_id": "GEO_001",
        "country": "China",
        "event_type": "sanctions",
        "severity": "high",
        "impact_on_supply": 0.75,
        "affected_materials": ["Lithium", "Rare Earths"],
        "description": "New trade restrictions announced"
    }


@pytest.fixture
def sample_fleet_data():
    """Sample fleet data for testing"""
    return {
        "fleet_size": 58,
        "vehicles_by_readiness": {
            "ready": 42,
            "conditional": 12,
            "not_ready": 4
        },
        "available_budget_inr": 200_000_000
    }
