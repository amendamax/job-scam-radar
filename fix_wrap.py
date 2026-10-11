import re

with open('server.py', 'r', encoding='utf-8') as f:
    server = f.read()

# Replace the specific wrap_html definition
new_wrap = '''def wrap_html(title, content):
    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body { 
            font-family: system-ui, -apple-system, sans-serif; 
            margin: 0; padding: 0; 
            background: linear-gradient(to bottom, rgba(15,23,42,0.85), rgba(2,6,23,1)), url('/dev_bg.webp') center top / cover fixed;
            color: #f8fafc;
        }
        header { background-color: rgba(15,23,42,0.9); padding: 20px; text-align: center; border-bottom: 1px solid #1e293b; }
        header h1 { margin: 0; font-size: 28px; }
        header h1 a { color: #38bdf8; text-decoration: none; }
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; min-height: 60vh; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .card { background-color: rgba(15,23,42,0.9); border: 1px solid #1e293b; border-radius: 8px; padding: 20px; transition: transform 0.2s; text-decoration: none; color: inherit; display: block; }
        .card:hover { transform: translateY(-3px); border-color: #38bdf8; }
        .card h4 { margin: 0 0 10px 0; font-size: 18px; color: #e2e8f0; }
        .card p { margin: 0; font-size: 14px; color: #94a3b8; line-height: 1.4; }
        .badge { display: inline-block; font-size: 12px; font-weight: bold; padding: 3px 8px; border-radius: 4px; margin-bottom: 10px; color: white; }
        
        .dossier { background: rgba(11,21,40,0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 30px; }
        .dossier .header { border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 20px; }
        .dossier h1 { margin: 0 0 10px 0; }
        .details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .detail-item { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); }
        .detail-item strong { color: #94a3b8; display: block; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }
        .reason { margin-top: 30px; padding: 20px; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; border-radius: 0 8px 8px 0; }
    </style>
</head>
<body>
    {HEADER_HTML}
    <div class="container">
        {content}
    </div>
    {FOOTER_HTML}
</body>
</html>
"""
    return template.replace('{title}', title).replace('{content}', content).replace('{HEADER_HTML}', HEADER_HTML).replace('{FOOTER_HTML}', FOOTER_HTML)'''

# Using regex to replace the function definition completely
server = re.sub(r'def wrap_html.*?return f"""<!DOCTYPE html>.*?</html>\n"""', new_wrap, server, flags=re.DOTALL)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(server)
