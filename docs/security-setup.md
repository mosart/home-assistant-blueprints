# Security setup ("Beveiliging")

The owner's alarm logic lives in Home Assistant (not in this repo). This file
records the design so a later session can maintain it. Edit through the HA MCP
tools.

## Pieces

| Entity | Role |
|---|---|
| `alarm_control_panel.beveiliging` | Template alarm panel (UI helper). State = `input_select.beveiliging_status`. Code format `number`, no code needed to arm. Disarm calls `script.beveiliging_uitschakelen` with the code. |
| `input_select.beveiliging_status` | `disarmed` / `armed_away` / `triggered`. |
| `input_text.alarm_code` | The code (password mode, 4–8 digits). Empty = code disarm impossible. |
| `input_number.alarm_afteltijd` | Countdown minutes before the critical notification (default 10). |
| `input_boolean.oppas_thuis` | Manual "babysitter is home" switch. |
| label `vertrouwd` | On `device_tracker` entities of trusted people (babysitter). Any trusted tracker `home` blocks arming and disarms. |
| `script.beveiliging_inschakelen` | Status → armed_away, arms the UniFi Protect Alarm Manager (Away profile). |
| `script.beveiliging_uitschakelen` | Checks code (or `zonder_code: true` from automations). Wrong code: tablet camera snapshot to `/media/alarm/`, push to Juul and Maurice. Right code: status → disarmed, UniFi disarmed, lights restored from `scene.alarm_lichten_voor`, tablet back to its default dashboard. |
| `automation.beveiliging_aan_als_niemand_thuis_is` | Arms when Juul and Maurice are `not_home` 10 min, no babysitter, no trusted device, and all indoor occupancy sensors off for 10 min. Disarms (no code) when either comes home, the babysitter switch turns on, or a trusted device comes home. |
| `automation.beveiliging_alarm_gaat_af` | Indoor occupancy `on` while armed: status triggered, snapshot lights into `scene.alarm_lichten_voor`, all `verlichting` lights red 100 %, tablet screen on + built-in `security` view, oprit snapshot pushed, then every minute a TTS message on the tablet (Companion app `notify.mobile_app_tablet_woonkamer`, `alarm_stream_max`) counting down. After the countdown: critical push (Android alarm channel, iOS critical sound). `mode: single` on purpose so new motion does not restart the countdown. |
| dashboard `dashboard-beveiliging` | Admin only. Alarm panel, presence, babysitter switch, trusted devices, cameras, motion, settings, and all UniFi Wi-Fi trackers for marking `vertrouwd`. |

## Pitfalls

- Sonoff SNZB-03P raw motion entities latch `on`; use the `…_bezetting`
  occupancy entities (see `zha-device-notes`).
- A freshly created scene (`scene.create`) has state `unknown`, so do not gate
  its restore on its state.
- HA has no link to an alarm centre; the TTS text must not promise that
  emergency services are called.
- UniFi only creates trackers for clients listed in the integration's
  "client_source" option; it was emptied (= all clients) so Wi-Fi devices can be
  marked trusted.
