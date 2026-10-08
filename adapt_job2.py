import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
index_html = os.path.join(base_dir, "index.html")

with open(index_html, "r", encoding="utf-8") as f:
    html = f.read()

reps = {
    "romance scam": "job scam",
    "Romance scam": "Job scam",
    "romance scammer": "job scammer",
    "romance fraud": "job fraud",
    "reverse image search face": "scam message screenshot",
    "biometric mapping": "text pattern mapping",
    "Biometric Mapping": "Text Pattern Mapping",
    "facial biometrics": "message patterns",
    "facial recognition": "screenshot reading",
    "Facial Recognition": "Screenshot Analysis",
    "Facial Matching": "Message Matching",
    "facial analysis": "text analysis",
    "AI Biometric": "AI Screenshot",
    "biometric scan": "screenshot scan",
    "Biometric scan": "Screenshot scan",
    "biometric mapping algorithms": "screenshot reading algorithms",
    "Tinder photo": "WhatsApp screenshot",
    "Tinder, Bumble, Hinge, Grindr": "WhatsApp, Telegram, Upwork, LinkedIn",
    "Bumble": "Telegram",
    "VKontakte": "fake Upwork",
    "pip install verifydating": "pip install jobscamradar",
    "Dating Security Report": "Job Scam Security Report",
    "Verifying a dating photo takes just 3 seconds": "Verifying a job offer takes just 3 seconds",
    "dating photo": "job offer screenshot",
    "dating profile": "job offer",
    "fake profile": "fake job offer",
    "AI Facial": "AI Text",
    "face search": "screenshot search",
    "Face Search": "Screenshot Search",
    "face verifi": "message verifi",
    "Face verification": "Message verification",
    "/api/v1/dating-docs": "/api/v1/job-docs",
    "btn-dating": "btn-jobscam"
}

for k, v in reps.items():
    html = html.replace(k, v)

with open(index_html, "w", encoding="utf-8") as f:
    f.write(html)

print("Remaining terms replaced!")
