"""Terminal/desktop palettes for the two Squatchware Omarchy themes.

Brand tokens come from squatchware.dev/brand/DESIGN.md. ANSI colours are nudged from the
brand accents until every one clears 4.5:1 on its background (check with build.py --check).
"""

DARK = {
    "name": "Squatchware", "slug": "squatchware", "mode": "dark", "icons": "Yaru-olive",
    "accent": "#D4A832", "selection": "#245333", "muted": "#AB9E7B",
    "background": "#0F1A14", "dark_background": "#0A120E", "darker_background": "#060C09",
    "lighter_background": "#183826",
    "foreground": "#F4E4BC", "dark_foreground": "#AB9E7B", "light_foreground": "#D9CCAA",
    "bright_foreground": "#FFF8DC",
    "red": "#DB6250", "yellow": "#D4A832", "orange": "#D4722A", "green": "#6FAE5A",
    "cyan": "#3AA597", "blue": "#5B8FB9", "magenta": "#A87AC8", "brown": "#A0582A",
    "bright_red": "#E8826F", "bright_yellow": "#E9C45A", "bright_green": "#8FCB78",
    "bright_cyan": "#5CC4B5", "bright_blue": "#7FAED4", "bright_magenta": "#C49BE0",
    "selection_background": "#245333", "selection_foreground": "#FFF8DC",
    # lock screen
    "text": "#F4E4BC", "placeholder": "#AB9E7B", "text-error": "#E8826F",
    "border": "#245333", "border-active": "#D4A832", "border-error": "#DB6250",
}

LIGHT = {
    "name": "Squatchware Light", "slug": "squatchware-light", "mode": "light", "icons": "Yaru-wartybrown",
    "accent": "#94450F", "selection": "#E0CC92", "muted": "#6B5F43",
    "background": "#F4E4BC", "dark_background": "#EADAAF", "darker_background": "#DFCD9F",
    "lighter_background": "#FBF1D6",
    "foreground": "#1C2A20", "dark_foreground": "#6B5F43", "light_foreground": "#3D4A3F",
    "bright_foreground": "#0F1A14",
    "red": "#A83232", "yellow": "#7D5F00", "orange": "#94450F", "green": "#2F6E2F",
    "cyan": "#1F6E64", "blue": "#2E5E8A", "magenta": "#6E3A92", "brown": "#7A4020",
    "bright_red": "#8E2525", "bright_yellow": "#6A5000", "bright_green": "#245A24",
    "bright_cyan": "#175A52", "bright_blue": "#244C72", "bright_magenta": "#5A2E78",
    "selection_background": "#E0CC92", "selection_foreground": "#0F1A14",
    "text": "#1C2A20", "placeholder": "#6B5F43", "text-error": "#A83232",
    "border": "#C9B27A", "border-active": "#94450F", "border-error": "#A83232",
}

COLOR_KEYS = ["accent", "selection", "muted", "background", "dark_background", "darker_background",
              "lighter_background", "foreground", "dark_foreground", "light_foreground", "bright_foreground",
              "red", "yellow", "orange", "green", "cyan", "blue", "magenta", "brown",
              "bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_blue", "bright_magenta",
              "selection_background", "selection_foreground"]
LOCK_KEYS = ["text", "placeholder", "text-error", "border", "border-active", "border-error"]
# Colours that are read as text and must clear 4.5:1 on the background ("brown" is decoration only).
TEXT_KEYS = ["accent", "muted", "foreground", "dark_foreground", "red", "yellow", "orange", "green",
             "cyan", "blue", "magenta", "bright_red", "bright_yellow", "bright_green", "bright_cyan",
             "bright_blue", "bright_magenta"]
