from .config import settings
from .exporters import save_pdf
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .models import ComicPanel, PromptRequest


def create_comic(request: PromptRequest) -> tuple[list[ComicPanel], str]:
    if len(request.story_prompt) > settings.max_story_prompt_chars:
        raise ValueError(f"Story prompt is too long; maximum is {settings.max_story_prompt_chars} characters.")

    outline = generate_outline(
        request.story_prompt,
        request.character_name,
        request.setting,
        request.tone,
        request.art_style,
    )
    if len(outline.panels) != settings.panel_count:
        raise RuntimeError(
            f"Outline model returned {len(outline.panels)} panels; expected {settings.panel_count}."
        )

    story = generate_story(outline, request.character_name, request.tone)
    image_paths = [generate_image(panel.image_prompt) for panel in outline.panels]
    layout = build_comic_layout(outline, story, image_paths)
    title = f"{request.character_name}'s Comic"
    pdf_path = save_pdf(layout, title=title)
    return layout, pdf_path
