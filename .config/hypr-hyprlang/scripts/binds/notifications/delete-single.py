import json
import subprocess


def is_dnd():
    result = subprocess.run(
        ["dunstctl", "get-pause-level"], stdout=subprocess.PIPE, check=True
    )
    isDND = result.stdout.decode("utf-8").strip()
    return isDND != "0"


def get_history_count():
    result = subprocess.run(
        ["dunstctl", "count", "history"], stdout=subprocess.PIPE, check=True
    )
    count = result.stdout.decode("utf-8").strip()
    return int(count)


def get_history():
    result = subprocess.run(["dunstctl", "history"], stdout=subprocess.PIPE, check=True)
    history = json.loads(result.stdout.decode("utf-8"))["data"][0]
    return history


def remove_top_notification(notification):
    notification_id = str(notification.get("id", {}).get("data", ""))

    if notification_id:
        subprocess.run(
            ["dunstctl", "history-rm", notification_id], check=True, timeout=5
        )


def main():
    if not is_dnd() and get_history_count() > 0:
        history = get_history()
        remove_top_notification(history[0])


if __name__ == "__main__":
    main()
