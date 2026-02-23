# app/routes/analytics.py

from fastapi import APIRouter
from app.database import cursor

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/overview")
def overview():

    cursor.execute("SELECT COUNT(*) FROM scan_history")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk='HIGH'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk='MEDIUM'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk='LOW'")
    low = cursor.fetchone()[0]

    return {
        "total_scans": total,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low
    }


@router.get("/recent")
def recent():

    cursor.execute("""
        SELECT message, risk, score, created_at
        FROM scan_history
        ORDER BY created_at DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()

    return [
        {
            "message": r[0],
            "risk": r[1],
            "score": r[2],
            "timestamp": r[3]
        }
        for r in rows
    ]