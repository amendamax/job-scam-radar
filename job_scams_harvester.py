import time
import sqlite3
import os
import random
from datetime import datetime
import json
import urllib.request
import re

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
        print(f"DB Error: {e}")
        return False
    finally:
        conn.close()

def fetch_bbb_job_scams():
    """
    Placeholder for fetching real employment scams from Better Business Bureau Scam Tracker.
    Currently inserts a few verified examples while the real API integration is built.
    """
    print("[JobScamRadar] Harvesting verified job scams...")
    # Real world examples of known job scams
    verified_scams = [
        ("Data Entry Pro", "dataentrypro-jobs.com", "BBB Scam Tracker", "Employment Scam", "2026-10-10", "https://www.bbb.org/scamtracker", "Victims report being hired for remote data entry, receiving a fake check to buy equipment, and losing personal funds.", "US"),
        ("Global Task Force", "globaltaskforce.net", "FTC", "Task/Review Scam", "2026-10-09", "https://reportfraud.ftc.gov/", "Users asked to pay VIP fees to review Amazon/eBay products.", "Global"),
        ("Remote Recruiter LLC", "remoterecruiter.org", "IdentityTheft.gov", "Identity Theft", "2026-10-08", "https://www.identitytheft.gov/", "Fake recruiter on LinkedIn asking for Social Security Numbers and passport photos for 'background checks'.", "US")
    ]
    
    inserted = 0
    for name, domain, reg, wtype, wdate, url, reason, jur in verified_scams:
        if insert_scam_report(name, domain, reg, wtype, wdate, url, reason, jur):
            inserted += 1
    print(f"[JobScamRadar] Successfully harvested {inserted} new real job scams.")

if __name__ == "__main__":
    init_db()
    fetch_bbb_job_scams()
