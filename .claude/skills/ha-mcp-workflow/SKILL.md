---
name: ha-mcp-workflow
description: How to work against the owner's live Home Assistant through the HA MCP tools — best-practices key, importing blueprints, editing automations/groups/scenes, quirks of the tools. Use before any change to the live Home Assistant instance.
---

# Working with the live Home Assistant (HA MCP)

The owner (Dutch speaker, writes Dutch; answer in Dutch, keep repo text English)
runs one live instance. Changes there are real: lights switch in a family home.
Say what you changed and what you did **not** test.

## Writes are gated by a rotating key
- `ha_config_set_automation`, `_set_helper`, `_set_scene`, `_set_script` reject
  calls without `BestPracticeKey` (`BPS_ACKNOWLEDGMENT_REQUIRED`).
- Fetch the key with any `ha_get_skill_guide(file='references/<x>.md')`; the
  first line reads `Acknowledgment key: I-HAVE-READ-THE-BEST-PRACTICES-GUIDE-…`.
  It **rotates hourly** — re-fetch on every rejection.
- Pass `BestPracticeKey=<key>` and `MandatoryBPS=false` (avoids the file being
  re-sent inline). Valid file names: SKILL.md, automation-actions.md,
  blueprint-guide.md, device-control.md, domain-docs.md, helper-selection.md,
  safe-refactoring.md, scenes.md, template-guidelines.md,
  triggers-and-conditions.md (all under `references/`), plus examples.yaml.
- The MCP server disconnects now and then; tools reappear after a moment. Load
  deferred tools with `ToolSearch select:<name>` and retry.

## Tool shapes that tripped me up
- `ha_config_get_automation(entity_id=…)` (not `identifier`). Returns
  `config_hash`.
- Edit an existing automation with `python_transform` + `config_hash`, e.g.
  `config['use_blueprint']['input']['x'] = 1`. A full `config=` rewrite works
  too but then every input must be repeated; an empty-string device input is
  rejected ("Unknown device ''").
- `ha_call_service(domain, service, data={...})`: put `entity_id` **inside
  `data`**. The separate `entity_id` argument does not accept a list.
- `ha_set_entity(entity_id, new_entity_id=…, labels=[…])` renames/labels; it
  does not rewrite consumers — search for the old id afterwards
  (`ha_search(query=…, search_types=[automation,script,scene,helper])`).
- Group helpers: `ha_config_set_helper(helper_type='group', helper_id=<entry_id>,
  action='update', config={'entities': [...]})`. List with
  `ha_config_list_helpers(helper_type='group')`.
- Scenes: update with `ha_config_set_scene(scene_id, config_hash,
  python_transform=…)`; `config['entities']` is a dict keyed by entity id.
- `ha_eval_template` is the way to test any Jinja before putting it in a
  blueprint (it sees real states). Test the *exact* expression with real
  values from the affected rooms.
- Area membership: `area_entities(...)`, labels: `Verlichting` is the lighting
  label (id `verlichting`) — put it on the light entity.
- `scene.create` scenes have state `unknown` until activated: test existence
  with `expand(entity) | count > 0`, not state.

## Blueprints in HA
- Import from GitHub **main**: `ha_manage_blueprints(action='import',
  url='https://github.com/mosart/home-assistant-blueprints/blob/main/<path>',
  overwrite=True)`. Importing reloads every automation using it.
- GitHub blob URLs can be served stale for a short time after a push; if a
  fresh branch version is needed before merging, import by **commit sha**
  (`…/blob/<sha>/<path>`).
- `ha_manage_blueprints(action='get')` returns the whole YAML (often >250 KB)
  and spills to a file: verify with
  `jq -r '.data.yaml' <file> | grep -c <new-input-name>` and check
  `.data.used_by`.
- Blueprint `source_url` should be the main-branch URL; every `[mosart]`
  blueprint in HA must come from main (stale branch URLs happen after
  importing from a branch).
- After any blueprint change: check all consuming automations are still `on`
  (`ha_search(query='presence', domain_filter='automation')`) and
  `ha_get_logs(source='system', search=<name>)` shows nothing new.
- Renaming/removing an input key breaks existing automations: keep keys, add
  new inputs with defaults, then migrate each automation's stored inputs.
- Input *types* are limited to HA's blueprint selectors. `ui_color` is not a
  blueprint selector (rejected: "Unknown selector type"); use `color_rgb`.
  No dependent/hidden fields, no thumbnails, no groups inside groups.
  Sections support `collapsed: true`, an icon and a description.

## Conventions the owner expects
- Descriptions of automations in Dutch, kept in sync with what they do.
- Do not leave things half-applied: after a test, restore what you toggled or
  say you left it changed.
- Ask before destructive/outward steps; otherwise just do it.

## Dashboards
- The lighting dashboard (`dashboard-verlichting`) design and maintenance rules
  live in `docs/lighting-dashboard.md` — read it before touching that dashboard.
- Lamps are found by the `verlichting` label + area; the label is the contract.
  When setting labels with `ha_set_entity`, `labels=[...]` REPLACES the list —
  read the entity's current labels first if it may have others.
- The dashboard screenshot beta is not enabled on this instance; visual checks
  are the owner's.
- Marketplace (2026.11+): installs fail with `warning_not_accepted` until the
  user the MCP server connects as has accepted the first-run notice. The owner
  accepting it in their own account did not unblock the MCP user. Removing
  repositories works without it.
- Frontend resources were cleaned up on 2026-11-05: only cards actually used by
  a dashboard remain (mushroom, auto-entities, card-mod, apexcharts,
  hue-like-light-card, hass-hue-icons, custom-brand-icons). Custom Brand Icons
  (`phu:` floor icons) was reinstalled by the owner via the Marketplace. ha_mcp_tools is installed from the mirror repo `homeassistant-ai/ha-mcp-integration`; the main repo `homeassistant-ai/ha-mcp` is now in the default catalog and installs the same component (switching is optional, owner informed).
  Before adding a card, check it is not already loaded; before removing one,
  search all dashboards (`ha_config_get_dashboard(query="custom:")`).
- Rooms with a Hue Smart Button (Ouderkamer, Kinderkamer): a light group
  `light.<room>_verlichting_groep` (area + `verlichting` label) is the
  blueprint's *Reference entity*; per button an `input_boolean` brightness
  toggle, per room one shared `input_text` slot helper. The group must be
  excluded from the room's dashboard card and from the "lampen aan" count
  (see `docs/lighting-dashboard.md`).
