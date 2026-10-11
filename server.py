import os
import sqlite3
import html as html_lib
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title="JobScamRadar Core API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheMiddleware)

DB_PATH = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

# Static routes
@app.get("/")
def serve_index():
    return FileResponse("index.html")

@app.get("/style.css")
def serve_style():
    return FileResponse("style.css")

@app.get("/index.css")
def serve_index_css():
    return FileResponse("index.css")

@app.get("/scammers")
def job_scams_directory(request: Request):
    """
    Directory listing of all Job Scams.
    """
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
        <a href="/scammer/{html_lib.escape(slug)}" style="text-decoration: none; display: block;">
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-bottom: 10px; color: white;">
                <h3 style="margin: 0 0 5px 0;">{html_lib.escape(entity_name)} <span style="font-size: 12px; padding: 2px 6px; background: {score_color}; border-radius: 4px; margin-left: 10px;">Risk: {risk_score}%</span></h3>
                <p style="margin: 0; font-size: 14px; color: #94a3b8;">Domain: {html_lib.escape(domain)} | Type: {html_lib.escape(warning_type)}</p>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #64748b;">Warned: {warning_date}</p>
            </div>
        </a>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Scam Directory - JobScamRadar</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #05080f; color: white; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Job Scam Directory ({len(rows)} Cases)</h1>
        <a href="/" style="color: #38bdf8; text-decoration: none; display: inline-block; margin-bottom: 20px;">&larr; Back to Home</a>
        <div class="list">
            {items_html}
        </div>
    </div>
</body>
</html>
"""
    return HTMLResponse(content=html)

@app.get("/scammer/{slug}")
def job_scam_detail(request: Request, slug: str, lang: str = "en"):
    """
    Dossier on an individual Job Scam Report.
    """
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

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_lib.escape(name)} - Scam Alert | JobScamRadar</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #05080f; color: white; padding: 20px; line-height: 1.6; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #0b1528; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 30px; }}
        .header {{ border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 20px; }}
        h1 {{ margin: 0 0 10px 0; }}
        .badge {{ display: inline-block; background: {score_color}; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 14px; margin-bottom: 20px; }}
        .details-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .detail-item {{ background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); }}
        .detail-item strong {{ color: #94a3b8; display: block; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }}
        .reason {{ margin-top: 30px; padding: 20px; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; border-radius: 0 8px 8px 0; }}
    </style>
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
</head>
<body>
    <div style="max-width: 800px; margin: 0 auto 20px auto;">
        <a href="/scammers" style="color: #38bdf8; text-decoration: none;">&larr; Back to Directory</a>
    </div>
    <div class="container">
        <div class="header">
            <h1>{html_lib.escape(name)}</h1>
            <div class="badge">Risk Score: {risk_score}%</div>
        </div>
        
        <div class="details-grid">
            <div class="detail-item">
                <strong>Domain</strong>
                {html_lib.escape(domain)}
            </div>
            <div class="detail-item">
                <strong>Regulator Warning</strong>
                {html_lib.escape(regulator)}
            </div>
            <div class="detail-item">
                <strong>Warning Type</strong>
                {html_lib.escape(warning_type)}
            </div>
            <div class="detail-item">
                <strong>Warning Date</strong>
                {warning_date}
            </div>
            <div class="detail-item">
                <strong>Jurisdiction</strong>
                {html_lib.escape(jurisdiction)}
            </div>
            <div class="detail-item">
                <strong>Official Source</strong>
                <a href="{html_lib.escape(official_url)}" target="_blank" style="color: #38bdf8;">View Original Alert</a>
            </div>
        </div>

        <div class="reason">
            <h3 style="margin-top:0;">Reason for Warning</h3>
            <p style="margin-bottom:0;">{html_lib.escape(reason)}</p>
        </div>
    </div>
</body>
</html>
"""
    return HTMLResponse(content=html)

@app.get("/sitemap.xml")
def sitemap_index():
    base_url = "https://jobscamradar.com"
    today = datetime.now().strftime("%Y-%m-%d")
    xml_index = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{base_url}/sitemap-job-scams.xml</loc>
    <lastmod>{today}</lastmod>
  </sitemap>
</sitemapindex>"""
    return Response(content=xml_index, media_type="application/xml")

@app.get("/sitemap-job-scams.xml")
def sitemap_part():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT slug, warning_date FROM job_scam_reports ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    today = datetime.now().strftime("%Y-%m-%d")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    xml.append('  <url>')
    xml.append('    <loc>https://jobscamradar.com/scammers</loc>')
    xml.append(f'    <lastmod>{today}</lastmod>')
    xml.append('    <changefreq>daily</changefreq>')
    xml.append('    <priority>0.9</priority>')
    xml.append('  </url>')

    for slug, rep_date in rows:
        safe_slug = html_lib.escape(slug)
        lastmod = rep_date if rep_date else today
        loc = f"https://jobscamradar.com/scammer/{safe_slug}"
        xml.append('  <url>')
        xml.append(f'    <loc>{loc}</loc>')
        xml.append(f'    <lastmod>{lastmod}</lastmod>')
        xml.append('    <changefreq>weekly</changefreq>')
        xml.append('    <priority>0.8</priority>')
        xml.append('  </url>')

    xml.append('</urlset>')
    return Response(content="\n".join(xml), media_type="application/xml")

@app.get("/robots.txt")
def robots():
    content = """User-agent: *
Allow: /
Sitemap: https://jobscamradar.com/sitemap.xml
"""
    return Response(content=content, media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
