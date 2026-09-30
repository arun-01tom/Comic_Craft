# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI + Jinja2 web app that turns a story idea into a five-panel comic. It follows the supplied project documentation: structured outline generation, detailed narration/dialogue, image generation, panel layout, PDF export, browser preview, and JSON API access.

## Architecture

- **FastAPI**: routing, validation, API, HTML rendering.
- **Gemini**: outline + story generation using the current Google Gen AI Python SDK. Model IDs are configurable via `.env`.
- **Hugging Face**: default image backend through `InferenceClient`, with a Stable Diffusion model configurable via `HF_IMAGE_MODEL`.
- **Local Diffusers**: optional image backend for users with suitable GPU/VRAM.
- **FPDF2 + Pillow**: PDF assembly and image handling.

The original document names Gemini 1.5 Flash/Pro and `runwayml/stable-diffusion-v1-5`. Those model identifiers are historical. This implementation keeps the same roles while making model IDs configurable and uses current SDKs/defaults. See the project documentation and the current provider docs in the final response.

## Requirements

- Python 3.11+ recommended.
- A Gemini API key.
- A Hugging Face token for the default `hf_api` image backend.
- Internet access for hosted inference.
- For `local_diffusers`, a compatible PyTorch installation and enough RAM/VRAM for the selected diffusion model.

## Quick start (Windows / VS Code)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add your keys:

```env
GEMINI_API_KEY=...
HF_TOKEN=...
```

Then run:

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs.

## Image backends

Default:

```env
IMAGE_PROVIDER=hf_api
HF_IMAGE_MODEL=stabilityai/stable-diffusion-xl-base-1.0
```

If your Hugging Face account/provider does not serve that model, choose another text-to-image Stable Diffusion-compatible model available to your account/provider.

For local Diffusers:

```powershell
pip install -r requirements-diffusers.txt
```

and set:

```env
IMAGE_PROVIDER=local_diffusers
LOCAL_IMAGE_MODEL=runwayml/stable-diffusion-v1-5
```

## API example

```powershell
curl -X POST http://127.0.0.1:8000/generate-comic/json `
  -H "Content-Type: application/json" `
  -d '{"story_prompt":"A brave fox exploring an enchanted forest","character_name":"Ember","setting":"enchanted forest","tone":"dramatic","art_style":"comic book"}'
```

The response contains the five-panel layout and a PDF URL.

## Tests

Run unit tests without calling external AI services:

```powershell
pytest -q
```

The test suite uses mocked AI/image services and validates the PDF/layout pipeline and API schema.

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── static/
│   ├── css/style.css
│   ├── panels/.gitkeep
│   └── exports/.gitkeep
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── tests/
│   ├── conftest.py
│   ├── test_layout.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-diffusers.txt
└── README.md
```
