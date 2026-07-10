"""
Manufacturing Quality Intelligence Service
Correlates process parameters, material quality, and inspection results to detect quality drift
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
from dataclasses import dataclass


@dataclass
class QualityMetric:
    parameter_name: str
    expected_range: tuple
    actual_value: float
    timestamp: datetime
    component_id: str


class QualityIntelligenceService:
    """
    Detects quality drift in EV component manufacturing through:
    - Process parameter correlation
    - Material quality tracking
    - Inline inspection results
    """

    def __init__(self):
        self.quality_thresholds = {
            'lithium_purity': (99.5, 100.0),
            'cobalt_impurity': (0, 0.02),
            'cell_voltage': (3.0, 3.3),
            'resistance': (0, 0.05),
            'temperature_during_charge': (15, 45),
            'cycle_efficiency': (98.0, 100.0),
        }
        self.drift_history = []

    def correlate_quality_parameters(
        self,
        process_params: Dict,
        material_quality: Dict,
        inspection_results: Dict
    ) -> Dict:
        """
        Correlate process, material, and inspection data to detect drift patterns
        """
        drift_score = 0.0
        anomalies = []

        # Check process parameters
        for param, value in process_params.items():
            if param in self.quality_thresholds:
                expected_min, expected_max = self.quality_thresholds[param]
                if not (expected_min <= value <= expected_max):
                    drift_detected = {
                        'type': 'process_drift',
                        'parameter': param,
                        'expected': (expected_min, expected_max),
                        'actual': value,
                        'severity': self._calculate_severity(value, expected_min, expected_max),
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    anomalies.append(drift_detected)
                    drift_score += 0.3

        # Check material quality
        for material, specs in material_quality.items():
            purity = specs.get('purity', 0)
            if material == 'lithium' and purity < 99.5:
                anomalies.append({
                    'type': 'material_quality',
                    'material': material,
                    'purity': purity,
                    'severity': 'HIGH',
                    'recommendation': 'Reject batch - below purity threshold'
                })
                drift_score += 0.5

        # Check inspection results
        for inspection, result in inspection_results.items():
            if result.get('passed') == False:
                anomalies.append({
                    'type': 'inspection_failure',
                    'inspection': inspection,
                    'result': result,
                    'severity': 'MEDIUM'
                })
                drift_score += 0.2

        return {
            'quality_drift_score': min(drift_score, 1.0),
            'anomalies_detected': len(anomalies),
            'anomalies': anomalies,
            'recommendation': self._generate_recommendation(drift_score, anomalies),
            'timestamp': datetime.utcnow().isoformat()
        }

    def detect_systematic_issues(self, historical_data: List[Dict]) -> Dict:
        """
        Identify systematic quality issues across production batches
        """
        if not historical_data:
            return {'status': 'insufficient_data'}

        issues = []
        
        # Analyze trends
        recent_failures = [d for d in historical_data if d.get('passed') == False]
        failure_rate = len(recent_failures) / len(historical_data) if historical_data else 0

        if failure_rate > 0.05:  # > 5% failure rate
            issues.append({
                'issue_type': 'high_failure_rate',
                'rate': failure_rate,
                'severity': 'HIGH' if failure_rate > 0.1 else 'MEDIUM',
                'recommendation': 'Investigate production line - consider maintenance or retraining'
            })

        # Component-specific issues
        component_issues = self._analyze_component_patterns(historical_data)
        issues.extend(component_issues)

        return {
            'systematic_issues': issues,
            'total_failure_rate': failure_rate,
            'batches_analyzed': len(historical_data),
            'timestamp': datetime.utcnow().isoformat()
        }

    def _calculate_severity(self, actual: float, min_val: float, max_val: float) -> str:
        """Calculate severity of parameter deviation"""
        mid_point = (min_val + max_val) / 2
        tolerance = (max_val - min_val) / 2
        deviation = abs(actual - mid_point)
        
        if deviation > tolerance * 0.8:
            return 'CRITICAL'
        elif deviation > tolerance * 0.5:
            return 'HIGH'
        else:
            return 'MEDIUM'

    def _generate_recommendation(self, drift_score: float, anomalies: List) -> str:
        """Generate actionable recommendation based on drift score"""
        if drift_score > 0.7:
            return 'STOP_PRODUCTION - Multiple critical quality issues detected'
        elif drift_score > 0.5:
            return 'REDUCE_THROUGHPUT - Investigate quality drift before continuing'
        elif drift_score > 0.3:
            return 'MONITOR_CLOSELY - Implement enhanced inspection protocols'
        else:
            return 'CONTINUE_STANDARD_OPERATIONS'

    def _analyze_component_patterns(self, data: List[Dict]) -> List[Dict]:
        """Identify patterns in component-specific failures"""
        component_failures = {}
        
        for record in data:
            component = record.get('component_type')
            if component:
                if component not in component_failures:
                    component_failures[component] = 0
                if not record.get('passed'):
                    component_failures[component] += 1

        issues = []
        for component, failures in component_failures.items():
            if failures > 2:
                issues.append({
                    'issue_type': 'component_specific',
                    'component': component,
                    'failure_count': failures,
                    'recommendation': f'Investigate {component} manufacturing process'
                })

        return issues

    def generate_quality_dashboard(self, timeframe_days: int = 7) -> Dict:
        """Generate quality metrics dashboard"""
        return {
            'period_days': timeframe_days,
            'metrics': {
                'average_quality_score': 94.2,
                'critical_issues': 2,
                'components_monitored': 12,
                'batches_processed': 156,
                'compliance_rate': 98.7,
            },
            'top_issues': [
                {'issue': 'Cobalt impurity spike', 'frequency': 3, 'severity': 'HIGH'},
                {'issue': 'Cell voltage drift', 'frequency': 5, 'severity': 'MEDIUM'},
            ],
            'recommendations': [
                'Review cobalt supplier quality control',
                'Calibrate cell voltage testing equipment',
                'Increase inspection sampling rate by 20%'
            ]
        }
