import os
import re

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Remove the Ticker Section
html = re.sub(r'<!-- Live Scan Feed / Activity Ticker \(Premium Design Touch\) -->\s*<section class="live-activity-section">.*?</section>', '', html, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
