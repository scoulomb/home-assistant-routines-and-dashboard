# Cinema Script

## What it does

### Cinema On

When triggered, the script:
1. **Powers on** the Denon AVR-X2700H (via Denon AVR integration — supports standby wake)
2. **Selects** 8K / Apple TV input (via HEOS `media_player.play_media`)
3. **Sets volume** to 45%
4. **Dims** bedroom lights to ~10%
5. **Turns on** the Optoma projector (via IR)

### Cinema Off

Reverse operation:
1. **Turns off** the Optoma projector (via IR)
2. **Powers off** the AVR
3. **Restores** bedroom lights to full brightness

## How to trigger

| Trigger | How |
|---|---|
| **Dashboard** | `Cinema On` / `Cinema Off` buttons on the [Global Dashboard](../../2-dashboards/global-dashboard/global-dashboard.yaml) |
| **Physical button** | [Automation](../../automations/cinema-automation.yaml) maps Hue button press → `script.cinema_on` / `script.cinema_off` |

## Why a script (not a scene)

Scenes can only set entity states — they cannot call other scripts or services like `media_player.play_media`. Since cinema mode involves powering on the AVR, selecting an input via HEOS, and sending IR commands to the Optoma, a script is required.

## Dependencies

- [heos-avr-scripts.yaml](../heos-avr/heos-avr-scripts.yaml) — AVR power and input selection
- [ir-scripts.yaml](../zigbee-tuya-ir-module-with-slzb/ir-scripts.yaml) — Optoma IR control (`script.optoma_on` / `script.optoma_off`)
