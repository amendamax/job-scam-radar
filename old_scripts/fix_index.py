import re

# 1. Update server.py API endpoint to use job_scam_reports instead of job_scam_profiles
server_code = open('server.py', 'r', encoding='utf-8').read()

server_code = server_code.replace(
    'cursor.execute("SELECT COUNT(*) FROM job_scam_profiles")', 
    'cursor.execute("SELECT COUNT(*) FROM job_scam_reports")'
)
server_code = server_code.replace(
    'SELECT slug, persona_name, gender, scam_category, claimed_age, claimed_profession, risk_score, views_count, first_reported_date FROM job_scam_profiles',
    'SELECT slug, entity_name, \'N/A\', warning_type, \'N/A\', regulator, risk_score, 100, warning_date FROM job_scam_reports'
)
open('server.py', 'w', encoding='utf-8').write(server_code)

# 2. Clean index.html
html = open('index.html', 'r', encoding='utf-8').read()

# Fix the texts
html = html.replace('Meet Genuine, Verified Singles', 'Meet Genuine, Verified Employers')
html = html.replace('Check Official Broker Licenses', 'Find Safe Remote Jobs')
html = html.replace('Browse Full Scammer Blacklist (350,000+ Dossiers)', 'Browse Full Job Scams Blacklist')
html = html.replace('85.4M+ verified job scam messages', 'latest verified remote job scams')
html = html.replace('Verify unknown contacts using our Official Security Toolkit.', 'Join platforms where every job is hand-screened and 100% verified by experts.')
html = html.replace('Tired of fake job offers, bots, and WhatsApp scammer traps?', 'Tired of WhatsApp recruiters and fake data entry jobs?')
html = html.replace('Check Official Broker Licenses ➔', 'Find 100% Verified Remote Jobs ➔')

# Remove the wait modal
html = re.sub(r'<div id="exit-intent-modal".*?<!-- Live Scammer Feed -->', '<!-- Live Scammer Feed -->', html, flags=re.DOTALL)

# Remove the photo scanner UI
html = re.sub(r'<div class="scanner-box">.*?</div>\s*<!-- Stats -->', '<!-- Stats -->', html, flags=re.DOTALL)
html = re.sub(r'<p style="color: var\(--text-muted\); font-size: 0\.95rem; margin-bottom: 25px;">Upload a screenshot of the WhatsApp message or the recruiter\'s profile photo to detect fraud instantly\.</p>', '', html, flags=re.DOTALL)


open('index.html', 'w', encoding='utf-8').write(html)
