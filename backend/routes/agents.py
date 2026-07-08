"""
Multi-Agent Orchestration Routes
Endpoints for coordinated fleet analysis, agent status, and individual agent execution
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import time

from agents.orchestrator import MultiAgentOrchestrator

router = APIRouter()
orchestrator = MultiAgentOrchestrator()


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CrossAgentInsightResponse(BaseModel):
    """Cross-agent conflict resolution insight"""
    type: str  # "conflict", "opportunity", "risk", "recommendation"
    message: str
    severity: str  # "critical", "high", "medium", "info"
    affected_agents: List[str]
    recommended_action: str
    confidence: float


class AgentResultResponse(BaseModel):
    """Result from a single agent"""
    status: str  # "success", "error"
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str


class CoordinatedAnalysisResponse(BaseModel):
    """Response from coordinated fleet analysis"""
    fleet_id: str
    agent_results: Dict[str, AgentResultResponse]
    cross_agent_insights: List[CrossAgentInsightResponse]
    overall_fleet_health_score: float
    orchestration_timestamp: str
    agents_run: List[str]
    execution_time_ms: float
    insights_count: int
    critical_insights_count: int


class AgentStatusResponse(BaseModel):
    """Status of a single agent"""
    name: str
    status: str  # "operational", "running", "error", "idle"
    last_run: Optional[str]
    response_time_ms: float
    insights_generated: int


class AgentStatusListResponse(BaseModel):
    """List of all agent statuses"""
    agents: List[AgentStatusResponse]
    total_agents: int
    operational_agents: int
    timestamp: str


class SingleAgentResultResponse(BaseModel):
    """Result from running a single agent"""
    agent_name: str
    status: str  # "success", "error"
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    response_time_ms: float
    timestamp: str


# ============================================================================
# COORDINATED FLEET ANALYSIS ENDPOINT
# ============================================================================

@router.post("/orchestrate", response_model=CoordinatedAnalysisResponse)
async def orchestrate_fleet_analysis(
    fleet_id: str = Query(..., description="Fleet identifier"),
    vehicle_count: int = Query(100, description="Number of vehicles in fleet"),
    run_parallel: bool = Query(False, description="Run agents in parallel (experimental)")
):
    """
    Run coordinated multi-agent analysis on entire fleet with cross-agent conflict resolution.

    **Agents Coordinated:**
    1. **Battery Health Agent** - SOH, RUL, degradation analysis
    2. **Supply Chain Agent** - Risk, concentration, alternatives
    3. **Fleet Readiness Agent** - EV transition readiness, TCO
    4. **Anomaly Detection Agent** - Unusual pattern detection
    5. **Manufacturing Quality Agent** - SPC, quality drift, process control
    6. **Carbon Intelligence Agent** - Emissions, net-zero roadmap

    **Cross-Agent Conflict Resolution (6 Rules):**
    - Rule 1: Low SOH (<70%) + Quality Drift → CRITICAL escalation
    - Rule 2: High Supply Chain Risk (>0.7) + Low Fleet Readiness (<50%) → Procurement urgency
    - Rule 3: High Carbon Impact (>3000t) + High Fleet Readiness (>0.8) → Priority for EV transition
    - Rule 4: Critical Anomalies + Battery Degradation → Investigate systematic issue
    - Rule 5: Quality OUT_OF_CONTROL + High Fleet Readiness → Quality must be resolved first
    - Rule 6: Supply Chain Stable + Fleet Ready + High Carbon → Accelerate EV transition

    **Overall Fleet Health Score:**
    - Calculated from 6 agent scores (0-100)
    - Penalty: -15 per critical insight, -5 per high insight
    - Range: 0-100

    **Example Request:**
    ```
    POST /api/v1/agents/orchestrate?fleet_id=FLEET_001&vehicle_count=100&run_parallel=false
    ```

    **Returns:**
    - agent_results: Individual agent analyses
    - cross_agent_insights: Detected conflicts & opportunities
    - overall_fleet_health_score: Composite fleet score
    - execution_time_ms: Total orchestration time
    - critical_insights_count: Number of critical alerts

    **Performance:**
    - Response time: ~500-1000ms (sequential), <500ms (parallel)
    - Processes all 6 agents simultaneously
    - Conflict resolution rules applied automatically

    **Use Cases:**
    - Daily fleet health dashboard
    - Pre-procurement decision support
    - EV transition planning verification
    - Supply chain risk assessment
    - Quality assurance oversight
    """

    try:
        start_time = time.time()

        # Run coordinated analysis
        result = orchestrator.run_coordinated_fleet_analysis(
            fleet_id=fleet_id,
            vehicle_count=vehicle_count,
            run_parallel=run_parallel
        )

        # Convert to response model
        response = CoordinatedAnalysisResponse(
            fleet_id=result["fleet_id"],
            agent_results={k: AgentResultResponse(**v) for k, v in result["agent_results"].items()},
            cross_agent_insights=[
                CrossAgentInsightResponse(**insight) for insight in result["cross_agent_insights"]
            ],
            overall_fleet_health_score=result["overall_fleet_health_score"],
            orchestration_timestamp=result["orchestration_timestamp"],
            agents_run=result["agents_run"],
            execution_time_ms=result["execution_time_ms"],
            insights_count=result["insights_count"],
            critical_insights_count=result["critical_insights_count"]
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestration error: {str(e)}")


# ============================================================================
# AGENT STATUS ENDPOINT
# ============================================================================

@router.get("/status", response_model=AgentStatusListResponse)
async def get_agents_status():
    """
    Get health and status of all 6 agents.

    **Returns:**
    - agents: List of agent statuses with metadata
    - total_agents: Always 6
    - operational_agents: Number currently operational
    - timestamp: Status check timestamp

    **Agent Status Values:**
    - "operational" - Running normally, ready for tasks
    - "running" - Currently executing a task
    - "error" - Last execution failed
    - "idle" - Not yet used in this session

    **Metrics per Agent:**
    - name: Agent identifier
    - status: Current operational status
    - last_run: Timestamp of most recent execution
    - response_time_ms: Average response time
    - insights_generated: Count of insights generated this session

    **Example Request:**
    ```
    GET /api/v1/agents/status
    ```

    **Use Case:**
    - Dashboard health check
    - Agent availability verification
    - Performance monitoring
    - Diagnostics
    """

    try:
        result = orchestrator.get_agent_status()

        response = AgentStatusListResponse(
            agents=[AgentStatusResponse(**agent) for agent in result["agents"]],
            total_agents=result["total_agents"],
            operational_agents=result["operational_agents"],
            timestamp=result["timestamp"]
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check error: {str(e)}")


# ============================================================================
# SINGLE AGENT EXECUTION ENDPOINT
# ============================================================================

@router.post("/run/{agent_name}", response_model=SingleAgentResultResponse)
async def run_single_agent(
    agent_name: str,
    vehicle_count: int = Query(100, description="Number of vehicles (for fleet-based agents)"),
    fleet_id: str = Query("FLEET_001", description="Fleet identifier")
):
    """
    Run a single agent independently and return its analysis.

    **Available Agents:**
    1. **battery** - Battery health analysis (SOH, RUL, degradation)
    2. **supply_chain** - Supply chain risk assessment
    3. **fleet** - Fleet readiness for EV transition
    4. **anomaly** - Anomaly detection in fleet data
    5. **quality** - Manufacturing quality control
    6. **carbon** - Emissions and net-zero planning

    **Agent Descriptions:**

    ### Battery Agent
    - Analyzes state-of-health across fleet
    - Predicts remaining useful life
    - Identifies vehicles requiring maintenance
    - Uses LSTM + thermal degradation models
    - Output: average_soh, vehicles_below_threshold, average_rul_days

    ### Supply Chain Agent
    - Assesses supplier concentration (Herfindahl Index)
    - Identifies single-source components
    - Evaluates supply delay risks
    - Checks geopolitical factors
    - Output: concentration_risk, alternative_sourcing_available

    ### Fleet Agent
    - Evaluates EV transition readiness
    - Calculates total cost of ownership
    - Assesses charging infrastructure availability
    - Output: readiness_score, ev_ready_vehicles, tco_payback_years

    ### Anomaly Agent
    - Detects unusual patterns using Isolation Forest
    - Identifies critical anomalies
    - Classifies anomaly types
    - Output: anomalies_detected, affected_vehicles, confidence_score

    ### Quality Agent
    - Statistical Process Control (SPC) metrics
    - Detects quality drift
    - Calculates capability indices (Cpk, Cp)
    - Output: lines_in_control, defects_per_million, yield_rate

    ### Carbon Agent
    - Calculates Scope 1 & 3 emissions
    - Generates net-zero roadmap (FAME-II aligned)
    - Identifies high-impact vehicles for EV transition
    - Output: total_emissions, carbon_saved, ev_percentage_target

    **Example Requests:**
    ```
    POST /api/v1/agents/run/battery?vehicle_count=100
    POST /api/v1/agents/run/supply_chain
    POST /api/v1/agents/run/fleet?fleet_id=FLEET_001
    POST /api/v1/agents/run/anomaly?vehicle_count=100
    POST /api/v1/agents/run/quality
    POST /api/v1/agents/run/carbon?vehicle_count=100
    ```

    **Returns:**
    - agent_name: Which agent ran
    - status: "success" or "error"
    - data: Agent-specific analysis results
    - response_time_ms: Execution time
    - timestamp: When it ran

    **Performance:**
    - Response time: 50-200ms per agent
    - Scales linearly with vehicle count
    - Cacheable for repeated parameters

    **Use Cases:**
    - Drill-down analysis on specific domain
    - Troubleshooting agent performance
    - Integration testing
    - Domain-specific dashboard
    """

    try:
        # Validate agent name
        valid_agents = ["battery", "supply_chain", "fleet", "anomaly", "quality", "carbon"]
        if agent_name not in valid_agents:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid agent: {agent_name}. Available: {valid_agents}"
            )

        # Prepare parameters
        params = {
            "vehicle_count": vehicle_count,
            "fleet_id": fleet_id
        }

        # Run single agent
        result = orchestrator.run_single_agent(agent_name, params)

        response = SingleAgentResultResponse(
            agent_name=result["agent_name"],
            status=result["status"],
            data=result.get("data"),
            error=result.get("error"),
            response_time_ms=result["response_time_ms"],
            timestamp=result["timestamp"]
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution error: {str(e)}")


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@router.get("/health-check")
async def agents_health_check():
    """Health check endpoint for agent orchestration system."""
    return {
        "service": "Multi-Agent Orchestration",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "agents_count": 6,
        "agents": [
            "battery",
            "supply_chain",
            "fleet",
            "anomaly",
            "quality",
            "carbon"
        ],
        "conflict_resolution_rules": 6,
        "capabilities": [
            "Coordinated multi-agent analysis",
            "Cross-agent conflict resolution",
            "Individual agent execution",
            "Fleet health scoring",
            "Real-time insights generation"
        ]
    }


@router.get("/agents")
async def list_available_agents():
    """List all available agents with descriptions."""
    return {
        "agents": [
            {
                "name": "battery",
                "description": "Battery health analysis (SOH, RUL, degradation)",
                "domain": "Battery & Health",
                "inputs": ["vehicle_count", "fleet_id"],
                "key_outputs": ["average_soh", "vehicles_below_80_soh", "average_rul_days"]
            },
            {
                "name": "supply_chain",
                "description": "Supply chain risk assessment and resilience",
                "domain": "Supply Chain",
                "inputs": ["fleet_id"],
                "key_outputs": ["herfindahl_index", "concentration_risk", "critical_suppliers"]
            },
            {
                "name": "fleet",
                "description": "Fleet readiness for EV transition",
                "domain": "Fleet Management",
                "inputs": ["vehicle_count", "fleet_id"],
                "key_outputs": ["readiness_score", "ev_ready_vehicles", "tco_payback_years"]
            },
            {
                "name": "anomaly",
                "description": "Anomaly detection in fleet data",
                "domain": "Advanced Features",
                "inputs": ["vehicle_count", "fleet_id"],
                "key_outputs": ["anomalies_detected", "critical_anomalies", "affected_vehicles"]
            },
            {
                "name": "quality",
                "description": "Manufacturing quality control (SPC)",
                "domain": "Manufacturing Quality",
                "inputs": [],
                "key_outputs": ["average_cpk", "defects_per_million", "yield_rate"]
            },
            {
                "name": "carbon",
                "description": "Emissions and net-zero planning (FAME-II aligned)",
                "domain": "Carbon & Net Zero",
                "inputs": ["vehicle_count"],
                "key_outputs": ["total_fleet_emissions", "carbon_saved", "ev_percentage_target"]
            }
        ],
        "total_agents": 6,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/insights-rules")
async def get_conflict_resolution_rules():
    """Get descriptions of all conflict resolution rules."""
    return {
        "rules": [
            {
                "id": 1,
                "name": "Battery + Quality Escalation",
                "condition": "battery.average_soh < 70% AND quality.drift_detected",
                "result": "CRITICAL escalation",
                "action": "Halt production, quarantine batches, root cause analysis"
            },
            {
                "id": 2,
                "name": "Supply Chain + Fleet Readiness",
                "condition": "supply_chain_risk > 0.7 AND fleet.readiness < 0.5",
                "result": "HIGH priority - procurement urgency",
                "action": "Diversify suppliers, increase inventory, accelerate readiness"
            },
            {
                "id": 3,
                "name": "Carbon + Fleet Opportunity",
                "condition": "carbon.addressable > 3000t AND fleet.readiness > 0.8",
                "result": "MEDIUM opportunity - EV transition priority",
                "action": "Approve Phase 1 procurement, secure subsidies, setup charging"
            },
            {
                "id": 4,
                "name": "Anomaly + Battery Pattern",
                "condition": "anomaly.critical > 0 AND battery.maintenance_vehicles > 5",
                "result": "HIGH risk - systematic issue investigation",
                "action": "Cross-reference vehicles, check charging profiles, review thermal"
            },
            {
                "id": 5,
                "name": "Quality Impact on Transition",
                "condition": "quality.status = OUT_OF_CONTROL AND fleet.readiness > 0.7",
                "result": "HIGH conflict - quality blocks transition",
                "action": "Delay procurement, implement corrections, re-baseline"
            },
            {
                "id": 6,
                "name": "Acceleration Conditions Met",
                "condition": "supply_chain_risk < 0.5 AND fleet.readiness > 0.85 AND carbon > 3500t",
                "result": "INFO recommendation - accelerate transition",
                "action": "Launch Phase 1 (30 vehicles), finalize infrastructure, training"
            }
        ],
        "total_rules": 6,
        "timestamp": datetime.utcnow().isoformat()
    }
