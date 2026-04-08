import httpx
import logging
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


async def search_sector_news(sector: str) -> list[dict]:
    query = f"{sector} sector India market news 2025 trade opportunities"
    results = []

    try:
        with DDGS() as ddgs:
            hits = list(ddgs.text(query, max_results=5))
            for hit in hits:
                results.append({
                    "title": hit.get("title", ""),
                    "url": hit.get("href", ""),
                    "snippet": hit.get("body", "")
                })
    except Exception as e:
        logger.warning(f"DuckDuckGo search failed: {e}, using fallback prompt")
        # fallback — sector name hi bhejo Groq ko
        results.append({
            "title": sector,
            "url": "",
            "snippet": f"Provide market analysis for {sector} sector in India based on your training knowledge."
        })

    return results

async def scrape_page(url: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(url, follow_redirects=True)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = " ".join(p.get_text(strip=True) for p in paragraphs)
            return text[:3000]
    except Exception as e:
        logger.warning(f"Scraping failed for {url}: {e}")
        return ""


async def collect_market_data(sector: str) -> tuple[str, list[str]]:
    search_results = await search_sector_news(sector)

    raw_texts = []
    source_urls = []

    for result in search_results:
        if result["snippet"]:
            raw_texts.append(result["snippet"])

        if result["url"]:
            page_text = await scrape_page(result["url"])
            if page_text:
                raw_texts.append(page_text)
                source_urls.append(result["url"])

    combined = "\n\n".join(raw_texts)[:8000]
    return combined, source_urls