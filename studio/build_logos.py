"""Build the canonical PivtMedia campaign logo variants from the v2 logo (Instrument Sans, inline brackets)."""
import os
import shutil

import paths
from PIL import Image

OUT = paths.LOGO_DIR
SRC = os.path.join(OUT, "v2")
os.makedirs(OUT, exist_ok=True)

dark_ink = Image.open(os.path.join(SRC, "pivt-logo-v2.png")).convert("RGBA")         # ink   -> for light photos
light_ink = Image.open(os.path.join(SRC, "pivt-logo-v2-cream.png")).convert("RGBA")  # cream -> for dark photos
print(f"source: {dark_ink.size[0]}x{dark_ink.size[1]}")


def flatten(src, bg):
    base = Image.new("RGBA", src.size, (*bg, 255))
    return Image.alpha_composite(base, src)


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

for src, name in [("pivt-logo-v2.svg", "pivt-logo-black.svg"), ("pivt-logo-v2-cream.svg", "pivt-logo-white.svg")]:
    shutil.copyfile(os.path.join(SRC, src), os.path.join(OUT, name))
    print(f"wrote {name}")
