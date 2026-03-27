#!/bin/bash

# credit: https://github.com/junaruga/framework-laptop-config/blob/main/home/script/control_wvkbd.sh

set -eu

PROG="$HOME/.local/bin/wvkbd-colemakdh"

# SIGUSR1 = hide, SIGUSR2 = show, SIGRTMIN = toggle
SIGNAL="SIGRTMIN"
if [ "${#}" -gt 0 ]; then
    SIGNAL="${1}"
fi

if ! pgrep -f "${PROG}" > /dev/null; then
    "${PROG}" \
        --hidden \
        --alpha 204 \
        --fn "VictorMono Nerd Font 16" \
        --bg 1E2030 \
        --fg 5B6078 \
        --text CAD3F5 \
        --press F0C6C6 \
        --swipe F0C6C6 \
        --fg-sp EE99A0 \
        --text-sp 24273A \
        --press-sp C6A0F6 \
        --swipe-sp C6A0F6 \
        &
    # "${PROG}" \
    #     --hidden \
    #     --alpha 80 \
    #     --non-exclusive \
    #     &
fi

pkill -f --signal "${SIGNAL}" "${PROG}"
