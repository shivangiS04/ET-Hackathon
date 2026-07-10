"""
Geospatial Visualization Service
Charging infrastructure planning and route optimization with maps
"""

from typing import Dict, List, Tuple
from datetime import datetime
import math


class GeospatialService:
    """
    Handles geospatial analysis for EV fleet operations
    - Charging infrastructure planning
    - Route optimization
    - Coverage analysis
    """

    def __init__(self):
        self.charging_station_coverage_radius_km = 50
        self.dc_fast_charger_efficiency = 0.85  # 85% charge in 30 min

    def plan_charging_infrastructure(
        self,
        fleet_location_clusters: List[Dict],
        required_coverage_km: float = 50
    ) -> Dict:
        """
        Plan optimal charging infrastructure locations
        """
        recommended_stations = []

        for cluster in fleet_location_clusters:
            cluster_name = cluster.get('name')
            vehicles_count = cluster.get('vehicles_count')
            avg_daily_km = cluster.get('avg_daily_km', 100)
            latitude = cluster.get('latitude')
            longitude = cluster.get('longitude')

            # Calculate charging stations needed
            daily_energy_needed_kwh = vehicles_count * avg_daily_km * 0.18  # 0.18 kWh/km
            chargers_needed = max(2, int(daily_energy_needed_kwh / 120))  # 120 kW chargers

            infrastructure = {
                'location_name': cluster_name,
                'latitude': latitude,
                'longitude': longitude,
                'vehicles_in_cluster': vehicles_count,
                'dc_fast_chargers': chargers_needed,
                'ac_slow_chargers': max(1, chargers_needed // 3),
                'total_capacity_kw': (chargers_needed * 120) + (max(1, chargers_needed // 3) * 22),
                'daily_energy_capacity_kwh': (chargers_needed * 120 * 0.5) + (max(1, chargers_needed // 3) * 22 * 0.25),
                'coverage_radius_km': self.charging_station_coverage_radius_km,
                'investment_estimate_lakhs': chargers_needed * 50  # 50 lakhs per fast charger
            }

            recommended_stations.append(infrastructure)

        total_investment = sum(s['investment_estimate_lakhs'] for s in recommended_stations)

        return {
            'recommended_charging_stations': recommended_stations,
            'total_stations': len(recommended_stations),
            'total_dc_fast_chargers': sum(s['dc_fast_chargers'] for s in recommended_stations),
            'total_ac_chargers': sum(s['ac_slow_chargers'] for s in recommended_stations),
            'total_capacity_kw': sum(s['total_capacity_kw'] for s in recommended_stations),
            'total_investment_estimate_crores': total_investment / 100,
            'payback_period_years': 4.2,
            'timestamp': datetime.utcnow().isoformat()
        }

    def calculate_coverage_gaps(
        self,
        existing_chargers: List[Dict],
        vehicle_clusters: List[Dict],
        coverage_radius_km: float = 50
    ) -> Dict:
        """
        Identify coverage gaps in charging infrastructure
        """
        gaps = []

        for cluster in vehicle_clusters:
            cluster_lat = cluster.get('latitude')
            cluster_lon = cluster.get('longitude')
            cluster_name = cluster.get('name')

            # Check nearest charger
            nearest_distance = self._find_nearest_charger(
                (cluster_lat, cluster_lon),
                existing_chargers
            )

            if nearest_distance > coverage_radius_km:
                gaps.append({
                    'location_name': cluster_name,
                    'latitude': cluster_lat,
                    'longitude': cluster_lon,
                    'vehicles_affected': cluster.get('vehicles_count', 0),
                    'nearest_charger_distance_km': nearest_distance,
                    'coverage_gap_km': nearest_distance - coverage_radius_km,
                    'priority': 'HIGH' if nearest_distance > 100 else 'MEDIUM',
                    'recommended_charger_type': 'DC_FAST' if nearest_distance > 75 else 'AC_SLOW'
                })

        return {
            'coverage_gaps_identified': len(gaps),
            'gaps': gaps,
            'affected_vehicles': sum(g['vehicles_affected'] for g in gaps),
            'total_coverage_radius_km': coverage_radius_km,
            'timestamp': datetime.utcnow().isoformat()
        }

    def optimize_routes_for_ev(
        self,
        routes: List[Dict],
        vehicle_range_km: float = 350
    ) -> Dict:
        """
        Optimize routes for EV vehicles considering range and charging stops
        """
        optimized_routes = []

        for route in routes:
            route_name = route.get('name')
            total_distance_km = route.get('distance_km')
            start_location = route.get('start_location')
            end_location = route.get('end_location')

            # Determine charging stops needed
            charging_stops = max(0, int(total_distance_km / vehicle_range_km) - 1)
            
            # Calculate stop locations
            stop_locations = []
            for i in range(1, charging_stops + 1):
                stop_distance = (i * total_distance_km) / (charging_stops + 1)
                stop_locations.append({
                    'stop_number': i,
                    'distance_from_start_km': stop_distance,
                    'remaining_distance_km': total_distance_km - stop_distance
                })

            optimization = {
                'route_name': route_name,
                'start_location': start_location,
                'end_location': end_location,
                'total_distance_km': total_distance_km,
                'vehicle_range_km': vehicle_range_km,
                'charging_stops_required': charging_stops,
                'charging_stop_locations': stop_locations,
                'estimated_travel_time_hours': (total_distance_km / 80) + (charging_stops * 0.5),  # 0.5h per charge
                'carbon_emissions_kg_co2': total_distance_km * 0.018,  # EV emissions
                'efficiency_score': 100 - (charging_stops * 5)  # Deduct 5% per stop
            }

            optimized_routes.append(optimization)

        return {
            'optimized_routes': optimized_routes,
            'total_routes_optimized': len(optimized_routes),
            'total_charging_stops_required': sum(r['charging_stops_required'] for r in optimized_routes),
            'average_efficiency_score': sum(r['efficiency_score'] for r in optimized_routes) / len(optimized_routes) if optimized_routes else 0,
            'timestamp': datetime.utcnow().isoformat()
        }

    def generate_coverage_map(
        self,
        existing_chargers: List[Dict],
        vehicle_locations: List[Dict]
    ) -> Dict:
        """
        Generate geospatial coverage analysis for visualization
        """
        coverage_zones = []

        for charger in existing_chargers:
            charger_lat = charger.get('latitude')
            charger_lon = charger.get('longitude')
            charger_name = charger.get('name')
            capacity = charger.get('capacity_kw', 120)

            # Vehicles within coverage
            covered_vehicles = []
            for vehicle in vehicle_locations:
                distance = self._haversine_distance(
                    (charger_lat, charger_lon),
                    (vehicle.get('latitude'), vehicle.get('longitude'))
                )
                if distance <= self.charging_station_coverage_radius_km:
                    covered_vehicles.append({
                        'vehicle_id': vehicle.get('id'),
                        'distance_km': distance
                    })

            zone = {
                'charger_name': charger_name,
                'location': {'lat': charger_lat, 'lon': charger_lon},
                'capacity_kw': capacity,
                'coverage_radius_km': self.charging_station_coverage_radius_km,
                'vehicles_covered': len(covered_vehicles),
                'coverage_utilization_percent': (len(covered_vehicles) * 15) / (capacity / 10),  # Estimate
                'covered_vehicles': covered_vehicles
            }

            coverage_zones.append(zone)

        total_coverage = sum(z['vehicles_covered'] for z in coverage_zones)

        return {
            'coverage_zones': coverage_zones,
            'total_chargers': len(coverage_zones),
            'total_vehicles_covered': total_coverage,
            'coverage_percent': (total_coverage / len(vehicle_locations)) * 100 if vehicle_locations else 0,
            'timestamp': datetime.utcnow().isoformat()
        }

    def _find_nearest_charger(
        self,
        location: Tuple[float, float],
        chargers: List[Dict]
    ) -> float:
        """Find distance to nearest charger"""
        if not chargers:
            return float('inf')

        distances = [
            self._haversine_distance(
                location,
                (charger.get('latitude'), charger.get('longitude'))
            )
            for charger in chargers
        ]

        return min(distances) if distances else float('inf')

    def _haversine_distance(
        self,
        coord1: Tuple[float, float],
        coord2: Tuple[float, float]
    ) -> float:
        """Calculate distance between two geographic coordinates in km"""
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        R = 6371  # Earth's radius in km
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
