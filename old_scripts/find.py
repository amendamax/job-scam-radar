import re
lines = open('server.py', 'r', encoding='utf-8').readlines()
for i, l in enumerate(lines):
    if '/scammer/{slug}' in l:
        print(f"{i}: {l.strip()}")
