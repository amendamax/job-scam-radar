import uuid
import requests
import json
import sqlite3
import time
import feedparser
from datetime import datetime
import re

DB_PATH = 'database.db'

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def scrape_reddit():
    print("Scraping Reddit /r/Scams via RSS...")
    url = "https://www.reddit.com/r/Scams/new.rss"
    reports = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title
            
            # Filter for job/task scams since we are pulling the general new feed
            title_lower = title.lower()
            if not any(k in title_lower for k in ['job', 'task', 'hiring', 'recruitment', 'remote', 'whatsapp', 'telegram']):
                continue
            link = entry.link
            pub_date = entry.updated
            try:
                date_obj = datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%S%z")
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except:
                formatted_date = datetime.now().strftime('%Y-%m-%d')
                
            # RSS content includes HTML, we can strip it roughly or just leave a generic text
            content_summary = entry.get('summary', '')
            # Clean basic HTML tags
            content_summary = re.sub('<[^<]+>', '', content_summary).strip()
            
            if len(content_summary) < 50:
                continue
                
            entity_name = title[:60] + "..." if len(title) > 60 else title
            slug = slugify(title[:40]) + f"-{uuid.uuid4().hex[:8]}"
            reason = content_summary[:500] + "..." if len(content_summary) > 500 else content_summary
            
            reports.append({
                'slug': slug,
                'entity_name': entity_name,
                'domain': 'reddit.com/r/scams',
                'regulator': 'Reddit /r/Scams Community',
                'warning_type': 'Task Scam / Fake Job',
                'warning_date': formatted_date,
                'official_url': link,
                'reason': reason,
                'jurisdiction': 'Global (Online)',
                'risk_score': 10,
                'blacklisted_urls': '',
                'clone_of': '',
                'details_json': json.dumps({"source": "Reddit RSS", "author": entry.author})
            })
        return reports
    except Exception as e:
        print(f"Failed to scrape Reddit RSS: {e}")
        return []

def scrape_google_news():
    print("Scraping Google News RSS for multiple queries...")
    queries = [
        "job scam OR recruitment fraud",
        "whatsapp task scam OR telegram job scam",
        "remote job scam alert",
        "part time online job scam",
        "freelance scam OR upwork scam",
        "data entry job scam"
    ]
    
    reports = []
    seen_links = set()
    
    for q in queries:
        url = f"https://news.google.com/rss/search?q={q.replace(' ', '+')}+when:14d"
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]: # Top 10 per query
                title = entry.title
                link = entry.link
                if link in seen_links:
                    continue
                seen_links.add(link)
                
                pub_date = entry.published
                try:
                    date_obj = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                except:
                    formatted_date = datetime.now().strftime('%Y-%m-%d')
                    
                entity_name = title[:60] + "..." if len(title) > 60 else title
                slug = slugify(title[:40]) + f"-{uuid.uuid4().hex[:8]}"
                reason = f"Global News Report: {title}. Read the full article for details on this recruitment fraud or job scam tactic."
                
                reports.append({
                    'slug': slug,
                    'entity_name': entity_name,
                    'domain': 'news.google.com',
                    'regulator': 'Google News Aggregator',
                    'warning_type': 'Verified Scam News',
                    'warning_date': formatted_date,
                    'official_url': link,
                    'reason': reason,
                    'jurisdiction': 'Global',
                    'risk_score': 8,
                    'blacklisted_urls': '',
                    'clone_of': '',
                    'details_json': json.dumps({"source": "Google News", "publisher": entry.get('source', {}).get('title', 'News')})
                })
        except Exception as e:
            print(f"Failed to scrape Google News for '{q}': {e}")
            
    return reports

def save_to_db(reports):
    if not reports:
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for r in reports:
        # Check if already exists by slug or exact title
        cursor.execute("SELECT id FROM job_scam_reports WHERE official_url = ? OR entity_name = ?", (r['official_url'], r['entity_name']))
        if cursor.fetchone():
            continue
            
        cursor.execute("""
            INSERT INTO job_scam_reports 
            (slug, entity_name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction, risk_score, blacklisted_urls, clone_of, details_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r['slug'], r['entity_name'], r['domain'], r['regulator'], r['warning_type'], 
            r['warning_date'], r['official_url'], r['reason'], r['jurisdiction'], 
            r['risk_score'], r['blacklisted_urls'], r['clone_of'], r['details_json'], 
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"Inserted {count} new real scam reports into DB!")

if __name__ == "__main__":
    reddit_data = scrape_reddit()
    news_data = scrape_google_news()
    
    all_reports = reddit_data + news_data
    print(f"Collected {len(all_reports)} potential reports. Saving...")
    save_to_db(all_reports)
