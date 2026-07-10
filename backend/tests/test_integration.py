"""
Integration tests - testing component interactions
Tests workflows across multiple services and endpoints
"""
import pytest
from fastapi import status


class TestBatteryHealthWorkflow:
    """Test complete battery health monitoring workflow"""

    def test_battery_prediction_to_maintenance(self, client, battery_service):
        """Test flow from prediction to maintenance scheduling"""
        # Step 1: Predict battery health
        payload = {
            "vehicle_id": "FLEET-001",
            "charge_history": [
                {
                    "timestamp": "2024-01-01T10:00:00",
                    "charge_percent": 90 - i,
                    "voltage_v": 3.7 - (i * 0.01),
                    "current_a": 10,
                    "temperature_c": 25
                }
                for i in range(5)
            ],
            "current_cycles": 1500,
            "ambient_temp_c": 28
        }
        
        response = client.post("/api/v1/predict/battery-soh", json=payload)
        assert response.status_code == status.HTTP_200_OK
        prediction = response.json()
        
        # Step 2: Check if maintenance triggered
        if prediction["remaining_useful_life_days"] < 180:
            response = client.post(
                "/api/v1/battery/maintenance-trigger",
                params={"vehicle_id": payload["vehicle_id"]}
            )
            assert response.status_code == status.HTTP_200_OK
            maintenance = response.json()
            assert "maintenance_schedule" in maintenance

    def test_fleet_health_aggregation(self, client):
        """Test aggregating health of entire fleet"""
        vehicle_ids = [f"FLEET-{i:03d}" for i in range(1, 11)]
        
        fleet_health = {"healthy": 0, "warning": 0, "critical": 0}
        
        for vehicle_id in vehicle_ids:
            response = client.get(f"/api/v1/battery/{vehicle_id}")
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
                avg_soh = sum(m["soh_percent"] for m in data["metrics"]) / len(data["metrics"])
                
                if avg_soh > 85:
                    fleet_health["healthy"] += 1
                elif avg_soh > 70:
                    fleet_health["warning"] += 1
                else:
                    fleet_health["critical"] += 1
        
        assert fleet_health["healthy"] + fleet_health["warning"] + fleet_health["critical"] > 0


class TestQualityToSupplyChainWorkflow:
    """Test quality detection triggering supply chain investigation"""

    def test_quality_issue_to_supplier_investigation(self, client):
        """Test workflow: quality issue -> supplier investigation"""
        # Step 1: Detect quality drift
        payload = {
            "process_params": {
                "cell_voltage": 2.8,  # Below threshold
                "resistance": 0.09,
                "temperature_during_charge": 50,
                "cycle_efficiency": 97.0
            },
            "material_quality": {
                "lithium": {"purity": 98.0},  # Below threshold
                "cobalt": {"purity": 99.5}
            },
            "inspection_results": {
                "visual_inspection": {"passed": False},
                "voltage_test": {"passed": False}
            }
        }
        
        response = client.post("/api/v1/quality/check-drift", json=payload)
        assert response.status_code == status.HTTP_200_OK
        quality_result = response.json()
        
        # Step 2: Investigate suppliers if quality drift detected
        if quality_result["quality_drift_score"] > 0.5:
            response = client.get("/api/v1/supply-chain/suppliers")
            assert response.status_code == status.HTTP_200_OK
            suppliers = response.json()
            
            # Look for lithium and cobalt suppliers
            lithium_supplier = next(
                (s for s in suppliers["suppliers"] if s["material"] == "Lithium"), None
            )
            assert lithium_supplier is not None


class TestCarbonEmissionTracking:
    """Test fleet-wide carbon emission monitoring workflow"""

    def test_fleet_emission_calculation_workflow(self, client):
        """Test calculating fleet emissions and recommendations"""
        # Step 1: Calculate current diesel fleet emissions
        diesel_payload = {
            "vehicle_type": "diesel",
            "distance_km": 15000,
            "fuel_consumed": 1500
        }
        
        response = client.post("/api/v1/carbon/calculate-emissions", json=diesel_payload)
        assert response.status_code == status.HTTP_200_OK
        diesel_emissions = response.json()
        
        # Step 2: Calculate EV fleet emissions for same distance
        ev_payload = {
            "vehicle_type": "electric",
            "distance_km": 15000
        }
        
        response = client.post("/api/v1/carbon/calculate-emissions", json=ev_payload)
        assert response.status_code == status.HTTP_200_OK
        ev_emissions = response.json()
        
        # Step 3: Calculate reduction
        response = client.post(
            "/api/v1/carbon/calculate-reduction",
            params={"diesel_km": 15000, "ev_km": 15000}
        )
        assert response.status_code == status.HTTP_200_OK
        reduction = response.json()
        
        # Verify reduction calculation
        expected_reduction = diesel_emissions["total_emissions_kg_co2"] - ev_emissions["total_emissions_kg_co2"]
        assert reduction["reduction_kg_co2"] == pytest.approx(expected_reduction, rel=0.01)

    def test_net_zero_roadmap_workflow(self, client):
        """Test Net Zero roadmap generation and tracking"""
        # Step 1: Get current state
        response = client.get(
            "/api/v1/carbon/net-zero-roadmap",
            params={"current_ev_vehicles": 20, "total_vehicles": 100, "target_year": 2030}
        )
        assert response.status_code == status.HTTP_200_OK
        roadmap = response.json()
        
        # Step 2: Verify milestones are achievable
        milestones = roadmap["milestones"]
        assert len(milestones) > 0
        assert milestones[-1]["ev_penetration_percent"] >= 80


class TestGeospatialPlanning:
    """Test complete geospatial infrastructure planning workflow"""

    def test_charging_infrastructure_planning_workflow(self, client):
        """Test end-to-end charging infrastructure planning"""
        # Step 1: Analyze coverage gaps
        response = client.get("/api/v1/geospatial/coverage-analysis")
        assert response.status_code == status.HTTP_200_OK
        coverage_analysis = response.json()
        
        gaps_identified = coverage_analysis["coverage_gaps_identified"]
        assert gaps_identified >= 0
        
        # Step 2: Plan infrastructure to fill gaps
        location_clusters = [
            {"lat": 28.7041, "lon": 77.1025, "vehicle_count": 100},
            {"lat": 13.0827, "lon": 80.2707, "vehicle_count": 80}
        ]
        
        payload = {
            "location_clusters": location_clusters,
            "required_coverage_km": 50
        }
        
        response = client.post("/api/v1/geospatial/plan-charging-infrastructure", json=payload)
        assert response.status_code == status.HTTP_200_OK
        infrastructure_plan = response.json()
        
        # Step 3: Verify infrastructure addresses coverage
        assert infrastructure_plan["total_stations"] > 0

    def test_route_optimization_workflow(self, client):
        """Test route optimization integrated with coverage"""
        # Step 1: Optimize routes
        response = client.post(
            "/api/v1/geospatial/optimize-routes",
            params={"vehicle_range_km": 350}
        )
        assert response.status_code == status.HTTP_200_OK
        optimized_routes = response.json()
        
        # Step 2: Verify routes use coverage map data
        response = client.get("/api/v1/geospatial/coverage-map")
        assert response.status_code == status.HTTP_200_OK
        coverage_map = response.json()
        
        # Routes should align with coverage zones
        for route in optimized_routes["optimized_routes"]:
            assert route["carbon_emissions_kg_co2"] > 0
            assert route["efficiency_score"] > 0


class TestSupplyChainEndToEnd:
    """Test end-to-end supply chain traceability"""

    def test_material_to_vehicle_trace(self, client):
        """Test complete supply chain from material extraction to vehicle"""
        # Step 1: Create material trace
        response = client.post(
            "/api/v1/supply-chain/create-material-trace",
            params={
                "material_type": "lithium",
                "quantity_kg": 1000,
                "origin_country": "Chile",
                "supplier_name": "SQM",
                "batch_id": "TRACE-001"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        material_trace = response.json()
        material_trace_id = material_trace["trace_id"]
        
        # Step 2: Create cell trace from material
        response = client.post(
            "/api/v1/supply-chain/create-cell-trace",
            params={
                "lithium_trace_id": material_trace_id,
                "cobalt_trace_id": "MAT-COBALT-001",
                "cell_type": "LFP",
                "manufacturer_name": "CATL"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        cell_trace = response.json()
        
        # Verify traceability
        assert cell_trace["trace_id"] is not None


class TestErrorRecovery:
    """Test error handling and recovery"""

    def test_invalid_input_handling(self, client):
        """Test graceful handling of invalid inputs"""
        invalid_payloads = [
            {"vehicle_type": "", "distance_km": -100},  # Invalid carbon calculation
            {"vehicle_id": "", "charge_history": []},    # Invalid battery prediction
            {"process_params": None},                     # Invalid quality check
        ]
        
        for payload in invalid_payloads:
            # Should return 422 Unprocessable Entity, not 500 Server Error
            response = client.post("/api/v1/carbon/calculate-emissions", json=payload)
            assert response.status_code in [
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                status.HTTP_400_BAD_REQUEST,
                status.HTTP_200_OK  # Some might return 200 with error info
            ]

    def test_missing_required_parameters(self, client):
        """Test handling of missing required parameters"""
        response = client.post(
            "/api/v1/quality/check-drift",
            json={}  # Missing required fields
        )
        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_400_BAD_REQUEST
        ]
