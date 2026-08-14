# Contributing

Thanks for taking the time. A few things up front, so nobody's expectations get
bruised.

## What this repository is

A personal collection. Each blueprint was written to solve a problem in my own
house, and is published because someone else might have the same problem. It is
not a product and there is no support commitment behind it.

That means:

- Issues may sit unanswered for a while. Bumping a thread does not speed it up.
- Fixes land when they land.
- A blueprint may be changed or removed if my own setup changes. Pin a copy in
  your own configuration if that matters to you.

## Before opening an issue

Please check that the problem is with the blueprint itself rather than with
Home Assistant, ZHA, or the `scene_presets` integration. A quick way to tell:
open the automation, go to **Traces**, and look at whether the expected branch
ran.

## Reporting a bug

Include at minimum:

- Home Assistant version and installation type
- Which blueprint, and the version line from its description
- The device model and how it is paired
- The relevant `zha_event` output. Developer Tools → Events → listen to
  `zha_event`, press the button, and paste what appears
- The automation trace, or at least the timeline tab

Reports without event output are hard to act on, because the whole class of
problems this blueprint runs into comes down to which commands a particular
firmware sends.

## Requesting device or integration support

These blueprints deliberately target one device on one integration. Requests to
add Zigbee2MQTT, deCONZ, or other remotes will usually be declined, not because
the idea is bad but because I cannot test what I do not own, and an untested
branch is worse than no branch.

If you want that support, forking is the right move. No permission needed, and
no need to ask first.

## Pull requests

Welcome, with two requests:

- Keep the diff small and focused on one thing.
- Say how you tested it, and on what hardware.

Cosmetic reformatting of whole files will be declined, since it makes future
diffs unreadable.

## Licence

By contributing you agree that your contribution is licensed under the
EUPL-1.2, the same licence as the rest of this repository.
