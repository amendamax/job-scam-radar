import re
s = open('server.py', 'r', encoding='utf-8').read()

replacement = """@app.get("/scammer/{slug}")
@app.get("/{lang}/scammer/{slug}")
async def job_scam_detail(request: Request, slug: str, lang: str = "en"):
    \"\"\"
    Dossier on an individual Job Scam Report.
    \"\"\"
    if lang not in ("en", "ro", "it", "es", "fr", "de", "pt", "ru"):
        lang = "en"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(\"\"\"
        SELECT id, entity_name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction, risk_score
        FROM job_scam_reports WHERE slug = ?
    \"\"\", (slug,))
    row = cursor.fetchone()
    conn.close()
            
    if not row:
        raise HTTPException(status_code=404, detail="Job Scam Report Not Found")
        
    pid, name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction, risk_score = row
    
    real_score = risk_score * 10 if risk_score <= 10 else risk_score
    
    T = {
        "en": {
            "title": f"{name} Job Scam Alert ({warning_type}) | JobScamRadar",
            "meta_desc": f"Forensic dossier on fake recruiter/job scam '{name}' ({domain}). Read the full report and protect yourself from {warning_type}.",
            "back": "&larr; Back to Scammer Blacklist",
            "verify_face": "📷 Verify Recruiter Face (Free) ↗",
            "risk_label": f"{real_score}% CONFIRMED JOB SCAM RISK",
            "reported": "Reported",
            "investigations": "Investigations",
            "claimed_label": f"<strong>Reported Entity:</strong> {name} &bull; Domain: {domain} &bull; Jurisdiction: {jurisdiction}",
            "victim_alert": f"⚠️ <strong>Warning:</strong> The entity known as {name} has been flagged for {warning_type}.",
            "script_heading": "🎭 Scam Alert Reason / Report",
            "flags_heading": "🚩 Key Red Flags & Source:",
            "aliases_heading": f"<strong>Official Warning Source:</strong> {regulator}",
            "chatting_q": "Are You Being Recruited By This Company?",
            "chatting_desc": "Don't send any money, cryptocurrency, or pay 'training' fees. Run our instant AI facial recognition audit on your recruiter to uncover if they are using stolen photos.",
            "scan_cta": "📷 Run Free Biometric Photo Scan ➔",
            "pdf_cta": "📄 Download Official PDF Report (100% Free)",
            "toolkit_title": "🛡️ Official Investigation & Safety Toolkit",
            "toolkit_desc": "Verified tools to run background checks, delete stolen personal info, and find genuine matches.",
        }
    }
    
    t = T.get(lang, T["en"])
    
    # We will use 'reason' for the script, 'official_url' for flags
    script_html = f\"\"\"<p style='color: #cbd5e1; font-size: 15px; white-space: pre-wrap; margin-bottom: 25px;'>{reason}</p>\"\"\"
    flags_html = f'<li style="color: #f87171; margin-bottom: 6px;">🚩 <strong>Source Link:</strong> <a href="{official_url}" style="color:#38bdf8;" target="_blank">{official_url}</a></li>'
"""

pattern = re.compile(r'@app\.get\("/scammer/\{slug\}"\).*?flags_html =.*?aliases_str = .*?\n.*?T =.*?\}', re.DOTALL)
s = pattern.sub(replacement + "\n", s)
open('server.py', 'w', encoding='utf-8').write(s)
print('Done!')
