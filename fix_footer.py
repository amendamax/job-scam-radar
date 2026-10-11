import re

footer_html = '''
<footer style="background-color: #05080f; padding: 60px 20px 20px 20px; font-family: system-ui, -apple-system, sans-serif; color: #94a3b8; font-size: 14px; border-top: 1px solid #1e293b; margin-top: 60px;">
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
</footer>
'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_html = re.sub(r'<footer.*?</footer>', footer_html, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# also replace inside server.py so it serves correctly
with open('server.py', 'r', encoding='utf-8') as f:
    server_html = f.read()

new_server_html = re.sub(r'<footer.*?</footer>', footer_html, server_html, flags=re.DOTALL)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(new_server_html)
