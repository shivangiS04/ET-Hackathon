"""
Unit tests for Manufacturing Quality Intelligence Service
Tests quality drift detection, anomaly correlation, and recommendations
"""
import pytest


class TestQualityDriftDetection:
    """Test quality drift detection in manufacturing"""

    def test_detect_drift_within_tolerance(self, quality_service, sample_process_params,
                                           sample_material_quality, sample_inspection_results):
        """Test detection when all parameters are within tolerance"""
        result = quality_service.correlate_quality_parameters(
            process_params=sample_process_params,
            material_quality=sample_material_quality,
            inspection_results=sample_inspection_results
        )
        
        assert result["quality_drift_score"] < 0.3
        assert result["anomalies_detected"] == 0
        assert "CONTINUE" in result["recommendation"].upper()

    def test_detect_drift_process_parameter_violation(self, quality_service,
                                                      sample_material_quality,
                                                      sample_inspection_results):
        """Test detection of process parameter drift"""
        bad_params = {
            "cell_voltage": 2.5,  # Below expected range
            "resistance": 0.08,   # Above threshold
            "temperature_during_charge": 52,  # Too high
            "cycle_efficiency": 97.0
        }
        
        result = quality_service.correlate_quality_parameters(
            process_params=bad_params,
            material_quality=sample_material_quality,
            inspection_results=sample_inspection_results
        )
        
        assert result["quality_drift_score"] > 0.3
        assert result["anomalies_detected"] > 0
        assert len(result["anomalies"]) > 0

    def test_detect_material_quality_issue(self, quality_service, sample_process_params,
                                           sample_inspection_results):
        """Test detection of material quality issues"""
        poor_material = {
            "lithium": {"purity": 98.0, "impurity_ppm": 200},  # Below threshold
            "cobalt": {"purity": 99.5, "impurity_ppm": 50},
            "nickel": {"purity": 99.2, "impurity_ppm": 80}
        }
        
        result = quality_service.correlate_quality_parameters(
            process_params=sample_process_params,
            material_quality=poor_material,
            inspection_results=sample_inspection_results
        )
        
        assert result["quality_drift_score"] > 0.4
        anomaly_types = [a["type"] for a in result["anomalies"]]
        assert "material_quality" in anomaly_types

    def test_detect_inspection_failure(self, quality_service, sample_process_params,
                                       sample_material_quality):
        """Test detection of inspection failures"""
        failed_inspection = {
            "visual_inspection": {"passed": False, "defects": 5},
            "voltage_test": {"passed": False, "min_voltage": 2.8},
            "resistance_test": {"passed": True, "max_resistance": 0.05},
            "thermal_test": {"passed": True, "temp_range": (15, 45)}
        }
        
        result = quality_service.correlate_quality_parameters(
            process_params=sample_process_params,
            material_quality=sample_material_quality,
            inspection_results=failed_inspection
        )
        
        assert result["quality_drift_score"] > 0.2
        anomaly_types = [a["type"] for a in result["anomalies"]]
        assert "inspection_failure" in anomaly_types


class TestQualityRecommendations:
    """Test quality control recommendations"""

    def test_recommendation_continue_operations(self, quality_service):
        """Test recommendation to continue operations"""
        recommendation = quality_service._generate_recommendation(
            drift_score=0.2,
            anomalies=[]
        )
        assert "CONTINUE" in recommendation.upper()

    def test_recommendation_monitor_closely(self, quality_service):
        """Test recommendation to monitor closely"""
        recommendation = quality_service._generate_recommendation(
            drift_score=0.4,
            anomalies=[{"severity": "MEDIUM"}]
        )
        assert "MONITOR" in recommendation.upper()

    def test_recommendation_reduce_throughput(self, quality_service):
        """Test recommendation to reduce throughput"""
        recommendation = quality_service._generate_recommendation(
            drift_score=0.6,
            anomalies=[{"severity": "HIGH"}, {"severity": "HIGH"}]
        )
        assert "REDUCE" in recommendation.upper()

    def test_recommendation_stop_production(self, quality_service):
        """Test recommendation to stop production"""
        recommendation = quality_service._generate_recommendation(
            drift_score=0.8,
            anomalies=[
                {"severity": "CRITICAL"},
                {"severity": "CRITICAL"},
                {"severity": "HIGH"}
            ]
        )
        assert "STOP" in recommendation.upper()


class TestSystematicIssueDetection:
    """Test detection of systematic manufacturing issues"""

    def test_detect_high_failure_rate(self, quality_service):
        """Test detection of high failure rate"""
        historical_data = [
            {"passed": False, "component_type": "cell_housing"},
            {"passed": True, "component_type": "terminal"},
            {"passed": False, "component_type": "cell_housing"},
            {"passed": False, "component_type": "cell_housing"},
            {"passed": False, "component_type": "cell_housing"},
            {"passed": True, "component_type": "terminal"},
            {"passed": False, "component_type": "cell_housing"},
            {"passed": False, "component_type": "cell_housing"},
            {"passed": False, "component_type": "seal"},
            {"passed": False, "component_type": "seal"},
        ]
        
        result = quality_service.detect_systematic_issues(historical_data)
        
        assert "systematic_issues" in result
        assert len(result["systematic_issues"]) > 0
        assert result["total_failure_rate"] > 0.05

    def test_detect_component_specific_failures(self, quality_service):
        """Test detection of component-specific failure patterns"""
        historical_data = [
            {"passed": i % 7 != 0, "component_type": "cell_housing"}
            for i in range(20)
        ]
        
        result = quality_service.detect_systematic_issues(historical_data)
        assert len(result["systematic_issues"]) > 0


class TestQualityDashboard:
    """Test quality dashboard generation"""

    def test_dashboard_generation(self, quality_service):
        """Test quality dashboard generation"""
        dashboard = quality_service.generate_quality_dashboard(timeframe_days=7)
        
        assert "period_days" in dashboard
        assert dashboard["period_days"] == 7
        assert "metrics" in dashboard
        assert "top_issues" in dashboard
        assert "recommendations" in dashboard
        assert len(dashboard["recommendations"]) > 0
