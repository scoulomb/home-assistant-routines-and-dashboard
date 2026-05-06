"""Pyscript service: Play random Qobuz favorite tracks on a HEOS player.

Install: Copy this file to /config/pyscript/play_qobuz_favorites_pyscript.py
Requires: pyscript integration with allow_all_imports: true in configuration.yaml:

    pyscript:
      allow_all_imports: true

Reload: Developer Tools → YAML → Pyscript Python scripting

Dashboard button:
    type: button
    name: Play Qobuz Favorites (Dressing)
    icon: mdi:music-box
    tap_action:
      action: perform-action
      perform_action: pyscript.play_qobuz_favorites
      data:
        host: "192.168.8.190"
        player_name: "dressing"
        count: 20
"""

import json
import random
import telnetlib
import time


def heos_command(host, cmd):
    """Send a HEOS command via telnet and return parsed JSON response."""
    tn = telnetlib.Telnet(host, 1255, timeout=10)
    tn.write(f"heos://{cmd}\r\n".encode("utf-8"))
    time.sleep(3)
    resp = tn.read_very_eager().decode("utf-8")
    tn.close()
    results = []
    for line in resp.strip().split("\r\n"):
        if line.strip():
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    for r in reversed(results):
        if "payload" in r:
            return r
    return results[-1] if results else None


def get_player_pid(host, player_name):
    """Find player PID by name (case-insensitive partial match)."""
    result = heos_command(host, "player/get_players")
    if not result or "payload" not in result:
        return None
    for player in result["payload"]:
        if player_name.lower() in player.get("name", "").lower():
            return player["pid"]
    return None


@service
def play_qobuz_favorites(host="192.168.8.190", player_name="dressing", count=20):
    """Play random Qobuz favorite tracks on a HEOS player."""
    log.info(f"play_qobuz_favorites: host={host} player={player_name} count={count}")

    pid = get_player_pid(host, player_name)
    if not pid:
        log.error(f"Player '{player_name}' not found")
        persistent_notification.create(message=f"Player '{player_name}' not found", title="Qobuz (error)")
        return

    log.info(f"Found player '{player_name}' (pid={pid})")

    sources = heos_command(host, "browse/get_music_sources")
    if not sources or "payload" not in sources:
        log.error("Could not get music sources")
        persistent_notification.create(message="Could not get music sources", title="Qobuz (error)")
        return

    qobuz_sid = None
    for src in sources["payload"]:
        if src.get("name") == "Qobuz":
            qobuz_sid = src["sid"]
            break

    if qobuz_sid is None:
        log.error("Qobuz not found in music sources")
        persistent_notification.create(message="Qobuz not found in music sources", title="Qobuz (error)")
        return

    tracks = heos_command(host, f"browse/browse?sid={qobuz_sid}&cid=library_tracks-TYPE-container")
    if not tracks or "payload" not in tracks or not tracks["payload"]:
        log.error("No favorite tracks found")
        persistent_notification.create(message="No favorite tracks found", title="Qobuz (error)")
        return

    all_tracks = tracks["payload"]
    selected = random.sample(all_tracks, min(count, len(all_tracks)))
    persistent_notification.create(message=f"Starting: adding {len(selected)} random tracks to queue...", title="Qobuz")

    track_list = []
    for i, track in enumerate(selected):
        mid = track.get("mid")
        if not mid:
            continue
        aid = 4 if i == 0 else 3
        result = heos_command(
            host,
            f"browse/add_to_queue?pid={pid}&sid={qobuz_sid}&cid=library_tracks-TYPE-container&mid={mid}&aid={aid}"
        )
        status = "ok" if result and result.get("heos", {}).get("result") == "success" else "FAILED"
        log.info(f"[{status}] {track.get('name')} — {track.get('artist')}")
        if status == "ok":
            track_list.append(f"- {track.get('name')} — {track.get('artist')}")
        if len(track_list) % 5 == 0 and len(track_list) > 0:
            persistent_notification.create(
                message=f"Progress: {len(track_list)}/{len(selected)} tracks queued\n" + "\n".join(track_list[-5:]),
                title="Qobuz"
            )

    summary = f"Playing {len(track_list)} tracks on {player_name}\n" + "\n".join(track_list)
    log.info(f"Done: {len(track_list)} tracks queued")
    persistent_notification.create(message=summary, title="Qobuz")
