import os
import re

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
index_html = os.path.join(base_dir, "index.html")

with open(index_html, "r", encoding="utf-8") as f:
    html = f.read()

# Remove header buttons for B2B API and Safety Toolkit
html = re.sub(r'<a href="/api/v1/job-docs" class="btn-api">.*?</a>', '', html, flags=re.DOTALL)
html = re.sub(r'<a href="/widget" class="btn-api btn-api-toolkit">.*?</a>', '', html, flags=re.DOTALL)

# Remove the whole B2B section
html = re.sub(r'<!-- DEVELOPER & DATING PLATFORMS B2B REST API SECTION.*?</section>', '', html, flags=re.DOTALL)

with open(index_html, "w", encoding="utf-8") as f:
    f.write(html)

print("API section removed from HTML.")
