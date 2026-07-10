"""
Pytest configuration and fixtures for entire test suite
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app
from services.battery_service import BatteryService
from services.quality_intelligence_service import QualityIntelligenceService
from services.carbon_tracking_service import CarbonTrackingService
from services.geospatial_service import GeospatialService
from services.supply_chain_traceability_service import SupplyChainTraceabilityService


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def battery_service():
    """Battery service instance"""
    return BatteryService()


@pytest.fixture
def quality_service():
    """Quality intelligence service instance"""
    return QualityIntelligenceService()


@pytest.fixture
def carbon_service():
    """Carbon tracking service instance"""
    return CarbonTrackingService()


@pytest.fixture
def geospatial_service():
    """Geospatial service instance"""
    return GeospatialService()


@pytest.fixture
def supply_chain_service():
    """Supply chain traceability service instance"""
    return SupplyChainTraceabilityService()


@pytest.fixture
def sample_charge_history():
    """Sample battery charge history data"""
    return [
        {
            "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
            "charge_percent": 85 - (i * 5),
            "voltage_v": 3.7 - (i * 0.05),
            "current_a": 10 + (i * 0.5),
            "temperature_c": 25 + (i * 0.2)
        }
        for i in range(10)
    ]


@pytest.fixture
def sample_process_params():
    """Sample manufacturing process parameters"""
    return {
        "cell_voltage": 3.15,
        "resistance": 0.035,
        "temperature_during_charge": 28.5,
        "cycle_efficiency": 99.2
    }


@pytest.fixture
def sample_material_quality():
    """Sample material quality data"""
    return {
        "lithium": {"purity": 99.8, "impurity_ppm": 20},
        "cobalt": {"purity": 99.5, "impurity_ppm": 50},
        "nickel": {"purity": 99.2, "impurity_ppm": 80}
    }


@pytest.fixture
def sample_inspection_results():
    """Sample inspection results"""
    return {
        "visual_inspection": {"passed": True, "defects": 0},
        "voltage_test": {"passed": True, "min_voltage": 3.0, "max_voltage": 3.3},
        "resistance_test": {"passed": True, "max_resistance": 0.05},
        "thermal_test": {"passed": True, "temp_range": (15, 45)}
    }
