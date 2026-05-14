import subprocess


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


def main():
    if not is_dnd():
        while get_history_count() > 0:
            _ = subprocess.run(["dunstctl", "history-pop"], check=True)


if __name__ == "__main__":
    main()
