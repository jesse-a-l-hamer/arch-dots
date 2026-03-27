# credit: https://github.com/junaruga/framework-laptop-config/blob/main/home/script/control_wvkbd.sh

set -eu

PROG="/usr/bin/nwg-drawer"

SIGNAL="SIGUSR1"
if [ "${#}" -gt 0 ]; then
    SIGNAL="${1}"
fi

if ! pgrep -f "${PROG}" > /dev/null; then
    "${PROG}" \
        -closebtn right \
        -fm "yazi.desktop" \
        -ovl \
        -pbexit "uwsm stop" \
        -pblock "hyprlock --grace 30" \
        -pbpoweroff "systemctl poweroff" \
        -pbreboot "systemctl reboot" \
        -pbsleep "systemctl suspend" \
        -pbuseicontheme \
        -term kitty \
        -wm uwsm \
        -r
fi

pkill -f --signal "${SIGNAL}" "${PROG}"
