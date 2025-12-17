from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from config import settings
from services.markdown_report import generate_markdown, save_markdown_report
from services.trade_search import fetch_market_news
from services.ai_service import analyze_sector as ai_analyze_sector
from security.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from models.schema import SectorValidator, ALLOWED_SECTORS

app = FastAPI()

# Adding rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid sector",
            "message": "Sector not allowed. Please choose from allowed sectors.",
            "allowed_sectors": sorted(list(ALLOWED_SECTORS))
        }
    )

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
    # Validate sector
    validated_sector = SectorValidator(sector=sector).sector
    
    # Fetch market news
    raw_data = await fetch_market_news(validated_sector)
    
    # Get AI analysis
    analysis = await ai_analyze_sector(validated_sector, raw_data)
    
    # Generate markdown report
    report = generate_markdown(validated_sector, analysis)
    
    # Save report to local file
    saved_path = save_markdown_report(validated_sector, report)

    return {
        "sector": validated_sector,
        "report": report,
        "saved_to": saved_path,
        "message": f"Report saved successfully to {saved_path}"
    }

