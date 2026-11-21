#!/usr/bin/env python3
"""Draws one invented passport spread (open passport) to $MAKEFUN_OUTPUT_DIR/entry.png.

Country: the Republic of Thalvern — a high-altitude archipelago whose islands
rise above the cloud line. Its character: every traveller pays a CLOUD TAX and
visas are valid only above 1,800 m. All dates agree:
  holder born 02 JUN 1994, Port Kestrel
  passport issued 14 MAR 2026, Port Kestrel; expires 13 MAR 2036
  stamps (chronological, all after issue, before expiry):
    29 MAR 2026  NORVASK entry   (Hafen Norvask)
    13 APR 2026  ILMAREN entry   (Ilmaren City)
    01 MAY 2026  SULDOR  entry   (Suldor Port)
    19 MAY 2026  THALVERN return (Port Kestrel)
Stdlib + PIL only, no network. Fonts: system TTFs with DejaVu fallback.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 700
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- fonts
DEJAVU = "/usr/share/fonts/truetype/dejavu/"
LIBER = "/usr/share/fonts/truetype/liberation/"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def pick(candidates, size):
    for p in candidates:
        if os.path.exists(p):
            return font(p, size)
    return ImageFont.load_default()


SERIF_B = lambda s: pick([DEJAVU + "DejaVuSerif-Bold.ttf", LIBER + "LiberationSerif-Bold.ttf"], s)
SERIF = lambda s: pick([DEJAVU + "DejaVuSerif.ttf", LIBER + "LiberationSerif-Regular.ttf"], s)
SANS = lambda s: pick([DEJAVU + "DejaVuSans.ttf", LIBER + "LiberationSans-Regular.ttf"], s)
SANS_B = lambda s: pick([DEJAVU + "DejaVuSans-Bold.ttf", LIBER + "LiberationSans-Bold.ttf"], s)
MONO = lambda s: pick([DEJAVU + "DejaVuSansMono.ttf", LIBER + "LiberationMono-Regular.ttf"], s)
MONO_B = lambda s: pick([DEJAVU + "DejaVuSansMono-Bold.ttf", LIBER + "LiberationMono-Bold.ttf"], s)

# ---------------------------------------------------------------- colours
INK = (28, 32, 48)          # near-black blue
NAVY = (26, 48, 92)
GOLD = (176, 138, 48)
CREAM = (248, 244, 232)
PAGE = (252, 250, 244)
RULE = (150, 148, 132)
LABEL = (96, 96, 88)
SKIN = (232, 196, 152)
SKIN_SH = (214, 172, 124)
HAIR = (58, 40, 26)
COAT = (34, 74, 96)
STAMP_BLUE = (32, 76, 150)
STAMP_RED = (168, 44, 40)
STAMP_GREEN = (34, 110, 72)
STAMP_PURPLE = (104, 58, 138)

img = Image.new("RGB", (W, H), (226, 220, 204))
d = ImageDraw.Draw(img, "RGBA")

# outer cover edge + spine
d.rounded_rectangle([6, 6, W - 7, H - 7], radius=10, fill=PAGE, outline=(120, 112, 88), width=2)
d.rectangle([W // 2 - 3, 10, W // 2 + 3, H - 10], fill=(196, 188, 164))
d.line([W // 2 - 6, 10, W // 2 - 6, H - 10], fill=(210, 202, 180), width=1)
d.line([W // 2 + 6, 10, W // 2 + 6, H - 10], fill=(210, 202, 180), width=1)

LX, RX = 28, W // 2 + 28          # left / right page origins
PW = W // 2 - 56                  # page width


def text(draw, xy, s, f, fill=INK, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def centre(draw, cx, y, s, f, fill=INK):
    draw.text((cx, y), s, font=f, fill=fill, anchor="ma")


def rule(draw, x0, y, x1, color=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ================================================================ emblem
def emblem(cx, cy, r):
    """Mountain peaks above a cloud line, a star above, a wave below."""
    # outer ring
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=2)
    d.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], outline=GOLD, width=1)
    # peaks
    d.polygon([(cx - r + 12, cy + r - 16), (cx - r // 3, cy - r + 14), (cx + 2, cy + r - 22),
               (cx + r // 3, cy - r + 22), (cx + r - 12, cy + r - 16)],
              fill=NAVY)
    # snow caps
    d.polygon([(cx - r // 3 - 7, cy - r + 22), (cx - r // 3, cy - r + 14),
               (cx - r // 3 + 7, cy - r + 22)], fill=(240, 244, 250))
    d.polygon([(cx + r // 3 - 6, cy - r + 30), (cx + r // 3, cy - r + 22),
               (cx + r // 3 + 6, cy - r + 30)], fill=(240, 244, 250))
    # cloud line
    d.ellipse([cx - r + 10, cy + 2, cx - 8, cy + 14], fill=(255, 255, 255))
    d.ellipse([cx - 2, cy + 6, cx + r - 10, cy + 18], fill=(255, 255, 255))
    # star
    sx, sy, sr = cx, cy - r + 4, 5
    d.polygon([(sx, sy - sr), (sx + 1.6, sy - 1.6), (sx + sr, sy), (sx + 1.6, sy + 1.6),
               (sx, sy + sr), (sx - 1.6, sy + 1.6), (sx - sr, sy), (sx - 1.6, sy - 1.6)],
              fill=GOLD)
    # wave
    for k, yy in enumerate([cy + r - 12, cy + r - 7]):
        d.arc([cx - r + 12, yy - 4, cx + r - 12, yy + 6], 0, 180, fill=NAVY, width=2)


# ================================================================ portrait
def portrait(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 226, 232), outline=NAVY, width=2)
    # faint guilloche arcs behind the head
    for i in range(5):
        d.arc([x0 - 30 + i * 8, y0 - 10, x0 + w + 30 - i * 8, y0 + h // 2 + 20],
              200, 340, fill=(190, 205, 216), width=1)
    cx = x0 + w // 2
    # shoulders / high-collar coat (mountain-island dress)
    d.pieslice([cx - 62, y0 + h - 78, cx + 62, y0 + h + 30], 180, 360, fill=COAT)
    d.polygon([(cx - 62, y0 + h), (cx - 34, y0 + h - 62), (cx + 34, y0 + h - 62),
               (cx + 62, y0 + h)], fill=COAT)
    # shirt + collar
    d.polygon([(cx - 16, y0 + h - 58), (cx, y0 + h - 34), (cx + 16, y0 + h - 58),
               (cx + 8, y0 + h), (cx - 8, y0 + h)], fill=(244, 242, 236))
    d.polygon([(cx - 16, y0 + h - 58), (cx, y0 + h - 40), (cx - 4, y0 + h - 58)], fill=COAT)
    d.polygon([(cx + 16, y0 + h - 58), (cx, y0 + h - 40), (cx + 4, y0 + h - 58)], fill=COAT)
    # gold collar pin (cloud-line badge)
    d.ellipse([cx - 4, y0 + h - 46, cx + 4, y0 + h - 38], fill=GOLD)
    # neck
    d.rectangle([cx - 11, y0 + h - 84, cx + 11, y0 + h - 56], fill=SKIN_SH)
    # head
    d.ellipse([cx - 30, y0 + 26, cx + 30, y0 + 96], fill=SKIN)
    # hair: dark sweep, tied back — islander's knot
    d.pieslice([cx - 32, y0 + 20, cx + 32, y0 + 78], 180, 360, fill=HAIR)
    d.ellipse([cx - 32, y0 + 44, cx - 22, y0 + 78], fill=HAIR)
    d.ellipse([cx + 22, y0 + 44, cx + 32, y0 + 78], fill=HAIR)
    d.ellipse([cx - 6, y0 + 16, cx + 6, y0 + 30], fill=HAIR)   # top knot
    # brows, eyes
    d.line([(cx - 20, y0 + 58), (cx - 8, y0 + 56)], fill=HAIR, width=2)
    d.line([(cx + 8, y0 + 56), (cx + 20, y0 + 58)], fill=HAIR, width=2)
    d.ellipse([cx - 17, y0 + 60, cx - 11, y0 + 65], fill=(30, 28, 26))
    d.ellipse([cx + 11, y0 + 60, cx + 17, y0 + 65], fill=(30, 28, 26))
    # nose + mouth
    d.line([(cx, y0 + 64), (cx - 2, y0 + 76), (cx + 2, y0 + 76)], fill=SKIN_SH, width=2)
    d.arc([cx - 8, y0 + 80, cx + 8, y0 + 90], 20, 160, fill=(150, 84, 66), width=2)
    # photo corner marks
    for (mx, my, sx, sy) in [(x0, y0, 1, 1), (x0 + w, y0, -1, 1),
                             (x0, y0 + h, 1, -1), (x0 + w, y0 + h, -1, -1)]:
        d.line([(mx, my), (mx + 10 * sx, my)], fill=NAVY, width=2)
        d.line([(mx, my), (mx, my + 10 * sy)], fill=NAVY, width=2)


# ================================================================ MRZ check digits
VALS = {c: i for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
VALS["<"] = 0


def check(s):
    total = 0
    for i, ch in enumerate(s):
        total += VALS[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)


# ================================================================ LEFT PAGE — data page
centre(d, LX + PW // 2, 22, "REPUBLIC OF THALVERN", SERIF_B(21), NAVY)
centre(d, LX + PW // 2, 46, "Lýðveldið Thalvern  ·  PASSPORT — VEGABÓK", SANS(10), LABEL)
rule(d, LX + 14, 66, LX + PW - 14, GOLD, 2)
emblem(LX + 46, 100, 28)

text(d, (LX + 92, 90), "Type / Tegund", SANS(9), LABEL)
text(d, (LX + 92, 102), "P", SANS_B(15))
text(d, (LX + 172, 90), "Code / Land", SANS(9), LABEL)
text(d, (LX + 172, 102), "THV", SANS_B(15))
text(d, (LX + 248, 90), "Passport No. / Númer", SANS(9), LABEL)
text(d, (LX + 248, 102), "THV482913", SANS_B(15))

# portrait
portrait(LX + 14, 148, 132, 172)
text(d, (LX + 14, 322), "PHOTO — MYND", SANS(8), LABEL)

# data fields (right of portrait)
FX = LX + 162
fields = [
    ("SURNAME / ÆTTARNAFN", "THORNE"),
    ("GIVEN NAMES / FORNÖFN", "ELIN MARA"),
    ("NATIONALITY / ÞJÓÐERNI", "THALVERNIC"),
    ("DATE OF BIRTH / FÆÐINGARDAGUR", "02 JUN 1994"),
    ("PLACE OF BIRTH / FÆÐINGARSTAÐUR", "PORT KESTREL, THALVERN"),
    ("SEX / KYN", "F"),
    ("DATE OF ISSUE / ÚTGÁFUDAGUR", "14 MAR 2026"),
    ("DATE OF EXPIRY / GILDISTÍMI", "13 MAR 2036"),
    ("PLACE OF ISSUE / ÚTGÁFUSTAÐUR", "PORT KESTREL"),
]
y = 146
for label, value in fields:
    text(d, (FX, y), label, SANS(8), LABEL)
    text(d, (FX, y + 10), value, SANS_B(13))
    y += 25
# signature line
text(d, (FX, y + 2), "HOLDER'S SIGNATURE / UNDIRSKRIFT", SANS(8), LABEL)
d.line([(FX, y + 34), (FX + 210, y + 34)], fill=INK, width=1)
d.text((FX + 6, y + 14), "Elin Thorne", font=SERIF(14), fill=INK)

# telling paperwork detail — the visa condition, printed on the data page
cy = 412
rule(d, LX + 14, cy, LX + PW - 14, RULE, 1)
text(d, (LX + 14, cy + 8), "CONDITION / SKILYRÐI", SANS_B(9), NAVY)
text(d, (LX + 14, cy + 22),
     "This passport is valid only above 1,800 m. Descent below", SANS(11))
text(d, (LX + 14, cy + 37),
     "the cloud line voids all visas. Cloud tax is payable", SANS(11))
text(d, (LX + 14, cy + 52),
     "at every border post — 12 crowns per crossing.", SANS(11))

# MRZ
line1 = "P<THVTHORNE<<ELIN" + "<" * (44 - len("P<THVTHORNE<<ELIN"))
doc, dob, exp = "THV482913", "940602", "360313"
personal = "KST8841207THV<"           # 14 chars
body2 = doc + check(doc) + "THV" + dob + check(dob) + "F" + exp + check(exp) + personal
line2 = body2 + check(personal) + check(body2 + check(personal))
assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
mrz_y = 486
d.rectangle([LX + 14, mrz_y - 6, LX + PW - 14, mrz_y + 46], fill=(238, 234, 220))
text(d, (LX + 20, mrz_y), line1, MONO(14))
text(d, (LX + 20, mrz_y + 20), line2, MONO(14))
text(d, (LX + 14, mrz_y + 54), "P<THV482913 · ISSUING AUTHORITY: CLOUD OFFICE, PORT KESTREL",
     SANS(8), LABEL)
text(d, (LX + 14, H - 34), "PAGE 1 — DATA PAGE", SANS(8), LABEL)
text(d, (LX + PW - 14, H - 34), "THV482913", SANS(8), LABEL, anchor="ra")

# ================================================================ RIGHT PAGE — visa / stamp page
centre(d, RX + PW // 2, 22, "VISAS — VEGABRÉF", SERIF_B(21), NAVY)
centre(d, RX + PW // 2, 46, "Entries and exits · Koma og brottför", SANS(10), LABEL)
rule(d, RX + 14, 66, RX + PW - 14, GOLD, 2)


def stamp(cx, cy, w, h, color, top, mid, bottom, angle, shape="rect", bot_size=11):
    """A border stamp drawn on its own layer, rotated, pasted with alpha."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    ox, oy = 20, 20
    if shape == "oval":
        sd.ellipse([ox, oy, ox + w, oy + h], outline=color + (220,), width=3)
        sd.ellipse([ox + 6, oy + 6, ox + w - 6, oy + h - 6], outline=color + (220,), width=1)
    else:
        sd.rounded_rectangle([ox, oy, ox + w, oy + h], radius=8,
                             outline=color + (220,), width=3)
        sd.rounded_rectangle([ox + 5, oy + 5, ox + w - 5, oy + h - 5], radius=6,
                             outline=color + (200,), width=1)
    f_top = SANS_B(13)
    f_mid = SANS_B(15)
    f_bot = SANS(bot_size)
    sd.text((ox + w // 2, oy + 12), top, font=f_top, fill=color + (235,), anchor="ma")
    sd.text((ox + w // 2, oy + h // 2 - 4), mid, font=f_mid, fill=color + (235,), anchor="ma")
    sd.text((ox + w // 2, oy + h - 26), bottom, font=f_bot, fill=color + (235,), anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.paste(layer, (cx - layer.width // 2, cy - layer.height // 2), layer)


# 4 stamps, chronological travel order, all after 14 MAR 2026 issue
stamp(RX + 118, 158, 200, 84, STAMP_BLUE, "★ NORVASK ★", "ENTRY", "29 MAR 2026", -4, "oval")
stamp(RX + PW - 118, 158, 200, 84, STAMP_RED, "★ ILMAREN ★", "ENTRY", "13 APR 2026", 3, "oval")
stamp(RX + 118, 300, 200, 84, STAMP_GREEN, "★ SULDOR ★", "ENTRY", "01 MAY 2026", 5, "oval")
stamp(RX + PW - 118, 300, 200, 84, STAMP_PURPLE, "★ THALVERN ★", "RETURN", "19 MAY 2026", -3, "oval")

# route line — the journey in order
text(d, (RX + 14, 368), "ROUTE / FERÐALEIÐ:", SANS_B(10), NAVY)
text(d, (RX + 14, 386),
     "Port Kestrel → Hafen Norvask → Ilmaren City → Suldor Port → Port Kestrel",
     SANS(11))
text(d, (RX + 14, 404),
     "28 MAR – 19 MAY 2026 · 4 crossings · cloud tax paid at each post",
     SANS(11))
rule(d, RX + 14, 428, RX + PW - 14, RULE, 1)

# fee stamp — the telling detail
stamp(RX + PW // 2, 500, 320, 92, STAMP_RED, "CLOUD TAX PAID", "12 CROWNS", "VALID ONLY ABOVE 1,800 M", -2, "rect", bot_size=10)
text(d, (RX + 14, 566), "Fee stamp No. 0417 — Cloud Office, Port Kestrel. One crossing, one tax.", SANS(9), LABEL)
text(d, (RX + 14, 582), "No descent below the cloud line is permitted on this visa.", SANS(9), LABEL)

text(d, (RX + 14, H - 34), "PAGE 2 — VISAS", SANS(8), LABEL)
text(d, (RX + PW - 14, H - 34), "THV482913", SANS(8), LABEL, anchor="ra")

img.save(os.path.join(OUT, "entry.png"))
print("saved", os.path.join(OUT, "entry.png"), img.size)
