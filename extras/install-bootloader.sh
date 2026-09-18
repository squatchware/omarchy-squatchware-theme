#!/bin/bash
# Theme the Limine boot menu: wallpaper, branding and colours. Run in a terminal (asks for sudo).
#   ./install-bootloader.sh            apply
#   ./install-bootloader.sh --restore  put back the limine.conf saved on first run
# Only the global keys at the top of /boot/limine.conf change; boot entries are left alone.
set -euo pipefail
cd "$(dirname "$0")"

boot=${BOOT:-/boot} # overridable for dry runs
conf=$boot/limine.conf
backup=$boot/limine.conf.pre-squatchware

if [[ ${1:-} == --restore ]]; then
  sudo test -f "$backup" || { echo "No backup at $backup" >&2; exit 1; }
  sudo cp "$backup" "$conf"
  sudo rm -f $boot/squatchware-boot.png "$backup"
  echo "Restored $conf"
  exit 0
fi

sudo test -f "$backup" || sudo cp "$conf" "$backup"
sudo install -m 644 bootloader/squatchware-boot.png $boot/squatchware-boot.png

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
sudo cat "$conf" >"$tmp"
while IFS= read -r line; do
  [[ $line =~ ^([a-z_]+):\ (.*)$ ]] || continue
  key=${BASH_REMATCH[1]}
  if grep -qE "^#?[[:space:]]*${key}:" "$tmp"; then
    # replace the first (possibly commented) occurrence, drop any others
    awk -v k="$key" -v l="$line" '
      $0 ~ "^#?[[:space:]]*" k ":" { if (!done) { print l; done = 1 } ; next }
      { print }' "$tmp" >"$tmp.new" && mv "$tmp.new" "$tmp"
  else
    # new keys go before the first boot entry (the first line starting with "/")
    awk -v l="$line" '!done && /^\// { print l; done = 1 } { print }
      END { if (!done) print l }' "$tmp" >"$tmp.new" && mv "$tmp.new" "$tmp"
  fi
done < <(grep -v '^#' bootloader/limine-squatchware.conf)

sudo install -m 644 "$tmp" "$conf"
echo "Limine themed. Backup: $backup  (undo with ./install-bootloader.sh --restore)"
