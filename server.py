from fastapi import FastAPI, Request
from config import settings
from services.markdown_report import generate_markdown, save_markdown_report
from services.trade_search import fetch_market_news
from services.ai_service import analyze_sector as ai_analyze_sector
from security.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# Adding rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Simple HTTP endpoint
@app.get("/")
async def home():
   return {
        "message": "FastAPI running 🚀",
        "environment": settings.ENVIRONMENT  
    }


@app.get("/analyze/{sector}")
@limiter.limit(f"{settings.RATE_LIMIT}/minute")
async def analyze_sector(request: Request, sector: str):
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
