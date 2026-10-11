import os

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Remove Scam Directory (A-Z)
html = html.replace('<a href="/directory"><i class="fa-solid fa-folder-tree"></i> Scam Directory (A-Z)</a>', '')

# Remove live-toast div
import re
html = re.sub(r'<!-- LIVE ACTIVITY TOAST -->\s*<div id="live-toast" class="toast-hidden">.*?</div>', '', html, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
