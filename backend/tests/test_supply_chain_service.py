"""
Unit tests for Supply Chain Traceability Service
Tests end-to-end material tracking from extraction to vehicle integration
"""
import pytest


class TestMaterialExtraction:
    """Test raw material extraction tracking"""

    def test_create_lithium_trace(self, supply_chain_service):
        """Test lithium extraction trace creation"""
        trace = supply_chain_service.create_material_trace(
            material_type="lithium",
            quantity_kg=1000,
            origin_country="Chile",
            supplier_name="SQM",
            batch_id="LI-BATCH-001"
        )
        
        assert trace["material_type"] == "lithium"
        assert trace["quantity_kg"] == 1000
        assert "trace_id" in trace
        assert trace["status"] == "extracted"
        assert 0 <= trace["quality_score"] <= 100

    def test_create_cobalt_trace(self, supply_chain_service):
        """Test cobalt extraction trace creation"""
        trace = supply_chain_service.create_material_trace(
            material_type="cobalt",
            quantity_kg=500,
            origin_country="Democratic Republic Congo",
            supplier_name="Glencore",
            batch_id="CO-BATCH-001"
        )
        
        assert trace["material_type"] == "cobalt"
        assert "trace_id" in trace

    def test_material_quality_scoring(self, supply_chain_service):
        """Test material quality scoring"""
        trace = supply_chain_service.create_material_trace(
            material_type="nickel",
            quantity_kg=800,
            origin_country="Indonesia",
            supplier_name="Vale",
            batch_id="NI-BATCH-001"
        )
        
        assert 90 <= trace["quality_score"] <= 100

    def test_material_risk_assessment(self, supply_chain_service):
        """Test material risk assessment"""
        trace = supply_chain_service.create_material_trace(
            material_type="lithium",
            quantity_kg=1000,
            origin_country="Afghanistan",
            supplier_name="Unknown",
            batch_id="RISK-001"
        )
        
        assert trace["risk_assessment"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class TestBatteryCellTracing:
    """Test battery cell assembly tracing"""

    def test_create_cell_trace_lfp(self, supply_chain_service):
        """Test LFP cell trace creation"""
        trace = supply_chain_service.create_cell_trace(
            lithium_trace_id="MAT-LI-001",
            cobalt_trace_id="MAT-CO-001",
            cell_type="LFP",
            manufacturer_name="CATL"
        )
        
        assert trace["material_type"] == "LFP"
        assert trace["status"] == "assembled"
        assert "trace_id" in trace
        assert len(trace["trace_id"]) > 10

    def test_create_cell_trace_ncm(self, supply_chain_service):
        """Test NCM cell trace creation"""
        trace = supply_chain_service.create_cell_trace(
            lithium_trace_id="MAT-LI-002",
            cobalt_trace_id="MAT-CO-002",
            cell_type="NCM811",
            manufacturer_name="Samsung"
        )
        
        assert trace["material_type"] == "NCM811"

    def test_cell_traceability_to_materials(self, supply_chain_service):
        """Test cell traceability links back to materials"""
        cell_trace = supply_chain_service.create_cell_trace(
            lithium_trace_id="MAT-LI-001",
            cobalt_trace_id="MAT-CO-001",
            cell_type="LFP",
            manufacturer_name="CATL"
        )
        
        assert "source_materials" in cell_trace
        assert cell_trace["source_materials"]["lithium"] == "MAT-LI-001"
        assert cell_trace["source_materials"]["cobalt"] == "MAT-CO-001"


class TestBatteryPackAssembly:
    """Test battery pack assembly tracing"""

    def test_create_battery_pack_trace(self, supply_chain_service):
        """Test battery pack trace creation"""
        cell_traces = ["CELL-001", "CELL-002", "CELL-003", "CELL-004"]
        
        trace = supply_chain_service.create_battery_pack_trace(
            cell_traces=cell_traces,
            pack_type="50kWh",
            manufacturer_name="BYD",
            quality_test_passed=True
        )
        
        assert trace["pack_type"] == "50kWh"
        assert trace["status"] == "assembled"
        assert "trace_id" in trace
        assert len(trace["source_cells"]) == 4

    def test_battery_pack_quality_certification(self, supply_chain_service):
        """Test battery pack quality certification"""
        trace = supply_chain_service.create_battery_pack_trace(
            cell_traces=["CELL-001", "CELL-002"],
            pack_type="40kWh",
            manufacturer_name="BYD",
            quality_test_passed=True
        )
        
        assert trace["certified"] is True

    def test_battery_pack_safety_records(self, supply_chain_service):
        """Test battery pack safety records tracking"""
        trace = supply_chain_service.create_battery_pack_trace(
            cell_traces=["CELL-001"],
            pack_type="30kWh",
            manufacturer_name="CATL",
            quality_test_passed=True
        )
        
        assert "safety_certifications" in trace
        assert len(trace["safety_certifications"]) > 0


class TestVehicleIntegration:
    """Test vehicle integration tracking"""

    def test_integrate_battery_to_vehicle(self, supply_chain_service):
        """Test battery pack integration to vehicle"""
        trace = supply_chain_service.integrate_battery_to_vehicle(
            battery_pack_trace_id="PACK-001",
            vehicle_vin="ABCD1234567890",
            vehicle_model="Nexon EV",
            manufacturer_name="Tata Motors",
            integration_date="2024-01-15"
        )
        
        assert trace["vehicle_vin"] == "ABCD1234567890"
        assert trace["status"] == "integrated"
        assert "trace_id" in trace

    def test_complete_supply_chain_trace(self, supply_chain_service):
        """Test complete end-to-end supply chain trace"""
        trace = supply_chain_service.get_complete_trace(vehicle_vin="ABCD1234567890")
        
        assert "material_extraction" in trace
        assert "cell_assembly" in trace
        assert "battery_pack_assembly" in trace
        assert "vehicle_integration" in trace
        
        # Verify chain of custody
        assert len(trace["chain_of_custody"]) > 0


class TestSupplyChainValidation:
    """Test supply chain validation and integrity"""

    def test_trace_integrity_validation(self, supply_chain_service):
        """Test trace integrity validation"""
        trace_data = {
            "material_trace_id": "MAT-001",
            "cell_trace_id": "CELL-001",
            "pack_trace_id": "PACK-001",
            "vehicle_vin": "VIN-001"
        }
        
        is_valid = supply_chain_service.validate_trace_integrity(trace_data)
        assert is_valid is True

    def test_detect_counterfeit_components(self, supply_chain_service):
        """Test detection of counterfeit components"""
        suspicious_trace = {
            "material_trace_id": "FAKE-001",
            "origin_country": "Unknown",
            "supplier_name": "Unverified",
            "certifications": []
        }
        
        is_legitimate = supply_chain_service.verify_component_legitimacy(suspicious_trace)
        assert is_legitimate is False

    def test_supply_chain_compliance_check(self, supply_chain_service):
        """Test supply chain compliance verification"""
        trace = supply_chain_service.create_material_trace(
            material_type="lithium",
            quantity_kg=1000,
            origin_country="Chile",
            supplier_name="SQM",
            batch_id="COMPLIANT-001"
        )
        
        compliance = supply_chain_service.check_compliance(trace)
        assert "compliant" in compliance
        assert compliance["certifications"] is not None


class TestTraceReporting:
    """Test supply chain trace reporting"""

    def test_generate_trace_report(self, supply_chain_service):
        """Test generation of supply chain trace report"""
        report = supply_chain_service.generate_trace_report(
            vehicle_vin="ABCD1234567890"
        )
        
        assert "vehicle_vin" in report
        assert "trace_timeline" in report
        assert "material_origins" in report
        assert "manufacturers" in report
        assert "compliance_status" in report

    def test_trace_timeline_accuracy(self, supply_chain_service):
        """Test trace timeline is accurate and complete"""
        report = supply_chain_service.generate_trace_report(vehicle_vin="VIN-001")
        
        timeline = report["trace_timeline"]
        assert len(timeline) > 0
        
        # Timeline should be in chronological order
        for i in range(len(timeline) - 1):
            assert timeline[i]["timestamp"] <= timeline[i + 1]["timestamp"]
