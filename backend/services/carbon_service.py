"""
Carbon Intelligence & Net Zero Roadmap Service
Calculates emissions (Scope 1 & 3), generates decarbonization strategies,
and identifies high-impact vehicles for EV transition
Uses realistic emission factors aligned with GRI, UNFCCC, and FAME-II policy
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class EmissionFactors:
    """Standardized emission factors (kg CO2/unit)"""
    DIESEL_DIRECT = 2.68                    # kg CO2/litre (Well-to-Wheel)
    DIESEL_SUPPLY_CHAIN = 0.5               # kg CO2/litre (upstream)
    DIESEL_FUEL_EFFICIENCY = 12.0           # km/litre for truck
    
    BATTERY_MFG_CO2_PER_VEHICLE = 8100      # kg CO2 per vehicle (WtW)
    BATTERY_LIFESPAN_YEARS = 8              # years
    BATTERY_ANNUAL_CO2 = 1010               # kg CO2/year amortized
    
    EV_EMISSION_FACTOR = 0.08               # kg CO2/km (grid electricity, India avg)
    
    # Supply chain freight (kg CO2 per tonne-km)
    FREIGHT_EMISSION_FACTOR = 0.08          # Sea freight constant
    
    # Supplier routes
    CHINA_DISTANCE_KM = 7500
    AUSTRALIA_DISTANCE_KM = 4500
    CHILE_DISTANCE_KM = 20000


class CarbonIntelligenceService:
    """AI-powered carbon accounting and net-zero transition planning"""
    
    def __init__(self):
        """Initialize emission factors and baseline data"""
        self.emission_factors = EmissionFactors()
        np.random.seed(42)
    
    def calculate_emissions_by_vehicle(
        self,
        vehicle_id: str,
        vehicle_type: str,
        route_km_per_day: float,
        is_ev: bool,
        working_days_per_year: int = 250
    ) -> dict:
        """
        Calculate Scope 1 and Scope 3 emissions for a vehicle.
        
        Scope 1: Direct emissions from fuel combustion
        Scope 3: Indirect emissions from supply chain & manufacturing
        
        Args:
            vehicle_id: Vehicle identifier (e.g., "VEH_00001")
            vehicle_type: "truck", "bus", "car", etc.
            route_km_per_day: Daily route distance (km)
            is_ev: Boolean indicating if vehicle is electric
            working_days_per_year: Annual working days (default 250)
        
        Returns:
            dict with emissions breakdown
        """
        
        # Calculate annual kilometers
        annual_km = route_km_per_day * working_days_per_year
        
        if is_ev:
            # EV Emissions (primarily from electricity generation)
            annual_scope1 = 0  # No direct combustion
            
            # Scope 3: Grid electricity emissions + battery manufacturing
            electricity_emissions_kg = annual_km * self.emission_factors.EV_EMISSION_FACTOR
            battery_emissions_kg = self.emission_factors.BATTERY_ANNUAL_CO2
            annual_scope3 = (electricity_emissions_kg + battery_emissions_kg) / 1000
            
            # Compare to diesel baseline
            diesel_liters_equivalent = annual_km / self.emission_factors.DIESEL_FUEL_EFFICIENCY
            diesel_direct = (diesel_liters_equivalent * 
                           self.emission_factors.DIESEL_DIRECT) / 1000
            diesel_supply = (diesel_liters_equivalent * 
                           self.emission_factors.DIESEL_SUPPLY_CHAIN) / 1000
            diesel_scope3_baseline = (diesel_liters_equivalent * 
                                     self.emission_factors.BATTERY_ANNUAL_CO2 / 1000)
            
            diesel_total = diesel_direct + diesel_supply + diesel_scope3_baseline
            ev_total = annual_scope1 + annual_scope3
            carbon_saved = diesel_total - ev_total
            vs_diesel_baseline = (carbon_saved / diesel_total * 100) if diesel_total > 0 else 0
            
        else:
            # Diesel Vehicle
            diesel_liters = annual_km / self.emission_factors.DIESEL_FUEL_EFFICIENCY
            
            # Scope 1: Direct combustion
            annual_scope1 = (diesel_liters * 
                           self.emission_factors.DIESEL_DIRECT) / 1000  # Convert to tonnes
            
            # Scope 3: Fuel supply chain + battery manufacturing
            fuel_supply_chain = (diesel_liters * 
                               self.emission_factors.DIESEL_SUPPLY_CHAIN) / 1000
            battery_amortized = self.emission_factors.BATTERY_ANNUAL_CO2 / 1000
            annual_scope3 = fuel_supply_chain + battery_amortized
            
            carbon_saved = 0
            vs_diesel_baseline = 0
        
        total_annual_tonnes = annual_scope1 + annual_scope3
        
        return {
            "vehicle_id": vehicle_id,
            "vehicle_type": vehicle_type,
            "is_ev": is_ev,
            "annual_km": annual_km,
            "annual_scope1_tonnes": round(annual_scope1, 3),
            "annual_scope3_tonnes": round(annual_scope3, 3),
            "total_annual_tonnes": round(total_annual_tonnes, 3),
            "vs_diesel_baseline_percent": round(vs_diesel_baseline, 1) if is_ev else 0,
            "carbon_saved_tonnes": round(carbon_saved, 3) if is_ev else 0,
            "breakdown": {
                "scope1_description": "Direct fuel combustion" if not is_ev else "None",
                "scope3_description": ("Fuel supply chain + battery mfg" if not is_ev 
                                      else "Grid electricity + battery mfg"),
                "fuel_type": "Diesel" if not is_ev else "Electric"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_net_zero_roadmap(
        self,
        total_vehicles: int,
        current_ev_count: int,
        target_year: int = 2030,
        base_year: int = 2026
    ) -> dict:
        """
        Generate year-by-year net-zero transition roadmap aligned with FAME-II policy.
        
        India's FAME-II target: 30% EV adoption by 2030
        
        Args:
            total_vehicles: Total fleet size
            current_ev_count: Current EVs in fleet
            target_year: Target year for 30% EV (default 2030)
            base_year: Starting year (default 2026)
        
        Returns:
            dict with phase-by-phase roadmap
        """
        
        current_diesel_count = total_vehicles - current_ev_count
        years_to_target = target_year - base_year
        
        # Calculate annual EV growth needed to reach 30% by target year
        target_ev_count = int(total_vehicles * 0.30)
        additional_evs_needed = target_ev_count - current_ev_count
        annual_ev_addition = max(1, additional_evs_needed // max(1, years_to_target))
        
        phases = []
        cumulative_savings = 0
        net_zero_year = None
        
        # Baseline emissions per vehicle (typical fleet composition)
        avg_diesel_emissions_per_vehicle = 45.0  # tonnes/year (from calculate_emissions_by_vehicle)
        avg_ev_emissions_per_vehicle = 3.2  # tonnes/year (from calculate_emissions_by_vehicle)
        
        for year_offset in range(years_to_target + 1):
            year = base_year + year_offset
            
            # EV ramp-up calculation
            if year_offset == 0:
                year_ev_count = current_ev_count
                year_diesel_count = current_diesel_count
            else:
                year_ev_count = min(
                    current_ev_count + (year_offset * annual_ev_addition),
                    total_vehicles
                )
                year_diesel_count = total_vehicles - year_ev_count
            
            # Calculate emissions
            diesel_emissions = year_diesel_count * avg_diesel_emissions_per_vehicle
            ev_emissions = year_ev_count * avg_ev_emissions_per_vehicle
            total_emissions = diesel_emissions + ev_emissions
            
            # Savings relative to 2026 baseline
            baseline_2026 = (current_diesel_count * avg_diesel_emissions_per_vehicle + 
                           current_ev_count * avg_ev_emissions_per_vehicle)
            year_savings = baseline_2026 - total_emissions
            cumulative_savings += year_savings if year_offset > 0 else 0
            
            # Investment (Tesla Model 3: ~3 Cr, diesel truck: ~30 Lakh)
            evs_added_this_year = (year_ev_count - (current_ev_count + 
                                  ((year_offset - 1) * annual_ev_addition if year_offset > 0 else 0)))
            investment_crores = (evs_added_this_year * 3.0) / 100  # 3 Cr per 100 vehicles
            
            # Carbon credits (1 tonne CO2 = ~3-4 credits at INR 500/credit)
            carbon_credits_tonnes = year_savings
            
            # Check net-zero (approximate: <10% of baseline emissions)
            emissions_vs_baseline = (total_emissions / baseline_2026 * 100) if baseline_2026 > 0 else 0
            if net_zero_year is None and emissions_vs_baseline < 10:
                net_zero_year = year
            
            phases.append({
                "year": year,
                "ev_vehicles": year_ev_count,
                "diesel_vehicles": year_diesel_count,
                "ev_percentage": round((year_ev_count / total_vehicles * 100), 1),
                "total_emissions_tonnes": round(total_emissions, 1),
                "year_savings_tonnes": round(year_savings, 1),
                "cumulative_savings_tonnes": round(cumulative_savings, 1),
                "investment_required_cr": round(investment_crores, 2),
                "carbon_credits_earned": round(carbon_credits_tonnes, 1),
                "policy_milestone": self._get_policy_milestone(year, year_ev_count / total_vehicles)
            })
        
        total_carbon_saved_2030 = cumulative_savings
        target_met = phases[-1]["ev_percentage"] >= 30
        
        return {
            "base_year": base_year,
            "target_year": target_year,
            "phases": phases,
            "2030_target_met": target_met,
            "target_ev_percentage": 30,
            "total_carbon_saved_2030_tonnes": round(total_carbon_saved_2030, 1),
            "cumulative_investment_cr": round(sum(p["investment_required_cr"] for p in phases), 2),
            "net_zero_year": net_zero_year,
            "policy_alignment": "FAME-II (30% EV by 2030)",
            "timeline_feasibility": self._assess_timeline_feasibility(
                phases, target_ev_count, total_vehicles
            ),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def identify_high_impact_targets(self, fleet_data: List[dict]) -> dict:
        """
        Identify high-priority vehicles for EV transition based on carbon impact.
        
        Impact score formula:
        score = route_km_per_day * (diesel_ef - ev_ef) * working_days_per_year
        
        where diesel_ef and ev_ef are emission factors (kg CO2/km)
        
        Args:
            fleet_data: List of vehicle dicts with:
                - vehicle_id, vehicle_type, route_km_per_day, is_ev, working_days_per_year
        
        Returns:
            dict with ranked high-impact targets
        """
        
        ranked_vehicles = []
        total_addressable_carbon = 0
        
        for vehicle in fleet_data:
            if vehicle.get("is_ev", False):
                continue  # Skip already-EV vehicles
            
            vehicle_id = vehicle["vehicle_id"]
            route_km_per_day = vehicle.get("route_km_per_day", 100)
            working_days = vehicle.get("working_days_per_year", 250)
            
            # Diesel emission factor: 2.68 kg/L ÷ 12 km/L = 0.223 kg CO2/km
            diesel_ef_per_km = (self.emission_factors.DIESEL_DIRECT / 
                              self.emission_factors.DIESEL_FUEL_EFFICIENCY)
            
            # EV emission factor: 0.08 kg CO2/km (grid electricity)
            ev_ef_per_km = self.emission_factors.EV_EMISSION_FACTOR
            
            # Impact score = tonnes CO2 saved per year
            annual_carbon_saving = (
                route_km_per_day * working_days * 
                (diesel_ef_per_km - ev_ef_per_km) / 1000
            )
            
            # Priority scoring (higher = more important)
            # Factors: annual savings, route intensity, consistency
            impact_score = annual_carbon_saving * 100  # Scale for visibility
            
            total_addressable_carbon += annual_carbon_saving
            
            # Determine priority (top 20% vehicles account for ~80% of savings)
            priority = "high" if impact_score > 50 else "medium" if impact_score > 20 else "low"
            
            ranked_vehicles.append({
                "vehicle_id": vehicle_id,
                "vehicle_type": vehicle.get("vehicle_type", "truck"),
                "route_km_per_day": route_km_per_day,
                "working_days_per_year": working_days,
                "current_annual_emissions_tonnes": round(
                    route_km_per_day * working_days * diesel_ef_per_km / 1000, 2
                ),
                "potential_annual_saving_tonnes": round(annual_carbon_saving, 2),
                "impact_score": round(impact_score, 1),
                "priority": priority,
                "payback_period_years": round(
                    3.0 / (annual_carbon_saving / 50) if annual_carbon_saving > 0 else 0, 1
                ),  # EV cost 3 Cr, diesel truck 30 Lakh
                "roi_carbon_tons_per_crore": round(
                    annual_carbon_saving / 3.0 * 100, 1
                )
            })
        
        # Sort by impact score descending
        ranked_vehicles.sort(key=lambda x: x["impact_score"], reverse=True)
        
        # Get top 5 for dashboard display
        top_5 = ranked_vehicles[:5]
        
        return {
            "ranked_vehicles": ranked_vehicles,
            "top_5_high_impact": top_5,
            "total_vehicles_analyzed": len(fleet_data),
            "vehicles_suitable_for_ev": len(ranked_vehicles),
            "total_addressable_carbon_tonnes": round(total_addressable_carbon, 1),
            "high_priority_count": len([v for v in ranked_vehicles if v["priority"] == "high"]),
            "medium_priority_count": len([v for v in ranked_vehicles if v["priority"] == "medium"]),
            "low_priority_count": len([v for v in ranked_vehicles if v["priority"] == "low"]),
            "carbon_reduction_potential_percent": round(
                (total_addressable_carbon / 
                 (total_addressable_carbon + sum(v["current_annual_emissions_tonnes"] 
                  for v in top_5)) * 100) if total_addressable_carbon > 0 else 0, 1
            ),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def calculate_scope3_supply_chain(self, supplier_data: List[dict]) -> dict:
        """
        Calculate Scope 3 emissions from supply chain by supplier origin.
        
        Assumes sea freight at 0.08 kg CO2/tonne-km across all origins.
        
        Args:
            supplier_data: List of supplier dicts with:
                - supplier_id, country, annual_tonnes_shipped, product_type
        
        Returns:
            dict with supply chain emissions breakdown
        """
        
        # Supplier routes and distances
        supplier_routes = {
            "china": {
                "distance_km": self.emission_factors.CHINA_DISTANCE_KM,
                "region": "East Asia"
            },
            "australia": {
                "distance_km": self.emission_factors.AUSTRALIA_DISTANCE_KM,
                "region": "Oceania"
            },
            "chile": {
                "distance_km": self.emission_factors.CHILE_DISTANCE_KM,
                "region": "South America"
            },
            "india": {
                "distance_km": 0,  # Domestic, minimal transport
                "region": "Domestic"
            }
        }
        
        by_supplier = []
        total_scope3_supply_chain = 0
        highest_emission_supplier = None
        highest_emission_value = 0
        
        for supplier in supplier_data:
            supplier_id = supplier.get("supplier_id", "Unknown")
            country = supplier.get("country", "india").lower()
            annual_tonnes = supplier.get("annual_tonnes_shipped", 100)
            
            # Get distance, default to India if not found
            route_info = supplier_routes.get(country, supplier_routes["india"])
            distance_km = route_info["distance_km"]
            
            # Calculate emissions: tonnes * distance * emission_factor
            emissions_kg = (annual_tonnes * distance_km * 
                          self.emission_factors.FREIGHT_EMISSION_FACTOR)
            emissions_tonnes = emissions_kg / 1000
            
            total_scope3_supply_chain += emissions_tonnes
            
            # Track highest emitter
            if emissions_tonnes > highest_emission_value:
                highest_emission_value = emissions_tonnes
                highest_emission_supplier = supplier_id
            
            by_supplier.append({
                "supplier_id": supplier_id,
                "country": country,
                "region": route_info["region"],
                "annual_tonnes_shipped": annual_tonnes,
                "transport_distance_km": distance_km,
                "annual_scope3_emissions_tonnes": round(emissions_tonnes, 2),
                "emissions_per_tonne_shipped": round(
                    (emissions_tonnes / annual_tonnes * 1000) if annual_tonnes > 0 else 0, 4
                ),
                "emission_factor_kg_per_tonne_km": self.emission_factors.FREIGHT_EMISSION_FACTOR
            })
        
        # Calculate diversification benefit
        # Moving away from long-distance suppliers reduces emissions
        if len(by_supplier) > 0:
            avg_distance = np.mean([s["transport_distance_km"] for s in by_supplier])
            if avg_distance > 5000:
                diversification_benefit_percent = 20  # Potential 20% reduction with diversification
            elif avg_distance > 2000:
                diversification_benefit_percent = 10
            else:
                diversification_benefit_percent = 5
            
            diversification_carbon_benefit = (
                total_scope3_supply_chain * diversification_benefit_percent / 100
            )
        else:
            diversification_carbon_benefit = 0
        
        return {
            "by_supplier": by_supplier,
            "total_suppliers": len(supplier_data),
            "total_scope3_supply_chain_tonnes": round(total_scope3_supply_chain, 1),
            "average_emissions_per_supplier_tonnes": round(
                total_scope3_supply_chain / max(1, len(by_supplier)), 1
            ),
            "highest_emission_supplier": highest_emission_supplier,
            "highest_emission_value_tonnes": round(highest_emission_value, 1),
            "diversification_carbon_benefit_tonnes": round(diversification_carbon_benefit, 1),
            "recommended_action": self._get_supply_chain_recommendation(
                total_scope3_supply_chain, highest_emission_value
            ),
            "top_3_suppliers_by_emissions": sorted(
                by_supplier, key=lambda x: x["annual_scope3_emissions_tonnes"], reverse=True
            )[:3],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _get_policy_milestone(self, year: int, ev_percentage: float) -> str:
        """Get relevant policy milestone for a given year and EV%"""
        if year == 2026:
            return "FAME-II Phase 1: Foundation"
        elif year <= 2027 and ev_percentage >= 0.15:
            return "15% EV adoption target"
        elif year <= 2028 and ev_percentage >= 0.20:
            return "20% EV adoption milestone"
        elif year <= 2030 and ev_percentage >= 0.30:
            return "FAME-II 30% EV target (2030)"
        else:
            return "Transition ongoing"
    
    def _assess_timeline_feasibility(
        self,
        phases: List[dict],
        target_ev_count: int,
        total_vehicles: int
    ) -> str:
        """Assess if the timeline is feasible given growth constraints"""
        final_ev_percent = phases[-1]["ev_percentage"]
        
        if final_ev_percent >= 30:
            return "FEASIBLE: 30% EV target achievable on schedule"
        elif final_ev_percent >= 25:
            return "CHALLENGING: Near 30% target, may need acceleration"
        elif final_ev_percent >= 20:
            return "AT_RISK: Significant gap to 30% target"
        else:
            return "CRITICAL: Timeline unfeasible, major changes required"
    
    def _get_supply_chain_recommendation(
        self,
        total_emissions: float,
        highest_emission: float
    ) -> str:
        """Get supply chain optimization recommendation"""
        highest_percent = (highest_emission / total_emissions * 100) if total_emissions > 0 else 0
        
        if highest_percent > 40:
            return "URGENT: Diversify away from highest-emission supplier"
        elif highest_percent > 25:
            return "IMPORTANT: Consider alternative suppliers for high-emission items"
        elif total_emissions > 500:
            return "RECOMMENDED: Explore regional sourcing to reduce transport distance"
        else:
            return "MONITOR: Continue current supply chain with periodic reviews"
