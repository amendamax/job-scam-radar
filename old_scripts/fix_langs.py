import re

lines = open('server.py', 'r', encoding='utf-8').read()

lines = re.sub(
    r'langs = \["ro", "it", "es", "fr", "de", "pt", "ru"\]\s*for l in langs:.*?<\/priority><\/url>\'\)', 
    '', 
    lines, 
    flags=re.DOTALL
)

lines = re.sub(
    r'langs = \["en", "ro", "it", "de", "fr", "es", "pt", "ru"\]\s*xml_entries = \[\]\s*for slug, created_at in part_rows:\s*date_str = created_at.*?(?=xml_entries\.append)', 
    'langs = ["en"]\n\n    xml_entries = []\n    for slug, created_at in part_rows:\n        date_str = created_at.split(" ")[0] if created_at else "2026-08-25"\n        for l in langs:\n            loc = f"{base_url}/scam-reports/{slug}"\n            ', 
    lines, 
    flags=re.DOTALL
)

# And remove it from sitemap_job_scams_part too
lines = re.sub(
    r'langs = \["en", "ro", "it", "de", "fr", "es", "pt", "ru"\]\s*for slug, first_reported_date in part_rows:\s*date_str = first_reported_date.*?(?=xml\.append)',
    'langs = ["en"]\n    for slug, first_reported_date in part_rows:\n        date_str = first_reported_date.split(" ")[0] if first_reported_date else "2026-08-25"\n        for l in langs:\n            loc = f"https://verifyjob.net/scammers/{slug}"\n            ',
    lines,
    flags=re.DOTALL
)

open('server.py', 'w', encoding='utf-8').write(lines)
