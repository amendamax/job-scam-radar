import os
import re

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"

def replace_colors(file_path):
    if not os.path.exists(file_path): return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace main blue with orange
    content = content.replace("#2563eb", "#ea580c") # Main primary
    content = content.replace("#3b82f6", "#f97316") # Hover / lighter
    content = content.replace("#1d4ed8", "#c2410c") # Darker
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

replace_colors(os.path.join(base_dir, "style.css"))
replace_colors(os.path.join(base_dir, "index.css"))
# Also inside app.js if there are hardcoded colors
replace_colors(os.path.join(base_dir, "broker-verifier", "app.js"))
replace_colors(os.path.join(base_dir, "broker-verifier", "style.css"))

print("Colors updated to Orange/Black theme!")
