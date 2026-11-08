---
name: blueprint-release
description: Git/PR/deploy workflow for this repo — branch rules, squash merge, why not to force-push, commit attribution, and the verify-then-import step into Home Assistant. Use when finishing any change to a blueprint.
---

# Release workflow for a blueprint change

The session branch (e.g. `claude/home-assistant-light-dimming-…`) is reused for
many changes. Each change is shipped the same way:

1. `git fetch origin main && git merge --no-edit origin/main` into the branch
   first. Earlier PRs are **squash-merged**, so the branch history never lines
   up with `main`; merging `main` in is fine. A conflict then usually comes from
   the squash: diff the old branch commit against the squash commit — an empty
   diff means keep the branch version (`git checkout --ours <file>`).
2. **Never force-push or rebase the pushed branch.** It is denied
   (`Git Destructive`). If histories diverge, merge `main` into the branch and
   push normally.
3. Validate: `python3 -m unittest discover -s scripts -p "test_*.py"`, parse the
   YAML with a loader that tolerates `!input`, check every `!input` key exists
   and every input key is used, and test new templates with `ha_eval_template`.
4. Update `README.md` in the same change (sections for the blueprint, field
   names exactly as in the UI). CLAUDE.md requires README to stay in sync.
5. Commit; end the message with the attribution lines the session reminder
   gives (Co-Authored-By + Claude-Session). No model names anywhere else.
6. `git push -u origin <branch>`; create the PR (`mcp__github__create_pull_request`,
   body = summary/testing, ends with the PR attribution lines); squash-merge
   with `expectedHeadSha`. The owner asks for the merge and the HA update as
   part of the job — do both, don't stop at the push.
7. Import into HA from `main` (see `ha-mcp-workflow`), verify with jq, check the
   consuming automations are on and the log is clean, then report in Dutch what
   changed, what was and wasn't tested, and anything that changes behaviour for
   existing rooms.

Related: the generated scene preset option block between the BEGIN/END markers
must be regenerated with `scripts/generate_scene_presets_options.py`, never
hand-edited. Adding a blueprint that uses it means adding its path to
`BLUEPRINT_PATHS` in that script.

## Adding a required input to a live blueprint
Every automation on the blueprint fails to load ("Missing input <key>") from
the moment the new version is imported until its stored inputs get the new
key. Keep that window short: create any helper the input needs first, import,
then update every automation in `used_by` straight away (the errors in the
log from those seconds are expected). Inputs dropped from a blueprint can be
removed from the stored config at the same time; HA ignores extra stored
inputs, so leaving them is harmless but confusing.
