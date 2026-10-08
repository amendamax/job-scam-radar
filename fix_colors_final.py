import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
index_html = os.path.join(base_dir, "index.html")

with open(index_html, "r", encoding="utf-8") as f:
    html = f.read()

# Replace hex and rgba pinks with amber/orange
html = html.replace("#ec4899", "#f59e0b")
html = html.replace("#db2777", "#d97706")
html = html.replace("#be185d", "#b45309")
html = html.replace("#f472b6", "#fbbf24")
html = html.replace("#f9a8d4", "#fcd34d")
html = html.replace("rgba(236, 72, 153", "rgba(245, 158, 11")
html = html.replace("rgba(219, 39, 119", "rgba(217, 119, 6")
html = html.replace("rgba(236,72,153", "rgba(245,158,11")
html = html.replace("VERIFY<strong style=\"color: #f59e0b;\">DATING</strong>", "JOB<strong style=\"color: #f59e0b;\">SCAM</strong>")

with open(index_html, "w", encoding="utf-8") as f:
    f.write(html)

server_py = os.path.join(base_dir, "server.py")
with open(server_py, "r", encoding="utf-8") as f:
    py = f.read()

# Remove the broken directory routes that use generate_az_page
import re
py = re.sub(r'@app\.get\("/directory/companys"\)[\s\S]*?return HTMLResponse\(content=generate_az_page[^\)]+\)\)\s*', '', py)
py = re.sub(r'@app\.get\("/directory/dating"\)[\s\S]*?return HTMLResponse\(content=generate_az_page[^\)]+\)\)\s*', '', py)

with open(server_py, "w", encoding="utf-8") as f:
    f.write(py)

print("Fixed HTML colors and removed broken Python routes.")
