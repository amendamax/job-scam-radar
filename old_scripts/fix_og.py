import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
index_html = os.path.join(base_dir, "index.html")

with open(index_html, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("verifydating_og_banner.jpg", "jobscamradar_og_banner.jpg")
html = html.replace("og_image.png", "jobscamradar_og.png")

with open(index_html, "w", encoding="utf-8") as f:
    f.write(html)
