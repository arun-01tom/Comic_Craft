from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .config import BASE_DIR, settings
from .image_generator import generate_image
from .models import PromptRequest
from .services import create_comic

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def _error_message(exc: Exception) -> str:
    return str(exc) if str(exc) else exc.__class__.__name__


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"settings": settings})


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        payload = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        layout, pdf_path = create_comic(payload)
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={"layout": layout, "pdf_path": pdf_path, "character_name": payload.character_name},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"settings": settings, "error": _error_message(exc)},
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        layout, pdf_path = create_comic(payload)
        return {
            "title": f"{payload.character_name}'s Comic",
            "panels": [panel.model_dump() for panel in layout],
            "pdf_path": pdf_path,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=_error_message(exc)) from exc


@router.post("/test-image")
async def test_image(prompt: str = Form(...)):
    try:
        return {"image_path": generate_image(prompt)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=_error_message(exc)) from exc


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf: str | None = None):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_path": pdf},
    )
