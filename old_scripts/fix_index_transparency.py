import re

with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Make the backgrounds solid
s = re.sub(r'background:\s*rgba\([^)]+,\s*0\.[12][05]?\)', 'background: #0f172a', s)
# Or maybe the background is set on the links
s = s.replace('background: rgba(16, 185, 129, 0.15)', 'background: #10b981')
s = s.replace('background: rgba(245, 158, 11, 0.15)', 'background: #f59e0b')
s = s.replace('background: rgba(255,255,255,0.03)', 'background: #1e293b')
s = s.replace('background: rgba(255,255,255,0.05)', 'background: #334155')
s = s.replace('background: rgba(15, 23, 42, 0.85)', 'background: #0f172a')

# specifically for the toolkit section
toolkit_idx = s.find('<section id="toolkit"')
if toolkit_idx != -1:
    toolkit_end = s.find('</section>', toolkit_idx)
    toolkit_html = s[toolkit_idx:toolkit_end]
    
    # Make buttons solid
    toolkit_html = toolkit_html.replace('background: rgba(16, 185, 129, 0.15);', 'background: #059669;')
    toolkit_html = toolkit_html.replace('background: rgba(16, 185, 129, 0.1);', 'background: #059669;')
    toolkit_html = toolkit_html.replace('background: rgba(245, 158, 11, 0.15);', 'background: #d97706;')
    toolkit_html = toolkit_html.replace('background: rgba(245, 158, 11, 0.1);', 'background: #d97706;')
    
    # Make text white instead of green/orange if background is solid
    toolkit_html = toolkit_html.replace('color: #10b981;', 'color: #ffffff;')
    toolkit_html = toolkit_html.replace('color: #f59e0b;', 'color: #ffffff;')
    
    # Make card backgrounds solid
    toolkit_html = toolkit_html.replace('background: rgba(255, 255, 255, 0.02);', 'background: #1e293b;')
    toolkit_html = toolkit_html.replace('background: rgba(255, 255, 255, 0.03);', 'background: #1e293b;')
    toolkit_html = toolkit_html.replace('backdrop-filter: blur(12px);', '')
    
    s = s[:toolkit_idx] + toolkit_html + s[toolkit_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)
