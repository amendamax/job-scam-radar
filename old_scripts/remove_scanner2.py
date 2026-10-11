import re

html = open('index.html', 'r', encoding='utf-8').read()

# Try to find the exact scanner grid block.
# Let's see the context
html = re.sub(r'<div class="scanner-grid">.*?<!-- Complete Job Safety', '<!-- Complete Job Safety', html, flags=re.DOTALL)
html = re.sub(r'<div class="scam-alert-banner">.*?</div>\s*</div>\s*<!-- Stats -->', '<!-- Stats -->', html, flags=re.DOTALL)

open('index.html', 'w', encoding='utf-8').write(html)
