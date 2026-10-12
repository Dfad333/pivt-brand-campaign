"""Build the 3 canonical PivtMedia campaign logo variants from the transparent barcode lockup."""
import os

import paths
from PIL import Image

SRC = os.path.join(paths.ROOT, os.pardir, "pivt-media-portal",
                   "src", "assets", "logo-barcode.png")
OUT = paths.LOGO_DIR
os.makedirs(OUT, exist_ok=True)

im = Image.open(SRC).convert("RGBA")
im = im.crop(im.split()[-1].getbbox())  # trim transparent padding
w, h = im.size
print(f"trimmed source: {w}x{h}")


def is_orange(r, g, b):
    """Accent bar: strongly red-dominant."""
    return r > 150 and r - g > 60 and r - b > 60


def recolor(src, ink):
    """Recolor non-accent ink pixels to `ink`, preserving alpha and the orange bar."""
    out = Image.new("RGBA", src.size)
    src_px, out_px = src.load(), out.load()
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            r, g, b, a = src_px[x, y]
            if a == 0:
                out_px[x, y] = (0, 0, 0, 0)
            elif is_orange(r, g, b):
                out_px[x, y] = (255, 92, 0, a)
            else:
                out_px[x, y] = (*ink, a)
    return out


def flatten(src, bg):
    base = Image.new("RGBA", src.size, (*bg, 255))
    return Image.alpha_composite(base, src)


dark_ink = recolor(im, (18, 18, 18))    # black ink  -> for light photos
light_ink = recolor(im, (255, 255, 255))  # white ink -> for dark photos

variants = {
    "pivt-logo-transparent-black.png": dark_ink,
    "pivt-logo-transparent-white.png": light_ink,
    "pivt-logo-on-white.png": flatten(dark_ink, (255, 255, 255)),
    "pivt-logo-on-black.png": flatten(light_ink, (18, 18, 18)),
}

for name, img in variants.items():
    path = os.path.join(OUT, name)
    img.save(path)
    print(f"wrote {name}  {img.size}  mode={img.mode}")
