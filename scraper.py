#!/usr/bin/env python3
"""
Loksujag.com RSS Feed Generator
Scrapes articles from loksujag.com and generates an RSS feed
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import hashlib

import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator


class LoksujagScraper:
    def __init__(self, cache_file: str = "articles_cache.json"):
        self.base_url = "https://loksujag.com"
        self.cache_file = Path(cache_file)
        self.cache = self._load_cache()
        
    def _load_cache(self) -> Dict:
        """Load previously scraped articles from cache"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"articles": [], "last_updated": None}
    
    def _save_cache(self):
        """Save scraped articles to cache"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def scrape_homepage(self) -> List[Dict]:
        """Scrape articles from the homepage"""
        try:
            response = requests.get(self.base_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            
            # Find article containers
            article_containers = soup.find_all('div', class_=lambda x: x and 'Card' in x if x else False)
            
            for container in article_containers:
                # Find article link
                link_el = container.find('a', href=lambda x: x and ('/story/' in x or '/special-edition/' in x))
                title_el = container.find(['h4', 'h5'])
                author_el = container.find('a', href=lambda x: x and '/author/' in x)
                img_el = container.find('img', alt='thumb')
                
                if link_el and title_el:
                    href = link_el.get('href', '')
                    url = href if href.startswith('http') else f"{self.base_url}{href}"
                    slug = href.split('/')[-1]
                    
                    article = {
                        'url': url,
                        'title': title_el.get_text(strip=True),
                        'author': author_el.get_text(strip=True) if author_el else '',
                        'thumbnail': img_el.get('src', '') if img_el else '',
                        'slug': slug,
                        'guid': hashlib.md5(url.encode()).hexdigest(),
                        'scraped_at': datetime.utcnow().isoformat()
                    }
                    articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Error scraping homepage: {e}")
            return []
    
    def scrape_article_content(self, url: str) -> str:
        """Scrape the content/description of a single article"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find article description or first paragraph
            description = ""
            
            # Look for meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '')
            
            # Fallback to first paragraph in article
            if not description:
                article_body = soup.find('article') or soup.find('div', class_=lambda x: x and 'content' in x.lower() if x else False)
                if article_body:
                    first_p = article_body.find('p')
                    if first_p:
                        description = first_p.get_text(strip=True)
            
            return description[:500]  # Limit description length
            
        except Exception as e:
            print(f"Error scraping article content from {url}: {e}")
            return ""
    
    def get_new_articles(self) -> List[Dict]:
        """Get only new articles that aren't in cache"""
        current_articles = self.scrape_homepage()
        
        cached_urls = {article['url'] for article in self.cache['articles']}
        new_articles = [a for a in current_articles if a['url'] not in cached_urls]
        
        # Enrich new articles with content
        for article in new_articles:
            print(f"Scraping content for: {article['title'][:50]}...")
            article['description'] = self.scrape_article_content(article['url'])
            time.sleep(1)  # Be respectful with rate limiting
        
        return new_articles
    
    def update_cache(self, new_articles: List[Dict]):
        """Update cache with new articles"""
        self.cache['articles'].extend(new_articles)
        # Keep only last 100 articles
        self.cache['articles'] = self.cache['articles'][-100:]
        self.cache['last_updated'] = datetime.utcnow().isoformat()
        self._save_cache()
    
    def generate_rss_feed(self, output_file: str = "loksujag_feed.xml"):
        """Generate RSS feed from cached articles"""
        fg = FeedGenerator()
        fg.id(self.base_url)
        fg.title('Loksujag - لوک سجاگ')
        fg.author({'name': 'Loksujag', 'email': 'info@loksujag.com'})
        fg.link(href=self.base_url, rel='alternate')
        fg.logo(f'{self.base_url}/assets/logo.png')
        fg.subtitle('Voices from the margins of power')
        fg.language('ur')
        
        # Add articles to feed (most recent first)
        for article in reversed(self.cache['articles'][-50:]):  # Last 50 articles
            fe = fg.add_entry()
            fe.id(article['guid'])
            fe.title(article['title'])
            fe.link(href=article['url'])
            
            if article.get('description'):
                fe.description(article['description'])
            
            if article.get('author'):
                fe.author({'name': article['author']})
            
            if article.get('thumbnail'):
                fe.enclosure(article['thumbnail'], 0, 'image/jpeg')
            
            # Use scraped_at as publication date
            pub_date = datetime.fromisoformat(article['scraped_at'])
            fe.pubDate(pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000'))
        
        # Write RSS feed to file
        fg.rss_file(output_file, pretty=True)
        print(f"RSS feed generated: {output_file}")
        
        return output_file


def main():
    """Main function to run the scraper"""
    scraper = LoksujagScraper()
    
    print("Checking for new articles...")
    new_articles = scraper.get_new_articles()
    
    if new_articles:
        print(f"Found {len(new_articles)} new articles")
        scraper.update_cache(new_articles)
    else:
        print("No new articles found")
    
    print("Generating RSS feed...")
    scraper.generate_rss_feed()
    print("Done!")


if __name__ == "__main__":
    main()
