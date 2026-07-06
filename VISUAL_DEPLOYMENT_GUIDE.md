# Visual Deployment Guide - Step by Step

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   ET-HACKATHON PROJECT                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────┐      ┌────────────────────┐  │
│  │  FRONTEND (Next.js) │      │ BACKEND (FastAPI)  │  │
│  │  React Components   │◄────►│ Python Services    │  │
│  │  @localhost:3000    │      │ @localhost:8000    │  │
│  └─────────────────────┘      └────────────────────┘  │
│         (Local Dev)                  (Local Dev)        │
│                                                         │
└─────────────────────────────────────────────────────────┘
                          │
                          │ (git push)
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   VERCEL DEPLOYMENT                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────┐      ┌────────────────────┐  │
│  │  FRONTEND (Vercel)  │      │ BACKEND (Vercel)   │  │
│  │ Next.js Serverless  │◄────►│ Python Serverless  │  │
│  │ CDN + Global Edge   │      │ Lambda Functions   │  │
│  │ https://...         │      │ https://...        │  │
│  └─────────────────────┘      └────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Phase 1: Preparation (5 minutes)

### Step 1.1: Verify Git Setup

```bash
cd /Users/shivangisingh/Desktop/ET-Hackathon
git log --oneline -5
# Should show your recent commits
```

**Expected Output:**
```
abc1234 Add Vercel deployment configuration
def5678 Previous commit
...
```

### Step 1.2: Check Project Files

**Frontend files needed:**
```
✅ frontend/package.json        (exists)
✅ frontend/next.config.js      (exists)
✅ frontend/app/page.tsx        (exists)
✅ frontend/tsconfig.json       (exists)
```

**Backend files needed:**
```
✅ backend/main.py              (exists)
✅ backend/requirements.txt      (exists)
✅ backend/vercel.json          (created ✓)
```

**Root files:**
```
✅ vercel.json                  (created ✓)
✅ .env.example                 (exists)
```

### Step 1.3: Commit and Push

```bash
git add vercel.json backend/vercel.json VERCEL_DEPLOYMENT.md DEPLOYMENT_QUICK_START.md ENVIRONMENT_SETUP.md VISUAL_DEPLOYMENT_GUIDE.md
git commit -m "Add comprehensive Vercel deployment configuration and guides"
git push origin main
```

**Wait for:** Green checkmark on GitHub (CI/CD if configured)

---

## 🚀 Phase 2: Deploy Frontend (10 minutes)

### Step 2.1: Open Vercel Import Page

1. Go to **https://vercel.com/new**
2. Click **"Import Git Repository"**

![Vercel New Project]

### Step 2.2: Connect GitHub Repository

1. Paste your repo URL:
   ```
   https://github.com/shivangiS04/ET-Hackathon
   ```
2. Click **"Continue"**
3. Select your account/team
4. Click **"Import"**

![Import Repository]

### Step 2.3: Configure Project

**You'll see the import dialog:**

```
┌─────────────────────────────────────────────────────┐
│ Configure Project                                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Project Name:                                       │
│ [ET-Hackathon-Frontend ]                            │
│                                                     │
│ Root Directory:                                     │
│ [frontend ]  ← SELECT THIS                          │
│                                                     │
│ Framework:                                          │
│ [Next.js ]  ← Auto-detected ✓                       │
│                                                     │
│ Build Command:                                      │
│ [npm run build]  ← Keep default ✓                   │
│                                                     │
│ Install Command:                                    │
│ [npm install]  ← Keep default ✓                     │
│                                                     │
│ Output Directory:                                   │
│ [.next]  ← Keep default ✓                           │
│                                                     │
│ Environment Variables:                              │
│ ┌───────────────────────────────────────────────┐  │
│ │ NEXT_PUBLIC_API_URL │ http://localhost:8000   │  │
│ └───────────────────────────────────────────────┘  │
│                    (Update after backend deploy)    │
│                                                     │
│              [Deploy] Button                        │
└─────────────────────────────────────────────────────┘
```

### Step 2.4: Set Environment Variables

**Add this variable:**

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` *(for now, we'll update this)* |

### Step 2.5: Click Deploy

1. Click the **"Deploy"** button
2. Watch the build progress:
   ```
   ⏳ Building...
   📦 Installing dependencies...
   🔨 Building application...
   ✅ Build complete!
   🌐 Deploying to CDN...
   ✅ Deployment successful!
   ```

3. **Wait 3-5 minutes** for completion

### Step 2.6: Get Your Frontend URL

Once deployment completes, you'll see:

```
┌─────────────────────────────────────────────────────┐
│ Congratulations!                                    │
│ Your project has been deployed                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Production URL:                                     │
│ https://et-hackathon-frontend-xyz.vercel.app       │
│                                                     │
│ [Visit Website] [Go to Dashboard]                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Copy this URL!** You'll need it later.

---

## 🔧 Phase 3: Deploy Backend (10 minutes)

### Step 3.1: Install Vercel CLI

```bash
npm install -g vercel
```

Verify installation:
```bash
vercel --version
# Should output: Vercel CLI xx.x.x
```

### Step 3.2: Login to Vercel CLI

```bash
vercel login
```

**Follow prompts:**
1. Choose login method (GitHub recommended)
2. Authorize in browser
3. Return to terminal (should show ✅ Logged in)

### Step 3.3: Deploy Backend

```bash
cd backend
vercel --prod
```

**You'll be prompted:**

```
? Set up and deploy "backend"? [Y/n] y
? Which scope should contain your project? your-account
? Link to existing project? [y/N] n
? What's your project's name? et-hackathon-backend
? In which directory is your code located? . (current)
? Want to modify these settings? [y/N] n
```

**Watch the deployment:**
```
> Creating project
> Linking to GitHub
> Building...
> Installing dependencies...
> Deploying...
✅ Production: https://et-hackathon-backend-xyz.vercel.app
```

### Step 3.4: Get Your Backend URL

**Copy the URL!**
```
https://et-hackathon-backend-xyz.vercel.app
```

Test it works:
```bash
curl https://et-hackathon-backend-xyz.vercel.app/health
# Should return: {"status": "healthy"}
```

---

## 🔗 Phase 4: Connect Frontend to Backend (5 minutes)

### Step 4.1: Update Frontend Environment Variable

1. Go to **https://vercel.com/dashboard**
2. Select your **Frontend project** (ET-Hackathon-Frontend)
3. Click **Settings**
4. Click **Environment Variables**

![Dashboard Navigation]

### Step 4.2: Update the API URL

Find `NEXT_PUBLIC_API_URL` and update it:

```
OLD: http://localhost:8000
NEW: https://et-hackathon-backend-xyz.vercel.app
```

1. Click the variable to edit
2. Change the value
3. Click **Save**

**Important:** This will trigger a redeployment

### Step 4.3: Verify Frontend Redeploy

1. Go back to **Deployments** tab
2. Watch for new deployment to complete
3. See ✅ "READY" status

---

## ✅ Phase 5: Testing (5 minutes)

### Test 1: Frontend is Accessible

```bash
curl https://et-hackathon-frontend-xyz.vercel.app
```

**Expected:** HTML response (not an error)

### Test 2: Backend API is Running

```bash
curl https://et-hackathon-backend-xyz.vercel.app/health
```

**Expected:**
```json
{"status": "healthy"}
```

### Test 3: API Documentation

Open in browser:
```
https://et-hackathon-backend-xyz.vercel.app/docs
```

**Expected:** Swagger UI with all endpoints listed

### Test 4: Frontend Can Call Backend

1. Open frontend in browser
2. Open DevTools (F12)
3. Go to Network tab
4. Interact with the app
5. Check that API calls go to correct backend URL

**Expected:** Requests to `https://et-hackathon-backend-xyz.vercel.app/api/...`

---

## 📊 Phase 6: Verification Checklist

```
✅ Frontend deployed to Vercel
   URL: https://et-hackathon-frontend-xyz.vercel.app

✅ Backend deployed to Vercel  
   URL: https://et-hackathon-backend-xyz.vercel.app

✅ Frontend can reach backend
   Check: Open frontend, test an API call in DevTools

✅ Health check passes
   curl https://your-backend/health
   Returns: {"status": "healthy"}

✅ API documentation available
   https://your-backend/docs
   Shows all endpoints

✅ No console errors
   Open browser DevTools, no red errors

✅ Automatic CI/CD enabled
   Push to main → Vercel auto-redeploys
```

---

## 📈 Post-Deployment Monitoring

### Monitor Deployments

```bash
# View recent deployments
vercel list

# View specific project
vercel projects --scope your-team

# View production deployments
vercel deployments --prod
```

### View Logs

```bash
# Frontend logs
vercel logs et-hackathon-frontend

# Backend logs
vercel logs et-hackathon-backend
```

### Check Performance

Visit Vercel Dashboard:
- Analytics tab → see traffic, response times
- Functions tab → see serverless function metrics
- Deployments tab → see build times

---

## 🆘 Troubleshooting Guide

### Problem: Frontend Build Fails

**Diagnosis:**
```bash
cd frontend
npm run build  # Try locally
```

**Common causes & fixes:**

| Error | Fix |
|-------|-----|
| `Cannot find module 'react'` | Run `npm install` in frontend |
| `TypeScript error` | Check `tsconfig.json`, fix type errors |
| `Port already in use` | Not an issue for Vercel deployments |
| `env variable undefined` | Add to Vercel Environment Variables |

### Problem: Backend Deployment Fails

**Diagnosis:**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Common causes & fixes:**

| Error | Fix |
|-------|-----|
| `Module not found` | Add to `requirements.txt` |
| `Python version mismatch` | Use Python 3.11+ |
| `Connection refused` | Check database credentials in env vars |
| `No module named 'main'` | Verify `backend/main.py` exists |

### Problem: API Calls Return 404/500

**Diagnosis:**
1. Check backend health: `curl https://your-backend/health`
2. Check frontend console (F12) for actual URL
3. Compare with expected URL

**Common causes & fixes:**

| Error | Fix |
|-------|-----|
| 404 Not Found | Wrong API endpoint path |
| 500 Server Error | Backend error, check logs |
| CORS error | Enable CORS in FastAPI |
| Timeout | Backend processing too slow |

### Problem: Environment Variables Not Working

**Diagnosis:**
```bash
# View current env vars
vercel env ls
```

**Common causes & fixes:**

| Issue | Fix |
|-------|-----|
| Variable not appearing | Redeploy after adding |
| Frontend can't access | Add `NEXT_PUBLIC_` prefix |
| Backend can't access | Set in backend project settings |
| Wrong value | Verify in Vercel dashboard |

---

## 🎉 Success Indicators

You'll know everything is working when:

✅ **Frontend loads without errors**
- No blank page
- No console errors (F12)
- Can see the app UI

✅ **Backend API responds**
- `/health` returns 200
- `/docs` shows Swagger UI
- Endpoints return data (not 500 errors)

✅ **Frontend communicates with backend**
- API calls visible in DevTools Network tab
- Data loads in UI (battery dashboard, fleet table, etc.)
- No CORS errors

✅ **Automatic updates work**
- Make a git commit
- Push to main
- Vercel auto-redeploys within 1-2 minutes
- See "READY" status in dashboard

---

## 📚 Next Steps

1. ✅ Both services deployed
2. ✅ Successfully tested
3. Next: 
   - Set up custom domain
   - Enable monitoring/alerts
   - Configure backup strategy
   - Plan scaling if needed

---

## 🚨 Emergency Rollback

If something goes wrong:

### Rollback Frontend
1. Vercel Dashboard → Frontend project
2. Deployments tab
3. Find previous working deployment
4. Click "..." → "Promote to Production"

### Rollback Backend
```bash
cd backend
vercel rollback
# Select previous deployment
```

---

## 📞 Support Resources

- **Vercel Docs:** https://vercel.com/docs
- **Next.js Docs:** https://nextjs.org/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Your Deployment Guides:**
  - `VERCEL_DEPLOYMENT.md` (detailed guide)
  - `DEPLOYMENT_QUICK_START.md` (quick reference)
  - `ENVIRONMENT_SETUP.md` (env vars guide)

---

## 🎊 Celebration Moment!

**Your ET-Hackathon project is now live on Vercel!**

🌐 **Frontend:** https://et-hackathon-frontend-xyz.vercel.app
🔌 **Backend:** https://et-hackathon-backend-xyz.vercel.app
📊 **Docs:** https://et-hackathon-backend-xyz.vercel.app/docs

Share these URLs with your team and celebrate the deployment! 🚀
