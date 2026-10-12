"""Composite the PivtMedia barcode lockup (and optional tagline) onto a campaign still.

Logo goes top-centre, matching the reference layout: ~13% of canvas width, ~5% top margin.
Ink colour is chosen from the measured brightness of the region the logo will sit in, so it
never disappears into the background.
"""
import argparse
import os

import paths
from PIL import Image, ImageDraw, ImageFont

LOGO_DIR = paths.LOGO_DIR
LOGO_LIGHT = os.path.join(LOGO_DIR, "pivt-logo-transparent-white.png")
LOGO_DARK = os.path.join(LOGO_DIR, "pivt-logo-transparent-black.png")
FONT_PATH = paths.F_BAHN

TARGET_W, TARGET_H = 1600, 2000  # 4:5


def crop_to_ratio(im, ratio=4 / 5, top_bias=0.35):
    """Centre-crop to `ratio`, biased upward so headroom for the logo is preserved."""
    w, h = im.size
    if w / h > ratio:                      # too wide -> trim sides
        new_w = int(round(h * ratio))
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(round(w / ratio))          # too tall -> trim height
    top = int(round((h - new_h) * top_bias))
    return im.crop((0, top, w, top + new_h))


def region_is_dark(im, box):
    """Mean luminance of `box` < 128."""
    px = im.convert("L").crop(box)
    return sum(px.getdata()) / (px.size[0] * px.size[1]) < 128


def compose(src_path, out_path, tagline=None, tagline_y=0.62,
            logo_w_pct=0.13, logo_top_pct=0.05, force_ink=None, type_pct=0.017):
    im = Image.open(src_path).convert("RGB")
    im = crop_to_ratio(im).resize((TARGET_W, TARGET_H), Image.LANCZOS)

    # --- logo ---
    logo_w = int(TARGET_W * logo_w_pct)
    probe_top = int(TARGET_H * logo_top_pct)
    probe = (TARGET_W // 2 - logo_w // 2, probe_top,
             TARGET_W // 2 + logo_w // 2, probe_top + int(logo_w * 0.55))

    if force_ink:
        use_light = force_ink == "white"
    else:
        use_light = region_is_dark(im, probe)

    logo = Image.open(LOGO_LIGHT if use_light else LOGO_DARK).convert("RGBA")
    logo = logo.resize((logo_w, int(logo_w * logo.height / logo.width)), Image.LANCZOS)
    im = im.convert("RGBA")
    im.alpha_composite(logo, (TARGET_W // 2 - logo.width // 2, probe_top))

    # --- tagline ---
    if tagline:
        ink = (255, 255, 255, 235) if use_light else (26, 26, 26, 235)
        size = int(TARGET_W * type_pct)
        font = ImageFont.truetype(FONT_PATH, size)
        draw = ImageDraw.Draw(im)
        tracking = int(size * 0.16)          # letterspacing, as in the references
        y = int(TARGET_H * tagline_y)
        for line in tagline.split("|"):
            line = line.strip().upper()
            widths = [draw.textlength(ch, font=font) for ch in line]
            total = sum(widths) + tracking * (len(line) - 1)
            x = (TARGET_W - total) / 2
            for ch, cw in zip(line, widths):
                draw.text((x, y), ch, font=font, fill=ink)
                x += cw + tracking
            y += int(size * 1.9)

    im.convert("RGB").save(out_path, quality=97)
    ink_name = "white" if use_light else "black"
    print(f"{os.path.basename(out_path)}  {TARGET_W}x{TARGET_H}  logo-ink={ink_name}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("out")
    p.add_argument("--tagline", default=None, help="use | to separate lines")
    p.add_argument("--tagline-y", type=float, default=0.62)
    p.add_argument("--logo-w", type=float, default=0.13)
    p.add_argument("--logo-top", type=float, default=0.05)
    p.add_argument("--ink", choices=["white", "black"], default=None)
    p.add_argument("--type-pct", type=float, default=0.017)
    a = p.parse_args()
    compose(a.src, a.out, a.tagline, a.tagline_y, a.logo_w, a.logo_top, a.ink, a.type_pct)
