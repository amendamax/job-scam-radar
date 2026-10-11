import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
server_py = os.path.join(base_dir, "server.py")

with open(server_py, "r", encoding="utf-8") as f:
    py = f.read()

py = py.replace('sitemap-dating-scams.xml', 'sitemap-scammers.xml')
py = py.replace('sitemap-dating-scams-{part}.xml', 'sitemap-scammers-{part}.xml')

with open(server_py, "w", encoding="utf-8") as f:
    f.write(py)
