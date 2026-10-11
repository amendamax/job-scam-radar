import re

with open('old_index_temp.html', 'r', encoding='utf-16') as f:
    old_html = f.read()
footer_match = re.search(r'<footer.*?</footer>', old_html, re.DOTALL)
old_footer = footer_match.group(0) if footer_match else '<footer>Footer not found</footer>'

with open('index.html', 'r', encoding='utf-8') as f:
    new_html = f.read()

# Replace footer
new_html = re.sub(r'<footer.*?</footer>', old_footer, new_html, flags=re.DOTALL)

# Add background to hero
new_html = new_html.replace(
    '.hero { padding: 60px 20px; text-align: center; background: linear-gradient(to bottom, #0f172a, #020617); }',
    ".hero { padding: 60px 20px; text-align: center; background: linear-gradient(to bottom, rgba(15,23,42,0.8), rgba(2,6,23,1)), url('/dev_bg.webp') center/cover; }"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# Add route to serve dev_bg.webp
with open('server.py', 'r', encoding='utf-8') as f:
    server_code = f.read()

if '/dev_bg.webp' not in server_code:
    route = '''@app.get("/dev_bg.webp")
def serve_dev_bg():
    return FileResponse("dev_bg.webp")
'''
    server_code = server_code.replace('def serve_index_css():\n    return FileResponse("index.css")', 'def serve_index_css():\n    return FileResponse("index.css")\n\n' + route)
    
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(server_code)
