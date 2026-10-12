# Third reference set — Google Drive "PIVT CONTENT › references"

`https://drive.google.com/drive/u/7/folders/1Y8MY_c5HqluxejfeoiAmUkOLAdKTdpDF`
Owner: hazemelgazzar20@gmail.com · 15 images · reviewed 2026-08-03

**Access note:** these files are auth-gated. A plain download returns a Google sign-in page,
and Drive's `read_file_content` returns nothing for photographs. Viewing them via base64
costs roughly 12–40k tokens *each*. The cheap route is the **claude-in-chrome** browser —
open the folder in the signed-in session and screenshot the thumbnail grid.

---

## What's in it

A **bright, saturated, playful retro-editorial** world — a real departure from the moody
luxury of the BOEGÖW/LONGEBLACK sets.

- **Surreal colour-blocked scenes** — navy sky with a single cloud over crimson ground, a
  white vintage car, an arched doorway; a lone bench on a green hill against flat blue
- **Retro editorial portraits** — tan suit against yellow curtains on a corded phone;
  aviators in a teal room; Robert Evans on a red telephone
- **Pastel product still lifes** — a sneaker resting on a small brown TV; a gold sneaker and
  red sock on a wooden box; close-packed cream tennis balls
- **Print/poster mockups in situ** — a poster on a black leather sofa; a framed
  "First, Concept then Design" print on a red chair; an "odd ritual" newspaper held open
- **A typographic collage** — torn paper, "this is trash"

## Direction agreed with Tarek

| Decision | Choice |
|---|---|
| People | **Partial figures only** — hands, legs, a foot, a back. No faces. |
| Directions to build | Surreal colour-blocked · poster mockups in situ · pastel product still lifes |
| Palette | **Expanded** — crimson, navy, mustard, teal as full grounds, orange kept as the brand accent |

Retro editorial portraits were *not* selected (leans hardest on faces).

## First outputs

- `57-wait.jpg` — mustard/teal colour block, **knockout** layout (revived from archive)
- `56-mockup-later.jpg` — the LATER poster placed into a real room via `studio/mockup.py`
- `58-balance.jpg` — pastel stack, **window** layout on a full orange field

## New capability this unlocked

`studio/mockup.py` places a finished poster **into** a photographed scene as a physical
print — the reverse of every other module, which put type onto a photo. Generate a room with
a genuinely blank poster ("CRITICAL: completely blank, nothing printed on it"), run
`probe()` to get a coordinate grid, read the four corners off it, then `place()`. Pure-Python
homography, no numpy.
