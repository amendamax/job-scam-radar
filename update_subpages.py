import re

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract header and footer
header_match = re.search(r'<header>.*?</header>', html, re.DOTALL)
header_html = header_match.group(0) if header_match else '<header><h1>JobScamRadar</h1></header>'
footer_match = re.search(r'<footer.*?</footer>', html, re.DOTALL)
footer_html = footer_match.group(0) if footer_match else '<footer></footer>'

# Update server.py to use these globally
with open('server.py', 'r', encoding='utf-8') as f:
    server = f.read()

# Define common wrapper in server.py
wrapper_code = f'''
HEADER_HTML = """{header_html}"""
FOOTER_HTML = """{footer_html}"""

def wrap_html(title, content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <style>
        body {{ 
            font-family: system-ui, -apple-system, sans-serif; 
            margin: 0; padding: 0; 
            background: linear-gradient(to bottom, rgba(15,23,42,0.85), rgba(2,6,23,1)), url('/dev_bg.webp') center top / cover fixed;
            color: #f8fafc;
        }}
        header {{ background-color: rgba(15,23,42,0.9); padding: 20px; text-align: center; border-bottom: 1px solid #1e293b; }}
        header h1 {{ margin: 0; font-size: 28px; }}
        header h1 a {{ color: #38bdf8; text-decoration: none; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 40px 20px; min-height: 60vh; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .card {{ background-color: rgba(15,23,42,0.9); border: 1px solid #1e293b; border-radius: 8px; padding: 20px; transition: transform 0.2s; text-decoration: none; color: inherit; display: block; }}
        .card:hover {{ transform: translateY(-3px); border-color: #38bdf8; }}
        .card h4 {{ margin: 0 0 10px 0; font-size: 18px; color: #e2e8f0; }}
        .card p {{ margin: 0; font-size: 14px; color: #94a3b8; line-height: 1.4; }}
        .badge {{ display: inline-block; font-size: 12px; font-weight: bold; padding: 3px 8px; border-radius: 4px; margin-bottom: 10px; color: white; }}
        
        .dossier {{ background: rgba(11,21,40,0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 30px; }}
        .dossier .header {{ border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 20px; }}
        .dossier h1 {{ margin: 0 0 10px 0; }}
        .details-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .detail-item {{ background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); }}
        .detail-item strong {{ color: #94a3b8; display: block; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }}
        .reason {{ margin-top: 30px; padding: 20px; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; border-radius: 0 8px 8px 0; }}
    </style>
</head>
<body>
    {{HEADER_HTML}}
    <div class="container">
        {{content}}
    </div>
    {{FOOTER_HTML}}
</body>
</html>
"""
'''

# Update the scammers route in server
scammers_route = '''@app.get("/scammers")
def job_scams_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT slug, entity_name, domain, warning_type, warning_date, risk_score
        FROM job_scam_reports
        ORDER BY warning_date DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    items_html = ""
    for row in rows:
        slug, entity_name, domain, warning_type, warning_date, risk_score = row
        score_color = "#ef4444" if risk_score and risk_score >= 80 else "#f59e0b"
        items_html += f"""
        <a href="/scammer/{html_lib.escape(slug)}" class="card">
            <div class="badge" style="background-color: {score_color};">Risk: {risk_score}%</div>
            <h4>{html_lib.escape(entity_name)}</h4>
            <p><strong>Domain:</strong> {html_lib.escape(domain)}<br>
            <strong>Type:</strong> {html_lib.escape(warning_type)}<br>
            <strong>Warned:</strong> {warning_date}</p>
        </a>
        """

    content = f"""
        <h1 style="border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 20px;">Job Scam Directory ({len(rows)} Cases)</h1>
        <div class="grid">
            {items_html}
        </div>
    """
    return HTMLResponse(content=wrap_html("Job Scam Directory - JobScamRadar", content))
'''

# Update scammer subpage
scammer_detail_route = '''@app.get("/scammer/{slug}")
def job_scam_detail(request: Request, slug: str, lang: str = "en"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, entity_name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction, risk_score
        FROM job_scam_reports WHERE slug = ?
    """, (slug,))
    row = cursor.fetchone()
    conn.close()
            
    if not row:
        raise HTTPException(status_code=404, detail="Job Scam Report Not Found")
        
    pid, name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction, risk_score = row
    
    score_color = "#ef4444" if risk_score and risk_score >= 80 else "#f59e0b"

    content = f"""
        <div style="margin-bottom: 20px;">
            <a href="/scammers" style="color: #38bdf8; text-decoration: none;">&larr; Back to Directory</a>
        </div>
        <div class="dossier">
            <div class="header">
                <h1>{html_lib.escape(name)}</h1>
                <div class="badge" style="background-color: {score_color};">Risk Score: {risk_score}%</div>
            </div>
            
            <div class="details-grid">
                <div class="detail-item"><strong>Domain</strong> {html_lib.escape(domain)}</div>
                <div class="detail-item"><strong>Regulator Warning</strong> {html_lib.escape(regulator)}</div>
                <div class="detail-item"><strong>Warning Type</strong> {html_lib.escape(warning_type)}</div>
                <div class="detail-item"><strong>Warning Date</strong> {warning_date}</div>
                <div class="detail-item"><strong>Jurisdiction</strong> {html_lib.escape(jurisdiction)}</div>
                <div class="detail-item"><strong>Official Source</strong> <a href="{html_lib.escape(official_url)}" target="_blank" style="color: #38bdf8;">View Original Alert</a></div>
            </div>

            <div class="reason">
                <h3 style="margin-top:0;">Reason for Warning</h3>
                <p style="margin-bottom:0;">{html_lib.escape(reason)}</p>
            </div>
        </div>
        
        <script type="application/ld+json">
        {{
          "@context": "https://schema.org",
          "@type": "ClaimReview",
          "datePublished": "{warning_date}",
          "url": "https://jobscamradar.com/scammer/{slug}",
          "author": {{
            "@type": "Organization",
            "name": "JobScamRadar",
            "url": "https://jobscamradar.com"
          }},
          "claimReviewed": "The company '{html_lib.escape(name)}' is offering legitimate jobs",
          "reviewRating": {{
            "@type": "Rating",
            "ratingValue": "1",
            "bestRating": "5",
            "worstRating": "1",
            "alternateName": "Confirmed Scam"
          }},
          "itemReviewed": {{
            "@type": "Organization",
            "name": "{html_lib.escape(name)}"
          }}
        }}
        </script>
    """
    return HTMLResponse(content=wrap_html(f"{html_lib.escape(name)} - Scam Alert | JobScamRadar", content))
'''

# Replace in server code
# First, insert wrapper code after imports
server = re.sub(r'(import sqlite3\n)', r'\1' + wrapper_code + '\n', server, 1)

# Replace the scammers route
server = re.sub(r'@app\.get\("/scammers"\).*?return HTMLResponse\(content=html\)', scammers_route, server, flags=re.DOTALL)

# Replace the scammer slug route
server = re.sub(r'@app\.get\("/scammer/\{slug\}"\).*?return HTMLResponse\(content=html\)', scammer_detail_route, server, flags=re.DOTALL)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(server)
