# Environment Variables Setup Guide

## Overview

This guide helps you set up the correct environment variables for both local development and Vercel deployment.

---

## Frontend Environment Variables

### Local Development (`.env.local`)

Create a `.env.local` file in the `frontend/` directory:

```bash
cd frontend
touch .env.local
```

Add these variables:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Node Environment
NODE_ENV=development
```

**Note:** Use `NEXT_PUBLIC_` prefix to expose variables to the browser. Never use it for secrets!

### Production (Vercel)

Set in Vercel Dashboard:

1. Go to https://vercel.com/dashboard
2. Select your project
3. **Settings** → **Environment Variables**
4. Add:

| Variable | Value | When to Use |
|----------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://et-hackathon-backend.vercel.app` | After backend is deployed |
| `NODE_ENV` | `production` | Auto-set by Vercel |

---

## Backend Environment Variables

### Local Development (`.env`)

Create a `.env` file in the `backend/` directory:

```bash
cd backend
cp ../.env.example .env
```

Edit `.env` with these values:

```env
# Database Configuration
MONGODB_URL=mongodb://localhost:27017/ev_intelligence
MONGODB_DATABASE=ev_intelligence
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password

# Neo4j Configuration (optional, can use postgres)
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_PLUGINS=["apoc"]

# Redis Configuration
REDIS_URL=redis://localhost:6379

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_TITLE=EV Supply Chain & Asset Intelligence API
LOG_LEVEL=INFO

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:3000
NODE_ENV=development

# Machine Learning
MODEL_PATH=./models
BATCH_SIZE=32
MAX_WORKERS=4

# Feature Flags
ENABLE_CACHING=true
CACHE_TTL_SECONDS=300
ENABLE_LOGGING=true
```

### Using Docker Compose (Easiest for Local)

The `docker-compose.yml` already includes all services. Just run:

```bash
docker-compose up -d
```

This automatically:
- ✅ Starts PostgreSQL with sample data
- ✅ Starts MongoDB
- ✅ Starts Redis
- ✅ Starts Neo4j
- ✅ Creates all tables and indexes

### Production (Vercel)

Set in Vercel via CLI or dashboard:

```bash
vercel env add MONGODB_URL
# Enter: <your MongoDB Atlas URL>

vercel env add REDIS_URL
# Enter: <your Redis Cloud URL>

vercel env add NEO4J_URL
# Enter: <your Neo4j AuraDB URL>
```

Or use Vercel CLI to bulk import:

```bash
vercel env pull .env.production.local
# Edit the file with production values
```

---

## Database Connection Strings

### MongoDB

**Local (Docker):**
```
mongodb://admin:password@localhost:27017/ev_intelligence
```

**Cloud (MongoDB Atlas):**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create cluster
3. Copy connection string: `mongodb+srv://username:password@cluster.mongodb.net/ev_intelligence`
4. Use in `MONGODB_URL`

### PostgreSQL

**Local (Docker):**
```
postgresql://ev_user:ev_password@localhost:5432/ev_fleet_db
```

**Local (Manual):**
```
psql -h localhost -U ev_user -d ev_fleet_db
```

**Cloud (Render, Railway, etc.):**
1. Create PostgreSQL database in your provider
2. Copy connection string
3. Use in environment

### Redis

**Local (Docker):**
```
redis://localhost:6379
```

**Cloud (Redis Cloud):**
1. Go to https://redis.com/cloud
2. Create database
3. Copy connection string: `redis://default:password@host:port`

### Neo4j

**Local (Docker):**
```
bolt://localhost:7687
```

**Cloud (Neo4j AuraDB):**
1. Go to https://neo4j.com/cloud/aura
2. Create instance
3. Copy connection URI

---

## Environment Variable References

### For Frontend

```env
# Required
NEXT_PUBLIC_API_URL=<backend-url>

# Optional
NODE_ENV=production|development
NEXT_PUBLIC_ANALYTICS_ID=<your-analytics-id>
NEXT_PUBLIC_SENTRY_DSN=<your-sentry-dsn>
```

### For Backend

```env
# Required
MONGODB_URL=<connection-string>
API_HOST=0.0.0.0
API_PORT=8000

# Optional but Recommended
REDIS_URL=<connection-string>
NEO4J_URL=<connection-string>
LOG_LEVEL=INFO|DEBUG|WARNING|ERROR
ENABLE_CACHING=true|false
CACHE_TTL_SECONDS=300
```

---

## Vercel CLI Environment Setup

### Install Vercel CLI

```bash
npm install -g vercel
```

### Login to Vercel

```bash
vercel login
```

### Set Environment Variables

**For Frontend Project:**

```bash
# Link to your project
cd frontend
vercel link

# Add environment variables
vercel env add NEXT_PUBLIC_API_URL
# (follow prompts)

# Verify
vercel env ls
```

**For Backend Project:**

```bash
# Link to your project
cd backend
vercel link

# Add environment variables
vercel env add MONGODB_URL
vercel env add REDIS_URL
vercel env add NEO4J_URL

# Verify
vercel env ls
```

### Pull Environment Variables Locally

```bash
vercel env pull .env.production.local
```

---

## GitHub Actions / CI/CD

If setting up automated deployments, add secrets to GitHub:

1. Go to your GitHub repo
2. **Settings** → **Secrets and variables** → **Actions**
3. Add these secrets:

```
MONGODB_URL = <your-mongodb-connection>
REDIS_URL = <your-redis-connection>
```

Then in your workflow file (e.g., `.github/workflows/deploy.yml`):

```yaml
env:
  MONGODB_URL: ${{ secrets.MONGODB_URL }}
  REDIS_URL: ${{ secrets.REDIS_URL }}
```

---

## Common Environment Variable Issues

### Issue: API URL not updating in frontend

**Solution:**
- Add `NEXT_PUBLIC_` prefix to variable name
- Redeploy after changing the variable
- Clear browser cache

### Issue: "Cannot connect to database" error

**Solution:**
- Verify connection string format
- Check database is running and accessible
- Verify username/password
- Check firewall/network rules

### Issue: Variables not available in production

**Solution:**
- Use Vercel dashboard or CLI to set them
- Don't commit `.env` files to git
- Ensure variables are set for Production environment (not just Preview)

### Issue: Secret values exposed in logs

**Solution:**
- Never log environment variables
- Use `***` masking in Vercel for sensitive data
- Rotate secrets regularly

---

## Security Best Practices

1. **Never commit `.env` files to git**
   ```bash
   # Already in .gitignore
   echo ".env*" >> .gitignore
   ```

2. **Use `.env.example` for documentation**
   ```bash
   # Keep this committed with placeholder values
   cp .env .env.example
   # Edit .env.example to remove sensitive data
   ```

3. **Rotate secrets regularly**
   - Change database passwords monthly
   - Update API keys quarterly
   - Revoke old tokens

4. **Use strong values**
   ```bash
   # Generate strong password (on Mac)
   openssl rand -base64 32
   ```

5. **Different values per environment**
   - Development: local values
   - Staging: test values
   - Production: real, secure values

---

## Quick Environment Checklists

### Local Development Setup ✓

- [ ] Create `frontend/.env.local`
- [ ] Create `backend/.env`
- [ ] `.env` files in `.gitignore`
- [ ] Run `docker-compose up -d`
- [ ] Verify database connections
- [ ] Start backend: `uvicorn main:app --reload`
- [ ] Start frontend: `npm run dev`

### Vercel Deployment Setup ✓

- [ ] Install Vercel CLI
- [ ] Login with `vercel login`
- [ ] Link projects with `vercel link`
- [ ] Set `NEXT_PUBLIC_API_URL` in frontend project
- [ ] Set database URLs in backend project
- [ ] Verify in Vercel dashboard
- [ ] Test API connectivity

### Production Verification ✓

- [ ] Frontend loads without errors
- [ ] Backend API responds to requests
- [ ] Database connections work
- [ ] API documentation accessible at `/docs`
- [ ] Health check passes: `GET /health`
- [ ] Analytics working

---

## Need Help?

- Check Vercel logs: Dashboard → Deployments → View Details
- Check backend logs: `vercel logs <project-name>`
- Test API directly: `curl https://your-backend/health`
- Review env setup: `vercel env ls --environment production`

---

## Next Steps

1. ✅ Set up local `.env` files
2. ✅ Configure Vercel project environment variables
3. ✅ Deploy frontend to Vercel
4. ✅ Deploy backend to Vercel
5. ✅ Update `NEXT_PUBLIC_API_URL` in frontend
6. ✅ Test full deployment

You're ready to deploy! 🚀
