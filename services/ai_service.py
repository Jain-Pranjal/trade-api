from google import genai
from google.genai import types
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
)

async def analyze_sector(sector: str, raw_data: str) -> str:
    prompt = f"""
You are a senior financial market analyst specializing in Indian equity markets.

Your task is to analyze the **{sector} sector in India** using the information provided
and produce a **clear, professional, and well-structured MARKDOWN report**.

### Instructions (VERY IMPORTANT):
- Output MUST be valid Markdown
- Do NOT include a title or H1 heading
- Do NOT include a disclaimer
- Use clear section headings (##, ###)
- Use bullet points where appropriate
- Keep insights concise, factual, and actionable
- Focus on **current and near-term trade opportunities**
- Avoid generic statements

---

### Required Sections (in this exact order):

## Current Market Overview
- Brief summary of the sector’s current performance in India
- Key drivers influencing the sector

## Recent News & Developments
- Important recent events, policy changes, earnings, or announcements
- Mention trends visible from recent news

## Trade Opportunities
- Short-term opportunities (days to weeks)
- Medium-term opportunities (weeks to months)
- Clearly explain the rationale behind each opportunity

## Risks & Challenges
- Market risks
- Regulatory or macroeconomic risks
- Sector-specific concerns

## Short-Term Outlook
- Expected direction of the sector in the near term
- Key indicators to watch

---

### Source Data:
{raw_data}
"""

    response = await client.aio.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=prompt,
    )

    return response.text
