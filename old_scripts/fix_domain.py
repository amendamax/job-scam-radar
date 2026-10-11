lines = open('server.py', 'r', encoding='utf-8').read()

lines = lines.replace('domain = "verifyjob.net" if is_job else "jobscamradar.com"', 'domain = "jobscamradar.com"')
lines = lines.replace('domain = \'verifyjob.net\' if is_job else \'jobscamradar.com\'', 'domain = "jobscamradar.com"')
lines = lines.replace('https://verifyjob.net', 'https://jobscamradar.com')

open('server.py', 'w', encoding='utf-8').write(lines)
