---
description: Generate PivtMedia brand campaign posters (Higgsfield imagery + local typography) — scoped only to campaign content, not website/portal/SOP
argument-hint: [what you want to generate, e.g. "2 more Practice Notes in a new palette"]
---

You are now working **exclusively on PivtMedia brand campaign content** — the poster system
for PivtMedia's own social media. Do **NOT** touch the marketing website (CONCEPT), the
client portal, the onboarding SOP, or outreach. If a request pulls in those, flag it.

## Read these first, in this order

1. `E:\PivtMedia\brand-campaign\CREATIVE-BRIEF.md` — the design system: both lineages, the
   palettes, the hard rules, all 21 layouts, prompt recipes, QA checklist.
2. `E:\PivtMedia\brand-campaign\README.md` — how to actually run the build.
3. `E:\PivtMedia\brand-campaign\references\REFERENCES.md` — the two inspiration accounts
   decoded, plus saved reference images in `references/boegow/`.

## Content directions

Three approved directions — pick the one the request belongs to (README "Content directions"):
- **Posters** (`layouts.py`, brief §3–§10) — organic feed, Higgsfield photo + type.
- **Ad creatives** (`ads.py`, brief §11) — paid social, type only, no credits.
- **Story highlights** (`highlights.py`, brief §12) — profile covers + inside stories, no credits.

New content renders into `final/` and stays on this device; only setup changes go to git.

## The core method — do not skip this

**These are designed posters, not AI images.** Higgsfield generates ONLY the photograph,
completely **text-free**. All typography, colour blocks, rules and the logo are composited
locally in Python. Never ask the image model to render a headline — spelling usually
survives, the typeface does not.

## How to build

```bash
cd E:\PivtMedia\brand-campaign\studio
python layouts.py          # lists all 21 layouts with descriptions
```

```python
from layouts import build
build("lb_statement", "../raw/NN-x.png", "../final/NN-x.jpg",
      "Practice notes — no. 08", "Line one|line two", "Body.", "PivtMedia", head_y=0.60)
```

Working examples of every layout are in `studio/recipes/`.

## Image generation settings

Higgsfield `generate_image`, model **`nano_banana_pro`**, `aspect_ratio: "4:5"`,
`resolution: "4k"`. `gpt_image_2` does NOT support 4:5. Always append the negative block from
CREATIVE-BRIEF §6, and reserve the type zone **inside the prompt** ("the lower middle is a
calm, tonally even expanse with nothing in it, falling off gradually with no hard edge or
band").

## Standing rules (each of these came from a rejected batch)

1. **No generated humans** — no faces, no figures, not even masked/faceless ones. Use
   abstract texture, landscape, architecture, materials, objects, interiors, or pure type.
2. **Every poster in a batch uses a DIFFERENT layout.** Layout repetition gets noticed faster
   than subject repetition.
3. **Never reproduce a reference's concept** — take the aesthetic, invent the idea.
4. **Orange `#FF5C00` is the accent.** Blue as a large flat field is banned.
5. **Prefer light/high-key over dark and moody**, but keep the orange saturated.
6. **Never render a real manufacturer's logo.** Prompt equipment as "completely unbranded".
7. **Never request "shallow depth of field"** on desk/still-life scenes — it reads as blurry.
8. **"Production set" means boutique, not warehouse** — a designer's studio, not a film stage.
9. **No invented facts** — no client counts, percentages or revenue figures. Positioning only.

## Verify before delivering

- Zoom in on every text element and check it against the background beneath it. Use
  `mean_lum` from `poster.py`; under a white headline it should read **< ~70**.
- Scan **all four edges separately** — renders often carry a 25–55px artifact on one side only.
- Check the headline hasn't auto-scaled into the rule below it.
- Confirm no faces, no legible brand names, no garbled lettering, and no palette leaks
  (count saturated pixels of the banned hue if unsure).

## Series in progress

**PRACTICE NOTES** — a numbered series using the `lb_statement` layout, one of the user's
favourites. Issued: 01 warm stone · 02 B&W lighting grid · 03 scatter variant · 04 deep green
· 05 Santorini · 06 Monaco harbour · 07 marble desk. Keep incrementing and change the palette
each issue.

## Ask before assuming

If the request is open-ended ("more content"), ask which lineage, which palette, and whether
to build a new layout or reuse proven ones — those three answers change the work materially.
