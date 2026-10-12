"""Every approved poster, reproducible in one run.

This is the single source of truth for what was built and how. The older
`build_batch*.py` scripts are kept for history but are superseded by this file.

    cd brand-campaign/studio
    python recipes/rebuild_all.py

Nothing here regenerates photographs — it only re-composites type onto the images
already in `raw/`, so it is free and instant. Change a headline here and re-run.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layouts import build                      # noqa: E402
from compose import compose                    # noqa: E402
from poster4 import MAGENTA, BLUE              # noqa: E402

RAW = "../raw/"
OUT = "../final/"
PN = "Practice notes — no. "


# ── EARLY: logo/tagline composited onto text-free photographs ───────────────
compose(RAW + "06-tangle-thread-light.png", OUT + "06-strategy-straight-line.jpg",
        tagline="STRATEGY IS THE STRAIGHT LINE", tagline_y=0.165)
compose(RAW + "07-facade-neutral.png", OUT + "07-everyone-built-the-same-building.jpg")


# ── BOEGÖW ─────────────────────────────────────────────────────────────────
build("split", RAW + "10-figure-bw.png", OUT + "10-no-noise.jpg",
      "NO NOISE.", "JUST SIGNAL.", "ON PURPOSE.",
      "We build the brand, the content and the systems that make attention turn into "
      "revenue. Nothing decorative.",
      "Independent. Selective. Accountable to the number, not the applause.",
      photo_tags=(("Enough strategy.", (0.06, 0.62)), ("Enough craft.", (0.62, 0.30))))

build("disc", RAW + "11-ink-bw.png", OUT + "11-no-guesswork.jpg",
      "[ NO GUESSWORK ]", "[ ONLY OUTCOMES ]",
      "Every decision traced to a number. Every asset earning its place.",
      "Where the idea meets the market.", "Strategy. Content. Systems.")

build("tape", RAW + "12-corridor-bw.png", OUT + "12-move-first.jpg",
      "MOVE FIRST.", "EXPLAIN LATER.", "No committee required",
      "Independent. Selective.",
      "Most brands wait for permission. The market rewards the ones already moving.",
      "Strategy. Content. Systems.")

build("split", RAW + "14-paper-stack-bw.png", OUT + "14-proof-not-promises.jpg",
      "PROOF.", "NOT PROMISES.", "RECEIPTS ONLY.",
      "Every claim we make about your growth is one you can open and audit yourself.",
      "No vanity metrics. No borrowed credit. No rounding up.",
      photo_tags=(("Show the work.", (0.06, 0.28)),
                  ("Then show the numbers.", (0.55, 0.70))))

build("disc", RAW + "15-foil-bw.png", OUT + "15-fewer-clients.jpg",
      "[ FEWER CLIENTS ]", "[ BETTER WORK ]",
      "Capacity is a strategy. We protect it on purpose.",
      "Depth over volume.", "Attention is finite. So is ours.")

build("index", RAW + "18-coat-bw.png", OUT + "18-the-whole-system.jpg",
      "[ NOTHING LEFT LOOSE ]", "THE WHOLE", "SYSTEM.",
      [("Positioning", "Who it is for"), ("Content", "Why they stay"),
       ("Paid", "How they find it"), ("Measurement", "What it returned")],
      "Four parts. One system. We do not sell them separately because they do not "
      "work separately.",
      tape_text="Built as one piece")

build("outline", RAW + "19-storm-bw.png", OUT + "19-weather-it.jpg",
      "ANYONE CAN", "SPEND IT.", "Media buying is not a strategy",
      "A budget is not a plan. Without a position to defend, spend just buys you a "
      "faster way to be forgotten.",
      "We build the position first.", bar_word="Then we scale it")

build("duotone", RAW + "22-jump-bw.png", OUT + "22-land-it.jpg",
      "DON'T LAUNCH.", "LAND IT.", "Timing is the campaign",
      "Anyone can pick a date. We pick the moment your market is already leaning in.",
      "Positioning. Timing. Spend. In that order.",
      shadow=(10, 14, 70), light=(255, 122, 0))

build("riso", RAW + "23-hands-bw.png", OUT + "24-reach-them.jpg",
      "REACH IS", "NOT DEMAND.", "Printed in two colours",
      "A million impressions and nobody moved. Reach is rented. Demand is built.",
      "We build the second one.", c1=MAGENTA, c2=BLUE)

build("stat", OUT + "25-three-seconds.jpg", "3", "SECONDS",
      "THAT'S THE", "WHOLE PITCH.",
      "Everything before the fourth second is the only part most people will ever see.",
      "Write for the scroll, not the boardroom.")

build("duotone", RAW + "30-dunes-bw.png", OUT + "30-slow-is-fine.jpg",
      "SLOW IS FINE.", "DRIFTING ISN'T.", "Direction over speed",
      "A brand that moves slowly toward something beats one that moves quickly toward "
      "nothing in particular.",
      "Pick the horizon first.", shadow=(28, 12, 6), light=(255, 138, 26))

build("riso", RAW + "31-stair-bw.png", OUT + "31-every-floor.jpg",
      "EVERY FLOOR", "LOOKS THE SAME.", "Two-colour print",
      "Scale without a system just repeats your problems on a bigger budget.",
      "Build the structure first.", c1=(230, 62, 20), c2=(120, 34, 96))

build("word", OUT + "32-later.jpg", "LATER.",
      [("The competitor who started last quarter", (0.06, 0.20)),
       ("The budget you will not get back", (0.60, 0.20)),
       ("The position someone else takes", (0.06, 0.72)),
       ("The version of this that costs triple", (0.60, 0.72))],
      "Four things that get more expensive every week you wait.",
      "There is no cheaper time than now.",
      bg=(17, 17, 17), word_col=(255, 92, 0), ghost="LATER.")

build("label", RAW + "32-object.png", OUT + "33-first-draft.jpg", "First draft",
      [("Medium", "Paper, pressure, patience"), ("Condition", "Deliberately unfinished"),
       ("Provenance", "Every good idea, ever"), ("Status", "Not the final form")],
      "Nobody frames the first draft. Everybody needs one. The work you admire is the "
      "twentieth version of something that started exactly like this.",
      cat_no="PM-014")

build("overlap", RAW + "36-horn-cut.png", OUT + "34-attention-redirected.jpg",
      "ATTENTION.", "REDIRECTED.",
      "talking louder is not the same as being heard",
      "Messages built to carry.", "PivtMedia visual direction.")

build("overlap", RAW + "37-cone-cut.png", OUT + "35-impossible-to-ignore.jpg",
      "IMPOSSIBLE.", "TO IGNORE.",
      "you can be polite or you can be remembered",
      "Positions worth defending.", "PivtMedia visual direction.")

build("scatter",
      [(RAW + "45-terracotta.png", "Positioning", (0.075, 0.145), 0.235),
       (RAW + "44-gel-form.png", "Creative", (0.355, 0.215), 0.235),
       (RAW + "46-silk.png", "Distribution", (0.655, 0.130), 0.235)],
      OUT + "42-three-questions.jpg", "THREE QUESTIONS.", "ONE ANSWER.",
      "PivtMedia — studio note",
      "Who is it for, why should they care, and where will they see it. Everything "
      "else is decoration.",
      body="Positioning tells you what to make. Creative decides whether anyone stops. "
           "Distribution decides whether it was ever seen at all.")

build("window", RAW + "46-silk.png", OUT + "43-warm-to-the-touch.jpg",
      "MADE TO BE", "FELT FIRST.", "[ colour is a decision ]",
      "People decide how they feel about a brand long before they read a word of it.",
      "Then they look for reasons.")

# ── Drive-reference set: saturated colour blocking ─────────────────────────
build("knockout", RAW + "63-mustard-teal.png", OUT + "57-wait.jpg",
      "WAIT.", "or take the room while it is empty.",
      "The brands that hesitated in January are the ones buying attention back at a "
      "premium in June.",
      "Move while it is cheap.")

build("overlap", RAW + "66-reader-cut.png", OUT + "59-nobody-reads.jpg",
      "NOBODY READS.", "EVERYONE SCANS.",
      "write for the three seconds you actually get",
      "Built to be understood at a glance.", "PivtMedia visual direction.")

build("outline", RAW + "67-red-wall-arch.png", OUT + "60-there-is-a-door.jpg",
      "THERE IS", "A DOOR.", "Most brands bring a ladder",
      "The opening is usually already there. Complexity is what people build when they "
      "have not found it yet.",
      "We look for the door first.", bar_word="Then we walk through it")

# ── Third-party reference photos — INTERNAL TEST ONLY, rights not cleared ──
build("label", RAW + "68-tv-sneakers.jpg", OUT + "61-obsolete.jpg", "Obsolete",
      [("Medium", "Cathode ray, borrowed time"), ("Condition", "Still switched on"),
       ("Provenance", "Every living room, 1994"),
       ("Status", "The habit outlived the hardware")],
      "The screen changed. What makes somebody stop did not. We build for the stop.",
      cat_no="PM-021")

build("outline", RAW + "69-blur-chair.jpg", OUT + "62-dont-sit-this-out.jpg",
      "DO NOT SIT", "THIS ONE OUT.", "The chair is always there",
      "Waiting feels responsible right up until the moment someone else owns the "
      "position.",
      "Comfort is a slow decision.", bar_word="Move while it matters")

build("tape", RAW + "70-cup-aviators.jpg", OUT + "63-show-up.jpg",
      "SHOW UP", "LIKE YOU MEANT IT.", "Presence is a decision",
      "Independent. Selective.",
      "Presence is a choice you make long before anyone is watching.",
      "Confidence reads. So does hesitation.")


# ── LONGEBLACK ─────────────────────────────────────────────────────────────
build("lb_hero", RAW + "38-ossara.png", OUT + "36-ossara.jpg",
      "Ossara", "A brand built by PivtMedia",
      "Scent, packaging and story. Built once, properly.")

build("lb_hero", RAW + "40-soundstage-bw.png", OUT + "38-pivtmedia-stage.jpg",
      "PivtMedia", "Production, direction, distribution",
      "The room is booked. The plan came first.")

build("lb_hero", RAW + "42-product-set.png", OUT + "40-built-here.jpg",
      "Built here", "Studio, strategy and spend under one roof",
      "Nothing gets handed off halfway.")

build("lb_hero", RAW + "43-content-studio.png", OUT + "41-the-quiet-part.jpg",
      "The quiet part", "Planned, lit, shot, cut, measured",
      "The unglamorous work is most of the work.")

build("lb_hero", RAW + "54-boutique-studio.png", OUT + "49-in-order.jpg",
      "In order", "Kit, crew, calendar, budget",
      "Chaos is expensive. We took it out of the process.")

build("lb_frame", RAW + "48-bone-silk.png", OUT + "45-restraint.jpg",
      "PivtMedia — est. principles", "Restraint", "is the whole craft.",
      "Anyone can add. Knowing what to leave out is the part that takes years.",
      "Strategy · Content · Systems")

# ── PRACTICE NOTES (lb_statement) — a running numbered series ──────────────
# head_y is chosen per image: put the headline where the DARK even zone actually is.
build("lb_statement", RAW + "39-grand-room.png", OUT + "37-the-long-view.jpg",
      PN + "01", "The long|view.",
      "We take on fewer brands than we are asked to, and stay with them longer than "
      "most agencies last.", "PivtMedia")

build("lb_statement", RAW + "41-grid-bw.png", OUT + "39-nothing-by-accident.jpg",
      PN + "02", "Nothing here|is an accident.",
      "Every light was placed. Every frame was argued about. That is the part you are "
      "paying for.", "PivtMedia")

build("lb_statement", RAW + "57-boardroom.png", OUT + "52-quiet-room.jpg",
      PN + "03", "Everything expensive|starts in a quiet room.",
      "The work people notice is decided long before anyone opens a camera bag.",
      "PivtMedia", head_y=0.60)

build("lb_statement", RAW + "61-modern-library.png", OUT + "53-chosen-twice.jpg",
      PN + "04", "Every word here|was chosen twice.",
      "Copy is not decoration. It is the part of the brand people actually repeat.",
      "PivtMedia", head_y=0.605)

build("lb_statement", RAW + "62-modern-library-alt.png", OUT + "53b-chosen-twice-alt.jpg",
      PN + "04", "Every word here|was chosen twice.",
      "Copy is not decoration. It is the part of the brand people actually repeat.",
      "PivtMedia", head_y=0.655)

build("lb_statement", RAW + "49-santorini.png", OUT + "46-best-rooms.jpg",
      PN + "05", "The best rooms|are never crowded.",
      "We would rather be worth waiting for than easy to book.",
      "PivtMedia", head_y=0.185)          # dark zone is the SEA, up top

build("lb_statement", RAW + "50-monaco.png", OUT + "47-quiet-money.jpg",
      PN + "06", "Quiet money|moves slowly.",
      "The brands that last are built at a pace that looks like patience and is "
      "actually discipline.", "PivtMedia", head_y=0.60)

build("lb_statement", RAW + "53-marble-desk.png", OUT + "48-strategy-before-shutter.jpg",
      PN + "07", "Strategy|before shutter.",
      "The camera is the last decision, not the first. By the time it comes out, "
      "everything has already been argued.", "PivtMedia", head_y=0.615)

build("lb_statement", RAW + "55-desert-villa.png", OUT + "50-nothing-grows-here.jpg",
      PN + "08", "Nothing grows here|by accident.",
      "Harsh markets reward the same thing harsh landscapes do: preparation, not "
      "enthusiasm.", "PivtMedia", head_y=0.615)

build("lb_statement", RAW + "56-alpine-lodge.png", OUT + "51-the-view-costs-the-climb.jpg",
      PN + "09", "The view costs|the climb.",
      "Every brand that looks effortless from below took a season of unglamorous work "
      "to get there.", "PivtMedia", head_y=0.575)   # dark zone is the charred timber

build("lb_statement", RAW + "59-billboard.png", OUT + "54-space-is-easy.jpg",
      PN + "10", "The space is easy.|The message is not.",
      "Anyone can buy the placement. Deciding what deserves to go on it is the actual "
      "work.", "PivtMedia", head_y=0.615)

build("lb_statement", RAW + "60-archive.png", OUT + "55-campaigns-end.jpg",
      PN + "11", "Campaigns end.|Reputations compound.",
      "Judge the work by what it leaves behind, not by how it performed in week one.",
      "PivtMedia", head_y=0.60)

build("lb_statement", RAW + "47-green-corridor.png", OUT + "44-say-no-more.jpg",
      PN + "12", "We say no|more than we say yes.",
      "A full roster is not a good sign. It means someone stopped choosing.",
      "PivtMedia")


# ── CAROUSEL 01 — "Nobody reads" (4 slides, swipe in order) ────────────────
# A carousel is the ONE case where the "different layout per batch" rule is
# inverted: every slide uses the SAME layout and geometry so the swipe feels
# continuous. Only the image and the line change.
# Arc: premise → failure → consequence → answer.
CAROUSEL = [
    ("66-reader-cut.png", "C1-nobody-reads.jpg",
     "NOBODY READS.", "EVERYONE SCANS.",
     "write for the three seconds you actually get",
     "Built to be understood at a glance."),
    ("71-chair-cut.png", "C2-at-the-fold.jpg",
     "YOU LOSE THEM", "AT THE FOLD.",
     "the second half is a rumour",
     "Front-load it or lose it."),
    ("72-walking-cut.png", "C3-do-not-come-back.jpg",
     "THEY DO NOT", "COME BACK.",
     "there is no second first impression",
     "One pass is all you get."),
]
for src, dst, l1, l2, spread, foot in CAROUSEL:
    build("overlap", RAW + src, OUT + dst, l1, l2, spread, foot,
          "PivtMedia visual direction.")

# Slide 4 deliberately BREAKS the pattern so a viewer knows the set has ended: the field
# inverts to ink, the photograph is gone, and the wordmark takes the space the subject
# occupied. Same typographic system, opposite treatment.
from poster7 import poster_endcard                                        # noqa: E402
poster_endcard(OUT + "C4-lead-with-the-point.jpg",
               "SO LEAD WITH", "THE POINT.",
               "say it before they decide not to care",
               "Start with the answer.", "PivtMedia visual direction.")

print("\nAll posters rebuilt.")

build("receipt", OUT + "111-you-keep-the-time.jpg", "Itemised.",
      [("Strategy", "Included"), ("Art direction", "Included"), ("Production", "Included"),
       ("Edit + delivery", "Included"), ("Guesswork", "Removed"),
       ("Second-guessing", "Removed")],
      "You keep", "THE TIME.",
      "Every line on this slip is something you stop doing yourself.", bg=(255, 92, 0))

build("knockout", RAW + "112-paper-offcuts.png", OUT + "112-edit.jpg",
      "EDIT.", "What you cut is the work.",
      "Anyone can add. The difference between a feed and a brand is everything that "
      "never made it in.",
      "Less, on purpose.", sub_bar=(17, 17, 17))

build("lb_statement", RAW + "113-limestone-gallery.png", OUT + "113-nothing-goes-up.jpg",
      PN + "13", "Nothing goes up|until it is ready.",
      "We would rather show you one finished thing than ten almost-finished ones.",
      "PivtMedia", head_y=0.70)   # dark zone is the polished floor
