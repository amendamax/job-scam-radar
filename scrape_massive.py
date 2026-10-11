import os
import uuid
import requests
import json
import sqlite3
import time
import feedparser
from datetime import datetime
import re
from dotenv import load_dotenv

load_dotenv()
DB_PATH = 'database.db'

PROXY_HOST = os.getenv('ANYIP_HOST', 'portal.anyip.io')
PROXY_PORT = os.getenv('ANYIP_PORT', '1080')
PROXY_USER = os.getenv('ANYIP_USER', '')
PROXY_PASS = os.getenv('ANYIP_PASS', '')

PROXIES = None
if PROXY_USER and PROXY_PASS:
    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
    PROXIES = {'http': proxy_url, 'https': proxy_url}

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def scrape_google_news_historical():
    print("Scraping Google News HISTORICAL (3 years)...")
    queries = [
        "job scam", "recruitment fraud", "whatsapp task scam", 
        "telegram job scam", "remote job scam", "part time online job scam",
        "freelance scam", "upwork scam", "data entry job scam",
        "employment fraud", "work from home scam", "fake recruiter linkedin",
        "reshipping scam job", "mystery shopper scam"
    ]
    
    # anii din care sa tragem
    timeframes = [
        "after:2021-01-01+before:2021-12-31",
        "after:2022-01-01+before:2022-12-31",
        "after:2023-01-01+before:2023-12-31",
        "after:2024-01-01+before:2025-01-01"
    ]
    
    reports = []
    seen_links = set()
    
    for q in queries:
        for tf in timeframes:
            url = f"https://news.google.com/rss/search?q={q.replace(' ', '+')}+{tf}"
            try:
                if PROXIES:
                    response = requests.get(url, proxies=PROXIES, timeout=15)
                    feed = feedparser.parse(response.content)
                else:
                    feed = feedparser.parse(url)
                    
                for entry in feed.entries[:20]: # Top 20 per an per query
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
                    reason = f"Historical Scam Report: {title}. This incident was reported in {formatted_date[:4]}."
                    
                    reports.append({
                        'slug': slug,
                        'entity_name': entity_name,
                        'domain': 'news.google.com',
                        'regulator': 'Google News Historical',
                        'warning_type': 'Historical Scam Alert',
                        'warning_date': formatted_date,
                        'official_url': link,
                        'reason': reason,
                        'jurisdiction': 'Global',
                        'risk_score': 8,
                        'blacklisted_urls': '',
                        'clone_of': '',
                        'details_json': json.dumps({"source": "Google News Historical", "year": formatted_date[:4]})
                    })
            except Exception as e:
                print(f"Failed to scrape Google News for '{q} {tf}': {e}")
            time.sleep(1) # un mic delay pentru stabilitate
            
    return reports

def save_to_db(reports):
    if not reports:
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for r in reports:
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
    print(f"Inserted {count} new historical scam reports into DB!")

if __name__ == "__main__":
    reports = scrape_google_news_historical()
    print(f"Collected {len(reports)} historical reports. Saving...")
    save_to_db(reports)
