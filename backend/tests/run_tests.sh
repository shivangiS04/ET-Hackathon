#!/bin/bash

# Comprehensive test runner script for Savaari Saarathi platform

set -e  # Exit on error

echo "=========================================="
echo "Savaari Saarathi - Comprehensive Test Suite"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
    echo -e "\n${BLUE}========== $1 ==========${NC}\n"
}

# Function to run tests with coverage
run_test_suite() {
    local test_file=$1
    local test_name=$2
    local marker=$3
    
    print_header "$test_name"
    
    if [ -z "$marker" ]; then
        pytest "$test_file" -v --tb=short
    else
        pytest "$test_file" -m "$marker" -v --tb=short
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $test_name PASSED${NC}"
    else
        echo -e "${RED}✗ $test_name FAILED${NC}"
        return 1
    fi
}

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}Installing pytest...${NC}"
    pip install pytest pytest-cov pytest-asyncio
fi

cd "$(dirname "$0")"

# Phase 1: Unit Tests
print_header "PHASE 1: Unit Tests"

run_test_suite "test_battery_service.py" "Battery SOH Service Tests" "unit"
run_test_suite "test_quality_service.py" "Quality Intelligence Tests" "unit"
run_test_suite "test_carbon_service.py" "Carbon Tracking Tests" "unit"
run_test_suite "test_geospatial_service.py" "Geospatial Service Tests" "unit"
run_test_suite "test_supply_chain_service.py" "Supply Chain Traceability Tests" "unit"

# Phase 2: API Route Tests
print_header "PHASE 2: API Route Tests"
run_test_suite "test_api_routes.py" "API Endpoint Tests" "api"

# Phase 3: Integration Tests
print_header "PHASE 3: Integration Tests"
run_test_suite "test_integration.py" "Integration Workflow Tests" "integration"

# Phase 4: Performance Tests
print_header "PHASE 4: Performance Tests"
run_test_suite "test_performance.py" "Performance & Load Tests" "performance"

# Phase 5: Full Test Coverage Report
print_header "PHASE 5: Coverage Report"
echo -e "${YELLOW}Generating test coverage report...${NC}\n"

pytest --cov=../services \
        --cov=../routes \
        --cov-report=html:coverage_report \
        --cov-report=term-missing \
        -v tests/

# Summary
print_header "Test Summary"

echo -e "${GREEN}All test phases completed!${NC}"
echo ""
echo "Test Statistics:"
pytest --collect-only -q 2>/dev/null | tail -1
echo ""
echo "Coverage Report: coverage_report/index.html"

echo -e "\n${BLUE}=========================================="
echo "Next Steps:"
echo "- Review coverage_report/index.html for coverage details"
echo "- Address any failing tests"
echo "- Run './run_tests.sh --watch' for continuous testing"
echo "==========================================${NC}\n"
