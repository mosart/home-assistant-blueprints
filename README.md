# Home Assistant Blueprints

A small collection of automation blueprints for Home Assistant, written for my
own setup and shared in case they are useful to someone else.

## Blueprints

### Hue Smart Button (ROM001) via ZHA

Controller for the Philips Hue Smart Button, paired through ZHA.

| Action | Behaviour |
| --- | --- |
| Short press | Toggles between off and a scene preset of your choice |
| Double press | Applies a second scene preset |
| Hold | Dims in steps; direction reverses on every new hold |

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhue_smart_button_rom001%2Fhue_smart_button_rom001.yaml)

#### Requirements

- The button paired via **ZHA**. Zigbee2MQTT and deCONZ are not supported;
  the blueprint listens for `zha_event` directly.
- The [`scene_presets`](https://github.com/Hypfer/hass-scene_presets) custom
  integration, installed through HACS.
- A **toggle helper** (`input_boolean`) per button, used to remember which way
  the next hold will dim. Create one under
  *Settings → Devices & services → Helpers → Toggle*.
- A **light group** (or any single light) to use as the reference entity. An
  area has no on/off state of its own, so the blueprint needs one entity to read
  it from. *Settings → Devices & services → Helpers → Group → Light group*.

#### Choosing presets

The preset inputs are a searchable dropdown, labeled and ordered the same
way the Scene Presets panel groups them (`Category — Preset name`) — type
to filter.

Presets you've added locally (via `userdata/`) aren't included in this
list; only presets shipped by Hypfer/hass-scene_presets itself are.

The dropdown is generated from upstream preset data by
`scripts/generate_scene_presets_options.py`. If Hypfer/hass-scene_presets adds
new presets and you want them reflected here, run
`python3 scripts/generate_scene_presets_options.py` and review the diff.

#### Notes on behaviour

The button keeps its own internal dim direction, which drifts out of sync with
the actual brightness of your lights. This blueprint therefore ignores the
direction reported by the button and tracks it in the helper instead, flipping
it on release. The practical effect is that every new hold dims the opposite way
from the previous one.

Holding at the very bottom or top does nothing until you release and hold again.
If the lights are off, a hold always brightens.

### Hue Tap Dial Switch (RDM002) via ZHA

Controller for the Philips Hue Tap Dial Switch, paired through ZHA.

| Action | Behaviour |
| --- | --- |
| Short press (any button) | Applies that button's preset |
| Double press (any button) | Applies that button's second preset, if configured |
| Dial rotation | Adjusts brightness; spin speed controls step size |

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhue_tap_dial_rdm002%2Fhue_tap_dial_rdm002.yaml)

#### Requirements

- The remote paired via **ZHA**. Zigbee2MQTT and deCONZ are not supported;
  the blueprint listens for `zha_event` directly.
- The [`scene_presets`](https://github.com/Hypfer/hass-scene_presets) custom
  integration, installed through HACS.

Unlike the Smart Button blueprint above, no toggle helper or reference
entity is needed — the dial reports real, absolute rotation direction, so
there's no internal state to track between triggers.

#### Choosing presets

Same picker as the Smart Button blueprint above — see "Choosing presets"
there. Each button's double-press field can be left blank to do nothing on
double press.

#### Notes on behaviour

Holding a button is not supported. On this device, a held button reports an
event that looks identical to turning the dial left — a known upstream
limitation ([zigpy/zha-device-handlers#3696](https://github.com/zigpy/zha-device-handlers/issues/3696))
that the device's quirk only partially filters. Short press, double press,
and dial rotation are unaffected.

Clicking the dial itself (as opposed to turning it) is not exposed to Home
Assistant at all — the device's ZHA quirk discards that event before it
becomes visible, so it can't be used in any blueprint built on ZHA.

## Why these are self-contained

These blueprints target one specific device on one specific integration. That
makes them shorter and easier to reason about than a universal controller
blueprint, at the cost of not being reusable elsewhere. If you need broad device
support, [Awesome HA Blueprints](https://github.com/EPMatt/awesome-ha-blueprints)
is the better starting point.

## Issues and contributions

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue. In short:

- These are shared as-is, maintained in whatever spare time exists. There is no
  support commitment and no response time to expect.
- Bug reports are welcome when they include the Home Assistant version, the
  integration used, and the relevant `zha_event` output or automation trace.
- Requests to support other devices or other Zigbee integrations will generally
  be declined. Forking is encouraged and needs no permission.

## Licence

Licensed under the [European Union Public Licence v1.2](LICENSE) (EUPL-1.2).

SPDX-License-Identifier: EUPL-1.2
