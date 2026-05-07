# Go to Bed Scene

## What it does

When triggered, the scene:
- Turns **off** all lights except bedroom
- **Dims** bedroom light (~10%)
- **Closes** living room shutter
- **Opens** bedroom sunilus

## How to trigger

| Trigger | How |
|---|---|
| **Dashboard** | `Go to Bed` button on the Global tab calls `scene.go_to_bed_ha` |
| **Physical button** | Automation maps button press → `scene.turn_on` → `scene.go_to_bed_ha` |

## Why a scene (not a script or automation)

A scene captures a **desired state** for multiple entities in one entity (`scene.go_to_bed_ha`).  
It can be triggered from anywhere — dashboard, button, voice assistant, or other automations — without duplicating logic.

## Deploy

1. Copy [go-to-bed-scene.yaml](./go-to-bed-scene.yaml) content into `scenes.yaml` on the HA instance (via [VS Code add-on](http://homeassistant.local:8123/a0d7b954_vscode/ingress))
2. Copy [go-to-bed-automation.yaml](../automation/go-to-bed-automation.yaml) content into `automations.yaml`, replacing `YOUR_HUE_DIMMER_DEVICE_ID` with your button's device ID (Settings → Devices)
3. Reload from [Developer Tools → YAML](http://homeassistant.local:8123/developer-tools/yaml) (Scenes + Automations)

## Brightness note

`brightness: 25` is ~10% on the 0–255 scale. Adjust to taste (e.g. `64` for ~25%, `13` for ~5%).

## Wake Up scene

The [wake-up-scene.yaml](./wake-up-scene.yaml) works the same way (scene + [automation](../automation/wake-up-automation.yaml) + dashboard button) but does the opposite: opens living room shutter and closes bedroom sunilus. Lights are not touched.
