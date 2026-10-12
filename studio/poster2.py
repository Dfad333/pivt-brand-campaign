"""Two further PivtMedia poster templates.

`poster_tape`     — BOEGÖW lineage: full-bleed B&W, huge white headline, rotated orange tape.
`poster_endorse`  — LONGEBLACK lineage: warm cinematic photo, thin letterspaced centred
                    headline, discreet endorsement lockup.
"""
import os
from PIL import Image, ImageDraw

from poster import (W, H, MARGIN, ORANGE, INK, PAPER, F_BOLD, font, track_text,
                    track_width, fit_size, wrap, micro_block, paste_logo, cover,
                    mean_lum, contrast_ink, scrim_bottom)

from paths import F_LIGHT  # resolved per-machine


def bottom_scrim(img, height_frac=0.55, strength=205):
    """Dark gradient up from the bottom edge so white type stays legible."""
    h = int(H * height_frac)
    grad = Image.new("L", (1, h))
    for y in range(h):
        grad.putpixel((0, y), int(strength * (y / (h - 1)) ** 1.6))
    mask = grad.resize((W, h))
    layer = Image.new("RGBA", (W, h), (0, 0, 0, 255))
    layer.putalpha(mask)
    img.alpha_composite(layer, (0, H - h))


def tape(img, text, xy, angle=-6.5, pad=(34, 18)):
    """Rotated orange tape strip carrying small black text."""
    f = font(F_BOLD, 27)
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tw = track_width(d0, text, f, 2.0)
    w, h = int(tw + pad[0] * 2), int(27 + pad[1] * 2)
    strip = Image.new("RGBA", (w, h), ORANGE + (255,))
    track_text(ImageDraw.Draw(strip), (pad[0], pad[1] - 3), text, f, INK, 2.0)
    strip = strip.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(strip, xy)


# ------------------------------------------------------------------ C: tape
def poster_tape(photo_path, out_path, l1, l2, tape_text, micro_top, micro_l, micro_r):
    img = cover(Image.open(photo_path).convert("RGB"), W, H).convert("RGBA")
    bottom_scrim(img)
    draw = ImageDraw.Draw(img)

    # top micro-copy sits on unscrimmed photograph — pick ink from that ground
    top_light = mean_lum(img, (MARGIN, int(H * 0.07), MARGIN + 440, int(H * 0.115))) >= 140
    micro_block(draw, (MARGIN, int(H * 0.075)), micro_top, size=19,
                fill=(24, 22, 20) if top_light else (255, 255, 255), max_w=430,
                stroke=2,
                stroke_fill=(255, 255, 255, 130) if top_light else (0, 0, 0, 130))

    tape(img, tape_text, (MARGIN - 10, int(H * 0.30)))

    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = H - 470 - int(size * 2.05)
    for line in (l1, l2):
        track_text(draw, (MARGIN, y), line, f, (255, 255, 255), tr)
        y += int(size * 1.02)

    rule_y = H - 300
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=(255, 255, 255, 90), width=2)
    micro_block(draw, (MARGIN, rule_y + 34), micro_l, max_w=470, fill=(255, 255, 255))
    micro_block(draw, (W - MARGIN, rule_y + 34), micro_r, max_w=470,
                fill=(255, 255, 255), right=True)

    lw = 150
    paste_logo(img, lw, ((W - lw) // 2, H - 150), white=True)
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  {W}x{H}  headline={size}px")


# ------------------------------------------------------------- D: endorsement
def poster_endorse(photo_path, out_path, headline, endorse_line, foot, tm="\u2122",
                   y_frac=0.40, scrim=0.42):
    img = cover(Image.open(photo_path).convert("RGB"), W, H).convert("RGBA")

    # decide ink from the ground the headline will sit on, before any scrim
    band = (int(W * 0.15), int(H * y_frac) - 20, int(W * 0.85), int(H * y_frac) + 130)
    light_ground = mean_lum(img, band) >= 125
    ink = (26, 22, 20) if light_ground else (255, 255, 255)
    if not light_ground:
        bottom_scrim(img, height_frac=scrim, strength=160)
    draw = ImageDraw.Draw(img)

    # thin, widely letterspaced centred headline
    size = 96
    f = font(F_LIGHT, size)
    tr = size * 0.24
    txt = headline.upper()
    while track_width(draw, txt, f, tr) > W - 2 * MARGIN - 60 and size > 30:
        size -= 3
        f = font(F_LIGHT, size)
        tr = size * 0.24
    total = track_width(draw, txt, f, tr)
    y = int(H * y_frac)
    track_text(draw, ((W - total) / 2, y), txt, f, ink, tr)

    ftm = font(F_LIGHT, int(size * 0.34))
    draw.text(((W + total) / 2 + 6, y - 2), tm, font=ftm, fill=ink + (220,))

    # endorsement lockup
    fe = font(F_BOLD, 20)
    we = track_width(draw, endorse_line.upper(), fe, 3.0)
    track_text(draw, ((W - we) / 2, y + int(size * 1.5)), endorse_line.upper(), fe,
               ink + (230,), 3.0)

    lw = 160
    paste_logo(img, lw, ((W - lw) // 2, y + int(size * 1.5) + 46), white=not light_ground)

    draw.line([(W // 2 - 34, H - 268), (W // 2 + 34, H - 268)], fill=ORANGE, width=4)

    ff = font(F_BOLD, 19)
    foot_ink = (26, 22, 20) if mean_lum(img, (int(W * 0.2), H - 226, int(W * 0.8), H - 186)) >= 125 \
        else (255, 255, 255)
    for i, line in enumerate(wrap(draw, foot.upper(), ff, 760, 1.4)):
        wf = track_width(draw, line, ff, 1.4)
        track_text(draw, ((W - wf) / 2, H - 216 + i * 30), line, ff, foot_ink + (235,), 1.4)

    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  {W}x{H}  headline={size}px")


if __name__ == "__main__":
    RAW = paths.RAW + os.sep
    OUT = paths.FINAL + os.sep

    poster_tape(
        RAW + "12-corridor-bw.png", OUT + "12-move-first.jpg",
        "MOVE FIRST.", "EXPLAIN LATER.", "No committee required",
        "Independent. Selective.",
        "Most brands wait for permission. The market rewards the ones already moving.",
        "Strategy. Content. Systems.",
    )

    poster_endorse(
        RAW + "13-lounge-warm.png", OUT + "13-a-brand-by.jpg",
        "The Standard", "A brand built by PivtMedia",
        "Not for everyone. That is the point.",
    )
