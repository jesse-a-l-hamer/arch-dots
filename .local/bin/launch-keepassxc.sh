#!/bin/sh

# Opens KeepassXC vault
# Requires KEEPASSXC_VAULT and KEEPASSXC_KEY environment variables

gpg --quiet --decrypt "$KEEPASSXC_KEY" | keepassxc --pw-stdin --minimized "$KEEPASSXC_VAULT"
