# Home Assistant Blueprints

A small collection of automation blueprints for Home Assistant, written for my
own setup and shared in case they are useful to someone else.

## Blueprints

| Blueprint | Description | Import |
| --- | --- | --- |
| [Hue Smart Button (ROM001) via ZHA](#hue-smart-button-rom001-via-zha) | Controller for the Philips Hue Smart Button, paired through ZHA: short press toggles a scene, double press applies a second scene, hold dims in steps. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhue_smart_button_rom001%2Fhue_smart_button_rom001.yaml) |
| [Hue Tap Dial Switch (RDM002) via ZHA](#hue-tap-dial-switch-rdm002-via-zha) | Controller for the Philips Hue Tap Dial Switch, paired through ZHA: each button short/double press applies a scene, long press can switch off, the dial adjusts brightness. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhue_tap_dial_rdm002%2Fhue_tap_dial_rdm002.yaml) |
| [Hue Dimmer Switch (RWL022) via ZHA](#hue-dimmer-switch-rwl022-via-zha) | Controller for the Philips Hue Dimmer Switch, paired through ZHA: the top button toggles on/off (restoring the last scene), the bottom button cycles through scenes, and the brightness buttons step the current brightness. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhue_dimmer_switch_rwl022%2Fhue_dimmer_switch_rwl022.yaml) |
| [Presence lighting with scene memory](#presence-lighting-with-scene-memory) | Presence lighting for one or more areas: motion or occupancy restores the last scene, or dims/switches off after being quiet, deferring to whatever scene is already in use instead of forcing a fixed one. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Frooms%2Fpresence_lighting%2Fpresence_lighting.yaml) |
| [Sonoff Motion Sensor (SNZB-03P) camera-snapshot notification](#sonoff-motion-sensor-snzb-03p-camera-snapshot-notification) | Notifies one or more phones when the sensor detects activity, with a live camera snapshot attached. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fsonoff_motion_snzb03p%2Fsonoff_motion_snzb03p.yaml) |
| [Scheduled evening dimming](#scheduled-evening-dimming) | Two-step evening dim for a set of areas: lights above a threshold are dimmed to a target level at one time, then dimmed further at a second, later time. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Frooms%2Fscheduled_dimming%2Fscheduled_dimming.yaml) |
| [Scheduled switch with motion boost](#scheduled-switch-with-motion-boost) | An on/off switch or light that follows a morning and an evening schedule window (clock time to sunrise, sunset to clock time), with a temporary motion-triggered boost outside of those windows. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Frooms%2Fscheduled_switch_with_motion%2Fscheduled_switch_with_motion.yaml) |
| [UniFi Protect person-detection notification](#unifi-protect-person-detection-notification) | Notifies phones with a live snapshot when a UniFi Protect camera detects a person, but only while everyone selected is away. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Funifiprotect_person_detection%2Funifiprotect_person_detection.yaml) |
| [Miele washing machine start/finished notification](#miele-washing-machine-startfinished-notification) | Notifies one or more phones when the washing machine starts an actual wash cycle, with the program, temperature and expected end time — and a second notification when it's done. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fmiele_washing_machine%2Fmiele_washing_machine.yaml) |
| [Home Connect dishwasher start/finished notification](#home-connect-dishwasher-startfinished-notification) | Notifies one or more phones when the dishwasher starts an actual wash cycle, with the program and expected end time — and a second notification when it's done. | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhome_connect_dishwasher%2Fhome_connect_dishwasher.yaml) |

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

#### Remembering the last scene

Every preset a short or double press applies is written to an `input_text`
helper named after the **Room** input — `input_text.<room>_laatste_preset`
(areas joined with `_` for a button spanning more than one). A short press
that just toggles the lights off writes nothing, same as a room going dark.

This is the same name the `[mosart] Presence lighting with scene memory`
and `[mosart] Hue Tap Dial Switch (RDM002) via ZHA` blueprints derive from
their own **Rooms**/**Room** input — point every instance in a room at the
same area(s) and they all agree on the helper without any of them being
told about the others. None of them need it to actually exist: pick
**Room** for a button in a space with no matching helper (or no
presence-lighting instance at all) and the feature just has nothing to
write to or restore from yet. Create the helper once, named to match, only
where you actually want the memory to work — Settings → Devices & services
→ Helpers → Text.

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
so this needs the "last chosen scene" helper described below to actually
exist. Without it the toggle has nothing to compare against and every short
press simply applies its preset. Double press is unaffected and always
applies its preset.

With **Long press turns the lights off** enabled (also off by default),
holding any of the four buttons switches the lights off regardless of which
preset is active.

#### Remembering the last scene

Every preset this remote applies is written to an `input_text` helper named
after the **Room** input — `input_text.<room>_laatste_preset` (areas
joined with `_` for a remote spanning more than one). That gives the room a
"last chosen scene" other automations can read — the pattern a Hue bridge
gets for free, where each room tracks which scene is currently active and
sensors fall back on it instead of forcing one fixed scene.

This is the same name the `[mosart] Presence lighting with scene memory`
blueprint derives from its own **Rooms** input (see its "The three
fallbacks" section below) — point both instances at the same area(s) and
they agree on the helper without either one being told about the other.
Neither blueprint needs it to actually exist: pick **Room** for a remote
in a space with no matching helper (or no presence-lighting instance at
all) and the feature just has nothing to write to or restore from yet.
Create the helper once, named to match, only where you actually want the
memory to work — Settings → Devices & services → Helpers → Text.

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

### Hue Dimmer Switch (RWL022) via ZHA

Controller for the Philips Hue Dimmer Switch, paired through ZHA. Physical
buttons top to bottom: On/Off, brightness up, brightness down, Scene (the
bottom button is printed with the Hue logo rather than an off icon on this
model).

| Action | Behaviour |
| --- | --- |
| On/Off (top button) | Toggles: turns the lights off if they're on, or restores the last scene applied through this switch (or the first scene, the first time) if they're off |
| Scene (bottom button) | Always applies the next scene in the list, cycling through them on repeated presses — turns the lights on from off |
| Brightness up / down | Steps the current brightness; a click steps once, holding steps repeatedly |

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhue_dimmer_switch_rwl022%2Fhue_dimmer_switch_rwl022.yaml)

#### Requirements

- The switch paired via **ZHA**. Zigbee2MQTT and deCONZ are not supported;
  the blueprint listens for `zha_event` directly.
- The [`scene_presets`](https://github.com/Hypfer/hass-scene_presets) custom
  integration, installed through HACS.
- A **light group** (or any single light) to use as the reference entity. An
  area has no on/off state of its own, so the blueprint needs one entity to
  read it from. *Settings → Devices & services → Helpers → Group → Light
  group*.
- A **text helper** named `input_text.<room>_laatste_preset` (see below).
  Unlike the other blueprints that share it, this one needs it: it's how
  the Scene button knows where it is in the cycle. Without it every press
  applies the first scene. *Settings → Devices & services → Helpers →
  Text*, max length 255.

#### Choosing presets

Same picker as the Smart Button blueprint above — see "Choosing presets"
there. The five scenes form a fixed cycle: repeatedly pressing the Scene
button steps through them in order, wrapping back to the first after the
fifth.

#### Remembering the last scene

Every scene applied (by the Scene button cycling, or the On/Off button
restoring one) is written to an `input_text` helper named after the
**Room** input —
`input_text.<room>_laatste_preset` (areas joined with `_` for a switch
spanning more than one). This is the same name the `[mosart] Presence
lighting with scene memory`, `[mosart] Hue Tap Dial Switch (RDM002) via
ZHA`, and `[mosart] Hue Smart Button (ROM001) via ZHA` blueprints derive
from their own **Rooms**/**Room** input — point every instance in a room
at the same area(s) and they all agree on the helper without any of them
being told about the others.

Turning the lights off with the On/Off button also snapshots their exact
state (including any Brightness-button adjustments) into a scene named
`scene.rwl022_<device_id>_snapshot`, and On restores that snapshot rather
than re-applying the named scene with its own fixed brightness.

#### Notes on behaviour

This model's ZHA quirk reports named per-button events
(`on_short_release`, `up_hold`, …) rather than the plain Zigbee
On/Off/Step commands some other ZHA remotes use — the blueprint relies on
that naming to tell the four buttons apart without a template. It also
still emits raw LevelControl `step`/`stop` cluster commands in parallel,
left over from whatever group/scene bindings the Hue bridge set up before
the device was moved to ZHA; those are ignored here.

Pressing On/Off while the lights are off never advances the Scene cycle —
it always restores whatever scene was last applied (or the first scene,
the first time), so a plain off/on doesn't skip one.

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

Tapping the notification opens the camera entity's more-info view (via
the Companion app's `entity_id` data key) — the live feed, and for a
camera with recorded history, its timeline to scrub back to the moment
that triggered it. The attached snapshot is a live image taken when the
notification is sent, not a frame pulled from that exact moment; the
timeline is how to see the actual detection.

The message includes the exact date and time of the trigger (e.g.
`25-09-2026 23:59:49`) via a `{{ trigger_time }}` template variable, so
that exact moment can be found in the camera's own recorded timeline — a
static snapshot alone doesn't always show who or what set it off,
especially at night.

### Presence lighting with scene memory

Presence lighting for one room. Where a motion automation normally forces one
fixed scene, this one defers to whatever scene is already in use.

| Situation | Behaviour |
| --- | --- |
| Motion, room dark | Depends on the current time slot's **How · On motion in a dark room** (below): the slot's own light, the last preset a remote applied, or the room's last light settings — at the slot's brightness unless the slot keeps the preset's own |
| Motion, room already lit | Normally nothing. With "Last light settings" at the slot's brightness, brightness follows the slot without touching the scene. A light changed by hand during the slot is always left alone |
| Motion while dimmed | Puts back exactly what was on before the dim |
| No motion (30 min, adjustable) | Dims as a warning, then switches off |
| Media actively playing in the room | Postpones dimming and switching off. A paused player doesn't. |
| A listed "counts while on" player (e.g. a Chromecast) is on | Postpones dimming and switching off, even while it reports paused or idle (up to a limit) |
| A new time slot begins | Optional: lights that are still on ease over to the new slot. Lights that are off stay off |

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

**Sensors that can drop offline** is optional. Home Assistant does not count a
sensor going straight from `unavailable` to detected as motion, so a battery
Zigbee sensor that drops offline for a while and recovers just as someone walks
in leaves the light off. List such sensors there and that recovery counts as
motion. It is an explicit list because a state trigger can't target an area;
normal detections still come from the areas, so nothing fires twice.

The set of lights is resolved when the automation runs, not when you save it,
so moving a lamp between areas is picked up without editing anything.

**Lights (override)** is for departing from that: control only a subset, or
reach a lamp that lives in another area. Leave it empty for the normal case.

**Lights to exclude** keeps the area-based set but leaves out the lights you
list — a wall tablet's screen exposed as a light, say. Lamps added to the area
later are still picked up. It only applies when **Lights (override)** is empty.

A light *group* in one of the areas (a Hue room/zone light, a light group
helper, or a ZHA Zigbee group) is left out of the derived set — only its
members are controlled. Snapshotting both a group and its members would
fight itself on restore, since changing a member also changes the group's
state. Set the override explicitly if you actually want the group driven
instead of its members.

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

When motion arrives in a dark room, and the current time slot's **preset
behaviour** is set to "Keep whichever preset is already showing, just fix
its brightness" (see below), the automation asks three questions in order
and stops at the first answer:

1. **Is there a snapshot?** Taken every time the room is dimmed, so it holds
   whatever was really on the lights — including changes made from a
   dashboard, a voice assistant, or anything else. Snapshots are transient and
   are lost when Home Assistant restarts, which is what the next two are for.
2. **Did a remote record a preset?** Read from
   `input_text.<room>_laatste_preset` — the same name the Hue Tap Dial and
   Hue Smart Button blueprints derive from their own **Room** input, so
   nothing needs wiring by hand (see their "Remembering the last scene"
   sections above). A room with no remote, or no such helper, simply has
   nothing to restore here.
3. **Otherwise, what time is it?** Night between the two boundary times,
   evening from its own boundary until night begins, daytime for everything
   else.

Whichever of the three ends up applied, its brightness is then pinned to
that slot's own brightness input — see "The three time slots" below. This
chain runs for "Last light settings"; "Last remote preset" starts at step 2,
and "This slot's light" skips it entirely.

"Last light settings" at the slot's brightness also acts when motion arrives in a room that's **already
lit** — a preset a remote, dashboard, or voice assistant just set by hand.
The three fallbacks above don't run again in that case (there's nothing to
restore; the preset is already showing), but its brightness is still pinned
to the current slot's level, so a scene picked earlier in the evening still
dims for the night instead of staying at whatever brightness it was set to.
The other combinations never touch an already-lit room.

#### The three time slots

The settings are grouped in collapsible sections, all collapsed by default. **Room** comes first, then
one section per time slot — **Daytime**, **Evening**, **Night** — each laid
out the same way, then **Dim & switch-off**, **Transitions**, **Media** and
**Advanced**. Inside a slot the field names start with *When*, *What* or
*How*:

| Field | What it does |
| --- | --- |
| **When · Start at sunrise / sunset** | Daytime and Evening only: follow the sun instead of the fixed time below. Off for Daytime, on for Evening by default. |
| **When · Fixed start time** | Daytime 07:00, Evening 18:00, Night 23:00 by default. Daytime's start is also the end of the night. |
| **What · Light** | A scene preset, **Light colour (pick below)**, **White (pick temperature below)**, or **No preset — turn off** (the room stays dark in that slot, e.g. an outdoor lamp in daylight). |
| **What · Colour** / **What · White temperature** | Only used for the matching choice above; ignored otherwise. |
| **What · Keep the preset's own brightness** | Off by default: the slot's brightness below is applied. A colour or white always uses the slot's brightness. |
| **What · Brightness** | Daytime 100%, Evening 50%, Night 3% by default. |
| **How · On motion in a dark room** | *This slot's light*, *Last remote preset* (else this slot's light), or *Last light settings* (else this slot's light) — see the three fallbacks above. Daytime defaults to this slot's light, Evening and Night to the last light settings. |
| **How · When the slot begins** | *Ease lit lights over* (default), or *Wait for motion*. |
| **How · Slot-start transition** | 0–300 seconds, for *Ease lit lights over*. |

With **Last light settings** and the slot's brightness (the default for
Evening and Night), motion in a room that's already lit keeps whatever scene
is showing and only brings its brightness to the slot's level — a scene
picked earlier in the evening still dims for the night without losing the
scene itself. With **Keep the preset's own brightness** on, a lit room is
left entirely alone. A Hue-style preset is mostly about colour, not
brightness, which is why the slot's brightness is applied by default.

**When the slot begins.** With *Ease lit lights over*, lights that are still
on at the slot boundary move over to the new slot in the given time — the
slot's light (and brightness), or with *Last light settings* only the slot's
brightness, keeping the colour. Lights that are **off** stay off until there
is motion: this blueprint never switches a light on in an empty room (a
vacation or presence-simulation automation is the place for that). A light
changed by hand in the previous slot eases over too — the new slot takes
over. Scene presets accept at most 300 seconds, hence the slider's range.
At the morning boundary the remote's preset memory is also forgotten first,
so a new day doesn't replay yesterday's remote choice.

A blueprint can't show HA's dashboard-style colour swatches or the presets'
thumbnails — there is no blueprint selector for either — hence a dropdown
plus the two pickers. Nor can a field be hidden depending on another one, so
the colour and white fields are always visible and simply ignored unless
chosen.

#### Always apply the slot's light on motion

Off by default. The three fallbacks above, and the "already lit" check
that normally makes motion in a lit room do nothing (beyond the brightness
sync described above), both exist to defer to whatever's already on the
lights — deliberately, since a light someone just set by hand shouldn't get
overridden by a passing motion event.

Note that this is a different fix from "keep whichever preset is already
showing" above: that mode preserves the preset a remote or app set and only
touches brightness, in both a dark and an already-lit room. This toggle
instead throws the preset away too — use it only when the preset itself
can't be trusted, not just its brightness.

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

This setting lives under **Advanced**. Each slot's **Keep the preset's own
brightness** still applies here. A light changed by hand during the current
slot is still left alone until the next slot (see "Lights changed by hand").

#### Transitions

Three separate transition times: a quick fade in and out, and a slow
adjustment when the lights are already on:

| Situation | Input | Default |
| --- | --- | --- |
| Motion in a dark room, or in a room this automation dimmed as a warning | **Fade-in from dark** | 3 seconds |
| Motion in a room whose lights are already on (e.g. easing an evening scene down to the night brightness, or a forced time-of-day preset taking over) | **Transition when already lit** | 5 minutes |
| The warning dim, the switch-off, and a slot set to "No preset — turn off" | **Fade-out (from dim) to dark** | 10 seconds |

Motion during a slow already-lit fade does not restart it. A light that is
fading reports its target brightness straight away, so the automation sees
it is already heading to the right level and leaves it alone.
**Transition when already lit** is capped at 5 minutes, the longest
transition scene presets accept.

#### Lights changed by hand

When the lights are already on, motion only adjusts a light that is off the
slot's level *and* was last changed before the current time slot began. A
light someone set by hand during this slot — brighter for reading or
playing the piano, from a remote, dashboard or voice assistant — is left
alone for the rest of the slot instead of being pulled back on every
motion. At the next slot boundary (evening → night, say) the automation
takes over again. A slot whose preset keeps its own brightness is applied
to a lit room once per slot, not on every motion.

#### Missed switch-offs

The "no motion" countdown runs inside Home Assistant and is lost whenever
the automation reloads mid-way — saving it, re-importing this blueprint, or
restarting Home Assistant. Without a safety net the light would then stay on
until the next motion. So the blueprint also re-checks once a minute: when a
light is still on and the room has been quiet for longer than **Dim after**
plus 2 minutes (or **Dim after** + **Switch off after** + 2 minutes if the
warning dim already happened), it runs the normal dim and switch-off after
all (or switches straight off if the dim already happened).

"Quiet" counts from whichever came last: the room's motion or occupancy
sensors all clearing, or a light being switched on. A light switched on by
hand in an empty room therefore also dims and switches off, **Dim after**
(+ 2 minutes) after it was switched on. The check only fires on the moment
the room *becomes* overdue; a room already overdue at the moment the
automation reloads is not caught until the lights or sensors change again.

#### Notes on behaviour

The dim is a warning, not a setting: the automation snapshots first, so the
dim never destroys the brightness you chose. **Dim by** is a relative step
(`brightness_step_pct`) off each light's own current brightness, not a fixed
target — so a light already resting low (e.g. on a dim Night preset) only
drops a little further instead of being pushed up to a shared level right
before it goes out. Returning motion during the dim window restarts the
automation, which cancels the pending switch-off and restores the snapshot.

Dimming and switching off are both skipped while a media player in the room
is actively playing. A player that's merely paused doesn't hold this back;
pause and leave, and the room still dims and switches off on schedule. Once
playback stops, the missed-switch-off check (above) starts the normal dim
delay from that moment.

Some players never say "playing" while in use: a Chromecast running a
streaming app typically reports "paused" or "idle" for a whole evening of
TV. List those under **Players that count while on** — the room then
counts as in use for as long as such a player is on at all, switching it on
cancels a pending dim, and switching it off starts the normal dim delay.
Such a player can also stay "paused" long after the TV itself is off, so its
hold is capped by **Longest hold for those players** (2 hours by
default): after that long without motion the room dims and switches off
as usual, whatever the player reports.

**Players to ignore** leaves players out of all of this — for a
duplicate entity of the same device (a Music Assistant or Spotify mirror of a
Chromecast, say) that keeps reporting "playing" after the device is off.

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

### Scheduled switch with motion boost

A plain on/off switch or light with no dimming and no scene memory — two
fixed schedule windows, plus a motion boost outside of them.

| Situation | Behaviour |
| --- | --- |
| Morning window on-time reached, sun not yet up | Turns on |
| Morning window on-time reached, sun already up (long summer day) | Nothing — avoids leaving it on for the rest of the day with no sunrise event left to turn it off |
| Sunrise | Turns off |
| Sunset | Turns on |
| Evening window off-time reached | Turns off |
| Motion, dark out, outside both windows | Turns on, then off again after being quiet for the boost duration |
| Motion, broad daylight | Nothing — a motion boost achieves nothing when it's already light outside |
| Motion, inside either window | Nothing — the window is already keeping it on |

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Frooms%2Fscheduled_switch_with_motion%2Fscheduled_switch_with_motion.yaml)

#### What it controls

**Switch (or light)** is a single entity — this blueprint doesn't dim or
apply scenes, so there's no `scene_presets` dependency and no per-room
helper to create, unlike presence lighting above. **Area(s) for motion**
works the same way it does in presence lighting: motion or occupancy in
any of the areas selected triggers the boost, whichever sensor type each
area has.

#### Why motion doesn't turn it off inside a window

The two schedule windows and the motion boost share one on/off switch, so
they have to agree on when it's safe to turn off. Motion always turns the
target on immediately, but the "turn off after being quiet" half of the
boost only fires if neither window is currently active — otherwise a quiet
spell during, say, the evening window would cut that window short, even
though it isn't supposed to end until the off-time.

#### Why the morning on-time checks the sun first

A fixed on-time paired with a sunrise off-trigger only works as a pair
when the on-time actually comes before sunrise. On a long summer day
sunrise can land before the on-time (e.g. sunrise at 05:30, on-time at
06:30) — without a check, the on-time would still fire and switch on, but
that day's sunrise event has already passed, so nothing would ever turn
it back off until sunset. The on-time is therefore gated on `sun, before:
sunrise`: if the sun's already up, it does nothing.

#### Notes on behaviour

- The morning and evening windows are fixed to sunrise/sunset for the
  transitions this blueprint doesn't take a clock-time input for — there's
  no toggle to pin those to fixed times instead, unlike the sunrise/sunset
  toggles in presence lighting. Add a second instance, or ask for the
  toggle to be added, if that's needed.
- The motion boost only fires while it's actually dark (before sunrise or
  after sunset) — broad daylight is excluded even outside the two
  schedule windows, since a driveway light doesn't need to react to motion
  when the sun is already doing the job.
- Built for a driveway light behind a Zigbee inline relay (no dimming, no
  power-on-state quirks to work around), but the blueprint itself doesn't
  assume that hardware — any switch or light entity works.

### UniFi Protect person-detection notification

Notifies one or more phones, with a live camera snapshot attached, when a
UniFi Protect camera's "Person detected" sensor fires — but only while
everyone selected is away.

| Situation | Behaviour |
| --- | --- |
| Person detected, everyone selected is away | Notifies every phone listed, title + message + live snapshot |
| Person detected, anyone selected is home | Nothing — they're there to notice it themselves |

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Funifiprotect_person_detection%2Funifiprotect_person_detection.yaml)

#### Requirements

- The [`unifiprotect`](https://www.home-assistant.io/integrations/unifiprotect/)
  core integration, with the target camera's "Person detected" binary
  sensor exposed (Settings → Devices & services → the camera's device page).
- One or more legacy `notify.mobile_app_...` services — see "Phones to
  notify" below.

#### Tapping the notification

The notification's tap target is the camera entity itself (via the
Companion app's `entity_id` data key), which opens that entity's more-info
view — the live feed, and for a UniFi Protect camera, its history
scrubber to step back into the clip that triggered the notification.

This deliberately doesn't try to deep-link into the UniFi Protect app
itself. Its iOS app does have an unofficial, community-reverse-engineered
URL scheme (`unifi-protect://protect/devices/<id>`), but it only opens a
camera's *live* view, not the specific event/clip, and the iOS Companion
app has a known issue launching external app URL schemes from a
notification tap in the first place — not something worth building on for
a notification going to an iPhone.

#### Notes on behaviour

**Everyone who must be away** takes multiple `person` entities and
requires all of them to read "not home" — pick everyone who'd otherwise
get a notification for something they're already there to see. There's no
"someone is away" mode; add a second instance if you want that instead.

### Miele washing machine start/finished notification

Notifies one or more phones when the washing machine starts an actual wash
cycle — with the program, temperature and expected end time — and again
when it's done.

| Situation | Behaviour |
| --- | --- |
| Appliance status sensor transitions to `in_use` | Notifies every phone listed: title + message with program, temperature and end time |
| Appliance status sensor transitions to `program_ended` | Notifies every phone listed: title + message |
| Sensor sits at `on`, `programmed` or `waiting_to_start` | Nothing — the machine is powered on or a delayed start is pending, but it isn't washing yet |

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fmiele_washing_machine%2Fmiele_washing_machine.yaml)

#### Requirements

- The [`miele`](https://www.home-assistant.io/integrations/miele/) core
  integration, with the appliance's main status sensor exposed (an `enum`
  sensor whose state is one of `on`/`in_use`/`program_ended`/etc.), plus its
  program, end-time and temperature sensors.
- One or more modern notify entities (`notify.<device>`, the kind the
  Mobile App integration creates per device) — no snapshot is attached
  here, so unlike this repo's camera-notification blueprints there's no
  need for the legacy `notify.mobile_app_...` service.

#### Why `in_use`, not `on`

The Miele integration's main status sensor goes through several states
before an actual wash: `on` (powered on, no program chosen yet), then
`programmed` or `waiting_to_start` once a program is selected but before it
begins (including a delayed start). "Started" only fires on the
transition to `in_use`, so a notification means the machine is genuinely
washing, not just switched on or armed for later.

#### No tap target

Notifications are plain title/message pushes — there's no tap-to-open onto
the appliance's status entity. The modern `notify.send_message` action
currently rejects any extra `data` keys beyond `title`/`message`
(including a tap-target `entity_id`), a known Home Assistant core
limitation as of this writing: it only reaches phones through notify
entities, not the legacy per-device `notify.mobile_app_...` service that
still accepts that payload. If you want a tap target back, this blueprint
would need to switch to that legacy per-phone service — see the camera
blueprints above for that pattern.

#### Notes on behaviour

- The program and temperature are read once, at the moment the "started"
  notification fires — later changes to those sensors don't retroactively
  edit an already-sent notification.
- Program names come through as the integration's own English slugs (e.g.
  `cottons_eco`); the blueprint humanizes them (underscores to spaces,
  capitalized) rather than hand-maintaining a translation table for every
  Miele program.
- The Miele integration reflects Miele's own cloud status for the
  appliance, not a local reading — expect the same few-seconds lag behind
  the machine's own display that the Miele app itself has.

### Home Connect dishwasher start/finished notification

Notifies one or more phones when the dishwasher starts an actual wash
cycle — with the program and expected end time — and again when it's done.
A separate blueprint from the Miele one above: Home Connect models its
appliance status, program and end time differently enough (different enum
values, the program as a `select` entity rather than a `sensor`, no
separate temperature reading) that adding it to the Miele blueprint would
mean bolting a second integration onto a single-integration blueprint —
this repo's convention is a fork instead, so it's its own blueprint here.

| Situation | Behaviour |
| --- | --- |
| Appliance status sensor transitions to `run` | Notifies every phone listed: title + message with program and end time |
| Appliance status sensor transitions to `finished` | Notifies every phone listed: title + message |
| Sensor sits at `inactive`, `ready` or `delayedstart` | Nothing — the dishwasher is idle, a program is armed, or a delayed start is pending, but it isn't running yet |

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmosart%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fcontrollers%2Fhome_connect_dishwasher%2Fhome_connect_dishwasher.yaml)

#### Requirements

- The [`home_connect`](https://www.home-assistant.io/integrations/home_connect/)
  core integration, with the appliance's main status sensor exposed (an
  `enum` sensor whose state is one of `inactive`/`ready`/`run`/`finished`/
  etc.), plus its active-program select and end-time sensor.
- One or more modern notify entities (`notify.<device>`, the kind the
  Mobile App integration creates per device).

#### Why `run`, not `ready`

The status sensor goes through several states before an actual wash:
`ready` (a program is selected but not started) or `delayedstart` (a
delayed start has been set but hasn't begun). "Started" only fires on the
transition to `run`, so a notification means the dishwasher is genuinely
running, not just armed or waiting for a delayed start.

#### No tap target

Same limitation as the Miele blueprint above: `notify.send_message`
currently rejects any extra `data` keys, so there's no tap-to-open onto
the appliance's status entity.

#### Delayed "started" notification

The "started" notification waits a few minutes (configurable, default 3)
before sending, and reads the program/end-time sensors after that delay
rather than the instant `run` first appears. Home Connect's cloud doesn't
estimate the end time until the wash has actually been running for a
bit — a soil-sensing program like Eco 50 especially — so notifying
immediately would often show "klaar rond" with no time to give. If the
end-time sensor is still `unknown` even after the delay, the default
message says so explicitly ("Eindtijd wordt nog berekend") instead of
printing a broken-looking "Klaar rond onbekend".

#### Notes on behaviour

- The program and end time are read once, after the configured delay —
  later changes don't retroactively edit an already-sent notification.
- Home Connect's program options come as vendor-prefixed slugs (e.g.
  `dishcare_dishwasher_program_eco_50`); the blueprint strips everything
  up to the last `_program_` and humanizes what's left (`Eco 50`) rather
  than hand-maintaining a translation table for every program.
- There's no separate temperature reading for this integration — the
  program name already carries it (`Eco 50`, `Intensiv 70`), unlike the
  Miele washing machine blueprint's dedicated temperature sensor.

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
