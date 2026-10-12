"""A/B test: production gear as abstracted craft texture vs. as hero object.

Identical layout, headline, kicker and micro-copy on both. The photograph is the only
variable, so the comparison is honest.
"""
import os
import paths
from poster import poster_split

RAW = paths.RAW + os.sep
OUT = paths.FINAL + os.sep

COPY = dict(
    l1="FOCUS IS",
    l2="A DECISION.",
    kicker="CRAFT, NOT KIT.",
    micro_l="Every frame is a choice about what the viewer is allowed to care about. "
            "Most brands never make it on purpose.",
    micro_r="Gear is table stakes. Judgement is the product.",
)

# A — gear abstracted almost past recognition
poster_split(RAW + "34-lens-macro.png", OUT + "A-gear-as-texture.jpg",
             COPY["l1"], COPY["l2"], COPY["kicker"], COPY["micro_l"], COPY["micro_r"])

# B — gear clearly legible as equipment
poster_split(RAW + "35-camera-rig.png", OUT + "B-gear-as-hero.jpg",
             COPY["l1"], COPY["l2"], COPY["kicker"], COPY["micro_l"], COPY["micro_r"])
