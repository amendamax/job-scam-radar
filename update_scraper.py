import os
import re

with open('scrape_real_scams.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add requests if not already imported
if 'import requests' not in code:
    code = 'import requests\n' + code

# Add dotenv support
import_dotenv = '''
import os
from dotenv import load_dotenv

load_dotenv()

PROXY_HOST = os.getenv('ANYIP_HOST', 'portal.anyip.io')
PROXY_PORT = os.getenv('ANYIP_PORT', '1080')
PROXY_USER = os.getenv('ANYIP_USER', '')
PROXY_PASS = os.getenv('ANYIP_PASS', '')

PROXIES = None
if PROXY_USER and PROXY_PASS:
    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
    PROXIES = {
        'http': proxy_url,
        'https': proxy_url
    }
'''
code = re.sub(r'DB_PATH = .*?\n', r'\g<0>' + import_dotenv + '\n', code, count=1)

# Modify feedparser calls to use requests with proxies
scrape_reddit_new = '''
    try:
        if PROXIES:
            print("Fetching Reddit with AnyIP Proxy...")
            response = requests.get(url, proxies=PROXIES, timeout=15)
            feed = feedparser.parse(response.content)
        else:
            feed = feedparser.parse(url)
'''
code = code.replace('''    try:
        feed = feedparser.parse(url)''', scrape_reddit_new, 1)

scrape_google_new = '''
        try:
            if PROXIES:
                print(f"Fetching Google News '{q}' with AnyIP Proxy...")
                response = requests.get(url, proxies=PROXIES, timeout=15)
                feed = feedparser.parse(response.content)
            else:
                feed = feedparser.parse(url)
'''
code = code.replace('''        try:
            feed = feedparser.parse(url)''', scrape_google_new, 1)

with open('scrape_real_scams.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('.env', 'w', encoding='utf-8') as f:
    f.write('''ANYIP_HOST=portal.anyip.io
ANYIP_PORT=1080
ANYIP_USER=
ANYIP_PASS=
''')

with open('.gitignore', 'a', encoding='utf-8') as f:
    f.write('\n.env\n')
