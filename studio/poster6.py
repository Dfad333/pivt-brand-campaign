"""Two quieter layouts to sit alongside the proven duotone / riso / stat set.

`poster_word`  — type-only: one enormous word on a colour field, with small numbered
                 annotations pinned around it.
`poster_label` — gallery-catalogue layout: a small centred image in generous white space,
                 with a museum specimen label beneath.
"""
import os
from PIL import Image, ImageDraw

from poster import (W, H, MARGIN, ORANGE, INK, PAPER, F_BOLD, font, track_text,
                    track_width, fit_size, wrap, micro_block, paste_logo, cover)

CREAM = (247, 243, 233)
RULE = (196, 192, 185)


# --------------------------------------------------------- 1: giant word
def poster_word(out_path, word, notes, foot_l, foot_r, bg=INK, word_col=ORANGE,
                ghost=None):
    """One huge word. `notes` are (text, (x_frac, y_frac)) annotations."""
    img = Image.new("RGBA", (W, H), bg + (255,))
    draw = ImageDraw.Draw(img)

    # optional oversized ghost of the same word, bleeding off the top
    if ghost:
        gs = 900
        fg = font(F_BOLD, gs)
        gw = track_width(draw, ghost, fg, -0.04 * gs)
        track_text(draw, ((W - gw) / 2, -int(gs * 0.30)), ghost, fg,
                   tuple(min(255, c + 16) for c in bg) + (255,), -0.04 * gs)

    size = 520
    f = font(F_BOLD, size)
    while track_width(draw, word, f, -0.035 * size) > W - 2 * MARGIN and size > 60:
        size -= 8
        f = font(F_BOLD, size)
    tr = -0.035 * size
    ww = track_width(draw, word, f, tr)
    wy = int(H * 0.40)
    track_text(draw, ((W - ww) / 2, wy), word, f, word_col, tr)

    fn = font(F_BOLD, 20)
    for i, (text, (nx, ny)) in enumerate(notes, start=1):
        x, y = int(W * nx), int(H * ny)
        track_text(draw, (x, y), f"{i:02d}", fn, ORANGE, 1.5)
        micro_block(draw, (x + 44, y), text, size=20, max_w=330, fill=CREAM)

    rule_y = H - 300
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=CREAM + (95,), width=2)
    micro_block(draw, (MARGIN, rule_y + 34), foot_l, max_w=470, fill=CREAM)
    micro_block(draw, (W - MARGIN, rule_y + 34), foot_r, max_w=470, fill=CREAM,
                right=True)

    lw = 150
    paste_logo(img, lw, ((W - lw) // 2, H - 150), white=True)
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  word  {size}px")


# ------------------------------------------------------- 2: catalogue label
def poster_label(photo_path, out_path, title, meta_rows, body, cat_no="PM-001"):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    draw = ImageDraw.Draw(img)

    # small plate, generous margins
    pw, ph = int(W * 0.70), int(H * 0.50)
    px, py = (W - pw) // 2, int(H * 0.085)
    img.paste(cover(Image.open(photo_path).convert("RGB"), pw, ph), (px, py))

    fc = font(F_BOLD, 19)
    track_text(draw, (px, py - 34), cat_no.upper(), fc, INK, 3.0)
    track_text(draw, (px + pw, py - 34), "PIVTMEDIA ARCHIVE", fc, INK, 3.0,
               anchor_right=True)

    # specimen label
    ly = py + ph + 66
    draw.line([(px, ly), (px + pw, ly)], fill=RULE, width=2)
    ly += 30

    ft = font(F_BOLD, 62)
    track_text(draw, (px, ly), title.upper(), ft, INK, -1.0)
    ly += 92

    fm = font(F_BOLD, 20)
    for k, v in meta_rows:
        track_text(draw, (px, ly), k.upper(), fm, ORANGE, 2.0)
        track_text(draw, (px + 250, ly), v.upper(), fm, INK, 2.0)
        ly += 34

    ly += 26
    draw.line([(px, ly), (px + pw, ly)], fill=RULE, width=2)
    end_y = micro_block(draw, (px, ly + 28), body, size=20, max_w=pw)

    lw = 132
    paste_logo(img, lw, (px, min(end_y + 54, H - 150)))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  label")
