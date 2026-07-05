"""
Test cases for Battery Service
Tests battery health prediction, degradation modeling, and maintenance recommendations
"""

import pytest
import math
from services.battery_service import BatteryService


class TestBatteryServiceSOHPrediction:
    """Test suite for State of Health (SOH) prediction"""
    
    def test_predict_soh_basic(self, sample_charge_history):
        """Test basic SOH prediction returns valid results"""
        result = BatteryService.predict_soh(
            current_cycles=1200,
            charge_history=sample_charge_history,
            ambient_temp_c=30
        )
        
        assert "soh" in result
        assert "rul_days" in result
        assert "confidence" in result
        assert "risk_level" in result
        assert "degradation_breakdown" in result
        
        # SOH should be within valid range
        assert BatteryService.SOH_MIN <= result["soh"] <= BatteryService.SOH_MAX
        
        # RUL should be positive
        assert result["rul_days"] >= 7
        
        # Confidence should be between 0 and 1
        assert 0 <= result["confidence"] <= 1
    
    def test_predict_soh_low_cycles(self, sample_charge_history):
        """Test SOH prediction for low cycle count (new battery)"""
        result = BatteryService.predict_soh(
            current_cycles=100,
            charge_history=sample_charge_history[:1],  # Minimal history
            ambient_temp_c=25
        )
        
        # New battery should have high SOH
        assert result["soh"] >= 90
        assert result["risk_level"] == "low"
    
    def test_predict_soh_high_cycles(self, sample_charge_history):
        """Test SOH prediction for high cycle count (degraded battery)"""
        result = BatteryService.predict_soh(
            current_cycles=2000,
            charge_history=sample_charge_history,
            ambient_temp_c=30
        )
        
        # Heavily used battery should have lower SOH
        assert result["soh"] < 95
        assert result["risk_level"] in ["medium", "high", "critical"]
    
    def test_predict_soh_high_temperature(self, sample_charge_history):
        """Test SOH prediction with high ambient temperature"""
        result_hot = BatteryService.predict_soh(
            current_cycles=1200,
            charge_history=sample_charge_history,
            ambient_temp_c=45  # Hot environment
        )
        
        result_normal = BatteryService.predict_soh(
            current_cycles=1200,
            charge_history=sample_charge_history,
            ambient_temp_c=25  # Normal environment
        )
        
        # High temperature should accelerate degradation
        assert result_hot["soh"] <= result_normal["soh"]
        assert result_hot["temperature_factor"] > result_normal["temperature_factor"]
    
    def test_predict_soh_empty_charge_history(self):
        """Test SOH prediction with empty charge history"""
        result = BatteryService.predict_soh(
            current_cycles=500,
            charge_history=[],
            ambient_temp_c=25
        )
        
        # Should still return valid results
        assert result["soh"] >= BatteryService.SOH_MIN
        assert result["thermal_stress_factor"] == 0
        assert result["fast_charge_events"] == 0
    
    def test_predict_soh_fast_charge_detection(self, sample_charge_history):
        """Test detection of fast charge events"""
        result = BatteryService.predict_soh(
            current_cycles=800,
            charge_history=sample_charge_history,
            ambient_temp_c=30
        )
        
        # Should detect fast charge events (current > 150A)
        assert result["fast_charge_events"] == 2  # Two events in sample data
    
    def test_predict_soh_degradation_breakdown(self, sample_charge_history):
        """Test degradation breakdown components"""
        result = BatteryService.predict_soh(
            current_cycles=1000,
            charge_history=sample_charge_history,
            ambient_temp_c=35
        )
        
        breakdown = result["degradation_breakdown"]
        
        assert "cycle_based" in breakdown
        assert "thermal_cycling" in breakdown
        assert "fast_charging" in breakdown
        assert "ambient_temperature" in breakdown
        
        # All breakdown values should be non-negative
        for key, value in breakdown.items():
            assert value >= 0, f"{key} should be non-negative"
    
    def test_predict_soh_risk_levels(self):
        """Test risk level classification"""
        test_cases = [
            (85, "low"),
            (75, "medium"),
            (65, "high"),
            (55, "critical")
        ]
        
        for soh_threshold, expected_risk in test_cases:
            # Create conditions to produce specific SOH
            cycles = int((100 - soh_threshold) / BatteryService.DEGRADATION_RATE)
            result = BatteryService.predict_soh(
                current_cycles=cycles,
                charge_history=[{"current_a": 100, "temperature_c": 25}],
                ambient_temp_c=25
            )
            
            # Risk level should match expected category (approximately)
            if result["soh"] >= 85:
                assert result["risk_level"] == "low"
            elif result["soh"] >= 70:
                assert result["risk_level"] == "medium"
            elif result["soh"] >= 60:
                assert result["risk_level"] == "high"
            else:
                assert result["risk_level"] == "critical"


class TestBatteryServiceThermalStress:
    """Test suite for thermal stress calculations"""
    
    def test_calculate_thermal_stress_normal_temps(self):
        """Test thermal stress with normal operating temperatures"""
        charge_history = [
            {"current_a": 100, "temperature_c": 25},
            {"current_a": 100, "temperature_c": 28},
            {"current_a": 100, "temperature_c": 30},
        ]
        
        stress = BatteryService._calculate_thermal_stress(charge_history)
        
        # Normal temps should produce low stress
        assert stress >= 0
        assert stress < 5  # Low stress threshold
    
    def test_calculate_thermal_stress_high_temps(self):
        """Test thermal stress with high operating temperatures"""
        charge_history = [
            {"current_a": 150, "temperature_c": 45},
            {"current_a": 180, "temperature_c": 48},
            {"current_a": 160, "temperature_c": 50},
        ]
        
        stress = BatteryService._calculate_thermal_stress(charge_history)
        
        # High temps should produce significant stress
        assert stress > 0
    
    def test_calculate_thermal_stress_advanced(self):
        """Test advanced thermal stress calculation"""
        charge_history = [
            {"current_a": 100, "temperature_c": 45, "timestamp": "2024-12-01"},
            {"current_a": 200, "temperature_c": 50, "timestamp": "2024-12-02"},  # Hot + high current
            {"current_a": 50, "temperature_c": 20, "timestamp": "2024-12-03"},
        ]
        
        stress = BatteryService._calculate_thermal_stress_advanced(charge_history)
        
        assert stress >= 0
        assert isinstance(stress, float)
    
    def test_calculate_fast_charge_stress(self):
        """Test fast charge stress calculation"""
        # Normal charging
        normal_charges = [
            {"current_a": 80, "temperature_c": 30},
            {"current_a": 100, "temperature_c": 32},
        ]
        normal_stress = BatteryService._calculate_fast_charge_stress(normal_charges)
        
        # Fast charging
        fast_charges = [
            {"current_a": 180, "temperature_c": 35},
            {"current_a": 200, "temperature_c": 40},
        ]
        fast_stress = BatteryService._calculate_fast_charge_stress(fast_charges)
        
        # Fast charging should produce higher stress
        assert fast_stress > normal_stress
    
    def test_calculate_fast_charge_stress_empty(self):
        """Test fast charge stress with no fast charge events"""
        charge_history = [
            {"current_a": 80, "temperature_c": 30},
            {"current_a": 100, "temperature_c": 32},
        ]
        
        stress = BatteryService._calculate_fast_charge_stress(charge_history)
        assert stress == 0


class TestBatteryServiceMaintenance:
    """Test suite for maintenance recommendations"""
    
    def test_maintenance_recommendation_healthy(self):
        """Test maintenance recommendation for healthy battery"""
        recommendation, days, urgency = BatteryService.get_maintenance_recommendation(
            soh=92,
            rul_days=2000
        )
        
        assert urgency == "routine"
        assert days == 180
        assert "normal operations" in recommendation.lower()
    
    def test_maintenance_recommendation_moderate(self):
        """Test maintenance recommendation for moderate battery health"""
        recommendation, days, urgency = BatteryService.get_maintenance_recommendation(
            soh=75,
            rul_days=500
        )
        
        assert urgency == "scheduled"
        assert days == 90
        assert "monitor" in recommendation.lower()
    
    def test_maintenance_recommendation_degraded(self):
        """Test maintenance recommendation for degraded battery"""
        recommendation, days, urgency = BatteryService.get_maintenance_recommendation(
            soh=62,
            rul_days=100
        )
        
        assert urgency == "urgent"
        assert days == 30
        assert "replacement" in recommendation.lower()
    
    def test_maintenance_recommendation_critical(self):
        """Test maintenance recommendation for critical battery"""
        recommendation, days, urgency = BatteryService.get_maintenance_recommendation(
            soh=55,
            rul_days=30
        )
        
        assert urgency == "critical"
        assert days == 7
        assert "critical" in recommendation.lower() or "immediately" in recommendation.lower()


class TestBatteryServiceForecast:
    """Test suite for degradation forecasting"""
    
    def test_forecast_degradation_basic(self):
        """Test basic degradation forecast"""
        forecast = BatteryService.forecast_degradation(soh=92, months=6)
        
        assert len(forecast) == 6
        
        for i, entry in enumerate(forecast):
            assert entry["month"] == i + 1
            assert "soh_percent" in entry
            assert "forecast_date" in entry
            assert entry["soh_percent"] <= 92  # Should degrade over time
    
    def test_forecast_degradation_progressive(self):
        """Test that forecast shows progressive degradation"""
        forecast = BatteryService.forecast_degradation(soh=90, months=12)
        
        soh_values = [entry["soh_percent"] for entry in forecast]
        
        # SOH should generally decrease over time
        for i in range(len(soh_values) - 1):
            assert soh_values[i] >= soh_values[i + 1] - 0.5  # Allow small variance
    
    def test_forecast_degradation_minimum_soh(self):
        """Test that forecast respects minimum SOH"""
        forecast = BatteryService.forecast_degradation(soh=55, months=12)
        
        for entry in forecast:
            assert entry["soh_percent"] >= BatteryService.SOH_MIN


class TestBatteryServiceFleetStats:
    """Test suite for fleet statistics calculations"""
    
    def test_calculate_fleet_statistics_basic(self):
        """Test basic fleet statistics calculation"""
        vehicles = [
            {"vehicle_id": "V001", "soh": 95},
            {"vehicle_id": "V002", "soh": 88},
            {"vehicle_id": "V003", "soh": 75},
            {"vehicle_id": "V004", "soh": 62},
        ]
        
        stats = BatteryService.calculate_fleet_statistics(vehicles)
        
        assert stats["total_vehicles"] == 4
        assert stats["average_soh"] == 80.0
        assert stats["min_soh"] == 62
        assert stats["max_soh"] == 95
        assert stats["vehicles_healthy"] == 2
        assert stats["vehicles_medium_risk"] == 1
        assert stats["vehicles_high_risk"] == 1
    
    def test_calculate_fleet_statistics_empty(self):
        """Test fleet statistics with empty fleet"""
        stats = BatteryService.calculate_fleet_statistics([])
        assert stats == {}
    
    def test_calculate_fleet_statistics_default_soh(self):
        """Test fleet statistics with missing SOH values"""
        vehicles = [
            {"vehicle_id": "V001"},  # No SOH
            {"vehicle_id": "V002", "soh": 90},
        ]
        
        stats = BatteryService.calculate_fleet_statistics(vehicles)
        
        # Should use default SOH of 85
        assert stats["total_vehicles"] == 2
        assert 85 <= stats["average_soh"] <= 90


class TestBatteryServiceArrhenius:
    """Test suite for Arrhenius equation implementation"""
    
    def test_temperature_acceleration_factor(self):
        """Test temperature acceleration factor calculation"""
        # Reference temperature should give factor close to 1
        result_ref = BatteryService.predict_soh(
            current_cycles=500,
            charge_history=[{"current_a": 100, "temperature_c": 25}],
            ambient_temp_c=25
        )
        
        # High temperature should give higher acceleration factor
        result_hot = BatteryService.predict_soh(
            current_cycles=500,
            charge_history=[{"current_a": 100, "temperature_c": 45}],
            ambient_temp_c=45
        )
        
        assert result_hot["temperature_factor"] > result_ref["temperature_factor"]
    
    def test_degradation_rate_temperature_dependence(self):
        """Test that degradation rate increases with temperature"""
        result_cold = BatteryService.predict_soh(
            current_cycles=500,
            charge_history=[],
            ambient_temp_c=15
        )
        
        result_hot = BatteryService.predict_soh(
            current_cycles=500,
            charge_history=[],
            ambient_temp_c=40
        )
        
        # Hot conditions should have higher degradation rate
        assert result_hot["degradation_rate"] > result_cold["degradation_rate"]
