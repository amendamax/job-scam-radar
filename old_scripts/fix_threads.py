import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
server_py = os.path.join(base_dir, "server.py")

with open(server_py, "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
for line in lines:
    if "threading.Thread(target=_daily_harvester" in line or "threading.Thread(target=_weekly_dating_harvester" in line:
        continue
    out.append(line)

with open(server_py, "w", encoding="utf-8") as f:
    f.write("".join(out))
