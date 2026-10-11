import os

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "https://www.instagram.com/verifydating_net/": "https://www.instagram.com/jobscamradar/",
    "dating-forum-archive.com/users": "scam-forum-archive.com/users",
    "Verified Safe Singles Dating": "Verified Safe Job Boards",
    "dating-safe-card": "job-safe-card",
    "SAFE DATING TOOLKIT": "SAFE RECRUITING TOOLKIT",
    "Match.com & OurTime (Verified Safe Dating)": "FlexJobs & Remote.co (Verified Safe Jobs)",
    "VERIFIED DATING": "VERIFIED JOBS",
    "/go/dating-singles": "/go/job-boards",
    "logo-dating-shield": "logo-job-shield",
    "dating_bg.webp": "jobscam_bg.webp"
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
