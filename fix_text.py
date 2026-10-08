import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return

    # Replace VerifyDating terms
    new_content = content.replace("VerifyDating", "JobScamRadar")
    new_content = new_content.replace("Verify Dating", "Job Scam Radar")
    new_content = new_content.replace("dating apps", "remote jobs")
    new_content = new_content.replace("Dating Apps", "Remote Jobs")
    new_content = new_content.replace("dating safety", "job safety")
    new_content = new_content.replace("Dating Safety", "Job Safety")
    new_content = new_content.replace("catfish", "scammer")
    new_content = new_content.replace("Catfish", "Scammer")
    new_content = new_content.replace("romance scams", "job scams")
    new_content = new_content.replace("Romance Scams", "Job Scams")
    new_content = new_content.replace("Romance Scam", "Job Scam")
    new_content = new_content.replace("dating profile", "job offer")
    new_content = new_content.replace("Dating Profile", "Job Offer")
    new_content = new_content.replace("Dating profile", "Job offer")
    new_content = new_content.replace("Tinder Photo", "WhatsApp Offer")
    new_content = new_content.replace("Bumble Profile", "Telegram Offer")
    new_content = new_content.replace("Hinge Profile", "Upwork Scam")
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

for root, dirs, files in os.walk(base_dir):
    for name in files:
        if name.endswith('.html') or name.endswith('.js') or name == "server.py":
            process_file(os.path.join(root, name))

print("Text replaced!")
