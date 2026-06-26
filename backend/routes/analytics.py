"""
Analytics API Routes
Endpoints for comprehensive platform analytics and insights
"""

from fastapi import APIRouter, Query
from typing import Dict, Any, Optional, List
from datetime import datetime

from services.analytics_service import get_analytics_service, TimeGranularity

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

analytics_service = get_analytics_service()


@router.get("/trends/battery-health")
async def get_battery_health_trends(
    granularity: str = Query("daily", description="Granularity: hourly, daily, weekly, monthly"),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
) -> Dict[str, Any]:
    """Get battery health trends over time"""
    try:
        granularity_enum = TimeGranularity[granularity.upper()]
    except KeyError:
        granularity_enum = TimeGranularity.DAILY
    
    return analytics_service.get_battery_health_trends(
        granularity=granularity_enum,
        days=days
    )


@router.get("/fleet/composition")
async def get_fleet_composition() -> Dict[str, Any]:
    """Get detailed fleet composition analytics"""
    return analytics_service.get_fleet_composition_analytics()


@router.get("/supply-chain/analytics")
async def get_supply_chain_analytics() -> Dict[str, Any]:
    """Get supply chain concentration and risk analytics"""
    return analytics_service.get_supply_chain_analytics()


@router.get("/maintenance/analytics")
async def get_maintenance_analytics() -> Dict[str, Any]:
    """Get maintenance cost and schedule analytics"""
    return analytics_service.get_maintenance_analytics()


@router.get("/roi/analysis")
async def get_roi_analysis(
    vehicles: int = Query(50, ge=1, le=156, description="Number of vehicles to transition")
) -> Dict[str, Any]:
    """Get ROI analysis for EV transition"""
    return analytics_service.get_roi_analytics(vehicles_to_transition=vehicles)


@router.get("/performance/benchmarks")
async def get_performance_benchmarks() -> Dict[str, Any]:
    """Get platform performance and API benchmarks"""
    return analytics_service.get_performance_benchmarks()


@router.get("/compliance/status")
async def get_compliance_status() -> Dict[str, Any]:
    """Get regulatory compliance status"""
    return analytics_service.get_compliance_status()


@router.get("/carbon/tracking")
async def get_carbon_tracking(
    fleet_size: int = Query(156, ge=1, le=500, description="Fleet size for carbon calculation")
) -> Dict[str, Any]:
    """Get carbon emissions and reduction tracking"""
    return analytics_service.get_carbon_tracking(fleet_size=fleet_size)


@router.get("/dashboard/summary")
async def get_analytics_dashboard_summary() -> Dict[str, Any]:
    """Get comprehensive analytics dashboard summary"""
    
    # Aggregate all analytics into one summary
    battery_trends = analytics_service.get_battery_health_trends(days=7)
    fleet_composition = analytics_service.get_fleet_composition_analytics()
    supply_chain = analytics_service.get_supply_chain_analytics()
    maintenance = analytics_service.get_maintenance_analytics()
    performance = analytics_service.get_performance_benchmarks()
    carbon = analytics_service.get_carbon_tracking()
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": {
            "fleet_health": {
                "total_vehicles": fleet_composition["total_vehicles"],
                "operational_percent": round(
                    (fleet_composition["by_status"]["operational"] / fleet_composition["total_vehicles"]) * 100, 1
                ),
                "average_battery_soh": battery_trends["summary"]["average_soh"],
                "readiness_score": 72.4
            },
            "supply_chain_health": {
                "overall_risk_score": supply_chain["supply_chain_health_score"],
                "active_suppliers": supply_chain["total_active_suppliers"],
                "critical_materials": len(supply_chain["material_breakdown"]),
                "risk_events_upcoming": supply_chain["risk_events_90d"]
            },
            "financial_metrics": {
                "ytd_savings_crores": 2.85,
                "maintenance_cost_crores": maintenance["cost_analysis"]["ytd_maintenance_cost_crores"],
                "projected_roi_years": 4.2
            },
            "platform_health": {
                "api_uptime_percent": performance["api_performance"]["uptime_percent"],
                "avg_response_ms": performance["api_performance"]["avg_response_time_ms"],
                "cache_hit_rate": performance["cache_efficiency"]["cache_hit_rate_percent"]
            },
            "carbon_impact": {
                "annual_emissions_tons_co2": carbon["emissions"]["total_annual_emissions_tons_co2"],
                "reduction_potential_percent": carbon["carbon_reduction"]["potential_reduction_percent"],
                "net_zero_target_year": carbon["net_zero_target"]["target_year"]
            }
        },
        "trends": battery_trends["summary"],
        "top_recommendations": [
            {
                "priority": "HIGH",
                "recommendation": "Diversify lithium suppliers to reduce concentration risk",
                "impact": "Reduce supply chain risk by 20%"
            },
            {
                "priority": "HIGH",
                "recommendation": "Phase 2 fleet transition (50 vehicles)",
                "impact": "Reduce annual operational costs by ₹2.5 Cr"
            },
            {
                "priority": "MEDIUM",
                "recommendation": "Update thermal management to improve battery SOH",
                "impact": "Extend battery life by 6 months"
            }
        ]
    }


@router.get("/health")
async def analytics_health() -> Dict[str, Any]:
    """Health check for analytics service"""
    return {
        "status": "operational",
        "service": "analytics",
        "timestamp": datetime.utcnow().isoformat()
    }
