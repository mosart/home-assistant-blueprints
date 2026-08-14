# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal collection of Home Assistant **automation blueprints**, each targeting one specific
device on one specific integration (not a universal/generic controller library). There is no
support commitment; see `CONTRIBUTING.md` before touching issue/PR-facing behavior.

## Structure and conventions

- Blueprints live under `controllers/<device_slug>/<device_slug>.yaml`. One directory per device.
- Each blueprint's `blueprint.source_url` must point to its own raw GitHub path
  (`https://github.com/mosart/home-assistant-blueprints/blob/main/controllers/.../<file>.yaml`) —
  update this if a blueprint is renamed or moved.
- `blueprint.homeassistant.min_version` should reflect the oldest HA release the YAML actually
  needs (e.g. features used in `trigger:`/`action:` syntax, `choose:`, template functions).
- Inputs use HA's `selector` schema (`device`, `entity`, `target`, `text`, `number`, ...). Prefer
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

## Testing changes

There is no build/lint/CI pipeline in this repo. Validate blueprint YAML by:
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
