"""Instagram story highlights — covers plus the stories that live inside each one.

Covers use the brand guidelines' progress barcode: the full lockup barcode with the orange
signal bar moved along it, one step per highlight, so the row of circles on the profile reads
left to right like the guidelines' own page rail. This is the *progress device*, not the logo
mark — the mark's signal bar never moves (Brand Guidelines V01, Mark & versions).

Inside stories reuse the ad frame from ads.py (micro row, Archivo Black, Mono, v2 logo) at
9:16, everything inside the 14% top / 20% bottom safe zone. Paper frames carry the content;
each highlight ends on an Ink frame with the one action.

    python highlights.py     # renders into ../final/highlights/ (local only)
"""
import os

from PIL import Image, ImageDraw

import paths
from ads import (Frame, F, put, cap_h, text_w, wrap, fit, PAPER, INK, SIGNAL, INK_60, INK_20,
                 SCALE)

OUT_DIR = os.path.join(paths.FINAL, "highlights")

# master lockup barcode [x, width, height] in its 396×120 space (from brand-guidelines/guidelines.js)
PIVT_BARS = [[0, 12, 120], [16, 4, 120], [28, 16, 120], [48, 8, 82], [60, 4, 120], [76, 4, 120],
             [88, 4, 120], [96, 16, 120], [120, 4, 120], [128, 12, 120], [144, 8, 120],
             [156, 4, 120], [168, 4, 120], [184, 8, 120], [196, 4, 120], [216, 4, 120],
             [224, 8, 120], [236, 4, 120], [252, 8, 120], [264, 4, 120], [276, 16, 120],
             [296, 4, 82], [308, 4, 120], [324, 4, 120], [332, 8, 120], [344, 4, 120],
             [364, 4, 120], [376, 4, 120], [392, 4, 120]]


def progress_bars(draw, x, y, w, step, steps, ink, signal_w=12, ground=INK):
    """The guidelines' progress barcode, signal on bar `step` of `steps`, scaled to width w.

    The signal bar is widened to `signal_w` units (as the guidelines' chapter barcodes do) so
    it still reads at avatar size; it is drawn last, over its neighbours.
    """
    s = w / 396
    pos = round((step + 0.5) / steps * (len(PIVT_BARS) - 1))
    for k, (bx, bw, bh) in enumerate(PIVT_BARS):
        if k != pos:
            draw.rectangle([x + bx * s, y, x + (bx + bw) * s - 1, y + bh * s], fill=ink)
    bx, bw, bh = PIVT_BARS[pos]
    cx = bx + bw / 2
    draw.rectangle([x + (cx - signal_w / 2 - 3) * s, y, x + (cx + signal_w / 2 + 3) * s,
                    y + bh * s], fill=ground)          # clear a gap so the signal stands alone
    draw.rectangle([x + (cx - signal_w / 2) * s, y, x + (cx + signal_w / 2) * s, y + bh * s],
                   fill=SIGNAL)
    return 120 * s


def save(fr, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f"{name}.jpg")
    fr.img.convert("RGB").resize((fr.W // SCALE, fr.H // SCALE), Image.LANCZOS).save(
        out, quality=95)
    print(os.path.relpath(out, paths.ROOT))


# ── covers ──────────────────────────────────────────────────────────────────

def cover(name, step, steps):
    """Ink ground, progress barcode centred inside the circle Instagram crops to."""
    fr = Frame("story", ground=INK)
    d, W, H = fr.d, fr.W, fr.H
    bw = int(W * 0.66)
    bh = progress_bars(d, (W - bw) / 2, 0, bw, step, steps, INK)    # measure only
    d.rectangle([0, 0, W, H], fill=INK)
    fn = F(paths.F_MONO_BOLD, 76 * SCALE)
    label = f"0{step + 1}"
    gap = 56 * SCALE
    top = (H - (bh + gap + cap_h(fn))) / 2
    progress_bars(d, (W - bw) / 2, top, bw, step, steps, PAPER)
    put(d, (W - text_w(d, label, fn, 0.1 * fn.size)) / 2, top + bh + gap, label, fn, PAPER,
        0.1 * fn.size)
    save(fr, name)


# ── inside-story frames ─────────────────────────────────────────────────────

def _chrome(fr, section, page, pages):
    y0 = fr.micro_row(f"[ {section} ]", f"{page:02d} / {pages:02d}")
    return y0, fr.foot()


def story_hook(name, section, page, pages, lines, body=None, ground=PAPER, cta=None,
               note=None):
    """Big Archivo Black stack, square orange full stop, optional body / CTA / note."""
    fr = Frame("story", ground=ground)
    d, W, M = fr.d, fr.W, fr.M
    y0, foot_y = _chrome(fr, section, page, pages)
    ink = fr.ink

    clean = [l.rstrip(".") for l in lines]
    size = fit(d, clean[:-1] + [clean[-1] + "  "], paths.F_BLACK, W - 2 * M, hi=420 * SCALE)
    fb = F(paths.F_BLACK, size)
    ch, lead = cap_h(fb), int(size * 0.92)
    body_lines = wrap(d, body, fr.body, int((W - 2 * M) * 0.86)) if body else []
    stack = ch + lead * (len(lines) - 1)
    if body_lines:
        stack += 64 * SCALE + int(fr.body.size * 1.42) * (len(body_lines) - 1) + cap_h(fr.body)
    if cta:
        stack += 60 * SCALE + cap_h(fr.mono_b) + 44 * SCALE
    if note:
        stack += 40 * SCALE + cap_h(fr.mono)
    y = y0 + (foot_y - y0 - stack) // 2

    for i, line in enumerate(lines):
        last = i == len(lines) - 1
        x_end = put(d, M, y + i * lead, clean[i] if last else line, fb, ink, -0.03 * size)
        if last and line.endswith("."):
            sq = int(size * 0.17)
            by = y + i * lead + ch
            d.rectangle([x_end + size * 0.04, by - sq, x_end + size * 0.04 + sq, by],
                        fill=SIGNAL)
    y += ch + lead * (len(lines) - 1)
    if body_lines:
        y = fr.body_text(y + 64 * SCALE, body, max_w=int((W - 2 * M) * 0.86))
    if cta:
        y = fr.cta(y + 60 * SCALE, cta)
    if note:
        put(d, M, y + 40 * SCALE, note.upper(), fr.mono, ink, 0.08 * fr.mono.size)
    save(fr, name)


def story_index(name, section, page, pages, title, items, foot_note=None):
    """Numbered list, hairline-divided: Mono numeral, ExtraBold name, one plain line each."""
    fr = Frame("story")
    d, W, M = fr.d, fr.W, fr.M
    y0, foot_y = _chrome(fr, section, page, pages)

    ft = F(paths.F_BLACK, fit(d, [title.rstrip(".") + "  "], paths.F_BLACK, W - 2 * M,
                              hi=160 * SCALE))
    fnum = F(paths.F_MONO_BOLD, 18 * SCALE)
    fname = F(paths.F_XBOLD, 38 * SCALE)
    fdesc = F(paths.F_REG, 21 * SCALE)
    indent = 96 * SCALE
    desc_w = W - 2 * M - indent

    blocks = [wrap(d, desc, fdesc, desc_w) for _, desc in items]
    row_pad = 30 * SCALE
    rows_h = sum(row_pad * 2 + cap_h(fname) + 20 * SCALE + cap_h(fdesc)
                 + int(fdesc.size * 1.42) * (len(b) - 1) for b in blocks)
    stack = cap_h(ft) + 70 * SCALE + rows_h + (50 * SCALE + cap_h(fr.mono) if foot_note else 0)
    y = y0 + (foot_y - y0 - stack) // 2

    x_end = put(d, M, y, title.rstrip("."), ft, INK, -0.03 * ft.size)
    sq = int(ft.size * 0.17)
    d.rectangle([x_end + ft.size * 0.04, y + cap_h(ft) - sq, x_end + ft.size * 0.04 + sq,
                 y + cap_h(ft)], fill=SIGNAL)
    y += cap_h(ft) + 70 * SCALE
    for i, ((nm, _), lines) in enumerate(zip(items, blocks), start=1):
        d.line([(M, y), (W - M, y)], fill=INK_20 if i > 1 else INK, width=SCALE)
        y += row_pad
        put(d, M, y + (cap_h(fname) - cap_h(fnum)) // 2, f"{i:02d}", fnum, INK, 0.06 * fnum.size)
        put(d, M + indent, y, nm, fname, INK, -0.02 * fname.size)
        y += cap_h(fname) + 20 * SCALE
        for j, ln in enumerate(lines):
            put(d, M + indent, y + j * int(fdesc.size * 1.42), ln, fdesc, INK_60)
        y += cap_h(fdesc) + int(fdesc.size * 1.42) * (len(lines) - 1) + row_pad
    if foot_note:
        put(d, M, y + 50 * SCALE, foot_note.upper(), fr.mono, INK, 0.08 * fr.mono.size)
    save(fr, name)


# ── the three highlights ────────────────────────────────────────────────────

HIGHLIGHTS = ["About", "Services", "Process"]


def build_all():
    n = len(HIGHLIGHTS)
    for i, h in enumerate(HIGHLIGHTS):
        cover(f"{i + 1:02d}-{h.lower()}-cover", i, n)

    # ABOUT — who we are, what we believe, the sign-off
    story_hook("01-about-1", "About", 1, 3,
               ["WE MAKE", "BRANDS", "IMPOSSIBLE", "TO SCROLL", "PAST."],
               body="PivtMedia is a social and content agency in Columbus, Ohio, for brands "
                    "done blending in.")
    story_index("01-about-2", "About", 2, 3, "OUR ORDER.",
                [("Strategy before content.", "We decide what to say before we decide how it "
                                              "looks."),
                 ("Taste before trends.", "Trends are studied, then bent, so the work still "
                                          "feels new a year later."),
                 ("Results before vanity.", "We measure what moves: reach, revenue, growth.")],
                foot_note="When two pull apart, the first word wins.")
    story_hook("01-about-3", "About", 3, 3, ["PROOF.", "NOT", "PROMISES."], ground=INK,
               body="Show the work instead of describing it. That's the whole approach.",
               cta="Book a call", note="pivtmedia.com")

    # SERVICES — the menu, the principle, the ask
    story_index("02-services-1", "Services", 1, 3, "WHAT WE MAKE.",
                [("Content", "Photo, video and short-form, made for the feed."),
                 ("Paid social", "Ads built to stop the scroll, then tested and tuned."),
                 ("Campaigns", "One idea, carried across every channel."),
                 ("Production", "Shoots planned, directed and delivered."),
                 ("Web", "Sites that look and sound like the brand.")])
    story_hook("02-services-2", "Services", 2, 3, ["ONE", "IDEA", "PER", "PIECE."],
               body="Whatever we make, it starts with one question: what is the single thing "
                    "people should remember?")
    story_hook("02-services-3", "Services", 3, 3, ["TELL US", "WHAT YOU", "NEED."], ground=INK,
               body="Send a DM or book a call. A real person answers.",
               cta="Book a call", note="contact@pivtmedia.com")

    # PROCESS — plan, produce, post, run
    story_hook("03-process-1", "Process", 1, 3, ["PLAN.", "PRODUCE.", "POST.", "RUN."],
               body="How every PivtMedia account works, start to finish.")
    story_index("03-process-2", "Process", 2, 3, "HOW IT WORKS.",
                [("Plan", "Who it's for, what it says, where it lives. Strategy comes first."),
                 ("Produce", "Shoots, edits and design, made to the plan."),
                 ("Post", "Published on schedule and written for each platform."),
                 ("Run", "Managed day to day. We test, learn and turn every result into the "
                         "next piece.")])
    story_hook("03-process-3", "Process", 3, 3, ["START", "WITH THE", "PLAN."], ground=INK,
               body="Every account begins with a strategy call. Bring the brand, we'll bring "
                    "the questions.",
               cta="Book a call", note="pivtmedia.com")


if __name__ == "__main__":
    build_all()
