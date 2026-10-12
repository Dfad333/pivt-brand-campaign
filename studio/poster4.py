"""Four colour-led BOEGÖW-lineage layouts, each a distinct visual system.

`poster_duotone` — full-bleed duotone photo, huge headline, colour block.
`poster_bands`   — Swiss colour-band stack, photo occupying one band.
`poster_riso`    — halftone dot screen printed in two colours with deliberate misregistration.
`poster_stat`    — type-only: giant numeral hero on a colour field.
"""
import os
from PIL import Image, ImageDraw, ImageOps

from poster import (W, H, MARGIN, ORANGE, INK, PAPER, F_BOLD, font, track_text,
                    track_width, fit_size, wrap, micro_block, paste_logo, cover)

BLUE = (18, 46, 214)
MAGENTA = (255, 45, 111)
YELLOW = (255, 206, 0)
CREAM = (247, 243, 233)


def duotone(im, shadow, light):
    """Map a greyscale image onto a two-colour ramp."""
    g = ImageOps.grayscale(im)
    return ImageOps.colorize(g, black=shadow, white=light).convert("RGBA")


def halftone(im, cell, colour, angle=0, size=(W, H)):
    """Return an RGBA layer of `colour` dots whose radius tracks image darkness."""
    g = ImageOps.grayscale(im.resize(size, Image.LANCZOS))
    if angle:
        g = g.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=255)
    px = g.load()
    layer = Image.new("RGBA", (size[0] * 2, size[1] * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r_max = cell * 0.78
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            v = px[min(x, size[0] - 1), min(y, size[1] - 1)]
            r = (1 - v / 255) * r_max
            if r > 0.35:
                cx, cy = (x + cell / 2) * 2, (y + cell / 2) * 2
                d.ellipse([cx - r * 2, cy - r * 2, cx + r * 2, cy + r * 2], fill=colour)
    return layer.resize(size, Image.LANCZOS)


# ------------------------------------------------------------- 1: duotone
def poster_duotone(photo_path, out_path, l1, l2, chip, micro_l, micro_r,
                   shadow=(10, 12, 60), light=(255, 92, 0)):
    img = duotone(cover(Image.open(photo_path).convert("RGB"), W, H), shadow, light)
    draw = ImageDraw.Draw(img)

    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = H - 430 - int(size * 2.05)
    for line in (l1, l2):
        track_text(draw, (MARGIN, y), line, f, CREAM, tr)
        y += int(size * 1.02)

    # colour chip
    fc = font(F_BOLD, 26)
    cw = track_width(draw, chip, fc, 3.0)
    draw.rectangle([MARGIN, int(H * 0.085), MARGIN + cw + 56, int(H * 0.085) + 58],
                   fill=CREAM)
    track_text(draw, (MARGIN + 28, int(H * 0.085) + 14), chip, fc, shadow, 3.0)

    rule_y = H - 300
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=CREAM + (110,), width=2)
    micro_block(draw, (MARGIN, rule_y + 34), micro_l, max_w=470, fill=CREAM)
    micro_block(draw, (W - MARGIN, rule_y + 34), micro_r, max_w=470, fill=CREAM, right=True)

    lw = 150
    paste_logo(img, lw, ((W - lw) // 2, H - 150), white=True)
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  duotone  headline={size}px")


# --------------------------------------------------------------- 2: bands
def poster_bands(photo_path, out_path, l1, l2, kicker, micro, rows):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, int(H * 0.10)], fill=BLUE)
    ph0, ph1 = int(H * 0.10), int(H * 0.46)
    img.paste(cover(Image.open(photo_path).convert("RGB"), W, ph1 - ph0), (0, ph0))
    draw.rectangle([0, ph1, W, int(H * 0.52)], fill=ORANGE)
    draw.rectangle([0, int(H * 0.855), W, H], fill=INK)

    fk = font(F_BOLD, 26)
    track_text(draw, (MARGIN, int(H * 0.038)), kicker.upper(), fk, CREAM, 4.0)
    fr = font(F_BOLD, 27)
    track_text(draw, (W - MARGIN, int(H * 0.038)), rows.upper(), fr, CREAM, 4.0,
               anchor_right=True)

    fb = font(F_BOLD, 30)
    track_text(draw, (MARGIN, int(H * 0.472)), micro.upper(), fb, INK, 3.0)

    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = int(H * 0.575)
    for line, col in ((l1, INK), (l2, BLUE)):
        track_text(draw, (MARGIN, y), line, f, col, tr)
        y += int(size * 1.02)

    lw = 150
    paste_logo(img, lw, ((W - lw) // 2, int(H * 0.90)), white=True)
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  bands  headline={size}px")


# ----------------------------------------------------------------- 3: riso
def poster_riso(photo_path, out_path, l1, l2, note, micro_l, micro_r,
                c1=MAGENTA, c2=(18, 46, 214)):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    src = cover(Image.open(photo_path).convert("RGB"), W, H)

    # two screens, deliberately misregistered
    img.alpha_composite(halftone(src, 11, c2 + (205,)), (7, 6))
    img.alpha_composite(halftone(src, 11, c1 + (190,)), (0, 0))
    draw = ImageDraw.Draw(img)

    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = int(H * 0.60)
    for line in (l1, l2):
        track_text(draw, (MARGIN, y), line, f, INK, tr)
        y += int(size * 1.02)

    fn = font(F_BOLD, 27)
    track_text(draw, (MARGIN, int(H * 0.083)), note.upper(), fn, INK, 3.5)

    rule_y = H - 300
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=INK + (110,), width=2)
    micro_block(draw, (MARGIN, rule_y + 34), micro_l, max_w=470)
    micro_block(draw, (W - MARGIN, rule_y + 34), micro_r, max_w=470, right=True)

    lw = 150
    paste_logo(img, lw, ((W - lw) // 2, H - 150))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  riso  headline={size}px")


# ----------------------------------------------------------------- 4: stat
def poster_stat(out_path, stat, unit, l1, l2, micro_l, micro_r, bg=ORANGE):
    img = Image.new("RGBA", (W, H), bg + (255,))
    draw = ImageDraw.Draw(img)

    # giant numeral
    ssize = 620
    fs = font(F_BOLD, ssize)
    while track_width(draw, stat, fs, -0.03 * ssize) > W - 2 * MARGIN - 150:
        ssize -= 10
        fs = font(F_BOLD, ssize)
    sw = track_width(draw, stat, fs, -0.03 * ssize)
    sx, sy = MARGIN, int(H * 0.20)
    track_text(draw, (sx, sy), stat, fs, INK, -0.03 * ssize)

    fu = font(F_BOLD, int(ssize * 0.16))
    track_text(draw, (sx + sw + 22, sy + int(ssize * 0.10)), unit, fu, CREAM, 2.0)

    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = int(H * 0.60)
    for line, col in ((l1, CREAM), (l2, INK)):
        track_text(draw, (MARGIN, y), line, f, col, tr)
        y += int(size * 1.02)

    rule_y = H - 300
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=INK + (110,), width=2)
    micro_block(draw, (MARGIN, rule_y + 34), micro_l, max_w=470)
    micro_block(draw, (W - MARGIN, rule_y + 34), micro_r, max_w=470, right=True)

    lw = 150
    paste_logo(img, lw, ((W - lw) // 2, H - 150))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  stat  numeral={ssize}px headline={size}px")
