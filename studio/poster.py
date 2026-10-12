"""Editorial poster builder for PivtMedia — BOEGÖW-style layout language.

Type is the hero; the Higgsfield image is a subordinate element. Everything textual is
set here with real fonts so it stays razor-sharp at any size.
"""
import os
from PIL import Image, ImageDraw, ImageFont

import paths

W, H = 1600, 2000
MARGIN = 96
ORANGE = (255, 92, 0)
INK = (17, 17, 17)
PAPER = (247, 245, 241)

# Fonts and folders resolve per-machine — see studio/paths.py. Re-exported here because
# every other module imports them from `poster`.
F_BOLD = paths.F_BOLD                        # Helvetica-like grotesque for headlines
F_REG = paths.F_REG
LOGO_DIR = paths.LOGO_DIR
LOGO_BLACK = os.path.join(LOGO_DIR, "pivt-logo-transparent-black.png")
LOGO_WHITE = os.path.join(LOGO_DIR, "pivt-logo-transparent-white.png")


def font(path, size):
    return ImageFont.truetype(path, size)


def track_text(draw, xy, text, fnt, fill, tracking=0, anchor_right=False,
               stroke=0, stroke_fill=(0, 0, 0, 150)):
    """Draw `text` with per-character `tracking`. Returns total width."""
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + tracking * max(0, len(text) - 1)
    x, y = xy
    if anchor_right:
        x -= total
    for c, cw in zip(text, widths):
        if stroke:
            draw.text((x, y), c, font=fnt, fill=fill,
                      stroke_width=stroke, stroke_fill=stroke_fill)
        else:
            draw.text((x, y), c, font=fnt, fill=fill)
        x += cw + tracking
    return total


def track_width(draw, text, fnt, tracking=0):
    return sum(draw.textlength(c, font=fnt) for c in text) + tracking * max(0, len(text) - 1)


def fit_size(draw, lines, path, max_w, tracking_ratio=-0.02, lo=20, hi=400):
    """Largest font size where every line fits `max_w`."""
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        f = font(path, mid)
        widest = max(track_width(draw, l, f, tracking_ratio * mid) for l in lines)
        if widest <= max_w:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best


def wrap(draw, text, fnt, max_w, tracking=0):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if track_width(draw, trial, fnt, tracking) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def micro_block(draw, xy, text, size=19, fill=INK, max_w=430, tracking=1.0,
                right=False, leading=1.55, bold=True, stroke=0,
                stroke_fill=(0, 0, 0, 150)):
    """Small annotation paragraph, boegow-style."""
    f = font(F_BOLD if bold else F_REG, size)
    x, y = xy
    for line in wrap(draw, text.upper(), f, max_w, tracking):
        track_text(draw, (x, y), line, f, fill, tracking, anchor_right=right,
                   stroke=stroke, stroke_fill=stroke_fill)
        y += int(size * leading)
    return y


def paste_logo(img, box_w, xy, white=False):
    logo = Image.open(LOGO_WHITE if white else LOGO_BLACK).convert("RGBA")
    logo = logo.resize((box_w, int(box_w * logo.height / logo.width)), Image.LANCZOS)
    img.alpha_composite(logo, xy)
    return logo.height


def cover(im, w, h):
    """Scale-and-crop `im` to exactly w x h."""
    src_r, dst_r = im.width / im.height, w / h
    if src_r > dst_r:
        new_w = int(im.height * dst_r)
        im = im.crop(((im.width - new_w) // 2, 0, (im.width - new_w) // 2 + new_w, im.height))
    else:
        new_h = int(im.width / dst_r)
        top = int((im.height - new_h) * 0.30)
        im = im.crop((0, top, im.width, top + new_h))
    return im.resize((w, h), Image.LANCZOS)


def mean_lum(img, box):
    """Mean luminance (0-255) of `box`, clamped to the canvas."""
    x0, y0, x1, y1 = (max(0, box[0]), max(0, box[1]), min(W, box[2]), min(H, box[3]))
    if x1 <= x0 or y1 <= y0:
        return 128
    px = img.convert("L").crop((x0, y0, x1, y1))
    return sum(px.getdata()) / (px.size[0] * px.size[1])


def contrast_ink(img, box):
    """White on dark ground, near-black on light ground."""
    return (255, 255, 255) if mean_lum(img, box) < 125 else (20, 20, 20)


def scrim_bottom(img, height_frac=0.30, strength=190):
    """Dark gradient up from the bottom edge so white type stays legible."""
    h = int(H * height_frac)
    grad = Image.new("L", (1, h))
    for y in range(h):
        grad.putpixel((0, y), int(strength * (y / (h - 1)) ** 1.6))
    layer = Image.new("RGBA", (W, h), (0, 0, 0, 255))
    layer.putalpha(grad.resize((W, h)))
    img.alpha_composite(layer, (0, H - h))


# ---------------------------------------------------------------- poster A: split
def poster_split(photo_path, out_path, l1, l2, kicker, micro_l, micro_r,
                 photo_tags=(), split=0.54):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    draw = ImageDraw.Draw(img)

    ph = int(H * split)
    img.paste(cover(Image.open(photo_path).convert("RGB"), W, ph), (0, 0))

    # small annotations floating on the photograph — ink picked from local ground
    for tag, (tx, ty) in photo_tags:
        px, py = int(W * tx), int(ph * ty)
        ink = contrast_ink(img, (px, py, px + 300, py + 24))
        halo = (0, 0, 0, 165) if ink == (255, 255, 255) else (255, 255, 255, 165)
        micro_block(draw, (px, py), tag, size=17, fill=ink, max_w=300, tracking=1.2,
                    stroke=2, stroke_fill=halo)

    # accent square straddling the split line
    sq = 196
    sx, sy = W - MARGIN - sq, ph - int(sq * 0.55)
    draw.rectangle([sx, sy, sx + sq, sy + sq], fill=ORANGE)

    rule_y = H - 300

    # headline — capped so the two lines plus kicker always clear the hairline
    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    size = min(size, int((rule_y - 150 - ph) / 2.66))
    f = font(F_BOLD, size)
    tr = -0.02 * size
    y = ph + int(size * 0.62)
    for line in (l1, l2):
        track_text(draw, (MARGIN, y), line, f, INK, tr)
        y += int(size * 1.02)

    # kicker, right-aligned under the headline, never past the hairline
    ksize = int(size * 0.20)
    fk = font(F_BOLD, ksize)
    ky = min(y + int(size * 0.10), rule_y - ksize - 26)
    track_text(draw, (W - MARGIN, ky), kicker, fk, INK, int(ksize * 0.10),
               anchor_right=True)

    # hairline + micro-copy row
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=(200, 197, 191), width=2)
    micro_block(draw, (MARGIN, rule_y + 34), micro_l, max_w=470)
    micro_block(draw, (W - MARGIN, rule_y + 34), micro_r, max_w=470, right=True)

    lw = 150
    paste_logo(img, lw, ((W - lw) // 2, H - 150))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  {W}x{H}  headline={size}px")


# ---------------------------------------------------------------- poster B: accent disc
def poster_disc(photo_path, out_path, frag1, frag2, body, foot_l, foot_r):
    img = Image.new("RGBA", (W, H), (10, 10, 10, 255))
    img.paste(cover(Image.open(photo_path).convert("RGB"), W, H), (0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy, r = W // 2, int(H * 0.40), 330
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE)

    lw = 168
    lh = paste_logo(img, lw, (cx - lw // 2, cy - 176))

    fb = font(F_BOLD, 25)
    y = cy - 176 + lh + 42
    for frag in (frag1, frag2):
        w_ = track_width(draw, frag, fb, 2.0)
        track_text(draw, (cx - w_ / 2, y), frag, fb, INK, 2.0)
        y += 40

    fbody = font(F_BOLD, 17)
    y += 22
    for line in wrap(draw, body.upper(), fbody, int(r * 1.25), 1.0):
        w_ = track_width(draw, line, fbody, 1.0)
        track_text(draw, (cx - w_ / 2, y), line, fbody, INK, 1.0)
        y += 27

    scrim_bottom(img, height_frac=0.26, strength=185)
    draw = ImageDraw.Draw(img)
    micro_block(draw, (MARGIN, H - 300), foot_l, size=19,
                fill=(255, 255, 255), max_w=460)
    micro_block(draw, (W - MARGIN, H - 300), foot_r, size=19,
                fill=(255, 255, 255), max_w=460, right=True)

    lw2 = 132
    paste_logo(img, lw2, ((W - lw2) // 2, H - 148), white=True)
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  {W}x{H}  disc r={r}px")


if __name__ == "__main__":
    RAW = paths.RAW + os.sep
    OUT = paths.FINAL + os.sep

    poster_split(
        RAW + "10-figure-bw.png", OUT + "10-no-noise.jpg",
        "NO NOISE.", "JUST SIGNAL.", "ON PURPOSE.",
        "We build the brand, the content and the systems that make attention "
        "turn into revenue. Nothing decorative.",
        "Independent. Selective. Accountable to the number, not the applause.",
        photo_tags=(("Enough strategy.", (0.06, 0.62)),
                    ("Enough craft.", (0.62, 0.30))),
    )

    poster_disc(
        RAW + "11-ink-bw.png", OUT + "11-no-guesswork.jpg",
        "[ NO GUESSWORK ]", "[ ONLY OUTCOMES ]",
        "Every decision traced to a number. Every asset earning its place.",
        "Where the idea meets the market.",
        "Strategy. Content. Systems.",
    )
