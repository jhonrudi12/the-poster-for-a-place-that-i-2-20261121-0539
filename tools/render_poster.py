#!/usr/bin/env python3
"""Render the VELMORA travel poster (build time only, Pillow).

A travel poster for a place that does not exist: VELMORA, the island above
the clouds. One landmark (the white Cloudspire tower), one palette
(deep-indigo sky grading to golden-hour gold, coral/cream cloud sea).
Deterministic: fixed coordinates, no randomness, no clock, no network.
Writes assets/poster.png, 1024x1024.
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "assets", "poster.png")

W = H = 1024

SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

# Palette
INDIGO_TOP = (24, 22, 64)
INDIGO_MID = (56, 44, 104)
DUSK = (138, 78, 118)
GOLD_HORIZON = (255, 186, 108)
SUN_CORE = (255, 232, 176)
SUN_GLOW = (255, 196, 120)
CREAM = (255, 244, 222)
CREAM_DIM = (238, 214, 180)
CLOUD_LIGHT = (255, 236, 214)
CLOUD_MID = (247, 196, 168)
CLOUD_SHADOW = (214, 148, 158)
ROCK = (52, 40, 84)
ROCK_LIT = (96, 68, 118)
PLATEAU = (196, 158, 92)
TOWER = (250, 240, 224)
TOWER_SHADE = (214, 196, 178)
WINDOW = (255, 196, 90)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(img, y0, y1, stops):
    """Fill rows y0..y1 with a multi-stop vertical gradient."""
    d = ImageDraw.Draw(img)
    n = y1 - y0
    for y in range(y0, y1):
        t = y / max(1, n)
        # find segment
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                f = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
                d.line([(0, y), (W, y)], fill=lerp(c0, c1, f))
                break


def tracked_text(draw, cx, y, text, font, fill, tracking):
    """Draw text centred on cx with extra tracking between glyphs."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking
    return total


def soft_ellipse(layer, box, fill):
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=fill)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # ---- sky: indigo -> dusk -> gold, down to the horizon (y=640) ----
    vertical_gradient(img, 0, 660, [
        (0.0, INDIGO_TOP),
        (0.45, INDIGO_MID),
        (0.75, DUSK),
        (1.0, GOLD_HORIZON),
    ])
    # warm haze band right above the horizon
    haze = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(haze)
    for i in range(90):
        a = int(70 * (1 - i / 90))
        hd.line([(0, 560 + i), (W, 560 + i)], fill=(255, 200, 130, a))
    img.paste(Image.alpha_composite(img.convert("RGBA"), haze).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)

    # ---- stars in the upper sky (fixed positions) ----
    stars = [(90, 60, 2), (180, 34, 1), (300, 90, 2), (420, 44, 1), (640, 70, 2),
             (760, 40, 1), (880, 96, 2), (940, 50, 1), (130, 150, 1), (700, 140, 1),
             (60, 230, 1), (950, 210, 1), (520, 30, 1), (360, 150, 1)]
    for x, y, r in stars:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 220))

    # ---- sun disc + glow, low near the horizon, clear of the island ----
    sun_cx, sun_cy, sun_r = 180, 500, 42
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in ((90, 26), (68, 40), (50, 60)):
        gd.ellipse([sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r],
                   fill=SUN_GLOW + (a,))
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
                 fill=SUN_CORE)
    # sun sits partly behind the cloud sea: it will be overlapped by clouds

    # birds (kept clear of the sun and the title)
    for bx, by, s in [(330, 300, 14), (380, 268, 11), (830, 330, 12), (880, 296, 9),
                      (700, 340, 9)]:
        draw.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340, fill=(40, 32, 70), width=3)
        draw.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340, fill=(40, 32, 70), width=3)

    # ---- cloud sea: layered soft clouds from y=620 to the bottom ----
    clouds = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(clouds)
    # base sea
    cd.rectangle([0, 640, W, H], fill=CLOUD_MID + (255,))
    # distant cloud band (lighter, catching the sun)
    for (x, y, rx, ry, col) in [
            (60, 600, 260, 46, CLOUD_LIGHT), (420, 585, 300, 52, CLOUD_LIGHT),
            (800, 605, 260, 48, (255, 222, 190)), (180, 640, 320, 60, CLOUD_LIGHT),
            (640, 645, 340, 62, (255, 226, 196)),
            (120, 668, 200, 40, CLOUD_LIGHT), (880, 668, 220, 42, CLOUD_LIGHT),
            (540, 672, 200, 38, (255, 230, 200))]:
        cd.ellipse([x - rx, y - ry, x + rx, y + ry], fill=col + (255,))
    # mid clouds
    for (x, y, rx, ry, col) in [
            (120, 720, 300, 70, CLOUD_LIGHT), (560, 700, 330, 76, CLOUD_LIGHT),
            (920, 730, 260, 66, (255, 224, 192)), (330, 800, 340, 80, CLOUD_MID),
            (760, 810, 320, 78, CLOUD_LIGHT),
            (180, 780, 180, 46, (255, 232, 204)), (860, 850, 200, 50, CLOUD_MID),
            (120, 610, 150, 34, (255, 240, 220)), (900, 612, 170, 36, (255, 238, 216))]:
        cd.ellipse([x - rx, y - ry, x + rx, y + ry], fill=col + (255,))
    # small bright puffs for texture in the lower sea
    for (x, y, rx, ry, col) in [
            (420, 860, 120, 34, CLOUD_LIGHT), (640, 880, 130, 36, (255, 232, 204)),
            (220, 880, 110, 30, CLOUD_LIGHT), (820, 760, 110, 30, CLOUD_LIGHT)]:
        cd.ellipse([x - rx, y - ry, x + rx, y + ry], fill=col + (255,))
    # foreground clouds, warmer and shadowed underneath
    for (x, y, rx, ry, col) in [
            (60, 900, 300, 90, CLOUD_LIGHT), (520, 920, 360, 96, (255, 228, 200)),
            (950, 905, 280, 88, CLOUD_LIGHT), (300, 985, 340, 70, CLOUD_SHADOW),
            (780, 990, 320, 66, CLOUD_SHADOW),
            (140, 1000, 260, 60, (226, 160, 168)), (880, 1000, 240, 58, (226, 160, 168))]:
        cd.ellipse([x - rx, y - ry, x + rx, y + ry], fill=col + (255,))
    clouds = clouds.filter(ImageFilter.GaussianBlur(10))
    img.paste(Image.alpha_composite(img.convert("RGBA"), clouds).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)

    # soft shadow under the island on the cloud sea
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([330, 720, 700, 830], fill=(120, 70, 90, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)

    # ---- the floating island ----
    # rock body: plateau at y=500, tapering to a point at y=800
    rock_pts = [(300, 500), (724, 500), (690, 590), (640, 690), (560, 770),
                (512, 800), (464, 770), (384, 690), (334, 590)]
    draw.polygon(rock_pts, fill=ROCK)
    # warm rim light on the sun-facing (right) edge
    draw.line([(724, 500), (690, 590), (640, 690), (560, 770), (512, 800)],
              fill=ROCK_LIT, width=7)
    draw.line([(300, 500), (334, 590), (384, 690)], fill=(70, 54, 100), width=5)
    # rock facets
    draw.polygon([(430, 590), (512, 590), (512, 730), (470, 690)], fill=(44, 34, 72))
    draw.polygon([(560, 590), (640, 590), (600, 690), (540, 670)], fill=(62, 48, 96))

    # plateau top (golden grass)
    draw.polygon([(296, 500), (728, 500), (700, 482), (324, 482)], fill=PLATEAU)
    draw.polygon([(296, 500), (728, 500), (716, 492), (308, 492)], fill=(214, 176, 108))

    # ---- the city on the plateau ----
    # small white houses
    houses = [(330, 482, 34, 26), (380, 482, 28, 20), (420, 482, 30, 24),
              (620, 482, 30, 22), (664, 482, 36, 28), (706, 482, 26, 18)]
    for x, y, w, h in houses:
        draw.rectangle([x, y - h, x + w, y], fill=TOWER)
        draw.polygon([(x - 2, y - h), (x + w // 2, y - h - 12), (x + w + 2, y - h)],
                     fill=(196, 120, 110))
    # warm windows on the houses
    for x, y, w, h in houses:
        for wx in range(x + 6, x + w - 4, 10):
            draw.rectangle([wx, y - h + 6, wx + 4, y - h + 11], fill=WINDOW)

    # ---- the Cloudspire: one tall white tower, the landmark ----
    tx0, tx1 = 492, 532
    # tower shaft (spire tip at y=296, clear of the subtitle above)
    draw.rectangle([tx0, 348, tx1, 482], fill=TOWER)
    draw.rectangle([tx0 + 26, 348, tx1, 482], fill=TOWER_SHADE)
    # cornices
    draw.rectangle([tx0 - 6, 380, tx1 + 6, 390], fill=TOWER)
    draw.rectangle([tx0 - 6, 440, tx1 + 6, 450], fill=TOWER)
    # spire roof
    draw.polygon([(tx0 - 8, 348), (tx1 + 8, 348), (512, 296)], fill=(226, 148, 128))
    # beacon at the tip
    draw.ellipse([506, 288, 518, 300], fill=(255, 214, 120))
    beacon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beacon)
    bd.ellipse([492, 274, 532, 314], fill=(255, 214, 120, 70))
    beacon = beacon.filter(ImageFilter.GaussianBlur(6))
    img.paste(Image.alpha_composite(img.convert("RGBA"), beacon).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)
    # tower windows: a vertical row of warm lights
    for wy in range(400, 478, 22):
        draw.rectangle([508, wy, 516, wy + 10], fill=WINDOW)
    # tiny pennant
    draw.line([(512, 296), (512, 272)], fill=(60, 44, 90), width=2)
    draw.polygon([(512, 272), (540, 279), (512, 286)], fill=(255, 120, 110))

    # ---- type ----
    title_font = ImageFont.truetype(SERIF_BOLD, 140)
    sub_font = ImageFont.truetype(SANS_BOLD, 32)
    foot_font = ImageFont.truetype(SANS, 27)

    # VELMORA — big cream serif, top centre
    tracked_text(draw, W // 2, 56, "VELMORA", title_font, CREAM, tracking=26)
    # thin rules flanking the subtitle
    sub_y = 210
    sub_w = draw.textlength("ABOVE THE CLOUDS", font=sub_font) + 8 * 11
    rule_y = sub_y + 17
    draw.line([(W // 2 - sub_w // 2 - 130, rule_y), (W // 2 - sub_w // 2 - 24, rule_y)],
              fill=CREAM_DIM, width=2)
    draw.line([(W // 2 + sub_w // 2 + 24, rule_y), (W // 2 + sub_w // 2 + 130, rule_y)],
              fill=CREAM_DIM, width=2)
    tracked_text(draw, W // 2, sub_y, "ABOVE THE CLOUDS", sub_font, CREAM_DIM, tracking=8)

    # bottom line
    tracked_text(draw, W // 2, 946, "WHERE THE SKY BEGINS", foot_font, CREAM, tracking=6)

    # ---- poster frame ----
    draw.rectangle([26, 26, W - 26, H - 26], outline=CREAM, width=3)
    draw.rectangle([36, 36, W - 36, H - 36], outline=(255, 244, 222, 90), width=1)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
