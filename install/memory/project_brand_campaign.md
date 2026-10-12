---
name: project-brand-campaign
description: "PivtMedia's own premium brand-campaign image pipeline — Higgsfield generation plus local logo/tagline compositing, and the corrected logo overlay asset set"
metadata: 
  node_type: memory
  type: project
  originSessionId: e834e237-b716-4dcd-84af-e9644bb7821d
  modified: 2026-08-05T02:21:00.579Z
---

Started 2026-08-02: a premium brand campaign for PivtMedia itself (not a client). Visual
language is drawn from two reference posts — (a) dark high-contrast B&W analogue still-life
with a single orange accent, (b) minimalist cream negative-space compositions — both with the
barcode lockup top-centre and a short aphoristic tagline.

**Working method Tarek asked for:** generate a maximum of 2 images per round in Higgsfield →
he approves → *then* the logo is composited locally, never inside Higgsfield (so the mark
isn't mangled). Imagery is generated deliberately **text-free**; the logo and tagline are set
typographically afterward, which keeps the type razor-sharp and avoids AI letterform artifacts.

**Generation settings that worked:** Higgsfield `generate_image`, model `nano_banana_pro`
(resolves to nano_banana_2 server-side), `aspect_ratio: "4:5"`, `resolution: "4k"`. Note
`gpt_image_2` does NOT support 4:5. Always append a long negative clause ("no text, no
lettering, no typography, no captions, no watermarks, no numbers…") — it works reliably.

**Logo asset gotcha:** `pivt-media-portal/src/assets/logo-barcode-white.png` is misnamed — it
is black-on-white RGB with no alpha, NOT a white-ink logo. The only true master is
`logo-barcode.png` (RGBA, 900x560, ink `#121212`, accent `#FF5C00`). The corrected overlay set
now lives at `E:\PivtMedia\Pivt Media Logos\campaign-overlay\`:
transparent-black, transparent-white, on-white, on-black.

**Layout constants matched to the references:** logo width ≈13% of canvas width, top margin
≈5%, tagline ≈1.7% of width with ~16% letterspacing, output 1600x2000. Typeface is
Bahnschrift (Windows' DIN-style grotesque) — closest available match to the reference type.

Campaign files: `E:\PivtMedia\brand-campaign\raw\` (Higgsfield originals) and `final\`
(composited). Compositing script is `compose.py` in the session scratchpad — worth promoting
into the repo if the campaign continues.

**Direction feedback from Tarek (2026-08-02), applies to all future rounds:**
1. References are for *aesthetic* only — he does NOT want the concepts reproduced. Round 1
   (loupe on contact sheet, lone figure in negative space) was rejected as "kind of look
   identical to the ones I gave you." Bring genuinely new subject matter each time; keep only
   the DNA — monochrome + single orange accent, editorial restraint, aphoristic tagline that
   the image itself argues for.
2. He prefers a **light / high-key palette** over dark moody grading. Dark versions were
   "very dark"; bright pale concrete and cream backgrounds were approved. Keep the orange
   fully saturated regardless.
3. Orange must be the *only* colour — he asked for a re-roll purely to remove an incidental
   blue-grey tint in window glass. Add explicit "no blue, no cyan, no colour tint anywhere
   except the accent" negatives.
4. Type policy is **mix, decided per image**: in-image Higgsfield text when the type belongs
   to the scene (e.g. lettering on a concrete wall), locally-composited type when it's a
   clean overlay floating in negative space.

**Approved round-2 concepts:** "EVERYONE BUILT THE SAME BUILDING" (modernist facade grid, one
orange window) and "STRATEGY IS THE STRAIGHT LINE" (macro thread tangle, one straight orange
thread).

**MAJOR DIRECTION CHANGE (2026-08-02, later in same session).** Tarek rejected all
photography-led rounds and pointed to **instagram.com/boegow** ("Connecting What Matters",
boegow.com) as the real target aesthetic. That account is NOT premium-photo-plus-small-logo —
it is **editorial poster design**, layout-led:

- Huge condensed grotesque headline (Helvetica-ish), broken over two lines, dominating the
  lower half; short declarative sentences ending in periods ("STRIPPED BACK." / "DIALED IN.")
- B&W photography used as a *cropped block or full-bleed element*, always subordinate to type;
  sometimes a grainy abstract blur instead of a subject
- ONE neon accent as a **solid geometric shape** — square, circle, or rotated tape — often with
  the wordmark sitting inside it. Their neon green maps to PivtMedia's #FF5C00.
- Clusters of tiny 6–8pt micro-copy floating in corners and over the image
- Hairline grid rules; bracketed fragments like "[ a new dawn ]"
- Small wordmark bottom-centre

**Method that follows from this:** Higgsfield generates ONLY the B&W photographic element.
The poster itself (all type, accent shapes, rules, micro-copy, logo) is built locally — this
style needs a dozen precise text elements and AI text rendering cannot do it. Builder script
is `poster.py` in the session scratchpad; two templates: `poster_split` (photo top / huge
headline bottom / accent square straddling the seam) and `poster_disc` (full-bleed abstract /
big orange circle holding logo + micro-copy). Headline auto-fits to width; Arial Bold for
headlines, negative tracking ~2%.

**SECOND REFERENCE ADDED — @longeblack** (longeblack.com, "Strategic Luxury Brand Management
Firm by @lxias", Cairo). Tarek asked for this saved alongside BOEGÖW. It is a *different
system*, not a variation: warm cinematic luxury photography (amber / honey-gold / caramel /
deep chocolate), centred **thin widely-letterspaced** headline (Segoe UI Light works), ™ and Ⓡ
marks, and a discreet endorsement lockup — "A BRAND BY LONGEBLACK" — under the client's name.
Copy voice is exclusivity: "Not for everyone. And that's the point."

Use BOEGÖW for PivtMedia speaking as itself (manifesto/statement posts, stark B&W, loud type);
use LONGEBLACK for presenting a *client* brand (warm, quiet type, endorsement lockup).
Full write-up saved at `E:\PivtMedia\brand-campaign\references\REFERENCES.md`, with BOEGÖW
post images in `references\boegow\`.

**Instagram scraping note:** post CDN URLs are cookie-bound — plain curl/urllib gets 403 on
longeblack (boegow's happened to work). View them through the logged-in browser session and
screenshot; don't waste time on header spoofing.

Four poster templates now exist across `poster.py` + `poster2.py`: `poster_split`,
`poster_disc`, `poster_tape` (full-bleed B&W + rotated orange tape + huge white headline),
`poster_endorse` (warm photo + thin centred headline + endorsement lockup).

**Real client work lives in the CONCEPT site repo** — `CONCEPT\site\public\projects\`.
Four campaigns, defined in `DarkroomBoard.tsx` / `DiceTV.tsx` / `Scene.tsx`:
- **COOL KIDS** — streetwear, 2025 · PIVT · 001 — content + paid social for a Fall '25 drop
- **SAY LESS** — loungewear, 002 — always-on content + UGC
- **GUFIT** — activewear, 003 — content + paid social
- **KLIN** — home goods / candles, 004 — art direction + social; tagline "odd by design."
  (NOTE: it is spelled **KLIN**, not KLN.)
Numbered shots are 3:4 portrait (~1050x1400); the `<name>.jpg` heroes are 16:9.

For LONGEBLACK-lineage client posters, **use this real photography rather than generating
stand-ins** — AI imagery would misrepresent actual client products. `poster_endorse` now picks
ink automatically from the ground luminance (dark type + black logo on KLIN's pale plaster,
white on COOL KIDS' alley) and only applies the bottom scrim when the type is white.

Six poster templates total: `poster_split`, `poster_disc` (poster.py); `poster_tape`,
`poster_endorse` (poster2.py); `poster_index` (paper ground, hairline grid, inset photo,
numbered index rows), `poster_outline` (full-bleed B&W, line 1 solid + line 2 outline-only,
vertical side text, orange bar) (poster3.py).

**Recurring gotchas:** Higgsfield sometimes returns a 40–55px border artifact — measure and
trim before compositing. Never place white micro-copy without checking local luminance;
`mean_lum` / `contrast_ink` / `scrim_bottom` / stroke halos in poster.py exist for this.

**LONGEBLACK lineage REJECTED (2026-08-02).** Tarek dropped it — the thin letterspaced
centred headline over busy photography was not readable enough, even on the real KLIN /
COOL KIDS shots. Do not revive `poster_endorse` without solving legibility first. **BOEGÖW
lineage is the approved direction.**

**Colour is now in play.** He asked for "different colourful designs", so the palette extends
beyond mono+orange: BLUE (18,46,214), MAGENTA (255,45,111), YELLOW (255,206,0),
CREAM (247,243,233), INK (17,17,17), plus ORANGE #FF5C00. Four colour templates in
`poster4.py`: `poster_duotone` (greyscale mapped onto a two-colour ramp via ImageOps.colorize),
`poster_bands` (Swiss horizontal colour-band stack with the photo as one band),
`poster_riso` (two halftone dot screens, deliberately misregistered by ~7px, on cream paper),
`poster_stat` (type-only, giant numeral on a flat colour field — needs no image at all).

**Standing request: every poster in a batch should be a DIFFERENT layout**, not the same
template re-run with new copy. Ten templates exist now across poster.py / poster2.py /
poster3.py / poster4.py.

**NO GENERATED HUMANS (standing rule, 2026-08-02).** Tarek asked to stop generating realistic
people. Use the **masked / anonymous figure** approach instead, referencing
instagram.com/p/DVV8DLviD4y (LONGEBLACK, "Not built to blend / Built to be remembered"):
figures in sharply tailored black overcoats with a **smooth matte faceted low-poly polyhedron
in place of a head** — completely featureless, against blown-out white. Prompt must stack the
negatives hard ("no face, no facial features, no eyes, no mouth, no human head, no skin") —
this works reliably and gives human silhouette and gesture with zero likeness.

**Colour note:** electric BLUE as a large flat field was rejected ("doesn't fit the
aesthetic") — the Swiss colour-bands poster was the one piece of that batch he disliked. Keep
the palette in PivtMedia's own world: ORANGE #FF5C00, CREAM, INK, warm ochre. Magenta/blue
worked fine inside the riso halftone treatment, so the objection is to blue as a dominant
flat field, not to blue existing.

Four more templates in `poster5.py`: `poster_diptych` (vertical split, photo | solid colour
type panel), `poster_knockout` (solid orange band with the headline punched out to reveal the
photo — strongest device so far), `poster_triptych` (three panels cropped from one frame),
`poster_receipt` (till-roll slip, torn edge, dotted leaders — plays off the barcode logo;
width_frac ~0.56 and self-sizing height, otherwise it reads as a wide card with a dead zone).

**Masked-figure batch also REJECTED (2026-08-02).** The diptych / knockout / triptych /
receipt set did not land either. Tarek: "stay away from generating human figures at the
moment" — that now includes the faceted-mask figures, not just realistic people. **Use
non-human subjects**: abstract textures, landscape, architecture, single objects, or pure
type.

**What has actually been liked, use these as the baseline:** `poster_duotone` (greyscale
mapped to a two-colour ramp), `poster_riso` (misregistered two-colour halftone), `poster_stat`
/ `poster_word` (type-only, no image needed at all — cheapest format to produce), and the
earlier `poster_disc` / `poster_split` B&W-plus-orange pieces. Proven non-human subjects:
ink-in-water, crumpled foil, paper-stack macro, storm clouds, aerial dunes, brutalist
architecture, single sculptural objects.

Two calmer templates added in `poster6.py`: `poster_word` (one enormous word on a colour
field, oversized ghost of the same word bleeding off the top, numbered annotations pinned
around it) and `poster_label` (gallery-catalogue layout — plate, specimen label with
MEDIUM/CONDITION/PROVENANCE rows, body text; size the plate ~0.70W x 0.50H and anchor the
logo to the end of the body block or the bottom third goes dead).

**Production-gear direction (Tarek's idea, 2026-08-02).** He wants cameras / lenses /
production tools in some posters to signal "marketing agency". Genuine upside: the abstract
subjects (dunes, foil, storm clouds) are brand-agnostic and say nothing about what PivtMedia
actually does; gear fixes that and is non-human. Risk flagged to him: gear-forward content
reads as *junior videographer*, not *strategic agency* — clients buy outcomes, not an FX3 —
and neither BOEGÖW nor LONGEBLACK shows any equipment at all. Recommendation: gear as
**abstracted craft texture** (macro lens elements, filter edges, cable coils, cage corners),
NOT hero product shots.

**Never render the Sony wordmark** or any real manufacturer's branding — implies a partnership
that doesn't exist, and image models garble logos. Prompt equipment as "completely unbranded
and unmarked" plus negatives for engraved numbers / focal-length markings / model names.

A/B built for comparison at `final/A-gear-as-texture.jpg` and `final/B-gear-as-hero.jpg` —
identical `poster_split` layout and copy ("FOCUS IS / A DECISION.", kicker "CRAFT, NOT KIT."),
only the photograph differs.

**Layout bug fixed in `poster_split`:** a short second line let `fit_size` scale the headline
up until the block overran the hairline and the kicker collided with the right micro-copy.
Headline is now capped at `(rule_y - 150 - ph) / 2.66` and the kicker y is clamped above the
rule. Worth re-checking any older split posters built before this fix.

**`poster_overlap` (poster7.py) — new device pulled from the saved BOEGÖW reference
`references/boegow/e-mar18.jpg` ("REALITY. REWRITTEN.").** Huge headline at the TOP; the
subject is a **cutout layered OVER the type** so it interrupts the letterforms; a micro-line
**justified edge-to-edge** beneath it; a bracketed credit in orange closes the poster
("[ PIVTMEDIA VISUAL DIRECTION. ]"). This is the only template where type sits *behind* the
image, which is what makes it read differently from the rest.

Cutouts come from Higgsfield `remove_background` (takes the generation job_id directly, no
re-upload). Keep `obj_bottom` ≈0.878 and `obj_h` ≈0.655 — at the original 0.945/0.74 the
object ran into the footer and the black footer text landed on the black cone base.

**Still unused from the saved references:** `references/boegow/h-aug10.jpg` — an asymmetric
**scatter/collage**: several small captioned image plates placed off-grid on a pale field,
connector bullet-dots, vertical side text, headline floating in open space. That's the next
new device to build when one is wanted.

**Feedback pattern worth remembering:** repeating an existing layout with new imagery gets
rejected as "similar to a lot of the pictures we have" — he notices layout repetition faster
than subject repetition. Always reach for a genuinely new arrangement, and go back to the
saved reference images for it rather than inventing.

**LONGEBLACK lineage REVIVED and now APPROVED (2026-08-02, later).** Tarek asked for it back.
The legibility failure was solved **compositionally, not typographically** — the thin
letterspaced type is unchanged:
1. The image prompt reserves a calm tonally-even empty zone AND demands a *gradual* falloff.
   Critical: asking for a dark "band"/"upper third in shadow" makes the model render a
   literal hard-edged black rectangle — must say "continuous gradual falloff, NO hard
   horizontal edge, NO visible band".
2. Layout deepens that zone with a **soft gaussian gradient** (`soft_band` in poster8.py),
   never a hard plate.
3. Measure it: mean luminance under the headline should be **< ~70** for white type. Both
   approved posters measured 30 and 56.

Templates in `poster8.py`: `poster_lb_hero` (brand name + ™ + endorsement lockup + logo +
orange rule + closing line) and `poster_lb_statement` (label + rule top-left, wordmark
top-right, thin headline lower-middle, body, bracketed wordmark).

**Mockup brands are approved** for template demos. Used **OSSARA** (fictional fragrance/home
brand). Always check an invented name isn't a real trademark before anything goes public.

**`CREATIVE-BRIEF.md` exists** at `brand-campaign/CREATIVE-BRIEF.md` — a standalone handoff
doc for Tarek's content agent covering the method, brand constants, both lineages, hard
rules, all 12 layouts, prompt recipes and a QA checklist. **Keep it updated whenever the
system changes.**

**PALETTE CORRECTION (Tarek, 2026-08-02).** LONGEBLACK must NOT be locked to warm amber — he
pushed back on that explicitly, wants variety so the grid doesn't look samey. **The palette is
a variable; the DNA is the thin letterspaced centred type + cinematic depth + restraint +
™/endorsement structure.** Approved variants: warm amber · **rich cinematic B&W** (deep
blacks, luminous highlights, real depth — NOT the flat graphic B&W used for BOEGÖW) · cool
neutral stone/concrete (grey only, flat electric blue still banned) · deep green · high-key
bone. On light grounds the logic inverts: dark ink type, and the type-zone gradient must
LIGHTEN rather than darken. Rule is "measure the ground, pick the ink that survives", not
"white type".

Built a **B&W production-set pair** showing PivtMedia itself: `38-pivtmedia-stage.jpg` (empty
soundstage + lit cyclorama, hero format, PIVTMEDIA™ + "Production, direction, distribution")
and `39-nothing-by-accident.jpg` (overhead lighting grid, statement format). Note a
production *environment* reads as craft; a camera product shot reads as kit-flex — see the
A/B finding above.

**B&W production-set posters are a HIT (2026-08-02).** Tarek: "I love the first one, the
production set looks like a marketing agency set and not a movie production set." The key is
**commercial studio, not film set** — sweep tables, seamless paper rolls, softboxes, C-stands,
sandbags, coiled cables, stools. Prompt "commercial rather than cinematic-film". Delivered
`40-built-here.jpg` (product sweep set) and `41-the-quiet-part.jpg` (seamless backdrop
corner), both `poster_lb_hero` with the name slot used for a short phrase rather than the
brand name.

Two more colour layouts in `poster9.py`: `poster_scatter` (the last unused BOEGÖW device from
`h-aug10` — off-grid captioned plates, orange connector dots, vertical side label, headline
low-right + body; needs the body paragraph or the lower middle goes dead) and `poster_window`
(flat colour field with a circular window revealing a vivid photo — inverse of `poster_disc`;
headline size must be capped against the hairline or it collides with the footer).

14 layouts total now, all catalogued in CREATIVE-BRIEF.md.

**"PRACTICE NOTES" IS A FAVOURITE SERIES (Tarek, 2026-08-02): "I also do like the PRACTICE
NOTES Pictures a lot."** That's the `poster_lb_statement` layout with a "PRACTICE NOTES —
NO. 0X" label top-left. **Treat it as a running numbered series** — keep incrementing and
vary the palette each issue. Issued: no. 01 warm stone interior · no. 02 B&W lighting grid ·
no. 03 (scatter variant) · no. 04 deep green marble corridor.

**Third LONGEBLACK layout added — `poster_lb_frame` (poster10.py).** Invitation-card device:
hairline rectangle inset from the edges, small label **breaking the top rule** (draw a
background-coloured box behind the label to interrupt the line), thin letterspaced type
stacked inside, orange rule, body, closing detail + logo inside the bottom of the frame.
**It auto-inverts for light grounds** — measures `mean_lum`, picks dark ink, and its
`soft_band` LIGHTENS instead of darkening. Proven on high-key bone (ground lum 232).

Palettes now proven beyond amber: **deep green** (emerald/malachite corridor, warm gold
accents, "no blue/cyan/teal" in prompt) and **high-key bone** (ivory silk, dark ink type).

15 layouts total. CREATIVE-BRIEF.md updated with both.

**Practice Notes issued so far:** no. 01 warm stone interior · no. 02 B&W lighting grid ·
no. 03 (scatter variant) · no. 04 deep green marble corridor · **no. 05 Santorini caldera
terrace at golden hour** · **no. 06 Monaco/Riviera harbour at dusk with superyachts**.
Tarek asked for luxury natural scenery — "Santorini, Monaco, water, yachts... not just trees".
Mediterranean luxury travel imagery works extremely well in this format.

**`poster_lb_statement` head_y must be chosen per image.** Default 0.575 assumes a dark
lower-middle. The Santorini shot was inverted (bright plaster below, dark sea above) so the
headline moved to `head_y=0.185` over the sea. Always look at where the dark even zone
actually is. The closing bracketed tag is now contrast-aware too — plain ORANGE on dark
ground, deepened `(176,58,0)` on light ground.

**Higgsfield jobs occasionally stall** (a Monaco render sat "in_progress" ~10 min while peers
took ~2). Re-fire the generation rather than waiting indefinitely.

**B&W production-set series now 4 pieces** (all `poster_lb_hero`): 38 soundstage/cyclorama ·
40 product sweep table · 41 seamless backdrop corner · **49 ordered grip corner** (flight
cases, apple boxes, sandbags, coiled cables on a rail, C-stands racked — "IN ORDER").
Practice Notes now runs to **no. 07** — a warm camera-on-desk planning scene (camera body,
storyboard sheets with blank sketched frames, notebook, pen) for "STRATEGY BEFORE SHUTTER".
A desk/planning scene reads as strategy, unlike a camera product shot which reads as kit-flex.

**Two recurring generation faults to check every time:**
1. **Palette leaks.** A "desk lamp" came back as a green banker's lamp despite a warm-only
   instruction — name the specific offender in the negatives ("no green lampshade, no green
   glass") and verify numerically (count saturated green/cyan pixels; got it from prominent
   to 0.17%).
2. **Edge artifacts appear on ONE side, not all four.** The grip-corner render had a 43px
   pure-white strip along the bottom only. Scan all four edges separately — comparing a
   uniform run against the inner value is what catches it.

**"Production set" means BOUTIQUE, not warehouse (Tarek, 2026-08-02).** He rejected a grip
corner of flight cases/apple boxes/sandbags as "more of a movie production and not a small
production set". The approved replacement is a **refined designer's studio**: polished
concrete, marble plinth, sculptural chair, architectural plant, steel-framed window, ONE
elegant softbox. Prompt it explicitly as "a designer's private studio, intimate and
expensive, NOT a warehouse, NOT a film stage, NOT an industrial space" and negative out
flight cases / cable clutter / scaffolding.

**Never ask for "shallow depth of field" on desk/still-life scenes** — it mushes the
foreground and he called it out as blurry. Use "EVERYTHING SHARP front to back, deep depth of
field, tack sharp, no blur, no bokeh" plus "shot at a small aperture", and negative out
blur/bokeh/shallow-DOF. The approved desk is honed dark marble with a brass edge, tan leather
portfolio, brass fountain pen, crystal tumbler, warm window light.

**SYSTEM IS NOW SAVED AND RUNNABLE (2026-08-02).** Everything was rescued out of the session
scratchpad into the repo. **Start here next time: run `/pivtcontent`.**

```
E:\PivtMedia\brand-campaign\
├── CREATIVE-BRIEF.md    design doc — lineages, palettes, hard rules, 21 layouts, QA
├── README.md            operating doc — how to actually build a poster
├── CONTACT-SHEET.jpg    all approved posters at a glance (regen: studio/contact_sheet.py)
├── studio/              THE CODE. layouts.py = registry of all 21 + build()
│   └── recipes/         working build scripts for every past batch
├── raw/                 untouched generated photos (never delete — lets type be re-set)
├── final/               34 approved posters
├── archive/             12 rejected + WHY-ARCHIVED.md explaining each
└── references/          BOEGÖW images + REFERENCES.md
```

`.claude/commands/pivtcontent.md` is the scoped entry point (matches the pivtweb/pivtportal
pattern) — it carries the method, all 9 standing rules, build commands, QA steps and the
Practice Notes series state.

Usage: `cd brand-campaign/studio; python layouts.py` lists all 21 layouts; then
`from layouts import build; build("lb_statement", photo, out, ...)`.

**`stat`, `word` and `receipt` need NO photograph** — pure typography, cheapest posts to make.
**Rescued from archive, worth reviving with non-figure subjects: `knockout` and `receipt`** —
both were rejected for their subject, not their layout.

**Practice Notes 08 + 09 added (2026-08-03):** no. 08 desert modernism (board-formed concrete
villa, reflecting pool, warm sand/terracotta) · no. 09 modern alpine lodge (charred timber,
stone, snow, warm interior glow). Both requested as "luxurious and modern" follow-ups to the
Santorini/Monaco pair — **modern architecture set in natural scenery** is the winning formula
for this series, not landscape alone.

**Template fix in `poster_lb_statement` (poster8.py):** the top-left label and the top-right
wordmark were hardcoded white and washed out on a pale overcast sky (ground lum 210). Both are
now contrast-aware via `mean_lum` — dark ink + deepened orange rule on light ground. All three
zones (headline, label/logo, closing tag) now adapt independently. Applies to every future
Practice Note.

**PRACTICE NOTES — full series state (2026-08-03).** All agency-relevant now:
01 warm stone interior · 02 B&W lighting grid · **03 empty boardroom (neutral)** ·
**04 letterpress workshop (warm)** · 05 Santorini · 06 Monaco harbour · 07 marble desk ·
08 desert villa · 09 alpine lodge · **10 blank billboard at dusk (cool)** ·
**11 archive of bound volumes (B&W)** · 12 green marble corridor (was 04, renumbered).
`42-three-questions` is a scatter layout and was relabelled "PivtMedia — studio note" so it
no longer claims a series number.

**Marketing-agency subjects that work in this series:** empty boardroom, letterpress type
cases, a BLANK billboard (prompt "CRITICAL: completely empty, no image, no text, no
advertisement on it" or the model fills it), archive of blank-spined bound volumes.

**Two more `poster_lb_statement` robustness fixes:**
- Label + wordmark are contrast-aware (`mean_lum`) — dark ink + deepened orange rule on light
  ground. Fixed white-on-pale-sky washout.
- The label now also carries a **subtle opposite-tone stroke halo (alpha 150)**. Mean-based
  ink choice fails on a *mixed* ground — in the archive shot a bright window ate the middle of
  "PRACTICE". The halo is invisible on even grounds and rescues high-contrast edges.

**"Craft" subjects must be MODERN, not heritage (Tarek, 2026-08-03).** A letterpress workshop
was rejected for Practice Note 04 — vintage press and wooden type cases read antique, not
luxury. Replaced with a **contemporary penthouse library** (dark oak shelving with concealed
lighting, modern leather armchair, stone table, floor-to-ceiling glass, city at dusk). Same
rule as "production set means boutique, not warehouse": when prompting craft/heritage-adjacent
subjects, add "contemporary design, NOT antique, NOT traditional or classical".

**THIRD REFERENCE SET — Google Drive "PIVT CONTENT › references"** (folder
`1Y8MY_c5HqluxejfeoiAmUkOLAdKTdpDF`, owner hazemelgazzar20@gmail.com, 15 images). Bright
saturated **retro-editorial** — surreal colour-blocking, pastel product still lifes, poster
mockups in situ. Full write-up: `references/DRIVE-FOLDER.md`.

**How to view Drive images cheaply:** they are auth-gated (plain download returns a sign-in
page) and `read_file_content` returns nothing for photos; base64 costs 12–40k tokens EACH.
Use **claude-in-chrome** — open the folder in the signed-in session and screenshot the
thumbnail grid, then zoom rows.

Agreed direction: **partial figures only** (hands/legs/feet, no faces) · build surreal
colour-blocked + poster-mockups-in-situ + pastel still lifes · **palette expanded** to
crimson/navy/mustard/teal as full grounds with orange still the brand accent.

**NEW CAPABILITY — `studio/mockup.py`.** Places a finished poster INTO a photographed scene
as a physical print (reverse of every other module). Generate a room with a genuinely blank
poster ("CRITICAL: completely blank, nothing printed on it"), call `probe()` for a coordinate
grid, read the four corners, then `place(scene, poster, out, corners, shade, warm)`.
Pure-Python homography — deliberately no numpy, since it isn't installed.

`knockout` revived successfully from the archive (rejected originally for its masked-figure
subject, not the layout). Its sub-line is now contrast-aware too.

**Drive-set round 1 verdict (2026-08-03):** only `57-wait.jpg` (mustard/teal knockout) kept.
The poster-in-room mockup and the pastel window were both rejected and deleted — so
`studio/mockup.py` exists and works but its output has NOT been approved; don't assume it.

**Round 2 — approved reference targets.** Tarek picked two images out of the Drive folder:
the surreal red-wall/arch/car with mirror reflection, and the "odd ritual" seated figure
holding a newspaper over their face. Built as:
- `60-there-is-a-door.jpg` — red wall + arch + white ladder + salt-flat reflection, cobalt
  sky, `outline` layout. Ladder swapped in for the car so it isn't a copy.
- `59-nobody-reads.jpg` — seated figure, blank newspaper hiding the face, background removed
  and run through `overlap` so the cutout interrupts the headline. **This is the model for
  partial-figure work**: face fully concealed by a prop, so no likeness is generated.

**`poster_outline` is now contrast-aware** — it was built for dark photos and both the white
headline and the thin white outline vanished on a bright salt flat. It now measures the
headline band and the footer band separately, flips ink to dark on light grounds, thickens
the outline stroke (size//40), and pushes the bottom scrim to 232 when the footer ground is
pale.

**Styling third-party reference photos (2026-08-03).** Tarek asked to apply PivtMedia layouts
directly to 3 found images from the Drive folder (TV+sneakers, motion-blur+chair, man with
cup). Built as `61-obsolete` (label), `62-dont-sit-this-out` (outline), `63-show-up` (tape).
**Internal test only** — flagged to him: they are found images, one has an identifiable face,
and SONY / "invade." brand marks are visible in the TV shot. Rights would need clearing before
any public post. Source files are only 736px wide, so ~2.2x upscale to the 1600px canvas
costs sharpness.

**Layout-to-image matching lesson:** `poster_disc` put its orange circle dead on the man's
face and destroyed the photograph. **Never use `disc` or `knockout` on a portrait** — their
solid shapes land centre-frame. For a face-forward image use `tape` (headline low) or `label`
(photo inset). `label` turned out to be a great fit for a single hero object — cataloguing the
TV as a museum specimen.

**`poster_tape` micro_top is now contrast-aware** with a stroke halo — it was hardcoded white
and vanished on a pale wall.

**EVERYTHING IS NOW SAVED AND REPRODUCIBLE (2026-08-04).**
`studio/recipes/rebuild_all.py` rebuilds **every approved poster in one run** — it is the
single source of truth and supersedes the older `build_batch*.py`. It re-composites type onto
images already in `raw/`, so it is free and instant; it also prints each headline's ground
luminance as a live QA pass (all clear <70). Change a headline there and re-run.
CREATIVE-BRIEF.md now carries 13 hard rules, the Practice Notes series table, the carousel
section, and the expanded QA checklist.

**CAROUSEL 01 — "Nobody reads" (4 slides), approved format.** `C1-nobody-reads` ·
`C2-at-the-fold` · `C3-do-not-come-back` · `C4-lead-with-the-point`. All `overlap`, cream
ground, cutout subjects. **A carousel INVERTS the different-layout-per-batch rule** — lock
layout and geometry across slides so the swipe is continuous; only image and line change.
Arc: **premise → failure → consequence → answer**. Direction of travel matters (slide 3 walks
rightward, pushing toward slide 4) and the last slide must resolve, not repeat.

**Uploading local images to Higgsfield** (needed for `remove_background` on user-supplied
files): `media_upload(files=[{filename, content_type}])` → `curl -X PUT --data-binary @file
'<upload_url>'` → `media_confirm(media_ids, type="image")` → pass the media_id to
`remove_background`. Do NOT flood-fill locally on these cream-seamless shots — it eats the
cream paper, which is the subject.

**Carousel end slides must BREAK the pattern (Tarek, 2026-08-04):** "the ending should follow
a different style so anyone can tell the carousel is over." He liked slides 2–3 and the slide-4
*copy*, but not its treatment. Solution = new `poster_endcard` in poster7.py: keeps the
`overlap` typographic system (top headline, justified micro-line, foot + bracketed credit) but
**inverts to ink, drops the photograph entirely, and puts the wordmark where the subject
stood**. The absence of the image is the signal. Wordmark must be large (~460px) or the empty
field reads as an accident rather than a deliberate close.

Related: [[project-business]], [[project-concept-site]]

## Motion work — what these video models can and cannot do (learned 2026-08-20)

**Hard limit found the expensive way (~78 credits):** AI video models will NOT drive an
object across the frame and off it. Three attempts on one shot — Hailuo, Seedance 1.5 Pro
(8s, both landscape and 9:16), MiniMax H3 (5s, start+end frames) — all kept the subject
near its start position. Frame-by-frame centroid tracking proved it: the Seedance take
drifted inside a small box (x 50–71%, y 30–44%) for a full 8s; the H3 take travelled only
x 70%→49% then froze for its last 0.6s. Explicit prompts, negative clauses, and an end
frame showing the object half-out of frame did not change this.

Also: **Seedance ignores portrait start/end frames unless `aspect_ratio` is passed
explicitly** — it silently returned 1920x1088 landscape from two 9:16 anchors.

**The pattern that works — AI for realism, code for trajectory.** Generate the object once
as a still, lift it out as a cutout, and animate it procedurally. Extraction trick: a plate
difference fails (the AI re-render differs subtly everywhere) and a saturation key eats the
object's shaded side — instead key a confident core, fit a circle/shape to it, and use that
as the alpha. Sell the motion with accumulation motion blur (stamp sub-frame copies along
the real path) and a height-keyed shadow. Shipped this way: `motion/90-ball-bounce-final.mp4`
(studio/bounce2.py) and stills `final/78-ideas-take-a-lane.jpg`, `final/91-…-ball.jpg`.

## Lens reel (started 2026-08-20)

Recreating a @subformers reel (13.12s, 720x1280, 30fps, ONE unbroken shot, no cuts): a
single coffee cup in a shopping basket multiplies until the pile fills the frame and the
brand mark resolves. **Key discovery from its final frame — the mark is projected onto the
finished pile from the camera's viewpoint**, not printed on the objects and arranged by
physics. It wraps over curves, breaks across gaps, and drops out in shadowed crevices. So
the simulation only has to build a convincing pile.

Tarek's version, agreed: **camera lenses** (not bulbs — glass is hard to make believable)
→ **black flight case** → **PIVT/MEDIA wordmark resolve** → **~8.5s**. Built in
`studio/lensreel.py`, output `motion/92-lens-reel-v1.mp4`, 0 credits.

Two non-obvious constraints found while building it:
- **Objects must be LIGHT and the container dark.** Dark lenses in a black case gave the
  projection no surface and the mark vanished entirely. The reference works because white
  cups sit in a dark basket. Fixed with aluminium barrels.
- **Fine tracked type gets shredded.** PIVTMEDIA on one line (121px cap) read as
  "IVI ME7IA". Stacked PIVT/MEDIA at 375px cap survives the breakup. The reference used a
  compact chunky glyph for this reason.

Lens art in v1 is a procedural placeholder; swap `make_lens()` for a photoreal top-down
Higgsfield plate when the connector is back. Nothing else needs to change.

## Portable + git-tracked (2026-10-12)

The campaign folder is now a **git repo** (`E:\PivtMedia\brand-campaign`, first commit
`054a657`), set up so it can run on Tarek's laptop as well as the desktop. Same Claude
account does NOT move files — only the Higgsfield connector follows the account; the
folder, the `/pivtcontent` command and this memory all had to be packaged.

What changed in the code — **do not reintroduce absolute paths**:
- **`studio/paths.py`** is the single source for every folder and font. It resolves `ROOT`
  from its own location, so the folder works on any drive/machine. Override with
  `PIVT_CAMPAIGN_ROOT`. Fonts resolve through `pick_font()` — Windows, then macOS, then
  Linux candidates — and raise with the full candidate list if none exist.
- **Logos moved into the repo** at `brand/logo/` (was `E:\PivtMedia\Pivt Media Logos\
  campaign-overlay\`, which only exists on the desktop). Originals left in place.
- `poster.py` re-exports `F_BOLD`/`F_REG`/`LOGO_DIR` from `paths`, because every other
  module imports them from `poster`.

**`raw/` (1.3 GB) and `motion/` (4.4 GB) are gitignored.** Neither is needed to create new
content; all 58 finished posters live in `final/`. Consequence worth remembering:
`rebuild_all.py` cannot run anywhere `raw/` is absent — it re-composites type onto those
source photographs. Copy `raw/` across manually if an old headline needs re-cutting.

`install/` carries what git can't place automatically: `pivtcontent.md` (goes in
`.claude/commands/`) and `memory/*.md` (import on the new machine). Setup steps are in
`SETUP-LAPTOP.md`.

Cross-machine rule: **always `git pull` before building.** `final/` is binary JPEGs and git
cannot merge them — simultaneous work on both machines means resolving by hand.
