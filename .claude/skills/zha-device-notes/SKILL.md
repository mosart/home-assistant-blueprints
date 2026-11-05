---
name: zha-device-notes
description: Device/firmware facts learned on this ZHA installation — Hue RWL022 events, Tuya TS0505B startup behaviour, Innr, Sonoff sensors, light transition behaviour. Use when touching device controllers or configuring lamps.
---

# ZHA device notes

## Tuya lamps (e.g. TS0505B, the "Nous" lamps)
ZHA shows no power-on settings for them, but they **accept writes** (verified by
power-cycling: the Nous Nachtlampje Kleine Beer remembered them). Use
`zha.set_zigbee_cluster_attribute` with `ieee`, `endpoint_id: 1`,
`cluster_type: in`:

| What | cluster_id | attribute | value |
| --- | --- | --- | --- |
| On at power-up | 6 | 16387 (0x4003) | 1 |
| Brightness at power-up | 8 | 16384 (0x4000) | 0–254 (3% ≈ 8) |
| Colour temperature at power-up | 768 | 16400 (0x4010) | mireds (2000 K = 500) |

A "success" from the service does not prove the lamp stores it — ask the owner
to pull the plug for a few seconds and see. Innr lamps expose these as entities
(`select…opstartgedrag`, `number…inschakelniveau`, …) instead.

## Light behaviour
- ZHA lights report the **target** brightness right when a transition starts;
  the blueprints rely on this ("already heading to the target, leave it").
- `scene_presets.apply_preset` accepts `transition` up to 300 s.
- Lamps differ: the woonkamer boekenkast lamp is brightness-only (no colour
  temperature); Hue/Innr colour lamps take `color_temp_kelvin` and `rgb_color`.
  Innr colour range 1798–6535 K (Hue 2000–6535 K); Innr nachtlampjes RB 256 C
  accept colour too (older text claiming "brightness only" is outdated).
- Innr RCL 232 C / Hue "Opstartgedrag: On" brings a lamp up at full white after
  a power cut — the reason the trappenhuis blueprint uses
  "always apply the slot's light on motion".

## Hue Dimmer Switch RWL022 (ZHA)
Emits named events: `on_short_release`, `off_short_release`, `up_short_release`,
`up_hold`, `up_long_release`, `down_*`. Raw `step`/`stop`/`recall`/`on` cluster
commands also arrive from leftover Hue bridge bindings; `step` `args[0]` is a
StepMode enum, not "up"/"down". Cycling presets needs the helper
`input_text.<room>_laatste_preset`.

## Sonoff SNZB-03P
The raw motion `binary_sensor` latches on after the first detection; use the
**occupancy** (`…_bezetting`) entity. Battery sensors drop to `unavailable` and
back: a plain state/occupancy trigger ignores `unavailable → on`
(see `recovery_sensors` in the presence blueprint).

## Media players
A Chromecast running an app reports `paused`/`idle` for a whole evening of TV
and the Music Assistant mirror of it can keep saying `playing` after the device
is off — see the presence blueprint's "Media" section for how that is handled.
