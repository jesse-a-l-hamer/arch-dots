#!/bin/sh

# Opens KeepassXC vault
# Requires KEEPASSXC_VAULT and KEEPASSXC_KEY environment variables

if pgrep -x keepassxc >/dev/null 2>&1; then
    keepassxc
else
    gpg --quiet --decrypt "$KEEPASSXC_KEY" | keepassxc --pw-stdin --minimized "$KEEPASSXC_VAULT"
fi
