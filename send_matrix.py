#!/usr/bin/env python3
"""
send_message.py

Send a message to a Matrix room (inside a Space or standalone).
- First run with --user and --password to fetch and save access_token.
- Later runs will reuse the saved token automatically.
"""

import os
import sys
import time
import json
import requests

from get_creds import get_credentials, get_room
from get_stats import get_system_stats

TOKEN_FILE = "matrix_token.json"


def save_token(user_id, token, homeserver):
    data = {"user_id": user_id, "access_token": token, "homeserver": homeserver}
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)
    print(f"[INFO] Saved token to {TOKEN_FILE}")


def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)


def login(hs, user, password):
    url = hs.rstrip("/") + "/_matrix/client/v3/login"
    payload = {"type": "m.login.password", "user": user, "password": password}
    resp = requests.post(url, json=payload, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"Login failed: {resp.status_code} {resp.text}")
    data = resp.json()
    save_token(data["user_id"], data["access_token"], hs)
    return data["access_token"]


def resolve_room_id(hs, room, token):
    if room.startswith("!"):
        return room  # already a room_id
    url = hs.rstrip("/") + f"/_matrix/client/v3/directory/room/{room}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()["room_id"]


def join_room(hs, room_id, token):
    url = hs.rstrip("/") + f"/_matrix/client/v3/join/{room_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, headers=headers, json={}, timeout=10)
    if resp.status_code not in (200, 403):  # 403 = already joined
        raise RuntimeError(f"Join failed: {resp.status_code} {resp.text}")
    return resp.json()


def send_message(hs, room_id, token, message):
    txn_id = str(int(time.time() * 1000))
    url = hs.rstrip("/") + f"/_matrix/client/v3/rooms/{room_id}/send/m.room.message/{txn_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"msgtype": "m.text", "body": message}
    resp = requests.put(url, headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main():
    HOMESERVER= "https://matrix.org"
    USERNAME, PASSWORD = get_credentials()
    ROOM = get_room()
    
    MESSAGE = get_system_stats()

    # Load token from file or login
    token_data = load_token()
    if token_data and token_data.get("homeserver") == HOMESERVER:
        token = token_data["access_token"]
        print(f"[INFO] Using saved token for {token_data['user_id']}")
    else:
        if not USERNAME or not PASSWORD:
            print("Error: need --user and --password (no saved token found)", file=sys.stderr)
            sys.exit(1)
        token = login(HOMESERVER, USERNAME, PASSWORD)

    # Resolve room ID (works for space child rooms too)
    room_id = resolve_room_id(HOMESERVER, ROOM, token)

    # Join room if needed
    join_room(HOMESERVER, room_id, token)

    # Send message
    result = send_message(HOMESERVER, room_id, token, MESSAGE)
    print("Message sent:", result)


if __name__ == "__main__":
    main()
