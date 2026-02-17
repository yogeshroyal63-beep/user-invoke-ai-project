# app/routes/security_stats.py

from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/api")

DB_PATH = "trustcheck.db"


@router.get("/security-stats")
def get_security_stats():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM security_logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM security_logs WHERE risk='HIGH'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM security_logs WHERE risk='MEDIUM'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM security_logs WHERE risk='LOW'")
    low = cursor.fetchone()[0]

    conn.close()

    return {
        "total_scans": total,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low
    }
