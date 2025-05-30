from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import analysis, results

app = FastAPI(
    title="DigitalPulse Social Media API",
    version="1.0.0",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)
app.include_router(results.router)
