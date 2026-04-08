import logging
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)
client = Groq(api_key=GROQ_API_KEY)


async def analyze_sector(sector: str, raw_data: str) -> str:
    system_prompt = """You are a senior financial analyst specializing in Indian markets.
Your job is to analyze raw market data and produce a structured, insightful report.
Always write in clear, professional English.
Format your response as clean markdown with proper headings and bullet points."""

    user_prompt = f"""Analyze the following market data for the {sector} sector in India.

Raw Data:
{raw_data}

Generate a detailed markdown report with exactly these sections:
# {sector.title()} Sector — India Market Analysis

## 1. Sector Overview
## 2. Current Market Conditions
## 3. Key Players & Companies
## 4. Trade Opportunities
## 5. Risks & Challenges
## 6. Short-Term Outlook (Next 6 Months)

Be specific, data-driven, and mention Indian market context wherever possible."""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=2048
        )
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Groq API call failed: {e}")
        raise RuntimeError("AI analysis failed. Please try again.")