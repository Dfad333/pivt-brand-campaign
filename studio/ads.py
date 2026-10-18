"""PivtMedia paid-social ad creatives — the ad counterpart to the poster layouts.

Different job from a poster: an ad has to stop the thumb in one second, make one point and
ask for one action. So every ad here carries the same frame:

    micro row (Mono)  ->  hook (Archivo Black)  ->  argument  ->  CTA block  ->  logo

Built straight to the Brand Guidelines V01: Archivo Black caps for the hook (-3%, leading 0.9),
Archivo Regular body, JetBrains Mono labels, Paper / Ink / one Signal orange.

Each concept renders in both formats from one function, so a test set is always matched:

    feed   1080 x 1350  (4:5)
    story  1080 x 1920  (9:16) — everything kept inside the 14% top / 20% bottom safe zone

Everything is drawn at 2x and downsampled, which keeps the type edges clean.

    python ads.py            # renders every concept in both formats into ../final/ads/
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

import paths

PAPER = (247, 245, 241)
INK = (18, 18, 18)
SIGNAL = (255, 92, 0)
INK_60 = (110, 109, 107)
INK_20 = (201, 200, 196)

SCALE = 2
FORMATS = {"feed": (1080, 1350), "story": (1080, 1920),
           "square": (1080, 1080), "landscape": (1920, 1080)}
SAFE = {"feed": (0.0, 0.0), "story": (0.14, 0.20),       # top / bottom safe-zone fractions
        "square": (0.0, 0.0), "landscape": (0.0, 0.0)}

OUT_DIR = os.path.join(paths.FINAL, "ads")


# ── type helpers ────────────────────────────────────────────────────────────

def F(path, size):
    return ImageFont.truetype(path, int(size))


def text_w(draw, text, f, tr=0.0):
    return sum(draw.textlength(c, font=f) for c in text) + tr * max(0, len(text) - 1)


def put(draw, x, y, text, f, fill, tr=0.0, right=False):
    """Draw tracked text with its top at the CAP height `y` (not the ascender)."""
    cap_off = f.getbbox("H")[1]
    if right:
        x -= text_w(draw, text, f, tr)
    for c in text:
        draw.text((x, y - cap_off), c, font=f, fill=fill)
        x += draw.textlength(c, font=f) + tr
    return x


def cap_h(f):
    b = f.getbbox("H")
    return b[3] - b[1]


def wrap(draw, text, f, max_w, tr=0.0):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f, tr) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])


def fit(draw, lines, path, max_w, tr_ratio=-0.03, hi=900):
    size = hi
    while size > 20:
        f = F(path, size)
        if max(text_w(draw, l, f, tr_ratio * size) for l in lines) <= max_w:
            return size
        size -= 4
    return size


def logo(img, w, x, y, white=False):
    src = os.path.join(paths.LOGO_DIR, "pivt-logo-transparent-white.png" if white
                       else "pivt-logo-transparent-black.png")
    lg = Image.open(src).convert("RGBA")
    lg = lg.resize((int(w), int(w * lg.height / lg.width)), Image.LANCZOS)
    img.alpha_composite(lg, (int(x), int(y)))
    return lg.height


def grease(draw, pts, width, color=SIGNAL, seed=0, wobble=None):
    """A grease-pencil stroke: jittered, slightly uneven, never a clean vector line."""
    rnd = random.Random(seed)
    wobble = width * 0.35 if wobble is None else wobble
    dense = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / (width * 1.2)))
        for i in range(n):
            t = i / n
            dense.append((x0 + (x1 - x0) * t + rnd.uniform(-wobble, wobble),
                          y0 + (y1 - y0) * t + rnd.uniform(-wobble, wobble)))
    dense.append(pts[-1])
    for (x0, y0), (x1, y1) in zip(dense, dense[1:]):
        w = int(width * rnd.uniform(0.82, 1.08))
        draw.line([(x0, y0), (x1, y1)], fill=color, width=w)
        r = w // 2
        draw.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=color)


def loop(cx, cy, rx, ry, turns=1.12, start=-2.6, n=60):
    """Points for a hand-drawn oval that overshoots its start, like a real circled word."""
    return [(cx + rx * math.cos(start + 2 * math.pi * turns * i / n) * (1 + 0.04 * i / n),
             cy + ry * math.sin(start + 2 * math.pi * turns * i / n)) for i in range(n + 1)]


# ── shared frame ────────────────────────────────────────────────────────────

class Frame:
    """Canvas + the furniture every ad shares: micro row, CTA, hairline, logo."""

    def __init__(self, fmt, ground=PAPER):
        w, h = FORMATS[fmt]
        self.fmt, self.W, self.H = fmt, w * SCALE, h * SCALE
        self.M = int(min(self.W, self.H) * 0.074)
        self.dark = ground == INK
        self.ink = PAPER if self.dark else INK          # type colour that reads on this ground
        st, sb = SAFE[fmt]
        self.top = max(self.M, int(self.H * st))
        self.bottom = self.H - max(self.M, int(self.H * sb))
        self.img = Image.new("RGBA", (self.W, self.H), ground + (255,))
        self.d = ImageDraw.Draw(self.img)
        self.mono = F(paths.F_MONO, 15 * SCALE)
        self.mono_b = F(paths.F_MONO_BOLD, 17 * SCALE)
        self.body = F(paths.F_REG, 22 * SCALE)

    def micro_row(self, left, right):
        tr = 0.08 * self.mono.size
        put(self.d, self.M, self.top, left.upper(), self.mono, self.ink, tr)
        put(self.d, self.W - self.M, self.top, right.upper(), self.mono, self.ink, tr, right=True)
        y = self.top + cap_h(self.mono) + 16 * SCALE
        self.d.line([(self.M, y), (self.W - self.M, y)], fill=self.ink, width=SCALE)
        return y

    def foot(self):
        """Hairline + logo at the bottom of the safe area. Returns the hairline y."""
        lw = int(min(self.W, self.H) * 0.13 * 1.25)   # 13% reads small on a phone; ads run larger
        with Image.open(os.path.join(paths.LOGO_DIR, "pivt-logo-transparent-black.png")) as lg:
            lh = int(lw * lg.height / lg.width)
        ly = self.bottom - lh
        logo(self.img, lw, (self.W - lw) / 2, ly, white=self.dark)
        hy = ly - 34 * SCALE
        self.d.line([(self.M, hy), (self.W - self.M, hy)], fill=self.ink, width=SCALE)
        return hy

    def body_text(self, y, text, max_w=None, fill=None, x=None, center=False):
        max_w = max_w or int((self.W - 2 * self.M) * 0.78)
        fill = fill or self.ink
        x = self.M if x is None else x
        lead = int(self.body.size * 1.42)
        for line in wrap(self.d, text, self.body, max_w):
            lx = (self.W - text_w(self.d, line, self.body)) / 2 if center else x
            put(self.d, lx, y, line, self.body, fill)
            y += lead
        return y - lead + cap_h(self.body)

    def cta(self, y, label, x=None, center=False):
        """Solid block with a Mono label — the one thing to press. Inverts on an Ink ground."""
        t = f"[ {label.upper()} ]  \u2192"
        tr = 0.06 * self.mono_b.size
        pad_x, pad_y = 30 * SCALE, 22 * SCALE
        tw = text_w(self.d, t, self.mono_b, tr)
        ch = cap_h(self.mono_b)
        bw = tw + 2 * pad_x
        x = (self.W - bw) / 2 if center else (self.M if x is None else x)
        self.d.rectangle([x, y, x + bw, y + ch + 2 * pad_y], fill=self.ink)
        put(self.d, x + pad_x, y + pad_y, t, self.mono_b, INK if self.dark else PAPER, tr)
        return y + ch + 2 * pad_y

    def save(self, name):
        os.makedirs(OUT_DIR, exist_ok=True)
        out = os.path.join(OUT_DIR, f"{name}-{self.fmt}.jpg")
        w, h = FORMATS[self.fmt]
        self.img.convert("RGB").resize((w, h), Image.LANCZOS).save(out, quality=95)
        print(f"{os.path.relpath(out, paths.ROOT)}  {w}x{h}")
        return out


# ── concept 01 — "You stopped." ─────────────────────────────────────────────

def ad_stopped(name, fmt, big=("YOU", "STOPPED"), kicker="THAT'S THE JOB.",
               body="This ad had 3 seconds to earn your attention. So does every ad you run. "
                    "We make them count.",
               cta="Book a call", micro=("[ Sponsored, obviously ]", "PivtMedia — Columbus, OH")):
    """The ad that admits it is an ad. Huge hook, the full stop is the Signal shape."""
    fr = Frame(fmt)
    d, W, M = fr.d, fr.W, fr.M
    y0 = fr.micro_row(*micro)
    foot_y = fr.foot()

    # hook — leave room on the last line for the square full stop
    size = fit(d, [big[0], big[-1] + "  "], paths.F_BLACK, W - 2 * M)
    fb = F(paths.F_BLACK, size)
    tr, ch, lead = -0.03 * size, cap_h(fb), int(size * 0.9)
    fk = F(paths.F_BLACK, size * 0.30)

    # measure the stack, then centre it in the space between micro row and foot
    body_lines = wrap(d, body, fr.body, int((W - 2 * M) * 0.78))
    stack = (ch + lead * (len(big) - 1) + int(size * 0.20) + cap_h(fk) + 70 * SCALE
             + int(fr.body.size * 1.42) * (len(body_lines) - 1) + cap_h(fr.body)
             + 56 * SCALE + cap_h(fr.mono_b) + 44 * SCALE)
    y = y0 + max(60 * SCALE, (foot_y - y0 - stack) // 2)

    for i, line in enumerate(big):
        x_end = put(d, M, y, line, fb, INK, tr)
        if i == len(big) - 1:
            sq = int(size * 0.17)
            d.rectangle([x_end + size * 0.04, y + ch - sq, x_end + size * 0.04 + sq, y + ch],
                        fill=SIGNAL)
        if i < len(big) - 1:
            y += lead
    y += ch + int(size * 0.20)
    put(d, M + 4 * SCALE, y, kicker, fk, INK, 0)
    y += cap_h(fk) + 70 * SCALE
    y = fr.body_text(y, body)
    fr.cta(y + 56 * SCALE, cta)
    return fr.save(name)


# ── concept 02 — "We'd cut this." ───────────────────────────────────────────

def ad_cut(name, fmt, hook="WE'D CUT THIS.",
           body="Most ads say everything and land nothing. We cut until only the point is "
                "left.",
           cta="Book a call", micro=("[ Brief — mark-up ]", "PivtMedia — Columbus, OH")):
    """A deliberately bland ad, marked up in grease pencil. Taste shown, not claimed."""
    fr = Frame(fmt)
    d, W, H, M = fr.d, fr.W, fr.H, fr.M
    y0 = fr.micro_row(*micro)
    foot_y = fr.foot()

    size = fit(d, [hook], paths.F_BLACK, W - 2 * M)
    fh = F(paths.F_BLACK, size)
    ch = cap_h(fh)

    # vertical budget: hook, card, body, CTA — card takes whatever is left
    body_lines = wrap(d, body, fr.body, W - 2 * M)
    body_h = int(fr.body.size * 1.42) * (len(body_lines) - 1) + cap_h(fr.body)
    tail = 56 * SCALE + body_h + 48 * SCALE + cap_h(fr.mono_b) + 44 * SCALE + 64 * SCALE
    hy = y0 + 56 * SCALE
    put(d, M, hy, hook, fh, INK, -0.03 * size)
    cy0 = hy + ch + 64 * SCALE
    cy1 = min(foot_y - tail, cy0 + int((W - 2 * M) * 1.0))

    # the bland ad — someone else's typical post, set in a generic system face on purpose
    cx0, cx1 = M, M + int((W - 2 * M) * 0.64)
    cw = cx1 - cx0
    d.rectangle([cx0 + 10 * SCALE, cy0 + 12 * SCALE, cx1 + 10 * SCALE, cy1 + 12 * SCALE],
                fill=(226, 223, 218))                       # soft offset shadow, paper-on-paper
    d.rectangle([cx0, cy0, cx1, cy1], fill=(255, 255, 255))
    pad = int(cw * 0.07)
    ix0, iy0, ix1 = cx0 + pad, cy0 + pad, cx1 - pad
    iy1 = iy0 + int((cy1 - cy0) * 0.42)
    d.rectangle([ix0, iy0, ix1, iy1], fill=(214, 214, 214))
    # stock-photo placeholder: sun + mountains
    mw, mh = ix1 - ix0, iy1 - iy0
    d.ellipse([ix0 + mw * 0.66, iy0 + mh * 0.16, ix0 + mw * 0.80, iy0 + mh * 0.16 + mw * 0.14],
              fill=(240, 240, 240))
    d.polygon([(ix0, iy1), (ix0 + mw * 0.34, iy0 + mh * 0.38), (ix0 + mw * 0.58, iy1)],
              fill=(178, 178, 178))
    d.polygon([(ix0 + mw * 0.36, iy1), (ix0 + mw * 0.66, iy0 + mh * 0.52), (ix1, iy1)],
              fill=(160, 160, 160))

    gen_b, gen_r = paths.pick_font(
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf", r"C:\Windows\Fonts\arialbd.ttf",
        paths.F_BOLD), paths.pick_font(
        "/System/Library/Fonts/Supplemental/Arial.ttf", r"C:\Windows\Fonts\arial.ttf",
        paths.F_REG)
    ty = iy1 + int(pad * 0.9)
    fgh = F(gen_b, cw * 0.064)
    head_lines = ["Unlock your brand's", "full potential!!"]
    head_box = []
    for ln in head_lines:
        x_end = put(d, ix0, ty, ln, fgh, (40, 40, 40))
        head_box.append((ix0, ty, x_end, ty + cap_h(fgh)))
        ty += int(fgh.size * 1.22)
    fgr = F(gen_r, cw * 0.036)
    ty += int(pad * 0.25)
    sub_box = None
    for ln in ["Innovative, cutting-edge solutions", "that elevate your business."]:
        x_end = put(d, ix0, ty, ln, fgr, (110, 110, 110))
        sub_box = (ix0, sub_box[1] if sub_box else ty, max(x_end, sub_box[2] if sub_box else 0),
                   ty + cap_h(fgr))
        ty += int(fgr.size * 1.5)
    ty += int(pad * 0.35)
    fbt = F(gen_b, cw * 0.034)
    bt = "CLICK HERE TO LEARN MORE"
    bw = text_w(d, bt, fbt) + pad
    bh = cap_h(fbt) + int(pad * 0.7)
    btn = (ix0, ty, ix0 + bw, ty + bh)
    if btn[3] < cy1 - pad * 0.4:
        d.rounded_rectangle(btn, radius=bh // 2, fill=(150, 150, 150))
        put(d, ix0 + pad / 2, ty + pad * 0.35, bt, fbt, (255, 255, 255))
    else:
        btn = None

    # mark-up: strike the headline, cross the stock image, circle the button
    stroke = 7 * SCALE
    for i, (x0, y0_, x1, y1_) in enumerate(head_box):
        mid = (y0_ + y1_) / 2
        grease(d, [(x0 - 12 * SCALE, mid + 6 * SCALE), (x1 + 14 * SCALE, mid - 4 * SCALE)],
               stroke, seed=11 + i)
    grease(d, [(ix0 + mw * 0.08, iy0 + mh * 0.12), (ix1 - mw * 0.08, iy1 - mh * 0.12)],
           stroke, seed=21)
    grease(d, [(ix1 - mw * 0.08, iy0 + mh * 0.12), (ix0 + mw * 0.08, iy1 - mh * 0.12)],
           stroke, seed=22)
    if btn:
        bx, by = (btn[0] + btn[2]) / 2, (btn[1] + btn[3]) / 2
        grease(d, loop(bx, by, (btn[2] - btn[0]) * 0.62, (btn[3] - btn[1]) * 1.05), stroke,
               seed=31, wobble=stroke * 0.25)

    # notes column — Ink Mono, joined to each mark by an orange leader
    nx = cx1 + 44 * SCALE
    fn = F(paths.F_MONO_BOLD, 15 * SCALE)
    ntr = 0.06 * fn.size
    notes = [(((iy0 + iy1) / 2), "STOCK.", ix1 - mw * 0.06),
             ((head_box[0][1] + head_box[-1][3]) / 2, "SAYS NOTHING.", head_box[0][2] + 20 * SCALE),
             ((btn[1] + btn[3]) / 2 if btn else (sub_box[1] + sub_box[3]) / 2,
              "WHO IS THIS FOR?", (btn[2] + (btn[2] - btn[0]) * 0.14) if btn else sub_box[2])]
    for k, (ny, label, ax) in enumerate(notes):
        lines = wrap(d, label, fn, W - M - nx - 30 * SCALE, ntr)
        block = cap_h(fn) + (len(lines) - 1) * int(fn.size * 1.5)
        top = ny - block / 2
        grease(d, [(ax, ny), (nx - 16 * SCALE, ny)], 3 * SCALE, seed=40 + k,
               wobble=0.4 * SCALE)
        for j, ln in enumerate(lines):
            put(d, nx, top + j * int(fn.size * 1.5), ln, fn, INK, ntr)

    y = cy1 + 12 * SCALE + 56 * SCALE
    y = fr.body_text(y, body, max_w=W - 2 * M)
    fr.cta(y + 48 * SCALE, cta)
    return fr.save(name)


# ── concept 03 — "Just signal." · 4:5 feed ─────────────────────────────────

NOISE_WORDS = ["UNLOCK", "ELEVATE", "SYNERGY", "LEVERAGE", "GAME-CHANGER", "BEST-IN-CLASS",
               "GO VIRAL", "GUARANTEED", "INNOVATIVE", "CUTTING-EDGE", "NEXT LEVEL",
               "DISRUPT", "WORLD-CLASS", "SEAMLESS", "HOLISTIC", "SUPERCHARGE"]


def ad_signal(name, fmt="feed", hook=("JUST", "SIGNAL"),
              body="Everyone else is using the same words. Say one thing clearly and it is the "
                   "only thing they hear.",
              cta="Book a call", micro=("[ No noise ]", "PivtMedia — Columbus, OH")):
    """The brand line made visible: a wall of filler words, one clear line on top of it."""
    fr = Frame(fmt)
    d, W, M = fr.d, fr.W, fr.M
    y0 = fr.micro_row(*micro)
    foot_y = fr.foot()

    body_lines = wrap(d, body, fr.body, int((W - 2 * M) * 0.80))
    tail = (64 * SCALE + int(fr.body.size * 1.42) * (len(body_lines) - 1) + cap_h(fr.body)
            + 52 * SCALE + cap_h(fr.mono_b) + 44 * SCALE + 56 * SCALE)
    z0, z1 = y0 + 40 * SCALE, foot_y - tail          # the noise field

    # the signal: one line, set in Ink in a clear band at the centre of the field
    size = fit(d, [hook[-1] + "  "], paths.F_BLACK, W - 2 * M)
    fb = F(paths.F_BLACK, size)
    ch, lead2 = cap_h(fb), int(size * 0.9)
    stack = ch + lead2 * (len(hook) - 1)
    hy = z0 + (z1 - z0 - stack) // 2
    pad = int(size * 0.16)
    clear0, clear1 = hy - pad, hy + stack + pad

    # the noise: the brand guidelines' banned words, a pale wall of type around it.
    # Whole rows only: a row sliced by the clear band reads as a glitch, not a choice.
    fn = F(paths.F_BLACK, 50 * SCALE)
    lead = int(fn.size * 1.04)
    rnd = random.Random(7)
    y, row = z0, 0
    while y + cap_h(fn) <= z1:
        if y + cap_h(fn) < clear0 or y > clear1:
            words = NOISE_WORDS[row % 4:] + NOISE_WORDS[:row % 4]
            x = -rnd.randint(0, 260) * SCALE
            layer = Image.new("RGBA", (W - 2 * M, cap_h(fn) + 4 * SCALE), (0, 0, 0, 0))
            put(ImageDraw.Draw(layer), x, 0, "  ".join(words * 2), fn, (226, 224, 220),
                -0.01 * fn.size)
            fr.img.alpha_composite(layer, (M, int(y)))
            row += 1
        y += lead

    for i, line in enumerate(hook):
        x_end = put(d, M, hy + i * lead2, line, fb, INK, -0.03 * size)
    sq = int(size * 0.17)
    by = hy + (len(hook) - 1) * lead2 + ch
    d.rectangle([x_end + size * 0.04, by - sq, x_end + size * 0.04 + sq, by], fill=SIGNAL)

    y = z1 + 64 * SCALE
    y = fr.body_text(y, body, max_w=int((W - 2 * M) * 0.80))
    fr.cta(y + 52 * SCALE, cta)
    return fr.save(name)


# ── concept 04 — "You paid for noise." · 1:1 square ────────────────────────

def ad_receipt(name, fmt="square", hook=("YOU", "PAID", "FOR", "NOISE."),
               rows=(("Boosted post", "Done"), ("Stock photo", "Done"),
                     ("Caption, 9 emoji", "Done"), ("30 hashtags", "Done"),
                     ("A reason to stop", "—")),
               total=("Attention", "NONE."), slip_foot="Thank you for scrolling past.",
               cta="Book a call", micro=("[ Itemised ]", "PivtMedia — Columbus, OH")):
    """A till slip for the average ad: everything ticked off except the one thing that matters."""
    fr = Frame(fmt, ground=INK)
    d, W, M = fr.d, fr.W, fr.M
    y0 = fr.micro_row(*micro)
    foot_y = fr.foot()

    # slip on the right
    sx0, sx1 = int(W * 0.50), W - M
    sw = sx1 - sx0
    pad = int(sw * 0.08)
    fr_lbl = F(paths.F_MONO, 15 * SCALE)
    fr_row = F(paths.F_MONO_BOLD, 16 * SCALE)
    ft = F(paths.F_BLACK, 40 * SCALE)
    row_gap = 42 * SCALE
    content = (cap_h(fr_lbl) + 34 * SCALE + len(rows) * row_gap + 30 * SCALE + cap_h(ft)
               + 46 * SCALE + cap_h(fr_lbl) + 20 * SCALE)
    sy0 = y0 + max(44 * SCALE, (foot_y - y0 - content - 2 * pad) // 2)
    sy1 = sy0 + content + 2 * pad
    d.rectangle([sx0, sy0, sx1, sy1], fill=PAPER)
    step = 18 * SCALE                                     # perforated bottom edge
    for x in range(sx0, sx1, step):
        d.ellipse([x, sy1 - step // 2, x + step, sy1 + step // 2], fill=INK)

    y = sy0 + pad
    put(d, sx0 + pad, y, "ORDER — THE AVERAGE AD", fr_lbl, INK, 0.08 * fr_lbl.size)
    y += cap_h(fr_lbl) + 18 * SCALE
    d.line([(sx0 + pad, y), (sx1 - pad, y)], fill=INK, width=SCALE)
    y += 16 * SCALE
    for label, val in rows:
        y += row_gap - cap_h(fr_row)
        put(d, sx0 + pad, y, label.upper(), fr_row, INK, 0.04 * fr_row.size)
        put(d, sx1 - pad, y, val.upper(), fr_row, INK, 0.04 * fr_row.size, right=True)
        dy = y + cap_h(fr_row) + 10 * SCALE
        for dx in range(sx0 + pad, sx1 - pad, 10 * SCALE):
            d.line([(dx, dy), (dx + 4 * SCALE, dy)], fill=INK_20, width=SCALE)
        y += cap_h(fr_row)
    y += 30 * SCALE
    put(d, sx0 + pad, y + (cap_h(ft) - cap_h(fr_row)), total[0].upper(), fr_row, INK,
        0.04 * fr_row.size)
    put(d, sx1 - pad, y, total[1], ft, SIGNAL, -0.02 * ft.size, right=True)
    y += cap_h(ft) + 46 * SCALE
    put(d, sx0 + pad, y, slip_foot.upper(), fr_lbl, INK_60, 0.06 * fr_lbl.size)

    # hook on the left, stacked
    col = sx0 - M - 56 * SCALE
    size = fit(d, list(hook), paths.F_BLACK, col)
    fb = F(paths.F_BLACK, size)
    ch, lead = cap_h(fb), int(size * 0.92)
    stack = ch + lead * (len(hook) - 1) + 56 * SCALE + cap_h(fr.mono_b) + 44 * SCALE
    y = sy0 + max(0, (sy1 - sy0 - stack) // 2)
    for i, line in enumerate(hook):
        put(d, M, y + i * lead, line, fb, PAPER, -0.03 * size)
    fr.cta(y + ch + lead * (len(hook) - 1) + 56 * SCALE, cta)
    return fr.save(name)


# ── concept 05 — "Brands done blending in." · 9:16 story ───────────────────

def ad_quiet(name, fmt="story", hook=("BRANDS", "DONE", "BLENDING IN."),
             body="Content, paid social and production for Columbus brands that refuse to get "
                  "scrolled past.",
             cta="Book a call", micro=("[ PivtMedia ]", "Social & content agency")):
    """The quiet register on Ink: thin, tracked, centered. Restraint as the thumb-stop."""
    fr = Frame(fmt, ground=INK)
    d, W, M = fr.d, fr.W, fr.M
    y0 = fr.micro_row(*micro)
    foot_y = fr.foot()

    tr_ratio = 0.24
    size = 120 * SCALE
    while size > 20 and max(text_w(d, l, F(paths.F_LIGHT, size), size * tr_ratio)
                            for l in hook) > (W - 2 * M) * 0.92:
        size -= 2
    fl = F(paths.F_LIGHT, size)
    ch, lead = cap_h(fl), int(size * 1.55)
    body_lines = wrap(d, body, fr.body, int((W - 2 * M) * 0.66))
    stack = (ch + lead * (len(hook) - 1) + 70 * SCALE + 4 * SCALE + 70 * SCALE
             + int(fr.body.size * 1.42) * (len(body_lines) - 1) + cap_h(fr.body)
             + 70 * SCALE + cap_h(fr.mono_b) + 44 * SCALE)
    y = y0 + (foot_y - y0 - stack) // 2
    for i, line in enumerate(hook):
        tw = text_w(d, line, fl, size * tr_ratio)
        put(d, (W - tw) / 2 + size * tr_ratio / 2, y + i * lead, line, fl, PAPER,
            size * tr_ratio)
    y += ch + lead * (len(hook) - 1) + 70 * SCALE
    d.rectangle([W / 2 - 36 * SCALE, y, W / 2 + 36 * SCALE, y + 4 * SCALE], fill=SIGNAL)
    y += 4 * SCALE + 70 * SCALE
    y = fr.body_text(y, body, max_w=int((W - 2 * M) * 0.66), center=True)
    fr.cta(y + 70 * SCALE, cta, center=True)
    return fr.save(name)


# ── concept 06 — "Every ad answers three questions." · 16:9 landscape ──────

def ad_three(name, fmt="landscape", hook=("EVERY AD", "ANSWERS", "THREE", "QUESTIONS"),
             items=(("Who is it for?", "Columbus businesses who want to be noticed."),
                    ("Why should they care?", "Because attention is the whole game now."),
                    ("What do they do next?", "Book a call. That is the whole ask.")),
             cta="Book a call", micro=("[ The brief, in three lines ]",
                                       "PivtMedia — Columbus, OH")):
    """Landscape index: big hook left, numbered answers right. The ad answers its own test."""
    fr = Frame(fmt)
    d, W, M = fr.d, fr.W, fr.M
    y0 = fr.micro_row(*micro)
    foot_y = fr.foot()

    split = int(W * 0.50)
    col = split - M - 80 * SCALE
    size = fit(d, list(hook[:-1]) + [hook[-1] + "  "], paths.F_BLACK, col)
    fb = F(paths.F_BLACK, size)
    ch, lead = cap_h(fb), int(size * 0.9)
    stack = ch + lead * (len(hook) - 1) + 60 * SCALE + cap_h(fr.mono_b) + 44 * SCALE
    y = y0 + (foot_y - y0 - stack) // 2
    for i, line in enumerate(hook):
        x_end = put(d, M, y + i * lead, line, fb, INK, -0.03 * size)
    sq = int(size * 0.17)
    by = y + (len(hook) - 1) * lead + ch
    d.rectangle([x_end + size * 0.04, by - sq, x_end + size * 0.04 + sq, by], fill=SIGNAL)
    fr.cta(by + 60 * SCALE, cta)

    # index rows on the right, hairline-divided
    fnum = F(paths.F_MONO_BOLD, 22 * SCALE)
    fq = F(paths.F_XBOLD, 40 * SCALE)
    fa = F(paths.F_REG, 22 * SCALE)
    row_h = (foot_y - y0 - 120 * SCALE) // len(items)
    ry = y0 + 60 * SCALE
    for i, (q, a) in enumerate(items, start=1):
        if i > 1:
            d.line([(split, ry), (W - M, ry)], fill=INK_20, width=SCALE)
        top = ry + (row_h - (cap_h(fq) + 26 * SCALE + cap_h(fa))) // 2
        put(d, split, top + (cap_h(fq) - cap_h(fnum)) // 2, f"0{i}", fnum, INK, 0.06 * fnum.size)
        put(d, split + 110 * SCALE, top, q, fq, INK, -0.02 * fq.size)
        put(d, split + 110 * SCALE, top + cap_h(fq) + 26 * SCALE, a, fa, INK_60)
        ry += row_h
    return fr.save(name)


CONCEPTS = {
    "ad01-you-stopped": (ad_stopped, ("feed", "story")),
    "ad02-wed-cut-this": (ad_cut, ("feed", "story")),
    "ad03-just-signal": (ad_signal, ("feed",)),
    "ad04-you-paid-for-noise": (ad_receipt, ("square",)),
    "ad05-blending-in": (ad_quiet, ("story",)),
    "ad06-three-questions": (ad_three, ("landscape",)),
}


if __name__ == "__main__":
    for name, (fn, fmts) in CONCEPTS.items():
        for fmt in fmts:
            fn(name, fmt)
