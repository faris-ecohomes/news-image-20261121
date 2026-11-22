#!/usr/bin/env python3
"""News poster for Saturday 21 November 2026.

Draws a 1024x1024 newspaper front page summarising the day's world news:
16 illustrated panels, a UTC timeline, a numbered world map, a 34-item
"ALSO ON" list and a DATE CHECK box. Only the Python standard library
and Pillow are used; there is no network access, no clock and no
randomness, so two runs write byte-identical PNGs.

Run:  python3 main.py
Writes: $MAKEFUN_OUTPUT_DIR/entry.png  (default /output/entry.png)
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER = (252, 248, 235)
INK = (26, 26, 26)
MUTED = (90, 84, 70)
RED = (164, 31, 31)
DARKRED = (120, 20, 20)
BLUE = (31, 78, 121)
TEAL = (14, 110, 110)
GREEN = (46, 110, 60)
ORANGE = (196, 90, 20)
PURPLE = (96, 60, 130)
GOLD = (176, 132, 20)
RULE = (180, 168, 140)
LIGHT = (238, 230, 208)

REGION_COLORS = {
    "MIDDLE EAST": RED,
    "N. AMERICA": (30, 90, 140),
    "EUROPE": BLUE,
    "UKRAINE WAR": (120, 40, 40),
    "MARKETS": (20, 90, 70),
    "CLIMATE": TEAL,
    "S. AMERICA": GREEN,
    "SPACE": PURPLE,
    "SPORT": ORANGE,
    "USA": (30, 90, 140),
    "ASIA": (150, 90, 20),
    "WORLD": (70, 70, 70),
}

# (number, region, topic, chip, headline, detail, icon, map lon/lat or None)
PANELS = [
    (1, "MIDDLE EAST", "CONFLICT", "CLAIM - IRGC",
     "Iran says it struck US bases in Bahrain",
     "Tehran claims hits at al-Riffa and Awali; Bahrain reports a fire at a civilian industrial site, no injuries.",
     "missile", (50.6, 26.2)),
    (2, "N. AMERICA", "JUSTICE", "CONFIRMED - AP",
     "Mexico captures 'El Chapo Isidro'",
     "FBI most-wanted cartel boss Fausto Isidro Meza Flores seized in Sinaloa; at least 11 die in the backlash.",
     "cuffs", (-108.5, 25.6)),
    (3, "UKRAINE WAR", "STRIKE", "CONFIRMED - AP",
     "Russian missile hits Zelenskyy's hometown",
     "Ballistic strike on Kryvyi Rih kills a boy of 7 and a woman of 20 and wounds 60 in a double-tap attack.",
     "blast", (33.4, 47.9)),
    (4, "EUROPE", "NATO", "CONFIRMED - AP",
     "Trump shrugs off Russian missiles in Poland",
     "Two missiles and a drone fell in SE Poland on Friday; Tusk calls it an 'intentional provocation'.",
     "flag", (21.8, 50.3)),
    (5, "MARKETS", "STOCKS", "CONFIRMED - UPI",
     "AI sell-off drags US stocks into correction",
     "S&P 500 down 3.7% on the week; Nasdaq wipes out its 2026 gains as chip shares plunge again.",
     "chart", (-74.0, 40.7)),
    (6, "CLIMATE", "COP31", "CONFIRMED - AP",
     "COP31 talks run into overtime, no deal",
     "Antalya summit passes its deadline; draft deal still omits fossil fuels as nearly 200 states argue.",
     "leaf", (30.7, 36.9)),
    (7, "EUROPE", "BALTIC", "CONFIRMED - BBC",
     "Drones set Russian cargo ship ablaze",
     "Sanctioned Sparta II, bound for Kaliningrad, catches fire in the Gulf of Finland and drifts toward Finnish waters.",
     "ship", (24.5, 59.8)),
    (8, "MIDDLE EAST", "SHIPPING", "CONFIRMED - AP",
     "Three tankers struck near Strait of Hormuz",
     "Attacks in or near the strait raise Gulf shipping risks; no casualties reported as oil holds near $90.",
     "tanker", (56.3, 26.5)),
    (9, "MIDDLE EAST", "GAZA", "CONFIRMED - AL JAZEERA",
     "Israeli strike kills three in Gaza food vehicle",
     "Air strike hits a food truck in Gaza City; Israel says the dead were militants. Six hurt in other breaches.",
     "aid", (34.5, 31.5)),
    (10, "MIDDLE EAST", "YEMEN", "CONFIRMED - AP",
     "Houthis and Saudi coalition trade strikes",
     "Riyadh intercepts missiles aimed at the kingdom; coalition hits Hodeidah as the Houthis claim 71 raids.",
     "burst", (46.7, 24.7)),
    (11, "S. AMERICA", "QUAKE", "CONFIRMED - USGS",
     "Magnitude 6.7 quake shakes central Peru",
     "Tremor strikes Junin at 00:09 UTC, felt in Lima; no deaths or serious damage in early reports.",
     "quake", (-76.0, -11.1)),
    (12, "SPACE", "MERCURY", "CONFIRMED - AP",
     "BepiColombo enters orbit around Mercury",
     "European-Japanese craft arrives after an eight-year, 10-billion-km cruise; only the second to orbit the planet.",
     "craft", None),
    (13, "USA", "ECONOMY", "CONFIRMED - AP",
     "Trump vows 10% cap on credit card rates",
     "President says he will work with the incoming Democratic Congress; median card rate is about 22%.",
     "card", (-77.0, 38.9)),
    (14, "USA", "CYBER", "CONFIRMED - AP",
     "FBI probes hack of police crime database",
     "Apparent breach of the National Crime Information Center is the second major FBI breach in two months.",
     "lock", (-77.0, 38.9)),
    (15, "SPORT", "FOOTBALL", "CONFIRMED - BBC",
     "Leeds stun Chelsea 4-1 at the Bridge",
     "First Leeds win at Stamford Bridge since 1999; Okafor scores twice as Xabi Alonso's Blues slump.",
     "ball", (-0.1, 51.5)),
    (16, "EUROPE", "ESPIONAGE", "CONFIRMED - BBC",
     "Denmark expels Russian diplomat over plot",
     "Defence attache expelled over an alleged plan to kill US-Ukrainian rapper Kyivstoner; Moscow denies it.",
     "spy", (12.6, 55.7)),
]

TIMELINE = [
    ("00:09 UTC", "6.7 quake shakes central Peru, felt in Lima"),
    ("OVERNIGHT", "Russian missile kills 2 in Kryvyi Rih"),
    ("MORNING", "Mexico captures 'El Chapo Isidro'"),
    ("MIDDAY", "COP31 passes deadline, still no deal"),
    ("AFTERNOON", "Leeds stun Chelsea 4-1 at the Bridge"),
    ("EVENING", "Iran says it struck US bases in Bahrain"),
]

ALSO_ON = [
    "Newcastle 2-2 Arsenal: Madueke rescues a point",
    "Man City held 1-1 by Fulham at the Etihad",
    "Alcaraz beats Shelton, faces Zverev in ATP final",
    "England 37-12 All Blacks, a record margin",
    "Wallabies edge Wales 29-26 in Cardiff",
    "Harden scores 51, passes Kobe on 50-pt list",
    "Verstappen on Las Vegas GP pole after penalty",
    "Kane out for months with ankle ligament tear",
    "A Lim Kim hole-in-one leads LPGA finale",
    "Canada takes four short-track medals in Seoul",
    "Cavalry FC win Canadian Premier League title",
    "Bolsonaro in intensive care, bowel obstruction",
    "Nigeria boat capsizes, at least 24 dead",
    "Virginia reports first measles death of 2026",
    "Man convicted of starting deadly Palisades fire",
    "EU and Indonesia sign trade deal after 10 years",
    "UK and EU sign three post-Brexit agreements",
    "French police sentenced over 2020 Zecler beating",
    "Trump threatens tax on firms building data centres abroad",
    "Nvidia chief ousted; Trump says he raised it with Xi",
    "UN talks agree to keep working on AI-weapons rules",
    "Tanzania opposition leader Lissu guilty of sedition",
    "Uganda restricts gatherings over Ebola fears",
    "Saudi Arabia and Japan agree oil stockpile deal",
    "Argentina bonds slide into distressed territory",
    "Fire at Basra power station kills four",
    "BTS win five awards at MAMA in Osaka",
    "UK defence chief in Kyiv backs Ukraine",
    "Princess Catherine reflects on cancer in new film",
    "Thunberg joins Tirana student march for Rama exit",
    "Voters oust sheriffs who aided Trump deportations",
    "Storms bring historic flooding to Florida",
    "San Francisco braces for massive tides",
    "Lewis Pugh swims 15 km through Strait of Hormuz",
]

DATE_CHECK_BEFORE = (
    "ICJ Myanmar genocide ruling (19 Nov) - Shenzhen Trump-Xi-Putin summit (19 Nov) - "
    "Anthropic record $81.3bn IPO debut (19 Nov) - Riemann-proof claim (first reported 20 Nov) - "
    "Fiona the hippo dies (19 Nov) - Brazil storm kills 3 (20 Nov)"
)
DATE_CHECK_FUTURE = (
    "Nepal PM's India visit (22-23 Nov) - Spain election (29 Nov) - Estonia border shutdown (1 Dec) - "
    "ATP final & Las Vegas GP (Sun 22 Nov) - Rikers Island closure (2032)"
)

# Coarse continent outlines as (lon, lat) polygons, for the schematic map.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-115, 73), (-100, 75), (-90, 80), (-80, 75),
     (-70, 62), (-60, 55), (-55, 47), (-65, 44), (-70, 42), (-75, 36), (-80, 27),
     (-85, 20), (-90, 14), (-95, 16), (-100, 19), (-108, 23), (-115, 29), (-122, 38),
     (-125, 48), (-135, 58), (-150, 60), (-162, 58), (-168, 62)],
    [(-58, 62), (-48, 60), (-40, 64), (-32, 68), (-25, 70), (-32, 76), (-50, 76),
     (-58, 72), (-60, 66)],
    [(-80, 9), (-76, 4), (-70, 11), (-62, 8), (-55, 4), (-50, 0), (-44, -3),
     (-38, -8), (-40, -18), (-47, -26), (-55, -34), (-64, -40), (-70, -48),
     (-74, -54), (-71, -44), (-73, -34), (-78, -22), (-81, -12), (-84, -4)],
    [(-10, 35), (-2, 35), (8, 37), (18, 33), (28, 31), (34, 28), (38, 20),
     (43, 12), (51, 11), (46, 2), (40, -4), (36, -14), (32, -22), (27, -30),
     (20, -35), (16, -30), (13, -20), (10, -8), (6, 4), (-2, 5), (-9, 6),
     (-15, 11), (-17, 15), (-16, 22), (-14, 28)],
    [(-10, 36), (-8, 43), (-2, 48), (0, 50), (3, 53), (7, 57), (10, 59),
     (13, 56), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (28, 66),
     (32, 70), (40, 68), (44, 66), (40, 60), (35, 55), (30, 50), (28, 46),
     (24, 44), (22, 40), (26, 38), (30, 36), (24, 36), (19, 41), (14, 45),
     (8, 44), (3, 42), (-1, 38)],
    [(32, 36), (38, 38), (44, 40), (48, 44), (52, 48), (58, 52), (64, 56),
     (68, 62), (70, 68), (78, 72), (88, 74), (98, 76), (108, 76), (118, 73),
     (128, 72), (138, 72), (150, 70), (160, 67), (170, 66), (178, 65),
     (170, 60), (162, 56), (156, 51), (150, 46), (142, 42), (136, 36),
     (130, 33), (126, 28), (122, 24), (118, 20), (112, 14), (108, 8),
     (104, 2), (100, 5), (96, 8), (92, 14), (88, 20), (82, 18), (78, 14),
     (74, 22), (70, 24), (66, 25), (60, 25), (56, 26), (52, 28), (48, 30),
     (44, 30), (40, 32), (36, 36)],
    [(113, -22), (114, -30), (119, -34), (128, -32), (136, -35), (143, -38),
     (150, -37), (153, -28), (150, -22), (146, -17), (142, -11), (136, -12),
     (131, -13), (126, -14), (121, -18), (115, -21)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (145, 44),
     (143, 42), (140, 36), (135, 33), (131, 32)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -9),
     (130, -4), (135, -2), (140, -5), (136, -8), (130, -5), (125, -2),
     (120, 0), (115, 3), (110, 5), (105, 2), (100, 5)],
]

# ---------------------------------------------------------------- fonts ---

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
]


def font(bold, serif, size):
    for path in FONT_PATHS:
        want_serif = "Serif" in path
        want_bold = "Bold" in path
        if want_serif == serif and want_bold == bold:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK):
    draw.text(xy, s, font=fnt, fill=fill)


def centered(draw, cx, y, s, fnt, fill=INK):
    w = draw.textlength(s, font=fnt)
    draw.text((cx - w / 2, y), s, font=fnt, fill=fill)


# --------------------------------------------------------------- icons ---

def draw_icon(d, kind, x, y, s):
    """Flat vector-style mini illustration inside a s x s box at (x, y)."""
    if kind == "missile":
        d.polygon([(x + s * .55, y + s * .05), (x + s * .85, y + s * .35),
                   (x + s * .55, y + s * .65), (x + s * .35, y + s * .45)],
                  fill=(120, 120, 120))
        d.polygon([(x + s * .35, y + s * .45), (x + s * .55, y + s * .65),
                   (x + s * .25, y + s * .85), (x + s * .15, y + s * .75)],
                  fill=ORANGE)
        d.ellipse([x + s * .05, y + s * .6, x + s * .3, y + s * .85], fill=(230, 180, 40))
        for i, yy in enumerate((0.15, 0.4, 0.65)):
            d.line([x + s * .05, y + s * yy, x + s * .25, y + s * yy],
                   fill=MUTED, width=2)
    elif kind == "cuffs":
        d.ellipse([x + s * .08, y + s * .25, x + s * .42, y + s * .6],
                  outline=INK, width=4)
        d.ellipse([x + s * .58, y + s * .25, x + s * .92, y + s * .6],
                  outline=INK, width=4)
        d.line([x + s * .42, y + s * .42, x + s * .58, y + s * .42],
               fill=INK, width=4)
        d.ellipse([x + s * .2, y + s * .37, x + s * .3, y + s * .47], fill=RED)
        d.ellipse([x + s * .7, y + s * .37, x + s * .8, y + s * .47], fill=RED)
    elif kind == "blast":
        cx, cy = x + s * .5, y + s * .5
        for ang in range(0, 360, 45):
            import math
            r1, r2 = s * .18, s * .48
            a = math.radians(ang)
            d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                    cx + r2 * math.cos(a), cy + r2 * math.sin(a)],
                   fill=ORANGE, width=5)
        d.ellipse([cx - s * .2, cy - s * .2, cx + s * .2, cy + s * .2],
                  fill=(230, 180, 40))
        d.ellipse([cx - s * .1, cy - s * .1, cx + s * .1, cy + s * .1], fill=RED)
    elif kind == "flag":
        d.rectangle([x + s * .1, y + s * .15, x + s * .9, y + s * .45], fill=(245, 245, 245),
                    outline=INK, width=2)
        d.rectangle([x + s * .1, y + s * .3, x + s * .9, y + s * .45], fill=RED,
                    outline=INK, width=2)
        d.line([x + s * .1, y + s * .15, x + s * .1, y + s * .9], fill=INK, width=3)
        d.polygon([(x + s * .45, y + s * .62), (x + s * .6, y + s * .85),
                   (x + s * .3, y + s * .85)], fill=GOLD, outline=INK)
        d.text((x + s * .44, y + s * .68), "!", font=font(True, False, 14), fill=INK)
    elif kind == "chart":
        d.line([x + s * .12, y + s * .85, x + s * .9, y + s * .85], fill=INK, width=3)
        d.line([x + s * .12, y + s * .85, x + s * .12, y + s * .12], fill=INK, width=3)
        d.line([x + s * .18, y + s * .25, x + s * .42, y + s * .45,
                x + s * .6, y + s * .4, x + s * .85, y + s * .75],
               fill=RED, width=4)
        d.polygon([(x + s * .85, y + s * .75), (x + s * .72, y + s * .72),
                   (x + s * .85, y + s * .58)], fill=RED)
    elif kind == "leaf":
        d.ellipse([x + s * .15, y + s * .15, x + s * .85, y + s * .85],
                  outline=TEAL, width=3)
        d.arc([x + s * .2, y + s * .2, x + s * .8, y + s * .8], 200, 340,
              fill=(230, 180, 40), width=5)
        d.ellipse([x + s * .32, y + s * .32, x + s * .68, y + s * .68], fill=GREEN)
        d.line([x + s * .5, y + s * .35, x + s * .5, y + s * .65], fill=(255, 255, 255),
               width=3)
    elif kind == "ship":
        d.polygon([(x + s * .1, y + s * .55), (x + s * .9, y + s * .55),
                   (x + s * .8, y + s * .8), (x + s * .2, y + s * .8)], fill=BLUE)
        d.rectangle([x + s * .2, y + s * .3, x + s * .4, y + s * .55], fill=RED)
        d.rectangle([x + s * .45, y + s * .3, x + s * .65, y + s * .55], fill=GOLD)
        d.rectangle([x + s * .7, y + s * .35, x + s * .85, y + s * .55], fill=TEAL)
        d.line([x + s * .05, y + s * .88, x + s * .95, y + s * .88], fill=BLUE, width=2)
        d.ellipse([x + s * .3, y + s * .1, x + s * .45, y + s * .25], fill=MUTED)
        d.ellipse([x + s * .55, y + s * .05, x + s * .7, y + s * .2], fill=MUTED)
    elif kind == "tanker":
        d.polygon([(x + s * .08, y + s * .6), (x + s * .92, y + s * .6),
                   (x + s * .82, y + s * .82), (x + s * .18, y + s * .82)], fill=INK)
        d.rectangle([x + s * .15, y + s * .4, x + s * .85, y + s * .6], fill=(60, 60, 60))
        d.ellipse([x + s * .4, y + s * .1, x + s * .6, y + s * .35], fill=ORANGE)
        d.polygon([(x + s * .5, y + s * .12), (x + s * .58, y + s * .3),
                   (x + s * .42, y + s * .3)], fill=ORANGE)
        d.line([x + s * .05, y + s * .9, x + s * .95, y + s * .9], fill=BLUE, width=2)
    elif kind == "aid":
        d.rectangle([x + s * .1, y + s * .3, x + s * .65, y + s * .75], fill=(245, 245, 245),
                    outline=INK, width=2)
        d.rectangle([x + s * .65, y + s * .45, x + s * .9, y + s * .75], fill=RED,
                    outline=INK, width=2)
        d.rectangle([x + s * .3, y + s * .42, x + s * .4, y + s * .62], fill=RED)
        d.rectangle([x + s * .25, y + s * .47, x + s * .45, y + s * .57], fill=RED)
        d.ellipse([x + s * .2, y + s * .72, x + s * .35, y + s * .87], fill=INK)
        d.ellipse([x + s * .7, y + s * .72, x + s * .85, y + s * .87], fill=INK)
    elif kind == "burst":
        cx, cy = x + s * .5, y + s * .45
        for r, col in ((s * .45, ORANGE), (s * .3, (230, 180, 40)), (s * .15, RED)):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        d.line([x + s * .1, y + s * .9, x + s * .9, y + s * .9], fill=INK, width=2)
    elif kind == "quake":
        d.line([x + s * .05, y + s * .6, x + s * .25, y + s * .6, x + s * .35, y + s * .4,
                x + s * .5, y + s * .75, x + s * .65, y + s * .45, x + s * .8, y + s * .6,
                x + s * .95, y + s * .6], fill=INK, width=3)
        d.polygon([(x + s * .3, y + s * .15), (x + s * .45, y + s * .15),
                   (x + s * .45, y + s * .4), (x + s * .3, y + s * .4)], fill=BLUE)
        d.polygon([(x + s * .55, y + s * .1), (x + s * .75, y + s * .1),
                   (x + s * .75, y + s * .4), (x + s * .55, y + s * .4)], fill=RED)
        d.line([x + s * .05, y + s * .85, x + s * .95, y + s * .85], fill=MUTED, width=2)
    elif kind == "craft":
        d.ellipse([x + s * .2, y + s * .25, x + s * .8, y + s * .85], fill=GOLD)
        d.ellipse([x + s * .05, y + s * .4, x + s * .95, y + s * .6], fill=(200, 200, 200))
        d.polygon([(x + s * .55, y + s * .05), (x + s * .75, y + s * .3),
                   (x + s * .5, y + s * .35), (x + s * .4, y + s * .15)], fill=BLUE)
        d.line([x + s * .15, y + s * .15, x + s * .3, y + s * .3], fill=INK, width=2)
        d.line([x + s * .85, y + s * .2, x + s * .7, y + s * .35], fill=INK, width=2)
    elif kind == "card":
        d.rectangle([x + s * .08, y + s * .2, x + s * .92, y + s * .8], fill=BLUE,
                    outline=INK, width=2)
        d.rectangle([x + s * .08, y + s * .3, x + s * .92, y + s * .45], fill=INK)
        d.text((x + s * .16, y + s * .52), "10%", font=font(True, False, 16),
               fill=(255, 255, 255))
        d.rectangle([x + s * .6, y + s * .55, x + s * .84, y + s * .7], fill=GOLD)
    elif kind == "lock":
        d.ellipse([x + s * .15, y + s * .15, x + s * .85, y + s * .85],
                  outline=INK, width=3)
        d.rectangle([x + s * .3, y + s * .35, x + s * .7, y + s * .6], fill=INK)
        d.rectangle([x + s * .38, y + s * .55, x + s * .62, y + s * .75], fill=RED)
        d.arc([x + s * .35, y + s * .2, x + s * .65, y + s * .45], 180, 360,
              fill=INK, width=4)
        d.line([x + s * .05, y + s * .9, x + s * .95, y + s * .9], fill=RED, width=3)
    elif kind == "ball":
        d.ellipse([x + s * .1, y + s * .1, x + s * .9, y + s * .9],
                  outline=INK, width=3, fill=(245, 245, 245))
        d.polygon([(x + s * .5, y + s * .32), (x + s * .68, y + s * .45),
                   (x + s * .61, y + s * .66), (x + s * .39, y + s * .66),
                   (x + s * .32, y + s * .45)], fill=INK)
        d.line([x + s * .5, y + s * .32, x + s * .5, y + s * .12], fill=INK, width=2)
        d.line([x + s * .68, y + s * .45, x + s * .88, y + s * .38], fill=INK, width=2)
        d.line([x + s * .32, y + s * .45, x + s * .12, y + s * .38], fill=INK, width=2)
    elif kind == "spy":
        d.rectangle([x + s * .1, y + s * .2, x + s * .9, y + s * .55], fill=RED,
                    outline=INK, width=2)
        d.rectangle([x + s * .1, y + s * .2, x + s * .3, y + s * .55], fill=(245, 245, 245))
        d.rectangle([x + s * .1, y + s * .33, x + s * .9, y + s * .42], fill=(245, 245, 245))
        d.line([x + s * .55, y + s * .65, x + s * .75, y + s * .85], fill=INK, width=4)
        d.line([x + s * .75, y + s * .65, x + s * .55, y + s * .85], fill=INK, width=4)

# -------------------------------------------------------------- layout ---

def draw_masthead(d):
    d.rectangle([0, 0, W, 112], fill=INK)
    text(d, (14, 8), "ONE DAY OF WORLD NEWS  ·  ONE PICTURE",
         font(True, False, 13), fill=(240, 220, 160))
    right_s = "50 STORIES  ·  7 REGIONS"
    text(d, (W - 14 - d.textlength(right_s, font=font(True, False, 13)), 8),
         right_s, font(True, False, 13), fill=(240, 220, 160))
    d.line([14, 30, W - 14, 30], fill=(120, 110, 90), width=1)
    centered(d, W // 2, 34, "Saturday 21 November 2026",
             font(True, True, 46), fill=(250, 246, 232))
    centered(d, W // 2, 86,
             "Iran hits US bases in Bahrain  ·  'El Chapo Isidro' captured  ·  Missile kills 2 in Kryvyi Rih",
             font(False, True, 15), fill=(210, 200, 175))


def draw_timeline(d):
    y0, y1 = 116, 158
    d.rectangle([12, y0, W - 12, y1], fill=PAPER, outline=RULE, width=1)
    slot_w = (W - 24) / len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        x = 12 + i * slot_w
        if i:
            d.line([x, y0 + 5, x, y1 - 5], fill=RULE, width=1)
        text(d, (x + 8, y0 + 4), when, font(True, False, 9), fill=RED)
        for j, line in enumerate(wrap(d, what, font(False, False, 10), slot_w - 16)):
            text(d, (x + 8, y0 + 18 + j * 12), line, font(False, False, 10))


def draw_panels(d):
    x0, y0 = 12, 164
    pw, ph, gx, gy = 244, 114, 8, 6
    for idx, (num, region, topic, chip, head, detail, icon, _ll) in enumerate(PANELS):
        r, c = divmod(idx, 4)
        x = x0 + c * (pw + gx)
        y = y0 + r * (ph + gy)
        col = REGION_COLORS.get(region, (70, 70, 70))
        d.rectangle([x, y, x + pw, y + ph], fill=PAPER, outline=RULE, width=1)
        d.rectangle([x, y, x + pw, y + 3], fill=col)
        # number badge
        d.ellipse([x + 6, y + 9, x + 26, y + 29], fill=col)
        num_s = str(num)
        tw = d.textlength(num_s, font=font(True, False, 12))
        d.text((x + 16 - tw / 2, y + 11), num_s, font=font(True, False, 12),
               fill=(255, 255, 255))
        text(d, (x + 31, y + 11), region + "  ·  " + topic,
             font(True, False, 9), fill=col)
        # chip
        chip_w = d.textlength(chip, font=font(True, False, 8)) + 8
        d.rectangle([x + pw - chip_w - 5, y + 30, x + pw - 5, y + 43],
                    fill=LIGHT, outline=RULE, width=1)
        text(d, (x + pw - chip_w - 1, y + 32), chip, font(True, False, 8),
             fill=DARKRED if chip.startswith("CLAIM") else TEAL)
        # headline + detail, icon at right of detail block
        icon_s = 40
        head_lines = wrap(d, head, font(True, False, 12), pw - 14)
        for j, line in enumerate(head_lines[:2]):
            text(d, (x + 7, y + 46 + j * 14), line, font(True, False, 12))
        det_w = pw - 14 - icon_s - 6
        det_lines = wrap(d, detail, font(False, False, 10), det_w)
        for j, line in enumerate(det_lines[:3]):
            text(d, (x + 7, y + 74 + j * 12), line, font(False, False, 10),
                 fill=(50, 48, 42))
        draw_icon(d, icon, x + pw - icon_s - 5, y + ph - icon_s - 5, icon_s)


def draw_also_on(d):
    x0, y0, w = 620, 644, 392
    d.rectangle([x0, y0, x0 + w, 1012], fill=PAPER, outline=RULE, width=1)
    d.rectangle([x0, y0, x0 + w, y0 + 22], fill=INK)
    text(d, (x0 + 8, y0 + 5), "ALSO ON SATURDAY 21 NOVEMBER",
         font(True, False, 12), fill=(250, 246, 232))
    row_h = 10.1
    for i, item in enumerate(ALSO_ON):
        y = y0 + 24 + i * row_h
        text(d, (x0 + 8, y), "·", font(True, False, 9), fill=RED)
        text(d, (x0 + 18, y), item, font(False, False, 9))


def draw_map(d):
    x0, y0, mw, mh = 12, 644, 596, 240
    d.rectangle([x0, y0, x0 + mw, y0 + mh], fill=(214, 230, 240), outline=RULE, width=1)
    text(d, (x0 + 8, y0 + 5), "WHERE IT HAPPENED",
         font(True, False, 12), fill=INK)
    map_note = "numbered as the panels"
    text(d, (x0 + mw - 8 - d.textlength(map_note, font=font(False, True, 10)), y0 + 6),
         map_note, font(False, True, 10), fill=MUTED)
    mx, my, mwd, mht = x0 + 6, y0 + 26, mw - 12, mh - 32

    def proj(lon, lat):
        px = mx + (lon + 180.0) / 360.0 * mwd
        py = my + (85.0 - lat) / 145.0 * mht
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(222, 210, 178), outline=(150, 140, 118))
    d.line([mx, my + (85.0 - 0) / 145.0 * mht, mx + mwd, my + (85.0 - 0) / 145.0 * mht],
           fill=(170, 190, 205), width=1)
    for num, region, _t, _c, _h, _de, _i, ll in PANELS:
        if ll is None:
            continue
        lon, lat = ll
        # nudge the two Washington pins apart
        if num == 14:
            lon, lat = lon + 14, lat - 6
        if num == 5:
            lon, lat = lon - 6, lat + 4
        px, py = proj(lon, lat)
        col = REGION_COLORS.get(region, (70, 70, 70))
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col, outline=(255, 255, 255),
                  width=1)
        ns = str(num)
        tw = d.textlength(ns, font=font(True, False, 9))
        d.text((px - tw / 2, py - 7), ns, font=font(True, False, 9),
               fill=(255, 255, 255))
    text(d, (x0 + 8, y0 + mh - 14),
         "No. 12 happened in orbit around Mercury - beyond this map.",
         font(False, True, 9), fill=MUTED)


def draw_date_check(d):
    x0, y0, w, h = 12, 890, 596, 122
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 250, 230), outline=RED, width=2)
    text(d, (x0 + 8, y0 + 5), "DATE CHECK - left out on purpose",
         font(True, False, 11), fill=DARKRED)
    text(d, (x0 + 8, y0 + 22), "Broke BEFORE Saturday:",
         font(True, False, 9), fill=INK)
    for j, line in enumerate(wrap(d, DATE_CHECK_BEFORE, font(False, False, 9), w - 16)):
        text(d, (x0 + 8, y0 + 35 + j * 11), line, font(False, False, 9))
    text(d, (x0 + 8, y0 + 62), "Not yet - still in the future:",
         font(True, False, 9), fill=INK)
    for j, line in enumerate(wrap(d, DATE_CHECK_FUTURE, font(False, False, 9), w - 16)):
        text(d, (x0 + 8, y0 + 75 + j * 11), line, font(False, False, 9))


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_timeline(d)
    draw_panels(d)
    draw_also_on(d)
    draw_map(d)
    draw_date_check(d)
    d.line([12, 1015, W - 12, 1015], fill=RULE, width=1)
    centered(d, W // 2, 1017,
             "Every story here happened or was first reported on 21 Nov 2026. "
             "CLAIM = one side's account. Sources: AP, Reuters, BBC, USGS, Al Jazeera.",
             font(False, False, 8), fill=MUTED)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path, img.size, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
