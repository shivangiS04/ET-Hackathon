# AI for Industrial EV Supply Chain & Asset Intelligence

**Accelerating Net Zero Through Predictive Asset Management & Supply Chain Visibility**

## 🎯 Problem Statement

India is accelerating EV adoption but industrial fleet operators lack the AI tools to manage EV procurement, battery lifecycle, charging infrastructure, and maintenance operations with operational rigor. Meanwhile, EV manufacturers face critical supply chain complexity without adequate visibility.

This platform addresses both challenges simultaneously through:

1. **EV Asset Performance Management (APM)** - Predictive battery health, degradation forecasting, maintenance triggers
2. **Fleet Electrification Readiness** - Optimal EV replacement mapping with confidence scores
3. **EV Supply Chain Risk Intelligence** - Multi-tier battery material tracking, supplier concentration risks
4. **Manufacturing Quality Intelligence** - Quality drift detection, traceability from cell to pack to vehicle
5. **Net Zero Progress Tracking** - Carbon intelligence and electrification progress monitoring

---

## 🏗️ Architecture

### Tech Stack

**Frontend Layer:**
- React 18 + Next.js 14
- Tailwind CSS + Recharts
- Real-time dashboard updates

**API Layer:**
- FastAPI (Python) - 8000
- Unicorn ASGI server
- OpenAPI documentation

**Data Layer:**
- MongoDB (27017) - Operational data
- Neo4j (7687) - Supply chain graph database
- Redis (6379) - Caching & real-time updates

**ML/Inference:**
- TensorFlow 2.13.0 + LSTM models
- XGBoost & LightGBM for ensemble
- Battery degradation prediction engine

**Data Pipeline:**
- Pandas + Scikit-learn preprocessing
- Scheduled ETL tasks
- Feature engineering pipeline

---

## 📂 Project Structure

```
ET-Hackathon/
├── backend/                      # FastAPI backend
│   ├── main.py                   # Entry point
│   ├── requirements.txt           # Python dependencies
│   ├── models/                   # ML models
│   │   ├── battery_soh_lstm.pkl
│   │   ├── fleet_readiness.pkl
│   │   └── scaler.pkl
│   ├── routes/                   # API endpoints
│   │   ├── battery.py            # Battery SOH prediction
│   │   ├── supply_chain.py       # Supply chain risk
│   │   └── fleet.py              # Fleet readiness
│   ├── services/                 # Business logic
│   │   ├── battery_service.py
│   │   ├── supply_chain_service.py
│   │   └── fleet_service.py
│   └── data/                     # Synthetic training data
│       └── train_data.csv
│
├── frontend/                     # React frontend
│   ├── package.json
│   ├── app/
│   │   ├── page.tsx              # Dashboard home
│   │   ├── battery/page.tsx      # Battery health
│   │   ├── supply-chain/page.tsx # Risk map
│   │   └── fleet/page.tsx        # Fleet readiness
│   ├── components/
│   │   ├── BatteryDashboard.tsx
│   │   ├── SupplyChainMap.tsx
│   │   └── FleetTable.tsx
│   └── public/
│
├── data/                         # Data pipeline
│   ├── train_data.csv
│   ├── supply_chain_graph.json
│   └── ETL pipeline description
│
├── docker-compose.yml            # Service orchestration
├── Dockerfile.backend            # Backend container
├── Dockerfile.frontend           # Frontend container
│
├── architecture.md               # System design
├── DEPLOYMENT.md                 # Deployment guide
└── TESTING.md                    # Testing checklist
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.10+

### Clone & Setup

```bash
cd /Users/shivangisingh/Desktop/ET-Hackathon

# Start all services
docker-compose up

# Services will be available at:
# - Frontend: http://localhost:3000
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - MongoDB: localhost:27017
# - Neo4j: http://localhost:7474
```

### Manual Setup (Development)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## 📊 API Endpoints

### Battery SOH Prediction
- `POST /api/v1/predict/battery-soh` - Predict battery state of health
- `GET /api/v1/battery/{vehicle_id}` - Get battery history

### Supply Chain Risk
- `GET /api/v1/supply-chain/risk-score` - Overall supply chain risk
- `GET /api/v1/supply-chain/supplier/{supplier_id}` - Supplier risk details
- `POST /api/v1/supply-chain/geopolitical-events` - Add geopolitical event

### Fleet Readiness
- `POST /api/v1/fleet/readiness-check` - Analyze fleet for EV readiness
- `GET /api/v1/fleet/vehicles` - List all vehicles with scores
- `POST /api/v1/fleet/electrification-plan` - Generate transition plan

---

## 📈 Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Battery Degradation Prediction Accuracy | RMSE < 3% | ⏳ |
| Supply Chain Risk Detection Lead Time | 7-14 days | ⏳ |
| Fleet Matching Accuracy | >90% vs expert baseline | ⏳ |
| API Response Time | <500ms | ⏳ |
| Demo Presentation | 5 mins crisp | ⏳ |

---

## 🔧 Development Workflow

### Adding a New Feature
1. Create route in `backend/routes/`
2. Implement service logic in `backend/services/`
3. Add React component in `frontend/components/`
4. Update dashboard page in `frontend/app/`
5. Test via API docs at `http://localhost:8000/docs`

### Running Tests
```bash
cd backend
pytest tests/ -v
```

---

## 📚 Documentation

- **[Architecture Diagram](./architecture.md)** - System design & data flow
- **[Deployment Guide](./DEPLOYMENT.md)** - Production deployment
- **[Testing Checklist](./TESTING.md)** - QA procedures
- **[API Reference](./api-reference.md)** - Complete endpoint docs

---

## 🎬 Demo Video Script

**Scenario:** Industrial fleet operator evaluating EV transition

1. **Battery Health Dashboard** - Show 92.3% SOH with 1,825-day RUL prediction
2. **Supply Chain Risk Map** - Geographic heatmap of supplier risks (China 45%, Australia 18%, Chile 10%)
3. **Fleet Readiness Table** - Show 3 ready vehicles (Delhi-IP 94.5%, Mum-Pune 91.2%, Urban MG 98.0%), 1 not ready (Long-haul 65.3%)
4. **Value Prop** - "Reduce EV transition risk through predictive intelligence"

---

## 📋 Evaluation Criteria (2026 Hackathon)

| Criteria | Weight | Evidence |
|----------|--------|----------|
| Innovation | 25% | Multi-agent architecture, graph-based supply chain analysis |
| Business Impact | 25% | Reduces fleet downtime, enables data-driven procurement |
| Technical Excellence | 20% | LSTM models, real-time dashboard, API design |
| Scalability | 15% | Docker/Kubernetes ready, multi-tenant database design |
| User Experience | 15% | Intuitive dashboards, mobile-responsive design |

---

## 👥 Team Notes

- **Data Sources:** Synthetic EV telematics, battery curves, supply chain networks
- **Assumptions:** Battery degradation follows predictable patterns; supplier risk is quantifiable
- **Known Limitations:** Demo uses simulated data; real deployment requires live BMS/SCADA feeds
- **Next Steps:** Integrate with real OEM APIs, add anomaly detection, implement predictive maintenance scheduling

---

**Built for ET AI Hackathon 2026** 🚀
