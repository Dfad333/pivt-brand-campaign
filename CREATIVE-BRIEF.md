# PivtMedia — Social Poster System
### Creative brief & production method (handoff for content team)

Everything below describes how the approved PivtMedia campaign posters are made. Follow the
method, not just the look — most failures come from skipping step 1.

---

## 1. THE CORE METHOD (most important section)

**These are not "AI images". They are designed posters that happen to use an AI-generated
photograph as one ingredient.**

The workflow is always:

1. **Generate ONLY the photograph** in an image model (we use Higgsfield / Nano Banana Pro,
   4:5, 4K). The image is generated **completely text-free**.
2. **Build the poster in a layout tool** (Figma, Photoshop, Canva, or code). All typography,
   colour blocks, rules, micro-copy and the logo are set here.

**Never ask the image model to render the headline.** It gets spelling right maybe 90% of the
time but the *typeface* drifts unpredictably — we once asked for a geometric sans and got a
Trajan-style serif, which read as a completely different brand. Setting type in the layout
tool also means any line can be rewritten later without regenerating the image.

The only exception: text that genuinely belongs to the scene (e.g. lettering painted on a
concrete wall). Even then, check it letter by letter.

---

## 2. NON-NEGOTIABLE BRAND CONSTANTS

| Item | Value |
|---|---|
| Canvas | **1600 × 2000 px (4:5)** — Instagram feed's largest real estate |
| Accent | **`#FF5C00`** orange — the only saturated colour in most posters |
| Ink | **`#121212`** near-black |
| Paper | **`#F7F5F1`** warm cream |
| Headline face | Helvetica Now / Neue Haas Grotesk Display **Bold** (Arial Bold as substitute) |
| Headline tracking | **−2%** (tight) |
| Micro-copy | Same family, ~19–20px, **+1.5 letterspacing**, ALL CAPS |
| Logo | PivtMedia barcode lockup, ~13% of canvas width |

**Logo files** live in `Pivt Media Logos/campaign-overlay/`:
`pivt-logo-transparent-black.png` (light backgrounds) · `pivt-logo-transparent-white.png`
(dark backgrounds) · plus flattened on-white / on-black versions.

Logo sits **top-centre** or **bottom-centre** depending on layout. Always keep the orange
accent bar in the barcode — never recolour the mark to flat black or flat white.

---

## 3. THE LINEAGE — what we're actually imitating

We studied two reference accounts. **Only one is approved.**

### ✅ BOEGÖW (@boegow) — THIS IS THE DIRECTION
Brutalist Swiss **editorial poster** design. Type is the hero; the photograph is subordinate.

- Huge condensed grotesque headline, usually broken over two lines
- Short declarative sentences **ending in full stops** — "STRIPPED BACK." / "DIALED IN."
- B&W photography used as a cropped block or full-bleed element — often abstract
- ONE neon accent used as a **solid geometric shape** (square, circle, tape), not as a tint
- Clusters of tiny 6–8pt micro-copy floating in corners
- Hairline rules; bracketed fragments — `[ NO GUESSWORK ]`
- Small wordmark bottom-centre

Their neon green maps directly onto our `#FF5C00`.

### ✅ LONGEBLACK (@longeblack) — ALSO APPROVED (after a legibility fix)
Quiet cinematic luxury. The opposite register to BOEGÖW — use it deliberately, not by blending.

**The DNA — these are what make it LONGEBLACK, and they never change:**
- **Thin, widely letterspaced, centred** headline — a brand name or short phrase. Small
  relative to the frame. (Segoe UI Light / Helvetica Neue UltraLight, ~24% letterspacing.)
- Cinematic photography with **real depth and tonal richness** — deep shadow, luminous
  highlights, a sense of atmosphere. Never flat or graphic.
- ™ and ® used deliberately
- A discreet endorsement lockup beneath the name — "A BRAND BUILT BY PIVTMEDIA"
- A short orange rule as a divider, and a bracketed wordmark to close
- Copy voice is **exclusivity and restraint**, not urgency
- Generous empty space; nothing shouts

> **The palette is a VARIABLE, not part of the lineage.** LONGEBLACK's own feed happens to be
> warm amber because of the clients they serve. Do **not** lock our version to it — if every
> post is amber the grid becomes monotonous. Rotate deliberately.

**Approved palette variants** — pick per post, and don't run two of the same back to back:

| Variant | Description | Type colour |
|---|---|---|
| **Warm amber** | Honey-gold, caramel, deep chocolate. Candlelight, atelier, interiors. | White |
| **Black & white** | Rich cinematic mono — deep blacks, luminous highlights, real depth. **Not** the flat high-contrast graphic B&W used in BOEGÖW. | White |
| **Cool stone / concrete** | Neutral greys, plaster, limestone, overcast light. Calm and architectural. *(Neutral grey only — electric blue as a flat field is banned, see §4.)* | White or ink |
| **Deep green** | Forest, moss, dark foliage, bottle-glass. Works for wellness, spirits, outdoor. | White |
| **High-key bone** | Pale cream and off-white, soft daylight, airy. The inverse mood — light instead of dark. | **Ink, not white** |

> ⚠️ On **high-key bone** and other light grounds the whole contrast logic flips: use dark ink
> type, and the gradient in the type zone must **lighten** the area rather than darken it.
> The rule is not "white type" — it is "measure the ground and pick the ink that survives".

> ⚠️ **This style failed on the first attempt and the reason matters.** Thin letterspaced type
> was dropped straight onto busy photography and vanished. **The fix is compositional, not
> typographic:**
> 1. In the image prompt, explicitly reserve a **calm, tonally even, empty zone** where the
>    type will go — and demand a **gradual light falloff with no hard edge or band**. Ask for
>    a "band" of darkness and the model will render a literal black rectangle.
> 2. In layout, deepen that zone with a **soft gaussian gradient**, never a hard-edged plate.
>    It should read as natural light falloff.
> 3. **Measure it.** Mean luminance under the headline should be **under ~70** for white type.
>    Don't eyeball this.

**Two LONGEBLACK formats:**
- **Brand hero** — client or brand name centred upper-third, ™, endorsement lockup, logo,
  orange rule, closing line at the bottom.
- **Statement piece** — no brand name. Small label and rule top-left, wordmark top-right,
  thin headline in the lower-middle, orange rule, two lines of body, bracketed wordmark.

**When to use which lineage:**

| Use BOEGÖW when… | Use LONGEBLACK when… |
|---|---|
| PivtMedia is speaking as itself | Presenting a client or a brand |
| The message is the product | The atmosphere is the product |
| Stark, high-contrast, loud type | Warm, cinematic, quiet type |
| Manifesto / statement posts | Case studies, launches, brand reveals |

---

## 4. HARD RULES (learned the hard way — each of these caused a rejected batch)

1. **No generated humans — with one worked exception.** No faces, no figures, no models.
   Anonymous figures with faceted geometric masks were tried and also rejected. Default to
   abstract texture, landscape, architecture, materials, single objects, or pure typography.
   **The exception that works: a figure whose face is fully concealed by a prop** — the
   seated reader holding an open newspaper over their head. Nothing resembling a person is
   generated, but the image still has human energy. Partial figures (hands, legs, a foot,
   a back) are also fine.
2. **Never copy a reference's concept.** Take the *aesthetic*, invent the *idea*. Our first
   round reproduced the reference compositions too literally and was rejected on sight.
3. **Every poster in a batch must use a DIFFERENT layout.** Repetition of arrangement gets
   noticed far faster than repetition of subject. **Carousels invert this rule** — every
   slide keeps the same layout and geometry so the swipe feels continuous; only the image
   and the line change. See §11.
4. **Orange is the only accent.** Blue as a large flat colour field was explicitly rejected.
   Secondary colours are fine *inside* a treatment (e.g. a two-colour halftone) but never as
   a dominant block.
5. **Prefer light/high-key over dark and moody.** Early dark versions were sent back as "very
   dark". Keep the orange fully saturated regardless.
6. **Never render a real manufacturer's logo** (Sony, Canon, etc.). It implies a partnership
   we don't have, and models garble logos anyway. Prompt equipment as "completely unbranded".
7. **Check every piece of small text against its background.** See §7.
8. **Never request "shallow depth of field"** on desk or still-life scenes — it reads as
   blurry and got a poster sent back. Use "everything sharp front to back, deep depth of
   field, no blur, shot at a small aperture", and negative out blur/bokeh.
9. **"Production set" means boutique, not warehouse.** A designer's private studio — polished
   concrete, a marble plinth, one elegant softbox — not flight cases and scaffolding. Say
   "NOT a warehouse, NOT a film stage" in the prompt or it drifts industrial every time.
10. **Craft subjects must read MODERN, not heritage.** A letterpress workshop was rejected as
   antique. Add "contemporary design, NOT antique, NOT traditional or classical".
11. **Never invent facts** — no client counts, percentages, revenue figures. Positioning only.
12. **Don't put solid-shape layouts on portraits.** `disc` and `knockout` place their shape
   centre-frame; on a face-forward image they land on the face and destroy the photograph.
   For portraits use `tape` (headline low) or `label` (photo inset).
13. **Third-party images need rights cleared.** Found/reference photos may carry an
   identifiable face and other companies' marks. Fine for internal tests, not for posting.

---

## 5. THE LAYOUT LIBRARY

Ten approved arrangements. Pick a different one each time.

| # | Layout | Structure |
|---|---|---|
| 1 | **Split** | Photo top ~54%, huge headline on paper below, accent square straddling the seam, micro-copy row under a hairline. *(Now over-used — rest it.)* |
| 2 | **Disc** | Full-bleed abstract, big orange circle centred holding the logo + bracketed fragments + body line. |
| 3 | **Tape** | Full-bleed B&W, huge white headline low, rotated orange "tape" strip with small black text. |
| 4 | **Index** | Paper ground, hairline grid, small inset photo, centred headline, numbered index rows (01/02/03) with orange numerals. |
| 5 | **Outline** | Full-bleed B&W. Line 1 solid white, **line 2 outline-only** (stroke, no fill). Vertical type up the left edge, orange bar. |
| 6 | **Duotone** | Greyscale photo mapped onto a two-colour ramp (dark shadow colour → orange highlight). Cream headline. |
| 7 | **Riso** | Two halftone dot screens, deliberately misregistered ~7px, printed on cream. Reads as real two-colour print. |
| 8 | **Stat / Word** | **Type only, no photograph.** A giant numeral or single word on a flat colour field, with numbered annotations. Cheapest and fastest format to produce. |
| 9 | **Catalogue label** | Gallery-specimen layout: plate in generous white space, then a label with MEDIUM / CONDITION / PROVENANCE rows. The quiet one. |
| 10 | **Overlap** | Headline at the **top**; subject **cut out and layered over the type** so it interrupts the letterforms; micro-line justified edge-to-edge; bracketed credit closes it. |
| 11 | **LB Brand hero** | *LONGEBLACK.* Full-bleed warm photo, soft gradient in the upper third, thin letterspaced brand name + ™, endorsement lockup, logo, orange rule, closing line. |
| 12 | **LB Statement** | *LONGEBLACK.* Full-bleed warm photo, label + orange rule top-left, wordmark top-right, thin headline lower-middle, orange rule, body lines, bracketed wordmark. |
| 13 | **Scatter** | Pale field, three small captioned plates placed **off-grid** at different heights, orange connector dots, vertical side label, headline floating low-right with body beneath. Editorial moodboard feel. |
| 14 | **Window** | Flat saturated colour field with a large **circular window** cut through it revealing a vivid photograph. Bracketed kicker above, two-tone headline below. Inverse of the Disc layout. |
| 15 | **LB Frame** | *LONGEBLACK.* Invitation-card device: a hairline rectangle inset from the edges with a small label **breaking the top rule**, thin letterspaced type stacked inside, orange rule, body, closing detail line and logo inside the bottom of the frame. The quietest, most ceremonial layout. Works on light or dark grounds — ink and gradient both invert automatically. |

### Not a layout — `studio/mockup.py`
Places a **finished poster INTO a photograph** as a physical print, the reverse of every
other module. Generate a room containing a genuinely blank poster ("CRITICAL: completely
blank, nothing printed on it"), run `probe()` to overlay a coordinate grid, read the four
corners off it, then `place(scene, poster, out, corners, shade, warm)`. Pure-Python
homography, no numpy. **Status: works, but its one output was rejected — unproven.**

> **PRACTICE NOTES is a running series, not a one-off.** The LB Statement layout with a
> "PRACTICE NOTES — NO. 0X" label top-left has been repeatedly singled out as a favourite.
> Keep numbering sequentially and vary the palette each time. Issued so far: no. 01 warm
> stone interior · no. 02 B&W lighting grid · no. 03 (scatter variant) · no. 04 deep green.

**Not yet built** (next new device, from BOEGÖW's `h-aug10` post): an asymmetric **scatter /
collage** — several small captioned image plates placed off-grid on a pale field, connector
bullet-dots, vertical side text, headline floating in open space.

---

## 6. IMAGE PROMPT RECIPE

Structure every prompt as:

```
[Shot type] + [subject] + [lighting] + [tonal description] +
"Completely monochrome, absolutely no colour" (when B&W) +
[texture: "rich analogue film grain"] + [quality: "museum-grade", "ultra high detail"] +
[composition note reserving space for type] +
NEGATIVE BLOCK
```

**Always append this negative block:**

> Negative: no text, no lettering, no typography, no captions, no watermarks, no logos, no
> numbers, no letters, no readable writing of any kind, no colour, no people, no figures,
> no faces, no hands, no clutter, no border, no frame, no white margin.

**Reserve space for the type in the prompt itself** — e.g. *"the top fifth of the frame is
clean empty dark space with nothing in it"*. This is what makes the headline sit comfortably
instead of fighting the picture.

**Proven subjects — BOEGÖW** (all B&W, non-human): ink diffusing in water · crumpled metallic
foil · macro of stacked paper edges · storm clouds · aerial sand dunes · brutalist concrete
geometry · spiral stairwells · single sculptural objects on seamless · macro lens elements.

**Proven subjects — LONGEBLACK** (non-human). Note the palette changes per post — see §3:
- *Warm amber:* amber apothecary glass by candlelight · craftsman's atelier in lamplight ·
  candlelit private dining room · vast stone interior with honey light raking the floor
- *Black & white:* empty film soundstage with a lit cyclorama · overhead lighting grid with
  haze beams · empty theatre · rain on glass at night
- *Cool stone:* plaster and limestone interiors under overcast light · gallery spaces
- *High-key bone:* pale studio corners, sheer fabric, soft daylight

**Palette instruction goes in the prompt, and must match the variant you chose.** For warm:
*"Warm amber and deep brown palette only, absolutely no blue, no green, no cool tones."*
For B&W: *"Completely monochrome, absolutely no colour"* plus *"cinematic tonal depth, rich
blacks and luminous highlights — not flat or graphic"* (this last clause is what keeps B&W in
the LONGEBLACK register rather than drifting into BOEGÖW's harder look).

Always add the falloff instruction from §3.

### Mockup brands
Inventing a fictional brand for a template demo is fine and often better than using a real
client. **Check the name isn't a real trademark before anything goes public** — we already hit
this once by reaching for a plausible-sounding name that turned out to be an actual hotel
group. Prefer invented, non-descriptive names.

---

## 7. QA CHECKLIST — run before every post goes out

- [ ] **Measure, don't eyeball.** `mean_lum` under a white headline should read **< ~70**.
      Every approved poster clears this; the rebuild script prints the number for each.
- [ ] **Zoom in on every text element.** Small white type placed without checking the
      background underneath is our single most common defect. If a caption crosses a
      light/dark boundary, either move it, add a gradient scrim, or give it a subtle outline.
      A mean-based ink choice **cannot** save text crossing a high-contrast edge — a bright
      window ate the middle of a label once. That case needs a stroke halo, not a colour flip.
- [ ] **Check all four image edges SEPARATELY.** The generator intermittently adds a 25–55px
      border artifact — often on **one side only**, which a general check misses. Compare each
      edge's value against the pixels just inside it.
- [ ] **Check headline vs. footer collision.** A short headline can auto-scale up until it
      overruns the rule below it. Cap the size against available space.
- [ ] **Confirm the accent is the only saturated colour** — count saturated pixels of the
      banned hue if unsure. A "desk lamp" once came back as a green banker's lamp despite a
      warm-only instruction. Neutral snow reading ~18% cool is fine; a green lampshade is not.
- [ ] **Confirm no faces, no legible brand names, no garbled lettering** anywhere in frame.
- [ ] **View it at thumbnail size.** If the headline isn't readable at 200px wide, it fails.

**The type layers are now self-defending.** Most layouts measure their own ground and adapt:
`lb_statement` (headline zone, label + wordmark, closing tag — three independent zones, plus a
stroke halo on the label), `lb_frame` (inverts ink *and* flips its gradient to lighten on pale
grounds), `outline`, `tape`, `knockout`, `split`. That is a safety net, not a substitute for
looking — compose a genuinely clean zone for the type in the *prompt* first.

---

## 8. COPY VOICE

Short. Declarative. Ends in a full stop. The image should *argue* the line, not decorate it.

Approved examples:
> NO NOISE. JUST SIGNAL. · PROOF. NOT PROMISES. · MOVE FIRST. EXPLAIN LATER. ·
> EVERYONE BUILT THE SAME BUILDING. · SLOW IS FINE. DRIFTING ISN'T. ·
> REACH IS NOT DEMAND. · [ FEWER CLIENTS ] [ BETTER WORK ] · LATER. · 3 SECONDS.

Supporting micro-copy is one or two sentences, plain, slightly blunt, no marketing padding.

**Do not invent factual claims** — no client counts, no percentage lifts, no revenue figures
unless someone supplies real numbers. Positioning statements only.

---

## 9. THE PRACTICE NOTES SERIES

The single most-praised format. It is the **LB Statement** layout with a
`PRACTICE NOTES — NO. 0X` label top-left. Treat it as a running numbered series: keep
incrementing, and **change the palette every issue**.

| # | Subject | Palette |
|---|---|---|
| 01 | Vast empty stone interior, honey light | Warm |
| 02 | Overhead studio lighting grid, haze | B&W |
| 03 | Empty executive boardroom | Neutral |
| 04 | Contemporary penthouse library | Warm |
| 05 | Santorini caldera terrace | Aegean gold + blue |
| 06 | Riviera harbour at dusk, superyachts | Amber dusk |
| 07 | Marble desk, camera, leather portfolio | Warm |
| 08 | Desert modernist villa, reflecting pool | Sand / terracotta |
| 09 | Alpine lodge, charred timber, snow | Cool neutral |
| 10 | Blank billboard at dusk | Cool slate |
| 11 | Archive of blank-spined volumes | B&W |
| 12 | Green marble corridor | Deep green |

**`head_y` must be chosen per image.** The default assumes a dark lower-middle. On the
Santorini shot the bright plaster was below and the dark sea above, so the headline moved to
`head_y=0.185`. Always look at where the dark even zone actually is.

**What works as a subject:** modern architecture set in natural scenery, and rooms that say
something about how an agency works (boardroom, library, billboard, archive). Landscape alone
is too generic; heritage craft reads antique.

---

## 10. CAROUSELS

A carousel is a **narrative**, not four posters side by side. Lock the layout and geometry
across every slide — same template, same `obj_h` / `obj_bottom` / `spread_y` — so swiping
feels like one continuous piece. Only the image and the headline change.

**The arc that works: premise → failure → consequence → answer.**

*Carousel 01 — "Nobody reads"* (`overlap` layout, cream ground, cutout subjects):

| Slide | Image | Line |
|---|---|---|
| 1 | Seated, reading behind a blank paper | NOBODY READS. EVERYONE SCANS. |
| 2 | Empty chair, paper dropped on the floor | YOU LOSE THEM AT THE FOLD. |
| 3 | Figure walking away, paper over face | THEY DO NOT COME BACK. |
| 4 | Figure facing camera, presenting the page | SO LEAD WITH THE POINT. |

Two craft notes. **Direction of travel matters** — the slide-3 figure walks rightward, which
pushes the eye toward the next slide. And the **final slide should resolve, not repeat**:
here the subject stops hiding behind the page and presents it.

Every subject is a cutout on the poster's own cream ground, so the four read as one set.
Use Higgsfield `remove_background` — it takes an uploaded `media_id` or a generation
`job_id`. A local flood-fill would eat the cream paper, which is the whole subject.

---

## 11. MOTION PIECES

Same method as a poster, one extra step: **generate the still text-free → animate the still →
burn the type over the clip.** Never prompt a video model for the headline; it garbles
letterforms *and* wobbles them frame to frame.

`studio/motion.py` is the module. Unlike every other layout it returns the type as a
**transparent RGBA layer** rather than a flattened JPG, so the same artwork can be composited
over video with ffmpeg:

```python
from motion import type_layer
type_layer("overlay.png", 1080, 1340, headline="CONTENT ON TAP.",
           foot="PIVT + MEDIA //", ink=(17,17,17), foot_bar=INK)
```

```bash
ffmpeg -i raw.mp4 -i overlay.png -filter_complex "[0:v][1:v]overlay=0:0" -c:v libx264 -crf 17 -pix_fmt yuv420p out.mp4
```

**Model notes (checked 2026-08-15).** Kling on our account only offers **16:9 / 9:16 / 1:1 —
no 4:5**, so it cannot hold the feed format. Use **`minimax_h3` with `aspect_ratio:"auto"`**
(derives the ratio from the start frame — returned a true 1440×1792) or **`minimax_hailuo`**
(1080×1340). Both take the still via `medias: [{role:"start_image", value:<job_id>}]`. The
video tools may refuse a submission and recommend a preset instead — retry the same call with
`declined_preset_id` set to the id in the error.

**Quote the credit cost before generating anything** (Tarek, 2026-08-15). `generate_image` and
`generate_video` accept `get_cost: true`, which returns the cost without submitting a job — run
it, state the number, then generate. The `*_batch` tools do **not** support `get_cost`, so
preflight one representative request and multiply. Baseline: Nano Banana Pro still (4:5, 4k)
= 4 credits · Hailuo 2.3 ~6s = 10 · MiniMax H3 ~6.6s = 24. Rerolls cost full price — price a
reroll before firing it.

**Default duration is 10 seconds** (Tarek, 2026-08-15 — the first piece ran 6s and he wanted
longer). `minimax_h3` accepts 4–15; `minimax_hailuo` accepts only 6 or 10. Expect the longer
run to strain the accumulation: models tend to stall the motion in the back half, so check the
midpoint *and* the end, and watch that the growing element doesn't overrun its container.

**Prompt the motion in one sentence and negate the camera.** "Locked-off static camera, no
zoom, no pan, no push" plus the single thing that should move. Long motion prompts make these
models invent camera moves. The two failure modes to check on every take: the hero object
slowly deforming, and the accumulating element **not actually accumulating** — the model loops
the motion without adding volume, which kills the whole idea.

> ⚠️ **The type-contrast rule is harder in motion: the ground moves.** Measure the type band on
> the **first and last** frames, not just the first. On the tap piece every candidate footer
> band swung 50–110 luminance as the coil grew, so no fixed ink survived the clip — and the
> mean said "fine" while the line was actually sitting on diagonal stripes. **The fix is a
> solid bar**, not an ink flip: `foot_bar=INK` gives the line its own ground on every frame,
> and a solid accent shape is the house device anyway. An ORANGE bar was tried first and
> rejected — it melts into the orange wall. Ink reads.

## 12. ASSET LOCATIONS

- `brand-campaign/final/` — 47 approved posters
- `brand-campaign/archive/` — 12 rejected, with `WHY-ARCHIVED.md` explaining each
- `brand-campaign/raw/` — untouched source photographs (so type can be re-set without
  regenerating). **Never delete these.**
- `brand-campaign/CONTACT-SHEET.jpg` — every approved poster at a glance
  (regenerate: `python studio/contact_sheet.py`)
- `brand-campaign/references/` — `REFERENCES.md` (BOEGÖW + LONGEBLACK decoded),
  `DRIVE-FOLDER.md` (the third, retro-editorial set), and the BOEGÖW images in `boegow/`
- `brand-campaign/motion/` — motion pieces: `raw-*.mp4` (untouched model output),
  `overlay-*.png` (transparent type layers), and the finished burned clips
- `brand-campaign/studio/` — the code. `layouts.py` is the entry point;
  `motion.py` handles video type layers.
- `brand-campaign/studio/recipes/rebuild_all.py` — **every poster, reproducible in one run.**
  Change a headline there and re-run; it re-composites type only, so it costs nothing.
- `Pivt Media Logos/campaign-overlay/` — the four logo variants
- `.claude/commands/pivtcontent.md` — the scoped entry point; run `/pivtcontent` to start
