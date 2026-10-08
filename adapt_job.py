import os
import re

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"
index_html = os.path.join(base_dir, "index.html")

with open(index_html, "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "Scammer Face Search": "Job Scam Screenshot Scanner",
    "scammer face search": "job scam screenshot scanner",
    "reverse image search face scanner": "AI screenshot analysis tool",
    "dating photo verifier": "recruiter message verifier",
    "scammer photo checker": "fake job offer checker",
    "AI Biometric Face Recognition Engine": "AI Scam Message Recognition Engine",
    "Reverse Image & Biometric Face Search for Job Safety": "WhatsApp & Telegram Scam Message Scanner",
    "biometric mapping": "text pattern mapping",
    "Biometric Face Matching Accuracy": "Scam Pattern Matching Accuracy",
    "FaceMatch Analysis Summary": "JobScam Analysis Summary",
    "68 unique facial biometrics": "120 unique scam language patterns",
    "(jaw structure, eye positioning, nose width)": "(fake salary promises, crypto requests, urgency triggers)",
    "mathematical model of the profile photo": "mathematical model of the job offer",
    "find duplicate copies of the face": "find duplicate copies of this exact scam script",
    "neural networks to map facial biometrics (eyes, nose, jawline)": "neural networks to map scam scripts (grammar, URLs, crypto addresses)",
    "biometric facial mapping algorithms": "AI screenshot reading algorithms",
    "identifying identical or heavily modified matches": "identifying identical or heavily modified scam messages",
    "even if the photo was cropped, mirrored, or filtered": "even if the message was slightly rephrased by the scammer",
    "FaceCheck.ID": "ScamAdviser",
    "run his Tinder photo through": "run the WhatsApp screenshot through",
    "found the exact same face": "found the exact same message script",
    "flagged her photo": "flagged the recruiter's message",
    "programmatic access to 482,930+ monitored stolen identities, reverse-face matching, and AI deepfake detection": "programmatic access to 482,930+ monitored scam phone numbers, fake company names, and AI threat detection",
    "482,930+ Stolen Faces": "482,930+ Scam Numbers & Scripts",
    "Protecting dating singles and exposing romance fraud syndicates.": "Protecting remote workers and exposing fake job syndicates.",
    "Instant biometric facial analysis": "Instant screenshot text analysis",
    "Drag & drop photo here": "Drag & drop screenshot here",
    "Upload a photo of the person": "Upload a screenshot of the message",
    "facial recognition AI": "AI text & image recognition",
    "Deepfake AI": "Fake Company",
    "Synthetic Face Detection": "Fake Registration Detection",
    "VERIFIABLE BIOMETRIC INTELLIGENCE": "VERIFIABLE THREAT INTELLIGENCE",
    "Objective Biometric Data": "Objective Cybersecurity Data",
    "dating app, social network": "job board, freelancer platform",
    "Social & Web Profiles": "Scam Messages & Numbers",
    "matches on Tinder, Bumble, Hinge, Grindr, Facebook, Instagram, or any other social network": "job offers on WhatsApp, Telegram, Upwork, LinkedIn, Indeed, or Facebook",
    "Romance scam statistics cited by leading media": "Job scam statistics cited by leading media"
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open(index_html, "w", encoding="utf-8") as f:
    f.write(html)

app_js = os.path.join(base_dir, "app.js")
if os.path.exists(app_js):
    with open(app_js, "r", encoding="utf-8") as f:
        js = f.read()
    
    js = js.replace("Face Match Found", "Scam Pattern Found")
    js = js.replace("Biometric match", "Pattern match")
    js = js.replace("Face Match", "Scam Match")
    js = js.replace("Face Signature", "Scam Signature")
    
    with open(app_js, "w", encoding="utf-8") as f:
        f.write(js)

print("HTML/JS content fully adapted to Job Scams.")
