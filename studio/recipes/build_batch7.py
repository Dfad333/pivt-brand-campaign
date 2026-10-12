"""Batch 7 — no figures at all. Two proven treatments on new abstract material,
plus two quieter layouts."""
import os
import paths
from poster4 import poster_duotone, poster_riso
from poster6 import poster_word, poster_label

RAW = paths.RAW + os.sep
OUT = paths.FINAL + os.sep

# 1 — duotone on aerial dunes, warm ink-to-orange ramp
poster_duotone(
    RAW + "30-dunes-bw.png", OUT + "30-slow-is-fine.jpg",
    "SLOW IS FINE.", "DRIFTING ISN'T.",
    "Direction over speed",
    "A brand that moves slowly toward something beats one that moves quickly toward "
    "nothing in particular.",
    "Pick the horizon first.",
    shadow=(28, 12, 6), light=(255, 138, 26),
)

# 2 — riso halftone on brutalist geometry, warm two-colour print
poster_riso(
    RAW + "31-stair-bw.png", OUT + "31-every-floor.jpg",
    "EVERY FLOOR", "LOOKS THE SAME.",
    "Two-colour print",
    "Scale without a system just repeats your problems on a bigger budget.",
    "Build the structure first.",
    c1=(230, 62, 20), c2=(120, 34, 96),
)

# 3 — type-only, giant word
poster_word(
    OUT + "32-later.jpg", "LATER.",
    [("The competitor who started last quarter", (0.06, 0.20)),
     ("The budget you will not get back", (0.60, 0.20)),
     ("The position someone else takes", (0.06, 0.72)),
     ("The version of this that costs triple", (0.60, 0.72))],
    "Four things that get more expensive every week you wait.",
    "There is no cheaper time than now.",
    bg=(17, 17, 17), word_col=ORANGE if False else (255, 92, 0), ghost="LATER.",
)

# 4 — gallery catalogue label
poster_label(
    RAW + "32-object.png", OUT + "33-first-draft.jpg",
    "First draft",
    [("Medium", "Paper, pressure, patience"),
     ("Condition", "Deliberately unfinished"),
     ("Provenance", "Every good idea, ever"),
     ("Status", "Not the final form")],
    "Nobody frames the first draft. Everybody needs one. The work you admire is the "
    "twentieth version of something that started exactly like this.",
    cat_no="PM-014",
)
