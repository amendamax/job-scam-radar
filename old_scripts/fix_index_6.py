import os
import re

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove Ticker Section
html = re.sub(r'<!-- Live Ticker Activity -->\s*<section class="ticker-section">.*?</section>', '', html, flags=re.DOTALL)

# 2. Remove Video Section
html = re.sub(r'<!-- Video Explainer Section -->\s*<section class="video-section".*?</section>', '', html, flags=re.DOTALL)

# 3. Remove App Container (The scan module)
html = re.sub(r'<!-- App/Scanner Container -->\s*<div class="app-container" id="scanner">.*?</div>\s*</section>', '</section>', html, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
