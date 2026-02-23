# app/services/behavior_engine.py

from app.database import cursor, conn
from datetime import datetime


def update_user_behavior(user_id, risk):

    cursor.execute(
        "SELECT total_scans, high_risk_count, medium_risk_count FROM user_behavior WHERE user_id=?",
        (user_id,)
    )
    row = cursor.fetchone()

    if row:
        total, high, medium = row
    else:
        total, high, medium = 0, 0, 0

    total += 1

    if risk == "HIGH":
        high += 1
    elif risk == "MEDIUM":
        medium += 1

    cursor.execute("""
        INSERT OR REPLACE INTO user_behavior
        (user_id, total_scans, high_risk_count, medium_risk_count, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, total, high, medium, datetime.utcnow()))

    conn.commit()


def behavioral_risk_adjustment(user_id, base_score):

    cursor.execute(
        "SELECT high_risk_count, medium_risk_count FROM user_behavior WHERE user_id=?",
        (user_id,)
    )
    row = cursor.fetchone()

    if not row:
        return base_score

    high, medium = row

    if high >= 5:
        base_score += 15
    elif medium >= 5:
        base_score += 10

    return min(base_score, 100)