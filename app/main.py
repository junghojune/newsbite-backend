from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.health import router as health_router
from .core.config import settings


app = FastAPI(title="NewsBite API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])  # 간단한 루트 응답
def read_root():
    return {"success": True, "data": {"service": "newsbite", "version": app.version}}


app.include_router(health_router)

