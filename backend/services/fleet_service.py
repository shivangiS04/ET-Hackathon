"""
Fleet Service Layer
Business logic for EV fleet readiness assessment and transition planning
"""

from typing import List, Dict, Tuple
from enum import Enum


class VehicleType(str, Enum):
    """Vehicle type classifications"""
    URBAN = "urban"
    DELIVERY = "delivery"
    LONG_HAUL = "long_haul"
    MINING = "mining"
    CONSTRUCTION = "construction"


class FleetService:
    """Service for EV fleet electrification readiness and planning"""
    
    # EV readiness thresholds
    READINESS_THRESHOLDS = {
        "ready": 85,
        "conditional": 70,
        "not_ready": 0
    }
    
    # Vehicle type optimal EV models
    EV_RECOMMENDATIONS = {
        "urban": {
            "models": ["Tata Nexon EV Max", "MG ZS EV", "Hyundai Kona"],
            "range_km": [450, 460, 470],
            "battery_kwh": [71.7, 70, 65],
            "price_range_inr": [13, 15, 16]  # in lakhs
        },
        "delivery": {
            "models": ["BYD Yuan", "SAIC MG eDeliver", "Tata Nexon"],
            "range_km": [405, 400, 420],
            "battery_kwh": [60, 55, 65],
            "price_range_inr": [12, 14, 15]
        },
        "long_haul": {
            "models": ["BYD Yuan Plus", "Nio ET7", "Xpeng G9"],
            "range_km": [600, 650, 580],
            "battery_kwh": [100, 101, 101],
            "price_range_inr": [25, 30, 28]
        },
        "mining": {
            "models": ["Volvo FM Electric", "Nikola Two", "Daimler eSprinter"],
            "range_km": [300, 500, 350],
            "battery_kwh": [150, 200, 110],
            "price_range_inr": [50, 60, 45]
        }
    }
    
    @staticmethod
    def calculate_readiness_score(
        vehicle_type: str,
        daily_distance_km: float,
        dwell_time_hours: float,
        payload_capacity_kg: float,
        annual_utilization_hours: int,
        current_age_years: float,
    ) -> Dict:
        """
        Calculate EV readiness score for a vehicle using weighted criteria.
        
        Scoring breakdown:
        - Distance suitability: 35%
        - Charging opportunity: 25%
        - Utilization rate: 20%
        - Vehicle age: 10%
        - Payload: 5%
        - Other factors: 5%
        """
        
        score = 0
        max_score = 100
        
        # 1. Distance suitability (35 points)
        distance_score = FleetService._score_distance(vehicle_type, daily_distance_km)
        score += distance_score * 0.35
        
        # 2. Charging opportunity (25 points)
        charging_score = FleetService._score_charging(dwell_time_hours)
        score += charging_score * 0.25
        
        # 3. Utilization rate (20 points)
        utilization_score = FleetService._score_utilization(annual_utilization_hours)
        score += utilization_score * 0.20
        
        # 4. Vehicle age (10 points)
        age_score = FleetService._score_vehicle_age(current_age_years)
        score += age_score * 0.10
        
        # 5. Payload capacity (5 points)
        payload_score = FleetService._score_payload(payload_capacity_kg)
        score += payload_score * 0.05
        
        # 6. Operational flexibility (5 points)
        flexibility_score = FleetService._score_flexibility(vehicle_type)
        score += flexibility_score * 0.05
        
        # Determine readiness level
        if score >= 85:
            readiness_level = "ready"
            recommendation = "Ready for immediate EV transition"
        elif score >= 70:
            readiness_level = "conditional"
            recommendation = "Conditional readiness - needs 6-12 month planning"
        else:
            readiness_level = "not_ready"
            recommendation = "Monitor battery technology advancement - reassess in 12 months"
        
        return {
            "readiness_score": round(score, 1),
            "readiness_level": readiness_level,
            "component_scores": {
                "distance_suitability": round(distance_score, 1),
                "charging_opportunity": round(charging_score, 1),
                "utilization_rate": round(utilization_score, 1),
                "vehicle_age": round(age_score, 1),
                "payload_capacity": round(payload_score, 1),
                "operational_flexibility": round(flexibility_score, 1),
            },
            "recommendation": recommendation,
            "confidence": round(0.85 + (score / max_score) * 0.15, 3)
        }
    
    @staticmethod
    def _score_distance(vehicle_type: str, daily_distance: float) -> float:
        """Score vehicle suitability based on daily distance"""
        thresholds = {
            "urban": {"optimal": 100, "acceptable": 150},
            "delivery": {"optimal": 80, "acceptable": 120},
            "long_haul": {"optimal": 300, "acceptable": 400},
            "mining": {"optimal": 50, "acceptable": 100},
        }
        
        threshold = thresholds.get(vehicle_type, {"optimal": 150, "acceptable": 250})
        
        if daily_distance <= threshold["optimal"]:
            return 100
        elif daily_distance <= threshold["acceptable"]:
            return 75
        elif daily_distance <= threshold["acceptable"] * 1.5:
            return 40
        else:
            return 10
    
    @staticmethod
    def _score_charging(dwell_time_hours: float) -> float:
        """Score based on available charging time (dwell time)"""
        if dwell_time_hours >= 8:
            return 100  # Fast charging possible
        elif dwell_time_hours >= 4:
            return 80   # Medium charging possible
        elif dwell_time_hours >= 2:
            return 50   # Slow charging only
        else:
            return 20   # Limited charging opportunity
    
    @staticmethod
    def _score_utilization(annual_hours: int) -> float:
        """Score based on annual utilization"""
        if annual_hours >= 2500:
            return 100  # Highly utilized (better ROI)
        elif annual_hours >= 2000:
            return 85
        elif annual_hours >= 1500:
            return 65
        else:
            return 40   # Low utilization (poor ROI)
    
    @staticmethod
    def _score_vehicle_age(age_years: float) -> float:
        """Score based on vehicle age (older = higher urgency to replace)"""
        if age_years >= 8:
            return 100  # Very old - urgent replacement
        elif age_years >= 5:
            return 75
        elif age_years >= 3:
            return 50
        else:
            return 30   # New - can wait for better EV options
    
    @staticmethod
    def _score_payload(payload_kg: float) -> float:
        """Score based on payload capacity"""
        if payload_kg >= 8000:
            return 100
        elif payload_kg >= 5000:
            return 85
        else:
            return 60
    
    @staticmethod
    def _score_flexibility(vehicle_type: str) -> float:
        """Score operational flexibility"""
        if vehicle_type == "urban":
            return 100
        elif vehicle_type == "delivery":
            return 90
        elif vehicle_type == "long_haul":
            return 40
        else:
            return 30
    
    @staticmethod
    def recommend_ev_model(vehicle_type: str, readiness_score: float) -> Dict:
        """Recommend optimal EV model for vehicle type"""
        
        recommendations = FleetService.EV_RECOMMENDATIONS.get(vehicle_type, {})
        
        if not recommendations:
            return {}
        
        models = recommendations.get("models", [])
        recommended_model = models[0] if models else "TBD"
        
        return {
            "primary_recommendation": recommended_model,
            "alternative_models": models[1:],
            "estimated_battery_kwh": recommendations.get("battery_kwh", [70])[0],
            "estimated_range_km": recommendations.get("range_km", [400])[0],
            "estimated_price_lakhs_inr": recommendations.get("price_range_inr", [15])[0],
            "confidence_score": round(0.85 + (readiness_score / 100) * 0.15, 3),
        }
    
    @staticmethod
    def generate_transition_plan(
        fleet_size: int,
        vehicles_by_readiness: Dict[str, int],
        available_budget_inr: float
    ) -> Dict:
        """
        Generate phased EV transition roadmap.
        
        Args:
            fleet_size: Total number of vehicles
            vehicles_by_readiness: Count by readiness level
            available_budget_inr: Total budget for transition
        
        Returns:
            Phased transition plan
        """
        
        ready = vehicles_by_readiness.get("ready", 0)
        conditional = vehicles_by_readiness.get("conditional", 0)
        not_ready = vehicles_by_readiness.get("not_ready", 0)
        
        avg_ev_price = 15_00_000  # ₹15 lakhs average
        cost_per_vehicle = avg_ev_price
        
        total_capacity = available_budget_inr / cost_per_vehicle
        
        phases = []
        
        # Phase 1: Ready vehicles (immediate)
        phase1_count = min(ready, int(total_capacity * 0.4))
        phases.append({
            "phase": 1,
            "timeline": "Q1-Q2",
            "vehicles": phase1_count,
            "investment_inr": phase1_count * cost_per_vehicle,
            "priority": "High readiness vehicles",
        })
        
        # Phase 2: Conditional + remaining ready
        remaining_capacity = total_capacity - phase1_count
        phase2_count = min(conditional + (ready - phase1_count), int(remaining_capacity * 0.5))
        phases.append({
            "phase": 2,
            "timeline": "Q3-Q4",
            "vehicles": phase2_count,
            "investment_inr": phase2_count * cost_per_vehicle,
            "priority": "Mixed readiness vehicles",
        })
        
        # Phase 3: Remaining
        phase3_count = min(not_ready, int(remaining_capacity * 0.1))
        phases.append({
            "phase": 3,
            "timeline": "2026",
            "vehicles": phase3_count,
            "investment_inr": phase3_count * cost_per_vehicle,
            "priority": "Future technology watch",
        })
        
        total_transitioned = sum(p["vehicles"] for p in phases)
        
        return {
            "phases": phases,
            "total_vehicles_phase1": phase1_count,
            "total_vehicles_phase2": phase2_count,
            "total_vehicles_phase3": phase3_count,
            "total_vehicles_transitioned": total_transitioned,
            "transition_percentage": round((total_transitioned / fleet_size) * 100, 1),
            "total_investment_required_inr": sum(p["investment_inr"] for p in phases),
            "annual_roi": round(available_budget_inr * 0.15, 0),  # Assume 15% annual ROI
        }
    
    @staticmethod
    def calculate_carbon_reduction(
        fleet_size: int,
        transitioned_count: int,
        annual_distance_per_vehicle: float = 50_000  # km
    ) -> Dict:
        """Calculate carbon reduction from EV transition"""
        
        # Diesel: ~2.3 kg CO2 per liter, ~6 km/liter = 0.38 kg CO2/km
        diesel_emissions_per_km = 0.38
        # EV (Grid avg): ~0.12 kg CO2/km (India's grid mix)
        ev_emissions_per_km = 0.12
        
        reduction_per_vehicle = (diesel_emissions_per_km - ev_emissions_per_km) * annual_distance_per_vehicle
        
        return {
            "transitioned_vehicles": transitioned_count,
            "remaining_diesel": fleet_size - transitioned_count,
            "co2_reduction_per_vehicle_annual_kg": round(reduction_per_vehicle, 0),
            "total_co2_reduction_annual_kg": round(reduction_per_vehicle * transitioned_count, 0),
            "total_co2_reduction_annual_tons": round((reduction_per_vehicle * transitioned_count) / 1000, 1),
            "equivalent_trees_needed_to_offset": round((reduction_per_vehicle * transitioned_count) / 20, 0),
        }
    
    @staticmethod
    def calculate_total_cost_of_ownership(
        vehicle_type: str,
        annual_distance: float,
        years_horizon: int = 8,
        diesel_price_per_liter: float = 90,
        electricity_price_per_kwh: float = 8.5
    ) -> Dict:
        """
        Calculate Total Cost of Ownership (TCO) comparison: EV vs Diesel
        
        Includes:
        - Purchase price
        - Fuel costs
        - Maintenance costs
        - Battery replacement (EV specific)
        - Salvage value
        - Road tax and insurance
        """
        
        # Vehicle specifications by type
        vehicle_specs = {
            "urban": {
                "diesel_price": 15_00_000,  # ₹15 lakhs
                "ev_price": 16_00_000,      # ₹16 lakhs
                "diesel_efficiency": 6,      # km/liter
                "ev_efficiency": 5,          # km/kwh
                "diesel_maintenance_annual": 15_000,
                "ev_maintenance_annual": 8_000,
            },
            "delivery": {
                "diesel_price": 18_00_000,
                "ev_price": 20_00_000,
                "diesel_efficiency": 5,
                "ev_efficiency": 4.5,
                "diesel_maintenance_annual": 20_000,
                "ev_maintenance_annual": 10_000,
            },
            "long_haul": {
                "diesel_price": 35_00_000,
                "ev_price": 45_00_000,
                "diesel_efficiency": 4,
                "ev_efficiency": 3.5,
                "diesel_maintenance_annual": 30_000,
                "ev_maintenance_annual": 15_000,
            }
        }
        
        specs = vehicle_specs.get(vehicle_type, vehicle_specs["urban"])
        
        # Diesel TCO calculation
        diesel_fuel_cost = (annual_distance / specs["diesel_efficiency"]) * diesel_price_per_liter * years_horizon
        diesel_maintenance = specs["diesel_maintenance_annual"] * years_horizon
        diesel_road_tax = 5_000 * years_horizon
        diesel_insurance = 8_000 * years_horizon
        diesel_salvage = specs["diesel_price"] * 0.25  # 25% salvage value
        
        diesel_tco = (
            specs["diesel_price"] +
            diesel_fuel_cost +
            diesel_maintenance +
            diesel_road_tax +
            diesel_insurance -
            diesel_salvage
        )
        
        # EV TCO calculation
        ev_fuel_cost = (annual_distance / specs["ev_efficiency"]) * electricity_price_per_kwh * years_horizon
        ev_maintenance = specs["ev_maintenance_annual"] * years_horizon
        ev_road_tax = 2_000 * years_horizon  # Lower tax for EVs
        ev_insurance = 6_000 * years_horizon
        ev_battery_replacement = 3_00_000 if years_horizon > 6 else 0  # Battery after 6 years
        ev_salvage = specs["ev_price"] * 0.30  # 30% salvage value
        ev_subsidy = min(3_00_000, specs["ev_price"] * 0.15)  # ~15% FAME subsidy
        
        ev_tco = (
            specs["ev_price"] +
            ev_fuel_cost +
            ev_maintenance +
            ev_road_tax +
            ev_insurance +
            ev_battery_replacement -
            ev_salvage -
            ev_subsidy
        )
        
        # TCO comparison
        tco_difference = diesel_tco - ev_tco
        roi_percent = (tco_difference / diesel_tco) * 100
        
        # Payback period calculation
        annual_saving = (diesel_fuel_cost - ev_fuel_cost) / years_horizon + \
                       (diesel_maintenance - ev_maintenance) / years_horizon + \
                       (diesel_road_tax - ev_road_tax) / years_horizon + \
                       (diesel_insurance - ev_insurance) / years_horizon
        
        price_difference = specs["ev_price"] - specs["diesel_price"] + ev_subsidy
        
        if annual_saving > 0:
            payback_years = min(years_horizon, price_difference / annual_saving)
        else:
            payback_years = years_horizon
        
        return {
            "vehicle_type": vehicle_type,
            "analysis_period_years": years_horizon,
            "annual_distance_km": annual_distance,
            "diesel_tco": {
                "purchase_price": specs["diesel_price"],
                "fuel_cost": round(diesel_fuel_cost, 0),
                "maintenance_cost": round(diesel_maintenance, 0),
                "road_tax": round(diesel_road_tax, 0),
                "insurance": round(diesel_insurance, 0),
                "salvage_value": round(diesel_salvage, 0),
                "total_tco": round(diesel_tco, 0)
            },
            "ev_tco": {
                "purchase_price": specs["ev_price"],
                "fuel_cost": round(ev_fuel_cost, 0),
                "maintenance_cost": round(ev_maintenance, 0),
                "road_tax": round(ev_road_tax, 0),
                "insurance": round(ev_insurance, 0),
                "battery_replacement": round(ev_battery_replacement, 0),
                "salvage_value": round(ev_salvage, 0),
                "subsidy": round(ev_subsidy, 0),
                "total_tco": round(ev_tco, 0)
            },
            "tco_advantage": {
                "absolute_savings": round(tco_difference, 0),
                "percentage_saving": round(roi_percent, 1),
                "payback_period_years": round(payback_years, 1),
                "recommendation": "Switch to EV" if roi_percent > 10 else "Monitor EV costs" if roi_percent > 0 else "Stick with Diesel"
            }
        }
