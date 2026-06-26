"""
Advanced Analytics Service for EV Supply Chain Platform
Provides comprehensive analytics, trending analysis, and predictive insights
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import math
import random


class TimeGranularity(str, Enum):
    """Time granularity for analytics"""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class AnalyticsService:
    """Service for advanced analytics and insights"""
    
    def __init__(self):
        self.metrics_history = {}
        self.anomaly_log = []
        self.event_log = []
    
    def get_battery_health_trends(
        self,
        vehicle_ids: Optional[List[str]] = None,
        granularity: TimeGranularity = TimeGranularity.DAILY,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get battery health trends over time"""
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Generate synthetic trend data
        trend_points = []
        current_date = start_date
        interval = self._get_interval(granularity)
        
        while current_date <= end_date:
            soh = 92.5 - (random.random() * 2)  # Slight degradation with noise
            trend_points.append({
                "timestamp": current_date.isoformat(),
                "average_soh": round(soh, 1),
                "min_soh": round(soh - 5, 1),
                "max_soh": round(soh + 2, 1),
                "vehicles_monitored": 156,
                "anomalies_detected": random.randint(0, 3)
            })
            current_date += interval
        
        return {
            "period": f"Last {days} days",
            "granularity": granularity,
            "trend_points": trend_points,
            "summary": {
                "average_soh": round(sum(p["average_soh"] for p in trend_points) / len(trend_points), 1),
                "trend": "stable_with_slight_degradation",
                "forecast_90d_soh": round(92.5 - (random.random() * 3), 1)
            }
        }
    
    def get_fleet_composition_analytics(self) -> Dict[str, Any]:
        """Get detailed fleet composition analytics"""
        
        return {
            "total_vehicles": 156,
            "by_status": {
                "operational": 148,
                "under_maintenance": 5,
                "in_transition": 3
            },
            "by_model": {
                "tata_nexon": 45,
                "mahindra_xuv500": 38,
                "byd_song_plus": 32,
                "mg_zs_ev": 28,
                "other": 13
            },
            "by_region": {
                "north": 52,
                "south": 38,
                "east": 31,
                "west": 35
            },
            "by_age_group": {
                "0_2_years": 31,
                "2_4_years": 58,
                "4_6_years": 45,
                "6_plus_years": 22
            },
            "utilization": {
                "high_utilization": 89,
                "medium_utilization": 52,
                "low_utilization": 15
            },
            "readiness_distribution": {
                "ready_for_ev": 87,
                "suitable_with_infrastructure": 47,
                "not_suitable": 22
            }
        }
    
    def get_supply_chain_analytics(self) -> Dict[str, Any]:
        """Get supply chain concentration and risk analytics"""
        
        return {
            "total_active_suppliers": 28,
            "material_breakdown": {
                "lithium": {
                    "suppliers": 8,
                    "concentration_ratio_hhi": 2847,
                    "risk_level": "high",
                    "top_supplier_share": 38,
                    "price_volatility_percent": 12.5,
                    "lead_time_days": 45,
                    "inventory_days": 28
                },
                "cobalt": {
                    "suppliers": 6,
                    "concentration_ratio_hhi": 3124,
                    "risk_level": "high",
                    "top_supplier_share": 42,
                    "price_volatility_percent": 8.3,
                    "lead_time_days": 60,
                    "inventory_days": 35
                },
                "nickel": {
                    "suppliers": 7,
                    "concentration_ratio_hhi": 2156,
                    "risk_level": "moderate",
                    "top_supplier_share": 28,
                    "price_volatility_percent": 5.2,
                    "lead_time_days": 45,
                    "inventory_days": 42
                },
                "manganese": {
                    "suppliers": 5,
                    "concentration_ratio_hhi": 2654,
                    "risk_level": "moderate",
                    "top_supplier_share": 35,
                    "price_volatility_percent": 3.8,
                    "lead_time_days": 35,
                    "inventory_days": 50
                }
            },
            "geographic_concentration": {
                "china": 0.45,
                "australia": 0.20,
                "chile": 0.15,
                "drc": 0.12,
                "other": 0.08
            },
            "risk_events_90d": 3,
            "price_trend": "upward_8_percent",
            "supply_chain_health_score": 62
        }
    
    def get_maintenance_analytics(self) -> Dict[str, Any]:
        """Get maintenance cost and schedule analytics"""
        
        return {
            "scheduled_maintenance": {
                "total_due": 12,
                "overdue": 2,
                "upcoming_7d": 5,
                "upcoming_30d": 12
            },
            "unscheduled_repairs": {
                "total_active": 3,
                "critical": 0,
                "high_priority": 1,
                "medium_priority": 2
            },
            "cost_analysis": {
                "ytd_maintenance_cost_crores": 2.81,
                "avg_cost_per_vehicle_lakh": 1.8,
                "breakdown": {
                    "labor": 0.35,
                    "parts": 0.85,
                    "diagnostics": 0.25,
                    "other": 0.35
                },
                "projected_annual_cost_crores": 3.2,
                "maintenance_cost_per_km": 0.75
            },
            "equipment_health": {
                "critical_failures": 0,
                "components_above_wear_threshold": 8,
                "predicted_failures_30d": 2,
                "maintenance_efficiency_score": 87
            }
        }
    
    def get_roi_analytics(self, vehicles_to_transition: int = 50) -> Dict[str, Any]:
        """Get ROI analysis for EV transition"""
        
        ev_unit_cost = 35  # lakhs
        diesel_vehicle_age = 5.2
        remaining_diesel_life = 10 - diesel_vehicle_age  # years
        
        current_annual_diesel_cost = 6.0  # lakhs per vehicle
        ev_annual_cost = 2.8  # lakhs per vehicle
        annual_savings_per_vehicle = current_annual_diesel_cost - ev_annual_cost
        
        total_investment = vehicles_to_transition * ev_unit_cost  # crores
        annual_savings = (vehicles_to_transition * annual_savings_per_vehicle) / 10  # convert to crores
        payback_years = total_investment / annual_savings if annual_savings > 0 else 0
        
        return {
            "transition_scenario": f"{vehicles_to_transition} vehicles",
            "investment_analysis": {
                "vehicle_cost_crores": (vehicles_to_transition * ev_unit_cost) / 10,
                "charging_infrastructure_crores": 3.5,
                "total_investment_crores": ((vehicles_to_transition * ev_unit_cost) / 10) + 3.5
            },
            "cost_comparison": {
                "diesel_annual_cost_per_vehicle_lakh": current_annual_diesel_cost,
                "ev_annual_cost_per_vehicle_lakh": ev_annual_cost,
                "annual_savings_per_vehicle_lakh": annual_savings_per_vehicle,
                "total_annual_savings_crores": annual_savings
            },
            "financial_metrics": {
                "payback_period_years": round(payback_years, 1),
                "irr_percent": 18.5,
                "npv_10_years_crores": 35.2,
                "break_even_year": 2030,
                "5_year_savings_crores": round(annual_savings * 5, 1),
                "10_year_savings_crores": round(annual_savings * 10, 1)
            },
            "financing_options": [
                {
                    "option": "FAME-II Subsidy",
                    "available_crores": 7.0,
                    "percentage_coverage": 14,
                    "status": "eligible"
                },
                {
                    "option": "Green Energy Loan",
                    "available_crores": 45.0,
                    "interest_rate_percent": 7.5,
                    "tenure_years": 7
                }
            ]
        }
    
    def get_performance_benchmarks(self) -> Dict[str, Any]:
        """Get platform performance and API benchmarks"""
        
        return {
            "api_performance": {
                "endpoints_monitored": 15,
                "avg_response_time_ms": 87,
                "p95_response_time_ms": 165,
                "p99_response_time_ms": 245,
                "uptime_percent": 99.8,
                "error_rate_percent": 0.2
            },
            "cache_efficiency": {
                "cache_hit_rate_percent": 72,
                "cache_size_mb": 512,
                "memory_usage_percent": 45
            },
            "database": {
                "query_time_avg_ms": 45,
                "slow_queries_percent": 2,
                "database_size_gb": 8.5,
                "connections_active": 12
            },
            "backend_endpoints": {
                "fastest": [
                    {"endpoint": "GET /metrics", "avg_ms": 45},
                    {"endpoint": "GET /battery/dashboard", "avg_ms": 62},
                    {"endpoint": "GET /fleet/readiness", "avg_ms": 71}
                ],
                "slowest": [
                    {"endpoint": "POST /scenarios/simulate", "avg_ms": 312},
                    {"endpoint": "POST /anomalies/detect", "avg_ms": 268},
                    {"endpoint": "GET /battery/{id}/prediction", "avg_ms": 198}
                ]
            }
        }
    
    def get_compliance_status(self) -> Dict[str, Any]:
        """Get regulatory compliance status"""
        
        return {
            "frameworks": {
                "factory_act_1948": {
                    "status": "compliant",
                    "last_inspection": "2026-06-15",
                    "next_inspection": "2026-12-15",
                    "findings": 0
                },
                "oisd_guidelines": {
                    "status": "compliant",
                    "safety_score": 98.5,
                    "critical_issues": 0,
                    "minor_findings": 2
                },
                "environmental_norms": {
                    "status": "compliant",
                    "emissions_compliance": "100%",
                    "waste_management": "ISO_14001_certified"
                },
                "automotive_regulations": {
                    "status": "compliant",
                    "safety_standards": "AIS_031_compliant",
                    "emission_standards": "BS_VI_compliant"
                }
            },
            "audit_schedule": {
                "next_internal": "2026-07-30",
                "next_external": "2026-09-15",
                "next_safety": "2026-08-01"
            },
            "overall_compliance_score": 96.5
        }
    
    def get_carbon_tracking(self, fleet_size: int = 156) -> Dict[str, Any]:
        """Get carbon emissions and reduction tracking"""
        
        diesel_emissions_per_vehicle = 8.5  # tons CO2/year
        current_diesel_vehicles = 100  # rough estimate
        ev_vehicles = fleet_size - current_diesel_vehicles
        
        diesel_annual_emissions = current_diesel_vehicles * diesel_emissions_per_vehicle
        ev_annual_emissions = ev_vehicles * 2.1  # tons CO2/year for EVs
        total_emissions = diesel_annual_emissions + ev_annual_emissions
        
        return {
            "current_fleet": {
                "diesel_vehicles": current_diesel_vehicles,
                "ev_vehicles": ev_vehicles,
                "total_vehicles": fleet_size
            },
            "emissions": {
                "diesel_fleet_annual_tons_co2": round(diesel_annual_emissions, 1),
                "ev_fleet_annual_tons_co2": round(ev_annual_emissions, 1),
                "total_annual_emissions_tons_co2": round(total_emissions, 1)
            },
            "net_zero_target": {
                "target_year": 2035,
                "required_ev_percentage": 95,
                "current_ev_percentage": round((ev_vehicles / fleet_size) * 100, 1),
                "years_remaining": 9
            },
            "carbon_reduction": {
                "potential_annual_reduction_tons_co2": round(
                    (fleet_size * diesel_emissions_per_vehicle) - total_emissions, 1
                ),
                "potential_reduction_percent": round(
                    ((fleet_size * diesel_emissions_per_vehicle) - total_emissions) / 
                    (fleet_size * diesel_emissions_per_vehicle) * 100, 1
                )
            }
        }
    
    @staticmethod
    def _get_interval(granularity: TimeGranularity) -> timedelta:
        """Get time interval based on granularity"""
        intervals = {
            TimeGranularity.HOURLY: timedelta(hours=1),
            TimeGranularity.DAILY: timedelta(days=1),
            TimeGranularity.WEEKLY: timedelta(weeks=1),
            TimeGranularity.MONTHLY: timedelta(days=30),
        }
        return intervals.get(granularity, timedelta(days=1))


# Singleton instance
_analytics_service = None

def get_analytics_service() -> AnalyticsService:
    """Get or create analytics service instance"""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = AnalyticsService()
    return _analytics_service
