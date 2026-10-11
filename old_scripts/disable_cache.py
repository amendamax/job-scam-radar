import re
with open('server.py', 'r', encoding='utf-8') as f:
    s = f.read()

s = re.sub(r'"Cache-Control": "public, max-age=\d+', '"Cache-Control": "no-cache, max-age=0', s)
s = re.sub(r'"Cache-Control"] = "public, max-age=\d+', '"Cache-Control"] = "no-cache, max-age=0', s)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(s)
