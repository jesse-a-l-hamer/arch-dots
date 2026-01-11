#!/usr/bin/python3
import json
import subprocess
import sys
from time import sleep

CATEGORY_APPNAMES: dict[str, set[str]] = {
    "email": {"Betterbird"},
    "chat": {"Fractal"},
    "system": {"uuctl", "Systemd timer notify", "FUMonitor"},
    "network": {"Mullvad VPN", "Syncthing Tray"},
    "battery": set([]),
    "update": set([]),
    "music": set([]),
    "volume": set([]),
    "hypr": {"Hyprland", "hyprland", "hypridle", "hyprlock"},
    "mpv": {"mpv"},
    "display": {"shikane"},
    "security": {"KeePassXC"},
    "timecheck": set([]),
}


def get_history():
    result = subprocess.run(["dunstctl", "history"], stdout=subprocess.PIPE, check=True)
    history = json.loads(result.stdout.decode("utf-8"))["data"][0]
    return history


def get_history_count():
    result = subprocess.run(
        ["dunstctl", "count", "history"], stdout=subprocess.PIPE, check=True
    )
    count = result.stdout.decode("utf-8").strip()
    return int(count)


def is_dnd():
    result = subprocess.run(
        ["dunstctl", "get-pause-level"], stdout=subprocess.PIPE, check=True
    )
    isDND = result.stdout.decode("utf-8").strip()
    return isDND != "0"


def format_history(history):
    count = len(history)
    text = f"({count})"

    if count > 0:
        notification = history[0]  # Get the top of the notification history stack

        appname = notification.get("appname", {}).get("data", "")
        summary = notification.get("summary", {}).get("data", "")
        category = notification.get("category", {}).get("data", "")

        if appname and category not in CATEGORY_APPNAMES:
            for c, a in CATEGORY_APPNAMES.items():
                if appname in a:
                    category = c
                    break

        formatted_notification = f"{appname}: {summary}" if appname else summary
        text += " " + formatted_notification
        if category:
            alt = category + "-notification"
        else:
            alt = "notification"
    else:
        alt = "none"

    formatted_history = {
        "text": text,
        "alt": alt,
    }
    return formatted_history


def main():
    if is_dnd():
        count = get_history_count()
        alt = "dnd" + ("-notification" if count > 0 else "")
        payload = {"text": f"({count})", "alt": alt}
    else:
        history = get_history()
        payload = format_history(history)
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()
    sleep(1)


if __name__ == "__main__":
    while True:
        main()
