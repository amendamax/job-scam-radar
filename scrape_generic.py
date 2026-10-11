"""
Generic web scraper: requests + BeautifulSoup, authenticated proxy from .env,
2s rate limiting, respects robots.txt, saves to date_extrase.json.

Example:
  python scrape_generic.py --url "https://example.com/reports?page={page}" ^
      --pages 5 --item ".card" --title "h2" --date ".date" --desc "p"

Use {page} in --url for paginated listings.
Stops on 403/429 (does NOT retry or try to evade blocks).
"""
import argparse
import json
import os
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = "Mozilla/5.0 (compatible; JobScamRadarBot/1.0)"
RATE_LIMIT_SECONDS = 2


def get_proxies():
    user = os.getenv("ANYIP_USER")
    pwd = os.getenv("ANYIP_PASS")
    host = os.getenv("ANYIP_HOST", "portal.anyip.io")
    port = os.getenv("ANYIP_PORT", "1080")
    if not (user and pwd):
        return None
    url = f"http://{user}:{pwd}@{host}:{port}"
    return {"http": url, "https": url}


def allowed_by_robots(url):
    p = urlparse(url)
    rp = RobotFileParser()
    try:
        rr = requests.get(f"{p.scheme}://{p.netloc}/robots.txt",
                          headers={"User-Agent": USER_AGENT}, timeout=20)
    except Exception:
        return True  # robots.txt unreachable -> treat as no restrictions
    if rr.status_code in (401, 403):
        return False  # site refuses us -> do not crawl
    if rr.status_code != 200:
        return True
    rp.parse(rr.text.splitlines())
    return rp.can_fetch(USER_AGENT, url)


def text_of(node, selector):
    if not selector:
        return ""
    el = node.select_one(selector)
    return el.get_text(" ", strip=True) if el else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL, may contain {page}")
    ap.add_argument("--pages", type=int, default=1)
    ap.add_argument("--item", required=True, help="CSS selector for repeated card/row")
    ap.add_argument("--title", required=True)
    ap.add_argument("--date", default="")
    ap.add_argument("--desc", default="")
    ap.add_argument("--out", default="date_extrase.json")
    args = ap.parse_args()

    proxies = get_proxies()
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    results = []

    for page in range(1, args.pages + 1):
        url = args.url.format(page=page)
        if not allowed_by_robots(url):
            print(f"[!] robots.txt interzice {url} - ma opresc.")
            break
        try:
            r = session.get(url, proxies=proxies, timeout=20)
        except requests.RequestException as e:
            print(f"[!] Eroare retea la {url}: {e}")
            break
        if r.status_code in (403, 429):
            print(f"[!] {r.status_code} la {url} - site-ul refuza accesul automat. Ma opresc.")
            break
        if r.status_code != 200:
            print(f"[!] HTTP {r.status_code} la {url} - ma opresc.")
            break

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select(args.item)
        if not items:
            print(f"[*] Niciun element gasit pe pagina {page}. Stop.")
            break
        for it in items:
            results.append({
                "titlu": text_of(it, args.title),
                "data": text_of(it, args.date),
                "poveste": text_of(it, args.desc),
                "url_sursa": url,
            })
        print(f"[+] Pagina {page}: {len(items)} elemente (total {len(results)})")
        time.sleep(RATE_LIMIT_SECONDS)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[*] Salvat {len(results)} inregistrari in {args.out}")


if __name__ == "__main__":
    main()
