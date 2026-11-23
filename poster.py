#!/usr/bin/env python3
"""Draw "The World in One Day - Monday 23 November 2026" as entry.png.

A single front-page poster summarising the world's news of Monday
23 November 2026. Every illustration is drawn in code with Pillow;
all text is word-wrapped to fit its box. Run `python3 poster.py`
to regenerate entry.png (1024 x 1024, under 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

# Palette: warm paper, deep ink navy, teal, rust red, ochre.
PAPER = (247, 243, 234)
INK = (18, 33, 61)
TEAL = (15, 106, 110)
RUST = (178, 58, 32)
OCHRE = (204, 138, 30)
FAINT = (90, 98, 110)
CARD_BG = (255, 252, 245)
RULE = (18, 33, 61)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """A cracked earth: teal oceans, ochre land blobs, a rust fissure."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(23, 94, 122),
                 outline=INK, width=4)
    # Land masses (rough blobs clipped by the circle via a mask).
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    land = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(land)
    ld.ellipse([cx - 88, cy - 78, cx - 8, cy - 6], fill=(96, 142, 84, 255))
    ld.ellipse([cx + 6, cy - 58, cx + 82, cy + 12], fill=(96, 142, 84, 255))
    ld.ellipse([cx - 52, cy + 22, cx + 34, cy + 86], fill=(112, 150, 92, 255))
    ld.ellipse([cx - 96, cy + 30, cx - 46, cy + 66], fill=(96, 142, 84, 255))
    globe = Image.composite(
        land, Image.new("RGBA", (W, H), (0, 0, 0, 0)), mask)
    img.paste(globe, (0, 0), globe)
    # Fissure: a jagged rust crack across the globe.
    crack = [(cx - 78, cy - 66), (cx - 40, cy - 30), (cx - 62, cy - 2),
             (cx - 18, cy + 26), (cx - 38, cy + 52), (cx + 6, cy + 84)]
    draw.line(crack, fill=RUST, width=7, joint="curve")
    # Smoke puffs rising from the crack.
    for i, (sx, sy, sr) in enumerate([(cx + 30, cy - 98, 9),
                                      (cx + 50, cy - 112, 7),
                                      (cx + 12, cy - 116, 6)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(120, 120, 120, 255) if i != 1 else (150, 150, 150, 255))


def story_card(draw, x, y, w, h, kicker, title, body, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD_BG, outline=accent, width=2)
    pad = 16
    draw.text((x + pad, y + 10), kicker, font=font(SANS_B, 17), fill=accent)
    t_lines = wrap(draw, title, font(SERIF_B, 26), w - 2 * pad)
    yy = draw_lines(draw, t_lines, x + pad, y + 34, font(SERIF_B, 26),
                    INK, 30)
    b_lines = wrap(draw, body, font(SANS, 17), w - 2 * pad)
    draw_lines(draw, b_lines, x + pad, yy + 4, font(SANS, 17), (52, 58, 68),
               22)


img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img, "RGBA")

# ---- Masthead -------------------------------------------------------
draw.text((MARGIN, 26), "THE WORLD IN ONE DAY",
          font=font(SERIF_B, 62), fill=INK)
draw.text((MARGIN, 100),
          "MONDAY 23 NOVEMBER 2026  •  ANTALYA  •  SEOUL  •  CIKANDE  •  KYIV",
          font=font(SANS_B, 19), fill=RUST)
rule(draw, MARGIN, 142, W - MARGIN, 3)

# ---- Lead story: COP31 ---------------------------------------------
lead_y = 164
draw.text((MARGIN, lead_y), "CLIMATE SUMMIT",
          font=font(SANS_B, 20), fill=TEAL)
draw.text((MARGIN, lead_y + 28), "COP31 COLLAPSES",
          font=font(SERIF_B, 54), fill=INK)
deck = ("No deal in Antalya as the words “fossil fuels” vanish "
        "from the final text — the first climate summit to fail "
        "since Copenhagen in 2009.")
d_lines = wrap(draw, deck, font(SERIF, 25), 560)
yy = draw_lines(draw, d_lines, MARGIN, lead_y + 104, font(SERIF, 25),
                (52, 58, 68), 32)
body = ("Two weeks of talks — the longest COP ever — ended with the "
        "EU, Britain and island states rejecting the pact.")
b_lines = wrap(draw, body, font(SANS, 19), 560)
draw_lines(draw, b_lines, MARGIN, yy + 8, font(SANS, 19), FAINT, 24)

draw_globe(draw, 830, 296, 104)
draw.text((755, 408), "ANTALYA, TURKIYE",
          font=font(SANS_B, 16), fill=FAINT)

rule(draw, MARGIN, 472, W - MARGIN, 2)

# ---- Four more stories ---------------------------------------------
cards = [
    ("SEOUL  •  EDUCATION", "Minister quits over AI exam cheating",
     "Choi Kyo-jin resigns after a cheating scare upended the Suneung "
     "exam; 111 device cases were logged. President Lee accepted "
     "within an hour.", TEAL),
    ("CIKANDE, INDONESIA  •  DISASTER", "Factory fire: 7 bodies found, ~50 missing",
     "A blaze tore through the PT Fonusa Agung Mulia candy factory in "
     "Serang, Banten, with 300 workers inside. DNA tests may take "
     "weeks.", RUST),
    ("KYIV  •  WAR", "Ship ablaze off Finland; 14 missing in Kyiv region",
     "A Russian cargo ship is still on fire off Finland after an "
     "attack. At least 14 are missing after a drone hit a building "
     "in the Kyiv region.", INK),
    ("SINALOA, MEXICO  •  CRIME", "“El Chapo Isidro” captured",
     "Mexican forces seize the FBI’s most-wanted cartel boss after "
     "firefights in Sinaloa that left 11 people dead.", OCHRE),
]
cw, ch, gap = 464, 188, 24
cx0, cy0 = MARGIN, 494
for i, (kicker, title, body, accent) in enumerate(cards):
    x = cx0 + (i % 2) * (cw + gap)
    y = cy0 + (i // 2) * (ch + gap)
    story_card(draw, x, y, cw, ch, kicker, title, body, accent)

# ---- Footer ticker --------------------------------------------------
rule(draw, MARGIN, 916, W - MARGIN, 2)
ticker = ("ALSO TODAY  •  UN to keep negotiating lethal-AI limits  •  "
          "Nepal PM Shah meets Modi in Delhi  •  India 720/9d, a Test "
          "record, in Wellington  •  Thousands march in Lisbon over "
          "living costs")
t_lines = wrap(draw, ticker, font(SANS, 18), W - 2 * MARGIN)
draw_lines(draw, t_lines, MARGIN, 930, font(SANS, 18), (52, 58, 68), 23)
draw.text((MARGIN, 988),
          "Sources: Reuters, AP, CNN, AFP, The Guardian — 23 November 2026",
          font=font(SANS, 14), fill=FAINT)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
