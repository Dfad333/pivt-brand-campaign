"""Place a finished PivtMedia poster into a photographed scene as a physical print.

This is the reverse of everything else in `studio/`. The other modules put type ONTO a
photograph; this one puts a finished poster INTO one, so the work reads as a printed object
in a real room rather than a digital file.

    from mockup import place
    place("../raw/scene.png", "../final/10-no-noise.jpg", "../final/mockup.jpg",
          corners=[(x1,y1),(x2,y2),(x3,y3),(x4,y4)])   # TL, TR, BR, BL of the blank area

`corners` are in the SCENE's own pixel coordinates. Use `probe()` to print a coordinate grid
over the scene so the corners can be read off by eye.
"""
import os

import paths
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


def probe(scene_path, out_path, step=0.05):
    """Write a copy of the scene with a labelled percentage grid, to read corners off."""
    im = Image.open(scene_path).convert("RGB")
    w, h = im.size
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(paths.F_BOLD, max(14, w // 90))
    n = int(1 / step)
    for i in range(n + 1):
        x, y = int(w * i * step), int(h * i * step)
        d.line([(x, 0), (x, h)], fill=(255, 0, 255), width=2)
        d.line([(0, y), (w, y)], fill=(255, 0, 255), width=2)
        d.text((x + 4, 4), f"{i*step:.2f}", font=f, fill=(255, 0, 255))
        d.text((4, y + 4), f"{i*step:.2f}", font=f, fill=(255, 0, 255))
    im.save(out_path, quality=90)
    print(f"{os.path.basename(out_path)}  grid over {w}x{h}")


def place(scene_path, poster_path, out_path, corners, shade=0.90, warm=1.0):
    """Perspective-map `poster` onto the quad `corners` in `scene`.

    corners: [top-left, top-right, bottom-right, bottom-left] in scene pixels.
    shade:   multiply the poster's brightness so it sits in the scene's light (<1 darkens).
    warm:    colour temperature nudge; >1 warms the poster toward the room light.
    """
    scene = Image.open(scene_path).convert("RGBA")
    poster = Image.open(poster_path).convert("RGBA")

    if shade != 1.0:
        poster = ImageEnhance.Brightness(poster).enhance(shade)
    if warm != 1.0:
        r, g, b, a = poster.split()
        r = ImageEnhance.Brightness(r).enhance(warm)
        b = ImageEnhance.Brightness(b).enhance(2.0 - warm)
        poster = Image.merge("RGBA", (r, g, b, a))

    tl, tr, br, bl = corners
    xs = [p[0] for p in corners]
    ys = [p[1] for p in corners]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    bw, bh = x1 - x0, y1 - y0

    # PIL maps the OUTPUT box back into the SOURCE, so pass source corners in
    # the order NW, SW, SE, NE relative to the destination box.
    def rel(p):
        return (p[0] - x0, p[1] - y0)

    rtl, rtr, rbr, rbl = rel(tl), rel(tr), rel(br), rel(bl)
    pw, ph = poster.size
    quad = _solve(( (0, 0), (pw, 0), (pw, ph), (0, ph) ), (rtl, rtr, rbr, rbl), bw, bh)

    warped = poster.transform((bw, bh), Image.PERSPECTIVE, quad,
                              Image.BICUBIC)
    scene.alpha_composite(warped, (x0, y0))
    scene.convert("RGB").save(out_path, quality=97)
    print(f"{os.path.basename(out_path)}  poster placed into {os.path.basename(scene_path)}")


def _solve(src, dst, w, h):
    """Coefficients mapping destination pixels back to source (what PIL wants).

    Builds the standard 8x8 homography system and solves it by Gaussian elimination,
    so the studio keeps its single dependency (Pillow) and needs no numpy.
    """
    rows = []
    for (dx, dy), (sx, sy) in zip(dst, src):
        rows.append([dx, dy, 1, 0, 0, 0, -sx * dx, -sx * dy, sx])
        rows.append([0, 0, 0, dx, dy, 1, -sy * dx, -sy * dy, sy])

    n = 8
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(rows[r][col]))
        if abs(rows[piv][col]) < 1e-12:
            raise ValueError("degenerate quad — check the corner coordinates")
        rows[col], rows[piv] = rows[piv], rows[col]
        pv = rows[col][col]
        rows[col] = [v / pv for v in rows[col]]
        for r in range(n):
            if r != col and rows[r][col]:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[col])]
    return [rows[i][n] for i in range(n)]
