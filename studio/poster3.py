"""Two further BOEGÖW-lineage layouts.

`poster_index`   — paper ground, hairline grid, small inset photo, numbered index rows.
`poster_outline` — full-bleed B&W with a huge outline-only headline and vertical side text.
"""
import os
from PIL import Image, ImageDraw

from poster import (W, H, MARGIN, ORANGE, INK, PAPER, F_BOLD, font, track_text,
                    track_width, fit_size, wrap, micro_block, paste_logo, cover,
                    mean_lum, scrim_bottom)
from poster2 import tape

RULE = (196, 192, 185)


# ---------------------------------------------------------- E: editorial index
def poster_index(photo_path, out_path, bracket, l1, l2, index_rows, foot,
                 tape_text=None):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    draw = ImageDraw.Draw(img)

    # hairline grid across the upper field
    for fy in (0.045, 0.075, 0.315, 0.345):
        y = int(H * fy)
        draw.line([(0, y), (W, y)], fill=RULE, width=2)
    for fx in (0.10, 0.90):
        x = int(W * fx)
        draw.line([(x, int(H * 0.045)), (x, int(H * 0.345))], fill=RULE, width=2)

    # inset photograph
    pw, ph = 520, 650
    px, py = (W - pw) // 2, int(H * 0.075)
    img.paste(cover(Image.open(photo_path).convert("RGB"), pw, ph), (px, py))

    if tape_text:
        tape(img, tape_text, (px - 90, py - 34), angle=-7)

    # bracketed fragment
    fb = font(F_BOLD, 34)
    wb = track_width(draw, bracket, fb, 3.0)
    track_text(draw, ((W - wb) / 2, int(H * 0.422)), bracket, fb, INK, 3.0)

    # headline
    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = int(H * 0.46)
    for line in (l1, l2):
        wl = track_width(draw, line, f, tr)
        track_text(draw, ((W - wl) / 2, y), line, f, INK, tr)
        y += int(size * 1.02)

    # numbered index rows
    fn = font(F_BOLD, 22)
    ry = int(H * 0.74)
    for i, (label, val) in enumerate(index_rows, start=1):
        draw.line([(MARGIN, ry), (W - MARGIN, ry)], fill=RULE, width=2)
        track_text(draw, (MARGIN, ry + 18), f"{i:02d}", fn, ORANGE, 1.5)
        track_text(draw, (MARGIN + 78, ry + 18), label.upper(), fn, INK, 1.5)
        track_text(draw, (W - MARGIN, ry + 18), val.upper(), fn, INK, 1.5,
                   anchor_right=True)
        ry += 64
    draw.line([(MARGIN, ry), (W - MARGIN, ry)], fill=RULE, width=2)

    micro_block(draw, (MARGIN, H - 168), foot, size=19, max_w=760)

    lw = 140
    paste_logo(img, lw, (W - MARGIN - lw, H - 168))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  {W}x{H}  headline={size}px")


# -------------------------------------------------------- F: outline headline
def poster_outline(photo_path, out_path, l1, l2, side_text, micro_l, micro_r,
                   bar_word=None):
    img = cover(Image.open(photo_path).convert("RGB"), W, H).convert("RGBA")

    # This layout was built for dark photographs. On a bright image (a salt flat, a pale
    # sky) white type and a thin white outline both disappear, so measure first and push
    # the scrim harder / flip to dark ink where needed.
    head_lum = mean_lum(img, (int(W * 0.10), int(H * 0.28),
                              int(W * 0.90), int(H * 0.62)))
    head_ink = (24, 22, 20) if head_lum >= 140 else (255, 255, 255)

    foot_lum = mean_lum(img, (MARGIN, H - 300, W - MARGIN, H - 150))
    scrim_bottom(img, height_frac=0.34,
                 strength=175 if foot_lum < 140 else 232)
    draw = ImageDraw.Draw(img)

    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = int(H * 0.30)

    # line 1 solid, line 2 outline-only — the device that carries this layout
    wl = track_width(draw, l1, f, tr)
    track_text(draw, ((W - wl) / 2, y), l1, f, head_ink, tr)
    y += int(size * 1.02)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    wl2 = track_width(draw, l2, f, tr)
    track_text(ld, ((W - wl2) / 2, y), l2, f, (0, 0, 0, 0), tr,
               stroke=max(4, size // 40), stroke_fill=head_ink + (255,))
    img.alpha_composite(layer)

    # orange bar under the outline line
    if bar_word:
        fb = font(F_BOLD, 26)
        bw = track_width(draw, bar_word, fb, 3.0)
        bx, by = (W - bw) / 2 - 26, y + int(size * 1.18)
        draw.rectangle([bx, by, bx + bw + 52, by + 54], fill=ORANGE)
        track_text(draw, (bx + 26, by + 12), bar_word, fb, INK, 3.0)

    # vertical side text down the left edge
    fs = font(F_BOLD, 21)
    sw = track_width(draw, side_text.upper(), fs, 3.0)
    side_ink = head_ink + (215,)
    strip = Image.new("RGBA", (int(sw) + 20, 40), (0, 0, 0, 0))
    track_text(ImageDraw.Draw(strip), (0, 0), side_text.upper(), fs, side_ink, 3.0)
    strip = strip.rotate(90, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(strip, (MARGIN - 34, int(H * 0.44)))

    rule_y = H - 300
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=(255, 255, 255, 95), width=2)
    micro_block(draw, (MARGIN, rule_y + 34), micro_l, max_w=470, fill=(255, 255, 255))
    micro_block(draw, (W - MARGIN, rule_y + 34), micro_r, max_w=470,
                fill=(255, 255, 255), right=True)

    lw = 150
    paste_logo(img, lw, ((W - lw) // 2, H - 150), white=True)
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  {W}x{H}  headline={size}px")
