"""LONGEBLACK lineage, rebuilt with the legibility problem solved.

The original attempt failed because thin letterspaced type was dropped straight onto live
photography. Fix: the photo is composed with a genuinely empty, tonally-even zone, and a
*soft* localised gradient (not a hard plate) deepens that zone just enough. The type keeps
its quiet character; it simply stops disappearing.

`poster_lb_hero`      — brand presentation: name, ™, endorsement lockup, logo.
`poster_lb_statement` — atmospheric positioning piece: no client name, no lockup.
"""
import math
import os
from PIL import Image, ImageDraw

from poster import (W, H, MARGIN, ORANGE, INK, F_BOLD, font, track_text,
                    track_width, wrap, paste_logo, cover, mean_lum)

from paths import F_LIGHT  # resolved per-machine
CREAM = (247, 243, 233)


def soft_band(img, y_center, sigma, strength=150):
    """Smooth gaussian darkening centred on y_center — reads as natural falloff."""
    col = Image.new("L", (1, H))
    px = col.load()
    for y in range(H):
        px[0, y] = int(strength * math.exp(-((y - y_center) ** 2) / (2 * sigma ** 2)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    layer.putalpha(col.resize((W, H)))
    img.alpha_composite(layer)


def fit_light(draw, text, max_w, start=104, track_ratio=0.26):
    size = start
    f = font(F_LIGHT, size)
    while track_width(draw, text, f, size * track_ratio) > max_w and size > 26:
        size -= 2
        f = font(F_LIGHT, size)
    return size, f, size * track_ratio


# ------------------------------------------------------------- A: brand hero
def poster_lb_hero(photo_path, out_path, name, endorse, foot, tm="\u2122",
                   head_y=0.155):
    img = cover(Image.open(photo_path).convert("RGB"), W, H).convert("RGBA")
    soft_band(img, int(H * (head_y + 0.06)), sigma=int(H * 0.13), strength=155)
    soft_band(img, int(H * 0.97), sigma=int(H * 0.10), strength=120)
    draw = ImageDraw.Draw(img)

    txt = name.upper()
    size, f, tr = fit_light(draw, txt, W - 2 * MARGIN - 80)
    total = track_width(draw, txt, f, tr)
    y = int(H * head_y)
    track_text(draw, ((W - total) / 2, y), txt, f, (255, 255, 255), tr)

    ftm = font(F_LIGHT, int(size * 0.32))
    draw.text(((W + total) / 2 + 8, y - 2), tm, font=ftm, fill=(255, 255, 255, 215))

    fe = font(F_BOLD, 20)
    we = track_width(draw, endorse.upper(), fe, 3.2)
    track_text(draw, ((W - we) / 2, y + int(size * 1.55)), endorse.upper(), fe,
               (255, 255, 255, 230), 3.2)

    lw = 156
    paste_logo(img, lw, ((W - lw) // 2, y + int(size * 1.55) + 48), white=True)

    draw.line([(W // 2 - 30, H - 214), (W // 2 + 30, H - 214)], fill=ORANGE, width=4)

    ff = font(F_BOLD, 19)
    fy = H - 176
    for line in wrap(draw, foot.upper(), ff, 820, 1.4):
        wf = track_width(draw, line, ff, 1.4)
        track_text(draw, ((W - wf) / 2, fy), line, ff, (255, 255, 255, 235), 1.4)
        fy += 30

    lum = mean_lum(img, (int(W * 0.2), y, int(W * 0.8), y + size))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  lb-hero  name={size}px  headline-ground lum={lum:.0f}")


# --------------------------------------------------------- B: statement piece
def poster_lb_statement(photo_path, out_path, label, headline, body, tag,
                        head_y=0.575):
    img = cover(Image.open(photo_path).convert("RGB"), W, H).convert("RGBA")
    soft_band(img, int(H * (head_y + 0.10)), sigma=int(H * 0.19), strength=165)
    draw = ImageDraw.Draw(img)

    # small label + rule, top left — ink picked from the ground beneath it
    label_light = mean_lum(img, (MARGIN, int(H * 0.05),
                                 MARGIN + 430, int(H * 0.098))) >= 140
    # A subtle halo in the opposite tone. Invisible on an even ground, but it saves the
    # label when it crosses a high-contrast edge (a bright window behind dark shelves,
    # for example) where a single ink choice cannot work.
    fl = font(F_BOLD, 19)
    track_text(draw, (MARGIN, int(H * 0.062)), label.upper(), fl,
               (26, 24, 22, 235) if label_light else (255, 255, 255, 225), 3.4,
               stroke=2,
               stroke_fill=(255, 255, 255, 150) if label_light else (0, 0, 0, 150))
    draw.line([(MARGIN, int(H * 0.092)), (MARGIN + 150, int(H * 0.092))],
              fill=ORANGE if not label_light else (176, 58, 0), width=3)

    # wordmark, top right — same treatment, else it washes out on pale sky
    lw = 118
    logo_light = mean_lum(img, (W - MARGIN - lw, int(H * 0.05),
                                W - MARGIN, int(H * 0.108))) >= 140
    paste_logo(img, lw, (W - MARGIN - lw, int(H * 0.055)), white=not logo_light)

    # headline, thin and wide, two lines allowed
    lines = headline.split("|")
    size, f, tr = fit_light(draw, max(lines, key=len).upper(), W - 2 * MARGIN - 40,
                            start=92)
    y = int(H * head_y)
    for line in lines:
        t = line.strip().upper()
        tw = track_width(draw, t, f, tr)
        track_text(draw, ((W - tw) / 2, y), t, f, (255, 255, 255), tr)
        y += int(size * 1.7)

    draw.line([(W // 2 - 30, y + 14), (W // 2 + 30, y + 14)], fill=ORANGE, width=4)

    fb = font(F_BOLD, 19)
    by = y + 56
    for line in wrap(draw, body.upper(), fb, 780, 1.4):
        wb = track_width(draw, line, fb, 1.4)
        track_text(draw, ((W - wb) / 2, by), line, fb, (255, 255, 255, 232), 1.4)
        by += 30

    # closing tag — orange on dark ground, deepened orange on light ground
    ft = font(F_BOLD, 19)
    tt = f"[ {tag.upper()} ]"
    wt = track_width(draw, tt, ft, 2.4)
    tag_ink = ORANGE if mean_lum(img, (int(W * 0.3), H - 140, int(W * 0.7), H - 104)) < 140 \
        else (176, 58, 0)
    track_text(draw, ((W - wt) / 2, H - 132), tt, ft, tag_ink, 2.4)

    lum = mean_lum(img, (int(W * 0.2), int(H * head_y), int(W * 0.8),
                         int(H * head_y) + size))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  lb-statement  head={size}px  headline-ground lum={lum:.0f}")
