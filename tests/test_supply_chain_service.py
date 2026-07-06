"""
Test cases for Supply Chain Service
Tests supply chain risk assessment, geopolitical analysis, and supplier management
"""

import pytest
from services.supply_chain_service import SupplyChainService


class TestSupplyChainServiceRiskCalculation:
    """Test suite for risk calculation methods"""
    
    def test_calculate_overall_risk_low(self):
        """Test overall risk calculation - low risk scenario"""
        overall, level = SupplyChainService.calculate_overall_risk(
            geopolitical_score=0.2,
            concentration_score=0.3,
            quality_score=0.2,
            logistics_score=0.1
        )
        
        assert 0 <= overall <= 1
        assert level == "Low"
    
    def test_calculate_overall_risk_medium(self):
        """Test overall risk calculation - medium risk scenario"""
        overall, level = SupplyChainService.calculate_overall_risk(
            geopolitical_score=0.5,
            concentration_score=0.4,
            quality_score=0.3,
            logistics_score=0.3
        )
        
        assert 0 <= overall <= 1
        assert level == "Medium"
    
    def test_calculate_overall_risk_high(self):
        """Test overall risk calculation - high risk scenario"""
        overall, level = SupplyChainService.calculate_overall_risk(
            geopolitical_score=0.7,
            concentration_score=0.65,
            quality_score=0.5,
            logistics_score=0.4
        )
        
        assert 0 <= overall <= 1
        assert level == "High"
    
    def test_calculate_overall_risk_critical(self):
        """Test overall risk calculation - critical risk scenario"""
        overall, level = SupplyChainService.calculate_overall_risk(
            geopolitical_score=0.9,
            concentration_score=0.85,
            quality_score=0.7,
            logistics_score=0.6
        )
        
        assert 0 <= overall <= 1
        assert level == "Critical"
    
    def test_calculate_overall_risk_weights(self):
        """Test that risk weights sum to 1.0"""
        weights = SupplyChainService.RISK_WEIGHTS
        total_weight = sum(weights.values())
        
        assert abs(total_weight - 1.0) < 0.001, "Risk weights must sum to 1.0"
    
    def test_calculate_overall_risk_clamping(self):
        """Test that overall risk is clamped to 0-1 range"""
        # Test with extreme values
        overall, _ = SupplyChainService.calculate_overall_risk(
            geopolitical_score=2.0,  # Above max
            concentration_score=-0.5,  # Below min
            quality_score=1.5,
            logistics_score=0.5
        )
        
        assert 0 <= overall <= 1


class TestSupplyChainServiceSupplierRisk:
    """Test suite for supplier risk assessment"""
    
    def test_calculate_supplier_risk_basic(self, sample_supplier_data):
        """Test basic supplier risk calculation"""
        supplier = sample_supplier_data[0]
        
        result = SupplyChainService.calculate_supplier_risk(
            supplier_data=supplier,
            country=supplier["country"],
            material=supplier["material"],
            concentration_percent=supplier["concentration_percentage"],
            quality_metrics={
                "defect_rate_ppm": supplier["defect_rate_ppm"],
                "on_time_delivery_percent": supplier["on_time_delivery_percent"],
                "invoice_accuracy_percent": supplier["invoice_accuracy_percent"],
                "delivery_risk": 0.4
            }
        )
        
        assert "overall_risk_score" in result
        assert "risk_level" in result
        assert "geopolitical_risk" in result
        assert "concentration_risk" in result
        assert "quality_risk" in result
        assert "delivery_risk" in result
        
        # Risk scores should be in valid range
        assert 0 <= result["overall_risk_score"] <= 1
    
    def test_calculate_supplier_risk_high_concentration(self, sample_supplier_data):
        """Test supplier risk with high concentration"""
        supplier = sample_supplier_data[1]  # Cobalt supplier with 60% concentration
        
        result = SupplyChainService.calculate_supplier_risk(
            supplier_data=supplier,
            country="DR Congo",
            material="Cobalt",
            concentration_percent=60,  # High concentration
            quality_metrics={
                "defect_rate_ppm": 350,
                "on_time_delivery_percent": 88,
                "invoice_accuracy_percent": 97.5,
                "delivery_risk": 0.6
            }
        )
        
        # High concentration should increase risk
        assert result["concentration_risk"] > 0.5
        assert result["risk_level"] in ["High", "Critical"]
    
    def test_calculate_supplier_risk_country_risk(self):
        """Test that country risk is properly applied"""
        # China supplier
        result_china = SupplyChainService.calculate_supplier_risk(
            supplier_data={"supplier_id": "TEST"},
            country="China",
            material="Lithium",
            concentration_percent=30,
            quality_metrics={"delivery_risk": 0.3}
        )
        
        # Australia supplier
        result_australia = SupplyChainService.calculate_supplier_risk(
            supplier_data={"supplier_id": "TEST"},
            country="Australia",
            material="Lithium",
            concentration_percent=30,
            quality_metrics={"delivery_risk": 0.3}
        )
        
        # China should have higher geopolitical risk
        assert result_china["geopolitical_risk"] > result_australia["geopolitical_risk"]
    
    def test_calculate_quality_risk(self):
        """Test quality risk calculation"""
        # Good quality
        good_quality = {
            "defect_rate_ppm": 100,
            "on_time_delivery_percent": 98,
            "invoice_accuracy_percent": 99.5
        }
        good_risk = SupplyChainService._calculate_quality_risk(good_quality)
        
        # Poor quality
        poor_quality = {
            "defect_rate_ppm": 1000,
            "on_time_delivery_percent": 85,
            "invoice_accuracy_percent": 90
        }
        poor_risk = SupplyChainService._calculate_quality_risk(poor_quality)
        
        assert good_risk < poor_risk
        assert 0 <= good_risk <= 1
        assert 0 <= poor_risk <= 1


class TestSupplyChainServiceGeopolitical:
    """Test suite for geopolitical event assessment"""
    
    def test_assess_geopolitical_events_basic(self, sample_geopolitical_event):
        """Test basic geopolitical event assessment"""
        result = SupplyChainService.assess_geopolitical_events(
            events=[sample_geopolitical_event],
            affected_suppliers=["LTH_001", "LTH_002"]
        )
        
        assert "total_events" in result
        assert "avg_impact_score" in result
        assert "affected_suppliers" in result
        assert "recommendation" in result
        
        assert result["total_events"] == 1
        assert result["affected_suppliers"] == 2
    
    def test_assess_geopolitical_events_multiple(self):
        """Test assessment with multiple events"""
        events = [
            {"severity": "low", "impact_on_supply": 0.3},
            {"severity": "medium", "impact_on_supply": 0.5},
            {"severity": "high", "impact_on_supply": 0.8}
        ]
        
        result = SupplyChainService.assess_geopolitical_events(
            events=events,
            affected_suppliers=["S1", "S2", "S3"]
        )
        
        assert result["total_events"] == 3
        assert 0 <= result["avg_impact_score"] <= 1
    
    def test_assess_geopolitical_events_empty(self):
        """Test assessment with no events"""
        result = SupplyChainService.assess_geopolitical_events(
            events=[],
            affected_suppliers=[]
        )
        
        assert result["total_events"] == 0
        assert result["avg_impact_score"] == 0
    
    def test_geopolitical_recommendation_levels(self):
        """Test recommendation levels based on impact"""
        # Critical impact
        rec_critical = SupplyChainService._get_geopolitical_recommendation(0.8)
        assert "CRITICAL" in rec_critical
        
        # High impact
        rec_high = SupplyChainService._get_geopolitical_recommendation(0.6)
        assert "HIGH" in rec_high
        
        # Medium impact
        rec_medium = SupplyChainService._get_geopolitical_recommendation(0.4)
        assert "MEDIUM" in rec_medium
        
        # Low impact
        rec_low = SupplyChainService._get_geopolitical_recommendation(0.2)
        assert "LOW" in rec_low


class TestSupplyChainServiceAlternatives:
    """Test suite for supplier alternative identification"""
    
    def test_identify_supplier_alternatives_basic(self):
        """Test basic alternative supplier identification"""
        primary = {"supplier_id": "PRIMARY_001"}
        
        alternatives = [
            {
                "supplier_id": "ALT_001",
                "supplier_name": "Alternative Supplier 1",
                "country": "Australia",
                "defect_rate_ppm": 150,
                "on_time_delivery_percent": 96,
                "concentration_percentage": 25,
                "lead_time_weeks": 8,
                "price_multiplier": 1.1
            },
            {
                "supplier_id": "ALT_002",
                "supplier_name": "Alternative Supplier 2",
                "country": "Chile",
                "defect_rate_ppm": 300,
                "on_time_delivery_percent": 90,
                "concentration_percentage": 40,
                "lead_time_weeks": 10,
                "price_multiplier": 1.2
            }
        ]
        
        result = SupplyChainService.identify_supplier_alternatives(
            primary_supplier=primary,
            material="Lithium",
            alternative_suppliers=alternatives
        )
        
        assert len(result) == 2
        # Should be sorted by suitability score (descending)
        assert result[0]["suitability_score"] >= result[1]["suitability_score"]
    
    def test_identify_supplier_alternatives_empty(self):
        """Test with no alternatives available"""
        result = SupplyChainService.identify_supplier_alternatives(
            primary_supplier={"supplier_id": "P1"},
            material="Cobalt",
            alternative_suppliers=[]
        )
        
        assert result == []
    
    def test_identify_supplier_alternatives_scoring(self):
        """Test that better suppliers get higher scores"""
        alternatives = [
            {
                "supplier_id": "GOOD",
                "supplier_name": "Good Supplier",
                "country": "Australia",
                "defect_rate_ppm": 100,  # Low defects
                "on_time_delivery_percent": 98,  # High on-time
                "concentration_percentage": 20,  # Low concentration
            },
            {
                "supplier_id": "POOR",
                "supplier_name": "Poor Supplier",
                "country": "China",
                "defect_rate_ppm": 500,  # High defects
                "on_time_delivery_percent": 85,  # Low on-time
                "concentration_percentage": 60,  # High concentration
            }
        ]
        
        result = SupplyChainService.identify_supplier_alternatives(
            primary_supplier={},
            material="Lithium",
            alternative_suppliers=alternatives
        )
        
        # Good supplier should rank higher
        good_supplier = next(s for s in result if s["supplier_id"] == "GOOD")
        poor_supplier = next(s for s in result if s["supplier_id"] == "POOR")
        
        assert good_supplier["suitability_score"] > poor_supplier["suitability_score"]


class TestSupplyChainServiceMaterialRisk:
    """Test suite for material sourcing risk assessment"""
    
    def test_calculate_material_sourcing_risk_basic(self):
        """Test basic material sourcing risk calculation"""
        suppliers = [
            {"risk_score": 0.7, "concentration_percentage": 45},
            {"risk_score": 0.5, "concentration_percentage": 30},
            {"risk_score": 0.4, "concentration_percentage": 25}
        ]
        
        result = SupplyChainService.calculate_material_sourcing_risk(
            material="Lithium",
            suppliers_data=suppliers
        )
        
        assert result["material"] == "Lithium"
        assert result["suppliers_count"] == 3
        assert "avg_risk_score" in result
        assert "herfindahl_index" in result
        assert "diversification_level" in result
    
    def test_calculate_material_sourcing_risk_empty(self):
        """Test with no suppliers"""
        result = SupplyChainService.calculate_material_sourcing_risk(
            material="Cobalt",
            suppliers_data=[]
        )
        
        assert result == {}
    
    def test_calculate_material_sourcing_risk_concentration(self):
        """Test concentration metrics calculation"""
        # Highly concentrated (single supplier dominates)
        concentrated = [
            {"risk_score": 0.5, "concentration_percentage": 80},
            {"risk_score": 0.3, "concentration_percentage": 15},
            {"risk_score": 0.2, "concentration_percentage": 5}
        ]
        
        # Well diversified
        diversified = [
            {"risk_score": 0.4, "concentration_percentage": 25},
            {"risk_score": 0.4, "concentration_percentage": 25},
            {"risk_score": 0.4, "concentration_percentage": 25},
            {"risk_score": 0.4, "concentration_percentage": 25}
        ]
        
        result_conc = SupplyChainService.calculate_material_sourcing_risk(
            material="Lithium",
            suppliers_data=concentrated
        )
        
        result_div = SupplyChainService.calculate_material_sourcing_risk(
            material="Lithium",
            suppliers_data=diversified
        )
        
        # Concentrated should have higher HHI
        assert result_conc["herfindahl_index"] > result_div["herfindahl_index"]
        assert result_conc["max_supplier_concentration"] == 80


class TestSupplyChainServiceRiskPropagation:
    """Test suite for supply chain risk propagation analysis"""
    
    def test_calculate_risk_propagation_basic(self):
        """Test basic risk propagation calculation"""
        suppliers = [
            {"risk_score": 0.7, "concentration_percentage": 40},
            {"risk_score": 0.5, "concentration_percentage": 35},
            {"risk_score": 0.4, "concentration_percentage": 25}
        ]
        
        result = SupplyChainService.calculate_supply_chain_risk_propagation(
            suppliers=suppliers,
            materials_graph={},
            max_depth=3
        )
        
        assert "tier_1_risk" in result
        assert "tier_2_risk" in result
        assert "tier_3_risk" in result
        assert "network_vulnerability_score" in result
        assert "network_resilience_score" in result
        assert "recommendation" in result
    
    def test_calculate_risk_propagation_decay(self):
        """Test that risk decays through tiers"""
        suppliers = [
            {"risk_score": 0.8, "concentration_percentage": 50},
            {"risk_score": 0.6, "concentration_percentage": 30},
        ]
        
        result = SupplyChainService.calculate_supply_chain_risk_propagation(
            suppliers=suppliers,
            materials_graph={},
            max_depth=3
        )
        
        # Tier 1 risk should be highest, decaying through tiers
        assert result["tier_1_risk"] >= result["tier_2_risk"]
        assert result["tier_2_risk"] >= result["tier_3_risk"]
    
    def test_calculate_risk_propagation_resilience(self):
        """Test resilience score calculation"""
        # High risk suppliers
        high_risk = [
            {"risk_score": 0.9, "concentration_percentage": 70},
        ]
        
        # Low risk suppliers
        low_risk = [
            {"risk_score": 0.2, "concentration_percentage": 20},
            {"risk_score": 0.2, "concentration_percentage": 20},
            {"risk_score": 0.2, "concentration_percentage": 20},
        ]
        
        result_high = SupplyChainService.calculate_supply_chain_risk_propagation(
            suppliers=high_risk,
            materials_graph={},
            max_depth=3
        )
        
        result_low = SupplyChainService.calculate_supply_chain_risk_propagation(
            suppliers=low_risk,
            materials_graph={},
            max_depth=3
        )
        
        # Low risk supply chain should have higher resilience
        assert result_low["network_resilience_score"] > result_high["network_resilience_score"]
    
    def test_calculate_risk_propagation_hhi(self):
        """Test Herfindahl-Hirschman Index calculation"""
        suppliers = [
            {"risk_score": 0.5, "concentration_percentage": 50},
            {"risk_score": 0.5, "concentration_percentage": 30},
            {"risk_score": 0.5, "concentration_percentage": 20}
        ]
        
        result = SupplyChainService.calculate_supply_chain_risk_propagation(
            suppliers=suppliers,
            materials_graph={},
            max_depth=3
        )
        
        # HHI should be between 0 and 1
        assert 0 <= result["herfindahl_hirschman_index"] <= 1


class TestSupplyChainServiceDiversification:
    """Test suite for diversification level classification"""
    
    def test_get_diversification_level_low(self):
        """Test low diversification classification"""
        level = SupplyChainService._get_diversification_level(0.75)
        assert "Low" in level
        assert "High concentration" in level
    
    def test_get_diversification_level_moderate(self):
        """Test moderate diversification classification"""
        level = SupplyChainService._get_diversification_level(0.45)
        assert "Moderate" in level
    
    def test_get_diversification_level_high(self):
        """Test high diversification classification"""
        level = SupplyChainService._get_diversification_level(0.20)
        assert "High" in level
        assert "diversified" in level.lower()


class TestSupplyChainServiceCountryRisks:
    """Test suite for country risk scores"""
    
    def test_country_risk_scores_valid(self):
        """Test that all country risk scores are in valid range"""
        for country, risk in SupplyChainService.COUNTRY_RISKS.items():
            assert 0 <= risk <= 1, f"Risk for {country} should be between 0 and 1"
    
    def test_country_risk_known_countries(self):
        """Test risk scores for known high-risk countries"""
        # China should be high risk due to geopolitical factors
        assert SupplyChainService.COUNTRY_RISKS["China"] > 0.5
        
        # DR Congo should be high risk due to political instability
        assert SupplyChainService.COUNTRY_RISKS["DR Congo"] > 0.5
        
        # Australia should be lower risk
        assert SupplyChainService.COUNTRY_RISKS["Australia"] < 0.5
        
        # Japan should be low risk
        assert SupplyChainService.COUNTRY_RISKS["Japan"] < 0.3
    
    def test_unknown_country_default_risk(self):
        """Test that unknown countries get a moderate default risk"""
        result = SupplyChainService.calculate_supplier_risk(
            supplier_data={"supplier_id": "TEST"},
            country="Unknown Country",
            material="Test",
            concentration_percent=30,
            quality_metrics={"delivery_risk": 0.3}
        )
        
        # Should use default risk of 0.5 for unknown countries
        assert 0.4 <= result["geopolitical_risk"] <= 0.6
