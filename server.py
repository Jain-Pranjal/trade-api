from fastapi import FastAPI
from config import settings
from services.markdown_report import generate_markdown, save_markdown_report
from services.trade_search import fetch_market_news
from services.ai_service import analyze_sector as ai_analyze_sector

app=FastAPI()

# Simple HTTP endpoint
@app.get("/")
async def home():
   return {
        "message": "FastAPI running 🚀",
        "environment": settings.ENVIRONMENT  
    }


@app.get("/analyze/{sector}")
async def analyze_sector(sector: str):
    # Fetch market news
    raw_data = await fetch_market_news(sector)
    
    # Get AI analysis
    analysis = await ai_analyze_sector(sector, raw_data)
    
    # Generate markdown report
    report = generate_markdown(sector, analysis)
    
    # Save report to local file
    saved_path = save_markdown_report(sector, report)

    return {
        "sector": sector,
        "report": report,
        "saved_to": saved_path,
        "message": f"Report saved successfully to {saved_path}"
    }
