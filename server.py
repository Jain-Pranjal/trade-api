from fastapi import FastAPI
from config import settings

app=FastAPI()

# Simple HTTP endpoint
@app.get("/")
async def home():
   return {
        "message": "FastAPI running 🚀",
        "environment": settings.ENVIRONMENT  # Example usage
    }



