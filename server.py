import os
import re
import json
import sqlite3
import html as html_lib
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, Response, FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

HEADER_HTML = """<header>
        <div style="font-size: 24px; font-weight: 800; margin: 0;"><a href="/" style="color: #38bdf8; text-decoration: none;">💼 JobScamRadar</a></div>
        <nav>
            <a href="/">Verifier</a>
            <a href="/scammers">Scam Directory</a>
            <a href="/privacy">Privacy &amp; Legal</a>
        </nav>
    </header>"""

FOOTER_HTML = """<footer class="vasiledev-ecosystem-footer" style="background: #03060a; border-top: 1px solid rgba(255, 255, 255, 0.1); padding: 50px 20px 24px; font-family: 'Inter', system-ui, -apple-system, sans-serif; color: #94a3b8; font-size: 0.85rem; line-height: 1.6; text-align: left; margin-top: 60px;">
        <div style="max-width: 1140px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 36px; margin-bottom: 36px;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                    <span style="display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 8px; background: rgba(56, 189, 248, 0.15); color: #38bdf8; font-size: 16px;">
                        💼
                    </span>
                    <span style="font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 800; color: #ffffff; letter-spacing: -0.3px;">
                        JOBSCAM<strong style="color: #38bdf8;">RADAR</strong>
                    </span>
                </div>
                <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5; margin: 0 0 12px 0;">
                    Employment fraud defense system. Identifying fake recruitment agencies, task scams, and human trafficking operations.
                </p>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <span style="background: rgba(16, 185, 129, 0.12); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px;">✔️ VIES Verified EU</span>
                    <span style="background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px;">🛡️ 100% Free Public Utility</span>
                </div>
            </div>
            <div>
                <h4 style="font-family: 'Outfit', sans-serif; font-size: 1rem; font-weight: 700; color: #38bdf8; margin: 0 0 14px 0;">VasileDev Group Ecosystem</h4>
                <p style="margin: 0 0 8px 0; color: #ffffff; font-weight: 600; font-size: 0.85rem;">VasileDev Group</p>
                <p style="margin: 0 0 8px 0; color: #cbd5e1; font-size: 0.85rem;">VAT / P.IVA: <code style="background: rgba(255, 255, 255, 0.1); color: #38bdf8; padding: 2px 6px; border-radius: 4px; font-family: monospace;">IT04226190041</code></p>
                <p style="margin: 0 0 8px 0; color: #94a3b8; font-size: 0.85rem;">Locations: Garessio (CN), Italy &amp; Odobești, Romania</p>
                <p style="margin: 0 0 8px 0; color: #94a3b8; font-size: 0.85rem;">Direct: <a href="mailto:amendamax@vasiledev.com" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">amendamax@vasiledev.com</a></p>
                <p style="margin: 0; color: #94a3b8; font-size: 0.85rem;">WhatsApp: <strong style="color: #cbd5e1;">+39 320 948 1876</strong></p>
            </div>
            <div>
                <h4 style="font-family: 'Outfit', sans-serif; font-size: 1rem; font-weight: 700; color: #38bdf8; margin: 0 0 14px 0;">Official Network</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px 14px; font-size: 0.85rem;">
                    <a href="https://isbrokersafe.com" target="_blank" rel="noopener" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">🏛️ IsBrokerSafe.com</a>
                    <a href="https://verifydating.net" target="_blank" rel="noopener" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">🛡️ VerifyDating.net</a>
                    <a href="https://dreamcarhunt.com" target="_blank" rel="noopener" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">🏎️ DreamCarHunt.com</a>
                    <a href="https://airparkrefund.com" target="_blank" rel="noopener" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">✈️ AirParkRefund.com</a>
                    <a href="https://jobscamradar.com" style="color: #38bdf8; font-weight: 700; text-decoration: none; white-space: nowrap;">💼 JobScamRadar.com</a>
                    <a href="https://pillscamradar.com" target="_blank" rel="noopener" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">💊 PillScamRadar.com</a>
                    <a href="https://appscamradar.com" target="_blank" rel="noopener" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">📱 AppScamRadar.com</a>
                    <a href="https://calcolaincentivi.it" target="_blank" rel="noopener" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">⚡ CalcolaIncentivi.it</a>
                    <a href="https://vasiledev.com" target="_blank" rel="noopener" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">👑 VasileDev.com</a>
                </div>
            </div>
        </div>
        <div style="max-width: 1140px; margin: 0 auto; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 20px; text-align: center; font-size: 0.8rem; color: #64748b;">
            <p style="margin: 0;">&copy; 2026 JobScamRadar™ by VasileDev Group (P.IVA IT04226190041). All Rights Reserved. Intellectual Property Protected under EU Copyright Law.</p>
            <div style="text-align: center; margin-top: 14px; display: flex; justify-content: center; gap: 18px; flex-wrap: wrap;">
                <a href="/scammers" style="color: #38bdf8; text-decoration: none; font-weight: 600;">&bull; Browse Full Recruitment Scam Directory</a>
                <a href="/privacy" style="color: #94a3b8; text-decoration: none;">Privacy Policy &amp; GDPR</a>
                <a href="/sitemap.xml" style="color: #94a3b8; text-decoration: none;">XML Sitemap</a>
                <a href="/llms.txt" style="color: #94a3b8; text-decoration: none;">LLMs.txt</a>
            </div>
        </div>
    </footer>"""

AFFILIATE_HTML = """<div class="affiliate-section">
            <div class="aff-card privacy">
                <h4 style="color: #38bdf8;">🛡️ Generate a Fake Identity</h4>
                <p>Don't give fake recruiters your real phone number or email. Use Surfshark Alternative ID to generate working proxy details and protect yourself from spam and identity theft.</p>
                <a href="https://www.tkqlhce.com/click-101863908-15740542" target="_blank" rel="sponsored noopener noreferrer">Protect Your Identity (Alternative ID)</a>
            </div>
            <div class="aff-card jobs">
                <h4>🤝 Meet Genuine, Verified Employers</h4>
                <p>Tired of WhatsApp recruiters and fake data entry jobs? Join platforms where every job is hand-screened.</p>
                <span class="btn-disabled" aria-disabled="true">🔒 Verified Job Board — Coming Soon</span>
            </div>
            <p class="aff-disclosure">Disclosure: some links above are affiliate links. If you sign up through them we may earn a commission, at no extra cost to you.</p>
        </div>"""


def wrap_html(title: str, content: str, description: str = "", canonical_path: str = "/"):
    if not description:
        description = "Track, verify, and avoid fake job offers, WhatsApp/Telegram task scams, imposter recruiters, and employment fraud globally with JobScamRadar."
    safe_desc = html_lib.escape(description[:160])
    safe_title = html_lib.escape(title)
    canonical_url = f"https://jobscamradar.com{canonical_path}"

    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <meta name="description" content="{safe_desc}">
    <link rel="canonical" href="{canonical_url}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="JobScamRadar">
    <meta property="og:title" content="{safe_title}">
    <meta property="og:description" content="{safe_desc}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content="https://jobscamradar.com/og_banner.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{safe_title}">
    <meta name="twitter:description" content="{safe_desc}">
    <meta name="twitter:image" content="https://jobscamradar.com/og_banner.jpg">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-950R9NXTL9"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-950R9NXTL9');
    </script>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0; padding: 0;
            background: linear-gradient(to bottom, rgba(15,23,42,0.85), rgba(2,6,23,0.96)), url('/dev_bg.webp') center top / cover fixed;
            color: #f8fafc;
        }}
        header {{ background-color: rgba(15,23,42,0.92); padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1e293b; backdrop-filter: blur(8px); }}
        header h1 {{ margin: 0; font-size: 24px; }}
        header h1 a {{ color: #38bdf8; text-decoration: none; }}
        header nav {{ display: flex; gap: 18px; align-items: center; font-size: 14px; font-weight: 600; }}
        header nav a {{ color: #cbd5e1; text-decoration: none; transition: color 0.2s; }}
        header nav a:hover {{ color: #38bdf8; }}
        .container {{ max-width: 1040px; margin: 0 auto; padding: 40px 20px; min-height: 60vh; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .card {{ background-color: rgba(15,23,42,0.9); border: 1px solid #1e293b; border-radius: 10px; padding: 20px; transition: transform 0.2s, border-color 0.2s; text-decoration: none; color: inherit; display: block; }}
        .card:hover {{ transform: translateY(-3px); border-color: #38bdf8; }}
        .card h4 {{ margin: 0 0 10px 0; font-size: 17px; color: #e2e8f0; line-height: 1.35; }}
        .card p {{ margin: 0; font-size: 13.5px; color: #94a3b8; line-height: 1.45; }}
        .badge {{ display: inline-block; font-size: 12px; font-weight: bold; padding: 3px 8px; border-radius: 4px; margin-bottom: 10px; color: white; }}

        .dossier {{ background: rgba(11,21,40,0.92); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 30px; }}
        .dossier .header {{ border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 20px; }}
        .dossier h1 {{ margin: 0 0 10px 0; font-size: 28px; line-height: 1.25; }}
        .details-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }}
        .detail-item {{ background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06); }}
        .detail-item strong {{ color: #94a3b8; display: block; font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 5px; }}
        .reason {{ margin-top: 26px; padding: 20px; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; border-radius: 0 8px 8px 0; line-height: 1.6; }}
        .checklist-box {{ margin-top: 24px; padding: 20px; background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 10px; }}
        .checklist-box h3 {{ margin: 0 0 10px 0; font-size: 17px; color: #38bdf8; }}
        .checklist-box ul {{ margin: 0; padding-left: 20px; color: #cbd5e1; font-size: 14px; line-height: 1.6; }}
        .affiliate-section {{ margin-top: 56px; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .aff-card {{ padding: 24px 20px; border-radius: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }}
        .aff-card.privacy {{ background-color: #022c22; }}
        .aff-card.jobs {{ background-color: #451a03; }}
        .aff-card h4 {{ margin: 0 0 10px 0; font-size: 20px; }}
        .aff-card p {{ font-size: 14px; color: #cbd5e1; margin-bottom: 16px; line-height: 1.5; }}
        .aff-card a {{ display: inline-block; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; color: white; background: rgba(0,0,0,0.35); border: 1px solid rgba(56,189,248,0.4); }}
        .btn-disabled {{ display: inline-block; padding: 10px 20px; border-radius: 6px; font-weight: bold; color: #94a3b8; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); cursor: not-allowed; user-select: none; pointer-events: none; opacity: 0.75; }}
        .aff-disclosure {{ grid-column: 1 / -1; font-size: 12px; color: #94a3b8; text-align: center; margin: 4px 0 0 0; }}
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
</html>"""
    return template


app = FastAPI(title="JobScamRadar Core API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SmartCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        path = request.url.path.lower()
        if path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        elif any(path.endswith(ext) for ext in (".webp", ".jpg", ".png", ".svg", ".ico", ".css")):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        elif path in ("/robots.txt", "/llms.txt", "/.well-known/llms.txt") or path.endswith(".xml"):
            response.headers["Cache-Control"] = "public, max-age=3600, s-maxage=86400"
        elif request.method in ("GET", "HEAD") and response.status_code == 200:
            response.headers["Cache-Control"] = "public, max-age=300, s-maxage=3600, stale-while-revalidate=86400"
        return response


app.add_middleware(SmartCacheMiddleware)

DB_PATH = "/var/data/database.db" if os.path.exists("/var/data/database.db") else "database.db"


def normalize_risk_score(risk_score):
    try:
        score = int(risk_score)
    except Exception:
        score = 88
    if score <= 10:
        return min(99, score * 10 + 8)
    return score


BAD_OFFTOPIC_IDS = (
    809, 810, 811, 812, 813, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826,
    828, 829, 831, 832, 833, 834, 835, 836, 837, 841, 842, 843, 844, 845, 847
)

CURATED_ADVISORY_OVERRIDES = {
    1: ("Imposter Recruiters Taking Over the Job Market", "Recruitment Fraud", "Regulatory and media advisory warning of imposter recruiters impersonating legitimate employers across online job boards to harvest candidate data and upfront fees.", 88),
    2: ("Sophisticated Job Scams: Recruitment Fraud Advisory", "Recruitment Fraud", "Consumer protection alert detailing sophisticated remote recruitment fraud tactics, fake interview pipelines, and advance-fee employment traps.", 88),
    3: ("Fake $600/Day Work-From-Home Text Message Scam", "SMS Task Scam", "Unsolicited SMS recruitment scam offering $600 per day for remote work-from-home tasks to lure job seekers into advance-fee payment schemes.", 92),
    4: ("BBB Warning: Reshipping & Parcel Mule Job Scam", "Reshipping Scam", "Better Business Bureau (BBB) Canton region alert warning job seekers of fraudulent reshipping and parcel forwarding work-from-home job offers.", 90),
    5: ("SAFE Net Regional Employment & Financial Fraud Alert", "Recruitment Fraud", "Regional task force advisory educating job seekers and residents on identifying unsolicited recruitment fraud and identity theft schemes.", 88),
    6: ("Fake LinkedIn Recruiter Brand Impersonation Scam", "LinkedIn Impersonation", "HR security warning regarding fraudulent LinkedIn recruiter profiles hijacking established corporate brands to deceive job candidates.", 91),
    7: ("Executive Wire Fraud & Illicit Gold Transfer Scheme", "Wire Fraud Alert", "Federal wire fraud enforcement alert involving high-value advance-fee deception and illicit financial transfers.", 88),
    8: ("Fake South African Electoral Commission (IEC) Job Adverts", "Government Job Scam", "Official verification alert warning job seekers against fraudulent South African Electoral Commission (IEC) recruitment advertisements circulating online.", 90),
    9: ("Hong Kong HK$2.16M Student Recruitment Scam Ring", "Recruitment Fraud Ring", "Law enforcement action dismantling an organized HK$2.16 million recruitment fraud and money mule syndicate targeting students.", 92),
    10: ("Budgam Fake Government Job Recruitment Scam", "Recruitment Fraud", "Police investigation and arrests targeting an organized fraudulent job placement syndicate collecting illicit fees from applicants.", 89),
    11: ("'Add Me on WhatsApp' Imposter Recruiter Call Scam", "WhatsApp Task Scam", "Telecommunications and regulatory investigation into automated 'Add me on WhatsApp' recruitment calls leading to task scams.", 93),
    12: ("Dubai Fake Job Offer & Visa Fee Recruitment Scam", "Visa & Job Fraud", "Employment fraud advisory warning international job seekers how to spot fake Dubai job offer letters and illegal visa processing fees.", 90),
    13: ("Fake FIRS Recruitment Advert & Government Job Portal Scam", "Government Job Scam", "Official agency warning confirming that viral Federal Inland Revenue Service (FIRS) recruitment advertisements are fraudulent.", 91),
    14: ("KPSC Public Service Recruitment Examination Fraud", "Recruitment Fraud", "Criminal Investigation Department (CID) probe into public service recruitment irregularities and fraudulent job placement promises.", 88),
    15: ("Hong Kong Fake Modeling Job & Money Laundering Scam", "Advance-Fee Job Scam", "Law enforcement crackdown on a fraudulent modeling agency recruitment scheme used for advance-fee fraud and money laundering.", 92),
    16: ("Fake 'Juror Focus Group' & Mock Juror Phishing Listing (Indeed)", "Identity Phishing Scam", "Fraudulent remote 'Mock Juror' job listing circulating on job boards that redirects applicants to external forms harvesting sensitive personal and financial data.", 98),
    17: ("Discord & Group-Chat Remote Task Scam Operation", "Task Scam / Fake Job", "Fraudulent remote team operation using Discord servers and WhatsApp group chats to pressure new hires into deceptive telemarketing and task schemes.", 98),
    18: ("Fake US Financial Services Call Center Cold-Calling Scam", "Call Center Job Scam", "Fraudulent offshore call center recruitment operation training applicants to impersonate US credit bureaus (Experian/Equifax) and pitch predatory loan scams.", 98),
    19: ("recruitmentoutreachgroup.com (Fake LEGO Digital Marketing Recruiter)", "Imposter Recruiter Scam", "Imposter recruitment domain (recruitmentoutreachgroup.com) sending unsolicited emails impersonating LEGO hiring managers for a fake Digital Marketing Manager role.", 98),
    20: ("City of Ottumwa Fake Social Media Municipal Job Ads", "Imposter Job Listing", "Municipal government warning alerting the public to fraudulent City of Ottumwa job advertisements posted on social media platforms.", 89),
    21: ("Fake ZipRecruiter Remote Job Scam ($80,000 Loss Report)", "Imposter Recruiter Scam", "Law enforcement report detailing an $80,000 financial loss resulting from a fraudulent employer impersonation scam initiated on ZipRecruiter.", 94),
    22: ("Financial Sector Employment Scam Surge (21-Country Report)", "Recruitment Fraud", "Cybersecurity intelligence report documenting a 300% surge in employment scam victims targeting financial firms across 21 countries.", 90),
    23: ("Top Employment & Financial Scams Advisory (BECU)", "Employment Fraud Alert", "Financial institution consumer alert warning members against fake remote job offers, fraudulent check deposits, and task-based payment traps.", 88),
    24: ("Online Recruitment & Digital Identity Fraud Advisory", "Online Job Fraud", "Consumer protection report examining widespread online recruitment deception, fake employer portals, and digital phishing schemes.", 88),
    25: ("Bengaluru Work-From-Home Task Scam (Rs 4.46L Loss)", "Work-From-Home Scam", "Cybercrime report detailing a fraudulent work-from-home task scheme that defrauded a software engineer of Rs 4.46 lakh via prepaid task deposits.", 92),
    26: ("Hyderabad Fake Telegram Part-Time Job Scam (Rs 3L Loss)", "Telegram Task Scam", "Cybercrime enforcement report regarding a fraudulent Telegram part-time rating and task job scam resulting in a Rs 3 lakh loss.", 93),
    27: ("Pan-India Fake Banking Recruitment Syndicate (CBI Enforcement)", "Banking Job Scam", "Central Bureau of Investigation (CBI) enforcement action dismantling a pan-India fraudulent banking recruitment network issuing forged appointment letters.", 92),
    28: ("Dubai Police Dh11.9M Recruitment & Cyber Fraud Crackdown", "Recruitment Fraud Ring", "Law enforcement operation arresting operators of a major Dh11.9 million fraud syndicate utilizing deceptive online recruitment and investment lures.", 91),
    29: ("Zamboanga Cyber Scam Hub & Forced Labor Recruitment Raid", "Trafficking / Scam Hub", "Law enforcement raid on an illicit cyber scam compound recruiting workers under false employment pretenses for online fraud operations.", 94),
    30: ("IIT Madras Study: Digital Recruitment & Cyber Fraud Vulnerability", "Cyber Fraud Research", "Academic cybersecurity study analyzing how white-collar professionals and job seekers are targeted by social engineering and fake employment offers.", 88),
    31: ("Hyderabad Work-From-Home & Task Fraud Ring (\u20b994.9L Loss)", "Work-From-Home Scam", "Cybercrime police investigation into organized online task and part-time employment fraudsters who defrauded victims of \u20b994.9 lakh.", 94),
    32: ("Dubai-Linked Cross-Border Recruitment & Cyber Fraud Syndicate", "Recruitment Fraud Ring", "Cybercrime cell arrest of a key operative linked to Dubai-based syndicates recruiting mule accounts and executing work-from-home scams.", 91),
    33: ("Automated 'Add Me on WhatsApp' Voice Call Job Scam Wave", "WhatsApp Task Scam", "Consumer warning explaining the surge in automated robocalls instructing recipients to add a WhatsApp number for fake remote commission jobs.", 93),
    34: ("Unverified Job Board & Spoofed Career Portal Phishing Risk", "Job Board Spoofing", "Employment security advisory highlighting the risks of spoofed job search portals and unverified third-party recruitment aggregators.", 88),
    35: ("Seasonal & Holiday Hiring Rush Recruitment Scam Alert", "Seasonal Job Fraud", "Workforce security advisory warning job seekers and HR departments of elevated recruitment fraud during seasonal holiday hiring surges.", 89),
    36: ("New York Remote Work Check & Equipment Fee Job Scam", "Work-From-Home Scam", "Consumer investigative report warning remote job applicants about fake home-office equipment check scams targeting New York residents.", 91),
    37: ("IRCC Warning: Fake Immigration & Work Permit Officials Using AI", "Work Permit Scam", "Immigration, Refugees and Citizenship Canada (IRCC) official warning regarding scammers using AI-generated content and fake officials to sell fraudulent job offers and visas.", 93),
    38: ("North Korean IT Worker Identity Fraud Targeting Corporate Hiring", "Remote IT Hiring Fraud", "Cybersecurity threat intelligence alert warning employers and recruiters of state-sponsored IT operatives using stolen identities to secure remote developer jobs.", 92),
    39: ("Advance-Fee Recruiter Scam: Upfront Training & Certification Trap", "Advance-Fee Job Scam", "Recruitment fraud case study exposing fake headhunters who demand upfront payment for mandatory resumes, background checks, or certifications before hiring.", 92),
    40: ("Student & Campus Back-to-School Part-Time Job Scam Alert", "Student Job Scam", "Consumer protection alert warning college and high school students against fraudulent part-time assistant and mystery shopper job offers.", 88),
    41: ("Social Engineering Tactics in Modern Employment Fraud", "Recruitment Fraud", "Behavioral cybersecurity analysis detailing how recruitment scammers use urgency, authority, and high-pay promises to manipulate job applicants.", 88),
    42: ("Newly Registered Fake Interview App & Malicious Career Site Scam", "Malicious Interview App", "Security alert regarding fake recruiters directing US job applicants to newly registered domains (created days prior) to download malicious interview software.", 94),
    43: ("Task-to-Crypto 'Pig Butchering' Employment & Investment Scam", "Task / Crypto Scam", "AARP fraud alert detailing how remote app-optimization job scams transition into high-loss cryptocurrency 'pig butchering' extortion schemes.", 95),
    44: ("Fraudulent Side-Hustle & Gig Platform Impersonation Traps", "Side-Hustle Scam", "Consumer advisory distinguishing legitimate remote side gigs from fraudulent task platforms that require upfront crypto or wire deposits.", 88),
    45: ("Publishing Industry Impersonation & Manuscript Phishing Scam", "Industry Impersonation", "Investigation into long-running identity impersonation and phishing tactics targeting publishing professionals, freelancers, and editors.", 89),
    46: ("Fake AI / ChatGPT Career Tool Malware Distribution Scam", "Malware Job Trap", "Cybersecurity alert warning remote workers and job seekers of trojanized AI productivity tools distributed via fake job assessments.", 93),
    47: ("Financial & Employment Fraud Prevention Advisory", "Recruitment Fraud", "Expert fraud prevention guidelines for identifying fake employer communications, advance-fee requests, and bank account harvesting.", 88),
    48: ("Cryptocurrency Payroll & Task Deposit Job Scams", "Crypto Task Scam", "Educational security guide explaining how fraudulent employers demand USDT/cryptocurrency deposits under the guise of payroll activation or task unlocking.", 91),
    49: ("Verified Corporate Social Media Account Hijacking Scams", "Brand Hijacking Scam", "Cybersecurity report on threat actors hijacking verified corporate X/social media accounts to broadcast fraudulent hiring and crypto links.", 90),
    50: ("Public Sector Patronage & Unlawful Job Fee Fraud Advisory", "Public Sector Fraud", "Regulatory overview of unlawful fee-for-office and public employment fraud schemes.", 88),
    51: ("Fake Corporate IT & Tech-Support Impersonation Scam ($22,500 Loss)", "Impersonation Fraud", "Consumer fraud report documenting a $22,500 loss to scammers impersonating Microsoft technical and onboarding support personnel.", 92),
    52: ("Freelance Marketplace Escrow & Upfront Security Fee Scams", "Freelance Job Scam", "Security advisory for remote freelancers warning against off-platform communication, fake escrow invoices, and refundable security deposit scams.", 88),
    53: ("Fake Product Review & E-Commerce Rating Task Scams", "Review Task Scam", "Investigation into fraudulent online review generation schemes where remote workers are recruited to boost product ratings before being defrauded.", 90),
    54: ("Zambia Cybercrime Syndicate: Cross-Border Call Center Arrests", "Trafficking / Scam Hub", "Law enforcement operation in Zambia arresting foreign nationals recruited into operating an illicit international cybercrime and scam call center.", 93),
    55: ("Foreign Affairs Alert: Cybercrime Call Center Trafficking Raid", "Trafficking / Scam Hub", "Official Foreign Affairs Ministry statement following the arrest of foreign nationals in a cross-border cybercrime compound raid.", 93),
    56: ("Fake $18\u2013$25/Hour Remote Data Entry Job Scams Targeting West Africa", "Data Entry Job Scam", "Regional employment fraud warning exposing fake $18\u2013$25/hour remote data entry listings that charge applicants for training materials or software.", 92),
    57: ("Government Job Warning: Overseas Cyber Scam Compound Recruitment", "Trafficking / Scam Hub", "Official government advisory warning job seekers against fraudulent overseas IT and customer service job offers following cybercrime raids in Zambia.", 94),
    58: ("Work-From-Home Job Scams Targeting Remote Applicants", "Work-From-Home Scam", "Consumer safety guide highlighting how to verify legitimate remote work opportunities and avoid advance-fee home assembly and typing scams.", 88),
    59: ("Human Trafficking & Forced Cyber-Scam Compound Recruitment Alert", "Trafficking / Scam Hub", "Diplomatic and law enforcement confirmation that victims were lured by fake overseas job advertisements into a cybercrime operation.", 95),
    60: ("AI-Generated Recruiter & Deepfake Job Interview Scam", "AI Recruitment Scam", "Security analysis of an AI-assisted recruitment scam utilizing realistic corporate emails, cloned job descriptions, and automated interview lures.", 94),
    61: ("UK Regulator Warning: 3,600+ Complaints Over 'Add Me on WhatsApp' Job Calls", "WhatsApp Task Scam", "Regulatory enforcement alert after more than 3,600 consumers reported automated scam calls directing victims to WhatsApp recruitment bots.", 94),
    62: ("Visakhapatnam Work-From-Home Task Cyberfraud (\u20b91+ Crore Loss)", "Work-From-Home Scam", "Police cybercrime report detailing how 20 residents lost over \u20b91 crore to fraudulent part-time work-from-home task and rating schemes.", 95),
    63: ("'Ghost' Job Interviews Harvesting Candidate Biometric & AI Training Data", "Data Harvesting Scam", "Employment privacy warning regarding deceptive automated video interviews ('ghost jobs') used to harvest applicant voice, video, and personal data.", 90),
    64: ("ICO Data Watchdog Investigation: Surge in WhatsApp Recruiter Scam Calls", "WhatsApp Task Scam", "Information Commissioner's Office (ICO) investigation into the massive wave of unsolicited automated recruitment scam calls across the UK.", 93),
    65: ("High-Risk Illicit Gig Recruitment & Money Mule Lures", "Illicit Gig Scam", "Advisory on predatory gig recruitment schemes that lure job seekers into high-risk illicit tasks and financial mule operations.", 89),
    66: ("Social Media Recruitment of Youths for Part-Time Money Mule Crime", "Money Mule Recruitment", "Law enforcement warning regarding organized crime syndicates using Instagram and Telegram part-time job ads to recruit young people as money mules.", 94),
    761: ("FTC Alert: Deceptive Gig Work & Misleading Pay Promises", "Official Consumer Alert", None, 94),
    767: ("FTC Alert: Unfair & Deceptive Gig Economy Earnings Claims", "Official Consumer Alert", None, 94),
    784: ("FTC Alert: Job Scams Targeting Military Spouses & Families", "Official Consumer Alert", None, 94),
    786: ("FTC Alert: Fake 'You Got the Job!' Overpayment Check Scam", "Official Consumer Alert", None, 94),
    787: ("FTC Alert: Phony Job Postings & Employment Identity Theft", "Official Consumer Alert", None, 94),
    790: ("FTC Alert: Peer-to-Peer Side Gig & Vehicle Rental Scam Risks", "Official Consumer Alert", None, 94),
    814: ("linkedrental.com (Fake Remote Interview & Identity Phishing Portal)", "Imposter Recruiter Scam", "Fraudulent recruitment domain (linkedrental.com) sending unsolicited remote job interview invitations to harvest applicant identity documents and banking credentials.", 98),
    815: ("UK Employment Alert: Fake SMS & WhatsApp Job Offers Targeting Gen Z", "SMS / WhatsApp Job Scam", "Consumer protection warning highlighting a major surge in fraudulent SMS and WhatsApp job offers targeting young job seekers with fake remote commission roles.", 92),
    816: ("Virgin Media O2 Scam Index: Surge in Fake Recruiter Text Messages", "SMS Recruiter Scam", "Telecom fraud intelligence report confirming fake recruitment text messages impersonating major HR agencies have entered the top 10 most reported consumer scams.", 93),
    827: ("Benaulim Online Task & Prepaid Rating Job Scam (\u20b91.68L Loss)", "Online Task Scam", "Cybercrime enforcement report detailing an online task and product-rating job scheme that defrauded a remote applicant of \u20b91.68 lakh via locked commission accounts.", 94),
    830: ("2026 Employment & Task Fraud Report: 67% Victim Loss Rate", "Employment Fraud Report", "National consumer fraud survey revealing that fake remote job offers and prepaid Telegram task scams account for a majority of unrecovered digital financial losses.", 90),
    838: ("Crypto Task-Scam Syndicate Reserve Audit ($4.8M Bitcoin Seizure/Loss)", "Crypto Task Scam Ring", "Blockchain intelligence report exposing the illicit cryptocurrency treasury operations behind international 'task optimization' fake job syndicates.", 94),
    839: ("Work Calendar Invite Phishing & Fake Interview Link Scam", "Interview Phishing Scam", "Cybersecurity advisory warning remote professionals and job applicants of malicious Google/Outlook work calendar invites disguising credential-harvesting phishing links as job interviews.", 93),
    840: ("US Law Enforcement Raid on 'Laptop Farms' for Fake Remote IT Workers ($3M Fraud)", "Remote IT Hiring Fraud", "Federal enforcement action dismantling illicit 'laptop farms' used by overseas operatives to pose as US-based remote software engineers and funnel $3 million in corporate salaries.", 95),
    846: ("Fake UNHCR (UN Refugee Agency) Job Recruitment Poster & Fee Hoax", "UN / NGO Job Scam", "Official verification alert confirming that viral recruitment posters advertising positions at UNHCR (UN Refugee Agency) are fraudulent advance-fee traps.", 94),
}


def sync_bundled_to_persistent(bundled_db: str, persistent_db: str):
    """Ensure any curated rows in the bundled repo database.db are present in /var/data/database.db."""
    if not os.path.exists(bundled_db) or not os.path.exists(persistent_db):
        return
    if os.path.abspath(bundled_db) == os.path.abspath(persistent_db):
        return
    try:
        b_conn = sqlite3.connect(bundled_db)
        p_conn = sqlite3.connect(persistent_db)
        b_cur = b_conn.cursor()
        p_cur = p_conn.cursor()

        b_rows = b_cur.execute(
            "SELECT id, slug, entity_name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction, risk_score, blacklisted_urls, clone_of, details_json, created_at FROM job_scam_reports"
        ).fetchall()
        for r in b_rows:
            rid, slug = r[0], r[1]
            if rid in BAD_OFFTOPIC_IDS:
                continue
            exists = p_cur.execute("SELECT 1 FROM job_scam_reports WHERE slug = ? OR id = ?", (slug, rid)).fetchone()
            if not exists:
                p_cur.execute(
                    """INSERT INTO job_scam_reports
                    (id, slug, entity_name, domain, regulator, warning_type, warning_date, official_url, reason, jurisdiction, risk_score, blacklisted_urls, clone_of, details_json, created_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    r
                )
        p_conn.commit()
        b_conn.close()
        p_conn.close()
    except Exception as e:
        print(f"[JobScamRadar DB Sync Error]: {e}")


def migrate_and_clean_db(db_file: str):
    if not os.path.exists(db_file):
        return
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(f"DELETE FROM job_scam_reports WHERE id IN ({','.join(map(str, BAD_OFFTOPIC_IDS))})")
        cur.execute("SELECT id, entity_name, domain, warning_type, reason, risk_score FROM job_scam_reports")
        rows = cur.fetchall()
        for row_id, name, domain, wtype, reason, score in rows:
            new_name = name or ""
            new_wtype = wtype or "Recruitment Fraud"
            new_reason = reason or ""
            new_domain = domain or ""
            if score is None or int(score) <= 10:
                s = int(score) if score is not None else 8
                if s == 8:
                    new_score = 88
                elif s == 9:
                    new_score = 94
                elif s == 10:
                    new_score = 98
                else:
                    new_score = min(99, s * 10 + 8)
            else:
                new_score = int(score)

            if row_id in CURATED_ADVISORY_OVERRIDES:
                ov_name, ov_type, ov_reason, ov_score = CURATED_ADVISORY_OVERRIDES[row_id]
                new_name = ov_name
                new_wtype = ov_type
                if ov_reason:
                    new_reason = ov_reason
                new_score = ov_score
                if row_id == 19:
                    new_domain = "recruitmentoutreachgroup.com"
                elif row_id == 814:
                    new_domain = "linkedrental.com"
            else:
                new_name = re.sub(r'\s+-\s+[^-]+$', '', new_name)
                new_name = re.sub(r'\.{2,}$', '', new_name).strip()

            if new_reason and not new_reason.endswith(('.', '!', '?')):
                last_dot = max(new_reason.rfind('. '), new_reason.rfind('? '), new_reason.rfind('! '))
                if last_dot > 40:
                    new_reason = new_reason[:last_dot + 1] + " Read the official FTC consumer alert for complete guidance on avoiding this employment scam."
                else:
                    new_reason = new_reason.rstrip(' ,;:-—') + ". Official consumer protection alert regarding deceptive employment and recruitment practices."

            if (new_name, new_domain, new_wtype, new_reason, new_score) != (name, domain, wtype, reason, score):
                cur.execute(
                    "UPDATE job_scam_reports SET entity_name = ?, domain = ?, warning_type = ?, reason = ?, risk_score = ? WHERE id = ?",
                    (new_name, new_domain, new_wtype, new_reason, new_score, row_id)
                )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[JobScamRadar DB Migration Error on {db_file}]: {e}")


sync_bundled_to_persistent("database.db", "/var/data/database.db")
for _candidate_db in ("database.db", "/var/data/database.db"):
    migrate_and_clean_db(_candidate_db)


def get_db_connection():
    return sqlite3.connect(DB_PATH)


@app.get("/")
def serve_index():
    conn = get_db_connection()
    cursor = conn.cursor()
    total_cases = cursor.execute("SELECT count(*) FROM job_scam_reports").fetchone()[0]
    cursor.execute("""
        SELECT slug, entity_name, warning_type, warning_date, risk_score
        FROM job_scam_reports
        ORDER BY warning_date DESC, id DESC
        LIMIT 6
    """)
    rows = cursor.fetchall()
    conn.close()

    cards_html = ""
    for row in rows:
        slug, entity_name, warning_type, warning_date, risk_score = row
        risk_score = normalize_risk_score(risk_score)
        score_color = "#ef4444" if risk_score >= 80 else "#f59e0b"
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
        html = (
            html.replace("{latest_scams}", cards_html)
            .replace("{affiliate_boxes}", AFFILIATE_HTML)
            .replace("{total_cases}", str(total_cases))
        )
        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(content=str(e))


@app.get("/api/verify-job")
def api_verify_job(q: str = ""):
    query = (q or "").strip()
    if not query:
        return JSONResponse({"verdict": "Enter a query", "risk_score": 0, "summary": "Please enter a company name, recruiter email/domain, or job offer text.", "flags": [], "matches": []})

    ql = query.lower()
    flags = []
    score = 18

    # 1. Database matches
    conn = get_db_connection()
    cursor = conn.cursor()
    words = [w for w in re.findall(r"[a-z0-9.-]{3,}", ql) if w not in ("the", "and", "for", "job", "scam", "com", "www", "http", "https")]
    matches = []
    seen_slugs = set()

    cursor.execute(
        "SELECT slug, entity_name, domain, warning_type, risk_score FROM job_scam_reports WHERE lower(entity_name) LIKE ? OR lower(domain) LIKE ? OR lower(reason) LIKE ? ORDER BY warning_date DESC LIMIT 5",
        (f"%{ql[:50]}%", f"%{ql[:50]}%", f"%{ql[:50]}%")
    )
    for r in cursor.fetchall():
        seen_slugs.add(r[0])
        matches.append({
            "slug": r[0],
            "entity_name": r[1],
            "domain": r[2],
            "warning_type": r[3],
            "risk_score": normalize_risk_score(r[4])
        })

    if not matches and words:
        for w in words[:3]:
            if len(w) < 4:
                continue
            cursor.execute(
                "SELECT slug, entity_name, domain, warning_type, risk_score FROM job_scam_reports WHERE lower(entity_name) LIKE ? OR lower(domain) LIKE ? OR lower(reason) LIKE ? ORDER BY warning_date DESC LIMIT 4",
                (f"%{w}%", f"%{w}%", f"%{w}%")
            )
            for r in cursor.fetchall():
                if r[0] not in seen_slugs:
                    seen_slugs.add(r[0])
                    matches.append({
                        "slug": r[0],
                        "entity_name": r[1],
                        "domain": r[2],
                        "warning_type": r[3],
                        "risk_score": normalize_risk_score(r[4])
                    })
    conn.close()

    # 2. Forensic Heuristic Checks
    known_bad_domains = ("recruitmentoutreachgroup.com", "linkedrental.com")
    if any(d in ql for d in known_bad_domains):
        score = max(score, 98)
        flags.append("🚨 <strong>Blacklisted Imposter Recruiter Domain:</strong> This domain is confirmed in our database for impersonating employers and harvesting applicant credentials.")

    if any(w in ql for w in ("@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com", "@proton.me", "@icloud.com")):
        score += 45
        flags.append("🚩 <strong>Free Webmail Recruiter Address:</strong> Legitimate corporate HR departments do not recruit or send offer letters from personal <code>@gmail.com</code>, <code>@outlook.com</code>, or <code>@yahoo.com</code> accounts.")

    if any(w in ql for w in ("whatsapp", "telegram", "t.me/", "wa.me/", "add me on", "text me on")):
        score += 48
        flags.append("🚩 <strong>Unsolicited WhatsApp / Telegram Outreach:</strong> Cold calls, robocalls, or SMS messages directing you to WhatsApp or Telegram for a job interview are the #1 vector for remote task scams.")

    if any(w in ql for w in ("$600", "$500", "$800", "per day", "/day", "usdt", "crypto", "task", "optimization", "product rating", "workbench", "30 tasks", "40 tasks", "recharge")):
        score += 50
        flags.append("🚩 <strong>Prepaid Task / App-Optimization Scam Pattern:</strong> Promises of high daily pay ($200–$800/day) for simple clicking, app rating, or 'data optimization' tasks that require USDT/crypto top-ups are Pig-Butchering Task Scams.")

    if any(w in ql for w in ("equipment check", "mobile deposit", "buy laptop", "training fee", "security deposit", "background check fee", "upfront fee", "visa fee")):
        score += 52
        flags.append("🚩 <strong>Advance-Fee / Fake Equipment Check Trap:</strong> Real employers never ask you to pay for training/certification upfront or deposit a check to buy home-office equipment from a specific vendor.")

    if any(w in ql for w in ("reshipping", "parcel", "package forwarding", "quality control inspector", "money mule")):
        score += 48
        flags.append("🚩 <strong>Reshipping / Money Mule Operation:</strong> Work-from-home offers asking you to receive and forward packages or transfer funds through your personal bank account are criminal mule schemes.")

    if matches:
        max_db_score = max(m["risk_score"] for m in matches)
        score = max(score, max_db_score)
        flags.append(f"⚠️ <strong>Database Alert Match:</strong> Found {len(matches)} matching employment fraud report(s) in JobScamRadar.")

    score = min(99, score)
    if score >= 80:
        verdict = "🚨 HIGH RISK — Confirmed / Highly Probable Employment Scam"
        summary = "Multiple critical employment fraud indicators or confirmed database reports were detected. Do NOT send money, cryptocurrency, or identity documents (SSN/Passport/IBAN)."
    elif score >= 45:
        verdict = "⚠️ SUSPICIOUS — Proceed With Extreme Caution"
        summary = "Warning signs associated with imposter recruiters or unsolicited job outreach were detected. Verify the job opening directly on the company's official career portal."
    else:
        verdict = "ℹ️ NO DIRECT BLACKLIST MATCH FOUND — Verify Independently"
        summary = "No exact blacklist match was found for this query, but new imposter domains are registered daily. Always confirm the recruiter's email domain matches the company's official website and never pay upfront fees."

    return JSONResponse({
        "query": query,
        "verdict": verdict,
        "risk_score": score,
        "summary": summary,
        "flags": flags,
        "matches": matches[:5]
    })


@app.get("/index.css")
def serve_index_css():
    return FileResponse("index.css")


@app.get("/dev_bg.webp")
def serve_dev_bg():
    return FileResponse("dev_bg.webp")


@app.get("/favicon.svg")
@app.get("/favicon.ico")
def serve_favicon():
    if os.path.exists("favicon.svg"):
        return FileResponse("favicon.svg", media_type="image/svg+xml")
    raise HTTPException(status_code=404)


@app.get("/og_banner.jpg")
def serve_og_banner():
    if os.path.exists("og_banner.jpg"):
        return FileResponse("og_banner.jpg", media_type="image/jpeg")
    raise HTTPException(status_code=404)


@app.get("/directory/jobs/{page}")
def redirect_legacy_directory(page: str):
    return RedirectResponse(url="/scammers", status_code=301)


@app.get("/scammers")
def job_scams_list(q: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT slug, entity_name, domain, warning_type, warning_date, risk_score
        FROM job_scam_reports
        ORDER BY warning_date DESC, id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    items_html = ""
    for row in rows:
        slug, entity_name, domain, warning_type, warning_date, risk_score = row
        risk_score = normalize_risk_score(risk_score)
        score_color = "#ef4444" if risk_score >= 80 else "#f59e0b"
        search_blob = html_lib.escape(f"{entity_name} {domain} {warning_type} {warning_date}".lower())
        items_html += f"""
        <a href="/scammer/{html_lib.escape(slug)}" class="card dir-card" data-search="{search_blob}">
            <div class="badge" style="background-color: {score_color};">Risk: {risk_score}%</div>
            <h4>{html_lib.escape(entity_name)}</h4>
            <p><strong>Domain / Source:</strong> {html_lib.escape(domain)}<br>
            <strong>Type:</strong> {html_lib.escape(warning_type)}<br>
            <strong>Warned:</strong> {warning_date}</p>
        </a>
        """

    initial_q = html_lib.escape(q or "")
    content = f"""
        <div style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:16px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:16px;margin-bottom:24px;">
            <div>
                <h1 style="margin:0 0 6px 0;">Job Scam Directory (<span id="visible-count">{len(rows)}</span> Cases)</h1>
                <p style="margin:0;color:#94a3b8;font-size:14px;">Verified recruitment fraud alerts, imposter HR domains, WhatsApp/Telegram task scams, and FTC employment warnings.</p>
            </div>
            <div style="min-width:280px;flex:1;max-width:420px;">
                <input type="search" id="dir-search" value="{initial_q}" oninput="filterDirectory()" placeholder="🔍 Filter by company, domain, WhatsApp, FTC, task scam..." style="width:100%;box-sizing:border-box;background:rgba(2,6,23,0.9);border:1px solid #334155;color:#f8fafc;padding:11px 14px;border-radius:8px;font-size:14px;outline:none;">
            </div>
        </div>
        <div class="grid" id="dir-grid">
            {items_html}
        </div>
        <script>
        function filterDirectory() {{
            const q = (document.getElementById('dir-search').value || '').toLowerCase().trim();
            const cards = document.querySelectorAll('.dir-card');
            let shown = 0;
            cards.forEach(c => {{
                const hay = c.getAttribute('data-search') || '';
                if (!q || hay.includes(q)) {{
                    c.style.display = 'block';
                    shown++;
                }} else {{
                    c.style.display = 'none';
                }}
            }});
            document.getElementById('visible-count').textContent = shown;
        }}
        if (document.getElementById('dir-search').value) filterDirectory();
        </script>
    """
    return HTMLResponse(
        content=wrap_html(
            f"Job Scam Directory ({len(rows)} Verified Cases) — JobScamRadar",
            content,
            description=f"Browse {len(rows)} verified employment scam alerts, fake recruitment domains, WhatsApp task scams, and FTC job fraud warnings.",
            canonical_path="/scammers"
        )
    )


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
    risk_score = normalize_risk_score(risk_score)
    score_color = "#ef4444" if risk_score >= 80 else "#f59e0b"

    is_specific_domain = domain and domain.lower() not in ("news.google.com", "consumer.ftc.gov", "reddit.com/r/scams", "")
    if is_specific_domain:
        schema_obj = {
            "@context": "https://schema.org",
            "@type": "ClaimReview",
            "datePublished": warning_date,
            "url": f"https://jobscamradar.com/scammer/{slug}",
            "author": {
                "@type": "Organization",
                "name": "JobScamRadar",
                "url": "https://jobscamradar.com"
            },
            "claimReviewed": f"The domain {domain} represents a legitimate employer or recruitment agency",
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": "1",
                "bestRating": "5",
                "worstRating": "1",
                "alternateName": f"High-Risk Employment Scam ({risk_score}% Risk)"
            },
            "itemReviewed": {
                "@type": "Organization",
                "name": domain,
                "url": f"https://{domain}"
            }
        }
    else:
        schema_obj = {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": name,
            "datePublished": warning_date,
            "dateModified": warning_date,
            "description": reason,
            "mainEntityOfPage": f"https://jobscamradar.com/scammer/{slug}",
            "image": ["https://jobscamradar.com/og_banner.jpg"],
            "author": {
                "@type": "Organization",
                "name": "JobScamRadar Threat Intelligence",
                "url": "https://jobscamradar.com"
            },
            "publisher": {
                "@type": "Organization",
                "name": "JobScamRadar (VasileDev Group)",
                "url": "https://jobscamradar.com",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://jobscamradar.com/favicon.svg"
                }
            }
        }

    schema_json = json.dumps(schema_obj, ensure_ascii=False, indent=2)

    content = f"""
        <div style="margin-bottom: 20px;">
            <a href="/scammers" style="color: #38bdf8; text-decoration: none; font-weight: 600;">&larr; Back to Scam Directory</a>
        </div>
        <div class="dossier">
            <div class="header">
                <h1>{html_lib.escape(name)}</h1>
                <div class="badge" style="background-color: {score_color};">Risk Score: {risk_score}%</div>
            </div>

            <div class="details-grid">
                <div class="detail-item"><strong>Domain / Source</strong> {html_lib.escape(domain)}</div>
                <div class="detail-item"><strong>Reporting Authority</strong> {html_lib.escape(regulator)}</div>
                <div class="detail-item"><strong>Warning Category</strong> {html_lib.escape(warning_type)}</div>
                <div class="detail-item"><strong>Warning Date</strong> {warning_date}</div>
                <div class="detail-item"><strong>Jurisdiction</strong> {html_lib.escape(jurisdiction)}</div>
                <div class="detail-item"><strong>Official Source</strong> <a href="{html_lib.escape(official_url)}" target="_blank" rel="noopener noreferrer" style="color: #38bdf8;">View Original Alert &rarr;</a></div>
            </div>

            <div class="reason">
                <h3 style="margin-top:0;">Forensic Summary &amp; Reason for Warning</h3>
                <p style="margin-bottom:0;">{html_lib.escape(reason)}</p>
            </div>

            <div class="checklist-box">
                <h3>🛡️ How to Protect Yourself From This Employment Scam</h3>
                <ul>
                    <li><strong>Never pay upfront fees:</strong> Legitimate employers never charge for training, background checks, visa processing, or task unlocking.</li>
                    <li><strong>Refuse 'Equipment Checks':</strong> Never deposit a check from a new employer and wire or Zelle money back to an 'equipment vendor'.</li>
                    <li><strong>Verify the recruiter's domain:</strong> Confirm that the hiring manager's email matches the official corporate domain (never trust unsolicited WhatsApp/Telegram messages).</li>
                </ul>
            </div>
        </div>

        <script type="application/ld+json">
{schema_json}
        </script>
    """
    return HTMLResponse(
        content=wrap_html(
            f"{name} — Employment Scam Alert | JobScamRadar",
            content,
            description=reason,
            canonical_path=f"/scammer/{slug}"
        )
    )


@app.get("/privacy")
@app.get("/privacy-policy.html")
@app.get("/terms.html")
def serve_privacy():
    content = """
        <div class="dossier">
            <div class="header">
                <h1>Privacy Policy, GDPR &amp; Legal Disclosure</h1>
            </div>
            <p style="color:#cbd5e1;line-height:1.65;">
                <strong>JobScamRadar.com</strong> is a public-interest cybersecurity and employment fraud awareness portal operated by <strong>VasileDev Group (Bratu Vasile)</strong>, registered in the European Union under VAT / P.IVA <code>IT04226190041</code> (VIES Verified), with operational offices in Garessio (CN), Italy and Odobești, Romania.
            </p>
            <h3 style="color:#38bdf8;">1. Data Collection &amp; GDPR Compliance (EU Reg. 2016/679)</h3>
            <p style="color:#cbd5e1;line-height:1.65;">
                Queries submitted to our instant Job &amp; Recruiter Verifier are processed transiently to match known fraud patterns and public regulatory alerts (FTC, BBB, ICO, law enforcement advisories). We do not sell personal data to third parties. For GDPR inquiries or data removal requests, contact <a href="mailto:amendamax@vasiledev.com" style="color:#38bdf8;">amendamax@vasiledev.com</a>.
            </p>
            <h3 style="color:#38bdf8;">2. Affiliate &amp; Editorial Disclosure</h3>
            <p style="color:#cbd5e1;line-height:1.65;">
                JobScamRadar is 100% free for public use. To sustain server and threat-intelligence indexing costs, pages may include clearly labeled affiliate links (marked with <code>rel="sponsored"</code>) to identity-protection tools such as Surfshark Alternative ID.
            </p>
        </div>
    """
    return HTMLResponse(
        content=wrap_html(
            "Privacy Policy & Legal Disclosure — JobScamRadar",
            content,
            description="Privacy Policy, GDPR compliance, and corporate disclosure for JobScamRadar.com by VasileDev Group (P.IVA IT04226190041).",
            canonical_path="/privacy"
        )
    )


@app.get("/llms.txt")
@app.get("/.well-known/llms.txt")
def serve_llms_txt():
    txt = """# JobScamRadar.com — Global Employment Fraud & Fake Recruiter Intelligence
> Operated by VasileDev Group (EU VIES VAT: IT04226190041)

## Overview
JobScamRadar monitors, curates, and indexes fraudulent job offers, imposter recruiter domains, WhatsApp/Telegram task-optimization scams, reshipping/money-mule traps, and official FTC consumer employment alerts.

## Key Endpoints
- Homepage & Instant Job/Recruiter Verifier: https://jobscamradar.com/
- Verified Job Scam Directory: https://jobscamradar.com/scammers
- Verification API: https://jobscamradar.com/api/verify-job?q={domain_or_keyword}
- XML Sitemap: https://jobscamradar.com/sitemap.xml
"""
    return Response(content=txt, media_type="text/plain; charset=utf-8")


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
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>https://jobscamradar.com/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>',
        f'  <url><loc>https://jobscamradar.com/scammers</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.9</priority></url>',
        f'  <url><loc>https://jobscamradar.com/privacy</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.5</priority></url>',
    ]

    for slug, rep_date in rows:
        safe_slug = html_lib.escape(slug)
        lastmod = rep_date if rep_date else today
        loc = f"https://jobscamradar.com/scammer/{safe_slug}"
        xml.append(f'  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>')

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
