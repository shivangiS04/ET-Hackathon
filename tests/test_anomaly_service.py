"""
Test cases for Anomaly Service
Tests anomaly detection algorithms and alerting logic
"""

import pytest
from services.anomaly_service import AnomalyDetectionService, Anomaly


class TestAnomalyDetectionService:
    """Test suite for anomaly detection service"""
    
    def test_detect_anomalies_basic(self):
        """Test basic anomaly detection with fleet and supply chain data"""
        service = AnomalyDetectionService()
        
        fleet_data = {
            "vehicles": [
                {
                    "id": "V001",
                    "battery": {"soh_percent": 85, "age_months": 24, "rulf_days": 1200},
                    "readiness_score": 75,
                    "region": "North"
                },
                {
                    "id": "V002",
                    "battery": {"soh_percent": 92, "age_months": 12, "rulf_days": 2000},
                    "readiness_score": 85,
                    "region": "North"
                }
            ]
        }
        
        supply_chain_data = {
            "overall_risk_score": 0.65,
            "suppliers": [
                {"market_share_percent": 40},
                {"market_share_percent": 35}
            ]
        }
        
        result = service.detect_anomalies(fleet_data, supply_chain_data)
        
        assert isinstance(result, list)
    
    def test_detect_battery_anomalies(self):
        """Test battery anomaly detection"""
        service = AnomalyDetectionService()
        
        fleet_data = {
            "vehicles": [
                {
                    "id": "V001",
                    "battery": {"soh_percent": 60, "age_months": 12, "rulf_days": 45},  # Fast degradation
                    "readiness_score": 50
                },
                {
                    "id": "V002",
                    "battery": {"soh_percent": 95, "age_months": 12, "rulf_days": 2000},
                    "readiness_score": 90
                }
            ]
        }
        
        anomalies = service._detect_battery_anomalies(fleet_data)
        
        # May detect fast degradation anomaly
        assert isinstance(anomalies, list)
    
    def test_detect_supply_chain_anomalies_high_risk(self):
        """Test supply chain anomaly detection with high risk"""
        service = AnomalyDetectionService()
        
        supply_chain_data = {
            "overall_risk_score": 0.85,
            "suppliers": [
                {"market_share_percent": 55},
                {"market_share_percent": 25}
            ]
        }
        
        anomalies = service._detect_supply_chain_anomalies(supply_chain_data)
        
        # Should detect high risk and single dependency
        assert isinstance(anomalies, list)
        assert len(anomalies) > 0  # Should have anomalies due to high risk and concentration
    
    def test_detect_fleet_anomalies_low_readiness(self):
        """Test fleet anomaly detection with low readiness"""
        service = AnomalyDetectionService()
        
        fleet_data = {
            "vehicles": [
                {"readiness_score": 45, "region": "South"},
                {"readiness_score": 50, "region": "South"},
                {"readiness_score": 55, "region": "South"}
            ]
        }
        
        anomalies = service._detect_fleet_anomalies(fleet_data)
        
        assert isinstance(anomalies, list)
    
    def test_detect_infrastructure_anomalies(self):
        """Test infrastructure anomaly detection"""
        service = AnomalyDetectionService()
        
        fleet_data = {
            "vehicles": [
                {"readiness_score": 85} for _ in range(50)
            ]
        }
        
        anomalies = service._detect_infrastructure_anomalies(fleet_data)
        
        assert isinstance(anomalies, list)
    
    def test_get_active_anomalies(self):
        """Test getting active anomalies"""
        service = AnomalyDetectionService()
        
        # Add some test data first
        fleet_data = {
            "vehicles": [
                {"id": "V001", "battery": {"soh_percent": 85, "age_months": 24, "rulf_days": 1200}}
            ]
        }
        supply_chain_data = {"overall_risk_score": 0.5, "suppliers": []}
        
        service.detect_anomalies(fleet_data, supply_chain_data)
        
        active = service.get_active_anomalies()
        
        assert isinstance(active, list)
    
    def test_acknowledge_anomaly(self):
        """Test acknowledging an anomaly"""
        service = AnomalyDetectionService()
        
        result = service.acknowledge_anomaly("TEST_ANOMALY_001")
        
        assert result is True
    
    def test_calculate_std_dev(self):
        """Test standard deviation calculation"""
        values = [10, 12, 14, 16, 18]
        mean = 14
        
        std_dev = AnomalyDetectionService._calculate_std_dev(values, mean)
        
        assert std_dev > 0
        assert isinstance(std_dev, float)


class TestAnomalyDataClass:
    """Test suite for Anomaly dataclass"""
    
    def test_anomaly_creation(self):
        """Test creating an anomaly instance"""
        from datetime import datetime
        
        anomaly = Anomaly(
            anomaly_id="TEST_001",
            type="battery",
            severity="high",
            description="Test anomaly",
            affected_count=5,
            start_time=datetime.now(),
            zscore=2.5,
            confidence=0.85,
            recommended_action="Test action",
            historical_trend=[1.0, 2.0, 3.0]
        )
        
        assert anomaly.anomaly_id == "TEST_001"
        assert anomaly.type == "battery"
        assert anomaly.severity == "high"
        assert anomaly.confidence == 0.85


class TestAnomalyServiceEdgeCases:
    """Test suite for edge cases"""
    
    def test_empty_fleet_data(self):
        """Test with empty fleet data"""
        service = AnomalyDetectionService()
        
        result = service.detect_anomalies({}, {})
        
        assert isinstance(result, list)
    
    def test_empty_vehicles_list(self):
        """Test with empty vehicles list"""
        service = AnomalyDetectionService()
        
        fleet_data = {"vehicles": []}
        supply_chain_data = {"overall_risk_score": 0.5, "suppliers": []}
        
        result = service.detect_anomalies(fleet_data, supply_chain_data)
        
        assert isinstance(result, list)
    
    def test_missing_battery_data(self):
        """Test with missing battery data"""
        service = AnomalyDetectionService()
        
        fleet_data = {
            "vehicles": [
                {"id": "V001"}  # No battery data
            ]
        }
        supply_chain_data = {"overall_risk_score": 0.5, "suppliers": []}
        
        result = service.detect_anomalies(fleet_data, supply_chain_data)
        
        assert isinstance(result, list)
