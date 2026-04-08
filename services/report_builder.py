from datetime import datetime


def build_report(sector: str, analysis: str, sources: list[str]) -> str:
    timestamp = datetime.now().strftime("%d %B %Y, %I:%M %p")

    header = f"""---
**Generated:** {timestamp}
**Sector:** {sector.title()}
**Market:** India
**Disclaimer:** This report is AI-generated for informational purposes only. Not financial advice.

---

"""

    sources_section = "\n\n---\n\n## Sources\n"
    if sources:
        for i, url in enumerate(sources, 1):
            sources_section += f"{i}. {url}\n"
    else:
        sources_section += "_No sources available._\n"

    return header + analysis + sources_section