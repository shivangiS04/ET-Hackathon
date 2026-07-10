#!/bin/bash

# Quick test runner - Run specific test suites

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Print usage
usage() {
    echo "Usage: ./quick_test.sh [option]"
    echo ""
    echo "Options:"
    echo "  battery       - Test battery service only"
    echo "  quality       - Test quality service only"
    echo "  carbon        - Test carbon tracking only"
    echo "  geospatial    - Test geospatial service only"
    echo "  supply-chain  - Test supply chain service only"
    echo "  api           - Test API routes only"
    echo "  integration   - Test integrations only"
    echo "  performance   - Test performance/load only"
    echo "  unit          - All unit tests"
    echo "  all           - All tests (default)"
    echo "  help          - Show this help"
}

# Run tests by category
run_tests() {
    local category=$1
    
    case $category in
        battery)
            echo -e "${BLUE}Running Battery Service Tests...${NC}"
            pytest test_battery_service.py -v
            ;;
        quality)
            echo -e "${BLUE}Running Quality Service Tests...${NC}"
            pytest test_quality_service.py -v
            ;;
        carbon)
            echo -e "${BLUE}Running Carbon Service Tests...${NC}"
            pytest test_carbon_service.py -v
            ;;
        geospatial)
            echo -e "${BLUE}Running Geospatial Service Tests...${NC}"
            pytest test_geospatial_service.py -v
            ;;
        supply-chain)
            echo -e "${BLUE}Running Supply Chain Service Tests...${NC}"
            pytest test_supply_chain_service.py -v
            ;;
        api)
            echo -e "${BLUE}Running API Route Tests...${NC}"
            pytest test_api_routes.py -v
            ;;
        integration)
            echo -e "${BLUE}Running Integration Tests...${NC}"
            pytest test_integration.py -v
            ;;
        performance)
            echo -e "${BLUE}Running Performance Tests...${NC}"
            pytest test_performance.py -v
            ;;
        unit)
            echo -e "${BLUE}Running All Unit Tests...${NC}"
            pytest test_battery_service.py \
                    test_quality_service.py \
                    test_carbon_service.py \
                    test_geospatial_service.py \
                    test_supply_chain_service.py \
                    -v
            ;;
        all)
            echo -e "${BLUE}Running All Tests...${NC}"
            pytest -v
            ;;
        help)
            usage
            ;;
        *)
            echo "Unknown option: $category"
            usage
            exit 1
            ;;
    esac
}

# Default to all tests
category=${1:-all}

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}Installing pytest and dependencies...${NC}"
    pip install -q -r requirements.txt
fi

# Change to tests directory
cd "$(dirname "$0")"

# Run tests
run_tests "$category"

echo -e "\n${GREEN}✓ Tests completed${NC}\n"
