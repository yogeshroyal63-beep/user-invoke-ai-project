# app/database.py

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "trustcheck.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ===============================
# CREATE TABLES IF NOT EXISTS
# ===============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS scan_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    message TEXT,
    risk TEXT,
    score INTEGER,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_behavior (
    user_id TEXT PRIMARY KEY,
    total_scans INTEGER,
    high_risk_count INTEGER,
    medium_risk_count INTEGER,
    updated_at TEXT
)
""")

conn.commit()