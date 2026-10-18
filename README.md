# PivtMedia Brand Campaign — how to run it

Two documents matter here:

- **`CREATIVE-BRIEF.md`** — the *design* doc. What the look is, why, and the rules.
  Hand this to a designer or content agent.
- **`README.md`** (this file) — the *operating* doc. How to actually produce a poster.

## Content directions

Three approved directions, each with its own module and its own section in the brief.
Everything renders into `final/` on this device only — nothing content goes to git.

| Direction | Module | Output | Credits | Brief |
|---|---|---|---|---|
| **Posters** — organic feed, photo + type | `layouts.py` | `final/` | ~4 per photo (type-only layouts free) | §3–§10 |
| **Ad creatives** — paid social, type only | `ads.py` | `final/ads/` | none | §11 |
| **Story highlights** — profile covers + stories | `highlights.py` | `final/highlights/` | none | §12 |

```bash
cd studio
python ads.py          # every ad, every format
python highlights.py   # every highlight cover and story
```

---

## The one thing to understand

**These are designed posters, not AI images.** The image model produces only the
photograph — completely text-free. Every headline, rule, colour block and the logo are set
afterwards in code, at exact sizes. That is why the typography is sharp and why any line can
be rewritten later without regenerating anything.

Two folders reflect this:

- **`raw/`** — untouched generated photographs. Never delete these; they let you re-set the
  type without paying to regenerate.
- **`final/`** — finished posters, 1600×2000 (4:5).

Both folders stay **on this device only** — they're in `.gitignore`. The GitHub repo is the
setup repo (code, docs, logos, the `/pivtcontent` command) for getting a new machine
running; it is not where content is stored. The original reference set of posters in
`final/` is still tracked, but nothing new you make gets committed.

---

## Producing a poster

### 1. Generate the photograph
Higgsfield → **Nano Banana Pro**, `aspect_ratio: "4:5"`, `resolution: "4k"`.
Prompt recipe and the mandatory negative block are in `CREATIVE-BRIEF.md` §6.
Save the result into `raw/`.

### 2. Build the poster

```bash
cd brand-campaign/studio
python -c "from layouts import build; build('lb_statement', '../raw/NN-name.png', '../final/NN-name.jpg', 'Practice notes — no. 08', 'Line one|line two', 'Body sentence.', 'PivtMedia', head_y=0.60)"
```

List every available layout and what it does:

```bash
python layouts.py
```

### 3. Check it before it ships
Run the QA checklist in `CREATIVE-BRIEF.md` §7. The three faults that recur most:
small text landing on a busy background, an edge artifact on **one** side of the render,
and a headline auto-scaling into the rule beneath it.

---

## What's in `studio/`

| File | Contents |
|---|---|
| **`layouts.py`** | **Start here.** Registry of all 21 layouts by friendly name, plus `build()`. Run `python layouts.py` to list them. |
| `poster.py` | Core constants, type helpers, contrast tools (`mean_lum`, `contrast_ink`, `scrim_bottom`), `split`, `disc`. |
| `poster2.py` … `poster10.py` | Layout implementations. Grouped by when they were built, not by what they do — use `layouts.py` instead of importing these directly. |
| **`ads.py`** | **Paid-social ad creatives**, type only. `python ads.py` renders every concept, every format, into `final/ads/`. See CREATIVE-BRIEF §11. |
| **`highlights.py`** | **Instagram story highlights** — progress-barcode covers + 3 stories per highlight. `python highlights.py`. See CREATIVE-BRIEF §12. |
| `mockup.py` | Places a finished poster **into** a photo as a physical print. `probe()` then `place()`. |
| `contact_sheet.py` | Rebuilds `CONTACT-SHEET.jpg` from everything in `final/`. |
| `build_logos.py` | Regenerates the four logo overlay variants from the v2 masters in `brand/logo/v2/`. |
| `compose.py` | The original simple logo-on-photo compositor (still used by posters 06 and 07). |
| **`recipes/rebuild_all.py`** | **Every approved poster, in one run.** The single source of truth for what was built and how. Supersedes the older `build_batch*.py`, which are kept for history. |

Dependency: **Pillow** only. Fonts are Windows system fonts (Arial Bold, Segoe UI Light,
Bahnschrift) — see `CREATIVE-BRIEF.md` §2.

---

## Layout cheat-sheet

**Need it fast and free?** `stat`, `word`, `receipt` need **no photograph at all** — pure
typography. Cheapest and quickest posts to make.

**Proven favourites:** `lb_statement` (the PRACTICE NOTES series), `lb_hero` (the B&W
production sets), `duotone`, `riso`, `disc`, `split`.

**Handle with care:** `bands` was rejected in blue — recolour before reuse.

---

## Changing copy on an existing poster

Don't regenerate anything. Edit the line in `studio/recipes/rebuild_all.py` and run it:

```bash
cd brand-campaign/studio
python recipes/rebuild_all.py
```

It re-composites type onto the images already in `raw/` — free, instant, and it re-verifies
every headline's contrast as it goes (each line prints its ground luminance; all should be
under ~70).

---

## Adding to the system

- **New poster, existing layout** → just call `build()`. Add it to `recipes/` if you want it
  reproducible.
- **New layout** → write it in a new `poster11.py`, register it in `layouts.py`, and add a
  row to the layout table in `CREATIVE-BRIEF.md`.
- **New palette** → add it to the palette table in `CREATIVE-BRIEF.md` §3. Remember that on
  light grounds the ink flips to dark and the type-zone gradient must *lighten*.

Keep `CREATIVE-BRIEF.md` current whenever the system changes — it is the file that gets
handed to other people.
