"""
Enhanced Carbon Tracking Service
Quantifies Scope 1 and 3 emission reductions per route and asset class
"""

from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class EmissionFactors:
    diesel_kg_co2_per_liter: float = 2.68
    electricity_kg_co2_per_kwh: float = 0.615  # India average grid
    ev_kwh_per_km: float = 0.18
    diesel_liter_per_km: float = 0.08


class CarbonTrackingService:
    """
    Tracks carbon emissions across fleet electrification
    - Scope 1: Direct emissions from vehicles
    - Scope 3: Upstream emissions (fuel production, electricity generation)
    """

    def __init__(self):
        self.emission_factors = EmissionFactors()
        self.routes_tracked = {}

    def calculate_scope1_emissions(
        self,
        vehicle_type: str,
        distance_km: float,
        fuel_consumed: float = None
    ) -> Dict:
        """
        Scope 1: Direct CO2 emissions from vehicle operation
        """
        if vehicle_type == 'diesel':
            # Diesel: 2.68 kg CO2 per liter
            if not fuel_consumed:
                fuel_consumed = distance_km * self.emission_factors.diesel_liter_per_km
            emissions_kg_co2 = fuel_consumed * self.emission_factors.diesel_kg_co2_per_liter
        else:  # electric
            # EV: 0 direct emissions (battery charged externally)
            emissions_kg_co2 = 0.0

        return {
            'vehicle_type': vehicle_type,
            'distance_km': distance_km,
            'fuel_consumed': fuel_consumed,
            'scope1_emissions_kg_co2': emissions_kg_co2,
            'emissions_type': 'Scope 1 (Direct)'
        }

    def calculate_scope3_emissions(
        self,
        vehicle_type: str,
        distance_km: float
    ) -> Dict:
        """
        Scope 3: Upstream emissions from fuel/energy production
        """
        if vehicle_type == 'diesel':
            # Diesel refining and distribution: ~15% of combustion emissions
            fuel_consumed = distance_km * self.emission_factors.diesel_liter_per_km
            combustion_emissions = fuel_consumed * self.emission_factors.diesel_kg_co2_per_liter
            scope3_emissions_kg_co2 = combustion_emissions * 0.15
        else:  # electric
            # Electricity generation and transmission losses
            energy_consumed_kwh = distance_km * self.emission_factors.ev_kwh_per_km
            scope3_emissions_kg_co2 = energy_consumed_kwh * self.emission_factors.electricity_kg_co2_per_kwh

        return {
            'vehicle_type': vehicle_type,
            'distance_km': distance_km,
            'scope3_emissions_kg_co2': scope3_emissions_kg_co2,
            'emissions_type': 'Scope 3 (Indirect)'
        }

    def calculate_total_emissions(
        self,
        vehicle_type: str,
        distance_km: float,
        fuel_consumed: float = None
    ) -> Dict:
        """
        Calculate total emissions (Scope 1 + Scope 3)
        """
        scope1 = self.calculate_scope1_emissions(vehicle_type, distance_km, fuel_consumed)
        scope3 = self.calculate_scope3_emissions(vehicle_type, distance_km)

        total_emissions = scope1['scope1_emissions_kg_co2'] + scope3['scope3_emissions_kg_co2']

        return {
            'vehicle_type': vehicle_type,
            'distance_km': distance_km,
            'scope1_kg_co2': scope1['scope1_emissions_kg_co2'],
            'scope3_kg_co2': scope3['scope3_emissions_kg_co2'],
            'total_emissions_kg_co2': total_emissions,
            'total_emissions_metric_tons': total_emissions / 1000,
            'timestamp': datetime.utcnow().isoformat()
        }

    def calculate_emission_reduction(
        self,
        diesel_distance_km: float,
        ev_distance_km: float
    ) -> Dict:
        """
        Calculate emission reductions from switching diesel to EV
        """
        diesel_emissions = self.calculate_total_emissions('diesel', diesel_distance_km)
        ev_emissions = self.calculate_total_emissions('electric', ev_distance_km)

        reduction_kg_co2 = diesel_emissions['total_emissions_kg_co2'] - ev_emissions['total_emissions_kg_co2']
        reduction_percent = (reduction_kg_co2 / diesel_emissions['total_emissions_kg_co2']) * 100 if diesel_emissions['total_emissions_kg_co2'] > 0 else 0

        return {
            'diesel_emissions_kg_co2': diesel_emissions['total_emissions_kg_co2'],
            'ev_emissions_kg_co2': ev_emissions['total_emissions_kg_co2'],
            'reduction_kg_co2': reduction_kg_co2,
            'reduction_percent': reduction_percent,
            'reduction_metric_tons': reduction_kg_co2 / 1000,
            'co2_equivalent_trees_saved': reduction_kg_co2 / 21,  # 1 tree absorbs ~21kg CO2/year
            'timestamp': datetime.utcnow().isoformat()
        }

    def calculate_fleet_emissions_by_route(self, routes: List[Dict]) -> Dict:
        """
        Calculate emissions per route across entire fleet
        """
        route_emissions = []

        for route in routes:
            route_name = route.get('name')
            vehicle_type = route.get('vehicle_type')
            distance_km = route.get('distance_km')
            num_trips = route.get('num_trips', 1)

            total_distance = distance_km * num_trips
            emissions = self.calculate_total_emissions(vehicle_type, total_distance)

            route_emissions.append({
                'route_name': route_name,
                'vehicle_type': vehicle_type,
                'num_trips': num_trips,
                'total_distance_km': total_distance,
                'emissions_kg_co2': emissions['total_emissions_kg_co2'],
                'emissions_metric_tons': emissions['total_emissions_kg_co2'] / 1000
            })

        total_fleet_emissions = sum(r['emissions_kg_co2'] for r in route_emissions)

        return {
            'routes': route_emissions,
            'total_fleet_emissions_kg_co2': total_fleet_emissions,
            'total_fleet_emissions_metric_tons': total_fleet_emissions / 1000,
            'average_emission_per_route_kg_co2': total_fleet_emissions / len(routes) if routes else 0
        }

    def calculate_fleet_emissions_by_asset_class(self, vehicles: List[Dict]) -> Dict:
        """
        Calculate emissions by vehicle class/model
        """
        class_emissions = {}

        for vehicle in vehicles:
            vehicle_class = vehicle.get('model')
            vehicle_type = vehicle.get('powertrain')  # 'diesel' or 'electric'
            annual_distance = vehicle.get('annual_distance_km', 50000)

            if vehicle_class not in class_emissions:
                class_emissions[vehicle_class] = {
                    'vehicles_count': 0,
                    'total_emissions_kg_co2': 0,
                    'average_emissions_per_vehicle_kg_co2': 0
                }

            emissions = self.calculate_total_emissions(vehicle_type, annual_distance)
            class_emissions[vehicle_class]['vehicles_count'] += 1
            class_emissions[vehicle_class]['total_emissions_kg_co2'] += emissions['total_emissions_kg_co2']

        # Calculate averages
        for vehicle_class in class_emissions:
            count = class_emissions[vehicle_class]['vehicles_count']
            class_emissions[vehicle_class]['average_emissions_per_vehicle_kg_co2'] = (
                class_emissions[vehicle_class]['total_emissions_kg_co2'] / count
            )

        return {
            'emissions_by_asset_class': class_emissions,
            'total_fleet_emissions_kg_co2': sum(v['total_emissions_kg_co2'] for v in class_emissions.values()),
            'timestamp': datetime.utcnow().isoformat()
        }

    def generate_net_zero_roadmap(
        self,
        current_ev_vehicles: int,
        total_vehicles: int,
        target_year: int = 2030
    ) -> Dict:
        """
        Generate Net Zero roadmap with electrification targets
        """
        years_to_target = target_year - datetime.now().year
        vehicles_to_convert = total_vehicles - current_ev_vehicles
        annual_conversion_target = vehicles_to_convert / years_to_target if years_to_target > 0 else 0

        milestones = []
        for year in range(datetime.now().year, target_year + 1):
            ev_count = min(current_ev_vehicles + (year - datetime.now().year) * annual_conversion_target, total_vehicles)
            penetration = (ev_count / total_vehicles) * 100

            milestones.append({
                'year': year,
                'ev_vehicles': int(ev_count),
                'diesel_vehicles': int(total_vehicles - ev_count),
                'ev_penetration_percent': penetration
            })

        return {
            'current_state': {
                'ev_vehicles': current_ev_vehicles,
                'diesel_vehicles': total_vehicles - current_ev_vehicles,
                'ev_penetration_percent': (current_ev_vehicles / total_vehicles) * 100
            },
            'annual_conversion_target': int(annual_conversion_target),
            'years_to_net_zero': years_to_target,
            'milestones': milestones,
            'projected_emission_reduction': f'{(current_ev_vehicles / total_vehicles) * 100:.1f}% reduction by year 1'
        }
