# app/services/telemetry.py

import logging

logging.basicConfig(
    filename="threat_telemetry.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

def log_threat(user_id, message, risk, score):
    logging.info(f"user={user_id} | risk={risk} | score={score} | message={message}")