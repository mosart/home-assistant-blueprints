#!/usr/bin/env python3
"""Regenerate the Scene Presets option list in hue_smart_button_rom001.yaml
from the upstream Hypfer/hass-scene_presets preset data. Run manually:

    python3 scripts/generate_scene_presets_options.py

Review the diff before committing.
"""
import json
import re
import urllib.request
from pathlib import Path

PRESETS_URL = (
    "https://raw.githubusercontent.com/Hypfer/hass-scene_presets/master/"
    "custom_components/scene_presets/presets.json"
)
BLUEPRINT_PATH = (
    Path(__file__).resolve().parent.parent
    / "controllers"
    / "hue_smart_button_rom001"
    / "hue_smart_button_rom001.yaml"
)
BEGIN_MARKER = "# BEGIN generated scene_presets options"
END_MARKER = "# END generated scene_presets options"


def fetch_presets_json(url=PRESETS_URL):
    with urllib.request.urlopen(url) as response:
        return json.load(response)


def build_options(data):
    categories = {category["id"]: category["name"] for category in data["categories"]}
    options = []
    for preset in data["presets"]:
        category_name = categories.get(preset["categoryId"], "Other")
        label = f"{category_name} — {preset['name']}"
        options.append({"label": label, "value": preset["id"]})
    options.sort(key=lambda option: option["label"])
    return options


def render_options_yaml(options, indent):
    pad = " " * indent
    lines = []
    for option in options:
        lines.append(f"{pad}- label: {json.dumps(option['label'])}")
        lines.append(f"{pad}  value: {json.dumps(option['value'])}")
    return "\n".join(lines)


def splice_generated_block(file_text, options, begin_marker=BEGIN_MARKER, end_marker=END_MARKER):
    pattern = re.compile(
        r"^(?P<indent>[ \t]*)"
        + re.escape(begin_marker)
        + r"\n(?P<body>.*?)^(?P=indent)"
        + re.escape(end_marker)
        + r"\s*?$",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(file_text)
    if match is None:
        raise ValueError(f"markers {begin_marker!r} / {end_marker!r} not found")

    indent = len(match.group("indent"))
    body = render_options_yaml(options, indent)
    replacement = f"{match.group('indent')}{begin_marker}\n{body}\n{match.group('indent')}{end_marker}"
    return file_text[: match.start()] + replacement + file_text[match.end() :]


def main():
    data = fetch_presets_json()
    options = build_options(data)
    file_text = BLUEPRINT_PATH.read_text()
    new_text = splice_generated_block(file_text, options)
    BLUEPRINT_PATH.write_text(new_text)
    print(f"Wrote {len(options)} options to {BLUEPRINT_PATH}")


if __name__ == "__main__":
    main()
