# app/routes/security_history.py

from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/api")

DB_PATH = "trustcheck.db"


@router.get("/security-history")
def get_security_history(limit: int = 20):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, risk, score, category, attack_pattern, created_at
        FROM security_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    results = []

    for row in rows:
        results.append({
            "message": row[0],
            "risk": row[1],
            "score": row[2],
            "category": row[3],
            "attack_pattern": row[4],
            "created_at": row[5]
        })

    return {
        "count": len(results),
        "data": results
    }
