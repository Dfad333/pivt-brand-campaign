"""Motion-frame type layer for PivtMedia.

Different from every other module in studio/: the other layouts flatten type onto a
still and save a JPG. This one builds the type as a **transparent RGBA layer** so the
same artwork can be burned over a video clip frame-for-frame.

Structure follows the locked-off "tap" motion piece: two micro-rules in the top
corners, one enormous line across the bottom. Nothing animates — the type is pinned
for the whole clip, which is what keeps it razor sharp.

    from motion import type_layer, preview
    type_layer("overlay.png", 1080, 1350, wordmark="PIVTMEDIA")
    preview("../raw/66-content-on-tap-A2.png", "../final/68-content-on-tap.jpg")
"""
import os
from PIL import Image, ImageDraw

from poster import (F_BOLD, INK, ORANGE, font, track_text, track_width,
                    fit_size, cover, paste_logo)

MICRO_L = "PIVT + MEDIA //"
MICRO_R = "WE MAKE IT LOOK EASY."


def _ground_lum(photo, W, H, box):
    """Mean luminance of `box` on the photo scaled to WxH (0-255)."""
    from PIL import ImageStat
    g = cover(photo.convert("RGB"), W, H).convert("L")
    x0, y0, x1, y1 = box
    return ImageStat.Stat(g.crop((max(0, x0), max(0, y0),
                                  min(W, x1), min(H, y1)))).mean[0]


def type_layer(out_path, W=1080, H=1350, wordmark="PIVTMEDIA", headline=None,
               ink=(255, 255, 255), micro_l=MICRO_L, micro_r=MICRO_R,
               head_y=0.855, logo=False, foot=None, foot_y=0.918, foot_ink=None,
               foot_bar=None, halo=True):
    """Transparent type overlay sized WxH. Returns the RGBA image.

    `wordmark` is the giant bottom line. Pass `headline` instead for a shorter
    statement line, closed by either the barcode lockup (`logo=True`) or a
    letterspaced text line (`foot="PIVT + MEDIA //"`). A text foot reads cleaner
    than the barcode when the ground under it is busy — the striped shelf eats
    the mark's fine bars.
    """
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    m = int(W * 0.055)

    # a soft halo keeps micro-copy alive where it crosses a light/dark edge
    stroke = 2 if halo else 0
    hfill = (0, 0, 0, 120) if ink == (255, 255, 255) else (255, 255, 255, 120)

    fm = font(F_BOLD, max(11, int(W * 0.0165)))
    tr = W * 0.0016
    track_text(draw, (m, m), micro_l, fm, ink, tr,
               stroke=stroke, stroke_fill=hfill)
    track_text(draw, (W - m, m), micro_r, fm, ink, tr, anchor_right=True,
               stroke=stroke, stroke_fill=hfill)

    if headline:
        size = fit_size(draw, [headline], F_BOLD, W - 2 * m)
        f = font(F_BOLD, size)
        w_ = track_width(draw, headline, f, -0.02 * size)
        # head_y is the BASELINE-ish anchor as a fraction of height. Put the headline
        # wherever the ground is stable for the whole clip, not just frame 1 — on a
        # depleting shot the bottom fills up, so the top is the only constant zone.
        y = int(H * head_y) - size
        track_text(draw, ((W - w_) / 2, y), headline, f, ink, -0.02 * size)
        if foot:
            ff = font(F_BOLD, max(11, int(W * 0.0175)))
            ftr = W * 0.0042                      # wide tracking so it reads as a lockup
            fw = track_width(draw, foot, ff, ftr)
            # On a motion piece the foot must survive EVERY frame, not just the first.
            # Here the growing coil swings the plate band by 50-110 lum and the shelf
            # is diagonally striped, so no fixed ink works and a mean-based choice
            # can't save type crossing that edge. A solid bar gives the line its own
            # ground on every frame — and a solid accent shape is the house device.
            if foot_bar:
                bar_h = int(H * 0.058)
                draw.rectangle([0, H - bar_h, W, H], fill=foot_bar)
                fink = foot_ink or (255, 255, 255)
                y = H - bar_h + (bar_h - ff.getbbox("H")[3]) // 2
                track_text(draw, ((W - fw) / 2, y), foot, ff, fink, ftr)
            else:
                fink = foot_ink or ink
                fhalo = ((0, 0, 0, 120) if fink == (255, 255, 255)
                         else (255, 255, 255, 120))
                track_text(draw, ((W - fw) / 2, int(H * foot_y)), foot, ff, fink, ftr,
                           stroke=stroke, stroke_fill=fhalo)
        elif logo:
            lw = int(W * 0.13)
            paste_logo(layer, lw, ((W - lw) // 2, int(H * 0.895)),
                       white=(ink == (255, 255, 255)))
    else:
        # giant wordmark, full measure, sitting on the bottom margin
        size = fit_size(draw, [wordmark], F_BOLD, W - int(W * 0.07), lo=20, hi=600)
        f = font(F_BOLD, size)
        w_ = track_width(draw, wordmark, f, -0.02 * size)
        asc, desc = f.getmetrics()
        y = H - int(H * 0.035) - asc
        track_text(draw, ((W - w_) / 2, y), wordmark, f, ink, -0.02 * size)

    if out_path:
        layer.save(out_path)
        print("%-34s %dx%d  type=%dpx  ink=%s"
              % (os.path.basename(out_path), W, H, size, ink))
    return layer


def preview(photo_path, out_path, W=1600, H=2000, auto_ink=True, ink=None, **kw):
    """Flatten the type layer over the still — the video's first frame."""
    photo = Image.open(photo_path)
    base = cover(photo.convert("RGB"), W, H).convert("RGBA")

    if ink is None:
        lum = _ground_lum(photo, W, H, (0, int(H * 0.78), W, int(H * 0.97)))
        ink = (255, 255, 255) if (lum < 125 or not auto_ink) else INK
        print("  bottom-band mean_lum = %.0f -> ink %s" % (lum, ink))

    base.alpha_composite(type_layer(None, W, H, ink=ink, **kw))
    base.convert("RGB").save(out_path, quality=97)
    print("  saved", out_path)
    return ink
