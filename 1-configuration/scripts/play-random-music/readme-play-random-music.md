# Play Random Music Script

## What it does

When triggered, the script:
1. **Powers on** HiFi plugs (bedroom + living room)
2. **Turns on** Atoll preamp + DAC (bedroom) and Atoll preamp (living room) via IR
3. **Selects input** — tuner on bedroom preamp, tape on living room preamp
4. **Ungroups** all HEOS speakers (avoids grouping issues)
5. **Groups** all HEOS speakers under HEOS Link (via native HA `media_player.join`)
6. **Plays** random Qobuz favorites via pyscript (telnet to HEOS API)

A lighter variant `launch_new_jukebox` skips steps 1–5 and only plays new random tracks (assumes the system is already on and grouped).

Note: turning on plugs could be done via a scene (it's just entity state),
but keeping everything in one script avoids splitting logic across two places.

## How to trigger

| Trigger | How |
|---|---|
| **Dashboard** | `Play Music` button on the Global tab calls `script.play_random_music` |
| **Dashboard** | `New Jukebox` button on the Global tab calls `script.launch_new_jukebox` (system already on) |
| **Physical button** | [Automation](../automation/play-random-music/play-random-music-automation.yaml) maps Hue button press → `script.turn_on` → `script.play_random_music` |
| **Dashboard (direct pyscript)** | A button can also call `pyscript.play_qobuz_favorites` directly with custom `data:` (see [pyscript docstring](../pyscript/heos-music-jukebox-button/play_qobuz_favorites_pyscript.py)) |

## Why a script (not a scene)

The [Go to Bed](../scene/readme-go-to-bed.md) routine uses a **scene** because it captures a **desired state** for multiple entities (lights off, shutter closed, etc.). A scene is essentially a snapshot of entity states that HA applies when activated.

Playing random music **cannot** use a scene because:

1. **Scenes only set entity states** — they declare "light X should be off, cover Y should be closed". They cannot call services or execute logic.
2. **Playing music requires a service call** — we need to invoke `pyscript.play_qobuz_favorites`, which runs Python code (telnet to HEOS, browse Qobuz, randomize tracks, queue them). There is no entity whose "state" we can set to achieve this.
3. **A script is the HA primitive for executing actions** — it runs a sequence of service calls, just like an automation's `action:` block, but packaged as a callable entity (`script.play_random_music`).

| | Scene | Script |
|---|---|---|
| **Purpose** | Set entities to a desired state | Execute a sequence of actions |
| **Example** | Turn off lights, close shutters | Call pyscript, send notifications |
| **Entity** | `scene.xxx` | `script.xxx` |
| **Can call services** | No | Yes |
| **Triggerable from dashboard/button/voice** | Yes | Yes |

Both scenes and scripts produce an entity that can be triggered from the dashboard, automations, physical buttons, or voice assistants — so the end-user experience is identical.

## Deploy

1. Ensure [play_qobuz_favorites_pyscript.py](../pyscript/heos-music-jukebox-button/play_qobuz_favorites_pyscript.py) is deployed to `/config/pyscript/` and pyscript is configured with `allow_all_imports: true`
2. Ensure Atoll IR scripts are already configured in `scripts.yaml` (defined in [ir-scripts.yaml](../script/zigbee-tuya-ir-module-with-slzb/ir-scripts.yaml), also used in [HiFi dashboard](../../2-dashboards/hifi-dashboard/hifi-dashboard.yaml))
3. Deploy [play-random-music-script.yaml](./play-random-music-script.yaml): copy content into `scripts.yaml`, or drop the file into `/config/scripts/` if using `!include_dir_merge_named` (see [configuration.yaml](../../configuration.yaml))
4. Deploy [play-random-music-automation.yaml](../automation/play-random-music/play-random-music-automation.yaml): copy content into `automations.yaml`, or drop the file into `/config/automations/` if using `!include_dir_merge_list` — replace the `device_id` and `subtype` with your button's values (discover via [Logbook](http://homeassistant.local:8123/logbook))
5. Add the dashboard button from [global-dashboard.yaml](../../2-dashboards/global-dashboard/global-dashboard.yaml) (Quick Actions section)
6. Reload from [Developer Tools → YAML](http://homeassistant.local:8123/developer-tools/yaml) (Scripts + Automations + Pyscript)

## Parameters

Default values in the script (can be changed in `play-random-music-script.yaml`):

| Parameter | Default | Description |
|---|---|---|
| `host` | `192.168.8.190` | HEOS device IP |
| `player_name` | `link` | Target speaker / group leader (partial, case-insensitive match) |
| `count` | `20` | Number of random tracks to queue |
