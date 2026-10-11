import re

html = open('index.html', 'r', encoding='utf-8').read()
html = re.sub(r'<div class="scanner-grid">.*?<!-- Official Threat Intelligence Network -->', '<!-- Official Threat Intelligence Network -->', html, flags=re.DOTALL)
html = re.sub(r'<div class="scam-alert-banner">.*?</div>', '', html, flags=re.DOTALL) # The Met Someone on Remote Jobs banner

open('index.html', 'w', encoding='utf-8').write(html)
