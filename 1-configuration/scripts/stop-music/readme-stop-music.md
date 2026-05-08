# Stop Music Script

## What it does

When triggered, the script:
1. **Stops playback** on all HEOS speakers
2. **Ungroups** all HEOS speakers
3. **Turns off** Atoll preamp + DAC (bedroom) and Atoll preamp (living room) via IR

This is the reverse of `play_random_music` (without cutting the plugs — see below).

## Cut Music Plug

A separate `cut_music_plug` script just powers off the HiFi smart plugs (bedroom + living room). It is kept separate from `stop_music` so you can verify the system is properly turned off before cutting the plug. Also useful when the system is already off but plugs are still on, or when you want to cut power without stopping playback first.

## How to trigger

| Trigger | How |
|---|---|
| **Dashboard** | `Stop Music` button on the Global tab calls `script.stop_music` |
| **Dashboard** | `Cut Music Plug` button on the Global tab calls `script.cut_music_plug` |
| **Physical button** | [Automation](../../automation/stop-music-automation.yaml) maps Hue button press → `script.turn_on` → `script.stop_music` |
| **Physical button** | [Automation](../../automation/stop-music-automation.yaml) maps Hue button press → `script.turn_on` → `script.cut_music_plug` |

## Why a script (not a scene)

Same reasoning as [play-random-music](../play-random-music/readme-play-random-music.md#why-a-script-not-a-scene): stopping playback and sending IR commands require service calls, which scenes cannot do.

## Deploy

1. Ensure Atoll IR scripts are already configured (defined in [ir-scripts.yaml](../zigbee-tuya-ir-module-with-slzb/ir-scripts.yaml), also used in [HiFi dashboard](../../2-dashboards/hifi-dashboard/hifi-dashboard.yaml))
2. Deploy [stop-music-script.yaml](./stop-music-script.yaml): copy content into `scripts.yaml`, or drop the file into `/config/scripts/` if using `!include_dir_merge_named` (see [configuration.yaml](../../configuration.yaml))
3. Deploy [stop-music-automation.yaml](../../automation/stop-music-automation.yaml): copy content into `automations.yaml`, or drop the file into `/config/automations/` if using `!include_dir_merge_list` — replace the `device_id` and `subtype` with your button's values (discover via [Logbook](http://homeassistant.local:8123/logbook))
4. Add the dashboard button from [global-dashboard.yaml](../../2-dashboards/global-dashboard/global-dashboard.yaml) (Quick Actions section)
5. Reload from [Developer Tools → YAML](http://homeassistant.local:8123/developer-tools/yaml) (Scripts + Automations)
