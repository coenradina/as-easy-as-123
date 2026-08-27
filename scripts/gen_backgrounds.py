#!/usr/bin/env python3
"""Generates the two cozy pixel-art background scenes (desktop + mobile).

Deliberately tiny native resolution, hard-edged (no anti-aliasing) shapes —
the CSS displays these with `image-rendering: pixelated` so the browser
does the chunky upscaling, which is what gives it the RPG pixel-art look.

Run: python3 scripts/gen_backgrounds.py
Outputs: assets/bg-desktop.png, assets/bg-mobile.png
"""
import os
from PIL import Image, ImageDraw

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- palette --
SKY_TOP = (33, 27, 46)
SKY_MID = (94, 56, 74)
SKY_LOW = (191, 108, 76)
SKY_GLOW = (232, 160, 106)

STAR = (246, 234, 208)
MOON = (243, 227, 195)
MOON_RIM = (214, 191, 150)

HILL_FAR = (124, 143, 110)
HILL_MID = (92, 112, 82)
HILL_NEAR = (58, 78, 51)

ROOF = (181, 99, 63)
ROOF_DARK = (146, 73, 46)
WALL = (234, 217, 184)
WALL_SHADE = (216, 195, 156)
DOOR = (107, 66, 38)
WINDOW = (244, 200, 105)
WINDOW_FRAME = (74, 52, 35)
CHIMNEY = (138, 117, 102)
SMOKE = (207, 197, 180)

TRUNK = (74, 52, 35)
LEAF_DARK = (61, 87, 48)
LEAF_MID = (79, 107, 63)
LEAF_LIGHT = (99, 128, 78)

PATH = (201, 177, 137)
PATH_SHADE = (182, 157, 118)
FIREFLY = (246, 224, 138)
FLOWER_TERRA = (196, 108, 78)
FLOWER_CREAM = (238, 222, 190)


def vgrad(draw, x0, x1, y0, y1, c0, c1):
    span = max(1, y1 - y0)
    for i, y in enumerate(range(y0, y1)):
        t = i / span
        c = tuple(int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def stars(draw, coords, color=STAR):
    for (x, y) in coords:
        draw.point((x, y), fill=color)


def moon(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MOON_RIM)
    draw.ellipse([cx - r + 1, cy - r + 1, cx + r - 1, cy + r - 1], fill=MOON)


def hill(draw, width, base_y, points, color):
    """points: list of (x, y) offsets from base_y forming the ridge line."""
    poly = [(0, base_y)] + points + [(width, base_y), (width, base_y + 40), (0, base_y + 40)]
    draw.polygon(poly, fill=color)


def pine(draw, cx, base_y, height, tiers, trunk_h, leaf_color, trunk_w=3):
    draw.rectangle(
        [cx - trunk_w // 2, base_y - trunk_h, cx + trunk_w // 2, base_y],
        fill=TRUNK,
    )
    top = base_y - trunk_h
    tier_h = height // tiers
    w = height * 0.62
    for i in range(tiers):
        y0 = top - (i + 1) * tier_h + tier_h // 3
        y1 = top - i * tier_h + tier_h // 2
        tw = w * (1 - i / (tiers + 1.4))
        draw.polygon(
            [(cx, y0), (cx - tw / 2, y1), (cx + tw / 2, y1)],
            fill=leaf_color,
        )


def cottage(draw, x0, y0, w, h, scale=1):
    roof_h = int(h * 0.55)
    wall_top = y0 + roof_h
    # walls
    draw.rectangle([x0, wall_top, x0 + w, y0 + h], fill=WALL)
    draw.rectangle([x0, y0 + h - 2, x0 + w, y0 + h], fill=WALL_SHADE)
    # roof
    draw.polygon(
        [(x0 - 3, wall_top), (x0 + w // 2, y0), (x0 + w + 3, wall_top)],
        fill=ROOF,
    )
    draw.polygon(
        [(x0 - 3, wall_top), (x0 + w // 2, y0), (x0 + w // 2, wall_top)],
        fill=ROOF_DARK,
    )
    # chimney
    ch_w = max(3, w // 8)
    ch_x = x0 + int(w * 0.72)
    ch_top = y0 + int(roof_h * 0.15)
    draw.rectangle([ch_x, ch_top, ch_x + ch_w, wall_top - 2], fill=CHIMNEY)
    # smoke puffs
    for i, (dx, dy, r) in enumerate([(1, -3, 2), (-1, -8, 2), (2, -13, 1)]):
        draw.ellipse(
            [ch_x + ch_w // 2 + dx - r, ch_top + dy - r, ch_x + ch_w // 2 + dx + r, ch_top + dy + r],
            fill=SMOKE,
        )
    # door
    door_w = max(4, int(w * 0.22))
    door_h = int((y0 + h) - (wall_top + h * 0.15))
    door_x = x0 + int(w * 0.56)
    door_y = y0 + h - door_h
    draw.rectangle([door_x, door_y, door_x + door_w, y0 + h], fill=DOOR)
    # window (glowing)
    win_w = max(4, int(w * 0.2))
    win_x = x0 + int(w * 0.16)
    win_y = wall_top + int((h - roof_h) * 0.22)
    draw.rectangle([win_x - 1, win_y - 1, win_x + win_w + 1, win_y + win_w + 1], fill=WINDOW_FRAME)
    draw.rectangle([win_x, win_y, win_x + win_w, win_y + win_w], fill=WINDOW)


def path_strip(draw, x0, y0, x1, y1, width_top, width_bottom, color=PATH, shade=PATH_SHADE):
    draw.polygon(
        [
            (x0 - width_top / 2, y0),
            (x0 + width_top / 2, y0),
            (x1 + width_bottom / 2, y1),
            (x1 - width_bottom / 2, y1),
        ],
        fill=color,
    )
    # a few stone flecks
    import itertools
    for i in range(6):
        t = i / 6
        y = int(y0 + (y1 - y0) * t)
        w = width_top + (width_bottom - width_top) * t
        x = int(x0 + (x1 - x0) * t + (w / 4 if i % 2 else -w / 4))
        draw.point((x, y), fill=shade)


def fireflies(draw, coords):
    for (x, y) in coords:
        draw.point((x, y), fill=FIREFLY)


def flowers(draw, coords):
    for i, (x, y) in enumerate(coords):
        c = FLOWER_TERRA if i % 2 == 0 else FLOWER_CREAM
        draw.point((x, y), fill=c)


# ============================================================== DESKTOP ==
def make_desktop():
    W, H = 160, 90
    img = Image.new("RGB", (W, H), SKY_TOP)
    d = ImageDraw.Draw(img)

    vgrad(d, 0, W, 0, 58, SKY_TOP, SKY_MID)
    vgrad(d, 0, W, 58, 72, SKY_MID, SKY_LOW)
    d.rectangle([0, 72, W, 90], fill=SKY_LOW)

    moon(d, 132, 14, 7)
    stars(d, [
        (10, 6), (20, 14), (34, 5), (46, 18), (58, 8), (70, 4), (86, 12),
        (14, 22), (26, 26), (100, 6), (110, 16), (150, 24), (142, 8), (6, 15),
    ])

    hill(d, W, 62, [(20, 54), (55, 60), (90, 52), (125, 58), (160, 54)], HILL_FAR)
    hill(d, W, 70, [(0, 66), (35, 72), (75, 64), (115, 70), (160, 66)], HILL_MID)
    hill(d, W, 90, [(0, 74), (40, 68), (80, 76), (120, 70), (160, 78)], HILL_NEAR)

    # trees flanking the cottage
    pine(d, 26, 78, 30, 3, 14, LEAF_DARK, trunk_w=3)
    pine(d, 16, 82, 22, 3, 10, LEAF_MID, trunk_w=2)
    pine(d, 138, 80, 26, 3, 12, LEAF_DARK, trunk_w=3)
    pine(d, 149, 84, 18, 3, 9, LEAF_MID, trunk_w=2)

    path_strip(d, 90, 62, 90, 90, 6, 16)
    cottage(d, 62, 42, 56, 34)

    fireflies(d, [(45, 76), (50, 80), (118, 78), (124, 74), (60, 84), (100, 82)])
    flowers(d, [(58, 88), (62, 87), (122, 88), (126, 87), (48, 89), (132, 89)])

    img.save(os.path.join(OUT_DIR, "bg-desktop.png"))
    print("wrote bg-desktop.png", img.size)


# =============================================================== MOBILE ==
def make_mobile():
    W, H = 100, 178
    img = Image.new("RGB", (W, H), SKY_TOP)
    d = ImageDraw.Draw(img)

    vgrad(d, 0, W, 0, 78, SKY_TOP, SKY_MID)
    vgrad(d, 0, W, 78, 96, SKY_MID, SKY_LOW)
    d.rectangle([0, 96, W, 178], fill=SKY_LOW)

    moon(d, 74, 20, 8)
    stars(d, [
        (10, 10), (22, 22), (36, 8), (50, 26), (16, 34), (30, 40), (60, 14),
        (8, 50), (44, 46), (66, 30), (12, 62), (54, 6),
    ])

    hill(d, W, 88, [(0, 80), (30, 88), (60, 76), (100, 84)], HILL_FAR)
    hill(d, W, 98, [(0, 92), (35, 100), (70, 90), (100, 96)], HILL_MID)
    # solid ground fill so no horizon-glow color shows through below the
    # hill ridges (the hill() polygons only extend a little past base_y)
    d.rectangle([0, 96, W, H], fill=HILL_MID)

    # tall framing pines
    pine(d, 14, 150, 46, 4, 22, LEAF_DARK, trunk_w=4)
    pine(d, 86, 152, 42, 4, 20, LEAF_DARK, trunk_w=4)
    pine(d, 26, 160, 30, 3, 14, LEAF_MID, trunk_w=3)
    pine(d, 76, 162, 26, 3, 12, LEAF_MID, trunk_w=3)

    path_strip(d, 50, 100, 50, 178, 8, 26)
    cottage(d, 34, 78, 32, 22)

    hill(d, W, 178, [(0, 168), (30, 174), (60, 166), (100, 172)], HILL_NEAR)

    fireflies(d, [(20, 140), (24, 146), (78, 142), (82, 148), (50, 158), (60, 152)])
    flowers(d, [(30, 168), (34, 170), (70, 168), (66, 170), (44, 174), (56, 173)])

    img.save(os.path.join(OUT_DIR, "bg-mobile.png"))
    print("wrote bg-mobile.png", img.size)


if __name__ == "__main__":
    make_desktop()
    make_mobile()
