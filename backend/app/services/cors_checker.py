import requests

def check_cors_misconfig(url: str):

    try:
        response = requests.get(url, timeout=5)
        header = response.headers.get("Access-Control-Allow-Origin")

        if header == "*":
            return True
    except Exception:
        pass

    return False