"""
Integration tests for all API endpoints
Tests request/response formats, error handling, and business logic
"""
import pytest
from fastapi import status


class TestBatteryRoutes:
    """Test battery health and prediction endpoints"""

    def test_predict_battery_soh_endpoint(self, client):
        """Test battery SOH prediction endpoint"""
        payload = {
            "vehicle_id": "EV-001",
            "charge_history": [
                {
                    "timestamp": "2024-01-01T10:00:00",
                    "charge_percent": 95,
                    "voltage_v": 3.7,
                    "current_a": 10,
                    "temperature_c": 25
                }
            ],
            "current_cycles": 500,
            "ambient_temp_c": 25
        }
        
        response = client.post("/api/v1/predict/battery-soh", json=payload)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["vehicle_id"] == "EV-001"
        assert 0 <= data["current_soh"] <= 100
        assert data["remaining_useful_life_days"] > 0

    def test_battery_history_endpoint(self, client):
        """Test battery history retrieval"""
        response = client.get("/api/v1/battery/EV-001?days=30")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["vehicle_id"] == "EV-001"
        assert len(data["metrics"]) == 30

    def test_battery_prediction_invalid_data(self, client):
        """Test battery prediction with invalid data"""
        payload = {
            "vehicle_id": "",
            "charge_history": [],
            "current_cycles": -1,
            "ambient_temp_c": 100
        }
        
        response = client.post("/api/v1/predict/battery-soh", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestSupplyChainRoutes:
    """Test supply chain risk endpoints"""

    def test_supply_chain_risk_score(self, client):
        """Test overall supply chain risk score"""
        response = client.get("/api/v1/supply-chain/risk-score")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 0 <= data["overall_risk_score"] <= 1
        assert "risk_breakdown" in data
        assert "top_risk_factors" in data

    def test_supplier_risks_endpoint(self, client):
        """Test supplier risk profile endpoint"""
        response = client.get("/api/v1/supply-chain/suppliers")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "suppliers" in data
        assert len(data["suppliers"]) > 0
        
        supplier = data["suppliers"][0]
        assert "risk_score" in supplier
        assert 0 <= supplier["risk_score"] <= 100


class TestQualityRoutes:
    """Test quality intelligence endpoints"""

    def test_quality_drift_check(self, client):
        """Test quality drift detection endpoint"""
        payload = {
            "process_params": {
                "cell_voltage": 3.15,
                "resistance": 0.035,
                "temperature_during_charge": 28.5
            },
            "material_quality": {
                "lithium": {"purity": 99.8},
                "cobalt": {"purity": 99.5}
            },
            "inspection_results": {
                "visual_inspection": {"passed": True},
                "voltage_test": {"passed": True}
            }
        }
        
        response = client.post("/api/v1/quality/check-drift", json=payload)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "quality_drift_score" in data
        assert "anomalies_detected" in data

    def test_quality_dashboard_endpoint(self, client):
        """Test quality dashboard endpoint"""
        response = client.get("/api/v1/quality/dashboard?timeframe_days=7")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["period_days"] == 7
        assert "metrics" in data
        assert "top_issues" in data


class TestCarbonRoutes:
    """Test carbon emissions tracking endpoints"""

    def test_calculate_emissions_diesel(self, client):
        """Test emission calculation for diesel vehicle"""
        payload = {
            "vehicle_type": "diesel",
            "distance_km": 1000,
            "fuel_consumed": 100
        }
        
        response = client.post("/api/v1/carbon/calculate-emissions", json=payload)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["vehicle_type"] == "diesel"
        assert data["scope1_kg_co2"] > 0
        assert data["scope3_kg_co2"] > 0

    def test_calculate_emissions_electric(self, client):
        """Test emission calculation for EV"""
        payload = {
            "vehicle_type": "electric",
            "distance_km": 1000
        }
        
        response = client.post("/api/v1/carbon/calculate-emissions", json=payload)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["scope1_kg_co2"] == 0
        assert data["scope3_kg_co2"] > 0

    def test_emission_reduction_calculation(self, client):
        """Test emission reduction calculation"""
        response = client.post(
            "/api/v1/carbon/calculate-reduction",
            params={"diesel_km": 10000, "ev_km": 10000}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["reduction_kg_co2"] > 0
        assert 0 <= data["reduction_percent"] <= 100

    def test_net_zero_roadmap(self, client):
        """Test Net Zero roadmap generation"""
        response = client.get(
            "/api/v1/carbon/net-zero-roadmap",
            params={"current_ev_vehicles": 20, "total_vehicles": 100, "target_year": 2030}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "current_state" in data
        assert "milestones" in data
        assert len(data["milestones"]) > 0


class TestGeospatialRoutes:
    """Test geospatial visualization endpoints"""

    def test_plan_charging_infrastructure(self, client):
        """Test charging infrastructure planning"""
        payload = {
            "location_clusters": [
                {"lat": 28.7041, "lon": 77.1025, "vehicle_count": 50},
                {"lat": 13.0827, "lon": 80.2707, "vehicle_count": 40}
            ],
            "required_coverage_km": 50
        }
        
        response = client.post("/api/v1/geospatial/plan-charging-infrastructure", json=payload)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "recommended_charging_stations" in data
        assert len(data["recommended_charging_stations"]) > 0

    def test_coverage_analysis(self, client):
        """Test coverage gap analysis"""
        response = client.get("/api/v1/geospatial/coverage-analysis")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "coverage_gaps_identified" in data
        assert "gaps" in data

    def test_optimize_routes_for_ev(self, client):
        """Test EV route optimization"""
        response = client.post(
            "/api/v1/geospatial/optimize-routes",
            params={"vehicle_range_km": 350}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "optimized_routes" in data
        assert len(data["optimized_routes"]) > 0

    def test_coverage_map(self, client):
        """Test coverage map generation"""
        response = client.get("/api/v1/geospatial/coverage-map")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "coverage_zones" in data
        assert "coverage_percent" in data


class TestSupplyChainTraceability:
    """Test supply chain traceability endpoints"""

    def test_create_material_trace(self, client):
        """Test creating material trace"""
        response = client.post(
            "/api/v1/supply-chain/create-material-trace",
            params={
                "material_type": "lithium",
                "quantity_kg": 1000,
                "origin_country": "Chile",
                "supplier_name": "SQM",
                "batch_id": "BATCH-001"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["material_type"] == "lithium"
        assert "trace_id" in data

    def test_create_cell_trace(self, client):
        """Test creating battery cell trace"""
        response = client.post(
            "/api/v1/supply-chain/create-cell-trace",
            params={
                "lithium_trace_id": "MAT-LI-001",
                "cobalt_trace_id": "MAT-CO-001",
                "cell_type": "LFP",
                "manufacturer_name": "CATL"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "trace_id" in data
