# HEOS Qobuz Integration for Home Assistant

Play random Qobuz favorites on HEOS speakers from a Home Assistant dashboard button.

**Final solution: [pyscript](#3-final-solution-pyscript)** — native HA service, no timeouts, parameterized.

---

## 1. Discovery & Exploration

### `discover_heos_ssdp.py`

This script discovers HEOS devices on your network via SSDP, lists all players with their IPs/PIDs, browses Qobuz favorite tracks, and plays them on the Dressing device.

Use it for:
- Finding device IPs and player IDs (PIDs)
- Exploring Qobuz library structure (sources, containers, tracks)
- Testing playback before integrating into Home Assistant

```bash
python3 discover_heos_ssdp.py
```

---

## 2. First Approach: shell_command (archived)

> **Status: Archived** — kept in `archive/` for reference. Superseded by pyscript.

The first approach was a standalone Python script (`archive/play_qobuz_favorites.py`) invoked via HA's `shell_command`. It takes host IP, player name, and optional track count as arguments, and reads the HA token from `archive/ha_token.txt`.

```bash
python3 play_qobuz_favorites.py <host_ip> <player_name> [count]
python3 play_qobuz_favorites.py 192.168.8.190 dressing 20
```

### Setup (for reference)

<details>
<summary>Click to expand shell_command setup steps</summary>

#### Copy scripts and token to HA

Copy `play_qobuz_favorites.py` and `ha_token.txt` to `/config/scripts/` on your Home Assistant instance.

You can do this via:
- VS Code add-on: http://homeassistant.local:8123/a0d7b954_vscode/ingress
- Samba share add-on
- SSH/SCP

The `ha_token.txt` file must contain your long-lived access token (one line, no quotes).
Generate one at: http://homeassistant.local:8123/profile/security → **Long-Lived Access Tokens** → Create Token.

#### Add shell command in `configuration.yaml`

First test with a simple command to verify shell_command works:

**Option A — Direct execution (for ≤15 tracks, stays within 60s):**

```yaml
shell_command:
  hello: "echo hello"
  play_qobuz_dressing: "python3 /config/scripts/play_qobuz_favorites.py 192.168.8.190 dressing 15"
```

Simpler, but HA will kill the script after 60s if it hasn't finished.

**Option B — Background execution (recommended for 20+ tracks):**

```yaml
shell_command:
  hello: "echo hello"
  play_qobuz_dressing: "/bin/sh -c 'python3 /config/scripts/play_qobuz_favorites.py 192.168.8.190 dressing 42 &'"
```

The `&` backgrounds the Python process so HA returns immediately (avoids the 60s shell_command timeout).
Music starts playing after the first track is queued (~6s). Progress notifications are sent every 5 tracks.

**Notes**
- HA may show a "killed" notification in the UI, but the script is still running in the background — ignore it.
- Changing the shell_command value requires a full HA restart (**Settings → System → Restart**), not just a YAML reload. (not a full restart but required actually at each changes)
<!-- we could have passed HA token as arugment but set in a text file as more convenient and initially beleieve did not work ebcause had not reloaded (no fully tested) -->

#### Reload configuration

Go to http://homeassistant.local:8123/developer-tools/yaml and click the yellow arrow next to **"Shell Commands"** to reload (not the full reboot button at the top).

**Important**: The first time you add `shell_command:` to `configuration.yaml`, a reload is not enough. You need a full HA restart: **Settings → System → Restart**  (yellow arrow). Subsequent changes can be reloaded without restart (quick reload).

#### Dashboard button

In your dashboard YAML (e.g. `hifi-dashboard.yaml`):

```yaml
- type: button
  name: Play Qobuz Favorites (Dressing)
  icon: mdi:music-box
  tap_action:
    action: call-service
    service: shell_command.play_qobuz_dressing
```

Or create a standalone dashboard with only this button:

```yaml
views:
  - title: Qobuz
    cards:
      - type: vertical-stack
        cards:
          - type: button
            name: Play Qobuz Favorites (Dressing)
            icon: mdi:music-box
            icon_height: 60px
            tap_action:
              action: call-service
              service: shell_command.play_qobuz_dressing
```

#### Optional: HA script wrapper

In `scripts.yaml`:

```yaml
play_qobuz_favorites_dressing:
  alias: "Play Qobuz Favorites on Dressing"
  sequence:
    - action: shell_command.play_qobuz_dressing
```

Execute at: http://homeassistant.local:8123/config/script/dashboard

</details>

### Why we moved on

- **60s timeout** — HA kills `shell_command` after 60s; requires `&` backgrounding hack
- **Per-player duplication** — need a separate `shell_command` entry for each player
- **Token file on disk** — requires managing `ha_token.txt` manually
- **Spurious notifications** — HA shows "killed" in the UI even when the script is running fine
- **No parameters** — can't pass arguments dynamically from a dashboard button

### Alternative considered: HEOS API Server

Instead of running a Python script via `shell_command`, one could use an external [HEOS API Server](https://github.com/open-denon-heos/heos-api-server/tree/main/api-server) exposing HEOS commands as a REST API via Docker. Dismissed because it only supports one player and adds an external service to maintain.

---

## 3. Final Solution: pyscript

[pyscript](https://github.com/custom-components/pyscript) (installable via HACS) lets you write the Qobuz logic directly as a native HA service in Python — no `shell_command` timeout issues, no external server to maintain, and callable from automations/dashboards like any other HA service.

### Step 1: Install HACS

- HACS download: https://www.hacs.xyz/docs/use/download/download/
- HACS integration setup: https://www.hacs.xyz/docs/use/configuration/basic/

### Step 2: Add pyscript config to `configuration.yaml`

Edit via VS Code add-on: http://homeassistant.local:8123/a0d7b954_vscode/ingress

```yaml
pyscript:
  allow_all_imports: true
  hass_is_global: true
  legacy_decorators: true
```

Required for `telnetlib`, `json`, `random`, etc. Restart HA after adding.

### Step 3: Copy the pyscript file

Copy `play_qobuz_favorites_pyscript.py` to `/config/pyscript/` on HA.

### Step 4: Reload pyscript

Developer Tools → YAML → "Pyscript Python scripting" → Reload

### Step 5: Test the service

Developer Tools → Action → search `pyscript.play_qobuz_favorites` → switch to YAML mode → "Perform Action"

```yaml
action: pyscript.play_qobuz_favorites
data:
  host: "192.168.8.190"
  player_name: "dressing"
  count: 20
```

### Step 6: Dashboard button

```yaml
type: button
name: Qobuz → Dressing
icon: mdi:music-box
tap_action:
  action: perform-action
  perform_action: pyscript.play_qobuz_favorites
  data:
    host: "192.168.8.190"
    player_name: "dressing"
    count: 20
```

### Why pyscript wins

| | shell_command | pyscript |
|---|---|---|
| Timeout | 60s limit, needs `&` hack | No limit — native async |
| Parameters | Hardcoded per shell_command | Dynamic via service data |
| Token | Needs `ha_token.txt` on disk | Calls `persistent_notification.create()` directly |
| Multi-player | Separate entry per player | One service, pass `player_name` |
| Logging | External log file | HA native logs (Settings → System → Logs) |
| Lifecycle | HA can't track backgrounded process | HA manages it |

### Trade-offs

- Requires HACS + pyscript setup (GitHub OAuth, extra integration)
- Script must use pyscript conventions (`@service` decorator, `log.info()` instead of `print()`)
- `allow_all_imports: true` is a broad permission

---

## How it works (protocol details)

1. Connects to a HEOS device via telnet (port 1255)
2. Gets music sources → finds Qobuz (`sid=30`)
3. Browses Qobuz > Library > Tracks (`cid=library_tracks-TYPE-container`)
4. Randomly picks N tracks from favorites
5. Adds them to the player queue one by one:
   - First track: `aid=4` (replace queue and play)
   - Remaining: `aid=3` (add to end of queue)
6. Sends a persistent notification to HA with the queued track list
7. Writes a log file to `/config/scripts/qobuz_last_run.txt` (shell_command version only)

## Notifications

The script sends a persistent notification (bell icon in HA) at the start and end with the list of queued tracks.

- **pyscript version**: calls `persistent_notification.create()` directly — no token needed.
- **shell_command version** (archived): reads the token from `ha_token.txt` in the same directory as the script (e.g. `/config/scripts/ha_token.txt`). If the file is missing or empty, the script still works — it just skips the notification.

## Notes

- Adding a full Qobuz container at once does not work — tracks must be added individually
- The 3s sleep per command is needed for the HEOS telnet interface to respond
- `telnetlib` is deprecated in Python 3.12+ but still works; a socket-based replacement could be done later


## HEOS IP vs player vs source

The `host` IP is the HEOS device we connect to via telnet — it can be any HEOS device on the network (they all expose the same control API). This is distinct from:

- **Group leader player/device** — the player that controls playback for a group. The leader receives and decodes the full hi-res stream (keeping full quality for itself), then re-distributes to other group members which may receive a downsampled version (typically 48kHz/16-bit) depending on their capabilities and network conditions.
- **Source-owning player** — the player that owns a local input source (e.g. a HEOS Amp with analog/optical inputs). Note on local input sharing:
  - **HEOS Amp** inputs (optical/AUX) can be streamed to other HEOS devices (Denon Home, HEOS Link, etc.) without the Amp needing to be the group leader.
  - **AVR** inputs cannot be shared this way — the AVR must be the group leader to distribute its local input to other players.
  - **Stream quality**: when a local input is redistributed to other players, the stream is typically limited to 48kHz/16-bit regardless of the original source quality.

In our case, since Qobuz is a cloud source, the source player distinction does not apply.

**Group leader choice in our automation:**
- If you care about **connectivity/reliability** → set an Ethernet-connected player as leader (Bedroom in my case)
- If you care about **audio quality** → set a best capable player as leader (HEOS Link plugged to Atoll DAC 100 in my case — hi-res DAC, keeps full quality for itself)

<!-- OK CCL 3:30 am 6jan-->