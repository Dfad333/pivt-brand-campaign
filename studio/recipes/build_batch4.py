"""Batch 4 — two new BOEGÖW layouts, plus LONGEBLACK applied to two real clients."""
import os
import paths
from poster2 import poster_endorse
from poster3 import poster_index, poster_outline

RAW = paths.RAW + os.sep
OUT = paths.FINAL + os.sep
SITE = os.path.join(paths.ROOT, os.pardir, "CONCEPT", "site",
                    "public", "projects") + os.sep

# ---- BOEGÖW lineage — two layouts not used before -------------------------
poster_index(
    RAW + "18-coat-bw.png", OUT + "18-the-whole-system.jpg",
    "[ NOTHING LEFT LOOSE ]", "THE WHOLE", "SYSTEM.",
    [("Positioning", "Who it is for"),
     ("Content", "Why they stay"),
     ("Paid", "How they find it"),
     ("Measurement", "What it returned")],
    "Four parts. One system. We do not sell them separately because they do not work separately.",
    tape_text="Built as one piece",
)

poster_outline(
    RAW + "19-storm-bw.png", OUT + "19-weather-it.jpg",
    "ANYONE CAN", "SPEND IT.", "Media buying is not a strategy",
    "A budget is not a plan. Without a position to defend, spend just buys you a faster way to be forgotten.",
    "We build the position first.",
    bar_word="Then we scale it",
)

# ---- LONGEBLACK lineage — real client work from the site ------------------
poster_endorse(
    SITE + "klin-04.jpg", OUT + "20-klin.jpg",
    "Klin", "Art direction & social by PivtMedia",
    "Odd by design.",
    y_frac=0.09,
)

poster_endorse(
    SITE + "cool-kids-07.jpg", OUT + "21-cool-kids.jpg",
    "Cool Kids", "Content & paid social by PivtMedia",
    "A Fall '25 drop, made unmissable.",
    y_frac=0.055, scrim=0.46,
)
