from fastapi import FastAPI, Request,Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from google.genai.errors import ClientError, ServerError
from config import settings
from services.markdown_report import generate_markdown, save_markdown_report
from services.trade_search import fetch_market_news
from services.ai_service import analyze_sector as ai_analyze_sector
from security.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from models.schema import SectorValidator, ALLOWED_SECTORS
from security.jwt import create_access_token
from datetime import timedelta
from security.auth import get_current_user


app = FastAPI()

# Adding rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Handle validation errors (invalid sector)
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

#  Google Gemini API server errors (503, 500)
@app.exception_handler(ServerError)
async def gemini_server_error_handler(request: Request, exc: ServerError):
    error_data = exc.args[1] if len(exc.args) > 1 else {}
    error_info = error_data.get('error', {}) if isinstance(error_data, dict) else {}
    
    return JSONResponse(
        status_code=exc.status_code if hasattr(exc, 'status_code') else 503,
        content={
            "error": error_info.get('status', 'AI Service Error'),
            "message": error_info.get('message', str(exc)),
            "code": error_info.get('code', 503)
        }
    )

#  Google Gemini API client errors (400, 401, 404)
@app.exception_handler(ClientError)
async def gemini_client_error_handler(request: Request, exc: ClientError):
    error_data = exc.args[1] if len(exc.args) > 1 else {}
    error_info = error_data.get('error', {}) if isinstance(error_data, dict) else {}
    
    return JSONResponse(
        status_code=exc.status_code if hasattr(exc, 'status_code') else 400,
        content={
            "error": error_info.get('status', 'AI Service Error'),
            "message": error_info.get('message', str(exc)),
            "code": error_info.get('code', 400)
        }
    )

# Simple HTTP endpoint
@app.get("/")
async def home():
   return {
        "message": "FastAPI running 🚀",
        "environment": settings.ENVIRONMENT  
    }



@app.post("/auth/token")
async def generate_token(username: str):
    token = create_access_token(
        subject=username,
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }



@app.get("/analyze/{sector}")
@limiter.limit(f"{settings.RATE_LIMIT}/minute")
async def analyze_sector(
    request: Request,
    sector: str,
    user: str = Depends(get_current_user)
):
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

