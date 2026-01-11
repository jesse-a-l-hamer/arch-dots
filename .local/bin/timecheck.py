"""This script keeps track of a time-check notification and updates its state each time
an associated timer (timecheck.service) elapses.

The state of the time-check notification is maintained in a tmp file. This tmp file
must be deleted either manually, or by routine system tmp file cleanup; this script only
creates the tmp file if it does not exist, and reads it if it does exist.

The tmp file contains the following information:
    - The randomly generated time-check notification ID.
    - The cumulative time (in minutes) which has elapsed since the timer was activated.

Assuming the tmp file already exists, the script will read its contents, use them to
emit a new notification, and then save the updated state of the notification. The new
notification is constructed by first adding the timer interval length to the cumulative
elapsed time. If this new cumulative elapsed time is a multiple of 60, then the urgency
of the notification is "critical"; otherwise, the urgency is "low". The summary of
the notification presents the total time elapsed, while the body presents an injunction
to the user encouraging them to be mindful of the time which has elapsed. The
low-urgency notifications are meant to be non-invasive reminders of time's passing,
whereas the critical-urgency notifications are meant to force the user to reflect on
whether they truly want to continue the current task. A progress bar is also displayed,
which shows the percentage of an hour which has passed since either the timer was first
activated, or the last full hour elapsed.

If the tmp file does not already exist, then a new one is created with a new randomly
generated ID and the cumulative time set to 0.
"""

import os
import random
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

NOTIF_FILE = Path(f"/tmp/timecheck-{os.getlogin()}/notification")
INTERVAL_MINUTES = 15
APPNAME = "Time Check"
CATEGORY = "timecheck-notification"
ICON = "/usr/share/icons/Papirus/32x32/apps/d-tracker.svg"


@dataclass
class TimeCheckNotif:
    _id: int = field(default_factory=lambda: random.randint(1000, 9999))
    _time_elapsed: int = field(default=0)
    _exists: bool = field(default=False)

    @classmethod
    def read_or_create(cls) -> Self:
        if NOTIF_FILE.exists():
            lines = [line.strip() for line in NOTIF_FILE.read_text().splitlines()]
            return cls(int(lines[0]), int(lines[1]), True)
        return cls()

    def update(self):
        self._time_elapsed += INTERVAL_MINUTES

    def _remove_existing_from_history(self):
        _ = subprocess.run(["dunstctl", "history-rm", self.id], check=True)

    def emit(self):
        self._remove_existing_from_history()
        _ = subprocess.run(self.notify_send_payload, check=True)

    def save(self):
        NOTIF_FILE.write_text("\n".join([self.id, str(self._time_elapsed)]))

    @property
    def exists(self) -> bool:
        return self._exists

    @property
    def hours_elapsed(self) -> int:
        return self._time_elapsed // 60

    @property
    def remainder_minutes_elapsed(self) -> int:
        return self._time_elapsed % 60

    @property
    def time_elapsed(self) -> str:
        str_parts = []
        if self.hours_elapsed > 0:
            str_parts.append(f"{self.hours_elapsed}h")
        if self.remainder_minutes_elapsed > 0:
            str_parts.append(f"{self.remainder_minutes_elapsed}m")
        return " ".join(str_parts)

    @property
    def id(self) -> str:
        return str(self._id)

    @property
    def urgency(self) -> str:
        if self.exists and self.remainder_minutes_elapsed == 0:
            return "critical"
        elif self.exists:
            return "low"
        else:
            return "normal"

    @property
    def hint_progress(self) -> list[str]:
        if self.urgency != "normal":
            return ["-h", f"int:value:{int(self.remainder_minutes_elapsed * 100 / 60)}"]
        else:
            return []

    @property
    def summary(self) -> str:
        if self.urgency == "low":
            return self.time_elapsed
        elif self.urgency == "critical":
            return " ".join(
                [
                    self.time_elapsed,
                    ("has" if self.hours_elapsed == 1 else "have"),
                    "elapsed!",
                ]
            )
        else:
            return "new timer started"

    @property
    def body(self) -> str:
        if self.urgency == "low":
            return "This is a reminder to be aware of time's passage."
        elif self.urgency == "normal":
            return f"This notification will be updated every {INTERVAL_MINUTES} minutes"
        else:
            return "Consider if the current task is what you still want to be doing!"

    @property
    def notify_send_payload(self) -> list[str]:
        payload: list[str] = [
            "notify-send",
            *["-a", APPNAME],
            *["-u", self.urgency],
            *["-i", ICON],
            *["-c", CATEGORY],
            *self.hint_progress,
            *["-r", self.id],
            self.summary,
            self.body,
        ]

        return [p for p in payload if p]


def main():
    notif = TimeCheckNotif.read_or_create()

    if notif.exists:
        notif.update()

    notif.emit()
    notif.save()


if __name__ == "__main__":
    NOTIF_FILE.parent.mkdir(parents=True, exist_ok=True)
    main()
