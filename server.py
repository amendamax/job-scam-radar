import os
import re
import sqlite3

HEADER_HTML = """<header>
        <h1 style="text-decoration: none;"><a href="/" style="color: #38bdf8; text-decoration: none;">JobScamRadar</a></h1>
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
                <p style="margin: 0; color: #94a3b8; font-size: 0.85rem;">Direct: <a href="mailto:amendamax@vasiledev.com" style="color: #cbd5e1; text-decoration: none; white-space: nowrap;">amendamax@vasiledev.com</a></p>
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
        </div>
    </footer>"""

INCOGNI_URL = os.getenv("INCOGNI_URL", "https://incogni.com/")
FLEXJOBS_URL = os.getenv("FLEXJOBS_URL", "https://flexjobs.com/")

AFFILIATE_HTML = """<div class="affiliate-section">
            <div class="aff-card privacy">
                <h4 style="color: #38bdf8;">🛡️ Generate a Fake Identity</h4>
                <p>Don\'t give fake recruiters your real phone number or email. Use Surfshark Alternative ID to generate working proxy details and protect yourself from spam and identity theft.</p>
                <a href="https://www.tkqlhce.com/click-101863908-15740542" target="_blank" rel="sponsored noopener noreferrer">Protect Your Identity (Alternative ID)</a>
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
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-950R9NXTL9"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-950R9NXTL9');
    </script>
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

DB_PATH = "/var/data/database.db" if os.path.exists("/var/data/database.db") else "database.db"

def normalize_risk_score(risk_score):
    try:
        score = int(risk_score)
    except Exception:
        score = 88
    if score <= 10:
        return min(99, score * 10 + 8)
    return score

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
    31: ("Hyderabad Work-From-Home & Task Fraud Ring (₹94.9L Loss)", "Work-From-Home Scam", "Cybercrime police investigation into organized online task and part-time employment fraudsters who defrauded victims of ₹94.9 lakh.", 94),
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
    56: ("Fake $18–$25/Hour Remote Data Entry Job Scams Targeting West Africa", "Data Entry Job Scam", "Regional employment fraud warning exposing fake $18–$25/hour remote data entry listings that charge applicants for training materials or software.", 92),
    57: ("Government Job Warning: Overseas Cyber Scam Compound Recruitment", "Trafficking / Scam Hub", "Official government advisory warning job seekers against fraudulent overseas IT and customer service job offers following cybercrime raids in Zambia.", 94),
    58: ("Work-From-Home Job Scams Targeting Remote Applicants", "Work-From-Home Scam", "Consumer safety guide highlighting how to verify legitimate remote work opportunities and avoid advance-fee home assembly and typing scams.", 88),
    59: ("Human Trafficking & Forced Cyber-Scam Compound Recruitment Alert", "Trafficking / Scam Hub", "Diplomatic and law enforcement confirmation that victims were lured by fake overseas job advertisements into a cybercrime operation.", 95),
    60: ("AI-Generated Recruiter & Deepfake Job Interview Scam", "AI Recruitment Scam", "Security analysis of an AI-assisted recruitment scam utilizing realistic corporate emails, cloned job descriptions, and automated interview lures.", 94),
    61: ("UK Regulator Warning: 3,600+ Complaints Over 'Add Me on WhatsApp' Job Calls", "WhatsApp Task Scam", "Regulatory enforcement alert after more than 3,600 consumers reported automated scam calls directing victims to WhatsApp recruitment bots.", 94),
    62: ("Visakhapatnam Work-From-Home Task Cyberfraud (₹1+ Crore Loss)", "Work-From-Home Scam", "Police cybercrime report detailing how 20 residents lost over ₹1 crore to fraudulent part-time work-from-home task and rating schemes.", 95),
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
}

def migrate_and_clean_db(db_file: str):
    if not os.path.exists(db_file):
        return
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
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
            else:
                # Generic cleanup for any remaining news/FTC rows
                new_name = re.sub(r'\s+-\s+[^-]+$', '', new_name)
                new_name = re.sub(r'\.{2,}$', '', new_name).strip()

            # Clean cut-off mid-sentence FTC reasons
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

for _candidate_db in ("database.db", "/var/data/database.db"):
    migrate_and_clean_db(_candidate_db)

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
        risk_score = normalize_risk_score(risk_score)
        score_color = "#ef4444" if risk_score >= 80 else "#f59e0b"
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
    risk_score = normalize_risk_score(risk_score)
    
    score_color = "#ef4444" if risk_score >= 80 else "#f59e0b"

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
