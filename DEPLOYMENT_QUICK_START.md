# Quick Start: Deploy to Vercel in 5 Minutes

## 🚀 Fast Track Deployment

### Step 1: Verify Git is Ready (1 min)
```bash
cd /Users/shivangisingh/Desktop/ET-Hackathon
git status
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### Step 2: Deploy Frontend to Vercel (2 min)

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. Paste: `https://github.com/shivangiS04/ET-Hackathon`
4. In **"Configure Project"** dialog:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Install Command**: `npm install`
   
5. In **"Environment Variables"** section, add:
   ```
   NEXT_PUBLIC_API_URL = https://et-hackathon-backend.vercel.app
   ```
   (Use placeholder for now, we'll update this later)

6. Click **"Deploy"** and wait 3-5 minutes

✅ **Your frontend is now live!** Copy the URL (e.g., `https://et-hackathon-frontend.vercel.app`)

---

### Step 3: Deploy Backend to Vercel (2 min)

1. Install Vercel CLI globally:
```bash
npm install -g vercel
```

2. Deploy from backend directory:
```bash
cd backend
vercel --prod
```

3. When prompted:
   - Set project name: `ET-Hackathon-Backend`
   - Link to existing project: `No`
   - Source directory: `.` (current)

4. Wait for deployment to complete (you'll get a URL like `https://et-hackathon-backend.vercel.app`)

5. Set environment variables in Vercel:
   ```
   MONGODB_URL = <your MongoDB Atlas connection string>
   REDIS_URL = <your Redis connection string or skip for now>
   ```

✅ **Your backend is now live!**

---

### Step 4: Update Frontend with Backend URL (1 min)

1. Go to Vercel Dashboard: https://vercel.com/dashboard
2. Select your frontend project
3. Click **"Settings"** → **"Environment Variables"**
4. Update `NEXT_PUBLIC_API_URL` with your actual backend URL:
   ```
   NEXT_PUBLIC_API_URL = https://et-hackathon-backend.vercel.app
   ```
5. Click **"Save"**
6. Vercel will automatically redeploy your frontend

---

### Step 5: Test Your Deployment (1 min)

Test Frontend:
```bash
curl https://et-hackathon-frontend.vercel.app
```

Test Backend:
```bash
curl https://et-hackathon-backend.vercel.app/health
```

Test API Docs:
```
https://et-hackathon-backend.vercel.app/docs
```

---

## ⚡ What Just Happened

✅ Frontend deployed to Vercel (auto-scales, CDN included)
✅ Backend deployed to Vercel (serverless functions)
✅ Both services connected via `NEXT_PUBLIC_API_URL`
✅ CI/CD enabled (updates on every git push)

---

## 🛠️ If Something Goes Wrong

### Frontend build fails
- Check `frontend/package.json` has correct dependencies
- Ensure `next.config.js` is valid
- Look at Vercel build logs (Dashboard → Deployments)

### Backend deployment fails
- Verify `backend/requirements.txt` has all dependencies
- Check `backend/main.py` is the entry point
- Ensure `backend/vercel.json` is valid
- Check Vercel CLI logs for errors

### API calls not working
- Verify `NEXT_PUBLIC_API_URL` matches your backend URL
- Check frontend DevTools Network tab for API URLs
- Ensure backend CORS is enabled (should be by default in FastAPI)

---

## 📊 Monitor Your Deployment

**Vercel Dashboard**: https://vercel.com/dashboard
- View deployments
- Check build logs
- Monitor analytics
- Manage domains

**Backend API Docs**: `https://your-backend-url/docs`
- Test API endpoints
- View request/response schemas

---

## 🔒 Production Checklist

After deployment:
- [ ] Both frontend and backend are accessible
- [ ] API calls from frontend work
- [ ] No console errors in browser DevTools
- [ ] Set up custom domain (optional)
- [ ] Enable automatic deployments
- [ ] Configure monitoring/alerting
- [ ] Update `.env` with production values

---

## 📚 Full Documentation

See `VERCEL_DEPLOYMENT.md` for detailed instructions, troubleshooting, and advanced configuration.

---

## 🎯 You're Done! 🎉

Your ET-Hackathon project is now live and deployed to Vercel!

Frontend: `https://et-hackathon-frontend.vercel.app`
Backend: `https://et-hackathon-backend.vercel.app`

Next steps:
1. Share your URLs with the team
2. Configure custom domain (if desired)
3. Set up monitoring
4. Continue development with automatic redeployment on git push

Questions? Check the full deployment guide or Vercel documentation.
