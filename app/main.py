from fastapi import FastAPI
from api.routes import router as api_router
from utils.logger import setup_logging
from config.settings import settings

app = FastAPI(title="BABEL App")

setup_logging()

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to BABEL App"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)