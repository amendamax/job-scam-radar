import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
index_html = os.path.join(base_dir, "index.html")

with open(index_html, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('Verify<span class="highlight">Dating</span>', 'JobScam<span class="highlight">Radar</span>')
content = content.replace('fa-shield-heart', 'fa-briefcase')
content = content.replace('verifydating.net', 'jobscamradar.com')
content = content.replace('JobScamRadar.net', 'JobScamRadar.com')

with open(index_html, "w", encoding="utf-8") as f:
    f.write(content)

index_css = os.path.join(base_dir, "index.css")
with open(index_css, "r", encoding="utf-8") as f:
    css = f.read()

# Replace pink/dating colors with orange/yellow
css = css.replace("#ec4899", "#f59e0b") # Pink to Amber
css = css.replace("#be185d", "#d97706") # Dark pink to Dark Amber
css = css.replace("rgba(236, 72, 153", "rgba(245, 158, 11") 
css = css.replace("rgba(190, 24, 93", "rgba(217, 119, 6")

with open(index_css, "w", encoding="utf-8") as f:
    f.write(css)

print("Logo and colors fixed.")
