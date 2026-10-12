"""Batch 6 — masked/anonymous figures, four more distinct layouts."""
import os
import paths
from poster5 import poster_diptych, poster_knockout, poster_triptych, poster_receipt

RAW = paths.RAW + os.sep
OUT = paths.FINAL + os.sep

poster_diptych(
    RAW + "26-figure-mask.png", OUT + "26-be-the-face.jpg",
    "LET THE WORK", "BE THE FACE.",
    "Anonymity is a strategy",
    "You should not need a founder cult to sell a good product. Build something that "
    "carries itself into the room.",
)

poster_knockout(
    RAW + "28-mask-closeup.png", OUT + "27-blend.jpg",
    "BLEND.", "or be remembered. pick one.",
    "Every safe choice looks reasonable on the day you make it, and invisible six months later.",
    "Distinct beats polished.",
)

poster_triptych(
    RAW + "27-three-masks.png", OUT + "28-three-moves.jpg",
    "THREE MOVES.", "ONE BRAND.",
    ["01 Position", "02 Presence", "03 Proof"],
    "Skip any one of them and the other two start working against you.",
)

poster_receipt(
    OUT + "29-the-bill.jpg",
    "The bill comes later",
    [("Skipping positioning", "paid in ad spend"),
     ("Chasing every trend", "paid in relevance"),
     ("No measurement", "paid in guesswork"),
     ("Building the system", "+ compounds")],
    "Net", "YOUR CALL",
    "Every shortcut is a loan. This is the repayment schedule.",
)
