import re
lines = open('server.py', 'r', encoding='utf-8').read()

html_banner = '''
<div style="margin: 25px 0; padding: 20px; background: rgba(239, 68, 68, 0.05); border-left: 4px solid #ef4444; border-radius: 4px;">
    <h3 style="color: #ef4444; margin-bottom: 10px; font-size: 1.1rem;">
        <i class="fas fa-shield-alt" style="margin-right: 8px;"></i>SECURITY WARNING: Did you apply for this job?
    </h3>
    <p style="color: #cbd5e1; margin-bottom: 15px; font-size: 0.95rem; line-height: 1.5;">
        If you sent your Resume, ID, Passport, or SSN to this fake recruiter, your identity is highly compromised. Scammers use this data to open fraudulent bank accounts in your name.
    </p>
    <a href="https://jobscamradar.com/out/lifelock" target="_blank" rel="nofollow sponsored" style="display: inline-block; background: #ef4444; color: #fff; padding: 10px 18px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.9rem;">
        <i class="fas fa-search" style="margin-right: 6px;"></i> Scan the Dark Web for Your Data Now
    </a>
</div>
<div style="margin: 20px 0; padding: 20px; background: rgba(16, 185, 129, 0.05); border-left: 4px solid #10b981; border-radius: 4px;">
    <h3 style="color: #10b981; margin-bottom: 10px; font-size: 1.1rem;">
        <i class="fas fa-briefcase" style="margin-right: 8px;"></i>Need a Real, Safe Remote Job?
    </h3>
    <p style="color: #cbd5e1; margin-bottom: 15px; font-size: 0.95rem; line-height: 1.5;">
        Stop wasting time on WhatsApp recruiters and Facebook groups. Join platforms where every job is hand-screened and 100% verified by experts.
    </p>
    <a href="https://jobscamradar.com/out/flexjobs" target="_blank" rel="nofollow sponsored" style="display: inline-block; background: #10b981; color: #fff; padding: 10px 18px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.9rem;">
        <i class="fas fa-check-circle" style="margin-right: 6px;"></i> Find 100% Verified Remote Jobs
    </a>
</div>
'''

# Find the place in get_scam_report_page where the HTML is generated
lines = lines.replace('<div class="action-buttons">', f'{html_banner}\n<div class="action-buttons">')

# And remove the 58 pages bug (the 6 broker reviews for sitemap)
lines = re.sub(r'for b in \[\"interactive-companys\", \"avatrade\", \"xm\", \"exness\", \"etoro\", \"plus500\"\]:.*?<\/priority><\/url>\'\)', '', lines, flags=re.DOTALL)

open('server.py', 'w', encoding='utf-8').write(lines)
