"""PivtMedia poster system — the single entry point.

Every layout is registered here under a friendly name. Import this, not the numbered
`poster*.py` modules (those are the implementation and are grouped by when they were
built, not by what they do).

    from layouts import LAYOUTS, build
    build("lb_statement", "raw/x.png", "final/y.jpg",
          label="Practice notes — no. 08", headline="Line one|line two",
          body="...", tag="PivtMedia", head_y=0.60)

Run `python layouts.py` to print the catalogue.
"""
import poster
import poster2
import poster3
import poster4
import poster5
import poster6
import poster7
import poster8
import poster9
import poster10

# name -> (function, lineage, one-line description)
LAYOUTS = {
    # ---------------- BOEGÖW lineage: type is the hero -------------------
    "split": (poster.poster_split, "BOEGOW",
              "Photo top ~54%, huge headline on paper below, accent square on the seam."),
    "disc": (poster.poster_disc, "BOEGOW",
             "Full-bleed abstract, orange circle holding logo + bracketed fragments."),
    "tape": (poster2.poster_tape, "BOEGOW",
             "Full-bleed B&W, huge white headline, rotated orange tape strip."),
    "index": (poster3.poster_index, "BOEGOW",
              "Paper ground, hairline grid, inset photo, numbered index rows."),
    "outline": (poster3.poster_outline, "BOEGOW",
                "Line 1 solid, line 2 outline-only. Vertical side text, orange bar."),
    "duotone": (poster4.poster_duotone, "BOEGOW",
                "Greyscale mapped onto a two-colour ramp. Cream headline."),
    "bands": (poster4.poster_bands, "BOEGOW",
              "Swiss horizontal colour bands. NOTE: rejected in blue — recolour before use."),
    "riso": (poster4.poster_riso, "BOEGOW",
             "Two misregistered halftone screens on cream. Reads as real 2-colour print."),
    "stat": (poster4.poster_stat, "BOEGOW",
             "TYPE ONLY, no photo. Giant numeral on a flat colour field."),
    "word": (poster6.poster_word, "BOEGOW",
             "TYPE ONLY, no photo. One huge word + ghost + numbered annotations."),
    "label": (poster6.poster_label, "BOEGOW",
              "Gallery catalogue: plate, specimen label, MEDIUM/CONDITION rows."),
    "diptych": (poster5.poster_diptych, "BOEGOW",
                "Vertical split: photo panel | solid colour type panel."),
    "knockout": (poster5.poster_knockout, "BOEGOW",
                 "Solid orange band with the headline punched out to reveal the photo."),
    "triptych": (poster5.poster_triptych, "BOEGOW",
                 "Three panels cropped from one frame, labelled beneath."),
    "receipt": (poster5.poster_receipt, "BOEGOW",
                "TYPE ONLY. Till-roll slip, torn edge, dotted leaders. Plays off the barcode."),
    "overlap": (poster7.poster_overlap, "BOEGOW",
                "Headline at TOP, cutout subject layered OVER the type. Justified micro-line."),
    "scatter": (poster9.poster_scatter, "BOEGOW",
                "Off-grid captioned plates, connector dots, vertical side label."),
    "window": (poster9.poster_window, "BOEGOW",
               "Flat colour field with a circular window cut through to the photo."),

    # ------------- LONGEBLACK lineage: quiet cinematic luxury -------------
    "lb_hero": (poster8.poster_lb_hero, "LONGEBLACK",
                "Brand/phrase + TM + endorsement lockup + logo. The B&W production sets."),
    "lb_statement": (poster8.poster_lb_statement, "LONGEBLACK",
                     "PRACTICE NOTES format. Label top-left, thin headline, body, tag."),
    "lb_frame": (poster10.poster_lb_frame, "LONGEBLACK",
                 "Invitation card: hairline frame, label breaks the top rule. Auto light/dark."),
}

# Layouts that need no photograph at all — cheapest and fastest to produce.
TYPE_ONLY = {"stat", "word", "receipt"}


def build(name, *args, **kwargs):
    """Build one poster by layout name."""
    if name not in LAYOUTS:
        raise KeyError(f"Unknown layout {name!r}. Options: {', '.join(sorted(LAYOUTS))}")
    return LAYOUTS[name][0](*args, **kwargs)


def catalogue():
    lines = []
    for lineage in ("BOEGOW", "LONGEBLACK"):
        lines.append(f"\n{lineage}")
        lines.append("-" * len(lineage))
        for n, (_, lg, desc) in sorted(LAYOUTS.items()):
            if lg == lineage:
                flag = "  [type-only]" if n in TYPE_ONLY else ""
                lines.append(f"  {n:<14} {desc}{flag}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(f"{len(LAYOUTS)} layouts registered.")
    print(catalogue())
