from pathlib import Path
from PIL import Image

from app.exporters import save_pdf
from app.layout_builder import build_comic_layout
from app.models import ComicOutline, ComicStory, PanelOutline, PanelStory


def test_layout_and_pdf(tmp_path, monkeypatch):
    from app import exporters
    monkeypatch.setattr(exporters, "EXPORTS_DIR", tmp_path)
    image_dir = Path(__file__).resolve().parents[1] / "static" / "panels"
    image_dir.mkdir(parents=True, exist_ok=True)
    image_file = image_dir / "test-panel.png"
    Image.new("RGB", (200, 200), "white").save(image_file)

    outline = ComicOutline(panels=[PanelOutline(panel_number=1, title="Start", scene_description="A fox enters.", image_prompt="fox")])
    story = ComicStory(panels=[PanelStory(panel_number=1, narration="Ember takes a step.", caption="Dawn", dialogue="Hello!")])
    layout = build_comic_layout(outline, story, ["/static/panels/test-panel.png"])
    assert layout[0].title == "Start"

    pdf_path = save_pdf(layout, "Test Comic")
    assert (tmp_path / Path(pdf_path).name).exists()
    image_file.unlink()
