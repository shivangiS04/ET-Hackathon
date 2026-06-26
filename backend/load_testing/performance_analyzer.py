"""
Performance Analysis Tool for EV Supply Chain Platform
Analyzes load test results and provides optimization recommendations
"""

import json
import csv
import statistics
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EndpointMetrics:
    """Metrics for a single endpoint"""
    name: str
    num_requests: int
    num_failures: int
    avg_response_ms: float
    min_response_ms: float
    max_response_ms: float
    
    @property
    def success_rate(self) -> float:
        if self.num_requests == 0:
            return 100.0
        return ((self.num_requests - self.num_failures) / self.num_requests) * 100
    
    @property
    def failure_rate(self) -> float:
        return 100 - self.success_rate
    
    @property
    def is_problematic(self) -> bool:
        """Check if endpoint has performance issues"""
        return (self.avg_response_ms > 500 or  # Avg response > 500ms
                self.failure_rate > 5 or        # Failure rate > 5%
                self.max_response_ms > 2000)    # Max response > 2 seconds


class LoadTestAnalyzer:
    """Analyze load test results and generate recommendations"""
    
    def __init__(self, results_dir: str = "backend/load_testing/results"):
        self.results_dir = Path(results_dir)
        self.metrics: List[EndpointMetrics] = []
        self.scenarios: Dict[str, dict] = {}
    
    def load_results(self):
        """Load all CSV results from load tests"""
        if not self.results_dir.exists():
            print(f"Results directory not found: {self.results_dir}")
            return False
        
        csv_files = sorted(self.results_dir.glob("*_stats_*.csv"))
        
        for csv_file in csv_files:
            self._parse_csv(csv_file)
        
        return len(self.metrics) > 0
    
    def _parse_csv(self, csv_path: Path):
        """Parse a CSV results file"""
        scenario = csv_path.stem.split("_stats_")[0]
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if row.get('Name') == 'Aggregated':
                    continue
                
                try:
                    metric = EndpointMetrics(
                        name=row.get('Name', 'Unknown'),
                        num_requests=int(row.get('Request Count', 0)),
                        num_failures=int(row.get('Failure Count', 0)),
                        avg_response_ms=float(row.get('Average Response Time', 0)),
                        min_response_ms=float(row.get('Min Response Time', 0)),
                        max_response_ms=float(row.get('Max Response Time', 0))
                    )
                    self.metrics.append(metric)
                except (ValueError, TypeError):
                    continue
    
    def generate_report(self) -> str:
        """Generate comprehensive performance analysis report"""
        report = []
        report.append("=" * 100)
        report.append("EV SUPPLY CHAIN PLATFORM - PERFORMANCE ANALYSIS REPORT")
        report.append("=" * 100)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 100)
        
        if self.metrics:
            total_requests = sum(m.num_requests for m in self.metrics)
            total_failures = sum(m.num_failures for m in self.metrics)
            overall_success = ((total_requests - total_failures) / total_requests * 100) if total_requests > 0 else 100
            
            avg_response_times = [m.avg_response_ms for m in self.metrics if m.num_requests > 0]
            
            report.append(f"Total Requests:           {total_requests:,}")
            report.append(f"Total Failures:           {total_failures:,}")
            report.append(f"Overall Success Rate:     {overall_success:.2f}%")
            report.append(f"Average Response Time:    {statistics.mean(avg_response_times):.2f} ms")
            report.append(f"Median Response Time:     {statistics.median(avg_response_times):.2f} ms")
            report.append(f"Max Response Time:        {max(avg_response_times):.2f} ms\n")
        
        # Endpoint Performance
        report.append("ENDPOINT PERFORMANCE ANALYSIS")
        report.append("-" * 100)
        report.append(f"{'Endpoint':<50} {'Requests':<12} {'Avg (ms)':<12} {'Max (ms)':<12} {'Success':<10}")
        report.append("-" * 100)
        
        sorted_metrics = sorted(self.metrics, key=lambda m: m.avg_response_ms, reverse=True)
        
        for metric in sorted_metrics:
            status = "⚠️  SLOW" if metric.is_problematic else "✓"
            report.append(
                f"{metric.name:<50} {metric.num_requests:<12} {metric.avg_response_ms:<12.2f} "
                f"{metric.max_response_ms:<12.2f} {metric.success_rate:<9.1f}% {status}"
            )
        
        report.append("")
        
        # Problem Endpoints
        problem_metrics = [m for m in self.metrics if m.is_problematic]
        if problem_metrics:
            report.append("PROBLEMATIC ENDPOINTS (Require Optimization)")
            report.append("-" * 100)
            
            for metric in problem_metrics:
                report.append(f"\n  🔴 {metric.name}")
                report.append(f"     Average Response Time: {metric.avg_response_ms:.2f} ms (Target: <500ms)")
                report.append(f"     Max Response Time:     {metric.max_response_ms:.2f} ms (Target: <2000ms)")
                report.append(f"     Failure Rate:          {metric.failure_rate:.2f}% (Target: <5%)")
                report.append(f"     Success Rate:          {metric.success_rate:.2f}%")
                report.append(f"     Total Requests:        {metric.num_requests}")
                
                # Recommendation
                report.append(f"     Recommendation: {self._get_optimization_recommendation(metric)}")
        
        report.append("\n")
        
        # Performance Tiers
        report.append("ENDPOINT PERFORMANCE TIERS")
        report.append("-" * 100)
        
        tier_excellent = [m for m in self.metrics if m.avg_response_ms < 100 and m.failure_rate < 1]
        tier_good = [m for m in self.metrics if m.avg_response_ms < 300 and m.failure_rate < 3]
        tier_acceptable = [m for m in self.metrics if m.avg_response_ms < 500 and m.failure_rate < 5]
        tier_poor = [m for m in self.metrics if m not in tier_acceptable]
        
        report.append(f"\n🟢 EXCELLENT (<100ms, <1% failures): {len(tier_excellent)} endpoints")
        for m in tier_excellent[:5]:
            report.append(f"   - {m.name}: {m.avg_response_ms:.2f}ms")
        
        report.append(f"\n🟡 GOOD (<300ms, <3% failures): {len(tier_good)} endpoints")
        for m in tier_good[:5]:
            report.append(f"   - {m.name}: {m.avg_response_ms:.2f}ms")
        
        report.append(f"\n🟠 ACCEPTABLE (<500ms, <5% failures): {len(tier_acceptable)} endpoints")
        report.append(f"\n🔴 POOR (>500ms or >5% failures): {len(tier_poor)} endpoints")
        for m in tier_poor:
            report.append(f"   - {m.name}: {m.avg_response_ms:.2f}ms ({m.failure_rate:.1f}% failures)")
        
        report.append("\n")
        
        # Optimization Recommendations
        report.append("OPTIMIZATION RECOMMENDATIONS")
        report.append("-" * 100)
        
        recommendations = self._generate_recommendations()
        for i, rec in enumerate(recommendations, 1):
            report.append(f"\n{i}. {rec['title']}")
            report.append(f"   {rec['description']}")
            report.append(f"   Impact: {rec['impact']}")
            report.append(f"   Effort: {rec['effort']}")
        
        report.append("\n")
        
        # Load Capacity Analysis
        report.append("LOAD CAPACITY ANALYSIS")
        report.append("-" * 100)
        
        total_requests = sum(m.num_requests for m in self.metrics)
        total_failures = sum(m.num_failures for m in self.metrics)
        success_rate = ((total_requests - total_failures) / total_requests * 100) if total_requests > 0 else 100
        
        if success_rate > 95:
            capacity_verdict = "✓ EXCELLENT - Platform can handle production load"
            recommended_users = "Up to 200 concurrent users recommended"
        elif success_rate > 90:
            capacity_verdict = "✓ GOOD - Platform is ready with minor optimizations"
            recommended_users = "Up to 150 concurrent users recommended"
        elif success_rate > 80:
            capacity_verdict = "⚠️  ACCEPTABLE - Requires optimization before production"
            recommended_users = "Up to 100 concurrent users recommended"
        else:
            capacity_verdict = "🔴 POOR - Significant optimization needed"
            recommended_users = "Up to 50 concurrent users until issues resolved"
        
        report.append(f"\nCapacity Verdict: {capacity_verdict}")
        report.append(f"Recommended Load: {recommended_users}")
        report.append(f"Overall Success Rate: {success_rate:.2f}%")
        
        report.append("\n" + "=" * 100 + "\n")
        
        return "\n".join(report)
    
    def _get_optimization_recommendation(self, metric: EndpointMetrics) -> str:
        """Get specific optimization recommendation for an endpoint"""
        issues = []
        
        if metric.avg_response_ms > 500:
            issues.append("Response time exceeds threshold")
        if metric.failure_rate > 5:
            issues.append("High failure rate")
        if metric.max_response_ms > 2000:
            issues.append("Excessive max response time")
        
        if "battery" in metric.name.lower() or "fleet" in metric.name.lower():
            return "Implement Redis caching for frequently accessed endpoints and add database indexing"
        elif "scenario" in metric.name.lower() or "anomaly" in metric.name.lower():
            return "Implement async processing with background jobs; add input validation caching"
        elif "update" in metric.name.lower() or "post" in metric.name.lower():
            return "Add request queuing and batch processing; implement rate limiting"
        else:
            return "Review database queries and add appropriate indexes; consider horizontal scaling"
    
    def _generate_recommendations(self) -> List[Dict]:
        """Generate optimization recommendations based on analysis"""
        recommendations = []
        
        # Recommendation 1: Caching
        high_latency_endpoints = [m for m in self.metrics if m.avg_response_ms > 300]
        if high_latency_endpoints:
            recommendations.append({
                'title': 'Implement Advanced Caching Strategy',
                'description': f'{len(high_latency_endpoints)} endpoints exceed 300ms. Implement Redis caching with appropriate TTLs. '
                              'Cache battery health data for 60s, fleet metrics for 120s, supply chain data for 300s.',
                'impact': 'Up to 70% reduction in response times for read-heavy endpoints',
                'effort': 'Medium - 4-6 hours implementation'
            })
        
        # Recommendation 2: Database Optimization
        recommendations.append({
            'title': 'Database Query Optimization',
            'description': 'Add composite indexes on frequently queried fields (vehicle_id, timestamp, supplier_id). '
                          'Review N+1 query patterns and implement batch loading.',
            'impact': '30-50% improvement in database query times',
            'effort': 'Medium - 3-5 hours'
        })
        
        # Recommendation 3: Async Processing
        heavy_compute = [m for m in self.metrics if 'scenario' in m.name.lower() or 'anomaly' in m.name.lower()]
        if heavy_compute:
            recommendations.append({
                'title': 'Implement Async Processing for Heavy Computations',
                'description': f'{len(heavy_compute)} compute-heavy endpoints detected. Move scenario simulation and anomaly '
                              'detection to background jobs using Celery/RQ.',
                'impact': 'Immediate response times <100ms; computation happens asynchronously',
                'effort': 'High - 8-12 hours implementation'
            })
        
        # Recommendation 4: Load Balancing
        recommendations.append({
            'title': 'Implement Load Balancing',
            'description': 'Deploy multiple backend instances behind nginx/HAProxy. Add horizontal scaling capability.',
            'impact': 'Linear scaling up to 10x current capacity',
            'effort': 'High - 12-16 hours'
        })
        
        # Recommendation 5: CDN for Frontend
        recommendations.append({
            'title': 'Deploy Frontend to CDN',
            'description': 'Move Next.js static assets and optimized images to CloudFlare/AWS CloudFront.',
            'impact': '60-80% reduction in frontend load times globally',
            'effort': 'Medium - 2-3 hours'
        })
        
        return recommendations


def main():
    """Main entry point"""
    analyzer = LoadTestAnalyzer()
    
    if analyzer.load_results():
        report = analyzer.generate_report()
        print(report)
        
        # Save report to file
        report_path = Path("backend/load_testing/results/PERFORMANCE_REPORT.txt")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"Report saved to: {report_path}")
    else:
        print("No load test results found. Run load tests first using: ./backend/load_testing/run_load_tests.sh")


if __name__ == "__main__":
    main()
