#!/usr/bin/env python3
"""
Comprehensive test runner and orchestrator
Runs all test phases with detailed reporting
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class TestRunner:
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def run(self):
        """Execute all test phases"""
        self.start_time = datetime.now()
        print(self._header("Savaari Saarathi - Comprehensive Test Suite"))
        print(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Phase 1: Unit Tests
        self._run_phase("Unit Tests", [
            ("Battery SOH Service", "test_battery_service.py"),
            ("Quality Intelligence", "test_quality_service.py"),
            ("Carbon Tracking", "test_carbon_service.py"),
            ("Geospatial Service", "test_geospatial_service.py"),
            ("Supply Chain Traceability", "test_supply_chain_service.py"),
        ])
        
        # Phase 2: API Route Tests
        self._run_phase("API Route Tests", [
            ("API Endpoints", "test_api_routes.py"),
        ])
        
        # Phase 3: Integration Tests
        self._run_phase("Integration Tests", [
            ("Component Workflows", "test_integration.py"),
        ])
        
        # Phase 4: Performance Tests
        self._run_phase("Performance Tests", [
            ("Load & Response Time", "test_performance.py"),
        ])
        
        self.end_time = datetime.now()
        self._print_summary()
    
    def _run_phase(self, phase_name: str, tests: List[tuple]):
        """Run a phase of tests"""
        print(self._header(phase_name))
        
        phase_results = []
        
        for test_name, test_file in tests:
            result = self._run_test(test_name, test_file)
            phase_results.append(result)
            self.results.append(result)
        
        # Phase summary
        passed = sum(1 for r in phase_results if r["passed"])
        total = len(phase_results)
        print(f"\n{phase_name} Summary: {passed}/{total} passed\n")
    
    def _run_test(self, test_name: str, test_file: str) -> Dict:
        """Run a single test file"""
        print(f"  Running: {test_name}...", end=" ", flush=True)
        
        test_path = self.test_dir / test_file
        
        try:
            start = time.time()
            result = subprocess.run(
                ["pytest", str(test_path), "-v", "--tb=short", "-q"],
                capture_output=True,
                timeout=300,
                cwd=str(self.test_dir)
            )
            duration = time.time() - start
            
            passed = result.returncode == 0
            
            if passed:
                print(f"✓ PASSED ({duration:.2f}s)")
            else:
                print(f"✗ FAILED ({duration:.2f}s)")
                if result.stderr:
                    print(f"    Error: {result.stderr.decode()[:100]}")
            
            return {
                "test": test_name,
                "file": test_file,
                "passed": passed,
                "duration": duration,
                "output": result.stdout.decode()
            }
        
        except subprocess.TimeoutExpired:
            print("✗ TIMEOUT")
            return {
                "test": test_name,
                "file": test_file,
                "passed": False,
                "duration": 300,
                "output": "Test timed out"
            }
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            return {
                "test": test_name,
                "file": test_file,
                "passed": False,
                "duration": 0,
                "output": str(e)
            }
    
    def _print_summary(self):
        """Print comprehensive test summary"""
        print(self._header("Test Execution Summary"))
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["passed"])
        failed_tests = total_tests - passed_tests
        total_duration = (self.end_time - self.start_time).total_seconds()
        
        print(f"Total Tests Run: {total_tests}")
        print(f"✓ Passed: {passed_tests}")
        print(f"✗ Failed: {failed_tests}")
        print(f"Total Duration: {total_duration:.2f}s")
        print(f"Average per Test: {total_duration / total_tests:.2f}s")
        
        if failed_tests > 0:
            print("\nFailed Tests:")
            for result in self.results:
                if not result["passed"]:
                    print(f"  - {result['test']} ({result['file']})")
        
        print(f"\nEnd Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(self._header(""))
        
        # Exit code
        return 0 if failed_tests == 0 else 1
    
    def _header(self, title: str) -> str:
        """Format section header"""
        return f"\n{'='*50}\n{title}\n{'='*50}\n"


class CoverageReporter:
    """Generate coverage reports"""
    
    @staticmethod
    def generate():
        """Generate coverage report"""
        print("\nGenerating Coverage Report...")
        
        try:
            result = subprocess.run(
                [
                    "pytest",
                    "--cov=../services",
                    "--cov=../routes",
                    "--cov-report=html:coverage_report",
                    "--cov-report=term-missing",
                    "-q"
                ],
                capture_output=True,
                timeout=600
            )
            
            print(result.stdout.decode())
            
            if result.returncode == 0:
                print("\n✓ Coverage report generated: coverage_report/index.html")
            
        except Exception as e:
            print(f"Error generating coverage report: {e}")


def main():
    """Main entry point"""
    runner = TestRunner()
    exit_code = runner.run()
    
    # Generate coverage report
    CoverageReporter.generate()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
