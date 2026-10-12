"""Build a single contact sheet of everything in final/ so the whole system is visible
at a glance. Re-run any time new posters are added.

    python contact_sheet.py
"""
import glob
import os

import paths
from PIL import Image, ImageDraw, ImageFont

FINAL = paths.FINAL
OUT = paths.CONTACT_SHEET
F_BOLD = paths.F_BOLD

COLS = 7
CELL_W = 300
PAD = 18
LABEL_H = 30
BG = (247, 243, 233)
INK = (17, 17, 17)

files = sorted(f for f in glob.glob(os.path.join(FINAL, "*.jpg"))
               if not os.path.basename(f).startswith("_"))
if not files:
    raise SystemExit("no posters found in final/")

cell_h = int(CELL_W * 2000 / 1600)
rows = (len(files) + COLS - 1) // COLS
W = COLS * (CELL_W + PAD) + PAD
H = rows * (cell_h + LABEL_H + PAD) + PAD + 70

sheet = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(sheet)

title = ImageFont.truetype(F_BOLD, 30)
small = ImageFont.truetype(F_BOLD, 15)
draw.text((PAD, 24), f"PIVTMEDIA — CAMPAIGN CONTACT SHEET   ·   {len(files)} POSTERS",
          font=title, fill=INK)

for i, path in enumerate(files):
    r, c = divmod(i, COLS)
    x = PAD + c * (CELL_W + PAD)
    y = 70 + PAD + r * (cell_h + LABEL_H + PAD)
    im = Image.open(path).convert("RGB").resize((CELL_W, cell_h), Image.LANCZOS)
    sheet.paste(im, (x, y))
    draw.rectangle([x, y, x + CELL_W, y + cell_h], outline=(206, 200, 190), width=1)
    name = os.path.splitext(os.path.basename(path))[0]
    if len(name) > 34:
        name = name[:33] + "…"
    draw.text((x, y + cell_h + 8), name.upper(), font=small, fill=INK)

sheet.save(OUT, quality=92)
print(f"wrote {OUT}  ({len(files)} posters, {W}x{H})")
