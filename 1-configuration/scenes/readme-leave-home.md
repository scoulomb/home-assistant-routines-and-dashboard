# Leave Home Scene

## What it does

When triggered, the scene:
- Turns **off** all lights
- **Deploys** bedroom sunilus at 50%

## How to trigger

| Trigger | How |
|---|---|
| **Dashboard** | `Leave Home` button on the Global tab calls `scene.leave_home_ha` |
| **Physical button** | [Automation](../automation/leave-home-automation.yaml) maps Hue button press → `scene.turn_on` → `scene.leave_home_ha` |

## Why a scene (not a script or automation)

Same reasoning as [Go to Bed](./readme-go-to-bed.md#why-a-scene-not-a-script-or-automation): the routine only sets entity states (lights off, shutter position), so a scene is the right HA primitive.

## Deploy

1. Deploy [leave-home-scene.yaml](./leave-home-scene.yaml): copy content into `scenes.yaml`, or drop the file into `/config/scenes/` if using `!include_dir_merge_list` (see [configuration.yaml](../configuration.yaml))
2. Deploy [leave-home-automation.yaml](../automation/leave-home-automation.yaml): copy content into `automations.yaml`, or drop the file into `/config/automations/` if using `!include_dir_merge_list` — replace the `device_id` and `subtype` with your button's values (discover via [Logbook](http://homeassistant.local:8123/logbook))
3. The dashboard button already exists in [global-dashboard.yaml](../../2-dashboards/global-dashboard/global-dashboard.yaml) (Quick Actions section)
4. Reload from [Developer Tools → YAML](http://homeassistant.local:8123/developer-tools/yaml) (Scenes + Automations)

## Sunilus position note

`current_position: 50` sets the sunilus at 50% deployed. Adjust to taste (e.g. `75` for more shade, `25` for less).
