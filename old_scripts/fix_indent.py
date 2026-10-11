import re

lines = open('server.py', 'r', encoding='utf-8').read()

lines = re.sub(r'\s*for l in langs:\s*urls.append.*?<\/url>\'\)', '', lines, flags=re.DOTALL)

open('server.py', 'w', encoding='utf-8').write(lines)
