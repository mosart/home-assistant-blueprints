# Design: name-based preset selection in the Hue Smart Button blueprint

Date: 2026-08-14

## Problem

`controllers/hue_smart_button_rom001/hue_smart_button_rom001.yaml` asks for the
two Scene Presets preset IDs (`preset_short`, `preset_double`) as free-text raw
UUIDs. That requires opening the Scene Presets panel, applying a preset, and
reading the service call off the robot icon just to fill in one input. The goal
is to pick presets by name in the blueprint's own input UI instead.

## Investigated ceiling

Verified against current Home Assistant selector docs and the actual
`Hypfer/hass-scene_presets` integration source (cloned and inspected directly,
not recalled from memory):

- **Named dropdown — achievable.** The blueprint `select` selector supports
  `options` as `{label, value}` pairs, `mode: dropdown` (a searchable
  combobox — filters as you type), `sort`, and `custom_value: true` (lets a
  user type a raw value that isn't in the list).
- **True category grouping — not achievable.** Selectors have no
  optgroup/heading concept, and blueprint inputs are static: one input's
  `options` cannot depend on another input's value, so a "pick a category,
  then a preset within it" cascading UI is not possible in a blueprint.
  The closest real approximation is prefixing each label with its category
  (`"Cozy — Rolling hills"`) and sorting alphabetically, so same-category
  entries cluster. This is not just cosmetic: the integration's own
  `presets.json` (146 presets / 23 categories — the same data the panel
  itself reads) has one genuine name collision (`Miami`, in two categories),
  so an unprefixed list would be ambiguous for at least one entry.
- **Thumbnails — not achievable in a blueprint.** No selector renders an
  arbitrary per-option image. The only HA mechanism that shows artwork per
  option is the media-browser selector, which requires the images to be
  served by a real integration acting as a media source — i.e. writing and
  maintaining a separate `custom_component`, not expressible in blueprint
  YAML. Out of scope.
- **Real Scene Presets favourites — not readable from a blueprint.**
  Confirmed by reading the panel's frontend bundle
  (`custom_components/scene_presets/frontend/scene_presets_panel.js`):
  favourites are stored via
  `window.localStorage.getItem("scene_presets_apply_page_favorite_presets")`
  — a plain per-browser `localStorage` array, with no backing HA entity,
  attribute, or WebSocket API. A blueprint only ever sees HA
  state/entities/services, so this data is fundamentally unreachable
  server-side. Decision: do not attempt to read or approximate it. The
  dropdown's built-in type-to-filter plus the category-prefixed sort are
  enough to navigate 146 options; no separate "pinned presets" mechanism is
  being added (considered and declined, to keep the blueprint's scope small).

Two things fall out of this for free:

- **Backward compatibility.** The input *keys* (`preset_short`,
  `preset_double`) are unchanged — only their selector type changes from
  `text` to `select`. Automations already built from the blueprint store the
  resolved UUID under those keys and don't re-derive anything from the
  selector at run time, so existing automations keep working untouched.
- **Custom/local presets.** Presets a user has added locally via `userdata/`
  aren't in the upstream list. `custom_value: true` on the same select covers
  this — pick from the list, or type an ID — with no extra input field.

## Design

### 1. Blueprint input changes

- `preset_short` and `preset_double` switch from `selector: text:` to
  `selector: select:`.
- `options`: list of `{label, value}` generated from upstream
  `custom_components/scene_presets/presets.json` (the integration's own
  source of truth — cleaner than parsing the human-facing `Readme.md`).
  `label` = `"<category name> — <preset name>"`, `value` = the preset UUID.
- `mode: dropdown`, `sort: true`, `custom_value: true`.
- To avoid duplicating a ~146-entry list twice in the file: `preset_short`'s
  `selector:` value carries a YAML anchor (`&preset_selector`); `preset_double`'s
  `selector:` is an alias (`*preset_selector`). Plain YAML, resolved before HA's
  schema validation ever runs — one canonical list, two inputs, no drift
  between them possible.
- The generated `options` block is wrapped in
  `# BEGIN generated scene_presets options` / `# END generated scene_presets
  options` marker comments so the regeneration script can replace just that
  block without touching the rest of the file (surrounding comments,
  formatting, the anchor line itself).
- Check during implementation whether `custom_value` requires bumping
  `blueprint.homeassistant.min_version` above the current `2024.10.0`, and
  bump it if so.

### 2. Generator script

- `scripts/generate_scene_presets_options.py` — Python, standard library only
  (`urllib.request`, `json`), no dependencies to install.
- Fetches `presets.json` from
  `raw.githubusercontent.com/Hypfer/hass-scene_presets/master/custom_components/scene_presets/presets.json`.
- Builds category-prefixed `label`/`value` pairs, sorted, hand-formats them as
  YAML-safe scalars (double-quoted via `json.dumps`, which produces valid YAML
  string syntax — no PyYAML dependency needed for output).
- Splices the result into `hue_smart_button_rom001.yaml` between the marker
  comments described above.
- Run manually — `python3 scripts/generate_scene_presets_options.py` — review
  the diff before committing. No CI, no scheduled workflow. This matches the
  repo's existing "no support commitment" stance in `CONTRIBUTING.md`: the
  script exists so refreshing the list is a five-second command instead of
  hand-editing 146 lines, without taking on a CI workflow to maintain.

### 3. Docs

- README's "Preset IDs" section is rewritten: picking a preset by name from
  the dropdown is now the primary path; typing a custom ID (for a
  locally-added preset) is documented as the escape hatch; a one-line pointer
  to the script covers refreshing the list when upstream adds presets.
- `CONTRIBUTING.md`: no changes — the "other integrations declined" policy is
  unrelated to this change.
- `CLAUDE.md`: gets a short note on the `scripts/` convention and the
  marker-comment splice technique, since that's a non-obvious repo
  convention future sessions should know about before editing the blueprint
  by hand.

### 4. Testing

- Script sanity: run it against live upstream data; confirm the spliced file
  still parses (`python3 -c "import yaml; yaml.safe_load(open(...))"`) and
  that both `preset_short` and `preset_double` resolve to the identical
  option list (anchor/alias worked).
- Real Home Assistant import: re-import the blueprint (existing "My Home
  Assistant" badge, or paste the raw file URL), open an automation that uses
  it, and confirm:
  - the dropdown shows ~146 category-prefixed options;
  - typing filters the list live;
  - typing an arbitrary UUID and moving on keeps it as a custom value;
  - an automation created under the *previous* text-input version of the
    blueprint still loads and runs correctly after the blueprint file is
    updated (fire a `zha_event` via Developer Tools → Events with the right
    `device_id`/`command` if no physical button is available).

## Explicitly out of scope

- Thumbnails/images per option (blueprint selectors cannot do this; would
  require a separate custom_component acting as a media source).
- True category grouping / cascading category→preset selection (blueprint
  inputs are static; not achievable).
- Reading real Scene Presets favourites (browser-localStorage-only, no
  server-side access path).
- A manually-maintained "pinned presets" substitute for favourites
  (considered, declined by the user to keep scope small).
- CI automation (scheduled Action / auto-PR) for keeping the preset list in
  sync with upstream (considered, declined in favor of a manually-run
  script).
