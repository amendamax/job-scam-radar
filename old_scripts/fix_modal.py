import re

html = open('index.html', 'r', encoding='utf-8').read()

html = re.sub(r'<div id="exit-intent-modal".*?</div>\s*</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
html = re.sub(r'var modal = document\.getElementById\(\'exit-intent-modal\'\);.*?\}\);', '', html, flags=re.DOTALL)
html = html.replace('<!-- Exit Intent Modal -->', '')

open('index.html', 'w', encoding='utf-8').write(html)
