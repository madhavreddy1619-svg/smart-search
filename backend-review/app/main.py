from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.search import router as search_router

app = FastAPI(title="Smart Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)

@app.get("/")
def home():
    return {"message": "Smart Search API is running"}