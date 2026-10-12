"""Where everything lives — resolved at runtime, never hardcoded.

The studio used to carry absolute `E:\\PivtMedia\\...` paths, which meant the whole
system only ran on one machine. Everything now resolves from this file's own location,
so the campaign folder can sit on any drive, on any computer, under any name.

Fonts are resolved from a candidate list rather than a single path, because the same
typeface lives somewhere different on Windows and macOS. The first one that exists wins.

Override the root with the PIVT_CAMPAIGN_ROOT environment variable if you ever need to
point the studio at a copy of the folder somewhere else.
"""
import os

# studio/paths.py -> studio/ -> brand-campaign/
ROOT = os.environ.get(
    "PIVT_CAMPAIGN_ROOT",
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)

RAW = os.path.join(ROOT, "raw")
FINAL = os.path.join(ROOT, "final")
ARCHIVE = os.path.join(ROOT, "archive")
REFERENCES = os.path.join(ROOT, "references")
LOGO_DIR = os.path.join(ROOT, "brand", "logo")
CONTACT_SHEET = os.path.join(ROOT, "CONTACT-SHEET.jpg")


def pick_font(*candidates):
    """Return the first font file that exists.

    Raises with the full candidate list rather than letting Pillow fail on a path the
    caller never sees — a missing font is the single most likely thing to break a fresh
    machine, so it should say exactly what it looked for.
    """
    for path in candidates:
        if path and os.path.exists(path):
            return path
    raise FileNotFoundError(
        "None of these fonts were found on this machine:\n  "
        + "\n  ".join(str(c) for c in candidates)
        + "\nInstall one of them, or edit studio/paths.py to add a local equivalent."
    )


_WIN = r"C:\Windows\Fonts"
_MAC = "/System/Library/Fonts/Supplemental"
_LIN = "/usr/share/fonts/truetype"

# Bold grotesque — every headline in the system. Helvetica-like, tight, neutral.
F_BOLD = pick_font(
    os.path.join(_WIN, "arialbd.ttf"),
    os.path.join(_MAC, "Arial Bold.ttf"),
    "/System/Library/Fonts/Helvetica.ttc",
    os.path.join(_LIN, "liberation/LiberationSans-Bold.ttf"),
    os.path.join(_LIN, "dejavu/DejaVuSans-Bold.ttf"),
)

# Regular weight — micro-copy and captions.
F_REG = pick_font(
    os.path.join(_WIN, "arial.ttf"),
    os.path.join(_MAC, "Arial.ttf"),
    "/System/Library/Fonts/Helvetica.ttc",
    os.path.join(_LIN, "liberation/LiberationSans-Regular.ttf"),
    os.path.join(_LIN, "dejavu/DejaVuSans.ttf"),
)

# Thin weight — the LONGEBLACK lineage's wide letterspaced headlines. The whole quiet
# register depends on this being genuinely light, so a bold fallback would be wrong;
# fall back through the thinnest things available before giving up on regular.
F_LIGHT = pick_font(
    os.path.join(_WIN, "segoeuil.ttf"),
    os.path.join(_MAC, "HelveticaNeue.ttc"),
    "/System/Library/Fonts/Helvetica.ttc",
    os.path.join(_LIN, "dejavu/DejaVuSans-ExtraLight.ttf"),
    os.path.join(_LIN, "liberation/LiberationSans-Regular.ttf"),
    F_REG,
)

# Condensed industrial — used by the tagline compositor.
F_BAHN = pick_font(
    os.path.join(_WIN, "bahnschrift.ttf"),
    os.path.join(_WIN, "arialbd.ttf"),
    os.path.join(_MAC, "Arial Narrow Bold.ttf"),
    F_BOLD,
)
