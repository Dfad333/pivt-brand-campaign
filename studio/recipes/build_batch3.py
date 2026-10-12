"""Batch 3 — two BOEGÖW-lineage posters and two LONGEBLACK-lineage posters."""
import os
import paths
from poster import poster_split, poster_disc
from poster2 import poster_endorse

RAW = paths.RAW + os.sep
OUT = paths.FINAL + os.sep

# ---- BOEGÖW lineage -------------------------------------------------------
poster_split(
    RAW + "14-paper-stack-bw.png", OUT + "14-proof-not-promises.jpg",
    "PROOF.", "NOT PROMISES.", "RECEIPTS ONLY.",
    "Every claim we make about your growth is one you can open and audit yourself.",
    "No vanity metrics. No borrowed credit. No rounding up.",
    photo_tags=(("Show the work.", (0.06, 0.28)),
                ("Then show the numbers.", (0.55, 0.70))),
)

poster_disc(
    RAW + "15-foil-bw.png", OUT + "15-fewer-clients.jpg",
    "[ FEWER CLIENTS ]", "[ BETTER WORK ]",
    "Capacity is a strategy. We protect it on purpose.",
    "Depth over volume.",
    "Attention is finite. So is ours.",
)

# ---- LONGEBLACK lineage ---------------------------------------------------
poster_endorse(
    RAW + "16-atelier-warm.png", OUT + "16-built-to-last.jpg",
    "Built to Last", "Brand systems by PivtMedia",
    "For founders who intend to still be here in ten years.",
    y_frac=0.38,
)

poster_endorse(
    RAW + "17-dining-warm.png", OUT + "17-the-long-game.jpg",
    "The Long Game", "Strategy by PivtMedia",
    "Compounding beats campaigns. Every single time.",
    y_frac=0.27, scrim=0.50,
)
