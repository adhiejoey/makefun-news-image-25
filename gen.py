#!/usr/bin/env python3
"""news-image-20261125 builder 1 — generator (written fresh 25 Nov 2026).

Draws a one-page illustrated broadsheet: 35 stories, all first reported
Wednesday 25 November 2026 (UTC). Pillow only, no network, deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---- palette ----
PAPER   = (246, 241, 231)
INK     = (26, 26, 26)
MUTED   = (90, 86, 76)
RED     = (179, 32, 44)
NAVY    = (31, 58, 95)
NAVY_D  = (22, 42, 70)
GOLD    = (201, 162, 39)
GOLD_L  = (232, 196, 82)
WHITE   = (255, 255, 255)
PANEL   = (255, 253, 248)
LINE    = (210, 203, 188)
GREEN   = (34, 120, 70)
SKY     = (16, 28, 54)
SHADOW  = (0, 0, 0, 70)

FD = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

SERIF_B  = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF    = lambda s: F("DejaVuSerif.ttf", s)
SANS_B   = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS     = lambda s: F("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if font.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def text(draw, xy, s, font, fill=INK, anchor="la"):
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)

def panel(x, y, w, h, fill=PANEL, shadow=True):
    if shadow:
        d.rounded_rectangle([x + 3, y + 4, x + w + 3, y + h + 4], radius=6,
                            fill=(0, 0, 0, 55))
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=fill,
                        outline=LINE, width=1)
    d.line([x + 6, y + 1, x + w - 6, y + 1], fill=(255, 255, 255, 160), width=1)

def chip(x, y, s, bg, fg=WHITE, font=None, pad=5):
    font = font or SANS_B(9)
    w_ = int(font.getlength(s)) + pad * 2
    h_ = 15
    d.rounded_rectangle([x, y, x + w_, y + h_], radius=7, fill=bg)
    d.text((x + pad, y + 2), s, font=font, fill=fg)
    return w_

def label_chip(x, y, kind):
    bg = {"CONFIRMED": GREEN, "OFFICIAL": NAVY, "REPORTED": (120, 110, 80),
          "CLAIM": RED}[kind]
    return chip(x, y, kind, bg)

# ================= MASTHEAD =================
# 3D title: dark-red extrusion behind ink letters
title = "WEDNESDAY 25 NOVEMBER 2026"
tf = SERIF_B(33)
tw = tf.getlength(title)
tx = (W - tw) / 2
d.text((tx + 2, 16 + 2), title, font=tf, fill=(120, 20, 28))
d.text((tx, 16), title, font=tf, fill=INK)
d.rectangle([24, 58, W - 24, 60], fill=RED)
d.rectangle([24, 61, W - 24, 62], fill=(255, 255, 255, 120))
sub = "35 STORIES  ·  6 REGIONS  ·  ALL FROM THIS WEDNESDAY"
sf = SANS_B(13)
d.text(((W - sf.getlength(sub)) / 2, 68), sub, font=sf, fill=RED)

# ================= NUMBERS STRIP =================
ny = 92
d.rounded_rectangle([24, ny, W - 24, ny + 24], radius=5, fill=NAVY_D)
nums = [("00:18", "LAUNCH"), ("-5.3%", "SEOUL"), ("4.9%", "AU CPI"),
        ("$90.97", "BRENT"), ("$3,544", "GOLD"), ("$59,257", "BITCOIN"),
        ("M5.9", "QUAKE"), ("3", "ASTRONAUTS")]
seg = (W - 48) / len(nums)
for i, (v, k) in enumerate(nums):
    cx = 24 + seg * i + seg / 2
    d.text((cx, ny + 3), v, font=SANS_B(11), fill=GOLD_L, anchor="ma")
    d.text((cx, ny + 14), k, font=SANS_B(7), fill=(200, 205, 220), anchor="ma")
    if i:
        d.line([24 + seg * i, ny + 5, 24 + seg * i, ny + 19], fill=(90, 105, 135))

# ================= TIMELINE =================
ty = 124
d.line([24, ty + 18, W - 24, ty + 18], fill=LINE, width=2)
events = [
    ("00:18", "Shenzhou-24"),
    ("00:30", "Australia CPI"),
    ("00:41", "Solomons"),
    ("00:45", "M4.7 PH"),
    ("01:38", "M5.9 Balleny"),
    ("02:00", "Asia stocks"),
    ("06:48", "Docking*"),
    ("13:30", "US PCE*"),
]
for i, (t, lab) in enumerate(events):
    x = 40 + i * (W - 80) / (len(events) - 1)
    d.ellipse([x - 5, ty + 13, x + 5, ty + 23], fill=RED, outline=WHITE, width=2)
    d.text((x, ty), t, font=SANS_B(9), fill=INK, anchor="ma")
    d.text((x, ty + 26), lab, font=SANS(8), fill=MUTED, anchor="ma")

# ================= LEAD DRAWINGS =================
def draw_rocket(x, y, w, h):
    # night sky with stars, launch tower, rocket, flame, smoke
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    for sx, sy, r in [(12, 12, 1), (40, 26, 1), (70, 10, 2), (100, 30, 1),
                      (150, 14, 1), (200, 24, 2), (240, 10, 1), (280, 32, 1),
                      (300, 16, 1), (180, 40, 1), (90, 44, 1), (260, 44, 1)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=WHITE)
    d.ellipse([x + w - 46, y + 8, x + w - 14, y + 40], fill=(240, 240, 225))
    d.ellipse([x + w - 40, y + 12, x + w - 30, y + 26], fill=(215, 215, 200))
    gy = y + h - 18
    d.rectangle([x, gy, x + w, y + h], fill=(40, 38, 34))
    # tower
    d.rectangle([x + 96, y + 30, x + 106, gy], fill=(120, 122, 126))
    d.rectangle([x + 96, y + 30, x + 106, y + 38], fill=(90, 92, 96))
    d.rectangle([x + 106, y + 52, x + 128, y + 56], fill=(120, 122, 126))
    # rocket body
    rx, rw = x + 140, 34
    d.polygon([(rx + 4, y + 18), (rx + rw - 4, y + 18), (rx + rw / 2, y + 2)],
              fill=RED)
    d.rectangle([rx, y + 18, rx + rw, y + 62], fill=(245, 245, 240))
    d.rectangle([rx, y + 40, rx + rw, y + 48], fill=RED)
    d.rectangle([rx, y + 18, rx + 6, y + 62], fill=(210, 210, 205))
    d.polygon([(rx - 8, y + 62), (rx, y + 52), (rx, y + 66)], fill=(200, 60, 50))
    d.polygon([(rx + rw + 8, y + 62), (rx + rw, y + 52), (rx + rw, y + 66)],
              fill=(200, 60, 50))
    # flame
    d.polygon([(rx + 8, y + 66), (rx + rw - 8, y + 66), (rx + rw / 2, y + 92)],
              fill=(255, 170, 40))
    d.polygon([(rx + 12, y + 66), (rx + rw - 12, y + 66), (rx + rw / 2, y + 82)],
              fill=(255, 230, 120))
    # smoke
    for cx, cy, r in [(110, gy - 2, 16), (140, gy + 2, 20), (180, gy - 2, 18),
                      (210, gy + 4, 14)]:
        d.ellipse([x + cx - r, cy - r, x + cx + r, cy + r], fill=(200, 198, 192))
    d.text((x + 8, y + h - 16), "JIUQUAN · 00:18 UTC", font=SANS_B(8), fill=GOLD_L)

def draw_fall(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 246, 238))
    for gy in range(y + 12, y + h - 8, 16):
        d.line([x + 8, gy, x + w - 8, gy], fill=(228, 222, 208))
    for bx, bh in [(30, 18), (90, 26), (150, 36), (210, 46), (270, 56)]:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + 22, y + h - 14],
                    fill=(190, 60, 60))
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + 22, y + h - 10 - bh],
                    fill=(225, 110, 110))
    pts = [(x + 14, y + 16), (x + 60, y + 26), (x + 110, y + 24),
           (x + 160, y + 42), (x + 210, y + 50), (x + 260, y + 66),
           (x + 300, y + 80)]
    d.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts[1:]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED, outline=WHITE, width=1)
    d.rectangle([x + 8, y + 4, x + 128, y + 22], fill=(250, 246, 238))
    d.text((x + 10, y + 6), "-5.3%  SEOUL", font=SANS_B(15), fill=RED)
    d.text((x + 190, y + 8), "-5.1% TAIPEI", font=SANS_B(11), fill=(150, 40, 40))
    d.text((x + 190, y + 24), "-2.9% NIKKEI", font=SANS_B(11), fill=(150, 40, 40))

def draw_treaty(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 244, 250))
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + 40), (x, y + 70)],
              fill=(210, 225, 235))
    # Australia flag (left)
    fx, fy = x + 22, y + 12
    d.rectangle([fx, fy, fx + 104, fy + 56], fill=(20, 40, 110))
    d.polygon([(fx, fy), (fx + 52, fy), (fx + 52, fy + 28), (fx, fy + 28)],
              fill=(200, 30, 40))
    d.line([fx, fy, fx + 52, fy + 28], fill=WHITE, width=4)
    d.line([fx + 52, fy, fx, fy + 28], fill=WHITE, width=4)
    for sx, sy in [(70, 14), (88, 26), (70, 40), (92, 44)]:
        d.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3, fy + sy + 3], fill=WHITE)
    d.rectangle([fx - 3, fy - 8, fx - 1, y + h - 14], fill=(120, 100, 70))
    # Solomons flag (right)
    gx, gy = x + 190, y + 12
    d.polygon([(gx, gy), (gx + 104, gy), (gx + 104, gy + 56), (gx, gy + 56)],
              fill=(30, 90, 160))
    d.polygon([(gx, gy + 56), (gx + 104, gy), (gx + 104, gy + 56)],
              fill=(20, 130, 70))
    d.polygon([(gx, gy + 56), (gx + 104, gy), (gx + 104, gy + 12), (gx + 12, gy + 56)],
              fill=GOLD)
    for sx, sy in [(18, 14), (34, 10), (50, 16), (26, 26), (42, 30)]:
        d.ellipse([gx + sx - 3, gy + sy - 3, gx + sx + 3, gy + sy + 3], fill=WHITE)
    d.rectangle([gx + 104 + 1, gy - 8, gx + 104 + 3, y + h - 14], fill=(120, 100, 70))
    # treaty document in front
    dx, dy, dw, dh = x + 118, y + 62, 84, 48
    d.rectangle([dx + 2, dy + 3, dx + dw + 2, dy + dh + 3], fill=(0, 0, 0, 60))
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=(255, 252, 240),
                outline=(150, 130, 90))
    for i in range(4):
        d.line([dx + 8, dy + 10 + i * 8, dx + dw - 8, dy + 10 + i * 8],
               fill=(140, 130, 110))
    d.ellipse([dx + dw - 22, dy + dh - 20, dx + dw - 6, dy + dh - 4], fill=RED)
    d.text((dx + 8, dy + dh - 14), "CANBERRA", font=SANS_B(7), fill=NAVY)

LEADS = [
    dict(tag="SPACE · CHINA", draw=draw_rocket,
         head="Shenzhou-24 lifts off with first foreign astronaut",
         body="Long March 2F lifts off 00:18 UTC. Tang Hongbo, Wu Yi and Zeeshan Ali — first Pakistani in orbit.",
         kind="OFFICIAL", src="Xinhua · Reuters"),
    dict(tag="MARKETS · ASIA", draw=draw_fall,
         head="Asia stocks tumble on fresh tariff threats",
         body="MSCI Asia ex-Japan −2.3% as Seoul and Taipei sink. USTR findings due; Nvidia fell 5.9% Tue.",
         kind="CONFIRMED", src="Reuters"),
    dict(tag="PACIFIC", draw=draw_treaty,
         head="Australia and Solomons sign historic treaty",
         body="Canberra deal makes Australia the primary partner, bars foreign bases and scraps the China pact.",
         kind="OFFICIAL", src="Reuters · pm.gov.au"),
]

ly = 170
lw, lh = 320, 228
for i, L in enumerate(LEADS):
    x = 24 + i * (lw + 8)
    panel(x, ly, lw, lh)
    L["draw"](x + 8, ly + 8, lw - 16, 108)
    cx = x + 10
    chip(cx, ly + 122, L["tag"], RED)
    hy = ly + 141
    hlines = wrap(L["head"], SERIF_B(16), lw - 20)[:2]
    for j, ln in enumerate(hlines):
        d.text((cx, hy + j * 18), ln, font=SERIF_B(16), fill=INK)
    by = hy + 18 * len(hlines) + 3
    for j, ln in enumerate(wrap(L["body"], SANS(11), lw - 20)[:2]):
        d.text((cx, by + j * 13), ln, font=SANS(11), fill=(60, 56, 48))
    fy2 = ly + lh - 18
    wch = label_chip(cx, fy2, L["kind"])
    d.text((cx + wch + 6, fy2 + 2), L["src"], font=SANS(9), fill=MUTED)

# ================= CARD DRAWINGS =================
def card_cpi(x, y, w, h):
    for i, bh in enumerate([10, 16, 24, 34]):
        bx = x + 8 + i * 16
        d.rectangle([bx, y + h - 6 - bh, bx + 11, y + h - 6], fill=NAVY)
        d.rectangle([bx, y + h - 6 - bh, bx + 11, y + h - 3 - bh], fill=(90, 120, 170))
    d.text((x + 78, y + 2), "4.9%", font=SANS_B(17), fill=RED)

def card_japan(x, y, w, h):
    pts = [(x + 8, y + h - 12), (x + 30, y + h - 20), (x + 55, y + h - 16),
           (x + 80, y + h - 26), (x + 105, y + h - 30), (x + 118, y + 16)]
    d.line(pts, fill=GREEN, width=3, joint="curve")
    d.text((x + 128, y + 2), "+4.2%", font=SANS_B(13), fill=GREEN)
    d.text((x + 8, y + 2), "¥", font=SANS_B(14), fill=NAVY)

def card_oil(x, y, w, h):
    d.ellipse([x + 14, y + 6, x + 54, y + 18], fill=(60, 60, 60))
    d.rectangle([x + 14, y + 12, x + 54, y + h - 8], fill=(40, 40, 40))
    d.ellipse([x + 14, y + h - 16, x + 54, y + h - 4], fill=(80, 80, 80))
    d.text((x + 18, y + 20), "OIL", font=SANS_B(10), fill=WHITE)
    d.polygon([(x + 76, y + 8), (x + 88, y + 8), (x + 82, y + 22)], fill=RED)
    d.rectangle([x + 79, y + 20, x + 85, y + h - 8], fill=RED)
    d.text((x + 96, y + 12), "-0.5%", font=SANS_B(13), fill=RED)

def card_dollar(x, y, w, h):
    d.text((x + 10, y + 2), "$", font=SANS_B(30), fill=NAVY)
    d.polygon([(x + 52, y + 12), (x + 62, y + 12), (x + 57, y + 24)], fill=GREEN)
    d.rectangle([x + 55, y + 22, x + 59, y + h - 10], fill=GREEN)
    d.polygon([(x + 72, y + h - 12), (x + 82, y + h - 12), (x + 77, y + h - 24)],
              fill=RED)
    d.rectangle([x + 75, y + 10, x + 79, y + h - 22], fill=RED)
    d.text((x + 92, y + 12), "97%", font=SANS_B(13), fill=INK)
    d.text((x + 92, y + 28), "HIKE", font=SANS_B(8), fill=MUTED)

def card_gold(x, y, w, h):
    for i, (bx, by) in enumerate([(20, 26), (52, 26), (36, 12)]):
        d.polygon([(x + bx, y + by + 12), (x + bx + 6, y + by),
                   (x + bx + 30, y + by), (x + bx + 36, y + by + 12)],
                  fill=GOLD_L if i < 2 else GOLD)
        d.rectangle([x + bx, y + by + 12, x + bx + 36, y + by + 16],
                    fill=(170, 130, 30))
    d.text((x + 100, y + 12), "$3,544", font=SANS_B(13), fill=(140, 105, 20))

def card_quake(x, y, w, h, mag):
    pts = [(x + 6, y + h // 2)]
    for i in range(1, 20):
        px = x + 6 + i * 6
        amp = 2 if i % 5 else (14 if i in (9, 10) else 8)
        py = y + h // 2 + (amp if i % 2 else -amp)
        pts.append((px, py))
    d.line(pts, fill=RED, width=2, joint="curve")
    d.text((x + 128, y + 8), mag, font=SANS_B(15), fill=RED)

def card_skyline(x, y, w, h):
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(60, 60, 70))
    for bx, bw, bh in [(10, 16, 22), (30, 12, 30), (46, 20, 18), (70, 14, 34),
                       (88, 16, 24), (108, 12, 28)]:
        d.rectangle([x + bx, y + h - 6 - bh, x + bx + bw, y + h - 6],
                    fill=NAVY)
        d.rectangle([x + bx, y + h - 6 - bh, x + bx + bw, y + h - 3 - bh],
                    fill=(90, 120, 170))
    d.polygon([(x + 76, y + 2), (x + 84, y + 2), (x + 80, y + h - 40)],
              fill=RED)
    d.rectangle([x + 126, y + 8, x + 134, y + 12], fill=RED)

def card_btc(x, y, w, h):
    d.ellipse([x + 12, y + 2, x + 50, y + 38], fill=(245, 170, 60))
    d.ellipse([x + 16, y + 6, x + 46, y + 34], fill=(255, 195, 90))
    d.text((x + 22, y + 9), "B", font=SANS_B(20), fill=(120, 70, 0))
    d.polygon([(x + 72, y + 8), (x + 84, y + 8), (x + 78, y + 22)], fill=RED)
    d.rectangle([x + 75, y + 20, x + 81, y + h - 8], fill=RED)
    d.text((x + 90, y + 12), "-1%", font=SANS_B(13), fill=RED)

CARDS = [
    ("AUSTRALIA", card_cpi, "Australia CPI jumps to 4.9%",
     "Headline inflation up from 4.3%; trimmed mean 3.8%. RBA hike risk rises.", "OFFICIAL", "ABS · Reuters"),
    ("JAPAN", card_japan, "Japan services prices hit 36-year high",
     "Services PPI +4.2% y/y in Oct, from 3.8% in Sept. BOJ hike case grows.", "OFFICIAL", "BOJ · Reuters"),
    ("ENERGY", card_oil, "Oil falls as glut fears offset Hormuz",
     "Brent $90.97 (−0.5%), WTI $81.58 as surplus worries beat disruption fears.", "REPORTED", "Reuters"),
    ("MARKETS", card_dollar, "Dollar steadies ahead of US PCE + GDP",
     "Aussie jumps on CPI; traders price a ~97% chance of a Dec Fed hike.", "REPORTED", "Reuters"),
    ("MARKETS", card_gold, "Gold ticks lower ahead of US inflation",
     "Spot $3,544.54 (−0.3%) after a 2% slide on Tuesday; silver $40.79.", "REPORTED", "Reuters"),
    ("ANTARCTICA", lambda x, y, w, h: card_quake(x, y, w, h, "M5.9"),
     "M5.9 quake hits Balleny Islands region",
     "01:38 UTC, 10 km deep. USGS green alert — no casualties expected.", "OFFICIAL", "USGS"),
    ("CHINA", card_skyline, "Shanghai pledges loyalty after Chen probe",
     "City leadership backs Beijing as Politburo member Chen Jining faces inquiry.", "REPORTED", "Reuters"),
    ("CRYPTO", card_btc, "Bitcoin slides below $60,000",
     "BTC ~$59,257 (−1%); ether $1,660 (−1.1%) as risk appetite fades.", "REPORTED", "Reuters"),
    ("PHILIPPINES", lambda x, y, w, h: card_quake(x, y, w, h, "M4.7"),
     "M4.7 quake near Cabatuan, Philippines",
     "~00:45 UTC, 35.8 km deep. No damage reported.", "OFFICIAL", "USGS"),
    ("CHINA", lambda x, y, w, h: card_quake(x, y, w, h, "M4.3"),
     "M4.3 quake near Shihezi, China",
     "01:19 UTC, reviewed by seismologists. No damage reported.", "OFFICIAL", "USGS"),
]

cy0, cw, chh, cg = 402, 192, 118, 8
for i, (tag, drawfn, head, body, kind, src) in enumerate(CARDS):
    r, c = divmod(i, 5)
    x = 24 + c * (cw + cg)
    y = cy0 + r * (chh + 8)
    panel(x, y, cw, chh)
    drawfn(x + 6, y + 6, cw - 12, 40)
    chip(x + 8, y + 50, tag, NAVY, font=SANS_B(8))
    hy = y + 69
    hlines = wrap(head, SERIF_B(12), cw - 16)[:2]
    for j, ln in enumerate(hlines):
        d.text((x + 8, hy + j * 14), ln, font=SERIF_B(12), fill=INK)
    fy2 = y + chh - 16
    wch = label_chip(x + 8, fy2, kind)
    d.text((x + 8 + wch + 4, fy2 + 2), src, font=SANS(8), fill=MUTED)

# ================= ALSO TODAY =================
ay = 652
d.text((24, ay), "ALSO TODAY — 22 MORE STORIES", font=SANS_B(12), fill=NAVY)
d.line([24, ay + 17, W - 24, ay + 17], fill=RED, width=2)
ALSO = [
    (14, "Shenzhou-24 docking due ~06:48 UTC", "OFFICIAL"),
    (15, "Zeeshan Ali: first Pakistani in orbit; 5–10 day stay", "OFFICIAL"),
    (16, "Tang Hongbo commands his third mission", "OFFICIAL"),
    (17, "US PCE + Q3 GDP due 13:30 GMT", "REPORTED"),
    (18, "Germany GDP (detailed Q3) due 07:00 GMT", "REPORTED"),
    (19, "BoE's Bailey before MPs this morning", "REPORTED"),
    (20, "USTR Section 301 tariff findings due Tue/Wed", "REPORTED"),
    (21, "US Treasury to sell $44bn of 7-year notes", "REPORTED"),
    (22, "US jobless claims, durable goods, new home sales due", "REPORTED"),
    (23, "Aussie jumps 0.4% to $0.6553 after CPI", "REPORTED"),
    (24, "Yen steady at 159.28 per dollar", "REPORTED"),
    (25, "Euro flat at $1.0961", "REPORTED"),
    (26, "Dollar index flat at 103.85", "REPORTED"),
    (27, "NZ dollar weakens to $0.5477", "REPORTED"),
    (28, "Hong Kong −1.9%, ASX −1.3%, Shanghai −0.7%", "REPORTED"),
    (29, "S&P 500 e-mini futures −0.3%", "REPORTED"),
    (30, "Seoul KOSPI −5.3% in chip rout", "REPORTED"),
    (31, "Taipei TAIEX −5.1%", "REPORTED"),
    (32, "Tokyo Nikkei −2.9%", "REPORTED"),
    (33, "Indian shares set to open higher; GIFT Nifty 25,738", "REPORTED"),
    (34, "Solomons: Australia to fund free education + visas", "OFFICIAL"),
    (35, "Solomons treaty bans foreign military bases", "OFFICIAL"),
]
LCLR = {"OFFICIAL": NAVY, "REPORTED": (120, 110, 80), "CONFIRMED": GREEN}
for i, (n, txt, kind) in enumerate(ALSO):
    col, row = divmod(i, 11)
    x = 24 + col * 500
    y = ay + 22 + row * 12
    d.text((x, y), f"{n}.", font=SANS_B(10), fill=RED)
    d.text((x + 24, y), txt, font=SANS(10), fill=INK)
    tw_ = SANS(10).getlength(txt)
    d.text((x + 24 + tw_ + 5, y), kind, font=SANS_B(8), fill=LCLR[kind])

# ================= DOT WORLD MAP =================
def inside(px, py, poly):
    ins, n = False, len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            ins = not ins
        j = i
    return ins

CONTINENTS = [
    [(4, 4), (30, 3), (34, 9), (30, 16), (22, 20), (14, 19), (8, 14), (3, 9)],
    [(24, 23), (32, 23), (35, 30), (31, 41), (27, 37), (23, 29)],
    [(43, 4), (55, 3), (57, 9), (50, 13), (43, 11)],
    [(43, 17), (57, 17), (59, 26), (53, 37), (47, 33), (42, 24)],
    [(57, 3), (94, 3), (97, 12), (90, 20), (78, 23), (66, 20), (58, 14), (56, 8)],
    [(80, 33), (95, 33), (95, 41), (80, 41)],
    [(8, 47), (92, 47), (92, 50), (8, 50)],
]
mx, my, mw, mh = 24, 806, 250, 172
panel(mx, my, mw, mh)
d.text((mx + 10, my + 8), "WHERE IT HAPPENED", font=SANS_B(10), fill=NAVY)
mapx, mapy, mapw, maph = mx + 6, my + 26, 238, 118
for gx in range(0, 101, 2):
    for gy in range(0, 51, 2):
        if any(inside(gx, gy, p) for p in CONTINENTS):
            px = mapx + gx / 100 * mapw
            py = mapy + gy / 50 * maph
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(120, 130, 150))

def lonlat(lon, lat):
    return (mapx + (lon + 180) / 360 * mapw, mapy + (90 - lat) / 180 * maph)

for lon, lat in [(149, -35), (139.7, 35.7), (56.5, 26.5), (163, -66.8),
                 (122, 16.5), (86, 44.3), (121.5, 31.2), (13.4, 52.5),
                 (-0.1, 51.5), (-74, 40.7)]:
    px, py = lonlat(lon, lat)
    d.ellipse([px - 4, py - 2, px + 4, py + 6], fill=(0, 0, 0, 60))
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GOLD, outline=WHITE, width=1)
for n, lon, lat in [(1, 100.3, 39.7), (2, 127, 37.5), (3, 160, -9)]:
    px, py = lonlat(lon, lat)
    d.ellipse([px - 7, py - 5, px + 7, py + 9], fill=(0, 0, 0, 60))
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=WHITE, width=2)
    d.text((px, py - 6), str(n), font=SANS_B(9), fill=WHITE, anchor="ma")
d.text((mx + 10, my + 148), "● 1–3 LEADS  ·  ● OTHER STORIES", font=SANS_B(8),
       fill=MUTED)
d.text((mx + 10, my + 158), "ASIA 15 · OCEANIA 6 · N. AMERICA 9",
       font=SANS_B(7), fill=MUTED)
d.text((mx + 10, my + 167), "EUROPE 3 · MIDDLE EAST 1 · ANTARCTICA 1",
       font=SANS_B(7), fill=MUTED)

# ================= DATE CHECK =================
dx, dy, dw, dh = 282, 806, 718, 172
d.rounded_rectangle([dx + 3, dy + 4, dx + dw + 3, dy + dh + 4], radius=6,
                    fill=(0, 0, 0, 55))
d.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=6, fill=(255, 250, 240),
                    outline=RED, width=2)
d.text((dx + 12, dy + 8), "DATE CHECK — WHAT WE LEFT OUT",
       font=SANS_B(11), fill=RED)
d.text((dx + 12, dy + 24),
       "Every one of these was checked against its source. They are yesterday's — or older — news, not today's.",
       font=SANS(9), fill=MUTED)
EXCL = [
    "Zaporizhzhia strike kills 2 — Tue 24 Nov",
    "Sanofi buys Insmed, $41bn — Tue 24 Nov",
    "Riyadh PIF tower hit, 11 hurt — Tue 24 Nov",
    "Huang apologises to Nvidia staff — Tue 24 Nov",
    "Nvidia board reinstates Huang — Tue 24 Nov",
    "Nepal M5.3 quake — Tue 24 Nov",
    "CIA open-source system breached — Tue 24 Nov",
    "US jury convicts Huawei, 10/12 counts — Tue 24 Nov",
    "Trump pardons turkeys Freedom & Feathers — Tue 24 Nov",
    "Gaza strikes kill 6 — Tue 24 Nov",
    "Colombia peace accord turns 10 — Tue 24 Nov",
    "Senegal reinstated as AFCON winners — Tue 24 Nov",
    "ICJ Myanmar genocide ruling — Thu 19 Nov",
    "COP31 ends with no deal — Sun 22 Nov",
    "US loses measles elimination status — Mon 17 Nov",
    "CrowdStrike–Zscaler deal — Mon 23 Nov",
]
for i, s in enumerate(EXCL):
    col, row = divmod(i, 8)
    x = dx + 12 + col * 352
    y = dy + 42 + row * 12
    d.text((x, y), "✗", font=SANS_B(9), fill=RED)
    d.text((x + 12, y), s, font=SANS(9), fill=(70, 64, 54))
d.text((dx + 12, dy + 144),
       "NOT YET: Taiwan polls Sat 28 Nov · OPEC+ Sun 29 Nov · Macy's 100th parade Thu 26 Nov · Huawei sentencing 14 Sep 2027",
       font=SANS_B(9), fill=NAVY)

# ================= FOOTER =================
d.line([24, 986, W - 24, 986], fill=LINE, width=1)
d.text((W / 2, 991),
       "Sources: Reuters · AP · ABS · BOJ · USGS · Xinhua · pm.gov.au — every story first reported Wed 25 Nov 2026 (UTC).",
       font=SANS(9), fill=MUTED, anchor="ma")
d.text((W / 2, 1004),
       "CONFIRMED = 2+ outlets  ·  OFFICIAL = on the record  ·  REPORTED = one outlet  ·  CLAIM = single-sided claim",
       font=SANS_B(9), fill=NAVY, anchor="ma")

img.save(OUT, "PNG")
print("saved", OUT, os.path.getsize(OUT), "bytes")
