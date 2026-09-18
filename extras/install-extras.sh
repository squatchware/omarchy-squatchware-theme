#!/bin/bash
# Squatchware extras, for either variant: the screensaver hook now, and the boot screens
# (which need sudo) if you ask. Run it from the installed theme:
#   ~/.config/omarchy/themes/squatchware/extras/install-extras.sh [--boot]
set -euo pipefail
cd "$(dirname "$0")"

omarchy hook install theme-set hooks/squatchware-screensaver >/dev/null
# the theme was already set when it was installed, so run the hook once for the current theme
hooks/squatchware-screensaver "$(omarchy theme current | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
echo "Screensaver hook installed."

if [[ ${1:-} == --boot ]]; then
  current=$(omarchy theme current | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  [[ $current == squatchware* ]] || current=squatchware
  omarchy plymouth set by theme "$current"
  ./install-bootloader.sh
else
  echo "For the boot splash and Limine menu (sudo): $0 --boot"
fi
