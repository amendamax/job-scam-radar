import os
import sqlite3

HEADER_HTML = """<header>
        <h1 style="text-decoration: none;"><a href="/" style="color: #38bdf8; text-decoration: none;">JobScamRadar</a></h1>
    </header>"""
FOOTER_HTML = """<footer style="background-color: #05080f; padding: 60px 20px 20px 20px; font-family: system-ui, -apple-system, sans-serif; color: #94a3b8; font-size: 14px; border-top: 1px solid #1e293b; margin-top: 60px;">
    <div style="max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px;">
        
        <div>
            <h3 style="color: #f8fafc; margin-top: 0; font-size: 18px; display: flex; align-items: center; gap: 8px;">
                <span style="width: 20px; height: 20px; background-color: #1e293b; border-radius: 4px; display: inline-block;"></span>
                JOBSCAM<span style="color: #38bdf8;">RADAR</span>
            </h3>
            <p style="line-height: 1.6; margin-bottom: 20px;">Employment fraud defense system. Identifying fake recruitment agencies, task scams, and human trafficking operations.</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <span style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 8px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.2); font-size: 12px;">✔️ VIES Verified EU</span>
                <span style="background: rgba(56, 189, 248, 0.1); color: #38bdf8; padding: 4px 8px; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.2); font-size: 12px;">⭐ 100% Free Public Utility</span>
            </div>
        </div>

        <div>
            <h4 style="color: #38bdf8; margin-top: 0; font-size: 16px; margin-bottom: 20px;">VasileDev Group Ecosystem</h4>
            <ul style="list-style: none; padding: 0; margin: 0; line-height: 2.2;">
                <li><strong>VAT / P.IVA:</strong> <span style="background: rgba(56, 189, 248, 0.1); color: #38bdf8; padding: 2px 6px; border-radius: 4px;">IT04226190041</span></li>
                <li><strong>Locations:</strong> Garessio (CN), Italy & Odobești, Romania</li>
                <li><strong>Direct:</strong> amendamax@vasiledev.com</li>
            </ul>
        </div>

        <div>
            <h4 style="color: #38bdf8; margin-top: 0; font-size: 16px; margin-bottom: 20px;">Official Network</h4>
            <ul style="list-style: none; padding: 0; margin: 0; line-height: 2.2;">
                <li><a href="https://isbrokersafe.com" style="color: #94a3b8; text-decoration: none;">🛡️ IsBrokerSafe.com</a></li>
                <li><a href="https://jobscamradar.com" style="color: #38bdf8; font-weight: bold; text-decoration: none;">💼 JobScamRadar.com</a></li>
                <li><a href="https://pillscamradar.com" style="color: #94a3b8; text-decoration: none;">💊 PillScamRadar.com</a></li>
                <li><a href="https://verifydating.net" style="color: #94a3b8; text-decoration: none;">❤️ VerifyDating.net</a></li>
                <li><a href="https://appscamradar.com" style="color: #94a3b8; text-decoration: none;">📱 AppScamRadar.com</a></li>
                <li><a href="https://dreamcarhunt.com" style="color: #94a3b8; text-decoration: none;">🏎️ DreamCarHunt.com</a></li>
                <li><a href="https://airparkrefund.com" style="color: #94a3b8; text-decoration: none;">✈️ AirParkRefund.com</a></li>
                <li><a href="https://vasiledev.com" style="color: #94a3b8; text-decoration: none;">👨‍💻 VasileDev.com</a></li>
            </ul>
        </div>

    </div>
    
    <div style="text-align: center; margin-top: 60px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); color: #64748b; font-size: 13px;">
        &copy; 2026 JobScamRadar™ by VasileDev Group. All rights reserved. Powered globally by Cloudflare Edge Network.
    </div>
</footer>"""

INCOGNI_URL = os.getenv("INCOGNI_URL", "https://incogni.com/")
FLEXJOBS_URL = os.getenv("FLEXJOBS_URL", "https://flexjobs.com/")

AFFILIATE_HTML = """<div class="affiliate-section">
            <div class="aff-card privacy">
                <h4>🛡️ Delete Personal Info &amp; Dark Web Defense</h4>
                <p>Shared your phone, email, or selfies with a fake recruiter? Automatically delete your records from 180+ data brokers.</p>
                <a href="{INCOGNI_URL}" target="_blank" rel="sponsored noopener noreferrer">Remove My Data (Incogni)</a>
            </div>
            <div class="aff-card jobs">
                <h4>🤝 Meet Genuine, Verified Employers</h4>
                <p>Tired of WhatsApp recruiters and fake data entry jobs? Join platforms where every job is hand-screened.</p>
                <a href="{FLEXJOBS_URL}" target="_blank" rel="sponsored noopener noreferrer">Find Safe Remote Jobs</a>
            </div>
            <p class="aff-disclosure">Disclosure: some links above are affiliate links. If you sign up through them we may earn a commission, at no extra cost to you.</p>
        </div>""".replace("{INCOGNI_URL}", INCOGNI_URL).replace("{FLEXJOBS_URL}", FLEXJOBS_URL)

def wrap_html(title, content):
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
        .affiliate-section { margin-top: 60px; display: grid; grid-template-columns: 1fr; gap: 20px; }
        .aff-card { padding: 20px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
        .aff-card.privacy { background-color: #022c22; }
        .aff-card.jobs { background-color: #451a03; }
        .aff-card h4 { margin: 0 0 10px 0; font-size: 20px; }
        .aff-card p { font-size: 14px; color: #cbd5e1; margin-bottom: 15px; }
        .aff-card a { display: inline-block; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; color: white; background: rgba(0,0,0,0.3); }
        .aff-disclosure { font-size: 12px; color: #94a3b8; text-align: center; margin: 0; }
    </style>
</head>
<body>
    {HEADER_HTML}
    <div class="container">
        {content}
        {AFFILIATE_HTML}
    </div>
    {FOOTER_HTML}
</body>
</html>
"""
    return template.replace('{title}', title).replace('{content}', content).replace('{HEADER_HTML}', HEADER_HTML).replace('{FOOTER_HTML}', FOOTER_HTML).replace('{AFFILIATE_HTML}', AFFILIATE_HTML)

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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT slug, entity_name, warning_type, warning_date, risk_score
        FROM job_scam_reports
        ORDER BY warning_date DESC
        LIMIT 6
    """)
    rows = cursor.fetchall()
    conn.close()
    
    cards_html = ""
    for row in rows:
        slug, entity_name, warning_type, warning_date, risk_score = row
        score_color = "#ef4444" if risk_score and risk_score >= 80 else "#f59e0b"
        cards_html += f"""
        <a href="/scammer/{html_lib.escape(slug)}" class="card">
            <div class="badge" style="background-color: {score_color};">Risk: {risk_score}%</div>
            <h4>{html_lib.escape(entity_name)}</h4>
            <p><strong>Type:</strong> {html_lib.escape(warning_type)}<br><strong>Warned:</strong> {warning_date}</p>
        </a>
        """
    
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("{latest_scams}", cards_html).replace("{affiliate_boxes}", AFFILIATE_HTML)
        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(content=str(e))


@app.get("/index.css")
def serve_index_css():
    return FileResponse("index.css")

@app.get("/dev_bg.webp")
def serve_dev_bg():
    return FileResponse("dev_bg.webp")


@app.get("/scammers")
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


@app.get("/scammer/{slug}")
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
