
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS email_status (
                        id INTEGER PRIMARY KEY,
                        recipient TEXT,
                        subject TEXT,
                        status TEXT,
                        sent_at DATETIME)''')
    conn.commit()
    conn.close()

def log_email_status(recipient: str, subject: str, status: str):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO email_status (recipient, subject, status, sent_at) VALUES (?, ?, ?, ?)",
                   (recipient, subject, status, datetime.now()))
    conn.commit()
    conn.close()