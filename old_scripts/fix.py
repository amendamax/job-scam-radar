import os

s = open('server.py', 'r', encoding='utf-8').read()

replacement = """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Force copy if persistent DB is empty but we have data in git
    try:
        cursor.execute("SELECT COUNT(*) FROM job_scam_reports")
        count = cursor.fetchone()[0]
        if count == 0 and os.path.exists("database.db"):
            print("Persistent DB is empty! Copying populated database.db from Git repository...")
            import shutil
            conn.close()
            shutil.copy("database.db", DB_PATH)
            conn = get_db_connection()
            cursor = conn.cursor()
    except Exception as e:
        print("Error checking DB:", e)
"""

if "Persistent DB is empty!" not in s:
    s = s.replace("    conn = get_db_connection()\n    cursor = conn.cursor()", replacement, 1)
    open('server.py', 'w', encoding='utf-8').write(s)
