#!/usr/bin/env python3
"""Build the Squatchware and Squatchware Light Omarchy themes.

    python3 build.py            # write themes/<slug>/ and bootloader/
    python3 build.py --check    # contrast check only

Sprites and the pixel font come from the brand kit in squatchware.dev/brand, so the squatch
here is always the same one as on the site. Override its location with SQUATCHWARE_BRAND.
"""
import os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
BRAND = Path(os.environ.get("SQUATCHWARE_BRAND", HERE.parent / "squatchware.dev" / "brand"))
FONT = BRAND.parent / "public" / "fonts" / "press-start-2p.woff2"
sys.path.insert(0, str(BRAND))

from sprite import grid, png  # noqa: E402  (brand kit)
import scene  # noqa: E402
from palettes import DARK, LIGHT, COLOR_KEYS, LOCK_KEYS, TEXT_KEYS  # noqa: E402

GOLD, ORANGE, INK = "#D4A832", "#D4722A", "#1A1A2E"


# ---------- contrast ----------

def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def ratio(a, b):
    x, y = sorted([lum(a), lum(b)])
    return (y + .05) / (x + .05)


def check(pal):
    bad = [(k, round(ratio(pal[k], pal["background"]), 2)) for k in TEXT_KEYS
           if ratio(pal[k], pal["background"]) < 4.5]
    sel = ratio(pal["selection_foreground"], pal["selection_background"])
    if sel < 4.5:
        bad.append(("selection_foreground on selection_background", round(sel, 2)))
    return bad


# ---------- text files ----------

def toml(pal, keys):
    width = max(len(k) for k in keys)
    return "".join(f'{k.ljust(width)} = "{pal[k]}"\n' for k in keys)


def colors_toml(pal):
    return f'mode = "{pal["mode"]}"\n\n' + toml(pal, COLOR_KEYS)


# ---------- logo (lock screen + Plymouth) ----------

def wordmark(text, size, face, shadow, shadow2=None):
    """Pixel wordmark with hard offset shadows, like the site's h1."""
    font = ImageFont.truetype(str(FONT), size)
    w, h = font.getbbox(text)[2], font.getbbox(text)[3]
    step = size // 12
    pad = step * (4 if shadow2 else 2)
    img = Image.new("RGBA", (w + pad, h + pad))
    d = ImageDraw.Draw(img)
    if shadow2:
        d.text((step * 4, step * 4), text, font=font, fill=shadow2)
    d.text((step * 2, step * 2), text, font=font, fill=shadow)
    d.text((0, 0), text, font=font, fill=face)
    return img


def logo(mode):
    """800x188: squatch head x8 beside the SQUATCHWARE wordmark, on transparency."""
    head = png("head", 8)
    mark = wordmark("SQUATCHWARE", 48, GOLD, ORANGE if mode == "dark" else INK,
                    (0, 0, 0, 110) if mode == "dark" else None)
    out = Image.new("RGBA", (800, 188))
    total = head.width + 40 + mark.width
    x = (800 - total) // 2
    out.alpha_composite(head, (x, (188 - head.height) // 2))
    out.alpha_composite(mark, (x + head.width + 40, (188 - mark.height) // 2 + 4))
    return out


# ---------- screensaver art ----------

SHADE = {"P": "█", "W": "█", "G": "█", "L": "▓", "R": "▓", "F": "▒", "b": "░", "D": "░", "o": " ", "e": " ", ".": " "}


def screensaver():
    """The head in shade blocks (2 columns per pixel keeps it square) over a half-block wordmark."""
    head = ["".join(SHADE[c] * 2 for c in row).rstrip() for row in grid("head")]
    font = ImageFont.truetype(str(FONT), 8)
    img = Image.new("1", (88, 8))
    ImageDraw.Draw(img).text((0, 0), "SQUATCHWARE", font=font, fill=1)
    word = []
    for y in range(0, 8, 2):
        row = ""
        for x in range(88):
            top, bot = img.getpixel((x, y)), img.getpixel((x, y + 1))
            row += "█" if top and bot else "▀" if top else "▄" if bot else " "
        word.append(row.rstrip())
    pad = (88 - 32) // 2
    art = [(" " * pad + r).rstrip() for r in head] + ["", ""] + word
    while art and not art[-1]: art.pop()
    return "\n".join(art) + "\n"


# ---------- previews ----------

def preview_unlock(wall, pal, logo_img):
    """Lock screen mock: dimmed wallpaper, logo, accent input line (matches other themes' previews)."""
    base = wall.resize((1920, 1200), Image.NEAREST).crop((0, 60, 1920, 1140)).convert("RGBA")
    shade = Image.new("RGBA", base.size, pal["background"] + ("b0" if pal["mode"] == "dark" else "a0"))
    base.alpha_composite(shade)
    base.alpha_composite(logo_img, ((1920 - 800) // 2, 380))
    d = ImageDraw.Draw(base)
    d.rectangle((790, 610, 1130, 614), fill=pal["accent"])
    return base


# ---------- build ----------

def build_theme(pal, readme):
    out = HERE / "themes" / pal["slug"]
    (out / "backgrounds").mkdir(parents=True, exist_ok=True)
    (out / "colors.toml").write_text(colors_toml(pal))
    (out / "shell.lock.toml").write_text(toml(pal, LOCK_KEYS))
    (out / "icons.theme").write_text(pal["icons"] + "\n")
    (out / "screensaver.txt").write_text(screensaver())
    (out / "README.md").write_text(readme)

    sky = scene.NIGHT if pal["mode"] == "dark" else scene.DAWN
    walls = [
        ("01-sighting.png", scene.render(sky, 7, png("stand" if pal["mode"] == "dark" else "wave", 1))),
        ("02-treeline.png", scene.render(sky, 21)),
    ]
    for name, img in walls:
        scene.upscale(img, 8).convert("RGB").save(out / "backgrounds" / name, optimize=True)

    lg = logo(pal["mode"])
    lg.save(out / "unlock.png")
    scene.upscale(walls[0][1], 4).convert("RGB").resize((1800, 1125), Image.NEAREST).crop((0, 56, 1800, 1068)).save(out / "preview.png")
    preview_unlock(scene.upscale(walls[0][1], 4), pal, lg).convert("RGB").save(out / "preview-unlock.png")
    return out


def build_bootloader():
    """Limine: a wallpaper for the boot menu plus the colour keys install-bootloader.sh writes."""
    out = HERE / "bootloader"
    out.mkdir(exist_ok=True)
    img = scene.render(scene.NIGHT, 7, png("stand", 1))
    scene.upscale(img, 4).convert("RGB").save(out / "squatchware-boot.png", optimize=True)
    p = DARK
    hexes = lambda keys: ";".join(p[k].lstrip("#").lower() for k in keys)
    (out / "limine-squatchware.conf").write_text(
        "# Squatchware keys for /boot/limine.conf, written by install-bootloader.sh.\n"
        "interface_branding: SQUATCHWARE\n"
        f"interface_branding_color: {GOLD.lstrip('#').lower()}\n"
        f"interface_help_color: {p['muted'].lstrip('#').lower()}\n"
        f"interface_help_color_bright: {p['bright_yellow'].lstrip('#').lower()}\n"
        "wallpaper: boot():/squatchware-boot.png\n"
        "wallpaper_style: stretched\n"
        f"backdrop: {p['background'].lstrip('#').lower()}\n"
        # TT = transparency (00 opaque .. ff clear): tint the menu area but let the forest show through
        f"term_background: 60{p['darker_background'].lstrip('#').lower()}\n"
        f"term_background_bright: {p['lighter_background'].lstrip('#').lower()}\n"
        f"term_foreground: {p['foreground'].lstrip('#').lower()}\n"
        f"term_foreground_bright: {p['bright_foreground'].lstrip('#').lower()}\n"
        f"term_palette: {hexes(['darker_background', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'foreground'])}\n"
        f"term_palette_bright: {hexes(['muted', 'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_foreground'])}\n"
    )


README = """# {name}

Part of the [Squatchware](https://squatchware.dev) Omarchy theme: {blurb}

Palette, sprites and wordmark come from the Squatchware brand kit (squatchware.dev/brand).
Backgrounds are real pixel art, 480x300 scenes scaled x8 with no smoothing:

- `01-sighting.png`: {scene} with the squatch at the edge of the trees
- `02-treeline.png`: the same forest with nobody in it (or so it seems)

`unlock.png` is the lock-screen logo and, via `omarchy plymouth set by theme {slug}`, the boot splash.
`screensaver.txt` is swapped in by the Squatchware theme-set hook. Suggested font: `JetBrainsMono Nerd Font`.

Activate with `omarchy theme set "{name}"`.
"""


def main():
    problems = {p["slug"]: check(p) for p in (DARK, LIGHT)}
    for slug, bad in problems.items():
        print(f"{slug}: " + ("all text colours >= 4.5:1" if not bad else f"LOW CONTRAST {bad}"))
    if "--check" in sys.argv:
        return
    if any(problems.values()):
        sys.exit("fix the palette before building")
    build_theme(DARK, README.format(name=DARK["name"], slug=DARK["slug"], scene="moonlit night forest",
                                    blurb="night forest, parchment text, campfire gold."))
    build_theme(LIGHT, README.format(name=LIGHT["name"], slug=LIGHT["slug"], scene="dawn over the pines",
                                     blurb="parchment daylight, forest ink, campfire orange."))
    build_bootloader()
    print("built themes/squatchware, themes/squatchware-light, bootloader/")


if __name__ == "__main__":
    main()
