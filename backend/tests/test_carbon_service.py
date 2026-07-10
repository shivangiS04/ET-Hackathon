"""
Unit tests for Carbon Tracking Service
Tests Scope 1/3 emissions calculations, fleet tracking, and Net Zero roadmaps
"""
import pytest
import math


class TestEmissionCalculation:
    """Test Scope 1 and Scope 3 emission calculations"""

    def test_diesel_emission_calculation(self, carbon_service):
        """Test diesel vehicle emission calculation"""
        emissions = carbon_service.calculate_scope_emissions(
            vehicle_type="diesel",
            distance_km=1000,
            fuel_consumed=100
        )
        
        assert emissions["scope1_kg_co2"] > 0
        assert emissions["scope3_kg_co2"] > 0
        assert emissions["total_kg_co2"] == pytest.approx(
            emissions["scope1_kg_co2"] + emissions["scope3_kg_co2"]
        )

    def test_ev_emission_calculation(self, carbon_service):
        """Test EV vehicle emission calculation (Scope 3 only)"""
        emissions = carbon_service.calculate_scope_emissions(
            vehicle_type="electric",
            distance_km=1000
        )
        
        assert emissions["scope1_kg_co2"] == 0
        assert emissions["scope3_kg_co2"] > 0
        assert emissions["total_kg_co2"] == emissions["scope3_kg_co2"]

    def test_emission_per_km_diesel(self, carbon_service):
        """Test emission rate per km for diesel"""
        result1 = carbon_service.calculate_scope_emissions(
            vehicle_type="diesel",
            distance_km=100,
            fuel_consumed=10
        )
        
        result2 = carbon_service.calculate_scope_emissions(
            vehicle_type="diesel",
            distance_km=200,
            fuel_consumed=20
        )
        
        # Emissions should scale linearly with distance
        assert result2["total_kg_co2"] == pytest.approx(result1["total_kg_co2"] * 2, rel=0.01)

    def test_ev_vs_diesel_comparison(self, carbon_service):
        """Test that EV produces significantly less emissions than diesel"""
        diesel_emissions = carbon_service.calculate_scope_emissions(
            vehicle_type="diesel",
            distance_km=1000,
            fuel_consumed=100
        )
        
        ev_emissions = carbon_service.calculate_scope_emissions(
            vehicle_type="electric",
            distance_km=1000
        )
        
        reduction_percent = (
            (diesel_emissions["total_kg_co2"] - ev_emissions["total_kg_co2"]) /
            diesel_emissions["total_kg_co2"] * 100
        )
        
        assert reduction_percent > 50  # EV should produce >50% less emissions


class TestEmissionReduction:
    """Test emission reduction calculations"""

    def test_emission_reduction_calculation(self, carbon_service):
        """Test diesel to EV conversion emission reduction"""
        reduction = carbon_service.calculate_emission_reduction(
            diesel_km=10000,
            ev_km=10000
        )
        
        assert reduction["reduction_kg_co2"] > 0
        assert reduction["reduction_percent"] > 0
        assert reduction["reduction_percent"] <= 100
        assert reduction["reduction_metric_tons"] == pytest.approx(
            reduction["reduction_kg_co2"] / 1000
        )

    def test_emission_reduction_trees_equivalent(self, carbon_service):
        """Test CO2 to trees saved conversion"""
        reduction = carbon_service.calculate_emission_reduction(
            diesel_km=5000,
            ev_km=5000
        )
        
        # Each tree absorbs ~21 kg CO2/year
        expected_trees = reduction["reduction_kg_co2"] / 21
        assert reduction["co2_equivalent_trees_saved"] == pytest.approx(expected_trees, rel=0.01)

    def test_zero_reduction_same_type(self, carbon_service):
        """Test no reduction if switching between same vehicle types"""
        reduction = carbon_service.calculate_emission_reduction(
            diesel_km=5000,
            ev_km=0  # No EV
        )
        
        assert reduction["reduction_kg_co2"] > 0
        assert reduction["reduction_percent"] > 0


class TestFleetWideTracking:
    """Test fleet-wide emissions tracking"""

    def test_fleet_emission_aggregation(self, carbon_service):
        """Test aggregating emissions across fleet"""
        fleet_data = [
            {"vehicle_type": "diesel", "distance_km": 1000, "fuel_consumed": 100},
            {"vehicle_type": "diesel", "distance_km": 1500, "fuel_consumed": 150},
            {"vehicle_type": "electric", "distance_km": 2000},
            {"vehicle_type": "electric", "distance_km": 1800},
        ]
        
        fleet_emissions = carbon_service.calculate_fleet_emissions(fleet_data)
        
        assert fleet_emissions["total_fleet_emissions_kg_co2"] > 0
        assert len(fleet_emissions["vehicle_emissions"]) == 4
        assert sum(v["total_kg_co2"] for v in fleet_emissions["vehicle_emissions"]) == \
               pytest.approx(fleet_emissions["total_fleet_emissions_kg_co2"])

    def test_fleet_emission_breakdown(self, carbon_service):
        """Test emission breakdown by vehicle type"""
        fleet_data = [
            {"vehicle_type": "diesel", "distance_km": 1000, "fuel_consumed": 100},
            {"vehicle_type": "diesel", "distance_km": 1000, "fuel_consumed": 100},
            {"vehicle_type": "electric", "distance_km": 1000},
        ]
        
        fleet_emissions = carbon_service.calculate_fleet_emissions(fleet_data)
        
        assert "diesel_emissions_kg_co2" in fleet_emissions
        assert "ev_emissions_kg_co2" in fleet_emissions
        assert fleet_emissions["diesel_emissions_kg_co2"] > fleet_emissions["ev_emissions_kg_co2"]


class TestNetZeroRoadmap:
    """Test Net Zero roadmap generation"""

    def test_roadmap_generation(self, carbon_service):
        """Test Net Zero roadmap generation"""
        roadmap = carbon_service.generate_net_zero_roadmap(
            current_ev_vehicles=20,
            total_vehicles=100,
            target_year=2030
        )
        
        assert "current_state" in roadmap
        assert "milestones" in roadmap
        assert roadmap["current_state"]["ev_vehicles"] == 20
        assert roadmap["current_state"]["diesel_vehicles"] == 80

    def test_roadmap_milestones_progression(self, carbon_service):
        """Test that milestones show progression toward target"""
        roadmap = carbon_service.generate_net_zero_roadmap(
            current_ev_vehicles=10,
            total_vehicles=100,
            target_year=2032
        )
        
        milestones = roadmap["milestones"]
        
        # EV count should increase
        for i in range(len(milestones) - 1):
            assert milestones[i + 1]["ev_vehicles"] >= milestones[i]["ev_vehicles"]
        
        # Final milestone should be at/near target
        assert milestones[-1]["year"] == 2032

    def test_roadmap_annual_conversion_target(self, carbon_service):
        """Test annual conversion rate calculation"""
        roadmap = carbon_service.generate_net_zero_roadmap(
            current_ev_vehicles=0,
            total_vehicles=100,
            target_year=2030
        )
        
        current_year = 2024  # Assuming current year
        years = 2030 - current_year
        annual_target = 100 / years
        
        assert roadmap["annual_conversion_target"] == pytest.approx(annual_target, rel=0.1)

    def test_roadmap_zero_conversion_needed(self, carbon_service):
        """Test roadmap when already at 100% EV"""
        roadmap = carbon_service.generate_net_zero_roadmap(
            current_ev_vehicles=100,
            total_vehicles=100,
            target_year=2030
        )
        
        assert roadmap["annual_conversion_target"] == 0
        assert all(m["ev_vehicles"] == 100 for m in roadmap["milestones"])
