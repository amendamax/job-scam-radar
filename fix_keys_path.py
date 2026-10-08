import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
indexer_py = os.path.join(base_dir, "google_indexer.py")

with open(indexer_py, "r", encoding="utf-8") as f:
    py = f.read()

# Make it check both local keys/ and Render /etc/secrets/
py = py.replace('KEY_PATH = os.path.join("keys", "jobscam-indexer.json")', 
'''KEY_PATH = "/etc/secrets/jobscam-indexer.json"
if not os.path.exists(KEY_PATH):
    KEY_PATH = os.path.join("keys", "jobscam-indexer.json")''')

with open(indexer_py, "w", encoding="utf-8") as f:
    f.write(py)

print("google_indexer.py updated to look in /etc/secrets/")
