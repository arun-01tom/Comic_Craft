from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import BASE_DIR, settings
from .routes import router

(BASE_DIR / "static" / "panels").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "static" / "exports").mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title=settings.app_name,
    description="AI comic story creator using Gemini and Stable Diffusion-compatible image generation.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name}
