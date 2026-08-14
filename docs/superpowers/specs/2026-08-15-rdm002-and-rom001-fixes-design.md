# Design: RDM002 blueprint, ROM001 dropdown fixes, and helper-naming guidance

Date: 2026-08-15

## Problem

Two things came out of using the ROM001 blueprint for real:

1. Its preset dropdown has two defects: after picking a preset, the field
   shows the raw UUID instead of the label once closed (so a month later you
   can't tell what's selected), and the list is alphabetized instead of
   following the Scene Presets panel's own category grouping.
2. There's a second Hue remote — the Tap Dial Switch (RDM002) — that should
   get its own blueprint, built the same way (Scene Presets integration,
   ZHA-only, self-contained), but its hardware is different enough that it
   isn't a copy-paste of ROM001: 4 independent buttons instead of 1, and a
   real rotary dial instead of a simulated hold-to-dim.

Also requested: a suggested name/icon for the `input_boolean` helper ROM001
needs, ideally created without leaving the blueprint's input form; and a
README that reads well with two blueprints instead of one.

## Investigated ceiling

Verified against real HA frontend/core source (cloned and read directly),
same standard as prior investigations in this repo:

- **Inline helper creation already exists, no blueprint change needed.**
  HA's entity picker shows a "+ Create input_boolean" option in its dropdown
  automatically whenever a blueprint input uses
  `selector: entity: domain: input_boolean` — which `direction_helper`
  already does. Confirmed in `ha-entity-picker.ts` and `selector.ts`'s
  `computeCreateDomains`.
- **A blueprint cannot suggest or pre-fill a name for that helper.** The
  create-helper dialog HA opens takes only a `domain` and a close-callback —
  no name parameter exists anywhere in its signature. The name field is
  always blank, freely typed by the user.
- **A blueprint cannot create a helper via a service call either.** Helpers
  are storage-collection-backed; `input_boolean`'s only registered services
  are `reload`/`turn_on`/`turn_off`/`toggle`. Creation is a websocket-only
  operation, not reachable from an automation `action:` sequence.
- **Blueprint input descriptions can't reference sibling input values.**
  Confirmed in `blueprint/schemas.py` (descriptions are plain `str`, not
  `cv.template`) and the frontend's input-row renderer (no cross-input
  context passed in). A description can't compute "Suggested name:
  `Hue Smart Button - <the area you picked above> - ...`" — there's no
  templating on that path at all, and no access to other inputs' live
  values even if there were.

Net effect: the best available implementation is a **static, generic
suggested-naming-pattern sentence** in `direction_helper`'s description,
next to the button that already lets you create the helper inline. Nothing
dynamic is possible; this is a hard ceiling, not an oversight.

## Design

### 1. ROM001: selector and generator fixes

- Blueprint's `preset_short`/`preset_double` selector drops `custom_value:
  true` (routes rendering through the older `ha-select` component, which
  correctly resolves a stored value back to its label — confirmed this is
  the actual root-cause fix, not a workaround) and drops `sort: true` (so
  the generated list's own order is what's displayed, not an alphabetical
  re-sort).
- Generator's `build_options` changes from sorting by label to a **stable
  sort by each preset's category's position in the upstream `categories`
  array** — this reproduces the Scene Presets panel's own order exactly
  (verified directly against live `presets.json`: the `presets` array is
  already grouped in that same category order, "Defaults" first).
- Trade-off accepted: dropping `custom_value` removes the "type a raw ID for
  a locally-added preset" escape hatch. Given the readability cost fell on
  100% of users while the escape hatch benefited only users with local
  presets, and pinned-favorites was already declined for the same
  simplicity reason, this is the right call.
- `direction_helper`'s `description` gains one line: a suggested naming
  pattern (`<Blueprint name> - <area/light> - <function>`, e.g.
  `Hue Smart Button - Ouderkamer - Brightness toggle`) and the icon
  recommendation `mdi:brightness-6`, positioned so it's visible right where
  the existing (unmodified) "+ Create input_boolean" picker button is.

### 2. New blueprint: RDM002 (Hue Tap Dial Switch)

`controllers/hue_tap_dial_rdm002/hue_tap_dial_rdm002.yaml`, following the
existing `controllers/<device_slug>/<device_slug>.yaml` convention.

Structurally different from ROM001, not a copy:

- **No hold-based interaction anywhere.** A held button on this device
  emits a `LevelControl.step_with_on_off` frame indistinguishable from a
  real left dial-turn (upstream zigpy/zha-device-handlers#3696); the quirk
  partially filters this before it becomes a `zha_event`, but the filter is
  known-incomplete. Building on `button_N_hold` would inherit that
  ambiguity. A YAML comment documents this inherited limitation; no
  additional filtering is added in the blueprint itself (duplicating the
  quirk's internal threshold would be fragile and presumptuous).
- **No direction helper, no reference-light input.** The dial reports real
  bidirectional rotation directly (`step_mode`: 0=up/1=down), so there's
  nothing to track across triggers the way ROM001's drifting internal
  counter required.
- **No on/off-toggle logic on buttons.** Each short press applies its
  configured preset directly — matches the "4 configurable presets" shape
  chosen over "on/off + 2 presets".

**Inputs:**
- `remote` — device selector, `filter: integration: zha, model: RDM002`
  (manufacturer string is unreliable here too — reports as either `Philips`
  or `Signify Netherlands B.V.` depending on firmware, same lesson as
  ROM001).
- `lights` — target selector, `domain: light`.
- `button_1_short` … `button_4_short` — required preset selects (4).
- `button_1_double` … `button_4_double` — optional preset selects (4),
  `default: ""`, skipped at run time if left unset.
- All 8 share the exact same generated option list via one YAML anchor
  defined on the first input and aliased on the other 7 — same list content
  as ROM001's, generated by the same script run.
- `dial_max_step` — number, %, default 10: brightness change for the
  fastest dial spin; slower spins scale down proportionally against the
  hardware's own `step_size` (0–255).
- `transition` — number, seconds, mirrors ROM001's input.

**Triggers:** 8 `id`-tagged `zha_event` triggers (`button_N_press` /
`button_N_double_press` for N in 1–4), plus 1 for the dial's
`step_with_on_off` LevelControl event, filtered by `device_id: !input
remote`.

**Actions:** a `choose:` block, same pattern as ROM001 (`condition: trigger,
id: <id>`):
- Short press → `scene_presets.apply_preset` with that button's preset,
  unconditionally (required input).
- Double press → same call, but wrapped in `if: condition: template` that
  checks the corresponding `!input` (captured into `variables:` at the top
  of the automation, same pattern ROM001 already uses for `dim_step`) is
  non-empty after trimming; skipped otherwise.
- Dial rotation → `light.turn_on` with `brightness_step_pct` computed from
  `step_size / 255 * dial_max_step`, signed by `step_mode` (compared as a
  string, since this cluster's fields are known to serialize inconsistently
  across HA versions — the same defensive pattern already used for
  ROM001's `step_mode` on its `step` trigger), and `transition: !input
  transition`.
- `mode: queued`, `max: 50` (raised from ROM001's 25 — a fast dial spin can
  emit more rotation events in quick succession than a held button did),
  `max_exceeded: silent`.

The `default: ""` behavior for an unmatched `select` value (no options entry
has value `""`) is expected to render as a blank/unset field — this is a
minor, low-risk assumption about picker fallback behavior that will be
confirmed during the same real-HA manual verification step this project has
consistently used to close out any remaining device/frontend unknowns; it
is not treated as a blocking design question.

### 3. Generator script: multi-file support

`BLUEPRINT_PATH` (singular) becomes `BLUEPRINT_PATHS` (a list containing
both blueprint files). `main()` fetches upstream data and builds the option
list once, then loops over each path, splicing that same list into each
file's own independent marker pair and reporting a count per file. No
change to `build_options`, `render_options_yaml`, or `splice_generated_block`
themselves — they're already file-content-agnostic (they operate on
whatever text and markers they're given), so this is purely a `main()`
change plus the constant becoming a list.

### 4. README restructuring

Adds a second `###`-level subsection for RDM002, mirroring ROM001's
existing structure (behaviour table, import badge, requirements,
preset-selection notes reusing the same "Choosing presets" wording since
both blueprints share the same preset-picking mechanism). The existing
"Why these are self-contained" and "Issues and contributions" sections
apply to both blueprints already and don't need duplicating.

## Explicitly out of scope

- GitHub Pages presentation — raised as a "bonus" idea, explicitly deferred
  by the user to its own separate round of work.
- Any dynamic/computed helper-name suggestion — confirmed impossible above,
  not attempted.
- Extra blueprint-side filtering for the hold/left-rotation collision bug
  beyond what the quirk itself already does — would duplicate an internal
  implementation detail of the quirk in a fragile way; documented via
  comment instead.
- A "pinned presets" or custom-value escape hatch for either blueprint's
  preset pickers — already declined in the original preset-select design,
  reinforced by this round's finding that `custom_value` actively breaks
  label display for everyone.
