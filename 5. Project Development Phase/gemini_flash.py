import json

from google import genai
from google.genai import types

from .config import settings
from .models import ComicOutline


def _client() -> genai.Client:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_outline(story_prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> ComicOutline:
    prompt = f"""
Create a cohesive {settings.panel_count}-panel comic outline.

Story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Requirements:
- Exactly {settings.panel_count} panels, numbered 1 through {settings.panel_count}.
- Each panel must advance the story.
- Keep the main character visually consistent across panels.
- scene_description describes composition, environment, action, lighting, and emotion.
- image_prompt is a self-contained prompt for a text-to-image model. Include the requested art style.
- Do not put dialogue in image_prompt.
""".strip()

    client = _client()
    response = client.models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
            response_schema=ComicOutline.model_json_schema(),
        ),
    )
    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty outline response.")
    try:
        return ComicOutline.model_validate_json(text)
    except Exception as exc:
        try:
            return ComicOutline.model_validate(json.loads(text))
        except Exception as json_exc:
            raise RuntimeError(f"Could not parse Gemini outline: {json_exc}") from exc
