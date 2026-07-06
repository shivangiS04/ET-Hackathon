#!/usr/bin/env python3
"""
Test Runner for EV Supply Chain & Asset Intelligence Platform
Runs all tests with coverage reporting
"""

import sys
import os
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_tests(test_type="all", verbose=True):
    """
    Run tests with optional coverage
    
    Args:
        test_type: Type of tests to run (all, unit, api, services)
        verbose: Enable verbose output
    """
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    # Add coverage if available
    try:
        import coverage
        cmd.extend(["--cov=.", "--cov-report=term-missing", "--cov-report=html"])
    except ImportError:
        print("Coverage not installed. Run: pip install pytest-cov")
    
    # Select test files based on type
    test_dir = Path(__file__).parent
    
    if test_type == "all":
        cmd.append(str(test_dir))
    elif test_type == "unit":
        cmd.extend([
            str(test_dir / "test_battery_service.py"),
            str(test_dir / "test_supply_chain_service.py"),
            str(test_dir / "test_fleet_service.py"),
            str(test_dir / "test_anomaly_service.py"),
            str(test_dir / "test_scenario_service.py"),
        ])
    elif test_type == "api":
        cmd.append(str(test_dir / "test_api_routes.py"))
    elif test_type == "services":
        cmd.extend([
            str(test_dir / "test_battery_service.py"),
            str(test_dir / "test_supply_chain_service.py"),
            str(test_dir / "test_fleet_service.py"),
        ])
    else:
        # Run specific test file
        cmd.append(str(test_dir / f"test_{test_type}.py"))
    
    # Run tests
    print(f"\n{'='*60}")
    print(f"Running {test_type.upper()} Tests")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, cwd=test_dir.parent)
    
    return result.returncode


def run_specific_test(test_name):
    """Run a specific test by name"""
    cmd = ["python", "-m", "pytest", "-v", "-k", test_name]
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode


def list_tests():
    """List all available tests"""
    cmd = ["python", "-m", "pytest", "--collect-only", "-q"]
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run tests for EV Intelligence Platform")
    parser.add_argument(
        "--type", "-t",
        choices=["all", "unit", "api", "services", "battery", "supply_chain", "fleet", "anomaly", "scenario"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available tests"
    )
    parser.add_argument(
        "--test", "-k",
        help="Run specific test by name pattern"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Reduce output verbosity"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_tests()
    elif args.test:
        sys.exit(run_specific_test(args.test))
    else:
        sys.exit(run_tests(test_type=args.type, verbose=not args.quiet))
