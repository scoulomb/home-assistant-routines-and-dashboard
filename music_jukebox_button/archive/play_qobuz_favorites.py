#!/usr/bin/env python3
"""Play random Qobuz favorite tracks on a HEOS player.
Usage: python3 play_qobuz_favorites.py <host_ip> <player_name> [count]
Example: python3 play_qobuz_favorites.py 192.168.8.190 dressing 20
"""

import sys
import json
import os
import random
import signal
import time
import telnetlib
import urllib.request


HA_URL = os.environ.get("HA_URL", "http://localhost:8123")
HA_TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ha_token.txt")
LOG_FILE = "/config/scripts/qobuz_last_run.txt"


def load_ha_token():
    """Load HA token from file."""
    try:
        with open(HA_TOKEN_FILE) as f:
            return f.read().strip()
    except Exception:
        return ""


HA_TOKEN = load_ha_token()


def handle_kill(signum, frame):
    """Log before being killed by HA timeout."""
    log_write(f"KILLED by signal {signum} at {time.strftime('%H:%M:%S')}")
    notify_ha(f"Script killed by signal {signum} at {time.strftime('%H:%M:%S')}", title="Qobuz (killed)")
    sys.exit(1)


signal.signal(signal.SIGTERM, handle_kill)
signal.signal(signal.SIGINT, handle_kill)


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


def notify_ha(message, title="Qobuz"):
    """Send a persistent notification to Home Assistant."""
    if not HA_TOKEN:
        log_write("  No HA_TOKEN provided, skipping notification")
        return
    url = f"{HA_URL}/api/services/persistent_notification/create"
    data = json.dumps({"message": message, "title": title}).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    })
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        log_write(f"  Notification failed: {e}")
        pass


def log_write(text, mode="a"):
    """Write to log file."""
    try:
        with open(LOG_FILE, mode) as f:
            f.write(text + "\n")
    except Exception:
        pass


def get_player_pid(host, player_name):
    """Find player PID by name (case-insensitive partial match)."""
    result = heos_command(host, "player/get_players")
    if not result or "payload" not in result:
        return None
    for player in result["payload"]:
        if player_name.lower() in player.get("name", "").lower():
            return player["pid"]
    return None


def play_qobuz_favorites(host, pid, count):
    """Play random Qobuz favorite tracks on a given player."""
    sources = heos_command(host, "browse/get_music_sources")
    if not sources or "payload" not in sources:
        print("Could not get music sources")
        return False

    qobuz_sid = None
    for src in sources["payload"]:
        if src.get("name") == "Qobuz":
            qobuz_sid = src["sid"]
            break

    if qobuz_sid is None:
        print("Qobuz not found in music sources")
        return False

    tracks = heos_command(host, f"browse/browse?sid={qobuz_sid}&cid=library_tracks-TYPE-container")
    if not tracks or "payload" not in tracks or not tracks["payload"]:
        print("No favorite tracks found")
        return False

    all_tracks = tracks["payload"]
    selected = random.sample(all_tracks, min(count, len(all_tracks)))
    log_write(f"Started: {time.strftime('%H:%M:%S')} — {len(selected)} tracks (token={'yes' if HA_TOKEN else 'no'})")
    notify_ha(f"Starting: adding {len(selected)} random tracks to queue...")
    print(f"Adding {len(selected)} random tracks to queue...")

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
        line = f"[{status}] {track.get('name')} — {track.get('artist')}"
        print(f"  {line}")
        log_write(f"  {line}")
        if status == "ok":
            track_list.append(f"- {track.get('name')} — {track.get('artist')}")
        if len(track_list) % 5 == 0 and len(track_list) > 0:
            notify_ha(f"Progress: {len(track_list)}/{len(selected)} tracks queued\n" + "\n".join(track_list[-5:]))

    summary = f"Playing {len(track_list)} tracks on pid={pid}\n" + "\n".join(track_list)
    log_write(f"Done: {time.strftime('%H:%M:%S')}")
    notify_ha(summary)
    print(f"Done. Playing {len(track_list)} tracks on pid={pid}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 play_qobuz_favorites.py <host_ip> <player_name> [count]")
        sys.exit(1)

    host = sys.argv[1]
    player_name = sys.argv[2]
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 17

    log_write(f"Args: host={host} player={player_name} count={count}", mode="w")

    pid = get_player_pid(host, player_name)
    if not pid:
        print(f"Player '{player_name}' not found")
        sys.exit(1)

    print(f"Found player '{player_name}' (pid={pid})")
    play_qobuz_favorites(host, pid, count)
