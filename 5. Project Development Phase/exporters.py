from datetime import datetime, timezone
from pathlib import Path
import re

from fpdf import FPDF
from PIL import Image

from .config import BASE_DIR
from .models import ComicPanel

EXPORTS_DIR = BASE_DIR / "static" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _strip_for_pdf(text: str) -> str:
    # Built-in Helvetica is not Unicode-complete; replace common typography that otherwise breaks export.
    return (
        text.replace("—", "-")
        .replace("–", "-")
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("…", "...")
    )


def _safe_title(title: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", title).strip("-")[:50] or "comic"


def save_pdf(layout: list[ComicPanel], title: str = "ComicCraft Comic") -> str:
    if not layout:
        raise ValueError("Cannot export an empty comic.")

    filename = f"{_safe_title(title)}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.pdf"
    path = EXPORTS_DIR / filename

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 10, _strip_for_pdf(f"Panel {panel.panel_number}: {panel.title}"))
        pdf.ln(2)

        image_file = BASE_DIR / panel.image_path.lstrip("/").replace("/", str(Path.sep))
        if not image_file.exists():
            raise FileNotFoundError(f"Panel image not found: {image_file}")

        with Image.open(image_file) as image:
            width, height = image.size
        max_w, max_h = 180, 110
        scale = min(max_w / width, max_h / height)
        display_w, display_h = width * scale, height * scale
        x = (210 - display_w) / 2
        pdf.image(str(image_file), x=x, y=pdf.get_y(), w=display_w, h=display_h)
        pdf.ln(display_h + 5)

        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 5, _strip_for_pdf(panel.scene_description))
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 11)
        if panel.caption:
            pdf.multi_cell(0, 6, _strip_for_pdf(f"Caption: {panel.caption}"))
        if panel.dialogue:
            pdf.multi_cell(0, 6, _strip_for_pdf(f"Dialogue: {panel.dialogue}"))
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, _strip_for_pdf(f"Narration: {panel.narration}"))

    pdf.output(str(path))
    return f"/static/exports/{filename}"
