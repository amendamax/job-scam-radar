import re

html = open('index.html', 'r', encoding='utf-8').read()

# Remove Add to Chrome
html = re.sub(r'<a href="/extension" target="_blank".*?Add to Chrome.*?</a>', '', html, flags=re.DOTALL)
# Remove Verify Broker
html = re.sub(r'<a href="https://isbrokersafe\.com/" target="_blank".*?Verify Broker.*?</a>', '', html, flags=re.DOTALL)
# Remove B2B API (the broker one)
html = re.sub(r'<a href="https://isbrokersafe\.com/api/v1/docs" target="_blank".*?B2B API.*?</a>', '', html, flags=re.DOTALL)

open('index.html', 'w', encoding='utf-8').write(html)
