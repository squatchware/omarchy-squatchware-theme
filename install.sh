#!/bin/bash
# Install both Squatchware themes and the screensaver hook for the current user.
# The boot screens need sudo and are separate: see README.md.
set -euo pipefail
cd "$(dirname "$0")"

themes=~/.config/omarchy/themes
for t in squatchware squatchware-light; do
  rm -rf "${themes:?}/$t"
  cp -r "themes/$t" "$themes/$t"
done
omarchy hook install theme-set hooks/squatchware-screensaver >/dev/null

echo "Installed. Apply with: omarchy theme set squatchware   (or squatchware-light)"
