"""Four further BOEGÖW layouts. Palette stays in PivtMedia's own world — orange, cream,
ink, warm ochre — no cold primaries.

`poster_diptych`  — vertical split: photo panel | solid colour type panel.
`poster_knockout` — solid orange band with the headline knocked out to reveal the photo.
`poster_triptych` — three stacked panels cropped from one frame, type beneath.
`poster_receipt`  — printed-receipt aesthetic, playing off the barcode mark.
"""
import os
from PIL import Image, ImageDraw

from poster import (W, H, MARGIN, ORANGE, INK, PAPER, F_BOLD, font, track_text,
                    track_width, fit_size, wrap, micro_block, paste_logo, cover,
                    scrim_bottom, mean_lum)

CREAM = (247, 243, 233)
OCHRE = (214, 138, 20)
BONE = (232, 226, 214)


# ------------------------------------------------------------- A: diptych
def poster_diptych(photo_path, out_path, l1, l2, kicker, micro, panel=ORANGE,
                   split=0.52):
    img = Image.new("RGBA", (W, H), panel + (255,))
    pw = int(W * split)
    img.paste(cover(Image.open(photo_path).convert("RGB"), pw, H), (0, 0))
    draw = ImageDraw.Draw(img)

    tx = pw + 56
    tw = W - tx - 56

    fk = font(F_BOLD, 24)
    track_text(draw, (tx, int(H * 0.10)), kicker.upper(), fk, INK, 4.0)

    size = fit_size(draw, [l1, l2], F_BOLD, tw)
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = int(H * 0.30)
    for line, col in ((l1, INK), (l2, CREAM)):
        track_text(draw, (tx, y), line, f, col, tr)
        y += int(size * 1.04)

    draw.line([(tx, int(H * 0.70)), (W - 56, int(H * 0.70))], fill=INK + (110,), width=2)
    micro_block(draw, (tx, int(H * 0.72)), micro, size=19, max_w=tw)

    lw = 132
    paste_logo(img, lw, (tx, H - 150))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  diptych  headline={size}px")


# ------------------------------------------------------------ B: knockout
def poster_knockout(photo_path, out_path, word, sub, micro_l, micro_r, band=ORANGE,
                    sub_bar=None):
    img = cover(Image.open(photo_path).convert("RGB"), W, H).convert("RGBA")
    scrim_bottom(img, height_frac=0.30, strength=180)
    draw = ImageDraw.Draw(img)

    # solid band with the word cut out of it
    by0, by1 = int(H * 0.36), int(H * 0.60)
    band_layer = Image.new("RGBA", (W, by1 - by0), band + (255,))
    bd = ImageDraw.Draw(band_layer)

    size = 400
    f = font(F_BOLD, size)
    while track_width(draw, word, f, -0.03 * size) > W - 2 * MARGIN and size > 40:
        size -= 8
        f = font(F_BOLD, size)
    tr = -0.03 * size
    ww = track_width(draw, word, f, tr)
    # punch the letters out of the band (alpha 0 where the glyphs are)
    track_text(bd, ((W - ww) / 2, (by1 - by0) / 2 - size * 0.62), word, f,
               (0, 0, 0, 0), tr)
    img.alpha_composite(band_layer, (0, by0))

    # sub-line sits just under the band, on whatever the photograph provides there —
    # pick ink from that ground rather than assuming a dark image
    fs = font(F_BOLD, 30)
    sw = track_width(draw, sub.upper(), fs, 4.0)
    # On a busy ground no single ink survives — sub_bar gives the line its own solid ground.
    if sub_bar:
        draw.rectangle([(W - sw) / 2 - 28, by1, (W + sw) / 2 + 28, by1 + 100], fill=sub_bar)
        sub_light = mean_lum(img, (int(W * 0.45), by1 + 40, int(W * 0.55), by1 + 70)) >= 125
    else:
        sub_light = mean_lum(img, (int(W * 0.2), by1 + 34, int(W * 0.8), by1 + 78)) >= 125
    track_text(draw, ((W - sw) / 2, by1 + 40), sub.upper(), fs,
               (22, 20, 18) if sub_light else (255, 255, 255), 4.0)

    rule_y = H - 300
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=(255, 255, 255, 95), width=2)
    micro_block(draw, (MARGIN, rule_y + 34), micro_l, max_w=470, fill=(255, 255, 255))
    micro_block(draw, (W - MARGIN, rule_y + 34), micro_r, max_w=470,
                fill=(255, 255, 255), right=True)

    lw = 150
    paste_logo(img, lw, ((W - lw) // 2, H - 150), white=True)
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  knockout  word={size}px")


# ------------------------------------------------------------ C: triptych
def poster_triptych(photo_path, out_path, l1, l2, labels, micro, crops=None):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    draw = ImageDraw.Draw(img)

    src = Image.open(photo_path).convert("RGB")
    gut, top = 14, int(H * 0.06)
    pw = (W - 2 * MARGIN - 2 * gut) // 3
    ph = int(H * 0.42)
    crops = crops or [(0.0, 0.34), (0.33, 0.67), (0.66, 1.0)]
    for i, (x0, x1) in enumerate(crops):
        piece = src.crop((int(src.width * x0), 0, int(src.width * x1), src.height))
        img.paste(cover(piece, pw, ph), (MARGIN + i * (pw + gut), top))

    fl = font(F_BOLD, 21)
    for i, lab in enumerate(labels):
        track_text(draw, (MARGIN + i * (pw + gut), top + ph + 18), lab.upper(), fl,
                   INK, 2.0)

    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = int(H * 0.60)
    for line, col in ((l1, INK), (l2, ORANGE)):
        track_text(draw, (MARGIN, y), line, f, col, tr)
        y += int(size * 1.02)

    rule_y = H - 290
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=INK + (90,), width=2)
    micro_block(draw, (MARGIN, rule_y + 32), micro, max_w=880)

    lw = 140
    paste_logo(img, lw, (W - MARGIN - lw, H - 152))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  triptych  headline={size}px")


# ------------------------------------------------------------- D: receipt
def poster_receipt(out_path, title, rows, total_label, total, foot, bg=INK,
                   paper=CREAM, width_frac=0.56, row_h=84):
    img = Image.new("RGBA", (W, H), bg + (255,))
    draw = ImageDraw.Draw(img)

    slip_w = int(W * width_frac)
    rx0, rx1 = (W - slip_w) // 2, (W + slip_w) // 2

    # measure the content so the slip is exactly as long as it needs to be
    fw_m = font(F_BOLD, 20)
    foot_lines = wrap(draw, foot.upper(), fw_m, rx1 - rx0 - 92, 1.4)
    logo_h = int(190 * 341 / 640)
    content_h = (64 + 44 + 62 + 40 + len(rows) * row_h + 26 + 74
                 + 96 + len(foot_lines) * 32 + 54 + logo_h + 86)
    ry0 = max(int(H * 0.05), (H - content_h) // 2)
    ry1 = ry0 + content_h
    draw.rectangle([rx0, ry0, rx1, ry1], fill=paper)

    # torn/perforated bottom edge
    step = 26
    for x in range(rx0, rx1, step):
        draw.ellipse([x, ry1 - step // 2, x + step, ry1 + step // 2], fill=bg)

    pad = 44
    ft = font(F_BOLD, 40)
    tw = track_width(draw, title.upper(), ft, 5.0)
    track_text(draw, ((W - tw) / 2, ry0 + 64), title.upper(), ft, INK, 5.0)

    y = ry0 + 64 + 44 + 62
    draw.line([(rx0 + pad, y), (rx1 - pad, y)], fill=INK + (70,), width=3)
    y += 40

    fr = font(F_BOLD, 25)
    for label, val in rows:
        track_text(draw, (rx0 + pad, y), label.upper(), fr, INK, 1.6)
        track_text(draw, (rx1 - pad, y), val.upper(), fr,
                   ORANGE if val.strip().startswith("+") else INK, 1.6,
                   anchor_right=True)
        y += row_h - 30
        for dx in range(rx0 + pad, rx1 - pad, 14):
            draw.line([(dx, y - 10), (dx + 7, y - 10)], fill=INK + (60,), width=2)
        y += 30

    y += 26
    fl = font(F_BOLD, 32)
    track_text(draw, (rx0 + pad, y + 12), total_label.upper(), fl, INK, 2.0)
    ftot = font(F_BOLD, 56)
    track_text(draw, (rx1 - pad, y - 6), total, ftot, ORANGE, -1.0, anchor_right=True)

    y += 96
    fw = font(F_BOLD, 20)
    for line in foot_lines:
        lw_ = track_width(draw, line, fw, 1.4)
        track_text(draw, ((W - lw_) / 2, y), line, fw, INK, 1.4)
        y += 32

    lw = 190
    paste_logo(img, lw, ((W - lw) // 2, y + 54))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  receipt")
