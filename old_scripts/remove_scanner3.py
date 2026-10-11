import re

html = open('index.html', 'r', encoding='utf-8').read()

# Remove Met Someone banner
html = re.sub(r'<div class="scam-alert-banner">.*?</div>', '', html, flags=re.DOTALL)

# Remove the whole scanner section
html = re.sub(r'<section class="scanner-section" id="scanner-workspace">.*?</section>', '', html, flags=re.DOTALL)

open('index.html', 'w', encoding='utf-8').write(html)
