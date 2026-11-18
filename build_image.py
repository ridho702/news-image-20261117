#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261117.

One 1024x1024 infographic summarising the world news of Tuesday
17 November 2026. All facts were researched from reputable outlets
(BBC, AP, CBS News, NPR, Al Jazeera, UN News) on 18 Nov 2026 and are
listed with sources in README.md. No invented news, no fake quotes.

Run: python3 build_image.py  -> writes entry.png next to this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 241, 232)
INK = (20, 20, 20)
NAVY = (15, 27, 45)
CARD = (255, 255, 255)
GREY = (90, 90, 90)
RED = (180, 35, 24)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

def fit_font(draw, text, name, start, max_w):
    """Largest font size <= start whose rendered text fits max_w."""
    size = start
    while size > 10:
        f = font(name, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(name, 10)

def wrap(draw, text, f, max_w, max_lines=2):
    """Word-wrap text to at most max_lines lines; adds '...' if cut short."""
    words = text.split()
    lines, cur = [], ""
    truncated = False
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        elif len(lines) < max_lines - 1:
            lines.append(cur)
            cur = w
        else:
            # last line: keep adding words only while they fit with "..." room
            t2 = (cur + " " + w).strip()
            if draw.textlength(t2 + "...", font=f) <= max_w:
                cur = t2
            else:
                truncated = True
                break
    if cur:
        lines.append(cur)
    if truncated and lines:
        last = lines[-1] + "..."
        while draw.textlength(last, font=f) > max_w and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
            last = lines[-1] + "..."
        lines[-1] = last
    return lines

def rounded(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)

# ---- simple white pictograms drawn inside a coloured square ----
def icon_burst(d, x, y, s, c):
    cx, cy = x + s // 2, y + s // 2
    pts = []
    for i in range(16):
        r = s * 0.42 if i % 2 == 0 else s * 0.18
        a = math.pi * i / 8 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=c)

def icon_bridge(d, x, y, s, c):
    d.arc([x + s*0.08, y + s*0.18, x + s*0.92, y + s*0.95], 180, 360, fill=c, width=7)
    d.line([x + s*0.06, y + s*0.52, x + s*0.94, y + s*0.52], fill=c, width=7)
    for fx in (0.28, 0.72):
        d.line([x + s*fx, y + s*0.52, x + s*fx, y + s*0.28], fill=c, width=5)
    d.arc([x + s*0.10, y + s*0.72, x + s*0.45, y + s*0.92], 0, 180, fill=c, width=5)
    d.arc([x + s*0.55, y + s*0.72, x + s*0.90, y + s*0.92], 0, 180, fill=c, width=5)

def icon_globe(d, x, y, s, c):
    cx, cy = x + s // 2, y + s // 2
    r = s * 0.40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=6)
    d.ellipse([cx - r, cy - r*0.45, cx + r, cy + r*0.45], outline=c, width=5)
    d.ellipse([cx - r*0.45, cy - r, cx + r*0.45, cy + r], outline=c, width=5)
    d.line([cx - r, cy, cx + r, cy], fill=c, width=4)

def icon_chip(d, x, y, s, c):
    d.rounded_rectangle([x + s*0.22, y + s*0.22, x + s*0.78, y + s*0.78],
                        radius=8, outline=c, width=7)
    d.rounded_rectangle([x + s*0.40, y + s*0.40, x + s*0.60, y + s*0.60],
                        radius=4, fill=c)
    for fx in (0.35, 0.50, 0.65):
        d.line([x + s*fx, y + s*0.08, x + s*fx, y + s*0.22], fill=c, width=5)
        d.line([x + s*fx, y + s*0.78, x + s*fx, y + s*0.92], fill=c, width=5)
        d.line([x + s*0.08, y + s*fx, x + s*0.22, y + s*fx], fill=c, width=5)
        d.line([x + s*0.78, y + s*fx, x + s*0.92, y + s*fx], fill=c, width=5)

def icon_virus(d, x, y, s, c):
    cx, cy = x + s // 2, y + s // 2
    for i in range(8):
        a = math.pi * i / 4
        x1, y1 = cx + s*0.30*math.cos(a), cy + s*0.30*math.sin(a)
        x2, y2 = cx + s*0.44*math.cos(a), cy + s*0.44*math.sin(a)
        d.line([x1, y1, x2, y2], fill=c, width=6)
        d.ellipse([x2-5, y2-5, x2+5, y2+5], fill=c)
    d.ellipse([cx - s*0.28, cy - s*0.28, cx + s*0.28, cy + s*0.28], fill=c)
    d.ellipse([cx - s*0.12, cy - s*0.16, cx - s*0.02, cy - s*0.06], fill=PAPER)
    d.ellipse([cx + s*0.05, cy + s*0.08, cx + s*0.15, cy + s*0.18], fill=PAPER)

def icon_plane(d, x, y, s, c):
    pts = [(x + s*0.10, y + s*0.55), (x + s*0.88, y + s*0.14),
           (x + s*0.72, y + s*0.86), (x + s*0.52, y + s*0.62)]
    d.polygon(pts, fill=c)
    d.line([x + s*0.52, y + s*0.62, x + s*0.30, y + s*0.88], fill=c, width=6)

STORIES = [
    dict(tag="MIDDLE EAST", color=(180, 35, 24), icon=icon_burst,
         headline="US strikes Iran after drone attack on Bahrain",
         summary="US jets hit a missile site on Qeshm Island; Iran fired drones at a US radar in Bahrain - its third strike there in five days."),
    dict(tag="UKRAINE WAR", color=(29, 78, 216), icon=icon_bridge,
         headline="Kerch Bridge span falls after second day of strikes",
         summary="Ukrainian drones hit the Crimea bridge again; a road section collapsed into the strait below."),
    dict(tag="ASIA-PACIFIC", color=(14, 116, 144), icon=icon_globe,
         headline="Trump in Manila on way to Xi-Putin summit",
         summary="The US president heads to the APEC summit in Shenzhen for planned three-way nuclear talks with Xi Jinping and Vladimir Putin."),
    dict(tag="BUSINESS", color=(22, 101, 52), icon=icon_chip,
         headline="Nvidia posts record $115bn quarter",
         summary="Revenue roughly doubled year on year - but the board will not bring back ousted chief Jensen Huang."),
    dict(tag="HEALTH", color=(124, 58, 237), icon=icon_virus,
         headline="Ebola passes 11,000 cases in DR Congo",
         summary="The UN reports more than 5,400 deaths as the outbreak more than doubles in three months."),
    dict(tag="MIGRATION", color=(180, 83, 9), icon=icon_plane,
         headline="Five EU states plan Rwanda returns hub",
         summary="Germany, Denmark, Austria, Greece and the Netherlands will send rejected asylum seekers to a joint facility from 2027."),
]

ALSO = ("ALSO TODAY: US loses measles-free status after 26 years  |  "
        "Depardieu admits assault charge in Paris  |  "
        "Nepal first to get UN climate-loss funds")
SOURCES = "Sources: BBC  |  AP  |  CBS News  |  NPR  |  Al Jazeera  |  UN News"

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.rectangle([0, 132, W, 138], fill=RED)
    f_date = fit_font(d, "TUESDAY, 17 NOVEMBER 2026", "DejaVuSans-Bold.ttf", 46, W - 28)
    d.text((14, 12), "TUESDAY, 17 NOVEMBER 2026", font=f_date, fill=(255, 255, 255))
    f_sub = font("DejaVuSans.ttf", 21)
    d.text((16, 82), "The world in one day - six stories that mattered",
           font=f_sub, fill=(200, 210, 225))
    f_kicker = font("DejaVuSans-Bold.ttf", 17)
    d.text((W - 16 - d.textlength("WORLD NEWS", font=f_kicker), 20),
           "WORLD NEWS", font=f_kicker, fill=(250, 180, 60))

    # ---- story rows ----
    top, row_h, gap, margin = 150, 132, 6, 14
    card_w = W - 2 * margin
    for i, s in enumerate(STORIES):
        y = top + i * (row_h + gap)
        rounded(d, [margin, y, margin + card_w, y + row_h], 10, CARD)
        # icon square
        ix, iy, isize = margin + 12, y + 16, 100
        rounded(d, [ix, iy, ix + isize, iy + isize], 12, s["color"])
        s["icon"](d, ix + 12, iy + 12, isize - 24, (255, 255, 255))
        tx = margin + 12 + isize + 16
        tw = margin + card_w - 14 - tx
        # tag
        f_tag = font("DejaVuSans-Bold.ttf", 17)
        d.text((tx, y + 10), s["tag"], font=f_tag, fill=s["color"])
        # headline, one line, shrunk to fit
        f_head = fit_font(d, s["headline"], "DejaVuSans-Bold.ttf", 27, tw)
        d.text((tx, y + 34), s["headline"], font=f_head, fill=INK)
        # summary, up to two lines
        f_sum = font("DejaVuSans.ttf", 19)
        lines = wrap(d, s["summary"], f_sum, tw, max_lines=2)
        for j, line in enumerate(lines):
            d.text((tx, y + 68 + j * 24), line, font=f_sum, fill=(60, 60, 60))

    # ---- footer strip ----
    fy = top + 6 * row_h + 5 * gap  # 150 + 792 + 30 = 972
    d.rectangle([0, fy, W, H], fill=NAVY)
    f_also = fit_font(d, ALSO, "DejaVuSans-Bold.ttf", 16, W - 28)
    d.text((14, fy + 8), ALSO, font=f_also, fill=(255, 255, 255))
    f_src = fit_font(d, SOURCES, "DejaVuSans.ttf", 14, W - 28)
    d.text((14, fy + 30), SOURCES, font=f_src, fill=(170, 180, 195))

    img.save("entry.png", optimize=True)
    print("wrote entry.png")

if __name__ == "__main__":
    main()
