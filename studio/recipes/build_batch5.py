"""Batch 5 — four colour-led BOEGÖW posters, four different systems."""
import os
import paths
from poster4 import poster_duotone, poster_bands, poster_riso, poster_stat, BLUE, MAGENTA

RAW = paths.RAW + os.sep
OUT = paths.FINAL + os.sep

# 1 — duotone: deep blue shadow into brand orange
poster_duotone(
    RAW + "22-jump-bw.png", OUT + "22-land-it.jpg",
    "DON'T LAUNCH.", "LAND IT.",
    "Timing is the campaign",
    "Anyone can pick a date. We pick the moment your market is already leaning in.",
    "Positioning. Timing. Spend. In that order.",
    shadow=(10, 14, 70), light=(255, 122, 0),
)

# 2 — Swiss colour bands
poster_bands(
    RAW + "24-profile-bw.png", OUT + "23-half-the-room.jpg",
    "HALF THE ROOM", "ALREADY LEFT.",
    "Attention audit", "You get three seconds. Most brands spend them clearing their throat.",
    "No. 05",
)

# 3 — riso halftone, magenta over blue
poster_riso(
    RAW + "23-hands-bw.png", OUT + "24-reach-them.jpg",
    "REACH IS", "NOT DEMAND.",
    "Printed in two colours",
    "A million impressions and nobody moved. Reach is rented. Demand is built.",
    "We build the second one.",
    c1=MAGENTA, c2=BLUE,
)

# 4 — type-only stat poster
poster_stat(
    OUT + "25-three-seconds.jpg",
    "3", "SECONDS",
    "THAT'S THE", "WHOLE PITCH.",
    "Everything before the fourth second is the only part most people will ever see.",
    "Write for the scroll, not the boardroom.",
)
