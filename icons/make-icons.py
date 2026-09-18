"""Draws the home-screen icon: a smiling gold star on the app's violet.

Run it from the repository root, with Pillow and numpy installed:

    python icons/make-icons.py

The icon is drawn here rather than pasted in as a binary, so that it can be
changed — a different colour, a fatter star, a bigger grin — without opening an
image editor, and so nobody has to wonder where the file came from. Every colour
below is one the app itself already uses.

A star because stars are what the board actually hands out, and a face on it
because a five year old should be able to find this on a home screen full of
grey squares. It is drawn once at 2048 and shrunk, which is what makes the edges
clean at 60 pixels.

Everything important sits inside the middle 78% of the square: Android crops
icons to a circle and iOS to a rounded square, and anything further out is
liable to be cut off.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = 2048                      # master size; every real icon is shrunk from this
OUT = [('icons/apple-touch-icon.png', 180),   # iPhone and iPad home screens
       ('icons/icon-192.png',         192),   # Android / Chrome
       ('icons/icon-512.png',         512),   # splash screens and app listings
       ('icons/favicon-32.png',        32)]   # the browser tab

# ---------------------------------------------------------------- the palette
BG_TL   = (0x52, 0x54, 0xE8)   # indigo, top left
BG_BR   = (0xA8, 0x55, 0xF7)   # violet, bottom right
STAR_T  = (0xFF, 0xDD, 0x6B)   # amber, the top of the star
STAR_B  = (0xFB, 0x92, 0x35)   # orange, the bottom of it
RIM     = (0xB4, 0x53, 0x09)   # a warm dark line around the star
SHADOW  = (0x2A, 0x10, 0x50)   # violet-black, so the shadow is not grey
INK     = (0x46, 0x24, 0x05)   # eyes and mouth: dark brown, never black
CHEEK   = (0xFB, 0x71, 0x85)   # rose

CX, CY = S * 0.5, S * 0.474    # a shade high: a face looks centred that way
R      = S * 0.345             # tip of the star from the centre

grid_y, grid_x = np.mgrid[0:S, 0:S].astype(np.float32)
grid_x += 0.5
grid_y += 0.5


def star_field():
    """Distance to the star, negative inside.

    The star is five tapered spokes and a disc in the middle, rather than a
    ten-cornered polygon. That is not a shortcut: a spoke that narrows to its
    tip gives the plump body and softly rounded valleys that make the thing
    look friendly, and there is no sharp corner anywhere to go ragged.
    """
    W, TAPER, TIP, CORE = S * 0.112, 0.95, S * 0.011, S * 0.132
    best = np.full((S, S), 1e9, np.float32)
    for k in range(5):
        a = -np.pi / 2 + k * 2 * np.pi / 5
        dx, dy = R * np.cos(a), R * np.sin(a)
        t = np.clip(((grid_x - CX) * dx + (grid_y - CY) * dy) / (dx * dx + dy * dy), 0.0, 1.0)
        d = np.hypot(grid_x - (CX + t * dx), grid_y - (CY + t * dy))
        best = np.minimum(best, d - (W * np.power(1.0 - t, TAPER) + TIP))
    return np.minimum(best, np.hypot(grid_x - CX, grid_y - CY) - CORE)


FIELD = star_field()


def star_mask(grow=0.0, aa=1.6):
    """The star as an 8-bit mask, grown outwards by `grow` pixels."""
    a = np.clip((grow - FIELD) / aa + 0.5, 0.0, 1.0)
    return Image.fromarray((a * 255).astype(np.uint8), 'L')


def ramp(c1, c2, horizontal=False):
    """A straight gradient from c1 to c2, as a full-size image."""
    t = (grid_x + grid_y) / (2 * S) if not horizontal else grid_x / S
    if not horizontal:
        t = np.clip(t * 1.15 - 0.07, 0.0, 1.0)
    out = np.empty((S, S, 3), np.uint8)
    for i in range(3):
        out[:, :, i] = (c1[i] + (c2[i] - c1[i]) * t).astype(np.uint8)
    return Image.fromarray(out, 'RGB')


def vertical_ramp(c1, c2, y0, y1):
    t = np.clip((grid_y - y0) / (y1 - y0), 0.0, 1.0)
    out = np.empty((S, S, 3), np.uint8)
    for i in range(3):
        out[:, :, i] = (c1[i] + (c2[i] - c1[i]) * t).astype(np.uint8)
    return Image.fromarray(out, 'RGB')


def layer():
    return Image.new('RGBA', (S, S), (0, 0, 0, 0))


def sparkle(d, x, y, s, alpha):
    """A four-pointed twinkle. Waisted, so it reads as a sparkle and not a plus."""
    w = s * 0.20
    d.polygon([(x, y - s), (x + w, y - w), (x + s, y), (x + w, y + w),
               (x, y + s), (x - w, y + w), (x - s, y), (x - w, y - w)],
              fill=(255, 255, 255, alpha))


# ------------------------------------------------------------------ the picture
img = ramp(BG_TL, BG_BR).convert('RGBA')

# a soft light behind the star, so the middle of the icon is not flat
glow = np.clip(1.0 - np.hypot(grid_x - CX, grid_y - CY) / (S * 0.50), 0.0, 1.0) ** 1.7
g = layer()
g.putalpha(Image.fromarray((glow * 46).astype(np.uint8), 'L'))
img = Image.alpha_composite(img, Image.composite(
    Image.new('RGBA', (S, S), SHADOW + (0,)), g, g))
glow_layer = Image.new('RGBA', (S, S), (255, 255, 255, 255))
glow_layer.putalpha(Image.fromarray((glow * 40).astype(np.uint8), 'L'))
img = Image.alpha_composite(img, glow_layer)

# the star's shadow: down and a little right, well blurred
sh = Image.new('RGBA', (S, S), SHADOW + (0,))
sh.putalpha(star_mask(grow=S * 0.004).filter(ImageFilter.GaussianBlur(S * 0.022)))
img = Image.alpha_composite(img, sh.transform(
    (S, S), Image.AFFINE, (1, 0, -S * 0.006, 0, 1, -S * 0.028)))

# a warm dark line around the star, which is what stops it dissolving into the
# violet at 60 pixels across
rim = Image.new('RGBA', (S, S), RIM + (0,))
rim.putalpha(star_mask(grow=S * 0.0125))
img = Image.alpha_composite(img, rim)

# the star itself
mask = star_mask()
body = vertical_ramp(STAR_T, STAR_B, CY - R * 0.95, CY + R * 0.85).convert('RGBA')
body.putalpha(mask)
img = Image.alpha_composite(img, body)

# a gloss across the top of it
gl = Image.new('RGBA', (S, S), (255, 255, 255, 255))
ga = np.clip((CY - grid_y) / (R * 0.85), 0.0, 1.0) ** 1.6 * 58
gl.putalpha(Image.composite(Image.fromarray(ga.astype(np.uint8), 'L'),
                            Image.new('L', (S, S), 0), mask))
img = Image.alpha_composite(img, gl)

# cheeks, blurred before they go on, so they are a blush and not two stickers
ch = layer()
d = ImageDraw.Draw(ch)
for sx in (-1, 1):
    x, y, r = CX + sx * S * 0.148, CY + S * 0.056, S * 0.046
    d.ellipse([x - r, y - r * 0.82, x + r, y + r * 0.82], fill=CHEEK + (135,))
ch = ch.filter(ImageFilter.GaussianBlur(S * 0.014))
img = Image.alpha_composite(img, Image.composite(ch, layer(), mask))

# the face
face = layer()
d = ImageDraw.Draw(face)
for sx in (-1, 1):
    x, y = CX + sx * S * 0.083, CY - S * 0.025
    rx, ry = S * 0.0280, S * 0.0380
    d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=INK + (255,))
    hr = S * 0.0100                                    # the glint that makes eyes alive
    d.ellipse([x - rx * 0.55 - hr, y - ry * 0.52 - hr,
               x - rx * 0.55 + hr, y - ry * 0.52 + hr], fill=(255, 255, 255, 235))

mw, mh, my = S * 0.076, S * 0.058, CY + S * 0.034      # the smile
lw = S * 0.0190
d.arc([CX - mw, my - mh, CX + mw, my + mh], 18, 162, fill=INK + (255,), width=int(lw))
for deg in (18, 162):                                   # round off both ends of it
    x, y = CX + mw * np.cos(np.radians(deg)), my + mh * np.sin(np.radians(deg))
    d.ellipse([x - lw / 2, y - lw / 2, x + lw / 2, y + lw / 2], fill=INK + (255,))
img = Image.alpha_composite(img, face)

# twinkles in the corners the star does not reach
tw = layer()
d = ImageDraw.Draw(tw)
sparkle(d, S * 0.845, S * 0.150, S * 0.052, 225)
sparkle(d, S * 0.135, S * 0.760, S * 0.038, 195)
sparkle(d, S * 0.150, S * 0.185, S * 0.026, 160)
sparkle(d, S * 0.870, S * 0.815, S * 0.030, 175)
img = Image.alpha_composite(img, tw)

# ------------------------------------------------------------------ write them
flat = Image.new('RGB', (S, S), BG_TL)
flat.paste(img, (0, 0), img)
for path, size in OUT:
    flat.resize((size, size), Image.LANCZOS).save(path, optimize=True)
    print('wrote %-32s %dx%d' % (path, size, size))
