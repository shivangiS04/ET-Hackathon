# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Option 1: Docker Compose (Recommended)

```bash
# Navigate to project
cd /Users/shivangisingh/Desktop/ET-Hackathon

# Start all services
docker-compose up

# Wait ~30 seconds for services to initialize...
```

**Now access:**
- 🌐 **Frontend**: http://localhost:3000
- 📚 **API Docs**: http://localhost:8000/docs
- 📊 **Live API**: http://localhost:8000

**Stop services:**
```bash
docker-compose down
```

---

### Option 2: Manual Setup (Advanced)

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
# API will be available at http://localhost:8000
```

#### Frontend (in new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# UI will be available at http://localhost:3000
```

---

## 📊 Exploring the Platform

### 1. Home Dashboard
Visit **http://localhost:3000**

You'll see:
- Platform overview
- Quick access cards to three main dashboards
- Statistics and key metrics
- API documentation link

### 2. Battery Health Dashboard
**http://localhost:3000/battery**

**Features:**
- Fleet average SOH: **92.3%** (Healthy)
- SOH distribution chart
- Historical trend visualization
- Maintenance alerts with urgency levels
- 6-month degradation forecast

**Key Metric:**
- Average fleet state-of-health: 87.5%
- 8 vehicles needing maintenance within 30 days

### 3. Supply Chain Risk Map
**http://localhost:3000/supply-chain**

**Features:**
- Overall risk score: **0.68** (High - requires attention)
- Risk breakdown by category:
  - Geopolitical: 75%
  - Supplier Concentration: 72%
  - Quality Deviations: 45%
  - Logistics: 58%
- Top 3 risk factors with impact scores
- Geographic risk heatmap (China 92%, DR Congo 85%, etc.)
- Supplier risk assessment table

**Critical Suppliers:**
1. China National Mineral (Lithium) - Risk 78
2. Glencore DRC (Cobalt) - Risk 82
3. Vale Indonesia (Nickel) - Risk 55
4. CATL Fujian (LFP Cells) - Risk 65

### 4. Fleet Readiness Assessment
**http://localhost:3000/fleet**

**Features:**
- Fleet size: 58 vehicles
- EV ready: 72.4% (42 vehicles)
- Individual vehicle readiness scores
- 3-phase transition timeline (Q1-Q4 2025)
- Financial projections

**Fleet Status:**
```
T001 Delhi-IP      → 94.5% Ready (✓)
T002 Mum-Pune      → 91.2% Ready (✓)
T003 Urban MG ZS   → 98.0% Ready (✓)
T004 Long-haul     → 65.3% Not Ready (✗)
```

**Financial Summary:**
- Total investment: ₹200 Cr
- Annual fuel savings: ₹35 Cr
- Payback period: 4.8 years
- NPV (10 years): ₹85 Cr

---

## 🔌 Testing the API

### Test Battery Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict/battery-soh \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "T001",
    "charge_history": [
      {
        "timestamp": "2024-12-01T10:00:00",
        "charge_percent": 100,
        "voltage_v": 3.9,
        "current_a": 0,
        "temperature_c": 25
      }
    ],
    "current_cycles": 1200,
    "ambient_temp_c": 30
  }'
```

**Expected Response:**
```json
{
  "vehicle_id": "T001",
  "current_soh": 92.3,
  "remaining_useful_life_days": 1825,
  "degradation_rate_percent_per_year": 8.2,
  "confidence_score": 0.925,
  "next_maintenance_days": 90,
  "risk_level": "low",
  "recommendation": "Continue normal operations. Schedule routine maintenance."
}
```

### Test Supply Chain Risk

```bash
curl http://localhost:8000/api/v1/supply-chain/risk-score
```

### Test Fleet Readiness

```bash
curl -X POST http://localhost:8000/api/v1/fleet/readiness-check \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "T001",
    "vehicle_type": "urban",
    "current_fuel": "diesel",
    "daily_distance_km": 120,
    "payload_capacity_kg": 5000,
    "dwell_time_hours": 8,
    "annual_utilization_hours": 2500,
    "current_age_years": 3
  }'
```

### View All Endpoints

Visit **http://localhost:8000/docs** for interactive API documentation

---

## 📁 Project Structure

```
ET-Hackathon/
├── backend/                    # FastAPI backend
│   ├── main.py                 # Entry point
│   ├── requirements.txt         # Python dependencies
│   ├── routes/
│   │   ├── battery.py          # Battery endpoints
│   │   ├── supply_chain.py     # Supply chain endpoints
│   │   └── fleet.py            # Fleet endpoints
│   └── Dockerfile
│
├── frontend/                   # React/Next.js frontend
│   ├── app/
│   │   ├── page.tsx            # Home page
│   │   ├── battery/            # Battery dashboard
│   │   ├── supply-chain/       # Supply chain dashboard
│   │   ├── fleet/              # Fleet dashboard
│   │   └── layout.tsx          # Root layout
│   ├── components/
│   │   ├── BatteryDashboard.tsx
│   │   ├── SupplyChainMap.tsx
│   │   └── FleetTable.tsx
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml          # Service orchestration
├── README.md                   # Project overview
├── QUICKSTART.md              # This file
├── DEPLOYMENT.md              # Deployment guide
└── ARCHITECTURE.md            # Technical architecture
```

---

## 🐛 Troubleshooting

### Services Won't Start

**Check logs:**
```bash
docker-compose logs api
docker-compose logs frontend
docker-compose logs mongo
```

**Restart everything:**
```bash
docker-compose down
docker-compose up --build
```

### Port Already in Use

If ports 3000, 8000, 27017, etc. are in use:

```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### API Returns 500 Error

Check MongoDB connection:
```bash
docker exec -it mongo mongosh --eval "db.adminCommand('ping')"
```

Check API logs:
```bash
docker-compose logs api --tail=50
```

### Frontend Won't Load Data

Check if API is accessible:
```bash
curl http://localhost:8000/
```

Check browser console for errors (F12 → Console)

---

## 📝 Demo Walkthrough (5 Minutes)

**Scenario:** Fleet operator evaluating EV transition

### Slide 1: Current State
- Show Battery Health Dashboard
- "Fleet average SOH: 87.5% - healthy but degrading"
- "8 vehicles need maintenance in 30 days"

### Slide 2: Risk Assessment
- Show Supply Chain Risk Map
- "Overall risk: 0.68 (High)"
- "Top risk: China has 45% of lithium supply"
- "45% cobalt from politically unstable DR Congo"

### Slide 3: Transition Plan
- Show Fleet Readiness Assessment
- "72.4% of fleet ready for EV transition"
- "42 vehicles can transition immediately"
- "16 vehicles need 6-12 month planning"

### Slide 4: Financial Case
- "₹200 Cr investment → 4.8 year payback"
- "₹43 Cr annual savings (fuel + maintenance)"
- "₹85 Cr NPV over 10 years"
- "1,250 tons CO₂ reduction annually"

### Slide 5: Call to Action
- "Use this platform to:"
  - ✓ Track battery health in real-time
  - ✓ Manage supply chain risks
  - ✓ Plan fleet electrification
  - ✓ Achieve net-zero commitments

---

## 🎯 Next Steps

1. **Customize Data**: Replace sample data with real fleet/supply chain data
2. **Integrate APIs**: Connect to OEM, battery management, and logistics systems
3. **Deploy**: Follow DEPLOYMENT.md for production setup
4. **Monitor**: Set up alerts for SOH degradation and supply chain risks
5. **Scale**: Add more vehicles, suppliers, and geopolitical data sources

---

## 📚 Resources

- **API Docs**: http://localhost:8000/docs
- **Architecture**: See ARCHITECTURE.md
- **Deployment**: See DEPLOYMENT.md
- **Code**: All frontend/backend code in respective directories

---

## ✅ Success Criteria (for Hackathon)

Your platform should achieve:

| Metric | Target | Status |
|--------|--------|--------|
| Battery Prediction Accuracy | RMSE < 3% | ⏳ |
| Supply Chain Risk Detection | 7-14 day lead time | ⏳ |
| Fleet Readiness Accuracy | >90% vs expert | ⏳ |
| API Response Time | <500ms | ⏳ |
| Dashboard Load Time | <1 second | ⏳ |
| Demo Duration | 5 minutes crisp | ⏳ |

---

**Questions?** Check http://localhost:8000/docs for API documentation.

**Ready to build?** Start with backend services, then connect the frontend!
