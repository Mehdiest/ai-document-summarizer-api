from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI Document Intelligence System",
    version="3.2"
)

app.include_router(router)


@app.get("/")
def root():
    return {"status": "running"}