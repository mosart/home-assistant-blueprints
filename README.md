# Home Assistant Blueprints

A small collection of automation blueprints for Home Assistant, written for my
own setup and shared in case they are useful to someone else.

## Blueprints

| Blueprint | Description | Import |
| --- | --- | --- |
| [Hue Smart Button (ROM001) via ZHA](#hue-smart-button-rom001-via-zha) | Controller for the Philips Hue Smart Button, paired through ZHA: short press toggles a scene, double press applies a second scene, hold dims in steps. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhue_smart_button_rom001%2Fhue_smart_button_rom001.yaml) |
| [Hue Tap Dial Switch (RDM002) via ZHA](#hue-tap-dial-switch-rdm002-via-zha) | Controller for the Philips Hue Tap Dial Switch, paired through ZHA: each button short/double press applies a scene, long press can switch off, the dial adjusts brightness. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhue_tap_dial_rdm002%2Fhue_tap_dial_rdm002.yaml) |
| [Presence lighting with scene memory](#presence-lighting-with-scene-memory) | Presence lighting for one or more areas: motion or occupancy restores the last scene, or dims/switches off after being quiet, deferring to whatever scene is already in use instead of forcing a fixed one. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Frooms%2Fpresence_lighting%2Fpresence_lighting.yaml) |
| [Sonoff Motion Sensor (SNZB-03P) camera-snapshot notification](#sonoff-motion-sensor-snzb-03p-camera-snapshot-notification) | Notifies one or more phones when the sensor detects activity, with a live camera snapshot attached. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fsonoff_motion_snzb03p%2Fsonoff_motion_snzb03p.yaml) |
| [Scheduled evening dimming](#scheduled-evening-dimming) | Two-step evening dim for a set of areas: lights above a threshold are dimmed to a target level at one time, then dimmed further at a second, later time. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Frooms%2Fscheduled_dimming%2Fscheduled_dimming.yaml) |

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
  *Settings → Devices & services → Helpers → Toggle*, or inline via the
  "+ Create input_boolean" option in this field when building the
  automation.
- A **light group** (or any single light) to use as the reference entity. An
  area has no on/off state of its own, so the blueprint needs one entity to read
  it from. *Settings → Devices & services → Helpers → Group → Light group*.

#### Choosing presets

The preset inputs are a searchable dropdown, labeled and ordered the same
way the Scene Presets panel groups them (`Category — Preset name`) — type
to filter.

Presets you've added locally (via `userdata/`) aren't included in this
list; only presets shipped by Hypfer/hass-scene_presets itself are.

If you typed a raw preset ID under the previous version of this field, it
still works — but the field will show as empty in the editor, and re-saving
the automation through the UI without picking a real option will lose it.

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
| Long press (any button) | Switches the lights off, if enabled |
| Dial rotation | Adjusts brightness; spin speed controls step size |

With the **Toggle off on repeat press** input enabled (off by default),
pressing the button whose preset is already showing switches the lights off.
Pressing a *different* button always switches to that button's preset, so
the remote never turns the lights off when you meant to change scene.

Recognising a repeat press means knowing which preset is currently showing,
so this needs the **Remember last preset in** helper below. Without it the
toggle has nothing to compare against and every short press simply applies
its preset. Double press is unaffected and always applies its preset.

With **Long press turns the lights off** enabled (also off by default),
holding any of the four buttons switches the lights off regardless of which
preset is active.

#### Remembering the last scene

Point the optional **Remember last preset in** input at an `input_text`
helper and every preset the remote applies is written to it. That gives the
room a "last chosen scene" that other automations can read — the pattern a
Hue bridge gets for free, where each room tracks which scene is currently
active and sensors fall back on it instead of forcing one fixed scene.

A presence automation can then restore what you actually picked:

```yaml
- if:
    - condition: template
      value_template: >-
        {{ states('input_text.living_room_last_preset')
           not in ['', 'unknown', 'unavailable'] }}
  then:
    - action: scene_presets.apply_preset
      data:
        preset_id: "{{ states('input_text.living_room_last_preset') }}"
        targets:
          area_id: living_room
  else:
    - action: scene.turn_on
      target:
        entity_id: scene.living_room_bright
```

Only presses that actually apply a preset are recorded — a press that just
toggles the lights off leaves the stored value alone, so it still reflects
the last scene you were in. The helper needs no particular length limit; a
preset id is 36 characters.

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

Holding a button emits a `button_N_hold` event, but it also emits
`LevelControl` steps that look like turning the dial left. The ZHA quirk
separates the two by transition time — 8 for a hold, 4 for the dial — and
mutes the hold ones, but that filter is not fully settled upstream
([zigpy/zha-device-handlers#3696](https://github.com/zigpy/zha-device-handlers/issues/3696)).

That residual ambiguity is harmless for the one thing this blueprint maps
onto a long press: if a stray step slips through it nudges the brightness a
moment before the lights go off anyway. It is why the long-press option is
off by default rather than assumed — and why a long press is not offered for
anything other than switching off. Short press, double press, and dial
rotation are unaffected.

Clicking the dial itself (as opposed to turning it) is not exposed to Home
Assistant at all — the device's ZHA quirk discards that event before it
becomes visible, so it can't be used in any blueprint built on ZHA.

### Sonoff Motion Sensor (SNZB-03P) camera-snapshot notification

Controller for the Sonoff SNZB-03P motion sensor (ZHA): notifies one or more
phones with a camera snapshot attached whenever the sensor detects activity.
Built for a mailbox sensor with a camera pointed at it, but works anywhere a
SNZB-03P sits near a camera.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fsonoff_motion_snzb03p%2Fsonoff_motion_snzb03p.yaml)

#### Requirements

- The sensor paired via **ZHA**. Zigbee2MQTT and deCONZ are not supported.
- A **camera** entity with a snapshot Home Assistant can fetch locally.
- One legacy **`notify.mobile_app_...`** service per phone (Developer Tools
  → Actions, search "notify"). The modern per-device notify entity
  (`notify.send_message`) doesn't support the camera-snapshot attachment, so
  this blueprint calls the legacy service directly instead.

#### Notes on behaviour

This device's raw motion `binary_sensor` reliably reports the first
detection but then latches "on" and does not reliably clear again, so a
trigger on it would only ever fire once. The blueprint triggers on the
**occupancy** entity instead, which clears properly using the sensor's own
presence time-out (a `number` entity on the device itself) and retriggers
correctly on every subsequent visit.

### Presence lighting with scene memory

Presence lighting for one room. Where a motion automation normally forces one
fixed scene, this one defers to whatever scene is already in use.

| Situation | Behaviour |
| --- | --- |
| Motion, room dark | Restores the room's last known state; falls back to the last preset a remote applied, then to the preset for the current time of day |
| Motion while dimmed | Puts back exactly what was on before the dim |
| No motion (30 min, adjustable) | Dims as a warning, then switches off |
| Media playing or paused in the room | Postpones dimming and switching off |

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Frooms%2Fpresence_lighting%2Fpresence_lighting.yaml)

#### Requirements

- The [`scene_presets`](https://github.com/Hypfer/hass-scene_presets) custom
  integration, installed through HACS.
- One `input_boolean` helper per instance, for the **Dimming flag helper**
  input. The automation sets it while it is the one holding the lights
  dimmed, which is how returning motion knows to restore rather than leave
  them dim. Give each instance its own; sharing one makes two rooms restore
  each other's state.
- A motion or occupancy sensor (or both) assigned to one of the selected
  areas. Everything is driven off the areas, so adding a sensor or a lamp to
  one is enough — there is no entity list to keep in step.

#### What it controls

**Rooms** takes one or more areas and everything follows from them: their
motion and occupancy sensors trigger it, their lights are what it controls,
their media players postpone dimming. Pick several to treat adjoining spaces
as one room — a living room and the open kitchen beside it, say.

Motion and occupancy are two independent trigger families, and either one
firing drives the same behaviour. This matters when a room's sensor exposes
only one of the two (a plain PIR has no occupancy entity), or when a device
exposes both and one of them turns out unreliable — a `motion` binary sensor
that gets stuck without a ZHA quirk properly enrolling it, for instance,
while the same device's `occupancy` entity keeps working. No configuration
is needed either way; the blueprint picks up whichever sensor type is present.

The set of lights is resolved when the automation runs, not when you save it,
so moving a lamp between areas is picked up without editing anything.

**Lights (override)** is for departing from that: control only a subset, or
reach a lamp that lives in another area. Leave it empty for the normal case.

A light *group* in one of the areas (a Hue room/zone light, or a light
group helper) is left out of the derived set — only its members are
controlled. Snapshotting both a group and its members would fight itself on
restore, since changing a member also changes the group's state. Set the
override explicitly if you actually want the group driven instead of its
members.

One consequence worth knowing: a motion sensor sitting in the wrong area
becomes presence for that room. A driveway camera filed under the living room
will keep the living room lit. Check the area assignments before blaming the
automation.

#### Checking what an area selection resolves to

The blueprint editor can't preview this — a field has no way to show a
computed result from another field. Two ways to check before saving:

- **Settings → Areas → open the area.** Its entity list is the live source
  this automation reads. Anything shown there (except light groups) is
  included.
- **Developer Tools → Template**, for the exact same computation the
  automation runs:

  ```jinja
  {{ ['living_room', 'kitchen']   {# your areas, by area_id #}
     | map('area_entities') | sum(start=[])
     | select('match', 'light\.') | list }}
  ```

  Swap in your own area IDs (visible in Settings → Areas → the area's URL,
  or via `area_id()` if you only know the friendly name) to see exactly
  which lights this blueprint would control — before the automation exists,
  and again any time later to confirm nothing drifted.

#### The three fallbacks

When motion arrives in a dark room, the automation asks three questions in
order and stops at the first answer:

1. **Is there a snapshot?** Taken every time the room is dimmed, so it holds
   whatever was really on the lights — including changes made from a
   dashboard, a voice assistant, or anything else. Snapshots are transient and
   are lost when Home Assistant restarts, which is what the next two are for.
2. **Did a remote record a preset?** Set the optional **Last preset helper**
   to the same `input_text` the Hue Tap Dial blueprint writes to.
3. **Otherwise, what time is it?** Night between the two boundary times,
   evening from its own boundary until night begins, daytime for everything
   else.

Time of day is deliberately last. It is the answer when the room has no
memory, not an override that reimposes a schedule on a room you just set by
hand.

#### The three time slots

Each preset has its own boundary input directly below it:

| Preset | Boundary | Default |
| --- | --- | --- |
| Daytime | **Morning begins** | 07:00, fixed time |
| Evening | **Evening begins** | Sun's sunset (toggle to switch to a fixed time) |
| Night | **Night begins** | 23:00, fixed time |

**Morning begins** and **Evening begins** each come with a toggle —
**Use sunrise instead** / **Use sunset instead** — to follow the sun rather
than a clock time that drifts against it across the seasons. Evening's
toggle is *on* by default (matching this blueprint's original behaviour,
sunset-only); morning's is *off* by default (a fixed time, as before). Night
has no such toggle — it only ever uses **Night begins**, a fixed time.

Turning either toggle on doesn't need a matching change anywhere else: the
Daytime/Evening/Night decision above and the "Always use the Daytime
preset during daytime" toggle below both read the same boundaries, so they
stay in sync automatically.

#### Always use the Daytime preset during daytime

On by default, and only affects the daytime slot (between **Morning
begins** and the evening boundary) — night and evening always restore
memory first, regardless of this setting.

While on, it skips straight past both memory fallbacks during the day: the
snapshot from last night and any last remote preset are ignored, and motion
always applies the **Daytime preset** instead — so mornings reliably reset to
a fixed look rather than pick up whatever mood was left over from the
previous evening.

Turn it off to restore the room's memory during the day too, the same as
night and evening.

#### Always apply time-of-day preset on motion

Off by default. The three fallbacks above, and the "already lit" check
that normally makes motion in a lit room do nothing, both exist to defer to
whatever's already on the lights — deliberately, since a light someone just
set by hand shouldn't get overridden by a passing motion event.

That assumption breaks for a light whose state changed for a reason outside
Home Assistant's control — the case that prompted this toggle: a smart bulb
wired behind a physical wall switch, where cutting and restoring power to
the switch makes the bulb come back at its own configured power-on
brightness (typically full, cool white), not anything this blueprint chose.
Home Assistant then sees an "on" light and, working as designed, leaves it
alone — which looks like the automation doing nothing.

Turning this on removes the "already lit" check and all three memory
fallbacks from the motion branch entirely. Every motion event applies the
Daytime/Evening/Night preset for whichever slot it currently is,
unconditionally — so a room like that always ends up in a known, correct
state a moment after someone walks in, regardless of what put it in its
previous state. The trade-off is the room's memory: a brightness or scene
you set by hand (from a dashboard, a voice assistant, or a remote) no longer
survives the next motion event either.

This mode also always sets the light to full brightness before applying the
preset's colour. `scene_presets.apply_preset` only ever changes colour — on
a light that's already on it leaves brightness exactly as it found it. Without
forcing brightness here, a light this same automation dimmed low moments
earlier (or one left low by anything else) would get the right colour but
stay just as dim, which looks identical to "nothing happened."

#### Notes on behaviour

The dim is a warning, not a setting: the automation snapshots first, so the
dim never destroys the brightness you chose. **Dim by** is a relative step
(`brightness_step_pct`) off each light's own current brightness, not a fixed
target — so a light already resting low (e.g. on a dim Night preset) only
drops a little further instead of being pushed up to a shared level right
before it goes out. Returning motion during the dim window restarts the
automation, which cancels the pending switch-off and restores the snapshot.

Switching off is skipped while a media player in the room is playing or
paused, checked again at the moment of switching off rather than only when the
room first went quiet.

### Scheduled evening dimming

Two-step evening dim for a set of areas — select every area to cover the
whole house.

| Time | Behaviour |
| --- | --- |
| First dim (default 22:30) | Lights above the first threshold (default 50%) are dimmed to the first target (default 50%) |
| Second dim (default 23:00) | Lights above the second threshold (default 1%) are dimmed to the second target (default 1%) |

Both steps only ever lower brightness. A light that is off stays off, and a
light already at or below a step's threshold is left alone — so the second
step doesn't re-trigger a transition on lights the first step already
brought down.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Frooms%2Fscheduled_dimming%2Fscheduled_dimming.yaml)

#### What it controls

Takes one or more areas and dims every light in them; **Lights (override)**
departs from that the same way it does in the presence lighting blueprint
above — leave it empty for the normal case. The set of lights is resolved
when the automation runs, not when you save it, and a light *group* in one
of the areas is left out in favour of its members, for the same reason
described under "What it controls" for presence lighting.

#### Notes on behaviour

Only two steps are offered, not an arbitrary schedule — pick times,
thresholds, and targets that fit your evening. If you want more than two
dims, add a second instance of this blueprint with its own times.

## Why these are self-contained

The `controllers/` blueprints target one specific device on one specific
integration. That makes them shorter and easier to reason about than a
universal controller blueprint, at the cost of not being reusable elsewhere.
If you need broad device support,
[Awesome HA Blueprints](https://github.com/EPMatt/awesome-ha-blueprints) is
the better starting point.

The `rooms/` blueprints are the exception: presence logic belongs to a room
rather than a device, so it cannot be written as a device controller. They are
still tied to `scene_presets`, so they are not generic either.

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
