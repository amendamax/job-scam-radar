import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
server_py = os.path.join(base_dir, "server.py")

with open(server_py, "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if "async def start_watchdog_daemons():" in line:
        skip = True
    if skip and "if __name__ == '__main__':" in line:
        skip = False
    
    if not skip and "asyncio.create_task(start_watchdog_daemons())" not in line:
        out.append(line)

with open(server_py, "w", encoding="utf-8") as f:
    f.writelines(out)
