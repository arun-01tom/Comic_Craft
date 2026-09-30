import json

from google import genai
from google.genai import types

from .config import settings
from .models import ComicOutline, ComicStory


def _client() -> genai.Client:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_story(outline: ComicOutline, character_name: str, tone: str) -> ComicStory:
    outline_json = outline.model_dump_json(indent=2)
    prompt = f"""
Expand this comic outline into polished comic narration, captions, and dialogue.

Main character: {character_name}
Tone: {tone}
Outline:
{outline_json}

Requirements:
- Return exactly one story object for every outline panel, preserving panel numbers.
- narration should be concise but vivid and suitable for a comic page.
- caption can describe time, place, atmosphere, or sound effects.
- dialogue should contain only spoken lines and character names when useful.
- Do not invent extra panels.
""".strip()

    client = _client()
    response = client.models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.85,
            response_mime_type="application/json",
            response_schema=ComicStory.model_json_schema(),
        ),
    )
    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty story response.")
    try:
        return ComicStory.model_validate_json(text)
    except Exception as exc:
        try:
            return ComicStory.model_validate(json.loads(text))
        except Exception as json_exc:
            raise RuntimeError(f"Could not parse Gemini story: {json_exc}") from exc
