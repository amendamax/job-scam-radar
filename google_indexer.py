import os
import json
import sqlite3
import requests
import time
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import Request

DB_PATH = "database.db"
KEY_PATH = "/etc/secrets/jobscam-indexer.json"
if not os.path.exists(KEY_PATH):
    KEY_PATH = os.path.join("keys", "jobscam-indexer.json")
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

TRACKER = "last_id_jobscam.txt"
DOMAIN = "https://jobscamradar.com/scammer"

def get_last_id(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read().strip()
            if content.isdigit():
                return int(content)
    return 0

def save_last_id(filename, last_id):
    with open(filename, 'w') as f:
        f.write(str(last_id))

def get_access_token(key_path):
    if not os.path.exists(key_path):
        print(f"[!] Lipseste cheia Google API: {key_path}")
        return None
    try:
        credentials = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=["https://www.googleapis.com/auth/indexing"]
        )
        request = Request()
        credentials.refresh(request)
        return credentials.token
    except Exception as e:
        print(f"[!] Eroare la autentificare token din {key_path}: {e}")
        return None

def publish_url(url, token):
    payload = {
        "url": url,
        "type": "URL_UPDATED"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    return requests.post(ENDPOINT, headers=headers, json=payload)

def main():
    print("==================================================")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] START GOOGLE INDEXER - JOBSCAMRADAR")
    print("==================================================")

    token = get_access_token(KEY_PATH)
    if not token:
        print("Nu am token, iesire.")
        return

    last_id = get_last_id(TRACKER)
    
    # Ne logam in baza de date
    if not os.path.exists(DB_PATH):
        print("Nu s-a gasit baza de date.")
        return
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Aducem inregistrarile noi
    c.execute("SELECT id, slug FROM regulatory_scam_reports WHERE id > ? ORDER BY id ASC LIMIT 200", (last_id,))
    rows = c.fetchall()
    
    if not rows:
        print("Nu sunt pagini noi de indexat astazi.")
        conn.close()
        return
        
    print(f"[*] Am gasit {len(rows)} pagini noi de trimis la Google...")
    
    success_count = 0
    quota_exceeded = False
    new_last_id = last_id
    
    for row in rows:
        row_id, slug = row
        url = f"{DOMAIN}/{slug}"
        
        response = publish_url(url, token)
        
        if response.status_code == 200:
            success_count += 1
            new_last_id = row_id
            print(f"[+] TRIMIS: {url}")
        elif response.status_code == 429:
            print("[!] LIMITA ZILNICA GOOGLE (Quota Exceeded). Robotul se opreste pe astazi.")
            quota_exceeded = True
            break
        else:
            print(f"[-] EROARE ({response.status_code}) la {url}: {response.text}")
            
        time.sleep(1) # Pauza ca sa nu suparam Google
        
    save_last_id(TRACKER, new_last_id)
    print(f"\n[*] PROCES FINALIZAT! Am trimis cu succes {success_count} pagini.")
    
    conn.close()

if __name__ == "__main__":
    main()
