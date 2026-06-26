"""
Scenario Simulation Engine for Supply Chain & Fleet Planning

Provides "what-if" analysis for various disruption scenarios:
- Lithium shortage
- Port closures
- Price shocks
- Supplier defaults
- Regional lockdowns
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import math


@dataclass
class ScenarioImpact:
    """Impact assessment for a scenario"""
    scenario_name: str
    severity: float  # 0-1 scale
    days_to_shortage: int
    cost_impact_percent: float
    affected_vehicles: int
    timeline_delay_months: int
    mitigation_steps: List[str]
    confidence_score: float


class ScenarioService:
    """Service for running supply chain disruption scenarios"""

    def __init__(self):
        self.scenarios = {
            "lithium_shortage": self._lithium_shortage_scenario,
            "port_closure": self._port_closure_scenario,
            "price_shock": self._price_shock_scenario,
            "supplier_default": self._supplier_default_scenario,
            "region_lockdown": self._region_lockdown_scenario,
        }

    def get_scenario_templates(self) -> List[Dict[str, Any]]:
        """Get list of available scenario templates"""
        return [
            {
                "id": "lithium_shortage",
                "name": "Lithium Supply Shortage",
                "description": "Reduction in lithium availability (e.g., China export restrictions)",
                "parameters": {
                    "availability_reduction": {"min": 0.1, "max": 0.9, "default": 0.5},
                    "duration_months": {"min": 1, "max": 24, "default": 6},
                },
                "impact_areas": ["Battery sourcing", "Electrification timeline", "Cost"],
                "severity": "HIGH",
            },
            {
                "id": "port_closure",
                "name": "Port Closure",
                "description": "Major shipping port unavailable (e.g., Strait of Hormuz)",
                "parameters": {
                    "shipping_delay_days": {"min": 5, "max": 60, "default": 30},
                    "affected_ports": {"options": ["Strait of Hormuz", "Suez Canal", "Singapore"], "default": "Strait of Hormuz"},
                },
                "impact_areas": ["Delivery timeline", "Cost escalation"],
                "severity": "MEDIUM",
            },
            {
                "id": "price_shock",
                "name": "Battery Price Shock",
                "description": "Sudden increase in battery component costs",
                "parameters": {
                    "price_increase_percent": {"min": 10, "max": 50, "default": 25},
                    "duration_months": {"min": 1, "max": 12, "default": 6},
                },
                "impact_areas": ["ROI", "Payback period", "Investment needed"],
                "severity": "MEDIUM",
            },
            {
                "id": "supplier_default",
                "name": "Supplier Default",
                "description": "Key battery supplier exits market or bankruptcy",
                "parameters": {
                    "supplier_capacity_percent": {"min": 20, "max": 80, "default": 50},
                    "recovery_months": {"min": 3, "max": 18, "default": 9},
                },
                "impact_areas": ["Supply continuity", "Cost escalation", "Timeline"],
                "severity": "CRITICAL",
            },
            {
                "id": "region_lockdown",
                "name": "Regional Lockdown",
                "description": "Manufacturing or logistics disruption in region",
                "parameters": {
                    "affected_region": {"options": ["North India", "South India", "East India", "West India"], "default": "North India"},
                    "duration_weeks": {"min": 2, "max": 16, "default": 8},
                },
                "impact_areas": ["Regional deployment", "Timeline"],
                "severity": "MEDIUM",
            },
        ]

    def simulate_scenario(self, scenario_id: str, parameters: Dict[str, float]) -> ScenarioImpact:
        """Run a specific scenario simulation"""
        if scenario_id not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_id}")

        scenario_func = self.scenarios[scenario_id]
        return scenario_func(parameters)

    def _lithium_shortage_scenario(self, params: Dict[str, float]) -> ScenarioImpact:
        """Model lithium shortage impact"""
        availability_reduction = params.get("availability_reduction", 0.5)
        duration_months = int(params.get("duration_months", 6))

        # Base fleet: 58 vehicles, need 200 batteries/year
        annual_demand = 58 * 3.5  # ~200 batteries/year for full fleet
        reduced_availability = annual_demand * (1 - availability_reduction)
        monthly_shortage = (annual_demand - reduced_availability) / 12

        # Calculate days to shortage at current procurement rate
        current_monthly_rate = annual_demand / 12
        months_until_shortage = reduced_availability / current_monthly_rate if current_monthly_rate > 0 else 0
        days_to_shortage = max(7, int(months_until_shortage * 30))

        # Cost impact: lithium is ~15% of battery cost, which is ~40% of vehicle cost
        cost_per_vehicle = 15_00_000  # ₹15L typical EV
        lithium_percent = 0.15 * 0.40  # 6% of vehicle cost
        cost_impact = lithium_percent * availability_reduction * 100

        # Affected vehicles: based on procurement rate vs demand
        affected_vehicles = int(58 * (availability_reduction / 2))

        # Timeline delay: months until alternate sourcing found
        timeline_delay = max(1, int(duration_months * availability_reduction / 2))

        mitigation_steps = [
            "Diversify lithium sourcing: Evaluate Argentina, Australia, Chile suppliers",
            "Negotiate long-term contracts with tier-1 suppliers before shortage",
            "Increase battery inventory buffer to 3-month supply",
            "Accelerate LFP chemistry adoption (less lithium intensive)",
            "Explore recycling partnerships to recover lithium from old batteries",
        ]

        confidence = max(0.7, 1.0 - (availability_reduction * 0.2))

        return ScenarioImpact(
            scenario_name="Lithium Supply Shortage",
            severity=min(1.0, availability_reduction),
            days_to_shortage=days_to_shortage,
            cost_impact_percent=cost_impact,
            affected_vehicles=affected_vehicles,
            timeline_delay_months=timeline_delay,
            mitigation_steps=mitigation_steps,
            confidence_score=confidence,
        )

    def _port_closure_scenario(self, params: Dict[str, float]) -> ScenarioImpact:
        """Model port closure impact on delivery timeline"""
        shipping_delay_days = int(params.get("shipping_delay_days", 30))
        affected_ports = params.get("affected_ports", "Strait of Hormuz")

        # Current: 30-45 days shipping from China to India
        base_shipping_time = 35
        total_delivery_time = base_shipping_time + shipping_delay_days

        # Alternative route: longer + more expensive
        alternative_premium = (shipping_delay_days / 30) * 0.15  # 15% premium per month of delay

        # Affected vehicles: 40% of supply chain uses affected port
        affected_vehicles = int(58 * 0.4)

        # Timeline impact in electrification plan (assume Q1 plans rely on these shipments)
        timeline_delay = max(1, shipping_delay_days // 30)

        mitigation_steps = [
            f"Source alternative suppliers not dependent on {affected_ports}",
            "Negotiate air freight for critical components (premium ~40%)",
            "Increase local supplier qualification and sourcing",
            "Establish strategic inventory (2-month buffer)",
            "Explore alternative shipping routes (e.g., via Middle East)",
        ]

        severity = min(1.0, shipping_delay_days / 60)
        confidence = 0.85

        return ScenarioImpact(
            scenario_name="Port Closure Disruption",
            severity=severity,
            days_to_shortage=shipping_delay_days,
            cost_impact_percent=alternative_premium * 100,
            affected_vehicles=affected_vehicles,
            timeline_delay_months=timeline_delay,
            mitigation_steps=mitigation_steps,
            confidence_score=confidence,
        )

    def _price_shock_scenario(self, params: Dict[str, float]) -> ScenarioImpact:
        """Model battery price shock impact"""
        price_increase_percent = params.get("price_increase_percent", 25)
        duration_months = int(params.get("duration_months", 6))

        # Vehicle cost breakdown: 40% battery (~₹6L), 60% vehicle (₹9L), total ₹15L
        base_battery_cost = 6_00_000
        increased_battery_cost = base_battery_cost * (1 + price_increase_percent / 100)
        cost_increase_per_vehicle = increased_battery_cost - base_battery_cost

        # Fleet electrification: 58 vehicles * ₹15L/vehicle = ₹87 Cr budget
        fleet_cost_increase = (58 * cost_increase_per_vehicle) / 1_00_00_000  # in Crores

        # Impact on ROI: assume 8-year payback, ₹5L annual fuel savings
        annual_savings = 5_00_000
        original_payback = 8
        new_investment = 15_00_000 * (1 + price_increase_percent / 100)
        new_payback = new_investment / annual_savings / 100_000  # in years
        payback_delay = new_payback - original_payback

        # All vehicles affected
        affected_vehicles = 58

        mitigation_steps = [
            f"Lock in fixed-price contracts NOW before {price_increase_percent}% increase",
            "Evaluate battery chemistry trade-offs (LFP vs NCA)",
            "Negotiate volume discounts for full fleet commitment",
            "Explore battery leasing vs ownership models",
            "Accelerate timeline to lock in current prices",
        ]

        severity = min(1.0, price_increase_percent / 100)
        confidence = 0.92

        return ScenarioImpact(
            scenario_name="Battery Price Shock",
            severity=severity,
            days_to_shortage=duration_months * 30,
            cost_impact_percent=price_increase_percent,
            affected_vehicles=affected_vehicles,
            timeline_delay_months=int(payback_delay * 12),  # delay in achieving ROI
            mitigation_steps=mitigation_steps,
            confidence_score=confidence,
        )

    def _supplier_default_scenario(self, params: Dict[str, float]) -> ScenarioImpact:
        """Model supplier bankruptcy or exit"""
        supplier_capacity_percent = params.get("supplier_capacity_percent", 50)
        recovery_months = int(params.get("recovery_months", 9))

        # Assume supplier provided 40% of batteries
        lost_capacity = 0.4 * (supplier_capacity_percent / 100)

        # Monthly demand: 58 vehicles * 3.5 batteries/year / 12 = 16.9 batteries/month
        monthly_demand = 16.9
        monthly_shortage = monthly_demand * lost_capacity

        # Time to stabilize on alternate suppliers
        days_to_shortage = 14  # Quick hit when supplier exits
        timeline_delay = recovery_months

        # Cost impact: rush orders + qualification of new suppliers
        cost_premium = (supplier_capacity_percent / 100) * 0.35  # 35% premium for emergency sourcing

        # Affected vehicles:battery shortage will affect procurement for X months
        affected_vehicles = int((monthly_shortage * recovery_months) / 3.5)  # 3.5 batteries/vehicle

        mitigation_steps = [
            f"Pre-qualify {recovery_months}-month supplier backup before relying on current vendor",
            "Reduce supplier concentration: avoid >25% dependence on single supplier",
            "Establish escrow agreements for critical components",
            "Build strategic inventory (6-month buffer for critical suppliers)",
            "Negotiate dual-source requirements in supply contracts",
        ]

        severity = 0.95  # CRITICAL
        confidence = 0.88

        return ScenarioImpact(
            scenario_name="Supplier Default/Bankruptcy",
            severity=severity,
            days_to_shortage=days_to_shortage,
            cost_impact_percent=cost_premium * 100,
            affected_vehicles=affected_vehicles,
            timeline_delay_months=timeline_delay,
            mitigation_steps=mitigation_steps,
            confidence_score=confidence,
        )

    def _region_lockdown_scenario(self, params: Dict[str, float]) -> ScenarioImpact:
        """Model regional lockdown impact"""
        affected_region = params.get("affected_region", "North India")
        duration_weeks = int(params.get("duration_weeks", 8))

        # Assume region has 25% of fleet
        regional_vehicles = int(58 * 0.25)

        # Service disruption
        days_to_impact = 3  # Quick impact
        timeline_delay = duration_weeks // 4  # weeks to months

        # No direct cost, but lost productivity
        cost_impact = 0  # Sunk cost, not incremental

        mitigation_steps = [
            f"Pre-position spare batteries and components in {affected_region}",
            "Establish mobile maintenance units outside affected region",
            "Cross-train technicians in adjacent regions",
            "Maintain 2-week inventory buffer for regional spares",
            "Establish remote diagnostics capability for vehicles",
        ]

        severity = 0.4  # MEDIUM
        confidence = 0.75  # Localized impact, less predictable

        return ScenarioImpact(
            scenario_name=f"Regional Lockdown: {affected_region}",
            severity=severity,
            days_to_shortage=days_to_impact,
            cost_impact_percent=cost_impact,
            affected_vehicles=regional_vehicles,
            timeline_delay_months=timeline_delay,
            mitigation_steps=mitigation_steps,
            confidence_score=confidence,
        )

    def compare_scenarios(self, scenario_ids: List[str], parameters: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Compare multiple scenarios side-by-side"""
        results = []

        for scenario_id in scenario_ids:
            params = parameters.get(scenario_id, {})
            impact = self.simulate_scenario(scenario_id, params)
            results.append({
                "scenario_id": scenario_id,
                "scenario_name": impact.scenario_name,
                "severity": impact.severity,
                "days_to_shortage": impact.days_to_shortage,
                "cost_impact_percent": impact.cost_impact_percent,
                "affected_vehicles": impact.affected_vehicles,
                "timeline_delay_months": impact.timeline_delay_months,
            })

        # Sort by severity
        results.sort(key=lambda x: x["severity"], reverse=True)

        return {
            "scenarios": results,
            "worst_case": results[0] if results else None,
            "best_case": results[-1] if results else None,
            "average_severity": sum(r["severity"] for r in results) / len(results) if results else 0,
        }
