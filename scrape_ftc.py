"""
FTC Consumer Alerts importer for JobScamRadar.

Reads the public listing at https://consumer.ftc.gov/consumer-alerts (paginated),
keeps only job/employment-related alerts and inserts them into job_scam_reports.

- Respects robots.txt: Crawl-delay 10s, no disallowed paths
- Direct connection (no proxy needed, no evasion)
- Only real data from the listing: title, date, official summary, source URL
"""
import json
import re
import sqlite3
import sys
import time
import uuid
from datetime import datetime
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE = "https://consumer.ftc.gov/consumer-alerts"
UA = "Mozilla/5.0 (compatible; JobScamRadarBot/1.0)"
CRAWL_DELAY = 10  # seconds, from FTC robots.txt
DB_PATH = "database.db"
MAX_PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 30

STRONG = [
    "employment", "recruiter", "recruiters", "recruitment", "hiring", "job offer", "job offers",
    "job scam", "job scams", "job seeker", "job seekers", "job listing", "job listings",
    "job posting", "job postings", "work from home", "work-from-home", "remote work",
    "mystery shopper", "mystery shopping", "money mule", "reshipping", "paycheck",
    "fake employer", "employer", "side hustle",
]
WEAK = ["job", "jobs", "gig", "gigs", "task", "tasks"]  # only counted in the TITLE
STRONG_RE = re.compile(r"\b(" + "|".join(re.escape(k) for k in STRONG) + r")\b", re.I)
WEAK_RE = re.compile(r"\b(" + "|".join(re.escape(k) for k in WEAK) + r")\b", re.I)


def is_job_related(title, summary):
    return bool(STRONG_RE.search(title + " " + summary) or WEAK_RE.search(title))


def slugify(text):
    text = re.sub(r"[^a-z0-9\s-]", "", text.lower())
    return re.sub(r"[\s-]+", "-", text).strip("-")


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for art in soup.select("article"):
        a = art.select_one("h3 a")
        if not a:
            continue
        t = art.select_one("time")
        body = art.select_one(".field--name-body .field__item")
        out.append({
            "title": a.get_text(" ", strip=True),
            "url": a.get("href"),
            "date": (t.get("datetime", "")[:10] if t else ""),
            "summary": body.get_text(" ", strip=True) if body else "",
        })
    return out


def main():
    rp = RobotFileParser()
    rr = requests.get("https://consumer.ftc.gov/robots.txt", headers={"User-Agent": UA}, timeout=30)
    rp.parse(rr.text.splitlines())

    session = requests.Session()
    session.headers.update({"User-Agent": UA})

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    total_seen = total_match = inserted = 0

    for page in range(MAX_PAGES):
        url = BASE if page == 0 else f"{BASE}?page={page}"
        if not rp.can_fetch(UA, url):
            print(f"[!] robots.txt interzice {url}. Stop.")
            break
        r = session.get(url, timeout=30)
        if r.status_code != 200:
            print(f"[!] HTTP {r.status_code} la {url}. Stop.")
            break
        items = parse_page(r.text)
        if not items:
            print(f"[*] Pagina {page} fara articole. Stop.")
            break

        page_match = 0
        for it in items:
            total_seen += 1
            if not is_job_related(it["title"], it["summary"]):
                continue
            total_match += 1
            page_match += 1
            cur.execute("SELECT 1 FROM job_scam_reports WHERE official_url = ?", (it["url"],))
            if cur.fetchone():
                continue
            title = it["title"]
            cur.execute(
                """INSERT INTO job_scam_reports
                (slug, entity_name, domain, regulator, warning_type, warning_date, official_url,
                 reason, jurisdiction, risk_score, blacklisted_urls, clone_of, details_json, created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    slugify(title)[:60] + "-" + uuid.uuid4().hex[:8],
                    title[:120], "consumer.ftc.gov", "FTC (US Federal Trade Commission)",
                    "Official Consumer Alert", it["date"], it["url"],
                    it["summary"], "United States", 9, "", "",
                    json.dumps({"source": "FTC Consumer Alerts"}),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            inserted += 1
        conn.commit()
        print(f"[+] Pagina {page}: {len(items)} alerte, {page_match} relevante | inserate total: {inserted}", flush=True)
        time.sleep(CRAWL_DELAY)

    conn.close()
    print(f"[*] GATA. Vazute: {total_seen}, relevante job: {total_match}, noi inserate: {inserted}")


if __name__ == "__main__":
    main()
