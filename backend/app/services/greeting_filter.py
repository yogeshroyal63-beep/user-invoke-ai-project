# app/services/greeting_filter.py

import re

GREETINGS = [
    "hi", "hello", "hey", "good morning",
    "good afternoon", "good evening"
]

def is_greeting(text: str) -> bool:
    clean = re.sub(r"[^\w\s]", "", text.lower()).strip()
    return clean in GREETINGS
