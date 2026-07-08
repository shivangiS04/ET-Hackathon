"""
Manufacturing Quality Intelligence Service
Detects quality drift, traces defects, provides SPC metrics, and predicts failures
Uses synthetic data for all operations - no real SCADA/BMS integration required
"""

import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from typing import Dict, List, Any


class ManufacturingQualityService:
    """AI-powered quality intelligence for EV battery manufacturing"""
    
    def __init__(self):
        """Initialize the quality service with trained models"""
        self.isolation_forest = IsolationForest(
            contamination=0.05,
            random_state=42,
            n_estimators=100
        )
        # Pre-train on synthetic baseline data
        self._train_baseline_model()
    
    def _train_baseline_model(self):
        """Train IsolationForest on baseline synthetic data"""
        baseline_data = []
        np.random.seed(42)
        
        # Generate 1000 baseline samples (normal manufacturing conditions)
        for _ in range(1000):
            baseline_data.append([
                np.random.normal(4.2, 0.05),      # voltage_mean
                np.random.normal(0.03, 0.01),    # voltage_std
                np.random.normal(35, 2),          # temperature_mean
                np.random.normal(3, 0.5),         # temperature_std
                np.random.normal(500, 50),        # cycle_count
                np.random.normal(0.001, 0.0002)  # capacity_fade_rate
            ])
        
        self.isolation_forest.fit(np.array(baseline_data))
    
    def detect_quality_drift(self, process_params: dict) -> dict:
        """
        Detect quality drift using Isolation Forest and SPC principles
        
        Args:
            process_params: dict with keys:
                - voltage_mean (float): Average cell voltage
                - voltage_std (float): Voltage standard deviation
                - temperature_mean (float): Average temperature
                - temperature_std (float): Temperature std dev
                - cycle_count (int): Number of cycles
                - capacity_fade_rate (float): Capacity degradation rate
        
        Returns:
            dict with quality metrics and recommendations
        """
        # Extract and validate parameters
        params_array = np.array([[
            process_params.get("voltage_mean", 4.2),
            process_params.get("voltage_std", 0.03),
            process_params.get("temperature_mean", 35),
            process_params.get("temperature_std", 3),
            process_params.get("cycle_count", 500),
            process_params.get("capacity_fade_rate", 0.001)
        ]])
        
        # Detect anomalies (-1 = anomaly, 1 = normal)
        anomaly_prediction = self.isolation_forest.predict(params_array)[0]
        anomaly_score = self.isolation_forest.score_samples(params_array)[0]
        
        # Convert anomaly score to defect risk (0-1, where 1 = highest risk)
        # Anomaly scores are typically negative; map to 0-1 range
        defect_risk_score = float(1 / (1 + np.exp(anomaly_score + 2)))  # Sigmoid mapping
        defect_risk_score = np.clip(defect_risk_score, 0, 1)
        
        # Determine severity based on risk score
        if defect_risk_score > 0.8:
            severity = "critical"
        elif defect_risk_score > 0.6:
            severity = "high"
        elif defect_risk_score > 0.3:
            severity = "medium"
        else:
            severity = "low"
        
        # Control chart signal (SPC)
        voltage_mean = process_params.get("voltage_mean", 4.2)
        temperature_mean = process_params.get("temperature_mean", 35)
        
        # UCL/LCL based on 3-sigma rule
        voltage_ucl = 4.35
        voltage_lcl = 4.05
        temp_ucl = 42
        temp_lcl = 28
        
        if (voltage_lcl <= voltage_mean <= voltage_ucl and 
            temp_lcl <= temperature_mean <= temp_ucl and
            defect_risk_score < 0.5):
            control_chart_signal = "IN_CONTROL"
        else:
            control_chart_signal = "OUT_OF_CONTROL"
        
        # Generate recommendations
        recommendations = {
            "low": "Continue normal production. Monitor for drift.",
            "medium": "Review process parameters. Schedule maintenance check.",
            "high": "Hold production lot for QA inspection. Investigate root cause.",
            "critical": "STOP production. Quarantine all units. Initiate RCA immediately."
        }
        
        recommended_action = recommendations.get(severity, "Unknown action")
        
        # Confidence is based on anomaly certainty
        confidence = float(abs(anomaly_score) / 2 + 0.5)  # Map to 0.5-1.0
        confidence = np.clip(confidence, 0.5, 1.0)
        
        return {
            "quality_drift_detected": anomaly_prediction == -1,
            "defect_risk_score": round(defect_risk_score, 3),
            "severity": severity,
            "recommended_action": recommended_action,
            "control_chart_signal": control_chart_signal,
            "confidence": round(confidence, 3),
            "timestamp": datetime.utcnow().isoformat(),
            "process_summary": {
                "voltage_status": "OK" if voltage_lcl <= voltage_mean <= voltage_ucl else "OUT_OF_SPEC",
                "temperature_status": "OK" if temp_lcl <= temperature_mean <= temp_ucl else "OUT_OF_SPEC",
                "capacity_fade_rate": process_params.get("capacity_fade_rate", 0.001)
            }
        }
    
    def trace_defect_source(self, cell_id: str) -> dict:
        """
        Trace defect chain from cell through pack to vehicle
        Simulates complete traceability chain
        
        Args:
            cell_id: Cell identifier (e.g., "CELL_001_A1")
        
        Returns:
            dict with complete traceability information
        """
        # Generate deterministic but realistic values based on cell_id
        seed = hash(cell_id) % (2**32)
        np.random.seed(seed)
        
        # Parse cell_id for batch and position
        parts = cell_id.split("_")
        batch_num = int(parts[1]) if len(parts) > 1 else 1
        position = parts[2] if len(parts) > 2 else "A1"
        
        # Cell -> Pack mapping (48 cells per pack)
        pack_num = (int(parts[1]) // 48) + 1
        pack_id = f"PACK_{pack_num:04d}_{chr(65 + (batch_num % 26))}"
        
        # Pack -> Vehicle mapping (5 packs per vehicle)
        vehicle_num = (pack_num // 5) + 1
        vehicle_id = f"VEH_{vehicle_num:05d}"
        
        # Manufacturing metadata
        manufacturing_date = (datetime.utcnow() - timedelta(days=np.random.randint(5, 90))).isoformat()
        batch_number = f"BATCH_2026_Q{((batch_num // 100) % 4) + 1}_{batch_num % 100:03d}"
        
        # Supplier rotation (3 main suppliers)
        suppliers = ["LithiumCorp", "CobaltMin", "NickelTech"]
        supplier_id = suppliers[batch_num % 3]
        
        # Simulate defect chain if any quality issues
        defect_chain = []
        np.random.seed(seed + 1)
        
        if np.random.random() < 0.15:  # 15% defect rate in simulation
            defects = [
                {"stage": "cell_manufacturing", "issue": "micro-crack", "severity": "medium"},
                {"stage": "pack_assembly", "issue": "misalignment", "severity": "low"},
                {"stage": "vehicle_integration", "issue": "loose_connector", "severity": "medium"}
            ]
            defect_chain = [d for d in defects if np.random.random() < 0.3]
        
        # Affected vehicles (if defect found)
        affected_vehicles = []
        if defect_chain:
            # Typically 1-3 vehicles affected per defect in same pack
            num_affected = np.random.randint(1, 4)
            affected_vehicles = [f"VEH_{(vehicle_num + i):05d}" for i in range(num_affected)]
        
        return {
            "cell_id": cell_id,
            "pack_id": pack_id,
            "vehicle_id": vehicle_id,
            "manufacturing_date": manufacturing_date,
            "batch_number": batch_number,
            "supplier_id": supplier_id,
            "defect_chain": defect_chain,
            "affected_vehicles": affected_vehicles,
            "traceability_status": "COMPLETE",
            "quality_score": round(1.0 - (len(defect_chain) * 0.15), 2),
            "recommendation": (
                "HOLD FOR INSPECTION" if defect_chain 
                else "CLEAR FOR ASSEMBLY"
            )
        }
    
    def get_spc_metrics(self, line_id: str) -> dict:
        """
        Get Statistical Process Control metrics for a production line
        
        Args:
            line_id: Production line identifier (e.g., "LINE_01")
        
        Returns:
            dict with SPC metrics and control chart data
        """
        # Deterministic generation based on line_id
        seed = hash(line_id) % (2**32)
        np.random.seed(seed)
        
        # Generate 10 recent readings (last 10 batches)
        last_10_readings = []
        mean_voltage = 4.2
        std_dev = 0.04
        
        for i in range(10):
            reading = np.random.normal(mean_voltage, std_dev)
            reading = np.clip(reading, 3.9, 4.5)  # Realistic bounds
            last_10_readings.append(round(reading, 4))
        
        mean = round(np.mean(last_10_readings), 4)
        stdev = round(np.std(last_10_readings), 4)
        
        # Calculate SPC indices
        spec_upper = 4.35
        spec_lower = 4.05
        
        # Cpk = min((USL - mean) / (3*sigma), (mean - LSL) / (3*sigma))
        cpk = min(
            (spec_upper - mean) / (3 * stdev) if stdev > 0 else 0,
            (mean - spec_lower) / (3 * stdev) if stdev > 0 else 0
        )
        cpk = max(cpk, 0)  # Cpk cannot be negative
        
        # Cp = (USL - LSL) / (6*sigma)
        cp = (spec_upper - spec_lower) / (6 * stdev) if stdev > 0 else 0
        
        # Process capability (Cpk > 1.33 is good manufacturing practice)
        if cpk > 1.33:
            defects_per_million = int(np.random.randint(50, 200))
        elif cpk > 1.0:
            defects_per_million = int(np.random.randint(500, 2000))
        else:
            defects_per_million = int(np.random.randint(5000, 50000))
        
        # Yield rate based on defects
        yield_rate = round(1.0 - (defects_per_million / 1_000_000), 4)
        
        # Control limits (UCL/LCL based on 3-sigma)
        ucl = round(mean + 3 * stdev, 4)
        lcl = round(mean - 3 * stdev, 4)
        
        # Check for control chart signals (Western Electric rules)
        out_of_control = any(
            r > ucl or r < lcl 
            for r in last_10_readings
        )
        
        return {
            "line_id": line_id,
            "cpk": round(cpk, 3),  # Process capability index
            "cp": round(cp, 3),    # Process capability (without centering)
            "defects_per_million": defects_per_million,
            "yield_rate": yield_rate,
            "last_10_readings": last_10_readings,
            "ucl": ucl,  # Upper Control Limit
            "lcl": lcl,  # Lower Control Limit
            "mean": mean,
            "std_dev": stdev,
            "control_status": "OUT_OF_CONTROL" if out_of_control else "IN_CONTROL",
            "capability_rating": (
                "EXCELLENT" if cpk > 1.67 else
                "GOOD" if cpk > 1.33 else
                "ADEQUATE" if cpk > 1.0 else
                "POOR"
            ),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def predict_failure_likelihood(self, vehicle_id: str, cell_data: dict) -> dict:
        """
        Predict battery failure likelihood based on cell characteristics
        
        Args:
            vehicle_id: Vehicle identifier
            cell_data: dict with cell performance metrics
                - soh (float): State of Health (0-100)
                - cycle_count (int): Total charge cycles
                - temperature_history_mean (float): Average temperature
                - voltage_variance (float): Voltage stability
        
        Returns:
            dict with failure prediction and recommendations
        """
        seed = hash(vehicle_id) % (2**32)
        np.random.seed(seed)
        
        # Extract parameters
        soh = cell_data.get("soh", 85)
        cycle_count = cell_data.get("cycle_count", 500)
        temp_mean = cell_data.get("temperature_history_mean", 35)
        voltage_variance = cell_data.get("voltage_variance", 0.01)
        
        # Failure likelihood factors (0-1 scale)
        soh_factor = max(0, 1.0 - (soh / 100))  # Higher SOH = lower risk
        cycle_factor = min(1.0, cycle_count / 2000)  # Risk increases with cycles
        temperature_factor = abs(temp_mean - 25) / 50  # Risk increases away from 25C
        variance_factor = voltage_variance * 50  # High variance = high risk
        
        # Weighted combination
        failure_probability = round(
            0.3 * soh_factor + 
            0.3 * cycle_factor + 
            0.2 * temperature_factor + 
            0.2 * variance_factor,
            3
        )
        failure_probability = np.clip(failure_probability, 0, 1)
        
        # Estimate days to failure (exponential decay model)
        if failure_probability < 0.1:
            estimated_days = np.random.randint(700, 1500)  # > 2 years
        elif failure_probability < 0.3:
            estimated_days = np.random.randint(300, 700)
        elif failure_probability < 0.6:
            estimated_days = np.random.randint(100, 300)
        else:
            estimated_days = np.random.randint(30, 100)
        
        # Contributing factors
        contributing_factors = []
        
        if soh < 80:
            contributing_factors.append({
                "factor": "Low State of Health",
                "weight": 0.3,
                "current_value": soh,
                "threshold": 80
            })
        
        if cycle_count > 1500:
            contributing_factors.append({
                "factor": "High Cycle Count",
                "weight": 0.3,
                "current_value": cycle_count,
                "threshold": 1500
            })
        
        if abs(temp_mean - 25) > 15:
            contributing_factors.append({
                "factor": "Thermal Stress",
                "weight": 0.2,
                "current_value": round(temp_mean, 1),
                "threshold": 25
            })
        
        if voltage_variance > 0.05:
            contributing_factors.append({
                "factor": "Voltage Instability",
                "weight": 0.2,
                "current_value": round(voltage_variance, 4),
                "threshold": 0.05
            })
        
        # Maintenance recommendations
        if failure_probability > 0.7:
            recommended_maintenance = "IMMEDIATE: Schedule replacement within 30 days"
        elif failure_probability > 0.4:
            recommended_maintenance = "URGENT: Schedule replacement within 60 days"
        elif failure_probability > 0.2:
            recommended_maintenance = "PLANNED: Include in next maintenance cycle (6 months)"
        else:
            recommended_maintenance = "PREVENTIVE: Monitor for changes. Check every 6 months"
        
        return {
            "vehicle_id": vehicle_id,
            "failure_probability": failure_probability,
            "failure_percentage": round(failure_probability * 100, 1),
            "estimated_days_to_failure": estimated_days,
            "estimated_months_to_failure": round(estimated_days / 30, 1),
            "contributing_factors": contributing_factors,
            "recommended_maintenance": recommended_maintenance,
            "urgency_level": (
                "CRITICAL" if failure_probability > 0.7 else
                "HIGH" if failure_probability > 0.4 else
                "MEDIUM" if failure_probability > 0.2 else
                "LOW"
            ),
            "confidence": round(0.85 + (np.random.random() * 0.1), 3),
            "timestamp": datetime.utcnow().isoformat()
        }
