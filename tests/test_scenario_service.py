"""
Test cases for Scenario Service
Tests what-if scenario simulation and impact analysis
"""

import pytest
from services.scenario_service import ScenarioService, ScenarioImpact


class TestScenarioServiceSimulation:
    """Test suite for scenario simulation"""
    
    def test_simulate_lithium_shortage(self):
        """Test lithium shortage scenario"""
        service = ScenarioService()
        
        result = service.simulate_scenario(
            scenario_id="lithium_shortage",
            parameters={"availability_reduction": 0.7, "duration_months": 6}
        )
        
        assert isinstance(result, ScenarioImpact)
        assert result.scenario_name == "Lithium Supply Shortage"
        assert result.severity > 0
        assert len(result.mitigation_steps) > 0
    
    def test_simulate_port_closure(self):
        """Test port closure scenario"""
        service = ScenarioService()
        
        result = service.simulate_scenario(
            scenario_id="port_closure",
            parameters={"shipping_delay_days": 30, "affected_ports": "Strait of Hormuz"}
        )
        
        assert isinstance(result, ScenarioImpact)
        assert "Port Closure" in result.scenario_name
        assert result.days_to_shortage > 0
    
    def test_simulate_price_shock(self):
        """Test price shock scenario"""
        service = ScenarioService()
        
        result = service.simulate_scenario(
            scenario_id="price_shock",
            parameters={"price_increase_percent": 25, "duration_months": 6}
        )
        
        assert isinstance(result, ScenarioImpact)
        assert "Price Shock" in result.scenario_name
        assert result.cost_impact_percent > 0
    
    def test_simulate_supplier_default(self):
        """Test supplier default scenario"""
        service = ScenarioService()
        
        result = service.simulate_scenario(
            scenario_id="supplier_default",
            parameters={"supplier_capacity_percent": 50, "recovery_months": 9}
        )
        
        assert isinstance(result, ScenarioImpact)
        assert "Supplier Default" in result.scenario_name or "Bankruptcy" in result.scenario_name
        assert result.severity > 0.5  # Should be critical
    
    def test_simulate_region_lockdown(self):
        """Test region lockdown scenario"""
        service = ScenarioService()
        
        result = service.simulate_scenario(
            scenario_id="region_lockdown",
            parameters={"affected_region": "North India", "duration_weeks": 8}
        )
        
        assert isinstance(result, ScenarioImpact)
        assert "Lockdown" in result.scenario_name
        assert result.affected_vehicles > 0
    
    def test_simulate_unknown_scenario(self):
        """Test unknown scenario type raises error"""
        service = ScenarioService()
        
        with pytest.raises(ValueError):
            service.simulate_scenario(
                scenario_id="unknown_scenario",
                parameters={}
            )


class TestScenarioServiceTemplates:
    """Test suite for scenario templates"""
    
    def test_get_scenario_templates(self):
        """Test getting scenario templates"""
        service = ScenarioService()
        
        templates = service.get_scenario_templates()
        
        assert isinstance(templates, list)
        assert len(templates) >= 5  # Should have 5 scenario types
        
        # Check template structure
        for template in templates:
            assert "id" in template
            assert "name" in template
            assert "description" in template
            assert "parameters" in template
    
    def test_scenario_template_ids(self):
        """Test that template IDs match scenario methods"""
        service = ScenarioService()
        
        templates = service.get_scenario_templates()
        template_ids = [t["id"] for t in templates]
        
        expected_ids = ["lithium_shortage", "port_closure", "price_shock", "supplier_default", "region_lockdown"]
        
        for expected_id in expected_ids:
            assert expected_id in template_ids


class TestScenarioServiceComparison:
    """Test suite for scenario comparison"""
    
    def test_compare_scenarios(self):
        """Test comparing multiple scenarios"""
        service = ScenarioService()
        
        result = service.compare_scenarios(
            scenario_ids=["lithium_shortage", "port_closure"],
            parameters={
                "lithium_shortage": {"availability_reduction": 0.5},
                "port_closure": {"shipping_delay_days": 30}
            }
        )
        
        assert "scenarios" in result
        assert "worst_case" in result
        assert "best_case" in result
        assert "average_severity" in result
        
        assert len(result["scenarios"]) == 2
    
    def test_compare_scenarios_sorted_by_severity(self):
        """Test that comparison results are sorted by severity"""
        service = ScenarioService()
        
        result = service.compare_scenarios(
            scenario_ids=["lithium_shortage", "price_shock", "supplier_default"],
            parameters={
                "lithium_shortage": {"availability_reduction": 0.9},
                "price_shock": {"price_increase_percent": 20},
                "supplier_default": {"supplier_capacity_percent": 80}
            }
        )
        
        scenarios = result["scenarios"]
        
        # Should be sorted by severity (descending)
        for i in range(len(scenarios) - 1):
            assert scenarios[i]["severity"] >= scenarios[i + 1]["severity"]


class TestScenarioServiceImpact:
    """Test suite for ScenarioImpact dataclass"""
    
    def test_scenario_impact_creation(self):
        """Test creating a ScenarioImpact instance"""
        impact = ScenarioImpact(
            scenario_name="Test Scenario",
            severity=0.75,
            days_to_shortage=45,
            cost_impact_percent=15.5,
            affected_vehicles=25,
            timeline_delay_months=3,
            mitigation_steps=["Step 1", "Step 2"],
            confidence_score=0.85
        )
        
        assert impact.scenario_name == "Test Scenario"
        assert impact.severity == 0.75
        assert impact.days_to_shortage == 45
        assert len(impact.mitigation_steps) == 2


class TestScenarioServiceMitigation:
    """Test suite for mitigation recommendations"""
    
    def test_mitigation_steps_provided(self):
        """Test that all scenarios provide mitigation steps"""
        service = ScenarioService()
        
        scenarios = ["lithium_shortage", "port_closure", "price_shock", "supplier_default", "region_lockdown"]
        
        for scenario_id in scenarios:
            result = service.simulate_scenario(scenario_id, {})
            
            assert len(result.mitigation_steps) > 0
            for step in result.mitigation_steps:
                assert isinstance(step, str)
                assert len(step) > 10  # Should be meaningful text
    
    def test_mitigation_steps_actionable(self):
        """Test that mitigation steps are actionable"""
        service = ScenarioService()
        
        result = service.simulate_scenario("lithium_shortage", {"availability_reduction": 0.5})
        
        # Mitigation steps should be specific and actionable
        for step in result.mitigation_steps:
            # Should contain action verbs
            action_words = ["evaluate", "negotiate", "increase", "accelerate", "explore", "establish", "source", "build"]
            assert any(word in step.lower() for word in action_words), f"Step should be actionable: {step}"


class TestScenarioServiceEdgeCases:
    """Test suite for edge cases"""
    
    def test_extreme_severity_values(self):
        """Test with extreme severity values"""
        service = ScenarioService()
        
        # Maximum severity
        result_max = service.simulate_scenario(
            "lithium_shortage",
            {"availability_reduction": 0.99, "duration_months": 24}
        )
        assert result_max.severity <= 1.0
        
        # Minimum severity
        result_min = service.simulate_scenario(
            "lithium_shortage",
            {"availability_reduction": 0.1, "duration_months": 1}
        )
        assert result_min.severity >= 0
    
    def test_zero_duration(self):
        """Test with zero duration"""
        service = ScenarioService()
        
        result = service.simulate_scenario(
            "price_shock",
            {"price_increase_percent": 25, "duration_months": 0}
        )
        
        # Should still produce valid result
        assert result is not None
    
    def test_empty_parameters(self):
        """Test with empty parameters (use defaults)"""
        service = ScenarioService()
        
        result = service.simulate_scenario("lithium_shortage", {})
        
        # Should use default parameters
        assert result is not None
        assert result.scenario_name is not None
    
    def test_confidence_score_range(self):
        """Test that confidence scores are in valid range"""
        service = ScenarioService()
        
        scenarios = ["lithium_shortage", "port_closure", "price_shock", "supplier_default", "region_lockdown"]
        
        for scenario_id in scenarios:
            result = service.simulate_scenario(scenario_id, {})
            
            assert 0 <= result.confidence_score <= 1.0
