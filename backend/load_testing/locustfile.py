"""
Load Testing Suite for EV Supply Chain & Asset Intelligence Platform
Using Locust framework to simulate concurrent users and measure performance
"""

from locust import HttpUser, task, between, TaskSet, events
from locust.contrib.fasthttp import FastHttpUser
import random
import json
import time
from datetime import datetime, timedelta
import statistics

# Sample data for realistic API calls
VEHICLE_IDS = [f"VEHICLE_{i:04d}" for i in range(1, 51)]
BATTERY_IDS = [f"BATTERY_{i:04d}" for i in range(1, 101)]
SUPPLIER_IDS = [f"SUPPLIER_{i:03d}" for i in range(1, 31)]

class APITaskSet(TaskSet):
    """Task set defining user behavior patterns"""
    
    @task(3)
    def get_battery_health(self):
        """Get battery health dashboard - High frequency endpoint"""
        vehicle_id = random.choice(VEHICLE_IDS)
        with self.client.get(
            f"/api/v1/battery/{vehicle_id}",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()  # Vehicle not found is acceptable
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task(2)
    def get_fleet_readiness(self):
        """Get fleet readiness data - Medium frequency endpoint"""
        with self.client.get(
            "/api/v1/fleet/readiness",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    response.success()
                else:
                    response.failure("Response missing 'data' field")
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(2)
    def get_supply_chain_risk(self):
        """Get supply chain risk assessment - Medium frequency endpoint"""
        supplier_id = random.choice(SUPPLIER_IDS)
        with self.client.get(
            f"/api/v1/supply-chain/risk/{supplier_id}",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(1)
    def predict_battery_failure(self):
        """Predict battery failure - Low frequency, heavy computation"""
        vehicle_id = random.choice(VEHICLE_IDS)
        with self.client.get(
            f"/api/v1/battery/{vehicle_id}/prediction",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(1)
    def get_scenario_simulation(self):
        """Simulate supply chain scenarios - Heavy computation"""
        scenario_data = {
            "scenario_type": random.choice([
                "lithium_shortage",
                "port_closure",
                "price_shock",
                "supplier_default",
                "region_lockdown"
            ]),
            "severity": random.uniform(0.5, 1.0),
            "duration_days": random.randint(30, 180)
        }
        with self.client.post(
            "/api/v1/scenarios/simulate",
            json=scenario_data,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(1)
    def detect_anomalies(self):
        """Detect anomalies in system - Heavy computation"""
        with self.client.post(
            "/api/v1/anomalies/detect",
            json={},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(2)
    def get_metrics(self):
        """Get system performance metrics - Low overhead"""
        with self.client.get(
            "/api/v1/metrics",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(1)
    def update_battery_data(self):
        """Create/update battery telemetry - Write operation"""
        battery_data = {
            "vehicle_id": random.choice(VEHICLE_IDS),
            "soh": random.uniform(70, 100),
            "temperature": random.uniform(20, 45),
            "cycles": random.randint(1000, 5000),
            "timestamp": datetime.now().isoformat()
        }
        with self.client.post(
            "/api/v1/battery/update",
            json=battery_data,
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")


class EVPlatformUser(FastHttpUser):
    """Simulates a regular user of the EV platform"""
    tasks = [APITaskSet]
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests


class PowerUser(FastHttpUser):
    """Simulates a power user making frequent requests"""
    tasks = [APITaskSet]
    wait_time = between(0.5, 1.5)  # More frequent requests


class DashboardViewer(FastHttpUser):
    """Simulates a user viewing dashboards"""
    
    @task(5)
    def view_battery_dashboard(self):
        """Frequently view battery dashboard"""
        with self.client.get("/api/v1/battery/dashboard", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(3)
    def view_fleet_dashboard(self):
        """View fleet dashboard"""
        with self.client.get("/api/v1/fleet/dashboard", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(2)
    def view_supply_chain_dashboard(self):
        """View supply chain dashboard"""
        with self.client.get("/api/v1/supply-chain/dashboard", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    wait_time = between(2, 5)


# Event handlers for custom metrics
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Initialize test metrics"""
    print("\n" + "="*80)
    print("LOAD TEST STARTED")
    print("="*80)
    print(f"Start time: {datetime.now()}")
    print(f"Target: {environment.host}")
    print("="*80 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Print comprehensive test results"""
    print("\n" + "="*80)
    print("LOAD TEST COMPLETED")
    print("="*80)
    print(f"End time: {datetime.now()}\n")
    
    # Calculate and display statistics
    stats = environment.stats
    
    print("RESPONSE TIME STATISTICS (ms)")
    print("-" * 80)
    
    response_times = []
    for stat in stats.entries.values():
        if stat.num_requests > 0:
            response_times.extend(stat.response_times)
    
    if response_times:
        response_times_sorted = sorted(response_times)
        print(f"Min:        {min(response_times_sorted):.2f} ms")
        print(f"Max:        {max(response_times_sorted):.2f} ms")
        print(f"Mean:       {statistics.mean(response_times_sorted):.2f} ms")
        print(f"Median:     {statistics.median(response_times_sorted):.2f} ms")
        print(f"P95:        {response_times_sorted[int(len(response_times_sorted)*0.95)]:.2f} ms")
        print(f"P99:        {response_times_sorted[int(len(response_times_sorted)*0.99)]:.2f} ms")
        print(f"StdDev:     {statistics.stdev(response_times_sorted):.2f} ms\n")
    
    print("ENDPOINT PERFORMANCE")
    print("-" * 80)
    print(f"{'Endpoint':<50} {'Requests':<12} {'Failures':<12} {'Avg Time':<12}")
    print("-" * 80)
    
    for endpoint_path, stat in sorted(stats.entries.items()):
        if endpoint_path == "Aggregated":
            continue
        avg_time = stat.avg_response_time if stat.num_requests > 0 else 0
        failure_rate = (stat.num_failures / stat.num_requests * 100) if stat.num_requests > 0 else 0
        print(f"{endpoint_path:<50} {stat.num_requests:<12} {stat.num_failures:<12} {avg_time:<12.2f}")
    
    print("-" * 80)
    print(f"{'TOTAL':<50} {stats.total.num_requests:<12} {stats.total.num_failures:<12}\n")
    
    # Success rate
    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    success_rate = ((total_requests - total_failures) / total_requests * 100) if total_requests > 0 else 0
    
    print(f"Total Requests:    {total_requests}")
    print(f"Total Failures:    {total_failures}")
    print(f"Success Rate:      {success_rate:.2f}%")
    print(f"Failure Rate:      {100 - success_rate:.2f}%")
    print("="*80 + "\n")


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Log individual requests for debugging"""
    if exception:
        print(f"[ERROR] {name} - {exception}")


# Configuration for different test scenarios
# Run with: locust -f locustfile.py --host=http://localhost:8000
# 
# SCENARIOS:
# 1. Steady load: locust -f locustfile.py --host=http://localhost:8000 -u 50 -r 5 -t 5m
# 2. Ramp test: locust -f locustfile.py --host=http://localhost:8000 -u 200 -r 10 -t 10m
# 3. Stress test: locust -f locustfile.py --host=http://localhost:8000 -u 500 -r 25 -t 15m
# 4. Spike test: locust -f locustfile.py --host=http://localhost:8000 -u 1000 -r 100 -t 2m
