---
name: presence-lighting-blueprint
description: Design, behaviour and pitfalls of rooms/presence_lighting/presence_lighting.yaml and how the owner's six room automations are configured. Use before editing that blueprint or its automations.
---

# `[mosart] Presence lighting with scene memory`

File: `rooms/presence_lighting/presence_lighting.yaml` (≈2000 lines). Live in HA
as `mosart/presence_lighting.yaml`, used by six automations: Keuken, Hal,
Voordeurlamp, Zolder, Trappenhuis, Woonkamer. `mode: restart`.

## Settings layout (keep it)
Sections, all `collapsed: true`: **Room** (`where`), **Daytime**, **Evening**,
**Night**, **Dim & switch-off**, **Transitions**, **Media**, **Advanced**.
Slot fields are named *When · / What · / How ·* and are in the same order in each
slot. Help texts are one line; long explanations live in the README and each
section links to it. **Input keys are a public API** — the owner's automations
store them; never rename or remove one without migrating every automation.

## Behaviour (what the README promises)
- Slot = Daytime / Evening / Night. *What*: scene preset, `color` (colour
  picker, `*_light_colour`), `white` (`*_white_kelvin`), or `off`. Colour and
  white always use the slot's brightness. Scene presets get brightness unless
  "keep the preset's own brightness".
- *On motion in a dark room* (`*_preset_source`): `time_slot` | `button` (last
  remote preset from `input_text.<room>_laatste_preset`) | `last` (snapshot
  scene `scene.presence_snapshot_<room>` taken when the room went quiet).
- Motion in an already-lit room: with source `last` + slot brightness only the
  brightness follows the slot; otherwise nothing. With
  `force_preset_on_motion` the slot's light is applied every motion.
- **Lights changed by hand during the current slot are left alone** until the
  next slot (`last_updated < slot_started_at`).
- Slow lit transition (`lit_transition`, ≤5 min) is not restarted by further
  motion: ZHA lights already report the target brightness (±2 tolerance).
- Quiet → snapshot + warning dim (`dim_brightness_pct`, relative step) →
  switch off after `no_motion_off_after`; `input_boolean` dim flag marks it.
- **Slot start** (`*_at_start`, default `ease`, `*_start_transition` 0–300 s):
  lights that are *on* at the boundary ease to the new slot; lights that are
  *off* stay off. The blueprint must **never** switch lights on in an empty
  room (that is the owner's holiday automation). Morning boundary also clears
  the remote-preset memory.
- Missed switch-off safety net: trigger `missed_off` re-checks every minute
  (template with `now()`); it exists because reloading/saving the automation
  loses the running countdown. It only fires on the moment a room *becomes*
  overdue.
- Media: players listed in `media_players_on` count as in use while on (capped
  by `media_hold_limit`, default 2 h, because a Chromecast can sit on `paused`
  all night); `media_players_ignore` removes mirrors that keep saying
  `playing`; ignored players must not restart the run (top-level condition).
- `lights_exclude` removes lights from the area-derived set (e.g. the kiosk
  tablet screen). `lights` (override) wins over it.

## Pitfalls found the hard way
- `enabled:` on a trigger/condition **cannot see blueprint inputs** (limited
  template). The sunrise/sunset toggles silently never worked that way. Slots
  are now decided by `is_night` / `is_evening` templates in `variables:`; both
  boundary triggers always attach and a top-level condition filters them.
- `variables:` render top to bottom; referencing a later name gives Undefined
  (e.g. "Preset '[' not found"). Reorder, don't default.
- Triggers are rendered before `variables:` exist: pass inputs via
  `trigger_variables:` (limited templates, no `states()`).
- Regex in blueprint YAML templates: `'light\.'` in a `>-` scalar is right;
  generating the file from Python needs care that backslashes aren't doubled.
- `motion.detected` / `occupancy.detected` ignore `unavailable → on`; the state
  trigger over `recovery_sensors` catches it (`from: [unavailable, unknown]`).
- Anchors (`&x`/`*x`) share a whole step across slots — change the anchor, not
  the aliases. `force_apply_slot`, `ease_to_slot`, `lit_brightness_sync/apply`,
  `turn_off_sequence`.
- `apply_preset` for `off` is replaced by `light.turn_off`; presets with brightness
  `-1` mean "keep own".
- A scene preset id value `off`, `color`, `white` are special strings in the
  dropdown, not preset ids.
- The `scene_presets` options block is generated (see CLAUDE.md).

## How the six rooms are set (at time of writing)
Keuken & Woonkamer & Trappenhuis & Zolder: `force_preset_on_motion: true` (bulbs
behind wall switches / want a known state). Hal: false. Voordeurlamp uses sun
boundaries and an explicit light. Woonkamer: `lights_exclude` the kiosk screen,
Chromecast in `media_players_on`, Music Assistant mirror in
`media_players_ignore`. Daytime in Keuken/Hal/Woonkamer is `white` 2500 K;
Hal/Keuken evening brightness 15 %, Hal night = Nightlight 3 %; all rooms
`ease` 120 s at every slot start. Check live values with
`ha_config_get_automation` instead of trusting this list.

## Pitfall: variable order
HA renders `variables:` top-down; a variable that uses one defined further down
sees it as undefined (logged as "Template variable warning: 'x' is undefined",
no error). Until 2026-11-06 `room_quiet_since` used `room_list` before it was
defined, so it was always empty and the `media_hold_limit` release never fired.
`room_list` now sits directly under `room:`. When adding a variable, define it
below everything it reads.
