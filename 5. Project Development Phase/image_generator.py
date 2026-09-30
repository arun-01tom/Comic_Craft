from pathlib import Path
import re
from uuid import uuid4

from PIL import Image

from .config import BASE_DIR, settings

PANELS_DIR = BASE_DIR / "static" / "panels"
PANELS_DIR.mkdir(parents=True, exist_ok=True)


def _safe_stem(prompt: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", prompt.lower()).strip("-")
    return (cleaned[:60] or "panel") + f"-{uuid4().hex[:8]}"


def _generate_hf(prompt: str) -> Image.Image:
    if not settings.hf_token:
        raise RuntimeError("HF_TOKEN is not configured. Add it to .env or use local_diffusers.")
    try:
        from huggingface_hub import InferenceClient
    except ImportError as exc:
        raise RuntimeError("huggingface-hub is not installed.") from exc

    client = InferenceClient(api_key=settings.hf_token)
    image = client.text_to_image(
        prompt=prompt,
        model=settings.hf_image_model,
        width=settings.image_width,
        height=settings.image_height,
        num_inference_steps=settings.image_steps,
    )
    return image.convert("RGB")


_local_pipe = None


def _generate_local(prompt: str) -> Image.Image:
    global _local_pipe
    try:
        import torch
        from diffusers import DiffusionPipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local Diffusers backend is not installed. Run: pip install -r requirements-diffusers.txt"
        ) from exc

    if _local_pipe is None:
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        _local_pipe = DiffusionPipeline.from_pretrained(settings.local_image_model, torch_dtype=dtype)
        if torch.cuda.is_available():
            _local_pipe = _local_pipe.to("cuda")
        else:
            _local_pipe = _local_pipe.to("cpu")

    result = _local_pipe(
        prompt,
        num_inference_steps=settings.image_steps,
        width=settings.image_width,
        height=settings.image_height,
    )
    return result.images[0].convert("RGB")


def generate_image(prompt: str) -> str:
    enhanced = (
        f"{prompt}. Clean comic panel composition, readable focal subject, strong visual storytelling, "
        "no text, no watermark, no logo."
    )
    if settings.image_provider.lower() == "local_diffusers":
        image = _generate_local(enhanced)
    elif settings.image_provider.lower() == "hf_api":
        image = _generate_hf(enhanced)
    else:
        raise RuntimeError(f"Unsupported IMAGE_PROVIDER: {settings.image_provider}")

    filename = _safe_stem(prompt) + ".png"
    path = PANELS_DIR / filename
    image.save(path, format="PNG", optimize=True)
    return f"/static/panels/{filename}"
