# System Architecture

## Overview

The EV Supply Chain & Asset Intelligence platform is built as a modern full-stack application with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                       │
│  React 18 + Next.js 14 + Tailwind CSS (localhost:3000)       │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/REST API
┌────────────────▼────────────────────────────────────────────┐
│                   API GATEWAY / ROUTING                       │
│          FastAPI + Uvicorn (localhost:8000)                  │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴──────────────────┐
        │                           │
┌───────▼──────────┐      ┌────────▼───────────┐
│  Business Logic  │      │  ML/Inference     │
│  Services Layer  │      │  Engine           │
├──────────────────┤      ├───────────────────┤
│ battery_service  │      │ LSTM Models       │
│ supply_chain...  │      │ XGBoost/LightGBM  │
│ fleet_service    │      │ Scikit-learn      │
└────────┬─────────┘      └───────────────────┘
         │
    ┌────┴─────────────────┬──────────────┐
    │                      │              │
┌───▼──────┐      ┌────────▼────┐   ┌───▼──────────┐
│ MongoDB  │      │   Neo4j     │   │    Redis     │
│(27017)   │      │  (7687)     │   │  (6379)      │
│          │      │             │   │              │
│Operational    │Supply Chain  │   │Real-time     │
│Data Store    │Graph DB      │   │Cache         │
└──────────┘      └─────────────┘   └──────────────┘
```

---

## Component Details

### 1. Frontend Layer (React + Next.js)

**Location:** `/frontend`

**Technology Stack:**
- React 18 - UI component library
- Next.js 14 - Full-stack framework with SSR
- Tailwind CSS - Utility-first styling
- Recharts - Data visualization
- Axios - HTTP client
- TypeScript - Type safety

**Key Pages:**
- `/` - Landing page with quick links
- `/battery` - Battery health dashboard
- `/supply-chain` - Supply chain risk map
- `/fleet` - Fleet readiness assessment

**Components:**
- `BatteryDashboard.tsx` - SOH trends, degradation, maintenance alerts
- `SupplyChainMap.tsx` - Geopolitical risks, supplier profiles
- `FleetTable.tsx` - Vehicle readiness scoring, transition plans

**State Management:**
- React Hooks for local state
- Axios for API calls
- Real-time updates via Redis polling

---

### 2. API Layer (FastAPI)

**Location:** `/backend/main.py`

**Technology Stack:**
- FastAPI - Modern async Python web framework
- Uvicorn - ASGI web server
- Pydantic - Data validation
- CORS middleware - Cross-origin requests

**Architecture:**
```
main.py (entry point)
├── routes/
│   ├── battery.py - Battery prediction endpoints
│   ├── supply_chain.py - Supply chain risk endpoints
│   └── fleet.py - Fleet readiness endpoints
├── services/ (business logic - TBD in full implementation)
│   ├── battery_service.py
│   ├── supply_chain_service.py
│   └── fleet_service.py
└── models/ (ML models - TBD)
    ├── battery_soh_lstm.pkl
    ├── fleet_readiness.pkl
    └── scaler.pkl
```

**Key Endpoints:**
```
POST   /api/v1/predict/battery-soh           → Predict battery health
GET    /api/v1/battery/{vehicle_id}          → Get battery history
GET    /api/v1/battery/fleet-summary         → Fleet aggregate metrics

GET    /api/v1/supply-chain/risk-score       → Overall risk assessment
GET    /api/v1/supply-chain/suppliers        → Supplier risk profiles
GET    /api/v1/supply-chain/supplier/{id}    → Supplier details
POST   /api/v1/supply-chain/geopolitical-events → Log risk events

POST   /api/v1/fleet/readiness-check         → Vehicle EV readiness
GET    /api/v1/fleet/vehicles                → Fleet readiness summary
POST   /api/v1/fleet/electrification-plan    → Transition roadmap
GET    /api/v1/fleet/charging-infrastructure → Infrastructure requirements
GET    /api/v1/fleet/carbon-tracking         → Net-zero progress
```

---

### 3. Data Layer

#### MongoDB (Document Store)

**Purpose:** Operational data storage
- Vehicle telemetry records
- Battery history & degradation curves
- Fleet maintenance logs
- Supply chain events
- Supplier profiles

**Collections (proposed):**
```
vehicles/
├── _id: ObjectId
├── vehicle_id: "T001"
├── vehicle_type: "urban"
├── battery_history: [...]
├── maintenance_records: [...]
└── electrification_status: "ready"

suppliers/
├── _id: ObjectId
├── supplier_id: "LTH_001"
├── country: "China"
├── materials: ["Lithium", ...]
├── risk_profile: {...}
└── historical_events: [...]
```

#### Neo4j (Graph Database)

**Purpose:** Supply chain relationship modeling
- Supplier → Material → Refinery relationships
- Geopolitical influence propagation
- Risk correlation networks

**Graph Model:**
```
(Lithium_Mine) -[:MINED_BY]-> (Supplier)
(Supplier) -[:SHIPS_TO]-> (Port)
(Port) -[:AFFECTED_BY]-> (Geopolitical_Event)
(Geopolitical_Event) -[:IMPACTS]-> (Supplier)
```

#### Redis (Cache Layer)

**Purpose:** Real-time data caching
- Battery SOH calculations (TTL: 5 minutes)
- Supply chain risk scores (TTL: 1 hour)
- Session management
- Rate limiting counters

---

### 4. Machine Learning Models

#### Battery SOH Prediction

**Architecture:** LSTM (Long Short-Term Memory)
```
Input (Time-series):
  ├── Voltage readings (300 samples)
  ├── Current measurements
  ├── Temperature data
  └── Charge cycle count
         ↓
    LSTM Layer (128 units)
         ↓
    Dense Layer (64 units)
         ↓
    Output: SOH% (0-100)
```

**Training Data:**
- Synthetic EV battery cycles
- Public battery degradation datasets
- OEM battery datasheets

**Performance Metrics:**
- RMSE < 3% on test set
- Inference time < 100ms per prediction
- Confidence score output

#### Fleet Readiness Scoring

**Algorithm:** Gradient Boosting (XGBoost/LightGBM)
```
Input Features:
  ├── Daily distance (km)
  ├── Dwell time (hours)
  ├── Payload capacity (kg)
  ├── Vehicle age (years)
  ├── Annual utilization (hours)
  └── Vehicle type (categorical)
         ↓
    Feature Engineering (Scikit-learn)
         ↓
    XGBoost Classifier
         ↓
    Output: Readiness Score (0-100)
```

**Performance:**
- Accuracy > 90% vs expert baseline
- Real-time scoring capability

#### Supply Chain Risk Assessment

**Method:** Multi-factor composite scoring
```
Risk Score = 0.4×Geopolitical + 0.3×Concentration + 0.2×Quality + 0.1×Logistics

Geopolitical Risk:
  ├── Sanctions (binary flag)
  ├── Political stability index
  ├── Trade dispute status
  └── Export restrictions

Concentration Risk:
  ├── Supplier count in category
  ├── Herfindahl index
  └── Geographic diversity

Quality Risk:
  ├── Defect rates from suppliers
  ├── Inspection failure rates
  └── Historical quality issues

Logistics Risk:
  ├── Average lead time
  ├── Port congestion
  └── Shipping delays
```

---

## Data Flow Diagrams

### Battery Prediction Flow

```
1. User submits vehicle data (web form)
                ↓
2. Frontend sends POST /api/v1/predict/battery-soh
                ↓
3. Backend receives & validates Pydantic model
                ↓
4. Load pre-trained LSTM model from disk
                ↓
5. Preprocess input data (normalization via Scaler)
                ↓
6. Run inference (LSTM forward pass)
                ↓
7. Generate prediction output + confidence
                ↓
8. Store in MongoDB battery collection
                ↓
9. Cache in Redis for 5 minutes
                ↓
10. Return BatteryHealthResponse to frontend
                ↓
11. Frontend renders charts and alerts
```

### Supply Chain Risk Update Flow

```
1. Admin logs geopolitical event via UI
                ↓
2. POST /api/v1/supply-chain/geopolitical-events
                ↓
3. Backend validates event data
                ↓
4. Store in MongoDB events collection
                ↓
5. Query affected suppliers from Neo4j graph
                ↓
6. Recalculate risk scores for all suppliers
                ↓
7. Update MongoDB supplier risk profiles
                ↓
8. Invalidate Redis cache
                ↓
9. Emit WebSocket event (future enhancement)
                ↓
10. Frontend receives update notification
                ↓
11. Refresh supply chain risk dashboard
```

### Fleet Readiness Assessment Flow

```
1. User inputs vehicle operational data
                ↓
2. POST /api/v1/fleet/readiness-check
                ↓
3. Backend receives VehicleOperationalData
                ↓
4. Feature engineering (distance→category, etc.)
                ↓
5. Load pre-trained XGBoost model
                ↓
6. Run inference on feature vector
                ↓
7. Map score to readiness level & EV model recommendation
                ↓
8. Generate transition timeline
                ↓
9. Calculate TCO impact analysis
                ↓
10. Store assessment in MongoDB
                ↓
11. Return FleetReadinessResponse
                ↓
12. Frontend displays readiness score, recommendations, timeline
```

---

## Deployment Architecture

### Local Development

```
Docker Network (ev-network)
├── api (FastAPI) ↔ Port 8000
├── frontend (Next.js) ↔ Port 3000
├── mongo ↔ Port 27017
├── neo4j ↔ Ports 7474, 7687
└── redis ↔ Port 6379
```

### Production (AWS)

```
┌─────────────────────────────────────────────┐
│         AWS CloudFront (CDN)                 │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│    AWS S3 (Frontend static assets)           │
│    + CloudFront Distribution                 │
└──────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│    AWS Application Load Balancer             │
│    (Port 443 - HTTPS)                       │
└────────┬──────────────────────────┬─────────┘
         │                          │
┌────────▼────────────┐   ┌────────▼──────────────┐
│ ECS Fargate         │   │ ECS Fargate           │
│ (FastAPI)           │   │ (Next.js - optional)  │
│ ├─ Task 1           │   │ ├─ Task 1             │
│ ├─ Task 2           │   │ └─ Task 2             │
│ └─ Task 3           │   └───────────────────────┘
└────────┬────────────┘
         │
    ┌────┴──────────────────┬──────────────┐
    │                       │              │
┌───▼──────────┐  ┌────────▼────┐  ┌─────▼──────┐
│AWS RDS       │  │AWS Neptune  │  │AWS         │
│(MongoDB)     │  │(Neo4j)      │  │ElastiCache │
│Multi-AZ      │  │Multi-AZ     │  │(Redis)     │
│Backup enabled│  │Automated    │  │Cluster     │
│              │  │snapshots    │  │mode        │
└──────────────┘  └─────────────┘  └────────────┘
```

---

## Performance Considerations

### API Performance Targets
- Battery prediction: < 500ms
- Supply chain risk query: < 1000ms  
- Fleet readiness: < 300ms
- Overall API response: < 2s (p95)

### Optimization Strategies
- Index MongoDB on frequently queried fields
- Use Redis caching for repeated queries
- Implement pagination for large result sets
- Compress API responses (gzip)
- Lazy-load components in frontend
- Code-split React bundles

### Scalability Limits
- **Current**: ~100 concurrent users
- **Scaled**: ~10,000 concurrent users (with infrastructure upgrades)

---

## Security Architecture

```
┌──────────────────────────────────────┐
│      HTTPS/TLS (In Transit)           │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│   AWS Secrets Manager                 │
│  (Database credentials, API keys)     │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│  VPC Security Groups                  │
│  (Network isolation)                  │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│  Database Encryption at Rest          │
│  (MongoDB, Neo4j)                     │
└──────────────────────────────────────┘
```

---

## Future Enhancements

1. **Real-time Updates**: WebSocket integration for live dashboard
2. **Advanced ML**: Ensemble models, transfer learning
3. **Multi-language**: Support for regional languages
4. **Mobile App**: React Native or Flutter
5. **GraphQL API**: GraphQL layer on top of REST
6. **Advanced Analytics**: Apache Superset integration
7. **Blockchain**: Supply chain traceability on blockchain
8. **IoT Integration**: Direct SCADA/BMS connectivity
