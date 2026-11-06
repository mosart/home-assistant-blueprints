# Lighting dashboard ("Verlichting")

The owner's Home Assistant has a dedicated lighting dashboard at
`/dashboard-verlichting/verlichting` (storage mode, sidebar title *Verlichting*,
icon `mdi:lightbulb-group`). It is **not** stored in this repo — Home Assistant
keeps it in `.storage`. This file records the design so a later session can
rebuild or extend it consistently. Edit it through the HA MCP dashboard tools
(`ha_config_get_dashboard` / `ha_config_set_dashboard`), never by hand.

## Goal

A phone-first "Hue app" experience: one tile per room, tap for the lamps and
scenes, swipe to dim. No entity lists, no technical names, nothing to maintain
when a lamp is added or replaced.

## Strategy

1. **Rooms, not lamps.** Every room is a single
   [Hue-Like Light Card](https://github.com/Gh61/lovelace-hue-like-light-card)
   (installed from the Marketplace). It shows the room in the colour of its lit
   lamps and has a switch and a brightness slider. Tap opens the Hue-style
   screen with the individual lamps and scenes. Hold opens HA's more-info
   dialog.
2. **Self-maintaining membership.** Each room card is wrapped in
   `custom:auto-entities` with this filter:
   `domain: light` + `area: <area_id>` + `label: verlichting`.
   - A new lamp appears in the right room once it has the right area and the
     `verlichting` label.
   - A dead lamp disappears as soon as it is removed.
   - `show_empty: false` hides a room with no lamps.
3. **The `verlichting` label is the contract.**
   - Every real lamp carries it.
   - Non-lamps that are `light.*` entities do not, e.g. the kiosk screen
     `light.kiosk_woonkamer_screen`.
   - Light **groups** (`light.keuken_spots`, `light.ouderkamer_verlichting_groep`,
     `light.tuinlicht`) also carry the label, so the "Alles uit" chip can use
     it. They are excluded per room card by `entity_id`, so their members are
     not shown twice.
   - When a new group is added to the house, add it to the room card's
     `exclude:` and to the count template.
4. **Floors as sections.** The view is a `sections` view with `max_columns: 4`,
   one section per floor, each opening with a `heading` card:
   - **Overzicht**
   - **Beganegrond**: Woonkamer is full width because it is the main room with
     the most lamps; Keuken and Hal are half width.
   - **Boven**: Ouderkamer, Kinderkamer, Trappenhuis and Zolder, 2×2.
   - **Buiten**: Tuin and Oprit.

   Half-width cards (`grid_options.columns: 6`) give two rooms per row on a
   phone and stay readable on a tablet or desktop.
5. **Overview chips** (`custom:mushroom-chips-card`):
   - A live count of lamps on. It uses the label and leaves out the groups.
   - **Alles uit**: `light.turn_off` on `label_id: verlichting`, with a
     confirmation.
   - **Buiten uit**: `light.turn_off` on areas `tuin` + `oprit`, with a
     confirmation.

   - **Nieuwe scène**: navigates to `/config/scene/edit/new`. HA's own scene
     editor takes over the current light states and assigns the area, so the
     new scene shows up in the room's Hue screen. Existing scenes are edited
     through hold → settings.

   Actions use `perform-action` and never templates (HA does not allow
   templates in dashboard actions).
6. **Scenes.** `sceneProvider: [ha-scenes, scene-presets]`, so both HA scenes in
   the area and the Hue-style presets of the Scene Presets integration show up
   on the Hue screen. These are the same presets the presence-lighting
   blueprint and the button controllers use.
7. **Consistent look.** Every card uses the area's own icon and
   `offColor: '#363636'`, so off rooms read as dark tiles rather than bright
   grey.

## Area → card map

| Section | Card | `area` | Excluded |
|---|---|---|---|
| Beganegrond | Woonkamer (full width) | `woonkamer` | `light.kiosk_woonkamer_screen` |
| Beganegrond | Keuken | `keuken` | `light.keuken_spots` |
| Beganegrond | Hal | `hal` | – |
| Boven | Ouderkamer | `slaapkamer` | `light.ouderkamer_verlichting_groep` |
| Boven | Kinderkamer | `kinderkamer` | – |
| Boven | Trappenhuis | `trappenhuis` | – |
| Boven | Zolder | `zolder` | – |
| Buiten | Tuin | `tuin` | `light.tuinlicht` |
| Buiten | Oprit | `oprit` | – |

Areas without lamps (Badkamer, Garage, Meterkast, CV ruimte) have no card.

## Lamp icons

Icons are set on the light entities themselves (entity registry), not in the
dashboard, using **Hass Hue Icons** (`hue:` prefix, real fixture shapes):

| Fixture | Icon | Lamps |
|---|---|---|
| Round ceiling light (Innr RCL 232 C and similar) | `hue:ceiling-round` | plafond lamps (hal ×2, keuken, piano, trappenhuis), kinderkamer, zolder overloop |
| Spot (Innr RS 232 C) | `hue:bulb-spot` / group `hue:bulb-group-spot` | keuken spots |
| Bedside/table lamp | `hue:table-shade` | nachtlampjes Juul/Maurice, kinderhoek |
| Children's bear night lamp | `mdi:teddy-bear` | nachtlampje kleine beer |
| Floor lamp | `hue:floor-shade` | groene stalamp |
| Pendant | `hue:pendant-round` | eettafel, bar |
| Under-bed strip | `hue:lightstrip` | bed onder |
| Outdoor wall lantern | `hue:wall-lantern` | oprit voordeur, garage, afdak 1/2 |
| Floodlight | `hue:flood` | pergola |
| Other groups | `hue:bulb-group-classic`, `mdi:string-lights` (tuinlicht) | |

The full icon list is in the `hass-hue-icons.js` bundle of
arallsopp/hass-hue-icons. `hue:` icons render wherever dashboard resources load
(web UI, Companion app), not in native OS widgets.

## Checklist when lamps change

- New or replaced lamp: set its area, add the `verlichting` label and give it
  the fixture icon from the table above.
- New light group: give it the `verlichting` label, then add it to the
  `exclude:` of its room card and to the `reject('in', [...])` list in both
  count-chip templates.
- New room with lamps: copy an existing auto-entities block and change
  `title`, `icon`, `area`.
