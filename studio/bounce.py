"""Composite a bouncing form across a static plate — the 'court' motion piece.

Why this exists: handing a flat graphic plate to a video model drifted the hue 170
degrees in 6 seconds (orange -> cyan). A flat abstract field gives the model nothing
to anchor on. So the plate stays a fixed image and only the form moves, which makes
colour drift structurally impossible and gives native 60fps instead of interpolated.

    python bounce.py
"""
import os

import paths
from PIL import Image, ImageDraw, ImageFilter

MO   = paths.MOTION
RAW  = paths.RAW
SEQ  = os.path.join(MO, "bounce-seq")

W, H   = 1080, 1920
FPS    = 60
SECS   = 8
N      = FPS * SECS

T_IN, T_OUT = 0.55, 7.05          # form on screen between these seconds
P0     = (0.88, 0.02)             # ground path, fractions of W/H
P1     = (-0.12, 0.78)            # exits left edge ABOVE the wordmark, never crosses it
BOUNCES   = 4
APEX      = 0.30                  # first apex as a fraction of H
DAMP      = 0.60                  # each bounce reaches this much of the last
SWITCH_AT = 2                     # contact number where sphere becomes cube
FORM_W    = 0.185                 # form width as a fraction of W


def key_white(path, thresh=248.0, soft=26.0):
    """White studio background -> alpha. The forms are near-black, so a luminance
    ramp keys them cleanly and keeps the antialiased edge."""
    im = Image.open(path).convert("RGB")
    lum = im.convert("L")
    a = lum.point(lambda v: 0 if v >= thresh else
                  (255 if v <= thresh - soft else int(255 * (thresh - v) / soft)))
    im = im.convert("RGBA"); im.putalpha(a)
    return im.crop(im.getbbox())


def height_at(u):
    """Bounce height 0..1 of APEX, plus the index of the last contact."""
    phase = u * BOUNCES
    idx, frac = int(phase), phase % 1.0
    return (DAMP ** idx) * 4 * frac * (1 - frac), idx


def main():
    os.makedirs(SEQ, exist_ok=True)
    plate = Image.open(os.path.join(MO, "court-src.png")).convert("RGB").resize(
        (W, H), Image.LANCZOS)

    forms = {}
    for name, f in (("sphere", "80-form-sphere.png"), ("cube", "81-form-cube.png")):
        im = key_white(os.path.join(RAW, f))
        fw = int(W * FORM_W)
        forms[name] = im.resize((fw, int(fw * im.height / im.width)), Image.LANCZOS)

    for i in range(N):
        t = i / FPS
        frame = plate.copy().convert("RGBA")

        if T_IN <= t <= T_OUT:
            u = (t - T_IN) / (T_OUT - T_IN)
            gx = (P0[0] + (P1[0] - P0[0]) * u) * W
            gy = (P0[1] + (P1[1] - P0[1]) * u) * H
            h, idx = height_at(u)
            form = forms["cube" if idx >= SWITCH_AT else "sphere"]
            fw, fh = form.size

            # cast shadow lives on the ground plane: tighter and darker on contact,
            # wider and fainter the higher the form is
            sw = fw * (1.02 - 0.30 * h)
            sh = sw * 0.34
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).ellipse(
                [gx - sw / 2, gy - sh / 2, gx + sw / 2, gy + sh / 2],
                fill=(60, 18, 4, int(120 * (1 - 0.60 * h))))
            frame.alpha_composite(lay.filter(ImageFilter.GaussianBlur(9 + 22 * h)))

            f = form
            if idx >= SWITCH_AT:                       # tumble only reads on the cube
                f = form.rotate(-26 * (u * BOUNCES - SWITCH_AT),
                                resample=Image.BICUBIC, expand=True)
            frame.alpha_composite(f, (int(gx - f.width / 2),
                                      int(gy - h * APEX * H - f.height * 0.82)))

        frame.convert("RGB").save(os.path.join(SEQ, "f%04d.png" % i))

    print("rendered %d frames at %dx%d, %d fps" % (N, W, H, FPS))


if __name__ == "__main__":
    main()
