# Name-Based Preset Selection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Hue Smart Button blueprint's free-text preset-UUID inputs with a searchable, category-labeled dropdown generated from the Scene Presets integration's own data, while keeping a custom-value escape hatch and full backward compatibility.

**Architecture:** A standalone, stdlib-only Python script (`scripts/generate_scene_presets_options.py`) fetches `Hypfer/hass-scene_presets`' `presets.json`, builds `{label, value}` option pairs, and splices them into a marker-delimited block inside the blueprint YAML. The blueprint's two preset inputs share that option list via a YAML anchor/alias so it's defined once.

**Tech Stack:** Python 3 standard library only (`json`, `re`, `urllib.request`, `unittest`, `pathlib`). No new runtime or test dependencies for the repo.

## Global Constraints

- No dependencies beyond the Python standard library (from the design doc's "stdlib only" decision — this is a hobby repo with no existing package manifest).
- `blueprint.homeassistant.min_version` stays `2024.10.0` — the `select` selector's `custom_value` property shipped in HA core PR home-assistant/core#68952 (merged 2022-03-31, released in HA 2022.5), well below the current floor. Verified directly against the PR; do not bump `min_version` for this change.
- Blueprint input *keys* (`preset_short`, `preset_double`) must not change, to preserve automations already built from the current text-input version.
- The generator script only ever rewrites the text strictly between the `# BEGIN generated scene_presets options` / `# END generated scene_presets options` marker lines — it must not reformat or touch the rest of the file.
- All option labels/values are rendered via `json.dumps(...)` (valid YAML double-quoted scalar syntax) — no hand-rolled quoting/escaping.
- Everything in the repo is in English (existing repo convention).

---

## File Structure

- **Create** `scripts/generate_scene_presets_options.py` — fetches upstream preset data, builds sorted category-prefixed options, splices them into the blueprint file. Contains the CLI entry point.
- **Create** `scripts/test_generate_scene_presets_options.py` — `unittest` tests for the three pure functions (`build_options`, `render_options_yaml`, `splice_generated_block`); no network access.
- **Modify** `controllers/hue_smart_button_rom001/hue_smart_button_rom001.yaml` — `preset_short`/`preset_double` inputs switch from `text` to `select` selectors sharing one anchored option list.
- **Modify** `README.md` — rewrite the "Preset IDs" section for the new dropdown UI.
- **Modify** `CLAUDE.md` — document the `scripts/` convention and the marker-comment splice technique.

---

### Task 1: Generator script — pure functions, test-first

**Files:**
- Create: `scripts/generate_scene_presets_options.py`
- Test: `scripts/test_generate_scene_presets_options.py`

**Interfaces:**
- Produces (consumed by Task 2 and by the script's own `main()` in this task):
  - `build_options(data: dict) -> list[dict]` — `data` is the parsed upstream JSON (`{"categories": [{"id": str, "name": str}, ...], "presets": [{"id": str, "categoryId": str, "name": str, ...}, ...]}`). Returns a list of `{"label": str, "value": str}` dicts, sorted by `label`.
  - `render_options_yaml(options: list[dict], indent: int) -> str` — renders a YAML block-sequence of `{label, value}` mappings, each line indented by `indent` spaces, joined with `"\n"`, no leading/trailing newline.
  - `splice_generated_block(file_text: str, options: list[dict], begin_marker: str = BEGIN_MARKER, end_marker: str = END_MARKER) -> str` — replaces the text strictly between the begin/end marker lines in `file_text` with `render_options_yaml(options, indent=<indent of the begin marker line>)`. Raises `ValueError` if either marker is missing.

- [ ] **Step 1: Write the failing tests**

Create `scripts/test_generate_scene_presets_options.py`:

```python
import unittest

from generate_scene_presets_options import (
    build_options,
    render_options_yaml,
    splice_generated_block,
)


class BuildOptionsTests(unittest.TestCase):
    def test_labels_are_category_prefixed_and_sorted(self):
        data = {
            "categories": [
                {"id": "cat-cozy", "name": "Cozy"},
                {"id": "cat-party", "name": "Party vibes"},
            ],
            "presets": [
                {"id": "id-warm", "categoryId": "cat-cozy", "name": "Warm embrace"},
                {"id": "id-miami-1", "categoryId": "cat-party", "name": "Miami"},
                {"id": "id-miami-2", "categoryId": "cat-cozy", "name": "Miami"},
            ],
        }

        options = build_options(data)

        self.assertEqual(
            options,
            [
                {"label": "Cozy — Miami", "value": "id-miami-2"},
                {"label": "Cozy — Warm embrace", "value": "id-warm"},
                {"label": "Party vibes — Miami", "value": "id-miami-1"},
            ],
        )

    def test_unknown_category_falls_back_to_other(self):
        data = {
            "categories": [],
            "presets": [{"id": "id-x", "categoryId": "missing", "name": "X"}],
        }

        options = build_options(data)

        self.assertEqual(options, [{"label": "Other — X", "value": "id-x"}])


class RenderOptionsYamlTests(unittest.TestCase):
    def test_renders_quoted_label_value_pairs_at_given_indent(self):
        options = [
            {"label": 'Cozy — "Warm" embrace', "value": "abc-123"},
            {"label": "Party vibes — Miami", "value": "def-456"},
        ]

        rendered = render_options_yaml(options, indent=4)

        self.assertEqual(
            rendered,
            '    - label: "Cozy \\u2014 \\"Warm\\" embrace"\n'
            '      value: "abc-123"\n'
            '    - label: "Party vibes \\u2014 Miami"\n'
            '      value: "def-456"',
        )


class SpliceGeneratedBlockTests(unittest.TestCase):
    def test_replaces_content_between_markers_preserving_indent(self):
        file_text = (
            "before\n"
            "    options:\n"
            "      # BEGIN generated scene_presets options\n"
            "      - label: \"stale\"\n"
            "        value: \"stale-id\"\n"
            "      # END generated scene_presets options\n"
            "after\n"
        )
        options = [{"label": "Cozy — Warm embrace", "value": "id-warm"}]

        result = splice_generated_block(file_text, options)

        self.assertEqual(
            result,
            "before\n"
            "    options:\n"
            "      # BEGIN generated scene_presets options\n"
            '      - label: "Cozy \\u2014 Warm embrace"\n'
            '        value: "id-warm"\n'
            "      # END generated scene_presets options\n"
            "after\n",
        )

    def test_handles_empty_body_between_adjacent_markers(self):
        # This is the state Task 2 hits on the first run: the markers are
        # scaffolded in with nothing between them yet.
        file_text = (
            "before\n"
            "    options:\n"
            "      # BEGIN generated scene_presets options\n"
            "      # END generated scene_presets options\n"
            "after\n"
        )
        options = [{"label": "Cozy — Warm embrace", "value": "id-warm"}]

        result = splice_generated_block(file_text, options)

        self.assertEqual(
            result,
            "before\n"
            "    options:\n"
            "      # BEGIN generated scene_presets options\n"
            '      - label: "Cozy \\u2014 Warm embrace"\n'
            '        value: "id-warm"\n'
            "      # END generated scene_presets options\n"
            "after\n",
        )

    def test_missing_markers_raises_value_error(self):
        with self.assertRaises(ValueError):
            splice_generated_block("no markers here", [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s scripts -p "test_*.py" -v`
Expected: `ModuleNotFoundError: No module named 'generate_scene_presets_options'` (the module doesn't exist yet).

- [ ] **Step 3: Write the minimal implementation**

Create `scripts/generate_scene_presets_options.py`:

```python
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s scripts -p "test_*.py" -v`
Expected: `OK` with 6 tests run (2 in `BuildOptionsTests`, 1 in `RenderOptionsYamlTests`, 3 in `SpliceGeneratedBlockTests`).

If a `SpliceGeneratedBlockTests` case fails on whitespace, check that the end-marker line's leading whitespace exactly matches the begin-marker line's — `splice_generated_block` requires both markers at the same indent (via the `(?P=indent)` backreference).

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_scene_presets_options.py scripts/test_generate_scene_presets_options.py
git commit -m "Add scene_presets option-list generator script

Standalone, stdlib-only script that fetches Hypfer/hass-scene_presets'
presets.json and splices category-labeled {label, value} options into
a marker-delimited block. Run manually; no CI wiring by design."
```

---

### Task 2: Wire the blueprint's preset inputs to the generated option list

**Files:**
- Modify: `controllers/hue_smart_button_rom001/hue_smart_button_rom001.yaml:52-63`

**Interfaces:**
- Consumes: `scripts/generate_scene_presets_options.py`'s `main()` (Task 1) — run as a subprocess/CLI, not imported.

- [ ] **Step 1: Replace the `preset_short`/`preset_double` input block**

In `controllers/hue_smart_button_rom001/hue_smart_button_rom001.yaml`, replace lines 52-63:

```yaml
    preset_short:
      name: Preset for short press
      description: >-
        Scene Presets preset ID. IDs are listed in the integration's docs, or use
        the robot icon in the Scene Presets panel to read one off.
      selector:
        text:
    preset_double:
      name: Preset for double press
      description: Scene Presets preset ID.
      selector:
        text:
```

with:

```yaml
    preset_short:
      name: Preset for short press
      description: >-
        Pick a preset by name (categories match the Scene Presets panel).
        To use a preset that isn't listed — for example one added locally
        via userdata/ — type its ID directly instead of picking an option.
      selector: &preset_selector
        select:
          mode: dropdown
          sort: true
          custom_value: true
          options:
            # BEGIN generated scene_presets options
            # END generated scene_presets options
    preset_double:
      name: Preset for double press
      description: Same preset list as above.
      selector: *preset_selector
```

This leaves `options:` with only marker comments between them — not yet valid against the HA blueprint schema (an empty `select.options`). That's expected; Step 2 fixes it before anything is committed.

- [ ] **Step 2: Run the generator against the real file**

Run: `python3 scripts/generate_scene_presets_options.py`
Expected output: `Wrote 146 options to .../controllers/hue_smart_button_rom001/hue_smart_button_rom001.yaml` (the count may differ slightly if upstream has changed since this plan was written — that's fine, it's meant to track upstream).

- [ ] **Step 3: Verify the file is valid YAML and the anchor/alias resolved identically**

Run:
```bash
python3 - <<'PYEOF'
import yaml

# The blueprint uses HA's custom `!input xyz` tag elsewhere (triggers/actions
# reference `!input button`, `!input lights`, etc). Plain yaml.safe_load()
# doesn't know that tag and raises ConstructorError, so register a loader
# that treats it as an opaque scalar — good enough for this structural check.
class BlueprintLoader(yaml.SafeLoader):
    pass

BlueprintLoader.add_constructor(
    "!input", lambda loader, node: loader.construct_scalar(node)
)

with open("controllers/hue_smart_button_rom001/hue_smart_button_rom001.yaml") as f:
    data = yaml.load(f, Loader=BlueprintLoader)

short_opts = data["blueprint"]["input"]["preset_short"]["selector"]["select"]["options"]
double_opts = data["blueprint"]["input"]["preset_double"]["selector"]["select"]["options"]

assert short_opts is double_opts, "anchor/alias did not resolve to the same list object"
assert len(short_opts) > 100, f"expected >100 options, got {len(short_opts)}"
assert all(set(o) == {"label", "value"} for o in short_opts)
print(f"OK: {len(short_opts)} options, shared between both inputs")
PYEOF
```
Expected: `OK: <N> options, shared between both inputs` with no `AssertionError` and no `ConstructorError`.

(If PyYAML isn't installed: `pip install --user pyyaml`, or `pip install --user --break-system-packages pyyaml` if the environment is externally managed, e.g. Debian/Ubuntu with PEP 668. It's a one-off verification tool, not a project dependency, so it doesn't need adding anywhere.)

- [ ] **Step 4: Commit**

```bash
git add controllers/hue_smart_button_rom001/hue_smart_button_rom001.yaml
git commit -m "Switch preset inputs to a name-based select with custom-value escape hatch

preset_short/preset_double now offer a searchable dropdown of Scene
Presets, labeled '<category> — <name>' and generated from upstream
presets.json. custom_value stays enabled so a locally-added preset ID
can still be typed directly. Input keys are unchanged, so automations
built from the previous text-input version keep working."
```

---

### Task 3: Update README's preset documentation

**Files:**
- Modify: `README.md:33-38`

- [ ] **Step 1: Replace the "Preset IDs" section**

Replace:

```markdown
#### Preset IDs

The two preset inputs expect Scene Presets IDs, not names. You can find them in
the [preset overview](https://github.com/Hypfer/hass-scene_presets/blob/master/custom_components/scene_presets/assets/Readme.md),
or apply a preset in the Scene Presets panel and click the robot icon in the top
right to read off the exact service call.
```

with:

```markdown
#### Choosing presets

The two preset inputs are a searchable dropdown, labeled the same way the
Scene Presets panel groups them (`Category — Preset name`) — type to filter.

If you've added a preset locally (via `userdata/`) it won't be in the list;
type its ID directly into the field instead of picking an option, and it will
be used as-is.

The dropdown is generated from upstream preset data by
`scripts/generate_scene_presets_options.py`. If Hypfer/hass-scene_presets adds
new presets and you want them reflected here, run
`python3 scripts/generate_scene_presets_options.py` and review the diff.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "Update README for name-based preset selection"
```

---

### Task 4: Document the scripts/ convention in CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add a "Generated content" subsection**

In `CLAUDE.md`, under the existing "## Structure and conventions" section, add (after the existing bullet list, before "## Testing changes"):

```markdown
### Generated content

- `controllers/hue_smart_button_rom001/hue_smart_button_rom001.yaml`'s
  `preset_short`/`preset_double` option list is generated, not hand-maintained.
  It lives between `# BEGIN generated scene_presets options` / `# END generated
  scene_presets options` marker comments. Regenerate it with
  `python3 scripts/generate_scene_presets_options.py` (stdlib-only, no
  dependencies) rather than hand-editing the options — the script only
  touches the text strictly between those markers, so anything outside them
  (including the surrounding YAML anchor) is untouched.
- `scripts/*.py` have matching `scripts/test_*.py` files, run with
  `python3 -m unittest discover -s scripts -p "test_*.py"`. No network calls
  in tests — network-dependent code (`fetch_presets_json`) is exercised
  manually when the script is actually run, not under test.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "Document the scene_presets generator script convention"
```

---

### Task 5: Manual verification in a real Home Assistant instance

**Files:** none (verification only)

- [ ] **Step 1: Re-import the blueprint**

In Home Assistant: **Settings → Automations & scenes → Blueprints → Import Blueprint**, paste the raw URL of your branch's `hue_smart_button_rom001.yaml` (or use the README's "My Home Assistant" badge once merged to `main`). If you already have this blueprint imported, HA will offer to update it in place — accept.

- [ ] **Step 2: Confirm the dropdown**

Open **Settings → Automations & scenes → Blueprints**, click the blueprint's "Create Automation", and check the "Preset for short press" field:
- It renders as a searchable combobox (not a plain text box).
- Typing e.g. `cozy` filters to only `Cozy — ...` options.
- Options are labeled `<Category> — <Preset name>`.

- [ ] **Step 3: Confirm the custom-value escape hatch**

In the same field, type a UUID that is *not* in the list (any random-looking string works for this check, e.g. `test-custom-id`) and move focus away. Confirm the field keeps that typed value rather than clearing or rejecting it.

- [ ] **Step 4: Confirm backward compatibility with an existing automation**

If you have an automation already built from the *previous* (text-input) version of this blueprint: after re-importing the updated blueprint, open that automation and confirm its stored preset values still show correctly (as the dropdown's matching named option, or as a custom value if the stored UUID isn't in the generated list), and that triggering it still applies the right preset. If you don't have a physical button handy, trigger it via **Developer Tools → Events**: listen to `zha_event`, or directly fire one with the automation's expected `device_id` and `command` (`on_short_release` / `on_double_press` / `step` / `on_long_release`) to exercise the relevant branch.

- [ ] **Step 5: Note results**

No commit for this task — it's verification only. If any check fails, stop and report back before proceeding further; do not paper over a failed check by adjusting the test instead.

---

## Self-Review Notes

- **Spec coverage:** Ceiling investigation (Task 0, already done in the design doc — no code task needed), select selector with category-prefixed labels + custom_value (Task 2), YAML anchor/alias dedup (Task 2), marker-comment splice (Task 1 + 2), manually-run generator script (Task 1), README update (Task 3), CLAUDE.md update (Task 4), backward-compat + real-HA testing (Task 5). No pinned-favorites task — explicitly declined in the design doc.
- **Placeholder scan:** none found; the `min_version` question flagged as "check during implementation" in the design doc is resolved above in Global Constraints (no bump needed, cited PR).
- **Type consistency:** `build_options` → `list[dict]` with `label`/`value` string keys is used consistently by `render_options_yaml` and by Task 2's Step 3 verification script; `splice_generated_block`'s marker constants (`BEGIN_MARKER`/`END_MARKER`) match the literal marker text used in Task 2's YAML edit.
