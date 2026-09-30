from .models import ComicOutline, ComicStory, ComicPanel


def build_comic_layout(outline: ComicOutline, story: ComicStory, image_paths: list[str]) -> list[ComicPanel]:
    stories = {item.panel_number: item for item in story.panels}
    layout: list[ComicPanel] = []

    if len(image_paths) != len(outline.panels):
        raise ValueError("Number of generated images does not match number of outline panels.")

    for outline_panel, image_path in zip(outline.panels, image_paths):
        panel_story = stories.get(outline_panel.panel_number)
        if panel_story is None:
            raise ValueError(f"Missing story content for panel {outline_panel.panel_number}.")
        layout.append(
            ComicPanel(
                panel_number=outline_panel.panel_number,
                title=outline_panel.title,
                scene_description=outline_panel.scene_description,
                image_prompt=outline_panel.image_prompt,
                image_path=image_path,
                narration=panel_story.narration,
                caption=panel_story.caption,
                dialogue=panel_story.dialogue,
            )
        )
    return layout
