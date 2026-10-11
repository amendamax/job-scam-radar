import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
server_py = os.path.join(base_dir, "server.py")

with open(server_py, "r", encoding="utf-8") as f:
    py = f.read()

py = py.replace('app.get("/video_thumbnail.png")', 'app.get("/video_thumbnail_v2.png")')
py = py.replace('os.path.exists("video_thumbnail.png")', 'os.path.exists("video_thumbnail_v2.png")')
py = py.replace('FileResponse("video_thumbnail.png")', 'FileResponse("video_thumbnail_v2.png")')

with open(server_py, "w", encoding="utf-8") as f:
    f.write(py)
