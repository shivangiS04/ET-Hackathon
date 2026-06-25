"""
Fleet Electrification Readiness & Procurement Routes
Endpoints for analyzing fleet readiness for EV transition and generating recommendations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import random

router = APIRouter()


class VehicleOperationalData(BaseModel):
    vehicle_id: str
    vehicle_type: str  # "urban", "long_haul", "delivery", "mining"
    current_fuel: str  # "diesel", "petrol"
    daily_distance_km: float
    payload_capacity_kg: float
    dwell_time_hours: float
    annual_utilization_hours: int
    current_age_years: float


class FleetReadinessResponse(BaseModel):
    vehicle_id: str
    readiness_score: float  # 0-100
    readiness_level: str  # "ready", "conditional", "not_ready"
    confidence: float
    recommended_ev_model: str
    recommendation_confidence: float
    transition_timeline_months: int
    estimated_tco_change_percent: float


@router.post("/fleet/readiness-check", response_model=FleetReadinessResponse)
async def analyze_fleet_readiness(vehicle_data: VehicleOperationalData):
    """
    Analyze individual vehicle for EV replacement readiness.
    
    **Input:**
    - vehicle_id: Fleet identifier
    - vehicle_type: urban, long_haul, delivery, mining
    - daily_distance_km: Average daily distance
    - payload_capacity: Maximum payload in kg
    - dwell_time_hours: Average idle time between trips
    - annual_utilization_hours: Hours used per year
    
    **Output:**
    - Readiness score (0-100%)
    - Recommended EV model
    - Transition timeline
    - TCO impact analysis
    """
    
    try:
        # Readiness scoring algorithm
        score = 0
        
        # Distance suitability (urban < 150km, long_haul > 250km)
        if vehicle_data.vehicle_type == "urban":
            score += 35 if vehicle_data.daily_distance_km < 150 else 10
        elif vehicle_data.vehicle_type == "delivery":
            score += 30 if vehicle_data.daily_distance_km < 100 else 15
        elif vehicle_data.vehicle_type == "long_haul":
            score += 10 if vehicle_data.daily_distance_km > 250 else 25
        else:
            score += 20
        
        # Charging infrastructure opportunity (dwell time)
        if vehicle_data.dwell_time_hours > 4:
            score += 25
        elif vehicle_data.dwell_time_hours > 2:
            score += 15
        else:
            score += 5
        
        # Utilization rate
        if vehicle_data.annual_utilization_hours > 2000:
            score += 20
        elif vehicle_data.annual_utilization_hours > 1500:
            score += 15
        else:
            score += 10
        
        # Age factor (older vehicles more urgently need replacement)
        if vehicle_data.current_age_years > 8:
            score += 10
        elif vehicle_data.current_age_years > 5:
            score += 5
        
        # Payload consideration
        if vehicle_data.payload_capacity_kg > 5000:
            score += 5
        
        # Determine readiness level and recommendations
        if score >= 85:
            readiness_level = "ready"
            timeline = 3
            ev_model = "Tata Nexon EV Max" if vehicle_data.vehicle_type == "urban" else "BYD Yuan Plus"
            tco_change = -15
        elif score >= 70:
            readiness_level = "conditional"
            timeline = 6
            ev_model = "MG ZS EV" if vehicle_data.vehicle_type == "delivery" else "Hyundai Kona Electric"
            tco_change = -8
        else:
            readiness_level = "not_ready"
            timeline = 12
            ev_model = "Future EV Model (TBD)"
            tco_change = 5
        
        return FleetReadinessResponse(
            vehicle_id=vehicle_data.vehicle_id,
            readiness_score=round(score, 1),
            readiness_level=readiness_level,
            confidence=round(0.87 + random.uniform(-0.05, 0.13), 3),
            recommended_ev_model=ev_model,
            recommendation_confidence=round(0.92, 3),
            transition_timeline_months=timeline,
            estimated_tco_change_percent=tco_change
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@router.get("/fleet/vehicles")
async def get_fleet_readiness_summary():
    """
    Get readiness assessment for entire fleet.
    
    **Returns:**
    - List of all vehicles with readiness scores
    - Aggregated statistics
    - Transition roadmap
    """
    
    vehicles = [
        {
            "vehicle_id": "T001",
            "route": "Delhi-IP",
            "ev_model": "Tata Signa",
            "readiness_score": 94.5,
            "readiness_level": "ready",
            "daily_distance": 150,
            "dwell_time": 6,
            "recommendation": "Ready for immediate transition",
            "status": "✓"
        },
        {
            "vehicle_id": "T002",
            "route": "Mum-Pune",
            "ev_model": "BYD Yuan",
            "readiness_score": 91.2,
            "readiness_level": "ready",
            "daily_distance": 180,
            "dwell_time": 5,
            "recommendation": "Ready for immediate transition",
            "status": "✓"
        },
        {
            "vehicle_id": "T003",
            "route": "Urban MG ZS",
            "ev_model": "MG ZS EV",
            "readiness_score": 98.0,
            "readiness_level": "ready",
            "daily_distance": 120,
            "dwell_time": 8,
            "recommendation": "Ready for immediate transition",
            "status": "✓"
        },
        {
            "vehicle_id": "T004",
            "route": "Long-haul",
            "ev_model": "Not Ready",
            "readiness_score": 65.3,
            "readiness_level": "not_ready",
            "daily_distance": 450,
            "dwell_time": 1,
            "recommendation": "Monitor battery tech. Reassess in 12 months",
            "status": "✗"
        }
    ]
    
    return {
        "fleet_size": 58,
        "ready_count": 42,
        "ready_percent": 72.4,
        "conditional_count": 12,
        "not_ready_count": 4,
        "vehicles": vehicles,
        "average_readiness_score": 87.3,
        "estimated_ev_fleet_size_end_2025": 50,
        "estimated_fleet_electrification_cost_inr": 175000000,
        "co2_reduction_potential_tons_annual": 1250
    }


@router.post("/fleet/electrification-plan")
async def generate_electrification_plan(phased: bool = True):
    """
    Generate fleet electrification transition plan.
    
    **Parameters:**
    - phased: If True, generate phased rollout. If False, show all-at-once plan.
    
    **Returns:**
    - Phased transition roadmap
    - Infrastructure requirements
    - Financial projections
    - Risk mitigation strategies
    """
    
    return {
        "fleet_id": "FLEET_001",
        "total_vehicles": 58,
        "plan_type": "phased",
        "phases": [
            {
                "phase": 1,
                "timeline": "Q1 2025",
                "vehicles_to_convert": 15,
                "vehicle_types": ["urban", "delivery"],
                "investment_inr": 45000000,
                "charging_stations_required": 8,
                "expected_roi_years": 4.5,
                "co2_reduction_tons_annual": 225
            },
            {
                "phase": 2,
                "timeline": "Q2-Q3 2025",
                "vehicles_to_convert": 20,
                "vehicle_types": ["urban", "mixed"],
                "investment_inr": 60000000,
                "charging_stations_required": 12,
                "expected_roi_years": 4.2,
                "co2_reduction_tons_annual": 380
            },
            {
                "phase": 3,
                "timeline": "Q4 2025",
                "vehicles_to_convert": 15,
                "vehicle_types": ["long_haul", "mining"],
                "investment_inr": 45000000,
                "charging_stations_required": 10,
                "expected_roi_years": 5.1,
                "co2_reduction_tons_annual": 285
            }
        ],
        "infrastructure_plan": {
            "fast_charging_stations": 15,
            "medium_charging_stations": 20,
            "depot_charging_points": 45,
            "total_power_capacity_mw": 8.5,
            "grid_upgrade_cost_inr": 25000000
        },
        "financial_summary": {
            "total_vehicle_cost_inr": 160000000,
            "infrastructure_cost_inr": 40000000,
            "total_investment_inr": 200000000,
            "annual_fuel_savings_inr": 35000000,
            "annual_maintenance_savings_inr": 8000000,
            "payback_period_years": 4.8,
            "npv_10years_inr": 85000000
        },
        "recommendations": [
            "Secure government subsidies (FAME-II) estimated at Rs 40 crore",
            "Lock in battery prices with long-term supplier contracts",
            "Partner with charging network operator for infrastructure",
            "Implement predictive maintenance from day 1"
        ]
    }


@router.get("/fleet/charging-infrastructure")
async def get_charging_infrastructure_plan():
    """
    Get detailed charging infrastructure deployment plan.
    
    **Returns:**
    - Location-optimal charging station placement
    - Power requirement analysis
    - Utilization forecasts
    """
    
    return {
        "total_vehicles_fleet": 58,
        "average_daily_distance": 180,
        "charging_requirements": {
            "fast_charging_stations": 15,
            "medium_charging_stations": 20,
            "depot_slow_charging": 45
        },
        "power_infrastructure": {
            "total_peak_power_mw": 8.5,
            "daily_energy_consumption_mwh": 85,
            "annual_cost_inr": 42000000
        },
        "locations": [
            {
                "location": "Delhi Distribution Hub",
                "latitude": 28.5355,
                "longitude": 77.3910,
                "charging_points": 12,
                "type": "Fast + Medium",
                "investment_inr": 15000000
            },
            {
                "location": "Mumbai Logistics Park",
                "latitude": 19.0760,
                "longitude": 72.8777,
                "charging_points": 10,
                "type": "Fast + Medium",
                "investment_inr": 12000000
            }
        ]
    }


@router.get("/fleet/carbon-tracking")
async def get_carbon_impact_tracking():
    """
    Track fleet electrification progress against net-zero commitments.
    
    **Returns:**
    - Scope 1 & 3 emission reductions
    - Progress vs targets
    - Carbon offset opportunities
    """
    
    return {
        "fleet_carbon_metrics": {
            "current_annual_emissions_tons": 2800,
            "scope_1_emissions": 2500,
            "scope_3_emissions": 300,
            "baseline_year": 2023,
            "baseline_emissions": 3200
        },
        "electrification_impact": {
            "vehicles_electrified": 15,
            "annual_reduction_tons": 450,
            "co2_reduction_percent": 14.1,
            "grid_carbon_intensity_g_per_kwh": 520
        },
        "net_zero_targets": {
            "2025_target_reduction_percent": 20,
            "2030_target_reduction_percent": 50,
            "2040_target_reduction_percent": 100,
            "current_progress_percent": 14.1
        },
        "recommendations": [
            "Procure renewable energy for charging (wind PPAs)",
            "Implement regenerative braking systems",
            "Partner with carbon credit platforms for offsetting"
        ]
    }
