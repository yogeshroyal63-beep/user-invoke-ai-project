# app/services/security_logger.py

import sqlite3
from datetime import datetime

DB_PATH = "trustcheck.db"

def init_security_log_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            risk TEXT,
            score INTEGER,
            category TEXT,
            attack_pattern TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def log_security_event(message, risk, score, category, attack_pattern):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO security_logs
        (message, risk, score, category, attack_pattern, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        message,
        risk,
        score,
        category,
        attack_pattern,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()
