# Loksujag RSS Feed Scraper

A Python-based scraper that periodically checks [loksujag.com](https://loksujag.com) for new articles and generates an RSS feed.

## Features

- ✅ Scrapes articles from loksujag.com homepage
- ✅ Extracts article metadata (title, author, thumbnail, description)
- ✅ Generates valid RSS 2.0 feed
- ✅ Caches articles to avoid duplicates
- ✅ Periodic automatic updates via GitHub Actions
- ✅ Free hosting on GitHub Pages

## Local Setup

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd loksujag-rss-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scraper:
```bash
python scraper.py
```

This will:
- Check for new articles on loksujag.com
- Update the cache file (`articles_cache.json`)
- Generate/update the RSS feed (`loksujag_feed.xml`)

## Cloud Hosting (Free)

### Option 1: GitHub Actions + GitHub Pages (Recommended)

This setup is completely free and runs automatically.

#### Setup Steps:

1. **Create a GitHub repository**:
   - Go to GitHub and create a new public repository
   - Push this code to the repository

2. **Enable GitHub Actions**:
   - Actions are enabled by default
   - The workflow file (`.github/workflows/scrape.yml`) will run automatically

3. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Under "Source", select "Deploy from a branch"
   - Select `main` branch and `/root` folder
   - Click Save

4. **Create index.html** (optional):
   Create an `index.html` file to make the feed accessible:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>Loksujag RSS Feed</title>
       <meta charset="utf-8">
   </head>
   <body>
       <h1>Loksujag RSS Feed</h1>
       <p>Subscribe to the RSS feed: <a href="loksujag_feed.xml">loksujag_feed.xml</a></p>
   </body>
   </html>
   ```

5. **Access your feed**:
   Your RSS feed will be available at:
   ```
   https://<your-username>.github.io/<repo-name>/loksujag_feed.xml
   ```

#### How it works:
- GitHub Actions runs the scraper every 6 hours (configurable in `.github/workflows/scrape.yml`)
- New articles are detected and added to the cache
- The RSS feed is automatically updated
- Changes are committed back to the repository
- GitHub Pages serves the RSS feed publicly

### Option 2: Render.com (Free Tier)

Render offers free tier with cron jobs.

#### Setup Steps:

1. **Create account** at [render.com](https://render.com)

2. **Create a new Cron Job**:
   - Click "New +" → "Cron Job"
   - Connect your GitHub repository
   - Configure:
     - Name: `loksujag-scraper`
     - Schedule: `0 */6 * * *` (every 6 hours)
     - Command: `python scraper.py`

3. **Add environment variables** (if needed)

4. **Enable persistent storage**:
   - Add a disk to store `articles_cache.json`
   - Mount path: `/data`
   - Update scraper to use `/data/articles_cache.json`

### Option 3: Railway.app (Free Tier)

Railway offers a free tier with cron jobs.

#### Setup Steps:

1. **Create account** at [railway.app](https://railway.app)

2. **Deploy from GitHub**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Add Cron Configuration**:
   Create a `railway.toml` file:
   ```toml
   [build]
   builder = "NIXPACKS"

   [deploy]
   startCommand = "python scraper.py"
   cronSchedule = "0 */6 * * *"
   ```

### Option 4: PythonAnywhere (Free Tier)

PythonAnywhere offers free tier with scheduled tasks.

#### Setup Steps:

1. **Create account** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload your code**:
   - Use Git to clone your repository
   - Or upload files directly

3. **Install dependencies**:
   ```bash
   pip3 install --user -r requirements.txt
   ```

4. **Setup scheduled task**:
   - Go to "Tasks" tab
   - Add a new scheduled task
   - Set to run every 6 hours: `python3 /home/<username>/loksujag-rss-scraper/scraper.py`

5. **Serve RSS feed**:
   - Copy `loksujag_feed.xml` to `/home/<username>/<username>.pythonanywhere.com/`
   - Access at: `https://<username>.pythonanywhere.com/loksujag_feed.xml`

## Configuration

### Change scraping frequency

Edit `.github/workflows/scrape.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Change this to your preferred schedule
```

Cron syntax:
- `0 */6 * * *` - Every 6 hours
- `0 */3 * * *` - Every 3 hours
- `0 0 * * *` - Daily at midnight
- `0 */1 * * *` - Every hour

### Customize cache size

Edit `scraper.py`, line 126:
```python
self.cache['articles'] = self.cache['articles'][-100:]  # Keep last 100 articles
```

### Customize feed size

Edit `scraper.py`, line 142:
```python
for article in reversed(self.cache['articles'][-50:]):  # Last 50 articles
```

## RSS Feed URL

Once deployed, subscribe to your feed in any RSS reader using:
- GitHub Pages: `https://<username>.github.io/<repo>/loksujag_feed.xml`
- Custom domain: Configure in GitHub Pages settings

## Troubleshooting

### Scraper not finding articles

The website structure might have changed. Update the CSS selectors in `scraper.py`:
- Line 47: Article container selector
- Line 51: Article link selector
- Line 52: Title selector
- Line 53: Author selector

### GitHub Actions failing

Check:
1. Actions are enabled in repository settings
2. Workflow has write permissions (Settings → Actions → General → Workflow permissions)

### RSS feed not updating

1. Check GitHub Actions logs for errors
2. Verify cache file is being committed
3. Check GitHub Pages is enabled and deploying

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Pull requests welcome! Please ensure the scraper remains respectful of the source website.
