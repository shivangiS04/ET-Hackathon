"""
Supply Chain Service Layer
Business logic for supply chain risk assessment and geopolitical analysis
"""

from typing import List, Dict, Tuple
from datetime import datetime
import math


class SupplyChainService:
    """Service for supply chain risk intelligence and analysis"""
    
    # Risk weights (must sum to 1.0)
    RISK_WEIGHTS = {
        "geopolitical": 0.40,
        "concentration": 0.30,
        "quality": 0.20,
        "logistics": 0.10
    }
    
    # Base country risk scores (0-1 scale)
    COUNTRY_RISKS = {
        "China": 0.92,
        "DR Congo": 0.85,
        "Indonesia": 0.55,
        "Australia": 0.35,
        "Chile": 0.42,
        "USA": 0.15,
        "Japan": 0.10,
        "Germany": 0.12,
    }
    
    @staticmethod
    def calculate_overall_risk(
        geopolitical_score: float,
        concentration_score: float,
        quality_score: float,
        logistics_score: float
    ) -> Tuple[float, str]:
        """
        Calculate overall supply chain risk using weighted average.
        
        Args:
            Scores in 0-1 range for each risk category
        
        Returns:
            Tuple of (overall_risk_score, risk_level)
        """
        overall = (
            geopolitical_score * SupplyChainService.RISK_WEIGHTS["geopolitical"] +
            concentration_score * SupplyChainService.RISK_WEIGHTS["concentration"] +
            quality_score * SupplyChainService.RISK_WEIGHTS["quality"] +
            logistics_score * SupplyChainService.RISK_WEIGHTS["logistics"]
        )
        
        overall = max(0, min(1, overall))  # Clamp to 0-1
        
        if overall >= 0.75:
            risk_level = "Critical"
        elif overall >= 0.60:
            risk_level = "High"
        elif overall >= 0.40:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return round(overall, 2), risk_level
    
    @staticmethod
    def calculate_supplier_risk(
        supplier_data: Dict,
        country: str,
        material: str,
        concentration_percent: float,
        quality_metrics: Dict
    ) -> Dict:
        """
        Calculate comprehensive risk score for a supplier.
        
        Args:
            supplier_data: Supplier profile data
            country: Supplier country
            material: Material supplied
            concentration_percent: % of total material from this supplier
            quality_metrics: Quality performance data
        
        Returns:
            Dictionary with risk breakdown
        """
        
        # Geopolitical risk (based on country)
        geo_risk = SupplyChainService.COUNTRY_RISKS.get(country, 0.50)
        
        # Concentration risk (higher concentration = higher risk)
        # Herfindahl index logic: risk increases exponentially with concentration
        conc_risk = math.sqrt(concentration_percent / 100)
        conc_risk = min(1.0, conc_risk)
        
        # Quality risk (from defect rates, on-time delivery, etc.)
        quality_risk = SupplyChainService._calculate_quality_risk(quality_metrics)
        
        # Delivery/logistics risk (lead time, port delays)
        delivery_risk = quality_metrics.get("delivery_risk", 0.40)
        
        # Overall risk
        overall, risk_level = SupplyChainService.calculate_overall_risk(
            geo_risk, conc_risk, quality_risk, delivery_risk
        )
        
        return {
            "supplier_id": supplier_data.get("supplier_id", "UNKNOWN"),
            "overall_risk_score": overall,
            "risk_level": risk_level,
            "geopolitical_risk": round(geo_risk, 3),
            "concentration_risk": round(conc_risk, 3),
            "quality_risk": round(quality_risk, 3),
            "delivery_risk": round(delivery_risk, 3),
            "country": country,
            "concentration_percentage": concentration_percent,
            "material": material,
        }
    
    @staticmethod
    def _calculate_quality_risk(quality_metrics: Dict) -> float:
        """Calculate quality risk from defect rates and compliance"""
        defect_rate = quality_metrics.get("defect_rate_ppm", 500) / 10000  # Convert ppm to %
        on_time = 100 - quality_metrics.get("on_time_delivery_percent", 95)
        invoice_error = 100 - quality_metrics.get("invoice_accuracy_percent", 98)
        
        # Weighted quality risk
        risk = (defect_rate * 0.6 + on_time * 0.3 + invoice_error * 0.1) / 100
        
        return min(1.0, risk)
    
    @staticmethod
    def assess_geopolitical_events(
        events: List[Dict],
        affected_suppliers: List[str]
    ) -> Dict:
        """
        Assess impact of geopolitical events on suppliers.
        
        Args:
            events: List of geopolitical events
            affected_suppliers: List of supplier IDs that could be affected
        
        Returns:
            Impact assessment
        """
        
        total_impact = 0
        event_count = len(events)
        
        for event in events:
            severity_map = {"low": 0.2, "medium": 0.5, "high": 1.0}
            severity = severity_map.get(event.get("severity", "low"), 0.5)
            total_impact += event.get("impact_on_supply", 0.5) * severity
        
        avg_impact = total_impact / event_count if event_count > 0 else 0
        
        return {
            "total_events": event_count,
            "avg_impact_score": round(avg_impact, 3),
            "affected_suppliers": len(affected_suppliers),
            "recommendation": SupplyChainService._get_geopolitical_recommendation(avg_impact),
            "last_updated": datetime.now().isoformat(),
        }
    
    @staticmethod
    def _get_geopolitical_recommendation(impact_score: float) -> str:
        """Get recommendation based on geopolitical impact"""
        if impact_score >= 0.7:
            return "🔴 CRITICAL: Activate alternative supplier protocols immediately"
        elif impact_score >= 0.5:
            return "⚠️ HIGH: Begin diversification planning and lock long-term contracts"
        elif impact_score >= 0.3:
            return "⚠ MEDIUM: Monitor situation and increase safety stock"
        else:
            return "✓ LOW: Continue normal operations with standard monitoring"
    
    @staticmethod
    def identify_supplier_alternatives(
        primary_supplier: Dict,
        material: str,
        alternative_suppliers: List[Dict]
    ) -> List[Dict]:
        """
        Identify and rank alternative suppliers for a material.
        
        Args:
            primary_supplier: Current supplier data
            material: Material type
            alternative_suppliers: List of potential alternatives
        
        Returns:
            Ranked list of alternatives
        """
        
        ranked = []
        for alt in alternative_suppliers:
            score = 100
            
            # Penalize for quality issues
            score -= alt.get("defect_rate_ppm", 0) / 100
            
            # Penalize for poor on-time delivery
            score -= (100 - alt.get("on_time_delivery_percent", 95))
            
            # Penalize for concentration risk
            concentration = alt.get("concentration_percentage", 30)
            score -= (concentration / 100) * 20
            
            ranked.append({
                "supplier_id": alt.get("supplier_id"),
                "supplier_name": alt.get("supplier_name"),
                "country": alt.get("country"),
                "suitability_score": max(0, score),
                "lead_time_weeks": alt.get("lead_time_weeks", 12),
                "price_relative_to_primary": alt.get("price_multiplier", 1.0),
            })
        
        # Sort by suitability score (descending)
        ranked.sort(key=lambda x: x["suitability_score"], reverse=True)
        
        return ranked
    
    @staticmethod
    def calculate_material_sourcing_risk(
        material: str,
        suppliers_data: List[Dict]
    ) -> Dict:
        """
        Calculate aggregate risk for sourcing a specific material.
        
        Args:
            material: Material name (e.g., "Lithium", "Cobalt")
            suppliers_data: List of supplier data for this material
        
        Returns:
            Material sourcing risk assessment
        """
        
        if not suppliers_data:
            return {}
        
        risks = [s.get("risk_score", 0.5) for s in suppliers_data]
        concentrations = [s.get("concentration_percentage", 20) for s in suppliers_data]
        
        total_concentration = sum(concentrations)
        herfindahl_index = sum((c/total_concentration)**2 for c in concentrations) if total_concentration > 0 else 0
        
        return {
            "material": material,
            "suppliers_count": len(suppliers_data),
            "avg_risk_score": round(sum(risks) / len(risks), 3),
            "max_supplier_concentration": round(max(concentrations), 1),
            "top_3_concentration": round(sum(sorted(concentrations, reverse=True)[:3]), 1),
            "herfindahl_index": round(herfindahl_index, 3),
            "diversification_level": SupplyChainService._get_diversification_level(herfindahl_index),
        }
    
    @staticmethod
    def _get_diversification_level(herfindahl: float) -> str:
        """Classify diversification level based on Herfindahl index"""
        if herfindahl > 0.66:
            return "Low (High concentration risk)"
        elif herfindahl > 0.33:
            return "Moderate"
        else:
            return "High (Well diversified)"
    
    @staticmethod
    def calculate_supply_chain_risk_propagation(
        suppliers: List[Dict],
        materials_graph: Dict[str, List[str]],
        max_depth: int = 3
    ) -> Dict:
        """
        Calculate risk propagation through multi-tier supply chain network.
        
        Simulates how disruption in one supplier cascades through tiers.
        Uses graph traversal with exponential decay of impact.
        
        Args:
            suppliers: List of supplier nodes with risk scores
            materials_graph: Graph of material dependencies
            max_depth: Maximum tiers to traverse
        
        Returns:
            Network-level risk assessment with cascade impact
        """
        
        # Calculate direct supplier risks
        direct_risks = [s.get("risk_score", 0.5) for s in suppliers]
        direct_avg = sum(direct_risks) / len(direct_risks) if direct_risks else 0
        
        # Calculate concentration (Herfindahl-Hirschman Index for network)
        concentrations = [s.get("concentration_percentage", 0) for s in suppliers]
        total_concentration = sum(concentrations)
        
        if total_concentration > 0:
            market_shares_normalized = [c / total_concentration for c in concentrations]
            hhi = sum(share ** 2 for share in market_shares_normalized)
        else:
            hhi = 0
        
        # Tier-based propagation (simplified multi-tier model)
        tier_risks = [direct_avg]  # Tier 1
        
        for tier in range(2, min(max_depth + 1, 4)):
            # Risk decays with each tier (10% propagation per tier beyond Tier 1)
            tier_risk = tier_risks[-1] * (0.3 ** (tier - 1))
            tier_risks.append(tier_risk)
        
        # Calculate network vulnerability
        network_vulnerability = sum(tier_risks) / len(tier_risks)
        
        # Resilience score (inverse of vulnerability)
        resilience = 1 - network_vulnerability
        
        # Recommendation based on network risk
        if network_vulnerability >= 0.7:
            recommendation = "🔴 CRITICAL: Urgent supply chain restructuring required"
            resilience_level = "Critical"
        elif network_vulnerability >= 0.5:
            recommendation = "⚠️ HIGH: Implement redundancy and alternative sourcing"
            resilience_level = "Low"
        elif network_vulnerability >= 0.3:
            recommendation = "⚠ MEDIUM: Develop secondary suppliers for critical materials"
            resilience_level = "Moderate"
        else:
            recommendation = "✓ LOW: Supply chain is resilient"
            resilience_level = "High"
        
        return {
            "tier_1_risk": round(tier_risks[0], 3),
            "tier_2_risk": round(tier_risks[1] if len(tier_risks) > 1 else 0, 3),
            "tier_3_risk": round(tier_risks[2] if len(tier_risks) > 2 else 0, 3),
            "network_vulnerability_score": round(network_vulnerability, 3),
            "network_resilience_score": round(resilience, 3),
            "resilience_level": resilience_level,
            "herfindahl_hirschman_index": round(hhi, 3),
            "supplier_concentration_risk": "High" if hhi > 0.5 else "Moderate" if hhi > 0.25 else "Low",
            "recommendation": recommendation,
            "estimated_recovery_time_days": int(30 * network_vulnerability),
            "critical_failure_probability": round(network_vulnerability, 2)
        }
