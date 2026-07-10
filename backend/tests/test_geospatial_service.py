"""
Unit tests for Geospatial Service
Tests charging infrastructure planning, coverage analysis, and route optimization
"""
import pytest
import math


class TestChargingInfrastructurePlanning:
    """Test charging station location planning"""

    def test_plan_infrastructure_basic(self, geospatial_service):
        """Test basic charging infrastructure planning"""
        location_clusters = [
            {"lat": 28.7041, "lon": 77.1025, "vehicle_count": 50},
            {"lat": 13.0827, "lon": 80.2707, "vehicle_count": 40}
        ]
        
        result = geospatial_service.plan_charging_infrastructure(
            location_clusters=location_clusters,
            required_coverage_km=50
        )
        
        assert "recommended_charging_stations" in result
        assert len(result["recommended_charging_stations"]) > 0
        assert result["total_stations"] > 0
        assert result["total_dc_fast_chargers"] > 0

    def test_infrastructure_capacity_calculation(self, geospatial_service):
        """Test charging capacity calculation"""
        location_clusters = [
            {"lat": 28.7041, "lon": 77.1025, "vehicle_count": 100}
        ]
        
        result = geospatial_service.plan_charging_infrastructure(
            location_clusters=location_clusters,
            required_coverage_km=50
        )
        
        total_kw = sum(s["total_capacity_kw"] for s in result["recommended_charging_stations"])
        assert total_kw > 0
        assert result["total_capacity_kw"] == pytest.approx(total_kw, rel=0.01)

    def test_infrastructure_investment_estimate(self, geospatial_service):
        """Test investment estimation for charging infrastructure"""
        location_clusters = [
            {"lat": 28.7041, "lon": 77.1025, "vehicle_count": 50}
        ]
        
        result = geospatial_service.plan_charging_infrastructure(
            location_clusters=location_clusters,
            required_coverage_km=50
        )
        
        assert "total_investment_estimate_crores" in result
        assert result["total_investment_estimate_crores"] > 0
        assert "payback_period_years" in result


class TestCoverageAnalysis:
    """Test coverage gap analysis"""

    def test_coverage_gap_identification(self, geospatial_service):
        """Test identification of coverage gaps"""
        result = geospatial_service.analyze_coverage_gaps(coverage_radius_km=50)
        
        assert "coverage_gaps_identified" in result
        assert "gaps" in result
        
        if result["coverage_gaps_identified"] > 0:
            gap = result["gaps"][0]
            assert "location_name" in gap
            assert "vehicles_affected" in gap
            assert "coverage_gap_km" in gap

    def test_gap_priority_assignment(self, geospatial_service):
        """Test priority assignment for coverage gaps"""
        result = geospatial_service.analyze_coverage_gaps(coverage_radius_km=50)
        
        for gap in result["gaps"]:
            assert gap["priority"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            assert gap["vehicles_affected"] > 0


class TestRouteOptimization:
    """Test EV route optimization"""

    def test_optimize_single_route(self, geospatial_service):
        """Test optimization of single route"""
        result = geospatial_service.optimize_routes_for_ev(vehicle_range_km=350)
        
        assert "optimized_routes" in result
        assert len(result["optimized_routes"]) > 0
        
        route = result["optimized_routes"][0]
        assert "total_distance_km" in route
        assert "charging_stops_required" in route
        assert route["charging_stops_required"] > 0

    def test_charging_stop_calculation(self, geospatial_service):
        """Test charging stop calculation based on vehicle range"""
        result = geospatial_service.optimize_routes_for_ev(vehicle_range_km=400)
        
        for route in result["optimized_routes"]:
            expected_stops = math.ceil(route["total_distance_km"] / 400) - 1
            assert route["charging_stops_required"] >= max(0, expected_stops - 1)

    def test_charging_stop_locations(self, geospatial_service):
        """Test charging stop location calculation"""
        result = geospatial_service.optimize_routes_for_ev(vehicle_range_km=350)
        
        for route in result["optimized_routes"]:
            stops = route["charging_stop_locations"]
            assert len(stops) == route["charging_stops_required"]
            
            # Stops should be evenly spaced
            for stop in stops:
                assert 0 < stop["distance_from_start_km"] < route["total_distance_km"]

    def test_efficiency_score_calculation(self, geospatial_service):
        """Test route efficiency score"""
        result = geospatial_service.optimize_routes_for_ev(vehicle_range_km=350)
        
        for route in result["optimized_routes"]:
            assert "efficiency_score" in route
            assert 0 <= route["efficiency_score"] <= 100

    def test_carbon_emissions_per_route(self, geospatial_service):
        """Test carbon emissions calculation for optimized route"""
        result = geospatial_service.optimize_routes_for_ev(vehicle_range_km=350)
        
        for route in result["optimized_routes"]:
            assert "carbon_emissions_kg_co2" in route
            assert route["carbon_emissions_kg_co2"] > 0


class TestCoverageMap:
    """Test coverage map generation"""

    def test_coverage_map_generation(self, geospatial_service):
        """Test basic coverage map generation"""
        result = geospatial_service.generate_coverage_map()
        
        assert "coverage_zones" in result
        assert len(result["coverage_zones"]) > 0
        assert "total_vehicles_covered" in result
        assert "coverage_percent" in result

    def test_coverage_zone_details(self, geospatial_service):
        """Test coverage zone detail accuracy"""
        result = geospatial_service.generate_coverage_map()
        
        for zone in result["coverage_zones"]:
            assert "charger_name" in zone
            assert "location" in zone
            assert "capacity_kw" in zone
            assert "coverage_radius_km" in zone
            assert 0 <= zone["coverage_utilization_percent"] <= 100

    def test_total_coverage_calculation(self, geospatial_service):
        """Test total coverage percentage calculation"""
        result = geospatial_service.generate_coverage_map()
        
        assert 0 <= result["coverage_percent"] <= 100
        
        total_covered = sum(z["vehicles_covered"] for z in result["coverage_zones"])
        assert result["total_vehicles_covered"] == total_covered


class TestDistanceCalculations:
    """Test geographic distance calculations"""

    def test_haversine_distance(self, geospatial_service):
        """Test haversine distance calculation between two points"""
        # Delhi to Bangalore coordinates
        delhi = {"lat": 28.7041, "lon": 77.1025}
        bangalore = {"lat": 12.9716, "lon": 77.5946}
        
        distance = geospatial_service.calculate_distance(delhi, bangalore)
        
        # Approximate distance Delhi-Bangalore ~1800 km
        assert 1700 < distance < 1900

    def test_point_in_radius(self, geospatial_service):
        """Test point within radius calculation"""
        center = {"lat": 28.7041, "lon": 77.1025}
        point = {"lat": 28.7150, "lon": 77.1100}
        radius_km = 50
        
        is_within = geospatial_service.is_point_within_radius(center, point, radius_km)
        assert is_within is True

    def test_point_outside_radius(self, geospatial_service):
        """Test point outside radius calculation"""
        center = {"lat": 28.7041, "lon": 77.1025}
        point = {"lat": 29.9, "lon": 78.2}  # ~150 km away
        radius_km = 50
        
        is_within = geospatial_service.is_point_within_radius(center, point, radius_km)
        assert is_within is False
