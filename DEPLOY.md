# Quick Deployment Guide

## Deploy to GitHub (Recommended - 100% Free)

### 1. Test Locally First
```bash
cd loksujag-rss-scraper
./setup.sh
source venv/bin/activate
python scraper.py
```

### 2. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Loksujag RSS scraper"
```

### 3. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `loksujag-rss-feed` (or any name you prefer)
3. Set to **Public** (required for free GitHub Pages)
4. Click "Create repository"

### 4. Push to GitHub
```bash
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
git branch -M main
git push -u origin main
```

### 5. Enable GitHub Actions
1. Go to your repository on GitHub
2. Click "Settings" → "Actions" → "General"
3. Under "Workflow permissions", select:
   - ✅ "Read and write permissions"
   - ✅ "Allow GitHub Actions to create and approve pull requests"
4. Click "Save"

### 6. Enable GitHub Pages
1. Go to "Settings" → "Pages"
2. Under "Source", select:
   - Branch: `main`
   - Folder: `/ (root)`
3. Click "Save"
4. Wait 1-2 minutes for deployment

### 7. Access Your RSS Feed
Your feed will be available at:
```
https://<YOUR-USERNAME>.github.io/<YOUR-REPO-NAME>/loksujag_feed.xml
```

Example:
```
https://aadil.github.io/loksujag-rss-feed/loksujag_feed.xml
```

### 8. Manual First Run (Optional)
To trigger the scraper immediately:
1. Go to "Actions" tab in your repository
2. Click "Scrape Loksujag and Update RSS Feed"
3. Click "Run workflow" → "Run workflow"

---

## Alternative: Deploy to Render.com

### Setup (5 minutes)
1. Sign up at https://render.com (free tier)
2. Click "New +" → "Cron Job"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `loksujag-scraper`
   - **Schedule**: `0 */6 * * *` (every 6 hours)
   - **Command**: `python scraper.py`
   - **Environment**: Python 3
5. Click "Create Cron Job"

### Add Persistent Storage
1. In your cron job dashboard, click "Disks"
2. Add disk:
   - **Name**: `cache-storage`
   - **Mount Path**: `/data`
   - **Size**: 1GB (free tier)
3. Update `scraper.py` line 20:
   ```python
   def __init__(self, cache_file: str = "/data/articles_cache.json"):
   ```

### Serve RSS Feed
1. Create a new "Static Site" in Render
2. Connect same repository
3. Set publish directory to `/`
4. Your feed will be at: `https://<your-site>.onrender.com/loksujag_feed.xml`

---

## Alternative: Deploy to Railway.app

### Setup (5 minutes)
1. Sign up at https://railway.app (free tier)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository

### Add Cron Job
Create `railway.toml` in your repository:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python scraper.py"
cronSchedule = "0 */6 * * *"
```

Push changes:
```bash
git add railway.toml
git commit -m "Add Railway configuration"
git push
```

---

## Troubleshooting

### GitHub Actions Not Running
- Check workflow permissions in Settings → Actions → General
- Ensure `.github/workflows/scrape.yml` exists
- Look at Actions tab for error logs

### RSS Feed Not Updating
- Verify the scraper ran successfully in Actions tab
- Check that `loksujag_feed.xml` exists in repository
- Clear browser cache or try incognito mode

### Python Dependencies Error
Make sure `requirements.txt` has all dependencies:
```txt
requests==2.31.0
beautifulsoup4==4.12.3
feedgen==1.0.0
lxml==5.1.0
```

### Scraper Not Finding Articles
Website structure may have changed. Check:
1. Visit https://loksujag.com manually
2. Inspect HTML structure
3. Update CSS selectors in `scraper.py`

---

## Monitoring

### Check Last Update
Visit your RSS feed URL - the `<lastBuildDate>` tag shows last update time.

### Subscribe to Feed
Test your feed in:
- Feedly: https://feedly.com/
- NewsBlur: https://newsblur.com/
- Any RSS reader app

### View Logs
- GitHub: Actions tab → Select workflow run → View logs
- Render: Dashboard → Logs
- Railway: Dashboard → Logs

---

## Customization

### Change Update Frequency
Edit `.github/workflows/scrape.yml`, line 6:
```yaml
- cron: '0 */6 * * *'  # Every 6 hours
```

Common schedules:
- `0 */3 * * *` - Every 3 hours
- `0 */12 * * *` - Twice daily
- `0 0 * * *` - Once daily at midnight

### Adjust Feed Size
Edit `scraper.py`, line 142:
```python
for article in reversed(self.cache['articles'][-50:]):
```
Change `50` to your preferred number of articles.

---

## Support

If you encounter issues:
1. Check GitHub Issues for similar problems
2. Review GitHub Actions logs for error messages
3. Verify the website structure hasn't changed
4. Test locally first with `python scraper.py`
