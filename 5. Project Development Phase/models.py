from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=2000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=120)
    tone: str = Field(min_length=1, max_length=50)
    art_style: str = Field(min_length=1, max_length=80)

    @field_validator("story_prompt", "character_name", "setting", "tone", "art_style")
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be blank")
        return value


class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=120)
    scene_description: str = Field(min_length=1, max_length=1000)
    image_prompt: str = Field(min_length=1, max_length=1500)


class ComicOutline(BaseModel):
    panels: list[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int = Field(ge=1)
    narration: str = Field(min_length=1, max_length=1200)
    caption: str = Field(default="", max_length=500)
    dialogue: str = Field(default="", max_length=1200)


class ComicStory(BaseModel):
    panels: list[PanelStory]


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str
    image_path: str
    narration: str
    caption: str
    dialogue: str


class ComicResponse(BaseModel):
    title: str
    panels: list[ComicPanel]
    pdf_path: str
