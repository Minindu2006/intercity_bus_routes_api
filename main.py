from fastapi import FastAPI
from routers import router

app = FastAPI(title="InterCity Bus Routes API")

app.include_router(router)