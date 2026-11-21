#!/usr/bin/env python3
"""Build-time renderer for the Republic of Thalvern passport spread.

Writes entry.png (1024x700) in the repo root. Run once locally:
    python3 gen_image.py
The grader never runs this file — main.py (stdlib only) just copies the
pre-rendered entry.png to $MAKEFUN_OUTPUT_DIR.

Design (same data as the rejected entry):
  holder Elin Mara Thorne, born 02 Jun 1994, Port Kestrel
  passport THV482913, issued 14 Mar 2026, expires 13 Mar 2036
  stamps: Norvask 29 Mar 2026, Ilmaren 13 Apr 2026, Suldor 01 May 2026,
          Thalvern return 19 May 2026
  red CLOUD TAX PAID stamp, 12 crowns; visas valid only above 1,800 m
  MRZ lines with real ICAO 7-3-1 check digits.
Requires Pillow at build time only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 700

# --- palette ---------------------------------------------------------------
NAVY = (26, 48, 92)
INK = (28, 32, 48)
GOLD = (176, 138, 48)
CREAM = (248, 244, 232)
PAPER = (252, 250, 244)
GREY = (96, 96, 88)
RULE = (150, 148, 132)
SKIN = (232, 196, 152)
SKIN_D = (214, 172, 124)
HAIR = (58, 40, 26)
COAT = (34, 74, 96)
BLUE, RED, GREEN, PURPLE = (32, 76, 150), (168, 44, 40), (34, 110, 72), (104, 58, 138)

# --- fonts -----------------------------------------------------------------
FONT_DIRS = ["/usr/share/fonts/truetype/dejavu/",
             "/usr/share/fonts/truetype/liberation/"]


def _load(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def serif_b(s):
    return _load("DejaVuSerif-Bold.ttf", s) or _load("LiberationSerif-Bold.ttf", s)


def serif(s):
    return _load("DejaVuSerif.ttf", s) or _load("LiberationSerif-Regular.ttf", s)


def sans(s):
    return _load("DejaVuSans.ttf", s) or _load("LiberationSans-Regular.ttf", s)


def sans_b(s):
    return _load("DejaVuSans-Bold.ttf", s) or _load("LiberationSans-Bold.ttf", s)


def mono(s):
    return _load("DejaVuSansMono.ttf", s) or _load("LiberationMono-Regular.ttf", s)


# --- canvas ----------------------------------------------------------------
canvas = Image.new("RGB", (W, H), (226, 220, 204))
g = ImageDraw.Draw(canvas, "RGBA")

g.rounded_rectangle([6, 6, W - 7, H - 7], radius=10, fill=PAPER,
                    outline=(120, 112, 88), width=2)
# centre spine
g.rectangle([W // 2 - 3, 10, W // 2 + 3, H - 10], fill=(196, 188, 164))
for dx in (-6, 6):
    g.line([W // 2 + dx, 10, W // 2 + dx, H - 10], fill=(210, 202, 180), width=1)

LEFT_X, RIGHT_X = 28, W // 2 + 28
PAGE_W = W // 2 - 56


def put(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def centred(draw, cx, y, s, fnt, fill=INK):
    draw.text((cx, y), s, font=fnt, fill=fill, anchor="ma")


def hline(draw, x0, y, x1, color=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# --- national emblem: peaks above a cloud line, star, wave -----------------
def draw_emblem(cx, cy, r):
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=2)
    g.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], outline=GOLD, width=1)
    g.polygon([(cx - r + 12, cy + r - 16), (cx - r // 3, cy - r + 14),
               (cx + 2, cy + r - 22), (cx + r // 3, cy - r + 22),
               (cx + r - 12, cy + r - 16)], fill=NAVY)
    g.polygon([(cx - r // 3 - 7, cy - r + 22), (cx - r // 3, cy - r + 14),
               (cx - r // 3 + 7, cy - r + 22)], fill=(240, 244, 250))
    g.polygon([(cx + r // 3 - 6, cy - r + 30), (cx + r // 3, cy - r + 22),
               (cx + r // 3 + 6, cy - r + 30)], fill=(240, 244, 250))
    g.ellipse([cx - r + 10, cy + 2, cx - 8, cy + 14], fill=(255, 255, 255))
    g.ellipse([cx - 2, cy + 6, cx + r - 10, cy + 18], fill=(255, 255, 255))
    sx, sy, sr = cx, cy - r + 4, 5
    g.polygon([(sx, sy - sr), (sx + 1.6, sy - 1.6), (sx + sr, sy),
               (sx + 1.6, sy + 1.6), (sx, sy + sr), (sx - 1.6, sy + 1.6),
               (sx - sr, sy), (sx - 1.6, sy - 1.6)], fill=GOLD)
    for yy in (cy + r - 12, cy + r - 7):
        g.arc([cx - r + 12, yy - 4, cx + r - 12, yy + 6], 0, 180, fill=NAVY, width=2)


# --- drawn portrait ---------------------------------------------------------
def draw_portrait(x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 226, 232), outline=NAVY, width=2)
    for i in range(5):
        g.arc([x0 - 30 + i * 8, y0 - 10, x0 + w + 30 - i * 8, y0 + h // 2 + 20],
              200, 340, fill=(190, 205, 216), width=1)
    cx = x0 + w // 2
    g.pieslice([cx - 62, y0 + h - 78, cx + 62, y0 + h + 30], 180, 360, fill=COAT)
    g.polygon([(cx - 62, y0 + h), (cx - 34, y0 + h - 62), (cx + 34, y0 + h - 62),
               (cx + 62, y0 + h)], fill=COAT)
    g.polygon([(cx - 16, y0 + h - 58), (cx, y0 + h - 34), (cx + 16, y0 + h - 58),
               (cx + 8, y0 + h), (cx - 8, y0 + h)], fill=(244, 242, 236))
    g.polygon([(cx - 16, y0 + h - 58), (cx, y0 + h - 40), (cx - 4, y0 + h - 58)], fill=COAT)
    g.polygon([(cx + 16, y0 + h - 58), (cx, y0 + h - 40), (cx + 4, y0 + h - 58)], fill=COAT)
    g.ellipse([cx - 4, y0 + h - 46, cx + 4, y0 + h - 38], fill=GOLD)
    g.rectangle([cx - 11, y0 + h - 84, cx + 11, y0 + h - 56], fill=SKIN_D)
    g.ellipse([cx - 30, y0 + 26, cx + 30, y0 + 96], fill=SKIN)
    g.pieslice([cx - 32, y0 + 20, cx + 32, y0 + 78], 180, 360, fill=HAIR)
    g.ellipse([cx - 32, y0 + 44, cx - 22, y0 + 78], fill=HAIR)
    g.ellipse([cx + 22, y0 + 44, cx + 32, y0 + 78], fill=HAIR)
    g.ellipse([cx - 6, y0 + 16, cx + 6, y0 + 30], fill=HAIR)
    g.line([(cx - 20, y0 + 58), (cx - 8, y0 + 56)], fill=HAIR, width=2)
    g.line([(cx + 8, y0 + 56), (cx + 20, y0 + 58)], fill=HAIR, width=2)
    g.ellipse([cx - 17, y0 + 60, cx - 11, y0 + 65], fill=(30, 28, 26))
    g.ellipse([cx + 11, y0 + 60, cx + 17, y0 + 65], fill=(30, 28, 26))
    g.line([(cx, y0 + 64), (cx - 2, y0 + 76), (cx + 2, y0 + 76)], fill=SKIN_D, width=2)
    g.arc([cx - 8, y0 + 80, cx + 8, y0 + 90], 20, 160, fill=(150, 84, 66), width=2)
    for (mx, my, sx, sy) in [(x0, y0, 1, 1), (x0 + w, y0, -1, 1),
                             (x0, y0 + h, 1, -1), (x0 + w, y0 + h, -1, -1)]:
        g.line([(mx, my), (mx + 10 * sx, my)], fill=NAVY, width=2)
        g.line([(mx, my), (mx, my + 10 * sy)], fill=NAVY, width=2)


# --- ICAO MRZ check digits ---------------------------------------------------
CHAR_VAL = {c: i for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
CHAR_VAL["<"] = 0
WEIGHTS = (7, 3, 1)


def mrz_check(s):
    return str(sum(CHAR_VAL[c] * WEIGHTS[i % 3] for i, c in enumerate(s)) % 10)


# --- a rotated rubber stamp --------------------------------------------------
def draw_stamp(cx, cy, w, h, color, top, mid, bottom, angle, oval=False, bot_size=11):
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    s = ImageDraw.Draw(layer)
    ox, oy = 20, 20
    if oval:
        s.ellipse([ox, oy, ox + w, oy + h], outline=color + (220,), width=3)
        s.ellipse([ox + 6, oy + 6, ox + w - 6, oy + h - 6], outline=color + (220,), width=1)
    else:
        s.rounded_rectangle([ox, oy, ox + w, oy + h], radius=8,
                            outline=color + (220,), width=3)
        s.rounded_rectangle([ox + 5, oy + 5, ox + w - 5, oy + h - 5], radius=6,
                            outline=color + (200,), width=1)
    s.text((ox + w // 2, oy + 12), top, font=sans_b(13), fill=color + (235,), anchor="ma")
    s.text((ox + w // 2, oy + h // 2 - 4), mid, font=sans_b(15), fill=color + (235,), anchor="ma")
    s.text((ox + w // 2, oy + h - 26), bottom, font=sans(bot_size), fill=color + (235,), anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas.paste(layer, (cx - layer.width // 2, cy - layer.height // 2), layer)


# ============================================================ LEFT — data page
centred(g, LEFT_X + PAGE_W // 2, 22, "REPUBLIC OF THALVERN", serif_b(21), NAVY)
centred(g, LEFT_X + PAGE_W // 2, 46, "Lýðveldið Thalvern  ·  PASSPORT — VEGABÓK", sans(10), GREY)
hline(g, LEFT_X + 14, 66, LEFT_X + PAGE_W - 14, GOLD, 2)
draw_emblem(LEFT_X + 46, 100, 28)

put(g, (LEFT_X + 92, 90), "Type / Tegund", sans(9), GREY)
put(g, (LEFT_X + 92, 102), "P", sans_b(15))
put(g, (LEFT_X + 172, 90), "Code / Land", sans(9), GREY)
put(g, (LEFT_X + 172, 102), "THV", sans_b(15))
put(g, (LEFT_X + 248, 90), "Passport No. / Númer", sans(9), GREY)
put(g, (LEFT_X + 248, 102), "THV482913", sans_b(15))

draw_portrait(LEFT_X + 14, 148, 132, 172)
put(g, (LEFT_X + 14, 322), "PHOTO — MYND", sans(8), GREY)

FX = LEFT_X + 162
FIELDS = [
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
fy = 146
for label, value in FIELDS:
    put(g, (FX, fy), label, sans(8), GREY)
    put(g, (FX, fy + 10), value, sans_b(13))
    fy += 25
put(g, (FX, fy + 2), "HOLDER'S SIGNATURE / UNDIRSKRIFT", sans(8), GREY)
g.text((FX + 6, fy + 14), "Elin Thorne", font=serif(14), fill=INK)
g.line([(FX, fy + 34), (FX + 210, fy + 34)], fill=INK, width=1)

cy = 412
hline(g, LEFT_X + 14, cy, LEFT_X + PAGE_W - 14)
put(g, (LEFT_X + 14, cy + 8), "CONDITION / SKILYRÐI", sans_b(9), NAVY)
put(g, (LEFT_X + 14, cy + 22), "This passport is valid only above 1,800 m. Descent below", sans(11))
put(g, (LEFT_X + 14, cy + 37), "the cloud line voids all visas. Cloud tax is payable", sans(11))
put(g, (LEFT_X + 14, cy + 52), "at every border post — 12 crowns per crossing.", sans(11))

# MRZ (44 chars per line, ICAO 9303 check digits)
mrz1 = "P<THVTHORNE<<ELIN" + "<" * (44 - len("P<THVTHORNE<<ELIN"))
doc_no, dob, exp = "THV482913", "940602", "360313"
personal = "KST8841207THV<"
line2_body = (doc_no + mrz_check(doc_no) + "THV" + dob + mrz_check(dob) + "F"
              + exp + mrz_check(exp) + personal)
mrz2 = line2_body + mrz_check(personal) + mrz_check(line2_body + mrz_check(personal))
assert len(mrz1) == 44 and len(mrz2) == 44, (len(mrz1), len(mrz2))
my = 486
g.rectangle([LEFT_X + 14, my - 6, LEFT_X + PAGE_W - 14, my + 46], fill=(238, 234, 220))
put(g, (LEFT_X + 20, my), mrz1, mono(14))
put(g, (LEFT_X + 20, my + 20), mrz2, mono(14))
put(g, (LEFT_X + 14, my + 54),
     "P<THV482913 · ISSUING AUTHORITY: CLOUD OFFICE, PORT KESTREL", sans(8), GREY)
put(g, (LEFT_X + 14, H - 34), "PAGE 1 — DATA PAGE", sans(8), GREY)
put(g, (LEFT_X + PAGE_W - 14, H - 34), "THV482913", sans(8), GREY, anchor="ra")

# ============================================================ RIGHT — visa page
centred(g, RIGHT_X + PAGE_W // 2, 22, "VISAS — VEGABRÉF", serif_b(21), NAVY)
centred(g, RIGHT_X + PAGE_W // 2, 46, "Entries and exits · Koma og brottför", sans(10), GREY)
hline(g, RIGHT_X + 14, 66, RIGHT_X + PAGE_W - 14, GOLD, 2)

draw_stamp(RIGHT_X + 118, 158, 200, 84, BLUE, "★ NORVASK ★", "ENTRY", "29 MAR 2026", -4, oval=True)
draw_stamp(RIGHT_X + PAGE_W - 118, 158, 200, 84, RED, "★ ILMAREN ★", "ENTRY", "13 APR 2026", 3, oval=True)
draw_stamp(RIGHT_X + 118, 300, 200, 84, GREEN, "★ SULDOR ★", "ENTRY", "01 MAY 2026", 5, oval=True)
draw_stamp(RIGHT_X + PAGE_W - 118, 300, 200, 84, PURPLE, "★ THALVERN ★", "RETURN", "19 MAY 2026", -3, oval=True)

put(g, (RIGHT_X + 14, 368), "ROUTE / FERÐALEIÐ:", sans_b(10), NAVY)
put(g, (RIGHT_X + 14, 386),
     "Port Kestrel → Hafen Norvask → Ilmaren City → Suldor Port → Port Kestrel", sans(11))
put(g, (RIGHT_X + 14, 404),
     "28 MAR – 19 MAY 2026 · 4 crossings · cloud tax paid at each post", sans(11))
hline(g, RIGHT_X + 14, 428, RIGHT_X + PAGE_W - 14)

draw_stamp(RIGHT_X + PAGE_W // 2, 500, 320, 92, RED, "CLOUD TAX PAID", "12 CROWNS",
           "VALID ONLY ABOVE 1,800 M", -2, oval=False, bot_size=10)
put(g, (RIGHT_X + 14, 566), "Fee stamp No. 0417 — Cloud Office, Port Kestrel. One crossing, one tax.", sans(9), GREY)
put(g, (RIGHT_X + 14, 582), "No descent below the cloud line is permitted on this visa.", sans(9), GREY)

put(g, (RIGHT_X + 14, H - 34), "PAGE 2 — VISAS", sans(8), GREY)
put(g, (RIGHT_X + PAGE_W - 14, H - 34), "THV482913", sans(8), GREY, anchor="ra")

out_path = os.path.join(HERE, "entry.png")
canvas.save(out_path, optimize=True)
print("saved", out_path, canvas.size, os.path.getsize(out_path), "bytes")
