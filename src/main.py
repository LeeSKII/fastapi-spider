from fastapi import FastAPI
from spider.weather import router as weather_router

app = FastAPI()

app.include_router(weather_router.router)

@app.get('/spider')
async def spider():
    return {"message": "Hello, Spider!"}

