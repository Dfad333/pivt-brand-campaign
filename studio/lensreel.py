"""PivtMedia lens reel — objects rain into a flight case until the wordmark resolves.

Reference: a 13.1s top-down reel (one unbroken shot, cups filling a basket, brand mark
resolving out of the pile).

The reference's key trick, confirmed by inspecting its final frame: the mark is NOT
printed on the objects and then arranged by luck. It is PROJECTED onto the finished
pile from the camera's viewpoint — it wraps over curved surfaces, breaks across the
gaps between objects, and drops out inside shadowed crevices. So the simulation never
has to cooperate; it only has to build a convincing pile.

Placeholder lens art is drawn procedurally here. When Higgsfield reconnects, swap
make_lens() for the photoreal top-down plate — nothing else needs to change.

    python lensreel.py
"""
import math
import os
import random

import paths

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

MO = paths.MOTION
SEQ = os.path.join(MO, "lens-seq")
F_BOLD = paths.F_BOLD
ORANGE = (255, 92, 0)

W, H = 1080, 1920
FPS, SECS = 60, 8.5
N = int(FPS * SECS)

CASE = (30, 150, 1050, 1770)          # outer shell of the flight case
LIP = 46                              # foam interior inset

N_LENS = 64
D_MIN, D_MAX = 168, 264               # lens diameter range
T_HERO, T_RAIN0, T_RAIN1 = 0.15, 0.95, 5.15
T_FLIGHT = 0.50
T_LOGO0, T_LOGO1 = 6.00, 7.15         # wordmark resolve window


# ---------------------------------------------------------------- art

def make_lens(d, rng):
    """Top-down camera lens: knurled barrel, silver ring, coated front element."""
    S = 3
    D = d * S
    im = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    c = D / 2.0

    dr.ellipse([0, 0, D - 1, D - 1], fill=(191, 192, 196, 255))
    off = rng.uniform(0, math.tau)
    for i in range(76):                                   # knurled grip
        a = off + i * math.tau / 76
        dr.line([c + math.cos(a) * D * 0.470, c + math.sin(a) * D * 0.470,
                 c + math.cos(a) * D * 0.415, c + math.sin(a) * D * 0.415],
                fill=(150, 151, 156, 255), width=max(1, int(D * 0.013)))

    def ring(fr, col):
        r = D * fr / 2
        dr.ellipse([c - r, c - r, c + r, c + r], fill=col)

    ring(0.815, (166, 167, 172, 255))
    ring(0.755, (232, 233, 238, 255))                     # silver band
    ring(0.720, (34, 34, 38, 255))

    # coated front element, built in numpy for a clean radial falloff
    R = D * 0.545 / 2
    yy, xx = np.mgrid[0:D, 0:D].astype(np.float32)
    rr = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / R
    ang = np.arctan2(yy - c, xx - c)
    inside = rr <= 1.0

    t = np.clip(rr, 0, 1)[..., None]
    glass = (np.array([30, 27, 46], np.float32) * (1 - t)
             + np.array([8, 8, 14], np.float32) * t)

    warm = np.exp(-((rr - 0.66) ** 2) / 0.020) * np.clip(np.cos(ang - 2.35), 0, 1) ** 2
    cool = np.exp(-((rr - 0.80) ** 2) / 0.012) * np.clip(np.cos(ang + 0.85), 0, 1) ** 2
    glass += warm[..., None] * np.array([150, 62, 12], np.float32)
    glass += cool[..., None] * np.array([26, 70, 105], np.float32)

    el = np.zeros((D, D, 4), np.uint8)
    el[..., :3] = np.clip(glass, 0, 255).astype(np.uint8)
    el[..., 3] = (inside * 255).astype(np.uint8)
    im.alpha_composite(Image.fromarray(el, "RGBA"))

    spec = Image.new("RGBA", (D, D), (0, 0, 0, 0))        # specular highlight
    ImageDraw.Draw(spec).ellipse(
        [c - R * 0.62, c - R * 0.74, c - R * 0.06, c - R * 0.30],
        fill=(255, 255, 255, 62))
    im.alpha_composite(spec.filter(ImageFilter.GaussianBlur(D * 0.035)))

    im = im.resize((d, d), Image.LANCZOS)
    return im.rotate(rng.uniform(0, 360), resample=Image.BICUBIC)


def make_shadow(d):
    """Soft contact shadow so stacked lenses read as solid objects, not decals."""
    p = 24
    sh = Image.new("L", (d + p, d + p), 0)
    ImageDraw.Draw(sh).ellipse([p / 2, p / 2, d + p / 2, d + p / 2], fill=150)
    return sh.filter(ImageFilter.GaussianBlur(d * 0.055))


def make_case():
    """Black flight case, shot from directly overhead, foam interior."""
    x0, y0, x1, y1 = CASE
    base = np.zeros((H, W, 3), np.float32)
    base[:] = (9, 9, 10)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = 1.0 - 0.55 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    base *= np.clip(vig, 0.35, 1)[..., None]
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    dr = ImageDraw.Draw(im)

    dr.rounded_rectangle([x0, y0, x1, y1], 34, fill=(20, 20, 22))
    dr.rounded_rectangle([x0 + 8, y0 + 8, x1 - 8, y1 - 8], 28, outline=(46, 46, 50), width=3)

    ix0, iy0, ix1, iy1 = x0 + LIP, y0 + LIP, x1 - LIP, y1 - LIP
    noise = np.random.default_rng(7).normal(0, 5.2, (iy1 - iy0, ix1 - ix0, 1))
    foam = np.clip(np.array([34, 35, 37], np.float32) + noise, 0, 255).astype(np.uint8)
    foam = np.repeat(foam, 3, axis=2)
    im.paste(Image.fromarray(foam, "RGB").filter(ImageFilter.GaussianBlur(0.6)), (ix0, iy0))

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))          # interior wall shadow
    ImageDraw.Draw(sh).rounded_rectangle([ix0, iy0, ix1, iy1], 20,
                                         outline=(0, 0, 0, 165), width=26)
    im = Image.alpha_composite(im.convert("RGBA"),
                               sh.filter(ImageFilter.GaussianBlur(11))).convert("RGB")

    dr = ImageDraw.Draw(im)
    for cx in (x0 + 190, x1 - 190):                       # latches
        dr.rounded_rectangle([cx - 54, y0 - 5, cx + 54, y0 + 30], 7, fill=(96, 97, 102))
        dr.rounded_rectangle([cx - 54, y1 - 30, cx + 54, y1 + 5], 7, fill=(96, 97, 102))
    return im


# ---------------------------------------------------------------- layout

def layout(rng):
    """Farthest-point sampling so the pile covers the case with no bald patches."""
    ix0, iy0 = CASE[0] + LIP + 60, CASE[1] + LIP + 60
    ix1, iy1 = CASE[2] - LIP - 60, CASE[3] - LIP - 60
    pts = [((ix0 + ix1) / 2, (iy0 + iy1) / 2)]
    while len(pts) < N_LENS:
        best, bd = None, -1
        for _ in range(48):
            p = (rng.uniform(ix0, ix1), rng.uniform(iy0, iy1))
            d = min((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for q in pts)
            if d > bd:
                best, bd = p, d
        pts.append(best)

    out = []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            t = T_HERO
        else:
            u = (i - 1) / max(1, N_LENS - 2)
            t = T_RAIN0 + u * (T_RAIN1 - T_RAIN0) + rng.uniform(-0.06, 0.06)
        out.append(dict(x=x, y=y, d=int(rng.uniform(D_MIN, D_MAX)), t=max(0.0, t),
                        dx=rng.uniform(-26, 26), dy=rng.uniform(-34, 34)))
    return out


def ease(u):
    """Ease-out with a small settle overshoot."""
    if u >= 1:
        return 1.0
    if u > 0.55:
        return 1 - (1 - u) ** 3 * math.cos(u * 7.5)
    return 1 - (1 - u) ** 3


# ---------------------------------------------------------------- wordmark

def wordmark_alpha():
    """PIVT / MEDIA stacked and centred in the case.

    Nine tracked letters on one line get shredded by the pile -- the reference used a
    compact chunky glyph for exactly this reason. Two big lines survive the breakup.
    """
    iw = (CASE[2] - CASE[0]) - 2 * LIP
    target = int(iw * 0.90)
    lines = ("PIVT", "MEDIA")

    def fit(txt):
        size = 10
        for sz in range(10, 700):
            f = ImageFont.truetype(F_BOLD, sz)
            if sum(f.getlength(ch) for ch in txt) > target:
                break
            size = sz
        return ImageFont.truetype(F_BOLD, size), size

    lay = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(lay)
    cy = (CASE[1] + CASE[3]) / 2
    caps = []
    for i, txt in enumerate(lines):
        f, size = fit(txt)
        caps.append(size)
        y = cy + (i - 0.5) * size * 1.02
        dr.text((W / 2, y), txt, font=f, fill=255, anchor="mm")
    return np.asarray(lay, np.float32) / 255.0, max(caps)


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def project(frame, mask, fade):
    """Composite the mark as if projected onto the pile from the camera."""
    arr = np.asarray(frame, np.float32)
    lum = arr @ np.array([0.299, 0.587, 0.114], np.float32)

    vis = 0.30 + 0.70 * smoothstep(52, 132, lum)                      # dies in crevices/shadow
    shade = 0.36 + 0.64 * np.clip(lum / 205.0, 0, 1)   # wraps over form
    a = (mask * fade * vis)[..., None]
    tint = np.array(ORANGE, np.float32) * shade[..., None]
    return Image.fromarray(np.clip(arr * (1 - a) + tint * a, 0, 255).astype(np.uint8), "RGB")


# ---------------------------------------------------------------- render

def main():
    os.makedirs(SEQ, exist_ok=True)
    rng = random.Random(11)
    case = make_case()
    items = layout(rng)
    for it in items:
        it["spr"] = make_lens(it["d"], rng)
        it["shd"] = make_shadow(it["d"])
    mask, cap = wordmark_alpha()
    print("case built | %d lenses | wordmark cap height %dpx" % (len(items), cap))

    for i in range(N):
        t = i / FPS
        fr = case.copy()
        for it in items:
            if t < it["t"]:
                continue
            u = min(1.0, (t - it["t"]) / T_FLIGHT)
            e = ease(u)
            sc = 1.55 - 0.55 * e                       # falls away from the camera
            x = it["x"] + it["dx"] * (1 - e)
            y = it["y"] + it["dy"] * (1 - e)
            d = max(8, int(it["d"] * sc))
            spr = it["spr"] if u >= 1 else it["spr"].resize((d, d), Image.BILINEAR)
            if u < 0.5:                                # motion smear while fast
                spr = spr.copy()
                spr.putalpha(spr.getchannel("A").point(
                    lambda v: int(v * (0.55 + 0.9 * u))))
            sd = it["shd"] if u >= 1 else it["shd"].resize(
                (spr.width + 24, spr.height + 24), Image.BILINEAR)
            fr.paste((0, 0, 0), (int(x - sd.width / 2 + 7), int(y - sd.height / 2 + 11)), sd)
            fr.paste(spr, (int(x - spr.width / 2), int(y - spr.height / 2)), spr)

        if t >= T_LOGO0:
            fade = float(smoothstep(T_LOGO0, T_LOGO1, np.float32(t)))
            fr = project(fr, mask, fade)

        fr.save(os.path.join(SEQ, "f%04d.png" % i))
        if i % 90 == 0:
            print("  frame %d/%d  t=%.2fs" % (i, N, t))

    print("rendered %d frames %dx%d @%dfps" % (N, W, H, FPS))


if __name__ == "__main__":
    main()
