"""`poster_overlap` — the device from BOEGÖW's "REALITY. REWRITTEN." piece.

Huge headline sits at the TOP of the canvas; the subject is a cutout layered OVER the
type so it interrupts the letterforms. A micro-line is justified edge-to-edge beneath,
and a bracketed credit closes the poster. Nothing else in the set puts type behind the
image, which is what makes this read differently.
"""
import os
from PIL import Image, ImageDraw

from poster import (W, H, MARGIN, ORANGE, INK, F_BOLD, font, track_text,
                    track_width, fit_size, wrap, paste_logo)

PALE = (249, 248, 245)


def justified(draw, text, fnt, x0, x1, y, fill, min_gap=10):
    """Spread words evenly so the line spans exactly x0..x1."""
    words = text.upper().split()
    if len(words) == 1:
        track_text(draw, (x0, y), words[0], fnt, fill, 2.0)
        return
    widths = [track_width(draw, w, fnt, 2.0) for w in words]
    gap = max(min_gap, ((x1 - x0) - sum(widths)) / (len(words) - 1))
    x = x0
    for w, ww in zip(words, widths):
        track_text(draw, (x, y), w, fnt, fill, 2.0)
        x += ww + gap


def poster_endcard(out_path, l1, l2, spread_line, foot_line, credit,
                   bg=(17, 17, 17), ink=(255, 255, 255), accent=ORANGE):
    """Closing slide for a carousel.

    Deliberately breaks the pattern so a viewer knows the set has ended: the field
    inverts to ink and the photograph is gone entirely — the absence IS the signal.
    It keeps `poster_overlap`'s typographic system (top headline, justified micro-line,
    bracketed credit) so it still reads as the same family, and the wordmark moves to
    the centre where the subject used to be.
    """
    img = Image.new("RGBA", (W, H), bg + (255,))
    draw = ImageDraw.Draw(img)

    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.025 * size
    y = int(H * 0.035)
    for line in (l1, l2):
        track_text(draw, (MARGIN, y), line, f, ink, tr)
        y += int(size * 1.02)

    fs = font(F_BOLD, 24)
    justified(draw, spread_line, fs, MARGIN, W - MARGIN, int(H * 0.365), ink)

    # wordmark sits where the subject stood on the previous slides — scale it up, or the
    # empty field reads as an accident rather than a deliberate close
    lw = 460
    paste_logo(img, lw, ((W - lw) // 2, int(H * 0.505)), white=True)

    ff = font(F_BOLD, 27)
    fw = track_width(draw, foot_line.upper(), ff, 2.0)
    track_text(draw, ((W - fw) / 2, H - 148), foot_line.upper(), ff, ink, 2.0)

    fc = font(F_BOLD, 27)
    ct = f"[ {credit.upper()} ]"
    cw = track_width(draw, ct, fc, 2.0)
    track_text(draw, ((W - cw) / 2, H - 104), ct, fc, accent, 2.0)

    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  endcard  headline={size}px")


def poster_overlap(cutout_path, out_path, l1, l2, spread_line, foot_line, credit,
                   bg=PALE, obj_h=0.655, obj_bottom=0.878, spread_y=0.365):
    img = Image.new("RGBA", (W, H), bg + (255,))
    draw = ImageDraw.Draw(img)

    # headline, top-aligned, as large as the width allows
    size = fit_size(draw, [l1, l2], F_BOLD, W - 2 * MARGIN)
    f = font(F_BOLD, size)
    tr = -0.025 * size
    y = int(H * 0.035)
    for line in (l1, l2):
        track_text(draw, (MARGIN, y), line, f, INK, tr)
        y += int(size * 1.02)

    # subject cutout, layered OVER the headline
    obj = Image.open(cutout_path).convert("RGBA")
    obj = obj.crop(obj.split()[-1].getbbox())
    target_h = int(H * obj_h)
    scale = target_h / obj.height
    obj = obj.resize((int(obj.width * scale), target_h), Image.LANCZOS)
    if obj.width > W - 2 * MARGIN:
        scale = (W - 2 * MARGIN) / obj.width
        obj = obj.resize((int(obj.width * scale), int(obj.height * scale)), Image.LANCZOS)
    img.alpha_composite(obj, ((W - obj.width) // 2,
                              int(H * obj_bottom) - obj.height))

    # justified micro-line, sitting on top of everything
    draw = ImageDraw.Draw(img)
    fs = font(F_BOLD, 24)
    justified(draw, spread_line, fs, MARGIN, W - MARGIN, int(H * spread_y), INK)

    # closing lines
    ff = font(F_BOLD, 27)
    fw = track_width(draw, foot_line.upper(), ff, 2.0)
    track_text(draw, ((W - fw) / 2, H - 148), foot_line.upper(), ff, INK, 2.0)

    fc = font(F_BOLD, 27)
    ct = f"[ {credit.upper()} ]"
    cw = track_width(draw, ct, fc, 2.0)
    track_text(draw, ((W - cw) / 2, H - 104), ct, fc, ORANGE, 2.0)

    lw = 118
    paste_logo(img, lw, (MARGIN, H - 150))
    img.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  overlap  headline={size}px")
