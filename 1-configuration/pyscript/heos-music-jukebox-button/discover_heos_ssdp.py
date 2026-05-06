#!/usr/bin/env python3
"""Discover HEOS devices on the local network via SSDP."""

import socket
import http.client
import io
import re
import json
import random
import time
import telnetlib


HEOS_URN = "urn:schemas-denon-com:device:ACT-Denon:1"


# --- Utility functions ---


def ssdp_discover(service, timeout=5, retries=1, mx=3):
    """Send SSDP M-SEARCH and collect responses."""
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        "M-SEARCH * HTTP/1.1",
        "HOST: {0}:{1}",
        'MAN: "ssdp:discover"',
        "ST: {st}",
        "MX: {mx}",
        "", "",
    ])
    socket.setdefaulttimeout(timeout)
    responses = []
    for _ in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        msg_bytes = message.format(*group, st=service, mx=mx).encode("utf-8")
        sock.sendto(msg_bytes, group)
        while True:
            try:
                data = sock.recv(4096)
                responses.append(data)
            except socket.timeout:
                break
        sock.close()
    return responses


def parse_ssdp_response(data):
    """Parse raw SSDP response bytes into a dict of headers."""
    class _FakeSocket(io.BytesIO):
        def makefile(self, *args, **kw):
            return self

    r = http.client.HTTPResponse(_FakeSocket(data))
    r.begin()
    return dict(r.getheaders())


def heos_command(host, cmd):
    """Send a HEOS command via telnet and return parsed JSON response(s)."""
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
    # Return the last response with a payload, or the last one
    for r in reversed(results):
        if "payload" in r:
            return r
    return results[-1] if results else None


# --- Discovery functions ---


def discover_devices():
    """Discover HEOS devices via SSDP and return list of {host, location}."""
    raw_responses = ssdp_discover(HEOS_URN, timeout=5, retries=2)
    seen_hosts = set()
    devices = []

    for data in raw_responses:
        headers = parse_ssdp_response(data)
        location = headers.get("LOCATION", "")
        st = headers.get("ST", "")

        if st != HEOS_URN:
            continue

        match = re.match(r"http://([^:]+):", location)
        if not match:
            continue

        host = match.group(1)
        if host in seen_hosts:
            continue
        seen_hosts.add(host)
        devices.append({"host": host, "location": location})

    return devices


def get_players(host):
    """Get all players reachable from a HEOS device."""
    return heos_command(host, "player/get_players")


# --- Browse functions ---


def browse_qobuz_favorites(host):
    """Browse Qobuz library favorite tracks."""
    sources = heos_command(host, "browse/get_music_sources")
    if not sources or "payload" not in sources:
        print("  Could not get music sources")
        return

    qobuz_sid = None
    for src in sources["payload"]:
        if src.get("name") == "Qobuz":
            qobuz_sid = src["sid"]
            break

    if qobuz_sid is None:
        print("  Qobuz not found in music sources")
        return

    print(f"\n  Qobuz source found (sid={qobuz_sid})")

    # Browse Qobuz > Library
    library = heos_command(host, f"browse/browse?sid={qobuz_sid}&cid=library-TYPE-container")
    if not library or "payload" not in library:
        print("  Could not browse Qobuz library")
        return

    # Browse Library > Tracks
    tracks = heos_command(host, f"browse/browse?sid={qobuz_sid}&cid=library_tracks-TYPE-container")
    if not tracks or "payload" not in tracks:
        print("  Could not browse favorite tracks")
        return

    print(f"  Qobuz Favorite Tracks ({len(tracks['payload'])} found):")
    for t in tracks["payload"]:
        print(f"    - {t.get('name')} — {t.get('artist')} (mid: {t.get('mid')}, album: {t.get('album')})")


def play_qobuz_favorites(host, pid, count=20):
    """Play random Qobuz favorite tracks on a given player (by pid)."""
    sources = heos_command(host, "browse/get_music_sources")
    if not sources or "payload" not in sources:
        print("  Could not get music sources")
        return False

    qobuz_sid = None
    for src in sources["payload"]:
        if src.get("name") == "Qobuz":
            qobuz_sid = src["sid"]
            break

    if qobuz_sid is None:
        print("  Qobuz not found in music sources")
        return False

    tracks = heos_command(host, f"browse/browse?sid={qobuz_sid}&cid=library_tracks-TYPE-container")
    if not tracks or "payload" not in tracks or not tracks["payload"]:
        print("  No favorite tracks found")
        return False

    # Randomly pick tracks
    all_tracks = tracks["payload"]
    selected = random.sample(all_tracks, min(count, len(all_tracks)))
    print(f"  Adding {len(selected)} random tracks to queue...")

    for i, track in enumerate(selected):
        mid = track.get("mid")
        if not mid:
            continue
        # First track: replace queue and play (aid=4), rest: add to end (aid=3)
        aid = 4 if i == 0 else 3
        result = heos_command(
            host,
            f"browse/add_to_queue?pid={pid}&sid={qobuz_sid}&cid=library_tracks-TYPE-container&mid={mid}&aid={aid}"
        )
        status = "ok" if result and result.get("heos", {}).get("result") == "success" else "FAILED"
        print(f"    [{status}] {track.get('name')} — {track.get('artist')}")

    print(f"  Playing {len(selected)} random Qobuz favorites on pid={pid}")
    return True


# --- Display functions ---


def print_players(devices):
    """Print all players reachable from each discovered device."""
    for dev in devices:
        print(f"  Host: {dev['host']}")
        print(f"  Location: {dev['location']}")

        try:
            result = get_players(dev["host"])
            if result and "payload" in result:
                print("  Players:")
                for player in result["payload"]:
                    print(f"    - {player.get('name')} (pid: {player.get('pid')}, ip: {player.get('ip')}, model: {player.get('model')})")
            else:
                print(f"  Raw response: {result}")
        except Exception as e:
            print(f"  Could not query players: {e}")
        print()


# --- Main ---
def main():
    print("Discovering HEOS devices via SSDP...")
    devices = discover_devices()

    if not devices:
        print("No HEOS devices found.")
        return

    print(f"\nFound {len(devices)} HEOS device(s):\n")
    print_players(devices)

    print("--- Qobuz Favorite Tracks ---")
    browse_qobuz_favorites(devices[0]["host"])

    # Play Qobuz favorites on Dressing device
    print("\n--- Playing Qobuz Favorites on Dressing ---")
    host = devices[0]["host"]
    result = get_players(host)
    if result and "payload" in result:
        dressing_pid = None
        for player in result["payload"]:
            if "dressing" in player.get("name", "").lower():
                dressing_pid = player["pid"]
                break
        if dressing_pid:
            play_qobuz_favorites(host, dressing_pid)
        else:
            print("  Dressing player not found")
    else:
        print("  Could not get players")


if __name__ == "__main__":
    main()
