#!/usr/bin/env python3
"""Draw 'THE WORLD - ONE DAY', a broadsheet front page summing up
Tuesday 24 November 2026 world news. Pure PIL shapes + text, no downloads.
Output: entry.png, 1024x1024, under 1 MiB."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (248, 244, 233)
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (24, 63, 120)
TEAL = (14, 110, 110)
GOLD = (176, 132, 20)
GREY = (90, 86, 76)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, kind, x, y, s, color):
    """Simple vector-style glyph inside a coloured square."""
    d.rectangle([x, y, x + s, y + s], fill=color)
    c = (255, 255, 255)
    if kind == "globe":
        d.ellipse([x + 7, y + 7, x + s - 7, y + s - 7], outline=c, width=3)
        d.ellipse([x + 15, y + 7, x + s - 15, y + s - 7], outline=c, width=2)
        d.line([x + 7, y + s // 2, x + s - 7, y + s // 2], fill=c, width=2)
    elif kind == "quake":
        d.line([x + 8, y + s - 10, x + 16, y + 12, x + 24, y + s - 14,
                x + 32, y + 12, x + s - 8, y + s - 10], fill=c, width=3)
    elif kind == "tower":
        d.rectangle([x + s // 2 - 4, y + 8, x + s // 2 + 4, y + s - 8], fill=c)
        d.rectangle([x + 10, y + s - 12, x + s - 10, y + s - 8], fill=c)
        d.polygon([(x + s // 2, y + 2), (x + s // 2 - 6, y + 10),
                   (x + s // 2 + 6, y + 10)], fill=c)
    elif kind == "trophy":
        d.rectangle([x + 13, y + 10, x + s - 13, y + 26], outline=c, width=3)
        d.arc([x + 6, y + 10, x + 16, y + 24], 90, 270, fill=c, width=3)
        d.arc([x + s - 16, y + 10, x + s - 6, y + 24], 270, 90, fill=c, width=3)
        d.line([x + s // 2, y + 26, x + s // 2, y + 34], fill=c, width=3)
        d.line([x + 14, y + 34, x + s - 14, y + 34], fill=c, width=3)
    elif kind == "rocket":
        d.polygon([(x + s // 2, y + 6), (x + s // 2 - 8, y + 24),
                   (x + s // 2 + 8, y + 24)], fill=c)
        d.rectangle([x + s // 2 - 8, y + 22, x + s // 2 + 8, y + 32], fill=c)
        d.polygon([(x + s // 2 - 8, y + 30), (x + s // 2 - 14, y + 38),
                   (x + s // 2 - 8, y + 34)], fill=c)
        d.polygon([(x + s // 2 + 8, y + 30), (x + s // 2 + 14, y + 38),
                   (x + s // 2 + 8, y + 34)], fill=c)


# (kicker, headline, subhead, icon-or-None)
STORIES = [
    # Column 1 - World / Middle East / Asia
    ("WORLD", "ICJ: Myanmar guilty of Rohingya genocide",
     "UK, Spain, Canada and 11 more back it.", "globe"),
    ("UNITED NATIONS", "Guterres: AI risk rules within a year",
     "UN chief pledges AI safety rules in a year.", None),
    ("ASIA", "Quake M5.6 hits Nepal",
     "Tremor strikes Koshi province near China.", "quake"),
    ("MIDDLE EAST", "Drone hits Riyadh PIF tower",
     "Houthi drone wounds 11 in the capital.", "tower"),
    ("MIDDLE EAST", "Gaza land called \u201ctoxic\u201d",
     "Oxfam warns of poisoned soil; meningitis.", None),
    ("IRAN", "Singer gets 74 lashes",
     "Ahmadi punished; Tehran sets 7 terms.", None),
    # Column 2 - Europe / US / Tech
    ("EUROPE", "Ukraine hits Russian ship off Libya",
     "Tripoli demands an explanation from Kyiv.", None),
    ("EUROPE", "Zaporizhzhia hit again",
     "Plant hit overnight; NATO jets over Poland.", None),
    ("UNITED STATES", "Democrats take the House",
     "Democrats win the majority with 259 seats.", None),
    ("UNITED STATES", "Trump honours Giuliani",
     "Medal of Freedom awarded to Rudy Giuliani.", None),
    ("UNITED STATES", "DOJ recovers $8 billion",
     "800+ charged in biggest US fraud sweep.", None),
    ("TECH", "Huawei guilty of trade theft",
     "Guilty of trade theft; racketeering cleared.", None),
    # Column 3 - Americas / Sport / Climate / Space / Health
    ("AMERICAS", "25 held hostage in Cartagena",
     "Gunman seizes shoppers in Colombian market.", None),
    ("SPORT", "Senegal win AFCON",
     "Title secured after a successful CAS appeal.", "trophy"),
    ("SPORT", "Ronaldo reaches 987 goals",
     "The striker closes in on 1,000 career goals.", None),
    ("CLIMATE", "COP31 ends with no fossil call",
     "Summit closes without a fossil-fuel pledge.", None),
    ("SPACE", "Tiangong opens to foreigners",
     "First foreign astronauts fly from Pakistan.", "rocket"),
    ("HEALTH", "US measles nears 6,000 cases",
     "Ninth death reported in Pennsylvania.", None),
]

TIMELINE = [
    "ICJ genocide ruling",
    "Nepal quake M5.6",
    "Riyadh drone strike",
    "Democrats take House",
    "Senegal win AFCON",
    "COP31 closes",
]

MARKETS = [
    ("S&P 500", "+4.7%"),
    ("Nasdaq", "+6.5%"),
    ("Nikkei", "+3.9%"),
    ("Brent", "$86.7"),
    ("Gold", "$3,620"),
]

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- Masthead ----
d.rectangle([0, 0, W, 10], fill=INK)
d.text((W // 2, 52), "THE WORLD", font=font(SERIF_B, 96), fill=INK, anchor="mt")
d.line([28, 132, W - 28, 132], fill=INK, width=3)
d.text((W // 2, 150), "TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 30),
       fill=RED, anchor="mt")
d.text((W // 2, 188), "The world in one day  \u2014  24 November 2026",
       font=font(SERIF, 22), fill=INK, anchor="mt")
d.line([28, 222, W - 28, 222], fill=INK, width=3)

# ---- Story columns ----
COLS = [STORIES[0:6], STORIES[6:12], STORIES[12:18]]
COL_X = [28, 356, 684]
COL_W = 312
TOP = 238
BOTTOM = 812
for ci, col in enumerate(COLS):
    x = COL_X[ci]
    y = TOP
    n = len(col)
    slot = (BOTTOM - TOP) // n
    for kicker, head, sub, icon in col:
        # kicker
        d.text((x, y), kicker, font=font(SANS_B, 13), fill=RED)
        hy = y + 18
        tx = x
        if icon:
            draw_icon(d, icon, x, hy, 40, BLUE if icon != "trophy" else GOLD)
            tx = x + 48
        hw = COL_W - (48 if icon else 0)
        lines = wrap(d, head, font(SERIF_B, 22), hw)[:2]
        ly = hy
        for ln in lines:
            d.text((tx, ly), ln, font=font(SERIF_B, 22), fill=INK)
            ly += 25
        sub_lines = wrap(d, sub, font(SANS, 13), COL_W)[:1]
        sy = ly + 2
        if icon:
            sy = max(sy, hy + 44)
        for ln in sub_lines:
            d.text((x, sy), ln, font=font(SANS, 13), fill=(52, 48, 40))
            sy += 18
        y += slot
        if y < BOTTOM - 4:
            d.line([x, y - 6, x + COL_W, y - 6], fill=(200, 192, 172), width=1)
    if ci < 2:
        d.line([COL_X[ci] + COL_W + 8, TOP, COL_X[ci] + COL_W + 8, BOTTOM],
               fill=(200, 192, 172), width=1)

# ---- UTC timeline strip ----
d.line([28, 828, W - 28, 828], fill=INK, width=2)
d.text((28, 838), "UTC TIMELINE  \u2014  THE DAY IN ORDER",
       font=font(SANS_B, 16), fill=INK)
d.line([48, 892, W - 48, 892], fill=INK, width=2)
for i, ev in enumerate(TIMELINE):
    cx = 80 + i * 160
    d.ellipse([cx - 7, 885, cx + 7, 899], fill=RED)
    d.text((cx, 908), ev, font=font(SANS_B, 12), fill=INK, anchor="mt")
    d.text((cx, 924), str(i + 1), font=font(SANS_B, 12), fill=GREY, anchor="mt")
for h, lx in [(0, 48), (6, 264), (12, 480), (18, 696), (24, 952)]:
    d.text((lx, 946), f"{h:02d}:00 UTC", font=font(SANS, 11), fill=GREY, anchor="ma")

# ---- Markets strip ----
d.rectangle([28, 968, W - 28, 1004], fill=INK)
mx = 44
d.text((mx, 978), "MARKETS", font=font(SANS_B, 16), fill=(255, 210, 90))
mx += 108
for name, val in MARKETS:
    d.text((mx, 978), f"{name} {val}", font=font(SANS_B, 16), fill=(255, 255, 255))
    mx += d.textlength(f"{name} {val}", font=font(SANS_B, 16)) + 26

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
