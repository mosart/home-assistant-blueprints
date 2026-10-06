# A real home built on these blueprints

This is a tour of how the blueprints in this repo — plus a handful of small,
house-specific automations and helpers around them — actually get used,
room by room. It exists because a few friends asked "what does your Home
Assistant setup actually *do*?" and a screenshot of the automations list
doesn't answer that.

This is **not** a config dump: entity IDs, exact addresses, device-tracker
details and family members' names are all left out on purpose, and a few
clearly personal/leftover helpers (location zones, person trackers, test
tags, a couple of unused-looking helpers) are skipped entirely. What's left
is the pattern each automation follows and why it exists — enough to steal
the idea for your own house.

Three of this repo's blueprints do most of the heavy lifting: **Presence
lighting with scene memory**, the **Hue Smart Button / Hue Tap Dial**
controllers, and the **Home Connect dishwasher** notifier. Everything else
below is a smaller, one-off automation that fills a gap the blueprints
don't (and aren't meant to) cover.

## Living room

- **Presence lighting** — an instance of this repo's `presence_lighting`
  blueprint. Motion restores whatever scene was last active instead of
  forcing a fixed "on" scene, and dims/switches off again after the room's
  been quiet for a while.
- **Hue Tap Dial switch** — an instance of the `hue_tap_dial_rdm002`
  controller blueprint. Each button applies a scene preset; the dial ring
  adjusts brightness.
- **A mood light that follows the "Stookwijzer" air-quality code** — when
  the Dutch national wood-burning advisory changes, a corner lamp's colour
  changes with it, as a passive reminder of whether burning a fire is
  currently discouraged.
- **Glitch compensation** — some multi-gang switches briefly flicker back
  on a few seconds after being turned off. This automation watches for
  that exact "off → on again almost immediately" pattern and turns the
  light back off, so an actual deliberate press is left alone but the
  flicker isn't.
- Supporting helpers: a toggle that records whether this room's evening dim
  step has already fired tonight, and small text helpers that remember the
  last scene applied and which lamp is currently "selected" for one-off
  brightness changes.

## Kitchen

- **Presence lighting**, same blueprint as the living room, with its own
  "already dimmed tonight" toggle.
- **Fridge & dishwasher plug protection** — a plug-based "turn all smart
  plugs off" routine (holiday mode, "everyone's in bed", etc.) would
  happily cut power to the fridge or a running dishwasher. This automation
  excludes those two from any such blanket action.
- **Dishwasher notifications** — an instance of this repo's
  `home_connect_dishwasher` blueprint: a push notification when the wash
  cycle actually starts (program + expected end time) and another when
  it's finished.
- **Dishwasher water-use tracking** — the appliance itself doesn't report
  water consumption, only a programme name. A small lookup table (sourced
  from the machine's own official spec sheet, litres per programme) adds
  an estimated amount to a running total the moment the status flips to
  "running", so the Energy dashboard's water section gets a plausible
  number instead of nothing.
- **Forcing a queued start past midnight** — if a delayed start is queued
  (not an immediate one — starting it directly in the evening is left
  alone), the automation nudges the delay just far enough that the cycle
  begins just after 00:00. That way a wash that runs overnight gets
  attributed to the day it actually mostly happens on, instead of
  splitting oddly across two days in the statistics.
- **Indicative gas split** — three template sensors divide the whole-home
  gas meter into "central heating", "hot water" and "the rest" (mostly the
  gas stove), using the boiler's own internal energy counters for the
  first two and subtracting from the meter for the third. Deliberately
  kept out of the Energy dashboard's own gas source (a derived, subtracted
  value is too unstable for that), but useful on a plain chart.
- A holiday-mode automation turns off the boiling-water tap while away.

## Hallway

- **Presence lighting**, same pattern, own dim-state toggle.
- **Washing machine notifications** — the same start/finished pattern as
  the dishwasher, for the laundry appliance that lives here.
- A water-pulse sensor feeding the ground-floor toilet's estimated usage
  (see "Whole-home water tracking" below).

## Stairwell

- **Presence lighting**, same pattern, own dim-state toggle.

## Driveway

- **Motion at the mailbox** triggers a push notification — useful for
  parcels as much as for post.
- **A separate "person detected" notification** for actual security
  interest, kept apart from the mailbox one so it isn't drowned out by
  every delivery.
- **Waste-collection reminder** — a notification tied to the Dutch
  "Afvalwijzer" bin-collection calendar.
- **Outdoor lighting** that combines a schedule window with motion, so the
  driveway light behaves sensibly whether or not anyone's walking up to
  the door.

## Bathroom & attic

- Toilet and shower water usage are tracked the same indirect way as the
  ground-floor toilet: a single whole-home water-flow sensor, a short
  manual calibration routine (start a timer, use the fixture once, note
  the litres), and a lookup helper per fixture that turns "a flush/shower
  just happened" into a reasonably accurate litre estimate — all without
  needing a flow meter on every single outlet.

## Garden

- Three small automations instead of one complex one: lights on at a fixed
  morning time *but only before actual sunrise* (so they don't fire in
  summer), lights on at sunset, lights off again at the next sunrise (or
  at a fallback late-night time if sunrise logic alone would leave them on
  too long).

## Primary bedroom

- **Hue Smart Button**, an instance of the `hue_smart_button_rom001`
  controller blueprint, for bedside control — short press toggles a scene,
  hold dims in steps.
- A paired toggle helper remembers which direction the next "hold" should
  dim in, exactly as the blueprint's own docs describe, plus a second
  toggle for a "make it brighter than the base scene" override.
- The two nightstand lamps are wired together as a light group, which is
  what the presence/button blueprints actually need as their one
  "reference" entity for an area.

## Kids' room

- A scene-memory text helper, in the same `<room>_laatste_preset` naming
  pattern the blueprints use, so a button or presence-lighting instance
  elsewhere in the house can restore this room's last scene without any
  of them needing to know about each other — they just agree on a name.

## Whole-home water tracking

Instead of a flow meter on every fixture, one whole-home water-pulse
sensor plus a short manual calibration step per fixture (start a timer,
use the fixture, log the litres) builds up a set of "litres per use"
constants. Each fixture then gets its own small statistics sensor derived
from that constant, which is enough to break the water bill down by room
on a dashboard without instrumenting the whole house.

## Whole-home: security & leaks

- **Water leak detection**, paired with an "alarm active" toggle so a
  detected leak can be acknowledged/silenced without the underlying
  automation needing to change.
- The same pulse-counting idea used for per-fixture water tracking above
  also runs a **"was that a deliberate flush/shower or just noise"**
  calibration check.

## Whole-home: holiday mode

A single toggle switches the house into "we're away" behaviour, backed by
seven automations:

- Leaving together arms holiday mode; returning together disarms it.
- The alarm itself arms automatically a short while after that.
- Morning and evening lighting on both floors fakes a lived-in house on a
  schedule, independently of any presence sensors (there's no one there to
  trigger them).

## Whole-home: system housekeeping

- Core updates install themselves inside a scheduled maintenance window
  rather than whenever they happen to be released.
- A separate automation raises a notification when updates are pending,
  for anything that isn't covered by the scheduled install.
- Battery levels across all battery-powered devices are checked on a
  schedule, with a notification for anything running low.
- A dashboard-selector pair (a dropdown plus a toggle) decides which
  dashboard opens by default — useful when different dashboards make
  sense on a wall tablet versus a phone.

## Cross-cutting helpers worth calling out

- **Light groups** for the garden and the kitchen spots — the
  presence-lighting and button blueprints both need one entity per area to
  read on/off state from, and a plain Hue/Zigbee integration doesn't
  always give you one for free.
- **A media-player group** bundling the TV, a speaker and a streaming
  target, so "whole-house media off" is one call instead of three.
- **A trend sensor** estimating remaining e-bike charge time from the
  charger's live power draw, rather than needing a smart plug that reports
  state of charge directly.
- A scheduled, two-step evening dim across every light in the house,
  independent of the per-room presence-lighting instances — a blunt
  "it's getting late" nudge that complements rather than replaces them.

---

Everything above either *is* one of this repo's blueprints in use, or is
glue around them that turned out to be too house-specific to generalise
into one (hardcoded appliance spec tables, a specific water meter's pulse
behaviour, calibration constants for one particular set of taps). If one
of the smaller patterns here would be useful as its own blueprint, open an
issue — see `CONTRIBUTING.md`.
