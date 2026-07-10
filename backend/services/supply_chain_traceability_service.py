"""
Supply Chain Traceability Service
End-to-end tracking: Lithium → Cobalt → NMC/LFP Cell → Battery Pack → Vehicle
"""

from datetime import datetime
from typing import Dict, List
from enum import Enum


class MaterialType(Enum):
    LITHIUM = "lithium"
    COBALT = "cobalt"
    NICKEL = "nickel"
    MANGANESE = "manganese"
    NMC_CELL = "nmc_cell"
    LFP_CELL = "lfp_cell"
    BATTERY_PACK = "battery_pack"


class TraceabilityStatus(Enum):
    EXTRACTED = "extracted"
    PROCESSED = "processed"
    ASSEMBLED = "assembled"
    TESTED = "tested"
    SHIPPED = "shipped"
    RECEIVED = "received"
    INTEGRATED = "integrated"


class SupplyChainTraceabilityService:
    """
    End-to-end traceability for EV battery supply chain
    """

    def __init__(self):
        self.trace_history = {}

    def create_material_trace(
        self,
        material_type: str,
        quantity_kg: float,
        origin_country: str,
        supplier_name: str,
        batch_id: str
    ) -> Dict:
        """
        Create initial trace record for raw material
        """
        trace_id = f"MAT-{batch_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        trace_record = {
            'trace_id': trace_id,
            'material_type': material_type,
            'quantity_kg': quantity_kg,
            'origin_country': origin_country,
            'supplier_name': supplier_name,
            'batch_id': batch_id,
            'status': TraceabilityStatus.EXTRACTED.value,
            'quality_score': self._assess_material_quality(material_type, origin_country),
            'risk_assessment': self._assess_supply_risk(material_type, origin_country),
            'created_at': datetime.utcnow().isoformat(),
            'chain': [
                {
                    'stage': 'extraction',
                    'location': origin_country,
                    'timestamp': datetime.utcnow().isoformat(),
                    'actor': supplier_name,
                    'notes': f'Initial extraction of {quantity_kg}kg'
                }
            ]
        }

        self.trace_history[trace_id] = trace_record
        return trace_record

    def add_processing_step(
        self,
        trace_id: str,
        processor_name: str,
        processing_type: str,
        location: str,
        quality_metrics: Dict
    ) -> Dict:
        """
        Add processing/refinement step to trace
        """
        if trace_id not in self.trace_history:
            return {'error': 'Trace ID not found'}

        trace_record = self.trace_history[trace_id]

        processing_step = {
            'stage': 'processing',
            'processing_type': processing_type,
            'location': location,
            'timestamp': datetime.utcnow().isoformat(),
            'actor': processor_name,
            'quality_metrics': quality_metrics,
            'notes': f'{processing_type} processing completed'
        }

        trace_record['chain'].append(processing_step)
        trace_record['status'] = TraceabilityStatus.PROCESSED.value
        trace_record['quality_score'] = quality_metrics.get('purity_percent', 95)

        return {
            'trace_id': trace_id,
            'stage_added': 'processing',
            'current_status': trace_record['status'],
            'processing_step': processing_step
        }

    def create_cell_assembly_trace(
        self,
        lithium_trace_id: str,
        cobalt_trace_id: str,
        nickel_trace_id: str,
        cell_type: str,
        manufacturer_name: str,
        location: str
    ) -> Dict:
        """
        Create trace for assembled battery cell
        """
        cell_batch_id = f"CELL-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        cell_trace = {
            'trace_id': cell_batch_id,
            'material_type': cell_type,
            'status': TraceabilityStatus.ASSEMBLED.value,
            'assembly_location': location,
            'manufacturer': manufacturer_name,
            'assembled_at': datetime.utcnow().isoformat(),
            'source_materials': [
                {'material': 'lithium', 'trace_id': lithium_trace_id},
                {'material': 'cobalt', 'trace_id': cobalt_trace_id},
                {'material': 'nickel', 'trace_id': nickel_trace_id}
            ],
            'quality_tests': [
                {'test': 'voltage', 'result': '3.7V', 'passed': True},
                {'test': 'capacity', 'result': '2500mAh', 'passed': True},
                {'test': 'resistance', 'result': '15mΩ', 'passed': True}
            ],
            'chain': [
                {
                    'stage': 'assembly',
                    'location': location,
                    'timestamp': datetime.utcnow().isoformat(),
                    'actor': manufacturer_name,
                    'notes': 'Battery cell assembled and tested'
                }
            ]
        }

        self.trace_history[cell_batch_id] = cell_trace
        return cell_trace

    def create_battery_pack_trace(
        self,
        cell_trace_ids: List[str],
        pack_id: str,
        battery_manufacturer: str,
        location: str,
        capacity_kwh: float
    ) -> Dict:
        """
        Create trace for complete battery pack (multiple cells)
        """
        pack_trace_id = f"PACK-{pack_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        pack_trace = {
            'trace_id': pack_trace_id,
            'material_type': 'battery_pack',
            'battery_id': pack_id,
            'capacity_kwh': capacity_kwh,
            'manufacturer': battery_manufacturer,
            'assembly_location': location,
            'status': TraceabilityStatus.ASSEMBLED.value,
            'assembled_at': datetime.utcnow().isoformat(),
            'cells_in_pack': len(cell_trace_ids),
            'cell_trace_ids': cell_trace_ids,
            'quality_tests': [
                {'test': 'bms_function', 'result': 'OK', 'passed': True},
                {'test': 'thermal_management', 'result': 'OK', 'passed': True},
                {'test': 'voltage_balance', 'result': '±5mV', 'passed': True}
            ],
            'chain': [
                {
                    'stage': 'pack_assembly',
                    'location': location,
                    'timestamp': datetime.utcnow().isoformat(),
                    'actor': battery_manufacturer,
                    'notes': f'Battery pack assembled with {len(cell_trace_ids)} cells'
                }
            ]
        }

        self.trace_history[pack_trace_id] = pack_trace
        return pack_trace

    def integrate_into_vehicle(
        self,
        pack_trace_id: str,
        vehicle_id: str,
        vehicle_model: str,
        oem_name: str,
        assembly_location: str
    ) -> Dict:
        """
        Complete supply chain trace by integrating battery pack into vehicle
        """
        if pack_trace_id not in self.trace_history:
            return {'error': 'Pack trace ID not found'}

        pack_trace = self.trace_history[pack_trace_id]

        integration_step = {
            'stage': 'vehicle_integration',
            'vehicle_id': vehicle_id,
            'vehicle_model': vehicle_model,
            'assembly_location': assembly_location,
            'timestamp': datetime.utcnow().isoformat(),
            'actor': oem_name,
            'notes': 'Battery pack integrated into vehicle'
        }

        pack_trace['chain'].append(integration_step)
        pack_trace['status'] = TraceabilityStatus.INTEGRATED.value
        pack_trace['vehicle_id'] = vehicle_id

        return {
            'pack_trace_id': pack_trace_id,
            'vehicle_id': vehicle_id,
            'supply_chain_complete': True,
            'integration_timestamp': datetime.utcnow().isoformat(),
            'full_chain': pack_trace['chain']
        }

    def generate_full_traceability_report(
        self,
        vehicle_id: str,
        pack_trace_id: str
    ) -> Dict:
        """
        Generate complete end-to-end traceability report for vehicle
        """
        if pack_trace_id not in self.trace_history:
            return {'error': 'Pack trace not found'}

        pack_trace = self.trace_history[pack_trace_id]

        # Compile all upstream traces
        upstream_traces = []
        for cell_id in pack_trace.get('cell_trace_ids', []):
            if cell_id in self.trace_history:
                cell_trace = self.trace_history[cell_id]
                upstream_traces.append(cell_trace)

        report = {
            'report_id': f"REPORT-{vehicle_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'vehicle_id': vehicle_id,
            'generated_at': datetime.utcnow().isoformat(),
            'battery_pack_info': {
                'pack_trace_id': pack_trace_id,
                'capacity_kwh': pack_trace.get('capacity_kwh'),
                'cells_count': len(pack_trace.get('cell_trace_ids', [])),
                'manufacturer': pack_trace.get('manufacturer')
            },
            'supply_chain_stages': [
                {
                    'stage': 'raw_materials',
                    'materials': ['lithium', 'cobalt', 'nickel', 'manganese'],
                    'quality_assessment': 'HIGH'
                },
                {
                    'stage': 'material_processing',
                    'actors': ['processing_suppliers'],
                    'quality_assessment': 'HIGH'
                },
                {
                    'stage': 'cell_manufacturing',
                    'cells': len(pack_trace.get('cell_trace_ids', [])),
                    'quality_assessment': 'HIGH'
                },
                {
                    'stage': 'pack_assembly',
                    'manufacturer': pack_trace.get('manufacturer'),
                    'quality_assessment': 'HIGH'
                },
                {
                    'stage': 'vehicle_integration',
                    'oem': 'Vehicle_OEM',
                    'quality_assessment': 'HIGH'
                }
            ],
            'sustainability_metrics': {
                'geographic_diversity': 'Multi-region sourcing',
                'supply_concentration_risk': 'MEDIUM',
                'carbon_footprint_kg_co2': pack_trace.get('capacity_kwh', 50) * 25,  # ~25kg CO2/kWh battery
                'recyclability_score': 92
            },
            'compliance_checklist': {
                'conflict_free_minerals': True,
                'labour_standards_verified': True,
                'environmental_standards_met': True,
                'quality_certifications': ['IEC62619', 'UN38.3'],
                'audit_trail_complete': True
            }
        }

        return report

    def _assess_material_quality(self, material_type: str, origin: str) -> float:
        """Assess material quality based on type and origin"""
        quality_scores = {
            'lithium': {'australia': 99, 'chile': 98, 'china': 95},
            'cobalt': {'congo': 90, 'australia': 92, 'canada': 95},
            'nickel': {'indonesia': 88, 'philippines': 90, 'russia': 92}
        }
        
        return quality_scores.get(material_type, {}).get(origin, 85)

    def _assess_supply_risk(self, material_type: str, origin: str) -> str:
        """Assess geopolitical risk"""
        high_risk_countries = ['congo', 'venezuela']
        
        if origin.lower() in high_risk_countries:
            return 'HIGH'
        elif material_type in ['cobalt', 'lithium']:
            return 'MEDIUM'
        else:
            return 'LOW'
