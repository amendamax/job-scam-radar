import time
import sqlite3
import os
import re
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.execute("PRAGMA journal_mode = WAL;")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_scam_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE,
            entity_name TEXT,
            domain TEXT,
            regulator TEXT,
            warning_type TEXT,
            warning_date TEXT,
            official_url TEXT,
            reason TEXT,
            jurisdiction TEXT,
            risk_score INTEGER DEFAULT 4,
            blacklisted_urls TEXT,
            clone_of TEXT,
            extra_data TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_scam_report(entity_name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction="Global"):
    if not entity_name:
        return False
    slug = re.sub(r'[^\w\s-]', '', entity_name).strip().lower().replace(' ', '-')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    risk_score = 9
    
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO job_scam_reports 
            (slug, entity_name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction, risk_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (slug, entity_name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction, risk_score, timestamp))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        return False
    finally:
        conn.close()

def extract_domain_from_text(text):
    match = re.search(r'([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', text)
    return match.group(1).lower() if match else "unknown-domain.com"

def harvest_google_news_scams():
    print("[JobScamRadar] Harvesting real-time job scam alerts from global news feeds...")
    url = 'https://news.google.com/rss/search?q=%22job+scam%22+OR+%22employment+scam%22+OR+%22recruitment+scam%22+OR+%22task+scam%22+OR+%22work+from+home+scam%22&hl=en-US&gl=US&ceid=US:en'
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=15)
        xml_data = res.read()
        root = ET.fromstring(xml_data)
        
        inserted = 0
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ""
            link = item.find('link').text if item.find('link') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            source = item.find('source').text if item.find('source') is not None else "News Report"
            
            if not title: continue
            
            clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
            words = clean_title.split()
            entity_name = " ".join(words[:5]) + " Scam Report"
            
            domain = extract_domain_from_text(title)
            warning_type = "Employment / Task Scam Alert"
            
            try:
                parsed_date = datetime.strptime(pub_date[:25].strip(), "%a, %d %b %Y %H:%M:%S")
                date_str = parsed_date.strftime("%Y-%m-%d")
            except:
                date_str = datetime.now().strftime("%Y-%m-%d")
                
            reason = f"Public alert regarding an employment scam. Source: {source}. Details: {title}"
            
            if insert_scam_report(entity_name, domain, source, warning_type, date_str, link, reason, "Global"):
                inserted += 1
                
        print(f"[JobScamRadar] Successfully harvested {inserted} new real job scams from news feeds.")
    except Exception as e:
        print(f"[JobScamRadar] Failed to harvest from RSS: {e}")

def harvest_ddgs_reddit_scams():
    if not DDGS:
        print("[JobScamRadar] duckduckgo_search not installed, skipping deep historical scrape.")
        return
    
    print("[JobScamRadar] Launching Deep Scrape on DuckDuckGo for Reddit r/scams historical reports...")
    
    keywords = [
        'site:reddit.com/r/scams "task scam"',
        'site:reddit.com/r/scams "job scam"',
        'site:reddit.com/r/scams "whatsapp recruiter"',
        'site:reddit.com/r/scams "telegram job"',
        'site:reddit.com/r/scams "data entry scam"',
        'site:reddit.com/r/scams "upwork scam"',
        'site:reddit.com/r/scams "indeed scam"',
        'site:reddit.com/r/jobs "job scam"',
        'site:reddit.com/r/recruitinghell "job scam"'
    ]
    
    ddgs = DDGS()
    total_inserted = 0
    
    for kw in keywords:
        print(f"[JobScamRadar] Querying DDGS for: {kw}")
        try:
            results = list(ddgs.text(kw, max_results=300))
            for res in results:
                title = res.get('title', '')
                href = res.get('href', '')
                body = res.get('body', '')
                
                # Try to extract the company name being warned about
                # Often people post "Is [Company] a scam?"
                entity_name = "Unknown Job Scam"
                match = re.search(r'is\s+([A-Za-z0-9\s]+?)\s+a scam', title, re.IGNORECASE)
                if match:
                    entity_name = match.group(1).strip() + " Job Scam"
                else:
                    clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title).replace('reddit', '').replace('rscams', '')
                    words = clean_title.split()
                    if len(words) > 0:
                        entity_name = " ".join(words[:6]) + " Scam"
                
                domain = extract_domain_from_text(title + " " + body)
                reason = body if body else title
                
                if insert_scam_report(entity_name, domain, "Reddit /r/scams Community", "Community Alert: Job/Task Scam", datetime.now().strftime("%Y-%m-%d"), href, reason, "Global"):
                    total_inserted += 1
            
            time.sleep(2) # rate limit
        except Exception as e:
            print(f"[JobScamRadar] DDGS Query failed for '{kw}': {e}")
            
    print(f"[JobScamRadar] Deep Scrape completed. Successfully harvested {total_inserted} new historical community alerts.")

if __name__ == "__main__":
    init_db()
    harvest_google_news_scams()
    harvest_ddgs_reddit_scams()
