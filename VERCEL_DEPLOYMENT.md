# Vercel Deployment Guide

## 🚀 Deploy to Vercel

This project is configured for automatic deployment to Vercel.

### Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Vikas8346/-Ai-based-maze-solver)

### Manual Deployment Steps

1. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with your GitHub account
   - Click "Add New Project"
   - Import `Vikas8346/-Ai-based-maze-solver`

2. **Configure Project:**
   - Framework Preset: **Other**
   - Root Directory: `./` (default)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

3. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be live at `https://ai-based-maze-solver.vercel.app/`

### Automatic Deployments

Every push to the `main` branch will automatically trigger a new deployment on Vercel.

### Local Testing

Before deploying, test locally:
```bash
cd web
python3 -m http.server 8000
# Open http://localhost:8000
```

### Configuration Files

- `vercel.json` - Vercel deployment configuration
- `index.html` - Main application entry point (root level)
- All JS/CSS files are in root for Vercel access

### Troubleshooting

**404 NOT_FOUND Error:**
- Ensure `index.html` exists in root directory
- Check `vercel.json` configuration
- Verify repository is connected in Vercel dashboard

**CSP Errors:**
- Check Content-Security-Policy meta tag in `index.html`
- Custom charts.js avoids eval() issues

**Build Fails:**
- No build step needed (static site)
- Verify all files are committed and pushed

### Live Demo

🌐 **Production URL:** https://ai-based-maze-solver.vercel.app/

### Features on Vercel

✅ Automatic HTTPS
✅ Global CDN
✅ Instant cache invalidation
✅ Analytics available
✅ Custom domain support
✅ Automatic Git integration

---

For more information, see [Vercel Documentation](https://vercel.com/docs)
