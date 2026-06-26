"""
Predictive Alerting System for Proactive Risk Management

Forecasts future states and generates alerts based on predicted thresholds:
- Battery RUL forecasts
- Supply chain risk trajectories
- Fleet readiness projections
- Cost trajectory predictions
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass
class PredictiveAlert:
    """Alert based on predictive forecasting"""
    alert_id: str
    alert_type: str  # battery_ruf, supply_risk, fleet_readiness, cost
    severity: str  # critical, high, medium, low
    description: str
    days_to_critical: int
    current_value: float
    threshold_value: float
    forecast_value_90days: float
    confidence: float
    recommended_action: str
    forecast_data: List[Dict[str, Any]]  # Time series points


class PredictiveAlertingService:
    """Service for generating predictive alerts based on forecasts"""

    def __init__(self):
        self.alerts_history: List[PredictiveAlert] = []
        self.thresholds = {
            "battery_ruf_critical": 30,  # days
            "battery_ruf_high": 60,  # days
            "supply_risk": 0.75,  # score 0-1
            "fleet_readiness": 0.65,  # %
            "cost_overage": 1.20,  # 20% increase
        }

    def generate_alerts(self, fleet_data: Dict[str, Any], supply_chain_data: Dict[str, Any]) -> List[PredictiveAlert]:
        """Generate predictive alerts for all relevant metrics"""
        alerts = []

        # Battery RUL forecasts
        alerts.extend(self._forecast_battery_ruf(fleet_data))

        # Supply chain risk trajectory
        alerts.extend(self._forecast_supply_chain_risk(supply_chain_data))

        # Fleet readiness projection
        alerts.extend(self._forecast_fleet_readiness(fleet_data))

        # Cost trajectory
        alerts.extend(self._forecast_cost_trajectory(fleet_data))

        self.alerts_history.extend(alerts)
        return alerts

    def _forecast_battery_ruf(self, fleet_data: Dict[str, Any]) -> List[PredictiveAlert]:
        """Forecast battery remaining useful life and generate alerts"""
        alerts = []

        vehicles = fleet_data.get("vehicles", [])

        for vehicle in vehicles:
            battery = vehicle.get("battery", {})
            ruf_days = battery.get("ruf_days", 365)
            soh_percent = battery.get("soh_percent", 80)
            degradation_rate = battery.get("degradation_percent_per_month", 0.5)

            # Forecast 90 days
            forecast_90d = ruf_days - (degradation_rate * 3)  # 3 months
            forecast_data = self._linear_forecast(ruf_days, degradation_rate, 90)

            # Critical alert if < 30 days
            if forecast_90d < self.thresholds["battery_ruf_critical"]:
                alert = PredictiveAlert(
                    alert_id=f"BATTERY_RUL_CRITICAL_{vehicle['id']}",
                    alert_type="battery_ruf",
                    severity="critical",
                    description=f"Vehicle {vehicle['id']} battery will reach end-of-life in ~{int(forecast_90d)} days",
                    days_to_critical=int(forecast_90d),
                    current_value=ruf_days,
                    threshold_value=self.thresholds["battery_ruf_critical"],
                    forecast_value_90days=forecast_90d,
                    confidence=0.92,
                    recommended_action=f"Schedule battery replacement for vehicle {vehicle['id']} within 14 days. Procure replacement battery now to avoid lead time delays.",
                    forecast_data=forecast_data,
                )
                alerts.append(alert)

            # High alert if 30-60 days
            elif forecast_90d < self.thresholds["battery_ruf_high"]:
                alert = PredictiveAlert(
                    alert_id=f"BATTERY_RUL_HIGH_{vehicle['id']}",
                    alert_type="battery_ruf",
                    severity="high",
                    description=f"Vehicle {vehicle['id']} battery will reach end-of-life in ~{int(forecast_90d)} days",
                    days_to_critical=int(forecast_90d),
                    current_value=ruf_days,
                    threshold_value=self.thresholds["battery_ruf_high"],
                    forecast_value_90days=forecast_90d,
                    confidence=0.90,
                    recommended_action=f"Plan battery replacement for vehicle {vehicle['id']} in next 30-45 days. Begin procurement process.",
                    forecast_data=forecast_data,
                )
                alerts.append(alert)

        return alerts

    def _forecast_supply_chain_risk(self, supply_chain_data: Dict[str, Any]) -> List[PredictiveAlert]:
        """Forecast supply chain risk trajectory"""
        alerts = []

        current_risk = supply_chain_data.get("overall_risk_score", 0.5)
        risk_trend = supply_chain_data.get("risk_trend_30d", [])  # List of last 30 days

        if risk_trend and len(risk_trend) >= 14:
            # Calculate trend
            recent_7d_avg = sum(risk_trend[-7:]) / 7
            prev_7d_avg = sum(risk_trend[-14:-7]) / 7
            trend_direction = recent_7d_avg - prev_7d_avg

            # Simple linear extrapolation
            forecast_90d = current_risk + (trend_direction * 12)  # 90 days = 12 weeks
            forecast_data = self._linear_forecast(current_risk, trend_direction / 7, 90)

            # Critical if will exceed 0.85
            if forecast_90d > 0.85:
                days_to_critical = self._days_to_threshold(current_risk, trend_direction / 7, 0.85)
                alert = PredictiveAlert(
                    alert_id="SUPPLY_CHAIN_RISK_CRITICAL_FORECAST",
                    alert_type="supply_risk",
                    severity="critical",
                    description=f"Supply chain risk will reach critical level (0.85+) in ~{days_to_critical} days if current trend continues",
                    days_to_critical=days_to_critical,
                    current_value=current_risk,
                    threshold_value=0.85,
                    forecast_value_90days=forecast_90d,
                    confidence=0.78,
                    recommended_action="Activate contingency supply plans. Review geopolitical risk factors. Increase inventory buffer to 3-month supply. Negotiate backup suppliers.",
                    forecast_data=forecast_data,
                )
                alerts.append(alert)

            # High if will exceed 0.70
            elif forecast_90d > 0.70:
                days_to_critical = self._days_to_threshold(current_risk, trend_direction / 7, 0.70)
                alert = PredictiveAlert(
                    alert_id="SUPPLY_CHAIN_RISK_HIGH_FORECAST",
                    alert_type="supply_risk",
                    severity="high",
                    description=f"Supply chain risk trending toward high level (0.70+), will likely reach it in ~{days_to_critical} days",
                    days_to_critical=days_to_critical,
                    current_value=current_risk,
                    threshold_value=0.70,
                    forecast_value_90days=forecast_90d,
                    confidence=0.82,
                    recommended_action="Monitor risk factors closely. Begin supplier diversification if not already in progress. Strengthen supply chain monitoring.",
                    forecast_data=forecast_data,
                )
                alerts.append(alert)

        return alerts

    def _forecast_fleet_readiness(self, fleet_data: Dict[str, Any]) -> List[PredictiveAlert]:
        """Forecast fleet readiness trend"""
        alerts = []

        vehicles = fleet_data.get("vehicles", [])
        readiness_scores = [v.get("readiness_score", 0) for v in vehicles if "readiness_score" in v]

        if readiness_scores and len(readiness_scores) >= 5:
            avg_readiness = sum(readiness_scores) / len(readiness_scores)

            # Assume degradation rate of 1% per month
            degradation_per_month = 1.0
            forecast_90d = avg_readiness - (degradation_per_month * 3)

            forecast_data = self._linear_forecast(avg_readiness, -degradation_per_month / 30, 90)

            # Critical if will drop below 50%
            if forecast_90d < 50:
                days_to_critical = self._days_to_threshold(avg_readiness, -degradation_per_month / 30, 50)
                alert = PredictiveAlert(
                    alert_id="FLEET_READINESS_CRITICAL_FORECAST",
                    alert_type="fleet_readiness",
                    severity="high",
                    description=f"Fleet readiness will decline to {forecast_90d:.0f}% in ~{days_to_critical} days if degradation continues",
                    days_to_critical=days_to_critical,
                    current_value=avg_readiness,
                    threshold_value=50,
                    forecast_value_90days=forecast_90d,
                    confidence=0.75,
                    recommended_action="Investigate root causes of readiness decline. Check vehicle compatibility with new routes, charging infrastructure capacity, or maintenance issues.",
                    forecast_data=forecast_data,
                )
                alerts.append(alert)

        return alerts

    def _forecast_cost_trajectory(self, fleet_data: Dict[str, Any]) -> List[PredictiveAlert]:
        """Forecast electrification cost trajectory"""
        alerts = []

        # Base cost assumption
        base_cost_per_vehicle = 15_00_000  # ₹15 lakhs
        total_vehicles = len(fleet_data.get("vehicles", []))
        budget_baseline = base_cost_per_vehicle * total_vehicles

        # Cost trend (assume 2% increase per month due to battery price inflation)
        monthly_cost_increase_percent = 0.02
        forecast_cost_90d = budget_baseline * ((1 + monthly_cost_increase_percent) ** 3)
        cost_overrun_percent = (forecast_cost_90d - budget_baseline) / budget_baseline

        forecast_data = self._cost_forecast(budget_baseline, monthly_cost_increase_percent, 90)

        # Alert if cost will overrun by > 15%
        if cost_overrun_percent > 0.15:
            alert = PredictiveAlert(
                alert_id="COST_TRAJECTORY_ALERT",
                alert_type="cost",
                severity="high",
                description=f"Electrification cost will increase by {cost_overrun_percent * 100:.0f}% ({cost_overrun_percent * budget_baseline / 1_00_00_000:.1f} Cr) in 90 days",
                days_to_critical=90,
                current_value=budget_baseline,
                threshold_value=budget_baseline * 1.15,
                forecast_value_90days=forecast_cost_90d,
                confidence=0.70,
                recommended_action=f"Lock in battery prices NOW through long-term contracts. Cost will increase ₹{int(cost_overrun_percent * budget_baseline / 1_00_00_000)} Cr if delays occur. Accelerate procurement timeline.",
                forecast_data=forecast_data,
            )
            alerts.append(alert)

        return alerts

    def get_upcoming_alerts(self) -> List[Dict[str, Any]]:
        """Get forecasted alerts ranked by days to critical"""
        upcoming = [
            {
                "alert_id": a.alert_id,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "description": a.description,
                "days_to_critical": a.days_to_critical,
                "current_value": a.current_value,
                "forecast_90d": a.forecast_value_90days,
                "confidence": a.confidence,
                "recommended_action": a.recommended_action,
            }
            for a in self.alerts_history
        ]
        # Sort by days to critical
        return sorted(upcoming, key=lambda x: x["days_to_critical"])

    def set_alert_threshold(self, metric: str, value: float) -> bool:
        """Customize alert thresholds"""
        if metric in self.thresholds:
            self.thresholds[metric] = value
            return True
        return False

    @staticmethod
    def _linear_forecast(current_value: float, daily_change: float, days: int) -> List[Dict[str, Any]]:
        """Generate linear forecast data points"""
        forecast = []
        for day in range(0, days + 1, 10):  # Data points every 10 days
            value = current_value + (daily_change * day)
            forecast.append({
                "day": day,
                "date": (datetime.now() + timedelta(days=day)).isoformat(),
                "value": max(0, value),  # Don't go below 0
            })
        return forecast

    @staticmethod
    def _cost_forecast(baseline: float, monthly_increase: float, days: int) -> List[Dict[str, Any]]:
        """Generate cost forecast with compounding"""
        forecast = []
        for day in range(0, days + 1, 10):
            months = day / 30
            value = baseline * ((1 + monthly_increase) ** months)
            forecast.append({
                "day": day,
                "date": (datetime.now() + timedelta(days=day)).isoformat(),
                "value": value,
            })
        return forecast

    @staticmethod
    def _days_to_threshold(current_value: float, daily_change: float, threshold: float) -> int:
        """Calculate days until threshold is crossed"""
        if daily_change == 0:
            return 999
        days = (threshold - current_value) / daily_change
        return max(1, int(days))
