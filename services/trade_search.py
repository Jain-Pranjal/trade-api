'''
This module handles fetching market news for a given sector.
Using the DuckDuckGo search as a simple example.
'''
import httpx

async def fetch_market_news(sector: str):
    query = f"India {sector} sector market news"
    url = "https://duckduckgo.com/?q=" + query

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return response.text[:2000]  # trim content
