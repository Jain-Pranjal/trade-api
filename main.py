from server import app
import uvicorn
from config import settings


def main():
    uvicorn.run(
        "server:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    main()


