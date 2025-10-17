from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .services.dataframe import load_transactions_csv
from .api.v1 import api_v1
from . import state

@asynccontextmanager
async def lifespan(app: FastAPI):
        # resolve the CSV path & load
    try:
        state.df = load_transactions_csv(settings.csv_path)  # <-- write into module var
        print(f"[lifespan] Loaded dataframe: {len(state.df):,} rows from {settings.csv_path}")
    except Exception as e:
        print(f"[lifespan] Failed to load CSV at {settings.csv_path}: {e}")
        state.df = None
    yield

app = FastAPI(title="Finance Analyst Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1
app.include_router(api_v1, prefix="")