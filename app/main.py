from fastapi import FastAPI, Depends, HTTPException, Header
from app.scraper import Scraper
from app.storage import JSONStorage
from app.cache import RedisCache
from app.config import STATIC_TOKEN

app = FastAPI()

def authenticate(authorization: str = Header(...)):
    if authorization != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

# cache = RedisCache()

scraper = Scraper(storage=JSONStorage(), cache=RedisCache())

@app.get("/scrape/")
def scrape(limit: int = 1, proxy: str = None, auth=Depends(authenticate)):
    result = scraper.scrape_catalog(limit, proxy)
    return result

# @app.on_event("startup")
# async def startup_event():
#     print("Application started successfully, even if Redis is unavailable.")

# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Application shutting down gracefully.")
