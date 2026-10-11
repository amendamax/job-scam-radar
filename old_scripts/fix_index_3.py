import os

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "genuine ID-verified matches": "genuine ID-verified recruiters",
    "OFFICIAL SECURITY & MATCHING NETWORK": "OFFICIAL THREAT INTELLIGENCE NETWORK",
    "affiliate-match-card": "affiliate-job-card",
    "dating-b2b-section": "job-b2b-section",
    "dating-b2b-actions-grid": "job-b2b-actions-grid"
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
