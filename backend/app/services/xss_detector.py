import re

def detect_xss_payload(message: str):

    patterns = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"onerror=",
        r"onload=",
        r"document\.cookie",
    ]

    for pattern in patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return True

    return False