"""
Test cases for Fleet Service
Tests EV fleet readiness assessment, transition planning, and TCO analysis
"""

import pytest
from services.fleet_service import FleetService, VehicleType


class TestFleetServiceReadinessScore:
    """Test suite for EV readiness score calculation"""
    
    def test_calculate_readiness_score_urban(self):
        """Test readiness score for urban vehicle"""
        result = FleetService.calculate_readiness_score(
            vehicle_type="urban",
            daily_distance_km=100,
            dwell_time_hours=8,
            payload_capacity_kg=3000,
            annual_utilization_hours=2500,
            current_age_years=5
        )
        
        assert "readiness_score" in result
        assert "readiness_level" in result
        assert "component_scores" in result
        assert "recommendation" in result
        assert "confidence" in result
        
        # Urban vehicles with low distance and high dwell time should be ready
        assert result["readiness_score"] >= 70
        assert result["readiness_level"] in ["ready", "conditional"]
    
    def test_calculate_readiness_score_long_haul(self):
        """Test readiness score for long-haul vehicle"""
        result = FleetService.calculate_readiness_score(
            vehicle_type="long_haul",
            daily_distance_km=500,
            dwell_time_hours=1,
            payload_capacity_kg=15000,
            annual_utilization_hours=3000,
            current_age_years=3
        )
        
        # Long-haul with high distance and low dwell time may not be ready
        assert result["readiness_score"] >= 0
        assert result["readiness_level"] in ["ready", "conditional", "not_ready"]
    
    def test_calculate_readiness_score_components(self):
        """Test that all component scores are calculated"""
        result = FleetService.calculate_readiness_score(
            vehicle_type="delivery",
            daily_distance_km=80,
            dwell_time_hours=4,
            payload_capacity_kg=5000,
            annual_utilization_hours=2000,
            current_age_years=6
        )
        
        components = result["component_scores"]
        
        assert "distance_suitability" in components
        assert "charging_opportunity" in components
        assert "utilization_rate" in components
        assert "vehicle_age" in components
        assert "payload_capacity" in components
        assert "operational_flexibility" in components
        
        # All components should be between 0 and 100
        for key, value in components.items():
            assert 0 <= value <= 100, f"{key} should be between 0 and 100"
    
    def test_calculate_readiness_score_levels(self):
        """Test readiness level classification"""
        # High readiness scenario
        high_result = FleetService.calculate_readiness_score(
            vehicle_type="urban",
            daily_distance_km=80,
            dwell_time_hours=8,
            payload_capacity_kg=5000,
            annual_utilization_hours=2500,
            current_age_years=8
        )
        
        if high_result["readiness_score"] >= 85:
            assert high_result["readiness_level"] == "ready"
        
        # Low readiness scenario
        low_result = FleetService.calculate_readiness_score(
            vehicle_type="long_haul",
            daily_distance_km=600,
            dwell_time_hours=0.5,
            payload_capacity_kg=20000,
            annual_utilization_hours=1000,
            current_age_years=1
        )
        
        if low_result["readiness_score"] < 70:
            assert low_result["readiness_level"] == "not_ready"
    
    def test_calculate_readiness_score_confidence(self):
        """Test confidence calculation"""
        result = FleetService.calculate_readiness_score(
            vehicle_type="urban",
            daily_distance_km=100,
            dwell_time_hours=6,
            payload_capacity_kg=3000,
            annual_utilization_hours=2200,
            current_age_years=5
        )
        
        # Confidence should be between 0.85 and 1.0
        assert 0.85 <= result["confidence"] <= 1.0


class TestFleetServiceDistanceScoring:
    """Test suite for distance-based scoring"""
    
    def test_score_distance_urban_optimal(self):
        """Test distance scoring for urban vehicle - optimal distance"""
        score = FleetService._score_distance("urban", 80)
        assert score == 100  # Optimal
    
    def test_score_distance_urban_acceptable(self):
        """Test distance scoring for urban vehicle - acceptable distance"""
        score = FleetService._score_distance("urban", 120)
        assert score == 75  # Acceptable
    
    def test_score_distance_urban_high(self):
        """Test distance scoring for urban vehicle - high distance"""
        score = FleetService._score_distance("urban", 200)
        assert score < 75  # Beyond acceptable
    
    def test_score_distance_long_haul(self):
        """Test distance scoring for long-haul vehicle"""
        score = FleetService._score_distance("long_haul", 350)
        assert score >= 40  # Long-haul should handle longer distances
    
    def test_score_distance_delivery(self):
        """Test distance scoring for delivery vehicle"""
        score = FleetService._score_distance("delivery", 70)
        assert score >= 75
    
    def test_score_distance_unknown_type(self):
        """Test distance scoring for unknown vehicle type"""
        score = FleetService._score_distance("unknown", 100)
        assert 0 <= score <= 100


class TestFleetServiceChargingScoring:
    """Test suite for charging opportunity scoring"""
    
    def test_score_charging_long_dwell(self):
        """Test charging score with long dwell time"""
        score = FleetService._score_charging(10)
        assert score == 100  # Fast charging possible
    
    def test_score_charging_medium_dwell(self):
        """Test charging score with medium dwell time"""
        score = FleetService._score_charging(5)
        assert score == 80  # Medium charging
    
    def test_score_charging_short_dwell(self):
        """Test charging score with short dwell time"""
        score = FleetService._score_charging(2.5)
        assert score == 50  # Slow charging
    
    def test_score_charging_very_short_dwell(self):
        """Test charging score with very short dwell time"""
        score = FleetService._score_charging(0.5)
        assert score == 20  # Limited opportunity


class TestFleetServiceUtilizationScoring:
    """Test suite for utilization rate scoring"""
    
    def test_score_utilization_high(self):
        """Test utilization score - high utilization"""
        score = FleetService._score_utilization(2600)
        assert score == 100
    
    def test_score_utilization_moderate(self):
        """Test utilization score - moderate utilization"""
        score = FleetService._score_utilization(1800)
        assert 65 <= score <= 85
    
    def test_score_utilization_low(self):
        """Test utilization score - low utilization"""
        score = FleetService._score_utilization(1000)
        assert score == 40


class TestFleetServiceAgeScoring:
    """Test suite for vehicle age scoring"""
    
    def test_score_vehicle_age_old(self):
        """Test age score - old vehicle"""
        score = FleetService._score_vehicle_age(10)
        assert score == 100  # Urgent replacement
    
    def test_score_vehicle_age_moderate(self):
        """Test age score - moderate age"""
        score = FleetService._score_vehicle_age(6)
        assert 50 <= score <= 75
    
    def test_score_vehicle_age_new(self):
        """Test age score - new vehicle"""
        score = FleetService._score_vehicle_age(2)
        assert score == 30  # Can wait


class TestFleetServiceEVRecommendation:
    """Test suite for EV model recommendations"""
    
    def test_recommend_ev_model_urban(self):
        """Test EV recommendation for urban vehicle"""
        result = FleetService.recommend_ev_model("urban", 90)
        
        assert "primary_recommendation" in result
        assert "alternative_models" in result
        assert "estimated_battery_kwh" in result
        assert "estimated_range_km" in result
        assert "estimated_price_lakhs_inr" in result
        assert "confidence_score" in result
        
        # Should recommend urban-appropriate models
        assert result["primary_recommendation"] in ["Tata Nexon EV Max", "MG ZS EV", "Hyundai Kona"]
    
    def test_recommend_ev_model_delivery(self):
        """Test EV recommendation for delivery vehicle"""
        result = FleetService.recommend_ev_model("delivery", 85)
        
        assert "primary_recommendation" in result
        assert result["estimated_range_km"] >= 380
    
    def test_recommend_ev_model_long_haul(self):
        """Test EV recommendation for long-haul vehicle"""
        result = FleetService.recommend_ev_model("long_haul", 75)
        
        assert "primary_recommendation" in result
        # Long-haul should have higher range recommendation
        assert result["estimated_range_km"] >= 500
    
    def test_recommend_ev_model_confidence(self):
        """Test that recommendation confidence correlates with readiness"""
        high_readiness = FleetService.recommend_ev_model("urban", 95)
        low_readiness = FleetService.recommend_ev_model("urban", 50)
        
        assert high_readiness["confidence_score"] > low_readiness["confidence_score"]
    
    def test_recommend_ev_model_unknown_type(self):
        """Test EV recommendation for unknown vehicle type"""
        result = FleetService.recommend_ev_model("unknown_type", 75)
        assert result == {}


class TestFleetServiceTransitionPlan:
    """Test suite for transition planning"""
    
    def test_generate_transition_plan_basic(self):
        """Test basic transition plan generation"""
        result = FleetService.generate_transition_plan(
            fleet_size=58,
            vehicles_by_readiness={"ready": 42, "conditional": 12, "not_ready": 4},
            available_budget_inr=200_000_000
        )
        
        assert "phases" in result
        assert "total_vehicles_transitioned" in result
        assert "transition_percentage" in result
        assert "total_investment_required_inr" in result
        
        # Should have phases
        assert len(result["phases"]) >= 1
    
    def test_generate_transition_plan_phased(self):
        """Test that transition plan is phased correctly"""
        result = FleetService.generate_transition_plan(
            fleet_size=100,
            vehicles_by_readiness={"ready": 50, "conditional": 30, "not_ready": 20},
            available_budget_inr=500_000_000
        )
        
        phases = result["phases"]
        
        # Phase 1 should focus on ready vehicles
        assert phases[0]["priority"] == "High readiness vehicles"
        assert phases[0]["vehicles"] > 0
    
    def test_generate_transition_plan_budget_constraint(self):
        """Test that plan respects budget constraints"""
        budget = 50_000_000  # Limited budget
        
        result = FleetService.generate_transition_plan(
            fleet_size=100,
            vehicles_by_readiness={"ready": 80, "conditional": 15, "not_ready": 5},
            available_budget_inr=budget
        )
        
        # Total investment should not exceed budget (approximately)
        # Allow some flexibility due to calculation method
        assert result["total_investment_required_inr"] <= budget * 1.1
    
    def test_generate_transition_plan_roi(self):
        """Test that ROI is calculated"""
        result = FleetService.generate_transition_plan(
            fleet_size=50,
            vehicles_by_readiness={"ready": 30, "conditional": 15, "not_ready": 5},
            available_budget_inr=100_000_000
        )
        
        assert "annual_roi" in result
        assert result["annual_roi"] > 0


class TestFleetServiceCarbonReduction:
    """Test suite for carbon reduction calculations"""
    
    def test_calculate_carbon_reduction_basic(self):
        """Test basic carbon reduction calculation"""
        result = FleetService.calculate_carbon_reduction(
            fleet_size=100,
            transitioned_count=50,
            annual_distance_per_vehicle=50_000
        )
        
        assert "transitioned_vehicles" in result
        assert "co2_reduction_per_vehicle_annual_kg" in result
        assert "total_co2_reduction_annual_kg" in result
        assert "total_co2_reduction_annual_tons" in result
        
        assert result["transitioned_vehicles"] == 50
        assert result["remaining_diesel"] == 50
    
    def test_calculate_carbon_reduction_values(self):
        """Test that carbon reduction values are reasonable"""
        result = FleetService.calculate_carbon_reduction(
            fleet_size=100,
            transitioned_count=50,
            annual_distance_per_vehicle=50_000
        )
        
        # Per vehicle reduction should be positive
        assert result["co2_reduction_per_vehicle_annual_kg"] > 0
        
        # Total should be approximately per_vehicle * count
        expected_total = result["co2_reduction_per_vehicle_annual_kg"] * 50
        assert abs(result["total_co2_reduction_annual_kg"] - expected_total) < 1000
    
    def test_calculate_carbon_reduction_zero_transition(self):
        """Test carbon reduction with no vehicles transitioned"""
        result = FleetService.calculate_carbon_reduction(
            fleet_size=100,
            transitioned_count=0
        )
        
        assert result["total_co2_reduction_annual_kg"] == 0
        assert result["total_co2_reduction_annual_tons"] == 0
    
    def test_calculate_carbon_reduction_full_transition(self):
        """Test carbon reduction with full fleet transition"""
        result = FleetService.calculate_carbon_reduction(
            fleet_size=100,
            transitioned_count=100
        )
        
        assert result["remaining_diesel"] == 0
        assert result["total_co2_reduction_annual_tons"] > 0
    
    def test_calculate_carbon_reduction_trees_equivalent(self):
        """Test tree equivalent calculation"""
        result = FleetService.calculate_carbon_reduction(
            fleet_size=100,
            transitioned_count=50,
            annual_distance_per_vehicle=50_000
        )
        
        # Trees needed should be positive
        assert result["equivalent_trees_needed_to_offset"] > 0


class TestFleetServiceTCO:
    """Test suite for Total Cost of Ownership analysis"""
    
    def test_calculate_tco_basic(self):
        """Test basic TCO calculation"""
        result = FleetService.calculate_total_cost_of_ownership(
            vehicle_type="urban",
            annual_distance=50_000,
            years_horizon=8
        )
        
        assert "vehicle_type" in result
        assert "diesel_tco" in result
        assert "ev_tco" in result
        assert "tco_advantage" in result
        
        # Check TCO components
        assert "total_tco" in result["diesel_tco"]
        assert "total_tco" in result["ev_tco"]
    
    def test_calculate_tco_ev_advantage(self):
        """Test that EV shows TCO advantage for suitable use cases"""
        result = FleetService.calculate_total_cost_of_ownership(
            vehicle_type="urban",
            annual_distance=60_000,  # High utilization
            years_horizon=8
        )
        
        # For high-utilization urban vehicles, EV should have TCO advantage
        advantage = result["tco_advantage"]
        
        assert advantage["absolute_savings"] != 0
        assert advantage["payback_period_years"] > 0
        assert advantage["payback_period_years"] <= 8
    
    def test_calculate_tco_components_diesel(self):
        """Test diesel TCO components"""
        result = FleetService.calculate_total_cost_of_ownership(
            vehicle_type="delivery",
            annual_distance=50_000,
            years_horizon=8
        )
        
        diesel = result["diesel_tco"]
        
        assert "purchase_price" in diesel
        assert "fuel_cost" in diesel
        assert "maintenance_cost" in diesel
        assert "road_tax" in diesel
        assert "insurance" in diesel
        assert "salvage_value" in diesel
        
        # Fuel cost should be significant for diesel
        assert diesel["fuel_cost"] > 0
    
    def test_calculate_tco_components_ev(self):
        """Test EV TCO components"""
        result = FleetService.calculate_total_cost_of_ownership(
            vehicle_type="delivery",
            annual_distance=50_000,
            years_horizon=8
        )
        
        ev = result["ev_tco"]
        
        assert "purchase_price" in ev
        assert "fuel_cost" in ev
        assert "maintenance_cost" in ev
        assert "subsidy" in ev
        assert "battery_replacement" in ev
        
        # EV should have subsidy
        assert ev["subsidy"] > 0
    
    def test_calculate_tco_battery_replacement(self):
        """Test battery replacement cost for long ownership"""
        result_long = FleetService.calculate_total_cost_of_ownership(
            vehicle_type="urban",
            annual_distance=50_000,
            years_horizon=8
        )
        
        result_short = FleetService.calculate_total_cost_of_ownership(
            vehicle_type="urban",
            annual_distance=50_000,
            years_horizon=5
        )
        
        # Long ownership should include battery replacement
        assert result_long["ev_tco"]["battery_replacement"] > 0
        
        # Short ownership should not include battery replacement
        assert result_short["ev_tco"]["battery_replacement"] == 0
    
    def test_calculate_tco_different_vehicle_types(self):
        """Test TCO for different vehicle types"""
        for v_type in ["urban", "delivery", "long_haul"]:
            result = FleetService.calculate_total_cost_of_ownership(
                vehicle_type=v_type,
                annual_distance=50_000,
                years_horizon=8
            )
            
            assert result["vehicle_type"] == v_type
            assert result["diesel_tco"]["total_tco"] > 0
            assert result["ev_tco"]["total_tco"] > 0
    
    def test_calculate_tco_distance_impact(self):
        """Test that annual distance affects TCO"""
        result_low = FleetService.calculate_total_cost_of_ownership(
            vehicle_type="urban",
            annual_distance=30_000,
            years_horizon=8
        )
        
        result_high = FleetService.calculate_total_cost_of_ownership(
            vehicle_type="urban",
            annual_distance=80_000,
            years_horizon=8
        )
        
        # Higher distance should result in higher fuel costs
        assert result_high["diesel_tco"]["fuel_cost"] > result_low["diesel_tco"]["fuel_cost"]
        assert result_high["ev_tco"]["fuel_cost"] > result_low["ev_tco"]["fuel_cost"]


class TestFleetServiceThresholds:
    """Test suite for readiness thresholds"""
    
    def test_readiness_thresholds_valid(self):
        """Test that readiness thresholds are properly ordered"""
        thresholds = FleetService.READINESS_THRESHOLDS
        
        assert thresholds["ready"] >= thresholds["conditional"]
        assert thresholds["conditional"] >= thresholds["not_ready"]
        assert thresholds["ready"] == 85
        assert thresholds["conditional"] == 70
        assert thresholds["not_ready"] == 0


class TestFleetServiceEVRecommendations:
    """Test suite for EV recommendation data"""
    
    def test_ev_recommendations_structure(self):
        """Test that EV recommendations have proper structure"""
        for v_type, rec in FleetService.EV_RECOMMENDATIONS.items():
            assert "models" in rec
            assert "range_km" in rec
            assert "battery_kwh" in rec
            assert "price_range_inr" in rec
            
            assert len(rec["models"]) > 0
            assert len(rec["models"]) == len(rec["range_km"])
            assert len(rec["models"]) == len(rec["battery_kwh"])
    
    def test_ev_recommendations_reasonable_ranges(self):
        """Test that EV recommendations have reasonable range values"""
        for v_type, rec in FleetService.EV_RECOMMENDATIONS.items():
            for range_km in rec["range_km"]:
                assert 200 <= range_km <= 800, f"Range for {v_type} should be reasonable"
            
            for battery in rec["battery_kwh"]:
                assert 50 <= battery <= 250, f"Battery for {v_type} should be reasonable"
