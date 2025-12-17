from google import genai
from config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def analyze_sector(sector: str, raw_data: str) -> str:
    prompt = f"""
You are a market analyst.

Analyze the Indian {sector} sector based on the data below.

Return a STRUCTURED MARKDOWN REPORT with:
- Overview
- Current Market Trends
- Trade Opportunities
- Risks
- Short-term Outlook

Data:
{raw_data}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )

    return response.text
