from fastapi import FastAPI
from app.router.routers import router as wallet_router

app = FastAPI(title="Tron API")


app.include_router(wallet_router)