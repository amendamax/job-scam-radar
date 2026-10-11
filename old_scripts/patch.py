import os
import re

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
server_file = os.path.join(base_dir, "server.py")
app_js_file = os.path.join(base_dir, "broker-verifier", "app.js")

with open(server_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Domain names
content = content.replace("isbrokersafe.com", "jobscamradar.com")
content = content.replace("IsBrokerSafe.com", "JobScamRadar.com")
content = content.replace("IsBrokerSafe", "JobScamRadar")

# Replace translations texts broadly
content = content.replace("Broker Verifier", "Job Scam Radar")
content = content.replace("broker", "company")
content = content.replace("Broker", "Company")
content = content.replace("BROKER", "COMPANY")

with open(server_file, "w", encoding="utf-8") as f:
    f.write(content)

print("server.py updated.")
