# Deployment Guide

## Local Development Setup

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.10+
- Git

### Quick Start with Docker Compose

```bash
cd /Users/shivangisingh/Desktop/ET-Hackathon

# Start all services
docker-compose up

# First time setup - wait ~30 seconds for services to initialize
# Then access:
# - Frontend: http://localhost:3000
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - MongoDB: localhost:27017
# - Neo4j: http://localhost:7474
# - Redis: localhost:6379
```

### Manual Development Setup (without Docker)

**Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
# API available at http://localhost:8000
```

**Frontend (new terminal):**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# UI available at http://localhost:3000
```

---

## Service Ports & Access

| Service | Port | Access URL | Credentials |
|---------|------|-----------|-------------|
| FastAPI | 8000 | http://localhost:8000/docs | N/A |
| React Frontend | 3000 | http://localhost:3000 | N/A |
| MongoDB | 27017 | localhost:27017 | admin/password |
| Neo4j | 7474 | http://localhost:7474 | neo4j/password |
| Neo4j Bolt | 7687 | bolt://localhost:7687 | neo4j/password |
| Redis | 6379 | localhost:6379 | N/A |

---

## Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database
MONGODB_URL=mongodb://admin:password@mongo:27017
NEO4J_URL=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
REDIS_URL=redis://redis:6379

# API
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
```

---

## API Endpoints Reference

### Battery SOH Prediction
```bash
# Predict battery health
POST /api/v1/predict/battery-soh
Content-Type: application/json

{
  "vehicle_id": "T001",
  "charge_history": [...],
  "current_cycles": 1200,
  "ambient_temp_c": 35
}

# Get battery history
GET /api/v1/battery/{vehicle_id}?days=30

# Fleet summary
GET /api/v1/battery/fleet-summary
```

### Supply Chain Risk
```bash
# Get overall risk score
GET /api/v1/supply-chain/risk-score

# Get supplier risks
GET /api/v1/supply-chain/suppliers

# Get specific supplier details
GET /api/v1/supply-chain/supplier/{supplier_id}

# Add geopolitical event
POST /api/v1/supply-chain/geopolitical-events
```

### Fleet Readiness
```bash
# Check vehicle readiness
POST /api/v1/fleet/readiness-check

# Get fleet summary
GET /api/v1/fleet/vehicles

# Generate transition plan
POST /api/v1/fleet/electrification-plan

# Get charging infrastructure plan
GET /api/v1/fleet/charging-infrastructure

# Get carbon tracking
GET /api/v1/fleet/carbon-tracking
```

---

## Testing the Platform

### Test Battery Prediction
```bash
curl -X POST http://localhost:8000/api/v1/predict/battery-soh \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "T001",
    "charge_history": [
      {"timestamp": "2024-12-01T10:00:00", "charge_percent": 100, "voltage_v": 3.9, "current_a": 0, "temperature_c": 25},
      {"timestamp": "2024-12-01T14:00:00", "charge_percent": 20, "voltage_v": 3.0, "current_a": 100, "temperature_c": 35}
    ],
    "current_cycles": 1200,
    "ambient_temp_c": 30
  }'
```

### Test Supply Chain Risk
```bash
curl -X GET http://localhost:8000/api/v1/supply-chain/risk-score

curl -X GET http://localhost:8000/api/v1/supply-chain/suppliers
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

---

## Production Deployment

### AWS Deployment (Recommended)

**Option 1: Using AWS ECS + Fargate**

```bash
# Build images
docker build -t ev-intelligence-api ./backend
docker build -t ev-intelligence-frontend ./frontend

# Tag for ECR
docker tag ev-intelligence-api:latest <aws-account>.dkr.ecr.<region>.amazonaws.com/ev-intelligence-api:latest
docker tag ev-intelligence-frontend:latest <aws-account>.dkr.ecr.<region>.amazonaws.com/ev-intelligence-frontend:latest

# Push to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-account>.dkr.ecr.<region>.amazonaws.com
docker push <aws-account>.dkr.ecr.<region>.amazonaws.com/ev-intelligence-api:latest
docker push <aws-account>.dkr.ecr.<region>.amazonaws.com/ev-intelligence-frontend:latest

# Deploy with Terraform or CloudFormation
```

**Option 2: Using AWS Lambda + API Gateway**

- Containerize FastAPI with FastAPI Lambda adapter
- Deploy frontend to S3 + CloudFront CDN
- Use RDS for MongoDB, Neptune for Neo4j
- Use ElastiCache for Redis

**Option 3: Using AWS AppRunner**

```bash
# Deploy directly from Docker image
aws apprunner create-service \
  --service-name ev-intelligence-api \
  --source-configuration ImageRepository={ImageIdentifier=<ecr-uri>,ImageRepositoryType=ECR}
```

### Database Backups

```bash
# MongoDB backup
mongodump --uri="mongodb://admin:password@mongo:27017" --out=/backups/mongo

# Neo4j backup
neo4j-admin backup --to-path=/backups/neo4j

# Restore from backup
mongorestore --uri="mongodb://admin:password@mongo:27017" /backups/mongo
```

### Monitoring & Logging

- **Backend**: Use CloudWatch for Python logs
- **Frontend**: Use CloudWatch for Next.js logs
- **Metrics**: Enable CloudWatch monitoring on ECS tasks
- **Alarms**: Set up CloudWatch alarms for high error rates

---

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy EV Intelligence

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker images
        run: |
          docker build -t ev-api:${{ github.sha }} ./backend
          docker build -t ev-frontend:${{ github.sha }} ./frontend
      
      - name: Push to ECR
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}
          docker push ${{ secrets.ECR_REGISTRY }}/ev-api:${{ github.sha }}
          docker push ${{ secrets.ECR_REGISTRY }}/ev-frontend:${{ github.sha }}
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster ev-cluster \
            --service ev-service \
            --force-new-deployment
```

---

## Scaling Considerations

### Horizontal Scaling
- **API**: Scale FastAPI behind load balancer (ALB)
- **Frontend**: Serve from CloudFront CDN
- **Database**: MongoDB Atlas with auto-scaling
- **Cache**: Redis Cluster mode

### Vertical Scaling
- **Memory**: Increase for LSTM model inference
- **CPU**: Match expected QPS (requests per second)

---

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs api
docker-compose logs frontend

# Restart specific service
docker-compose restart api
```

### Database connection errors
```bash
# Verify MongoDB is running
docker exec -it mongo mongosh --eval "db.adminCommand('ping')"

# Verify Neo4j is running
curl http://localhost:7474
```

### API returning 500 errors
```bash
# Check API logs
docker-compose logs api

# Verify database connection in API container
docker exec -it ev-intelligence-api python -c "from pymongo import MongoClient; print(MongoClient('mongodb://mongo:27017').server_info())"
```

---

## Performance Optimization

- Enable Redis caching for frequent queries
- Implement pagination for large result sets
- Use database indexes on frequently queried fields
- Compress API responses (gzip)
- Minify and bundle frontend assets
- Use CDN for static assets

---

## Security

- Rotate database credentials regularly
- Use secrets manager (AWS Secrets Manager, Vault)
- Enable HTTPS/TLS for all communications
- Implement API authentication (JWT tokens)
- Use VPC security groups to restrict database access
- Enable audit logging for database operations
- Regular security scanning of Docker images

---

For more help, check API documentation at http://localhost:8000/docs
