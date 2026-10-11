import re

with open('server.py', 'r', encoding='utf-8') as f:
    s = f.read()

# Replace the json_ld_schema block in job_scam_detail
replacement = """    json_ld_schema = f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "ClaimReview",
      "datePublished": "{warning_date}",
      "url": "https://jobscamradar.com/scammer/{slug}",
      "author": {{
        "@type": "Organization",
        "name": "JobScamRadar",
        "url": "https://jobscamradar.com"
      }},
      "claimReviewed": "The company '{name}' is offering legitimate jobs ({domain})",
      "reviewRating": {{
        "@type": "Rating",
        "ratingValue": "1",
        "bestRating": "5",
        "worstRating": "1",
        "alternateName": "Confirmed Scam"
      }},
      "itemReviewed": {{
        "@type": "Organization",
        "name": "{name}",
        "sameAs": "{domain}"
      }}
    }}
    </script>
    '''"""

s = re.sub(r'    json_ld_schema = f\"\"\"[\s\S]*?    \"\"\"', replacement, s)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(s)
