import os


class Settings:

    # ===============================
    # APP
    # ===============================
    APP_NAME: str = "TrustCheck AI"
    VERSION: str = "2.0"

    # ===============================
    # SECURITY
    # ===============================
    API_KEY: str = os.getenv("TRUSTCHECK_API_KEY", "trustcheck-secret")

    ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://your-production-domain.com"
    ]

    # ===============================
    # RATE LIMIT
    # ===============================
    RATE_LIMIT: int = 20
    RATE_WINDOW: int = 60

    # ===============================
    # OLLAMA
    # ===============================
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct-q4_K_M")
    OLLAMA_VISION_MODEL: str = os.getenv("OLLAMA_VISION_MODEL", "llava:13b")

    # ===============================
    # THREAT INTEL
    # ===============================
    VIRUSTOTAL_API_KEY: str = os.getenv("VT_API_KEY", "")
    GOOGLE_SAFE_BROWSING_KEY: str = os.getenv("GSB_API_KEY", "")

    # ===============================
    # DATABASE
    # ===============================
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./trustcheck.db")


settings = Settings()
