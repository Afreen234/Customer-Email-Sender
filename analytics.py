import sqlite3

def get_email_analytics():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM email_status GROUP BY status")
    stats = cursor.fetchall()
    conn.close()
    return {"analytics": stats}