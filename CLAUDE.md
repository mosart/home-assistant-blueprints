# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal collection of Home Assistant **automation blueprints**. There is no support
commitment; see `CONTRIBUTING.md` before touching issue/PR-facing behavior.

Two categories, deliberately kept apart:

- **Device controllers** (`controllers/`) — each targets one specific device on one specific
  integration, not a universal/generic controller library. This is the original and still the
  dominant category.
- **Room behaviour** (`rooms/`) — presence/lighting logic for a room rather than a device.
  Integration-specific where it has to be (currently `scene_presets`), but not tied to one
  piece of hardware. Keep this category small; it exists because presence logic genuinely
  isn't expressible as a device controller.

## Structure and conventions

- Device controllers live under `controllers/<device_slug>/<device_slug>.yaml`. One directory
  per device. Room-behaviour blueprints live under `rooms/<behaviour_slug>/<behaviour_slug>.yaml`.
- Each blueprint's `blueprint.source_url` must point to its own raw GitHub path
  (`https://github.com/mosart/home-assistant-blueprints/blob/main/controllers/.../<file>.yaml`) —
  update this if a blueprint is renamed or moved.
- `blueprint.homeassistant.min_version` should reflect the oldest HA release the YAML actually
  needs (e.g. features used in `trigger:`/`action:` syntax, `choose:`, template functions).
- Inputs use HA's `selector` schema (`device`, `entity`, `target`, `text`, `number`, `select`, ...). Prefer
  `selector: device: filter: [integration: ..., model: ...]` for device pickers so the blueprint
  only matches the intended hardware.
- `triggers` use `id:` to tag each event trigger, and `actions` branch on
  `condition: trigger, id: <id>` inside a `choose:` block — this is the pattern all blueprints in
  this repo follow for multi-event device controllers (short press / double press / hold / release).
- Comments in the YAML explain *device/firmware quirks* (e.g. why a trigger fires once vs.
  repeatedly, why a helper is needed to track state HA can't read from the device) — keep this
  style when adding new blueprints or editing existing ones.
- README.md documents each blueprint's behaviour, requirements, and a "My Home Assistant" import
  badge; keep the README in sync when adding, renaming, or removing a blueprint.

### Generated content

- Three files share one generated `scene_presets` option list each — the
  `preset_short`/`preset_double` inputs in
  `controllers/hue_smart_button_rom001/hue_smart_button_rom001.yaml`, the 8
  `button_N_short`/`button_N_double` inputs in
  `controllers/hue_tap_dial_rdm002/hue_tap_dial_rdm002.yaml`, and the 3
  `preset_day`/`preset_evening`/`preset_night` inputs in
  `rooms/presence_lighting/presence_lighting.yaml`. The lists are
  generated (not hand-maintained) from the same upstream fetch. Each file's
  list lives between its own `# BEGIN generated scene_presets options` /
  `# END generated scene_presets options` marker comments. Regenerate both
  with `python3 scripts/generate_scene_presets_options.py` (stdlib-only, no
  dependencies) rather than hand-editing the options — the script only
  touches the text strictly between each file's own markers, so anything
  outside them (including the surrounding YAML anchor) is untouched.
  Adding a further blueprint that reuses this list means adding its path to
  `BLUEPRINT_PATHS` in the script.
- `scripts/*.py` have matching `scripts/test_*.py` files, run with
  `python3 -m unittest discover -s scripts -p "test_*.py"`. No network calls
  in tests — network-dependent code (`fetch_presets_json`) is exercised
  manually when the script is actually run, not under test.

## Testing changes

There is no build/lint/CI pipeline in this repo (the `scripts/` generator has
its own `unittest` suite — see "Generated content" above for the run
command). Validate blueprint YAML by:
- Checking it's valid YAML and matches Home Assistant's blueprint schema (top-level `blueprint:`,
  `triggers`/`conditions`/`actions` or legacy `trigger`/`condition`/`action` keys).
- Importing it into a real Home Assistant instance (Settings → Automations → Blueprints → Import)
  and exercising it against the actual hardware — this repo's bug reports are expected to include
  `zha_event` output and automation traces, so changes should be validated the same way.

## Contribution norms (from CONTRIBUTING.md)

- Keep PRs small and focused on one blueprint/behavior; no whole-file cosmetic reformatting.
- Do not add support for other integrations (e.g. Zigbee2MQTT, deCONZ) to an existing
  single-integration blueprint — that's expected to be declined upstream. Forking is the suggested
  path for unsupported devices/integrations.
- License is EUPL-1.2 (`SPDX-License-Identifier: EUPL-1.2`); contributions are accepted under the
  same license.
