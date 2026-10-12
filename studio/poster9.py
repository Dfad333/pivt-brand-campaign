"""Two colour-led layouts, both new.

`poster_scatter` — the last unused BOEGÖW device (`references/boegow/h-aug10.jpg`): several
                   small captioned plates placed off-grid on a pale field, connector dots,
                   vertical side text, headline floating in open space.
`poster_window`  — inverse of the disc: a flat colour field with a large circular window cut
                   through it revealing the photograph.
"""
import os
from PIL import Image, ImageDraw

from poster import (W, H, MARGIN, ORANGE, INK, F_BOLD, font, track_text,
                    track_width, fit_size, wrap, micro_block, paste_logo, cover)

CREAM = (247, 243, 233)
RULE = (198, 194, 186)


# ------------------------------------------------------------- 1: scatter
def poster_scatter(plates, out_path, l1, l2, side_text, foot, body=None, bg=CREAM):
    """`plates` = list of (path, caption, (x_frac, y_frac), w_frac)."""
    img = Image.new("RGBA", (W, H), bg + (255,))
    draw = ImageDraw.Draw(img)

    fc = font(F_BOLD, 18)
    centres = []
    for path, caption, (fx, fy), fw in plates:
        pw = int(W * fw)
        ph = int(pw * 1.18)
        px, py = int(W * fx), int(H * fy)
        img.paste(cover(Image.open(path).convert("RGB"), pw, ph), (px, py))
        track_text(draw, (px, py + ph + 16), caption.upper(), fc, INK, 2.2)
        centres.append((px + pw // 2, py + ph // 2))

    # connector dots between plates
    for cx, cy in centres:
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=ORANGE)

    # vertical side text, left edge
    fs = font(F_BOLD, 19)
    sw = track_width(draw, side_text.upper(), fs, 3.0)
    strip = Image.new("RGBA", (int(sw) + 20, 34), (0, 0, 0, 0))
    track_text(ImageDraw.Draw(strip), (0, 0), side_text.upper(), fs, INK, 3.0)
    strip = strip.rotate(90, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(strip, (MARGIN - 30, int(H * 0.30)))

    # headline floating in open space, right of centre
    size = fit_size(draw, [l1, l2], F_BOLD, int(W * 0.58))
    f = font(F_BOLD, size)
    tr = -0.02 * size
    hx, hy = int(W * 0.38), int(H * 0.565)
    for line in (l1, l2):
        track_text(draw, (hx, hy), line, f, INK, tr)
        hy += int(size * 1.04)

    if body:
        micro_block(draw, (hx, hy + 30), body, size=20, max_w=int(W * 0.56))

    draw.line([(MARGIN, H - 250), (W - MARGIN, H - 250)], fill=RULE, width=2)
    micro_block(draw, (MARGIN, H - 218), foot, size=19, max_w=760)

    lw = 130
    paste_logo(img, lw, (W - MARGIN - lw, H - 214))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  scatter  headline={size}px")


# -------------------------------------------------------------- 2: window
def poster_window(photo_path, out_path, l1, l2, kicker, foot_l, foot_r,
                  field=ORANGE, radius=0.27, cy=0.36, head_y=0.665):
    """Flat colour field with a circular window punched through to the photograph."""
    photo = cover(Image.open(photo_path).convert("RGB"), W, H).convert("RGBA")
    field_layer = Image.new("RGBA", (W, H), field + (255,))

    mask = Image.new("L", (W * 2, H * 2), 255)
    md = ImageDraw.Draw(mask)
    r = int(W * radius) * 2
    md.ellipse([W - r, int(H * cy) * 2 - r, W + r, int(H * cy) * 2 + r], fill=0)
    field_layer.putalpha(mask.resize((W, H), Image.LANCZOS))

    img = photo
    img.alpha_composite(field_layer)
    draw = ImageDraw.Draw(img)

    rule_y = H - 250

    fk = font(F_BOLD, 24)
    kw = track_width(draw, kicker.upper(), fk, 4.0)
    track_text(draw, ((W - kw) / 2, int(H * 0.042)), kicker.upper(), fk, INK, 4.0)

    # cap the headline so both lines clear the hairline below
    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    size = min(size, int((rule_y - 46 - int(H * head_y)) / 2.02))
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = int(H * head_y)
    for line, col in ((l1, INK), (l2, CREAM)):
        lw_ = track_width(draw, line, f, tr)
        track_text(draw, ((W - lw_) / 2, y), line, f, col, tr)
        y += int(size * 1.02)

    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=INK + (110,), width=2)
    micro_block(draw, (MARGIN, rule_y + 30), foot_l, max_w=460)
    micro_block(draw, (W - MARGIN, rule_y + 30), foot_r, max_w=460, right=True)

    lw = 140
    paste_logo(img, lw, ((W - lw) // 2, H - 132))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  window  headline={size}px")
