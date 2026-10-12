"""Photoreal bouncing ball across the court plate — full trajectory control.

Three AI video attempts (Hailuo, Seedance, MiniMax H3) all refused to drive the ball
off-frame; each kept it near its start position. So the realism comes from AI and the
trajectory comes from code:

  * the ball is a REAL photographic cutout, extracted by differencing an AI frame
    against the clean plate, so it keeps its actual felt texture and lighting
  * accumulation motion blur (stamping sub-frame copies) — what actually sells speed
  * shadow keyed to height: large/soft/offset at apex, tight/dark/under at contact
  * enters right, three bounces each landing further left, exits left

    python bounce2.py
"""
import math
import os

import paths
from PIL import Image, ImageChops, ImageDraw, ImageFilter

MO  = paths.MOTION
RAW = paths.RAW
SEQ = os.path.join(MO, "bounce2-seq")

W, H = 1080, 1920
FPS, SECS = 60, 5
N = FPS * SECS

T_IN, T_OUT = 0.18, 4.25          # ball on screen; empty court after it leaves
X0, X1 = 1.12, -0.14              # ground x, fractions of W: off right -> off left
Y0, Y1 = 0.30, 0.70               # ground y travels down-frame, stays above the wordmark
BOUNCES, APEX, DAMP = 3, 0.30, 0.55
BALL_W = 0.30                     # ball width as a fraction of W
BLUR_STEPS = 7                    # sub-frame samples for accumulation motion blur
BLUR_WIN = 0.5                    # fraction of a frame the shutter is open; a full
                                  # frame is physically right but smears the felt away


def extract_ball():
    """Lift the real photographed ball out of an AI frame.

    Differencing against the plate fails — the AI re-render differs subtly everywhere.
    Keying on saturation alone eats the ball's shaded side, which is dark. So: key a
    confident CORE (desaturated + bright), fit a circle to it, and use that circle as
    the alpha. A tennis ball is round, so the fit is exact and the shaded side survives.
    """
    shot = Image.open(os.path.join(RAW, "86-ball-end.png")).convert("RGB")
    W_, H_ = shot.size
    crop = shot.crop((int(W_ * 0.10), int(H_ * 0.585), int(W_ * 0.56), int(H_ * 0.86)))
    cw, ch = crop.size

    _, S, V = crop.convert("HSV").split()
    core = ImageChops.multiply(S.point(lambda s: 255 if s < 105 else 0),
                               V.point(lambda v: 255 if v > 150 else 0))
    bb = core.filter(ImageFilter.MedianFilter(9)).getbbox()

    cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    r = max(bb[2] - bb[0], bb[3] - bb[1]) / 2
    alpha = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(alpha).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    alpha = alpha.filter(ImageFilter.GaussianBlur(2))

    ball = crop.convert("RGBA")
    ball.putalpha(alpha)
    return ball.crop((int(cx - r - 3), int(cy - r - 3), int(cx + r + 3), int(cy + r + 3)))


def state(t):
    """Ground position and height (0..1 of APEX) at time t."""
    u = (t - T_IN) / (T_OUT - T_IN)
    gx = (X0 + (X1 - X0) * u) * W
    gy = (Y0 + (Y1 - Y0) * u) * H
    phase = u * BOUNCES
    idx, frac = int(phase), phase % 1.0
    h = (DAMP ** idx) * 4 * frac * (1 - frac)
    return gx, gy, h, u


def main():
    os.makedirs(SEQ, exist_ok=True)
    plate = Image.open(os.path.join(MO, "court-src.png")).convert("RGB").resize(
        (W, H), Image.LANCZOS)

    ball = extract_ball()
    bw = int(W * BALL_W)
    ball = ball.resize((bw, int(bw * ball.height / ball.width)), Image.LANCZOS)
    ball.save(os.path.join(MO, "ball-sprite.png"))
    print("ball sprite %dx%d" % ball.size)

    for i in range(N):
        t = i / FPS
        frame = plate.copy().convert("RGBA")

        if T_IN <= t <= T_OUT:
            gx, gy, h, u = state(t)

            # shadow: on the ground, tight and dark at contact, wide and faint at apex
            sw = ball.width * (0.98 - 0.22 * h)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).ellipse(
                [gx - sw / 2, gy - sw * 0.30 / 2, gx + sw / 2, gy + sw * 0.30 / 2],
                fill=(72, 22, 6, int(150 * (1 - 0.55 * h))))
            frame.alpha_composite(lay.filter(ImageFilter.GaussianBlur(7 + 26 * h)))

            # accumulation motion blur: stamp sub-frame copies along the real path
            acc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            for k in range(BLUR_STEPS):
                tk = t + (k / BLUR_STEPS - 0.5) * BLUR_WIN / FPS
                if not (T_IN <= tk <= T_OUT):
                    continue
                bx, by, bh, bu = state(tk)
                spr = ball.rotate(-150 * bu, resample=Image.BICUBIC, expand=True)
                stamp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                stamp.paste(spr, (int(bx - spr.width / 2),
                                  int(by - bh * APEX * H - spr.height * 0.88)))
                acc = Image.blend(acc, stamp, 1.0 / (k + 1))
            frame.alpha_composite(acc)

        frame.convert("RGB").save(os.path.join(SEQ, "f%04d.png" % i))

    print("rendered %d frames at %dx%d, %d fps" % (N, W, H, FPS))


if __name__ == "__main__":
    main()
