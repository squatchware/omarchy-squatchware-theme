"""Pixel-art forest scenes for the wallpapers and lock screen.

Scenes are drawn at 480x300 real pixels, then scaled x8 with nearest-neighbour, so every
wallpaper pixel is a crisp 8x8 block. Sprites go in at 1:1 so they match the scene's pixel size.
Gradients use 4x4 ordered (Bayer) dithering, per the brand's pixel rules.
"""
import random
from PIL import Image

W, H = 480, 300
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

NIGHT = {
    "sky": ["#0A120E", "#0F1A14", "#13241A", "#1B3325"],
    "stars": ["#F4E4BC", "#F4E4BC", "#F4E4BC", "#D4A832", "#3AA597"],
    "moon": "#F4E4BC", "moon_shade": "#D9C690", "glow": "#1F3A2A",
    "far": "#132B1E", "back": "#11261A", "front": "#183826", "ground": "#0C1510",
    "eyes": "#D4A832",
}
DAWN = {
    "sky": ["#FBF1D6", "#F4E4BC", "#EDD39A", "#E4B878"],
    "stars": [],
    "moon": "#D4A832", "moon_shade": "#C4912A", "glow": "#F1D69A",
    "far": "#B9C4A0", "back": "#7E9F76", "front": "#245333", "ground": "#1B3F27",
    "eyes": None,
}


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def dither_band(img, y0, y1, c0, c1):
    """Vertical gradient from c0 to c1 over rows y0..y1 using ordered dithering."""
    a, b = hexrgb(c0), hexrgb(c1)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        for x in range(W):
            img.putpixel((x, y), b if t * 16 > BAYER[y % 4][x % 4] + 0.5 else a)


def sky(img, pal):
    stops = pal["sky"]
    bands = len(stops) - 1
    edges = [int(i * H * 0.8 / bands) for i in range(bands + 1)]
    for i in range(bands):
        dither_band(img, edges[i], edges[i + 1], stops[i], stops[i + 1])
    for y in range(edges[-1], H):
        for x in range(W):
            img.putpixel((x, y), hexrgb(stops[-1]))


def stars(img, pal, rng, n=140):
    for _ in range(n):
        x, y = rng.randrange(W), rng.randrange(int(H * 0.6))
        img.putpixel((x, y), hexrgb(rng.choice(pal["stars"])))


def disc(img, cx, cy, r, colour, shade=None, glow=None):
    """A pixel circle with an optional crescent shade and a dithered glow ring."""
    if glow:
        g = hexrgb(glow)
        for y in range(cy - r - 6, cy + r + 7):
            for x in range(cx - r - 6, cx + r + 7):
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if r < d <= r + 6 and (x + y) % 2 == 0 and 0 <= x < W and 0 <= y < H:
                    img.putpixel((x, y), g)
    c, s = hexrgb(colour), hexrgb(shade) if shade else None
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + r:
                lit = s is None or (x - cx + r * 0.35) ** 2 + (y - cy + r * 0.25) ** 2 <= (r * 1.05) ** 2
                img.putpixel((x, y), c if lit else s)


def pine(img, cx, base, h, colour):
    """A tiered pine: three stacked sawtooth triangles plus a stub trunk."""
    c = hexrgb(colour)
    tiers = 3
    tier_h = h / (tiers + 0.4)
    for dy in range(int(h)):
        y = base - int(h) + dy
        tier = min(tiers - 1, int(dy / tier_h * 0.85))
        within = (dy - tier * tier_h * 1.1765) / tier_h
        within = max(0.0, min(1.0, within))
        half = int((0.10 + 0.08 * tier) * h * (0.35 + 0.65 * within)) + 1
        for x in range(cx - half, cx + half + 1):
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), c)
    for y in range(base, min(H, base + 3)):
        for x in range(cx - 1, cx + 2):
            if 0 <= x < W:
                img.putpixel((x, y), c)


def treeline(img, rng, colour, base, h_min, h_max, spacing, jitter, fill_to=None):
    x = -spacing
    while x < W + spacing:
        pine(img, x + rng.randint(-jitter, jitter), base + rng.randint(-2, 2), rng.randint(h_min, h_max), colour)
        x += spacing
    c = hexrgb(colour)
    for y in range(base - 3, fill_to or H):
        for xx in range(W):
            img.putpixel((xx, y), c)


def eyes(img, x, y, colour):
    c = hexrgb(colour)
    img.putpixel((x, y), c)
    img.putpixel((x + 3, y), c)


def paste_sprite(img, sprite_img, x, y):
    img.alpha_composite(sprite_img, (x, y))


def render(pal, seed, squatch=None, squatch_at=(372, 286)):
    """Build one 480x300 scene. `squatch` is an RGBA sprite at 1:1 or None."""
    rng = random.Random(seed)
    img = Image.new("RGBA", (W, H))
    sky(img, pal)
    if pal["stars"]:
        stars(img, pal, rng)
        disc(img, 392, 58, 14, pal["moon"], pal["moon_shade"], pal["glow"])
    else:
        disc(img, 100, 150, 22, pal["moon"], None, pal["glow"])
    treeline(img, rng, pal["far"], 212, 28, 44, 17, 5)
    treeline(img, rng, pal["back"], 234, 40, 70, 22, 7)
    if pal["eyes"]:
        for ex, ey in ((58, 214), (171, 206), (433, 219)):
            eyes(img, ex, ey, pal["eyes"])
    treeline(img, rng, pal["front"], 258, 34, 58, 26, 6)
    for y in range(284, H):
        for x in range(W):
            img.putpixel((x, y), hexrgb(pal["ground"]))
    if squatch is not None:  # standing in front of the trees, feet on the ground line
        x, y = squatch_at
        paste_sprite(img, squatch, x, y - squatch.height)
    return img


def upscale(img, factor=8):
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)
