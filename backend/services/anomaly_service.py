"""
Anomaly Detection System for EV Fleet & Supply Chain

Identifies unusual patterns that indicate problems:
- Battery degradation accelerating
- Supplier concentration increasing
- Geopolitical risks spiking
- Fleet vehicles failing earlier than expected
- Charging infrastructure bottlenecks
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass
class Anomaly:
    """Detected anomaly"""
    anomaly_id: str
    type: str  # battery, supply_chain, fleet, infrastructure
    severity: str  # critical, high, medium, low
    description: str
    affected_count: int
    start_time: datetime
    zscore: float
    confidence: float
    recommended_action: str
    historical_trend: List[float]


class AnomalyDetectionService:
    """Service for detecting anomalies in fleet and supply chain data"""

    def __init__(self):
        # Store anomaly history (in production, this would be in a database)
        self.anomalies_history: List[Anomaly] = []
        self.last_baseline = {}

    def detect_anomalies(self, fleet_data: Dict[str, Any], supply_chain_data: Dict[str, Any]) -> List[Anomaly]:
        """Scan all data sources for anomalies"""
        anomalies = []

        # Battery anomalies
        anomalies.extend(self._detect_battery_anomalies(fleet_data))

        # Supply chain anomalies
        anomalies.extend(self._detect_supply_chain_anomalies(supply_chain_data))

        # Fleet-level anomalies
        anomalies.extend(self._detect_fleet_anomalies(fleet_data))

        # Infrastructure anomalies
        anomalies.extend(self._detect_infrastructure_anomalies(fleet_data))

        # Store in history
        self.anomalies_history.extend(anomalies)

        return anomalies

    def _detect_battery_anomalies(self, fleet_data: Dict[str, Any]) -> List[Anomaly]:
        """Detect battery-related anomalies"""
        anomalies = []

        vehicles = fleet_data.get("vehicles", [])
        if not vehicles:
            return anomalies

        # Calculate average degradation rate
        degradation_rates = []
        for vehicle in vehicles:
            battery = vehicle.get("battery", {})
            if battery.get("soh_percent") and battery.get("age_months"):
                degradation_per_month = (100 - battery["soh_percent"]) / max(1, battery["age_months"])
                degradation_rates.append(degradation_per_month)

        if degradation_rates:
            avg_degradation = sum(degradation_rates) / len(degradation_rates)
            std_degradation = self._calculate_std_dev(degradation_rates, avg_degradation)

            # Find vehicles with abnormal degradation
            for i, vehicle in enumerate(vehicles):
                battery = vehicle.get("battery", {})
                if battery.get("age_months"):
                    degradation = (100 - battery["soh_percent"]) / battery["age_months"]
                    zscore = (degradation - avg_degradation) / max(0.1, std_degradation)

                    # Flag if >2 sigma above mean (faster degradation than normal)
                    if zscore > 2.0:
                        anomaly = Anomaly(
                            anomaly_id=f"BATTERY_DEGRAD_{vehicle['id']}",
                            type="battery",
                            severity="high" if zscore > 3.0 else "medium",
                            description=f"Battery degradation rate {degradation:.2f}%/month is {zscore:.1f}σ above normal",
                            affected_count=1,
                            start_time=datetime.now(),
                            zscore=zscore,
                            confidence=min(1.0, 0.7 + (zscore / 10)),
                            recommended_action=f"Inspect vehicle {vehicle['id']} battery. May indicate thermal stress or charging issues. Schedule maintenance within 2 weeks.",
                            historical_trend=degradation_rates[-5:] if len(degradation_rates) >= 5 else degradation_rates,
                        )
                        anomalies.append(anomaly)

        # Check for RUL approaching (< 60 days)
        vehicles_near_eol = 0
        for vehicle in vehicles:
            battery = vehicle.get("battery", {})
            if battery.get("rulf_days", 0) < 60:
                vehicles_near_eol += 1

        if vehicles_near_eol > int(len(vehicles) * 0.1):  # >10% near end of life
            anomaly = Anomaly(
                anomaly_id="BATTERY_EOL_CLUSTERING",
                type="battery",
                severity="high",
                description=f"{vehicles_near_eol} vehicles have battery RUL < 60 days",
                affected_count=vehicles_near_eol,
                start_time=datetime.now(),
                zscore=2.5,
                confidence=0.9,
                recommended_action="Schedule battery replacement program. Coordinate with suppliers for bulk procurement. Consider staggered replacement to maintain fleet availability.",
                historical_trend=[vehicles_near_eol],
            )
            anomalies.append(anomaly)

        return anomalies

    def _detect_supply_chain_anomalies(self, supply_chain_data: Dict[str, Any]) -> List[Anomaly]:
        """Detect supply chain anomalies"""
        anomalies = []

        overall_risk = supply_chain_data.get("overall_risk_score", 0.5)
        suppliers = supply_chain_data.get("suppliers", [])

        # Check for sudden risk score increase
        if overall_risk > 0.75:
            zscore = (overall_risk - 0.5) / 0.2  # Assume normal is 0.5 ± 0.2
            anomaly = Anomaly(
                anomaly_id="SUPPLY_CHAIN_RISK_HIGH",
                type="supply_chain",
                severity="critical" if overall_risk > 0.85 else "high",
                description=f"Overall supply chain risk elevated to {overall_risk:.2f}/1.0",
                affected_count=len(suppliers),
                start_time=datetime.now(),
                zscore=zscore,
                confidence=0.88,
                recommended_action="Review recent geopolitical events, supplier announcements. Activate contingency suppliers. Consider spot purchases to increase buffer inventory.",
                historical_trend=[overall_risk],
            )
            anomalies.append(anomaly)

        # Check for supplier concentration (Herfindahl index)
        if suppliers:
            supplier_shares = [s.get("market_share_percent", 0) for s in suppliers]
            hhi = sum(x ** 2 for x in supplier_shares)  # Herfindahl-Hirschman Index

            # HHI > 2500 indicates high concentration
            if hhi > 2500:
                anomaly = Anomaly(
                    anomaly_id="SUPPLIER_CONCENTRATION_HIGH",
                    type="supply_chain",
                    severity="high",
                    description=f"Supplier concentration HHI index at {hhi:.0f} (>2500 is monopolistic)",
                    affected_count=1,
                    start_time=datetime.now(),
                    zscore=2.8,
                    confidence=0.92,
                    recommended_action="Diversify supplier base. Identify and qualify 2-3 alternative suppliers for each component. Negotiate contracts with >2 suppliers per material.",
                    historical_trend=[hhi],
                )
                anomalies.append(anomaly)

            # Check for single supplier > 50%
            max_share = max(supplier_shares) if supplier_shares else 0
            if max_share > 50:
                anomaly = Anomaly(
                    anomaly_id="SUPPLIER_SINGLE_DEPENDENCY",
                    type="supply_chain",
                    severity="critical",
                    description=f"Single supplier has {max_share:.0f}% market share (> 50% threshold)",
                    affected_count=1,
                    start_time=datetime.now(),
                    zscore=3.5,
                    confidence=0.95,
                    recommended_action="URGENT: Reduce dependency on dominant supplier to <40%. Activate backup suppliers immediately. Negotiate multi-source contracts.",
                    historical_trend=[max_share],
                )
                anomalies.append(anomaly)

        return anomalies

    def _detect_fleet_anomalies(self, fleet_data: Dict[str, Any]) -> List[Anomaly]:
        """Detect fleet-level anomalies"""
        anomalies = []

        vehicles = fleet_data.get("vehicles", [])
        readiness_scores = [v.get("readiness_score", 0) for v in vehicles if "readiness_score" in v]

        if readiness_scores:
            avg_readiness = sum(readiness_scores) / len(readiness_scores)

            # If average readiness < 60%, flag it
            if avg_readiness < 60:
                zscore = (avg_readiness - 75) / 15  # Assume target is 75 ± 15
                anomaly = Anomaly(
                    anomaly_id="FLEET_READINESS_LOW",
                    type="fleet",
                    severity="high" if avg_readiness < 50 else "medium",
                    description=f"Fleet average readiness score is {avg_readiness:.0f}% (below 60% threshold)",
                    affected_count=len([s for s in readiness_scores if s < 50]),
                    start_time=datetime.now(),
                    zscore=abs(zscore),
                    confidence=0.85,
                    recommended_action="Review underperforming vehicles. Update route compatibility analysis. May indicate charging infrastructure gaps or vehicle age issues.",
                    historical_trend=readiness_scores[-5:] if len(readiness_scores) >= 5 else readiness_scores,
                )
                anomalies.append(anomaly)

            # Check for clustering of low-readiness vehicles (may indicate regional issue)
            regions_readiness = {}
            for vehicle in vehicles:
                region = vehicle.get("region", "Unknown")
                score = vehicle.get("readiness_score", 0)
                if region not in regions_readiness:
                    regions_readiness[region] = []
                regions_readiness[region].append(score)

            for region, scores in regions_readiness.items():
                if len(scores) >= 3:  # Only flag if 3+ vehicles
                    avg_regional = sum(scores) / len(scores)
                    if avg_regional < avg_readiness - 10:
                        anomaly = Anomaly(
                            anomaly_id=f"FLEET_REGIONAL_LOW_{region}",
                            type="fleet",
                            severity="medium",
                            description=f"{region} region has {len(scores)} vehicles with avg readiness {avg_regional:.0f}% (10% below fleet avg)",
                            affected_count=len(scores),
                            start_time=datetime.now(),
                            zscore=1.8,
                            confidence=0.80,
                            recommended_action=f"Investigate {region} infrastructure or vehicle selection issues. Check charging station capacity and vehicle compatibility with regional routes.",
                            historical_trend=scores,
                        )
                        anomalies.append(anomaly)

        return anomalies

    def _detect_infrastructure_anomalies(self, fleet_data: Dict[str, Any]) -> List[Anomaly]:
        """Detect charging infrastructure anomalies"""
        anomalies = []

        # Check if infrastructure is undersized
        vehicles = fleet_data.get("vehicles", [])
        ready_vehicles = len([v for v in vehicles if v.get("readiness_score", 0) > 60])

        # Assume each vehicle needs 7 kW charging; assume available is ~10 kW per vehicle currently
        current_capacity_kw = len(vehicles) * 10
        needed_capacity_kw = ready_vehicles * 7

        if needed_capacity_kw > current_capacity_kw * 0.8:  # >80% utilization
            utilization = (needed_capacity_kw / current_capacity_kw) * 100
            anomaly = Anomaly(
                anomaly_id="INFRASTRUCTURE_CAPACITY_LOW",
                type="infrastructure",
                severity="high" if utilization > 90 else "medium",
                description=f"Charging infrastructure at {utilization:.0f}% capacity utilization",
                affected_count=ready_vehicles,
                start_time=datetime.now(),
                zscore=(utilization - 60) / 15,
                confidence=0.88,
                recommended_action=f"Expand charging infrastructure by {int((needed_capacity_kw - current_capacity_kw * 0.8) / 7)} more stations. Current bottleneck will limit fleet electrification.",
                historical_trend=[utilization],
            )
            anomalies.append(anomaly)

        return anomalies

    def get_active_anomalies(self) -> List[Dict[str, Any]]:
        """Get currently active anomalies (not yet resolved)"""
        # In production, would check timestamps and mark resolved ones
        return [
            {
                "anomaly_id": a.anomaly_id,
                "type": a.type,
                "severity": a.severity,
                "description": a.description,
                "affected_count": a.affected_count,
                "start_time": a.start_time.isoformat(),
                "confidence": a.confidence,
                "recommended_action": a.recommended_action,
            }
            for a in self.anomalies_history[-10:]  # Last 10 anomalies
        ]

    def acknowledge_anomaly(self, anomaly_id: str) -> bool:
        """Mark anomaly as acknowledged"""
        # In production, would update database
        # For now, just return success
        return True

    @staticmethod
    def _calculate_std_dev(values: List[float], mean: float) -> float:
        """Calculate standard deviation"""
        if len(values) < 2:
            return 0.1
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
