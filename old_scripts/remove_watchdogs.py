import os
import re

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
server_py = os.path.join(base_dir, "server.py")

with open(server_py, "r", encoding="utf-8") as f:
    py = f.read()

# We need to remove the watchdogs start_watchdog_daemons()
py = re.sub(r'async def start_watchdog_daemons\(\):.*?asyncio\.create_task\(start_watchdog_daemons\(\)\)', '', py, flags=re.DOTALL)
py = py.replace('asyncio.create_task(start_watchdog_daemons())', '')

with open(server_py, "w", encoding="utf-8") as f:
    f.write(py)

print("Watchdogs removed")
