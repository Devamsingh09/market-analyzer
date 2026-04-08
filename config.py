import os
from dotenv import load_dotenv

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-change-this")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24

RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 60

CACHE_TTL_MINUTES = 30

SECTOR_PATTERN = r"^[a-zA-Z\s\-]{2,50}$"