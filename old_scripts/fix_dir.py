import re
with open('server.py', 'r', encoding='utf-8') as f:
    s = f.read()

replacement = """
    # Base count for filtered query
    count_query = "SELECT COUNT(*) FROM job_scam_reports WHERE 1=1"
    query_str = "SELECT id, slug, entity_name, domain, warning_type, risk_score, warning_date FROM job_scam_reports WHERE 1=1"
    params = []
    
    if category:
        count_query += " AND warning_type LIKE ?"
        query_str += " AND warning_type LIKE ?"
        params.append(f"%{category}%")
    if q:
        count_query += " AND (entity_name LIKE ? OR domain LIKE ? OR reason LIKE ?)"
        query_str += " AND (entity_name LIKE ? OR domain LIKE ? OR reason LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])
        
    cursor.execute(count_query, params)
    filtered_total = cursor.fetchone()[0]
    
    query_str += f" ORDER BY id DESC LIMIT {limit} OFFSET {offset}"
    cursor.execute(query_str, params)
    profiles = cursor.fetchall()
    conn.close()
    
    total_pages = max(1, (filtered_total + limit - 1) // limit)
    
    cards_html = ""
    for p in profiles:
        pid, slug, name, domain, cat, score, rep_date = p
        real_score = score * 10 if score <= 10 else score
        
        cards_html += f'''
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 20px; transition: all 0.25s ease;" onmouseover="this.style.borderColor='#ec4899'; this.style.boxShadow='0 0 16px rgba(236,72,153,0.35)';" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'; this.style.boxShadow='none';">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <span style="background: rgba(236, 72, 153, 0.15); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.3); padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700;">{cat}</span>
                <span style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 800;">{real_score}% RISK</span>
            </div>
            <h3 style="font-family: 'Outfit', sans-serif; font-size: 18px; color: #fff; margin: 0 0 6px 0;">{name}</h3>
            <p style="color: #94a3b8; font-size: 13px; margin: 0 0 14px 0; line-height: 1.4;">Domain: {domain}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 12px;">
                <span style="color: #64748b; font-size: 11px;">⚠️ Alert Date: {rep_date}</span>
                <a href="/scammer/{slug}" style="background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); color: #fff; text-decoration: none; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 700;">View Dossier ➔</a>
            </div>
        </div>
        '''
"""

# Find the block from # Base count to the end of the cards loop
pattern = re.compile(r'# Base count for filtered query.*?cat_pills_html =', re.DOTALL)
s, count = pattern.subn(replacement + "\n    cat_pills_html =", s)
print('Replacements made:', count)
with open('server.py', 'w', encoding='utf-8') as f:
    f.write(s)
