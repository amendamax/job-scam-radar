import os
import re

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Remove the entire Scanner Section
html = re.sub(r'<section class="scanner-section" id="scanner-workspace">.*?</section>', '', html, flags=re.DOTALL)

# Remove the entire Exit-Intent Modal
html = re.sub(r'<!-- EXIT-INTENT MODAL -->\s*<div id="exit-intent-modal" class="exit-modal-backdrop".*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
