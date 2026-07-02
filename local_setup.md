# ET Hackathon 2026 - Local Setup Guide

**Platform:** EV Supply Chain & Asset Intelligence  
**Date:** June 2026  
**Setup Time:** ~15 minutes

---

## System Requirements Verified ✅

Your system has all required dependencies:

```
Node.js:        v20.17.0     ✅
npm:            11.11.0      ✅
Python:         3.12.2       ✅
pip:            (via conda)   ✅
Docker:         29.2.1       ✅
Docker Compose: 5.0.2        ✅
Git:            2.39.5       ✅
```

---

## Quick Start (5-minute setup)

### Option 1: Full Stack with Docker Compose (Recommended)

```bash
# 1. Navigate to project
cd /Users/shivangisingh/Desktop/ET-Hackathon

# 2. Start all services (PostgreSQL, Redis, MongoDB, Neo4j, Backend, Frontend)
docker-compose up

# 3. Wait for all services to start (~30-60 seconds)
# You'll see: "Backend running on http://localhost:8000"
# And:       "Frontend running on http://localhost:3000"
```

**That's it!** Access at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/docs (Swagger)
- **Health Check:** http://localhost:8000

---

### Option 2: Manual Setup (More Control)

Follow the step-by-step guide below.

---

## Step-by-Step Manual Setup

### Step 1: Backend Setup (Python/FastAPI)

```bash
# 1. Navigate to backend
cd /Users/shivangisingh/Desktop/ET-Hackathon/backend

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate
# On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start backend server
python -m uvicorn main:app --reload

# Backend running at: http://localhost:8000
# API Docs at: http://localhost:8000/docs
```

**Keep this terminal open** - backend is now running.

---

### Step 2: Frontend Setup (React/Next.js)

**Open a new terminal tab/window:**

```bash
# 1. Navigate to frontend
cd /Users/shivangisingh/Desktop/ET-Hackathon/frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# Frontend running at: http://localhost:3000
```

**Keep this terminal open** - frontend is now running.

---

### Step 3: Start Databases (Docker)

**Open another new terminal tab/window:**

```bash
# 1. Navigate to project root
cd /Users/shivangisingh/Desktop/ET-Hackathon

# 2. Start database containers
docker-compose up

# This starts:
# - PostgreSQL:  localhost:5432  (ev_user / ev_password)
# - Redis:       localhost:6379
# - MongoDB:     localhost:27017
# - Neo4j:       localhost:7687  (neo4j / password)
```

---

## Verifying Everything Works

### Test Backend API

```bash
# In a new terminal, test the health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2026-06-01T..."}

# Test battery validation endpoint
curl http://localhost:8000/api/v1/battery/validation/synthetic-test

# Expected: JSON with RMSE, MAE, R², MAPE metrics
```

### Test Frontend

Open browser to http://localhost:3000

Expected to see:
- ✅ Home page with India-focused content
- ✅ FAME-II and 30% adoption target stats
- ✅ Navigation working (Take a Tour button visible)
- ✅ All pages accessible

### Test API Documentation

Open http://localhost:8000/docs

Expected to see:
- ✅ Interactive Swagger UI
- ✅ 25+ endpoints listed
- ✅ Try-it-out functionality

---

## Accessing Different Pages

Once frontend is running at http://localhost:3000:

| Page | URL | Purpose |
|------|-----|---------|
| Home | http://localhost:3000 | India-focused homepage with FAME-II stats |
| Onboarding | http://localhost:3000/onboarding | 8-step guided tour |
| Battery | http://localhost:3000/battery | Battery health with confidence intervals |
| Supply Chain | http://localhost:3000/supply-chain | Supply chain risk analysis |
| Fleet | http://localhost:3000/fleet | Fleet readiness with financial metrics |
| Advanced Features | http://localhost:3000/advanced-features | Scenarios, anomalies, alerts |
| Reports | http://localhost:3000/reports | Report generation and export |
| Carbon Tracker | http://localhost:3000/carbon-tracker | Net zero roadmap and emissions |

---

## Troubleshooting

### Issue: Port 8000 already in use (Backend)

```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Then restart backend
python -m uvicorn main:app --reload

# Or run on different port
python -m uvicorn main:app --reload --port 8001
# Then access at http://localhost:8001
```

### Issue: Port 3000 already in use (Frontend)

```bash
# Kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Then restart frontend
npm run dev

# Or run on different port
npm run dev -- -p 3001
# Then access at http://localhost:3001
```

### Issue: Port 5432 already in use (PostgreSQL in Docker)

```bash
# Stop existing Docker containers
docker-compose down

# Then restart
docker-compose up
```

### Issue: Node modules issues

```bash
# Clear node modules and reinstall
rm -rf frontend/node_modules
rm frontend/package-lock.json
npm install --prefix frontend
```

### Issue: Python virtual environment issues

```bash
# Delete and recreate venv
rm -rf backend/venv
python -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

---

## Environment Variables (Optional)

Create `.env` file in backend directory for custom configuration:

```bash
# backend/.env
DATABASE_URL=postgresql://ev_user:ev_password@localhost:5432/ev_fleet_db
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://localhost:27017
NEO4J_URL=bolt://localhost:7687
JWT_SECRET_KEY=your-secret-key-here
```

---

## Database Access

### PostgreSQL

```bash
# Connect to PostgreSQL
psql -h localhost -U ev_user -d ev_fleet_db

# Password: ev_password

# View tables
\dt

# Example query
SELECT * FROM vehicles LIMIT 5;
```

### Redis

```bash
# Connect to Redis
redis-cli -h localhost

# View keys
KEYS *

# Check cache hit rate
INFO stats
```

### MongoDB

```bash
# Connect to MongoDB
mongosh mongodb://localhost:27017

# List databases
show dbs

# Use ev_database
use ev_database
```

---

## Performance Metrics

Once running, check platform performance:

```bash
# View Prometheus metrics (JSON format)
curl http://localhost:8000/metrics/json

# View Prometheus metrics (Prometheus format)
curl http://localhost:8000/metrics

# View API metrics
curl http://localhost:8000/api/v1/metrics
```

---

## Testing the Platform

### Test Battery Prediction API

```bash
curl -X POST http://localhost:8000/api/v1/predict/battery-soh \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "VEH001",
    "current_cycles": 500,
    "ambient_temp_c": 35,
    "charge_history": [
      {"current_a": 100, "temperature_c": 35, "timestamp": "2026-06-01T10:00:00"}
    ]
  }'
```

### Test Synthetic Validation

```bash
curl http://localhost:8000/api/v1/battery/validation/synthetic-test
```

### Test Carbon Tracking

```bash
curl http://localhost:8000/api/v1/analytics/carbon/tracking?fleet_size=156
```

---

## Stop All Services

### To stop everything cleanly:

```bash
# In frontend terminal: Ctrl+C
# In backend terminal: Ctrl+C
# In Docker terminal: Ctrl+C

# Or stop Docker services
docker-compose down

# To remove all volumes (database data)
docker-compose down -v
```

---

## Next Steps

1. **Explore the UI:** Navigate through all pages
2. **Test the API:** Use Swagger UI at http://localhost:8000/docs
3. **Check the dashboard:** Battery health, supply chain, fleet readiness
4. **View Carbon Tracker:** http://localhost:3000/carbon-tracker
5. **Run the tour:** http://localhost:3000/onboarding

---

## Common Commands

```bash
# Start everything with Docker
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose stop

# Remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Restart specific service
docker-compose restart backend

# Access backend shell
docker-compose exec backend bash

# View running containers
docker ps

# Check Docker logs
docker logs <container_id>
```

---

## Support & Debugging

If something doesn't work:

1. **Check ports:** `lsof -ti:8000` (backend), `lsof -ti:3000` (frontend)
2. **Check logs:** Terminal output or `docker logs`
3. **Verify services:** http://localhost:8000/health
4. **Clear cache:** Browser cache (Cmd+Shift+Delete on Chrome)
5. **Restart everything:** Stop all and `docker-compose up`

---

## Architecture Overview (Running Locally)

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Machine                             │
│                                                              │
│  ┌──────────────┐         ┌──────────────────────────────┐  │
│  │              │         │   Docker Compose             │  │
│  │  Port 3000   │         │  ┌──────────────────────────┐│  │
│  │  Frontend    │         │  │ PostgreSQL      :5432    ││  │
│  │  (Next.js)   │◄────────►  │ Redis           :6379    ││  │
│  │              │         │  │ MongoDB         :27017   ││  │
│  └──────────────┘         │  │ Neo4j           :7687    ││  │
│         ▲                  │  └──────────────────────────┘│  │
│         │                  └──────────────────────────────┘  │
│         │ HTTP                                               │
│         │                                                    │
│  ┌──────▼──────────────────────┐                            │
│  │   Port 8000                 │                            │
│  │   Backend API (FastAPI)     │                            │
│  │   - 8 Services              │                            │
│  │   - 25+ Endpoints           │                            │
│  │   - Real-time metrics       │                            │
│  └─────────────────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Ready to Go! 🚀

Your ET Hackathon platform is now running locally and ready for:
- ✅ Exploration and testing
- ✅ API integration testing
- ✅ Demo preparation
- ✅ Judge walkthrough
- ✅ Performance verification

Start with Option 1 (Docker Compose) for the simplest setup!
