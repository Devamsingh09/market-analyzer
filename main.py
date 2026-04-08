import re
import logging
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import SECTOR_PATTERN, CACHE_TTL_MINUTES
from auth.jwt_handler import create_guest_token, verify_token
from middleware.rate_limiter import is_rate_limited
from services.scraper import collect_market_data
from services.analyzer import analyze_sector
from services.report_builder import build_report
from models.schemas import TokenResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

security = HTTPBearer()

app = FastAPI(
    title="India Market Analyzer",
    description="Analyzes Indian market sectors and returns trade opportunity reports.",
    version="1.0.0"
)

cache: dict = {}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    guest_id = verify_token(token)

    if not guest_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return guest_id


@app.get("/health")
async def health():
    return {"status": "running", "message": "Market Analyzer is up!"}


@app.post("/auth/guest", response_model=TokenResponse)
async def get_guest_token():
    token, guest_id = create_guest_token()
    logger.info(f"New guest session created: {guest_id}")
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in="24 hours"
    )


@app.get("/analyze/{sector}")
async def analyze(sector: str, guest_id: str = Depends(get_current_user)):

    sector = sector.strip().lower()
    if not re.match(SECTOR_PATTERN, sector):
        raise HTTPException(
            status_code=422,
            detail="Invalid sector name. Use only letters, spaces, or hyphens (2-50 chars)."
        )

    if is_rate_limited(guest_id):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Max 5 requests per minute allowed."
        )

    if sector in cache:
        cached_entry = cache[sector]
        if datetime.now() < cached_entry["expires_at"]:
            logger.info(f"Cache hit for sector: {sector}")
            return PlainTextResponse(
                content=cached_entry["report"],
                media_type="text/markdown",
                headers={"X-Cache": "HIT"}
            )

    logger.info(f"Analyzing sector: {sector} for guest: {guest_id}")

    try:
        raw_data, sources = await collect_market_data(sector)
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise HTTPException(status_code=502, detail="Failed to collect market data.")

    try:
        analysis = await analyze_sector(sector, raw_data)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    final_report = build_report(sector, analysis, sources)

    cache[sector] = {
        "report": final_report,
        "expires_at": datetime.now() + timedelta(minutes=CACHE_TTL_MINUTES)
    }

    logger.info(f"Report generated successfully for: {sector}")

    return PlainTextResponse(
        content=final_report,
        media_type="text/markdown",
        headers={"X-Cache": "MISS"}
    )