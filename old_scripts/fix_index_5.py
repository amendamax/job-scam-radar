import os
import re

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Remove Directory link line
html = re.sub(r'<p style="margin: 0 0 10px 0;"><a href="/directory".*?</a></p>', '', html)

# Remove social proof toast
html = re.sub(r'<!-- Social Proof Toast Notification Container -->.*?</div>\s*</div>\s*<button class="toast-close".*?</button>\s*</div>', '', html, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
