"""`poster_lb_frame` — a third LONGEBLACK arrangement.

An invitation-card device: a hairline rectangle inset from the edges, with a small label
breaking the top rule, thin letterspaced type stacked inside, and a closing detail line at
the bottom of the frame. Quieter and more ceremonial than the hero or statement formats.

Handles light grounds properly: ink and the type-zone gradient both invert, so it works on
high-key bone as well as dark palettes.
"""
import math
import os
from PIL import Image, ImageDraw

from poster import (W, H, ORANGE, F_BOLD, font, track_text, track_width, wrap,
                    paste_logo, cover, mean_lum)

from paths import F_LIGHT  # resolved per-machine


def soft_band(img, y_center, sigma, strength, lighten=False):
    """Gaussian lift or darken centred on y_center — reads as natural falloff."""
    col = Image.new("L", (1, H))
    px = col.load()
    for y in range(H):
        px[0, y] = int(strength * math.exp(-((y - y_center) ** 2) / (2 * sigma ** 2)))
    layer = Image.new("RGBA", (W, H), (255, 255, 255, 255) if lighten else (0, 0, 0, 255))
    layer.putalpha(col.resize((W, H)))
    img.alpha_composite(layer)


def poster_lb_frame(photo_path, out_path, label, l1, l2, body, detail,
                    inset=0.055, head_y=0.315):
    img = cover(Image.open(photo_path).convert("RGB"), W, H).convert("RGBA")

    # decide ink from the ground the type will sit on, then lift or deepen that zone
    band = (int(W * 0.2), int(H * head_y) - 30, int(W * 0.8), int(H * head_y) + 260)
    light_ground = mean_lum(img, band) >= 128
    ink = (28, 26, 24) if light_ground else (255, 255, 255)
    soft_band(img, int(H * (head_y + 0.10)), sigma=int(H * 0.22),
              strength=120 if light_ground else 150, lighten=light_ground)

    draw = ImageDraw.Draw(img)
    x0, y0 = int(W * inset), int(H * inset * 0.8)
    x1, y1 = W - x0, H - y0

    draw.rectangle([x0, y0, x1, y1], outline=ink + (150,), width=2)

    # small label breaking the top rule
    fl = font(F_BOLD, 19)
    lw_ = track_width(draw, label.upper(), fl, 3.6)
    gap = 30
    draw.rectangle([(W - lw_) / 2 - gap, y0 - 16, (W + lw_) / 2 + gap, y0 + 16],
                   fill=(250, 248, 244) if light_ground else (14, 13, 12))
    track_text(draw, ((W - lw_) / 2, y0 - 10), label.upper(), fl, ink, 3.6)

    # thin letterspaced headline, two lines
    size = 86
    f = font(F_LIGHT, size)
    tr = size * 0.26
    longest = max([l1, l2], key=len).upper()
    while track_width(draw, longest, f, tr) > (x1 - x0) - 120 and size > 30:
        size -= 2
        f = font(F_LIGHT, size)
        tr = size * 0.26
    y = int(H * head_y)
    for line in (l1, l2):
        t = line.upper()
        tw = track_width(draw, t, f, tr)
        track_text(draw, ((W - tw) / 2, y), t, f, ink, tr)
        y += int(size * 1.72)

    draw.line([(W // 2 - 30, y + 10), (W // 2 + 30, y + 10)], fill=ORANGE, width=4)

    fb = font(F_BOLD, 19)
    by = y + 52
    for line in wrap(draw, body.upper(), fb, 720, 1.4):
        wb = track_width(draw, line, fb, 1.4)
        track_text(draw, ((W - wb) / 2, by), line, fb, ink + (235,), 1.4)
        by += 30

    # closing detail line + logo inside the bottom of the frame
    fd = font(F_BOLD, 18)
    wd = track_width(draw, detail.upper(), fd, 3.4)
    track_text(draw, ((W - wd) / 2, y1 - 66), detail.upper(), fd, ink + (215,), 3.4)

    lw = 128
    paste_logo(img, lw, ((W - lw) // 2, y1 - 156), white=not light_ground)

    lum = mean_lum(img, (int(W * 0.2), int(H * head_y), int(W * 0.8),
                         int(H * head_y) + size))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  lb-frame  head={size}px  "
          f"ground lum={lum:.0f}  ink={'dark' if light_ground else 'white'}")
