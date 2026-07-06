# Vercel Deployment Guide - ET-Hackathon

This guide walks you through deploying the ET-Hackathon project (Next.js frontend + FastAPI backend) to Vercel.

## Overview

Your project has a multi-service architecture:
- **Frontend**: Next.js (React) - deploys to Vercel
- **Backend**: FastAPI (Python) - needs separate deployment

## Frontend Deployment (Next.js)

### Step 1: Prepare Your Project

Ensure all changes are committed to git:
```bash
cd /Users/shivangisingh/Desktop/ET-Hackathon
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign up or log in with your GitHub account
3. Click **"Add New..." → "Project"**
4. Select **"Import Git Repository"**
5. Paste your repository URL: `https://github.com/shivangiS04/ET-Hackathon`
6. Click **"Import"**

### Step 3: Configure Project Settings

In the Vercel import dialog, configure:

**Project Name:**
- `ET-Hackathon-Frontend` (or your preference)

**Root Directory:**
- Select **"frontend/"** from the dropdown

**Framework:**
- Auto-detected: **Next.js**

**Build Command:**
- Default is fine: `npm run build`

**Install Command:**
- Default is fine: `npm install`

**Output Directory:**
- Default is fine: `.next`

### Step 4: Environment Variables

Add the following environment variables in Vercel:

1. Click **"Environment Variables"** section
2. Add these variables:

| Key | Value | Notes |
|-----|-------|-------|
| `NEXT_PUBLIC_API_URL` | `https://your-backend-url.vercel.app` | Update after backend deployment |
| `NODE_ENV` | `production` | Automatically set by Vercel |

**For now, use**: `http://localhost:8000` (for local testing) or a placeholder

### Step 5: Deploy Frontend

1. Click **"Deploy"** button
2. Wait for the build to complete (usually 2-5 minutes)
3. You'll get a live URL like: `https://et-hackathon-frontend.vercel.app`

---

## Backend Deployment (FastAPI)

FastAPI cannot be deployed directly to Vercel's standard Next.js deployment. You have several options:

### Option A: Deploy Backend Separately to Vercel (Recommended)

**Requirements:**
- A `vercel.json` configuration at the backend root
- A `requirements.txt` with all Python dependencies

**Steps:**

1. Create `/backend/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb",
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

2. Install the Vercel CLI:
```bash
npm i -g vercel
```

3. Deploy backend from the backend directory:
```bash
cd backend
vercel --prod
```

4. Get your backend URL (e.g., `https://et-hackathon-backend.vercel.app`)

5. Update your frontend `NEXT_PUBLIC_API_URL` environment variable in Vercel dashboard

### Option B: Deploy Backend to Railway, Render, or Fly.io (Alternative)

**Railway.app (Easiest)**

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select the `backend` directory
4. Set environment variables
5. Deploy

Get your Railway URL and update frontend environment variables.

**Render.com**

1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect GitHub repository
4. Set `Root Directory` to `backend`
5. Set `Build Command` to `pip install -r requirements.txt`
6. Set `Start Command` to `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Fly.io**

1. Install Fly CLI: `brew install flyctl` (on Mac)
2. In backend directory: `flyctl launch`
3. Follow prompts to configure
4. Deploy: `flyctl deploy`

### Option C: Use Docker Container (Railway or similar)

Your project already has Docker Compose configured! Use it with:

**Railway:**
1. Push Docker image to Railway
2. Railway auto-detects `docker-compose.yml`

**Render:**
1. Select "Docker" as environment
2. Point to `Dockerfile` in backend

---

## Environment Variables Configuration

### Frontend Environment Variables (Set in Vercel Dashboard)

```
NEXT_PUBLIC_API_URL=https://your-backend-domain.vercel.app
NODE_ENV=production
```

### Backend Environment Variables (Set in Deployment Platform)

Update these in your backend deployment (Railway/Render/Fly.io):

```
# Database
MONGODB_URL=<Your MongoDB Atlas URL>
REDIS_URL=<Your Redis URL>
NEO4J_URL=<Your Neo4j instance>

# API
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# Features
ENABLE_CACHING=true
CACHE_TTL_SECONDS=300
```

---

## Using the vercel.json File

The `vercel.json` in your root directory handles rewrites from frontend to backend. Update it with your actual backend URL once deployed:

```json
{
  "rewrites": [
    {
      "source": "/api/backend/:path*",
      "destination": "https://your-actual-backend-url.vercel.app/:path*"
    }
  ]
}
```

---

## Deployment Checklist

### Before Deploying

- [ ] All code committed to git
- [ ] No `.env` files in repository (only `.env.example`)
- [ ] `package.json` has correct build/start scripts
- [ ] `requirements.txt` is up to date
- [ ] All dependencies are specified
- [ ] Environment variables are documented

### Frontend Deployment

- [ ] Connected to GitHub repository
- [ ] Root directory set to `frontend/`
- [ ] Build command: `npm run build`
- [ ] Environment variables configured
- [ ] Successfully deployed and accessible

### Backend Deployment

- [ ] Deployment platform selected (Vercel/Railway/Render/Fly)
- [ ] Python runtime version specified (3.11+)
- [ ] All environment variables set
- [ ] Database connections working
- [ ] Backend URL obtained

### Post-Deployment

- [ ] Update `NEXT_PUBLIC_API_URL` in frontend with backend URL
- [ ] Update `vercel.json` rewrites with real backend URL
- [ ] Redeploy frontend after URL changes
- [ ] Test API calls from frontend
- [ ] Verify all endpoints work
- [ ] Check Vercel analytics dashboard
- [ ] Set up monitoring/alerting

---

## Testing Your Deployment

### Test Frontend
```bash
# Visit your Vercel deployment URL
https://et-hackathon-frontend.vercel.app
```

### Test Backend API
```bash
# Replace with your backend URL
curl https://your-backend-url.vercel.app/health

# Test with API documentation
https://your-backend-url.vercel.app/docs
```

### Test API Connection from Frontend
1. Open browser DevTools (F12)
2. Go to Network tab
3. Click around the frontend
4. Check that API requests go to correct backend URL

---

## Common Issues & Solutions

### Issue: Frontend builds but backend API calls fail

**Solution:** 
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Ensure backend is deployed and accessible
- Check CORS is enabled in FastAPI backend
- Verify API route paths match

### Issue: "Cannot find module" errors during build

**Solution:**
- Ensure all dependencies in `package.json` exist
- Run `npm install` locally and commit lock file
- Check Node.js version (need 16+)

### Issue: Backend deployment fails

**Solution:**
- Verify all Python dependencies in `requirements.txt`
- Check Python version (need 3.9+)
- Ensure database credentials are correct
- Check for hardcoded localhost URLs

### Issue: Timeout errors from Vercel

**Solution:**
- Optimize API responses (paginate large datasets)
- Implement caching (already configured with Redis)
- Use serverless function timeout options
- Consider moving to dedicated backend host

---

## Production Optimization Tips

1. **Enable Image Optimization**: Vercel automatically optimizes images in Next.js
2. **Use Vercel Analytics**: Get performance insights in dashboard
3. **Set up CI/CD**: Automatic deployments on git push
4. **Enable Preview Deployments**: Test branches before merging
5. **Configure Custom Domain**: Set up your domain in Vercel DNS settings
6. **Enable DDoS Protection**: Vercel provides this by default
7. **Set up Error Tracking**: Use Sentry or Vercel's built-in error reporting

---

## Rollback & Updates

### To rollback to previous version:
1. Go to Vercel Dashboard
2. Select your project
3. Click "Deployments"
4. Find the previous working deployment
5. Click the three dots → "Promote to Production"

### To update after making changes:
1. Commit changes to git
2. Push to main branch
3. Vercel automatically redeploys (if auto-deployment is enabled)
4. View deployment status in Vercel Dashboard

---

## Next Steps

1. Deploy frontend first (easier setup)
2. Choose and deploy backend platform
3. Get both URLs
4. Update environment variables
5. Test integration
6. Set up monitoring
7. Configure custom domain (optional)

Good luck with your deployment! 🚀
