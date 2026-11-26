#!/usr/bin/env python3
"""Pixel-art dusk fire for the 26 November 2026 front page.

A fuel tanker overturned on Cairo's Ring Road in Warraq on Wednesday
evening, 25 November 2026, and burst into flames: at least 31 people
killed, 21 injured, more than two dozen cars charred. The picture is
built one pixel at a time on a 234 by 48 grid — a graded dusk sky, a
low sun, the Cairo skyline with a minaret, the elevated ring road
with its cars, the overturned tanker, a layered fire column and smoke
drifting over the city. It is scaled up with NEAREST so every pixel
stays crisp.

Deterministic: one fixed seed, no network, no clock.

Run:  python3 pixel.py
Writes scene.png beside this file: 936 by 192.
"""
import random

from PIL import Image, ImageDraw

W, H = 234, 48
SCALE = 4
SEED = 1126

PAL = {
    "night": (14, 18, 44),
    "violet": (58, 42, 90),
    "magenta": (140, 58, 90),
    "ember": (214, 104, 50),
    "amber": (250, 158, 66),
    "sun": (255, 222, 130),
    "glow": (255, 168, 76),
    "skyline": (26, 22, 34),
    "skyline_far": (40, 32, 48),
    "lamp": (255, 206, 96),
    "deck": (72, 70, 72),
    "deck_top": (104, 102, 100),
    "deck_dark": (46, 44, 46),
    "asphalt": (38, 36, 40),
    "pillar": (56, 54, 56),
    "ground": (22, 20, 24),
    "ground_lit": (64, 40, 28),
    "tank": (176, 172, 164),
    "tank_shade": (120, 116, 110),
    "tank_dark": (58, 54, 52),
    "cab": (150, 40, 32),
    "car": (28, 28, 34),
    "car_lit": (70, 66, 60),
    "headlight": (255, 232, 150),
    "taillight": (255, 60, 40),
    "flame_white": (255, 248, 214),
    "flame_yellow": (255, 210, 88),
    "flame_orange": (255, 146, 38),
    "flame_red": (228, 66, 18),
    "flame_deep": (168, 30, 12),
    "smoke_dark": (88, 84, 88),
    "smoke": (140, 136, 138),
    "smoke_light": (192, 188, 190),
    "smoke_pale": (224, 220, 222),
    "smoke_warm": (255, 178, 88),
    "debris": (96, 88, 80),
}


def build():
    rng = random.Random(SEED)
    canvas = Image.new("RGB", (W, H), PAL["night"])
    pen = ImageDraw.Draw(canvas)

    def dot(x, y, name):
        if 0 <= x < W and 0 <= y < H:
            canvas.putpixel((x, y), PAL[name])

    def stripe(y0, y1, name):
        pen.rectangle([0, y0, W - 1, y1], fill=PAL[name])

    def speckle(y, first, second):
        for x in range(W):
            dot(x, y, first if (x + y) % 2 == 0 else second)

    def disc(cx, cy, rx, ry, name):
        pen.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=PAL[name])

    def diamond(cx, cy, radius, name):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if abs(dx) + abs(dy) <= radius:
                    dot(cx + dx, cy + dy, name)

    # Dusk sky, graded from indigo at the top to amber at the horizon.
    for y0, y1, name in [
        (0, 6, "night"), (7, 11, "violet"), (12, 16, "magenta"),
        (17, 20, "ember"), (21, 23, "amber"),
    ]:
        stripe(y0, y1, name)
    speckle(11, "violet", "magenta")
    speckle(16, "magenta", "ember")
    speckle(20, "ember", "amber")

    # A few early stars high up, fading into the dusk.
    for _ in range(26):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, 6)
        dot(x, y, "sun" if rng.random() < 0.3 else "smoke_light")

    # Low sun sinking behind the skyline, left of centre.
    diamond(52, 19, 6, "glow")
    diamond(52, 19, 3, "sun")
    dot(52, 19, "flame_white")

    # Cairo skyline along the horizon: blocks, a minaret, lit windows.
    for bx, bw, bh in [
        (0, 22, 3), (24, 16, 5), (42, 12, 2), (58, 20, 4), (80, 14, 6),
        (96, 18, 3), (150, 20, 5), (172, 12, 3), (186, 22, 6),
        (210, 24, 4),
    ]:
        pen.rectangle([bx, 24 - bh, bx + bw, 24], fill=PAL["skyline"])
    # Minaret: thin tower with a pointed cap, right of the fire.
    pen.rectangle([196, 12, 198, 24], fill=PAL["skyline"])
    pen.rectangle([195, 11, 199, 12], fill=PAL["skyline"])
    dot(197, 9, "skyline")
    dot(197, 10, "skyline")
    # A farther, paler row of blocks behind the first.
    for bx, bw, bh in [(10, 18, 2), (66, 14, 2), (120, 16, 2), (160, 14, 2)]:
        pen.rectangle([bx, 24 - bh, bx + bw, 24], fill=PAL["skyline_far"])
    # Lit windows in the skyline.
    for wx, wy in [(8, 22), (30, 21), (48, 22), (66, 22), (86, 20),
                   (104, 22), (156, 21), (176, 22), (192, 20), (216, 22),
                   (224, 21)]:
        dot(wx, wy, "lamp")

    # The elevated Ring Road deck across the whole picture.
    stripe(25, 25, "deck_top")
    stripe(26, 29, "deck")
    stripe(30, 30, "deck_dark")
    # Lane dashes on the deck.
    for x in range(4, W, 12):
        dot(x, 27, "deck_top")
        dot(x + 1, 27, "deck_top")
    # Support pillars dropping to the ground below.
    for px in (30, 108, 204):
        pen.rectangle([px, 31, px + 3, 40], fill=PAL["pillar"])
        pen.rectangle([px, 31, px + 3, 32], fill=PAL["deck_top"])

    # Ground below the overpass, dark, with the tunnel mouth.
    stripe(31, H - 1, "ground")
    speckle(33, "ground", "ground_lit")
    # Tunnel 10 mouth under the road, centre-left of the fire.
    pen.rectangle([88, 36, 132, 47], fill=PAL["night"])
    pen.rectangle([88, 36, 132, 37], fill=PAL["deck_dark"])
    for lx in (94, 104, 114, 124):
        dot(lx, 40, "headlight")
    # Fire glow washing the ground under the blaze.
    for _ in range(90):
        x = rng.randint(96, 150)
        y = rng.randint(41, 47)
        dot(x, y, "ground_lit" if rng.random() < 0.6 else "flame_orange")

    # Cars on the deck, queueing either side of the wreck.
    for cx in (6, 20, 36, 62, 74, 160, 176, 192, 208, 224):
        pen.rectangle([cx, 23, cx + 7, 25], fill=PAL["car"])
        pen.rectangle([cx + 1, 22, cx + 5, 22], fill=PAL["car_lit"])
    # Headlights facing the fire, taillights away from it.
    for hx in (14, 28, 44, 70, 82):
        dot(hx, 24, "headlight")
    for hx in (168, 184, 200, 216, 230):
        dot(hx, 24, "taillight")
    # Two burnt-out hulks near the fire, blackened shells.
    pen.rectangle([88, 23, 95, 25], fill=PAL["tank_dark"])
    pen.rectangle([142, 23, 149, 25], fill=PAL["tank_dark"])
    dot(91, 22, "flame_orange")
    dot(145, 22, "flame_orange")

    # The overturned tanker, lying across the deck at the centre.
    # Cylindrical tank tilted on its side, cab crushed beneath it.
    pen.rectangle([100, 20, 138, 24], fill=PAL["tank"])
    pen.rectangle([100, 23, 138, 24], fill=PAL["tank_shade"])
    pen.rectangle([100, 20, 138, 21], fill=PAL["smoke_pale"])
    for x in (108, 120, 132):
        pen.rectangle([x, 20, x, 24], fill=PAL["tank_shade"])
    pen.rectangle([96, 22, 100, 25], fill=PAL["cab"])
    pen.rectangle([138, 22, 142, 25], fill=PAL["tank_dark"])
    # Wheels poking up from the overturned chassis.
    for wx in (106, 118, 130):
        dot(wx, 19, "tank_dark")
        dot(wx + 1, 19, "tank_dark")

    # Fire column rising from the tanker: layered white to deep red,
    # narrow at the top, wide at the base, edges scattered by the seed.
    for dy in range(17):
        y = 20 - dy
        half = 2 + (16 - dy) // 3
        for dx in range(-half, half + 1):
            if rng.random() < 0.92:
                if dy < 3:
                    name = "flame_white" if abs(dx) <= 1 else "flame_yellow"
                elif dy < 7:
                    name = "flame_yellow" if abs(dx) <= 2 else "flame_orange"
                elif dy < 11:
                    name = "flame_orange" if abs(dx) <= 3 else "flame_red"
                else:
                    name = "flame_red" if abs(dx) <= 4 else "flame_deep"
                dot(119 + dx, y, name)
    # Bright glow halo around the base of the column.
    for _ in range(60):
        x = rng.randint(104, 134)
        y = rng.randint(21, 26)
        if rng.random() < 0.55:
            dot(x, y, "flame_orange" if rng.random() < 0.7 else "flame_yellow")
    # Sparks flying up and out from the blaze.
    for _ in range(34):
        x = 119 + rng.randint(-22, 22)
        y = rng.randint(2, 18)
        dot(x, y, "flame_yellow" if rng.random() < 0.5 else "flame_orange")

    # Smoke billowing up from the fire and drifting right.
    for cx, cy, rx, ry, name in [
        (119, 4, 10, 3, "smoke_dark"), (128, 2, 12, 3, "smoke_dark"),
        (140, 4, 12, 3, "smoke"), (152, 6, 11, 3, "smoke"),
        (164, 8, 10, 3, "smoke_light"), (176, 10, 9, 3, "smoke_light"),
        (110, 2, 8, 2, "smoke"), (100, 5, 7, 2, "smoke_dark"),
        (188, 12, 8, 2, "smoke_pale"), (200, 14, 7, 2, "smoke_pale"),
    ]:
        disc(cx, cy, rx, ry, name)
    for _ in range(60):
        x = rng.randint(96, 210)
        y = rng.randint(0, 12)
        if rng.random() < 0.5:
            dot(x, y, "smoke_pale" if rng.random() < 0.5 else "smoke_light")
    # Warm rim light on the smoke, on the side facing the flame.
    for x, y in [(112, 5), (113, 7), (111, 9), (130, 5), (129, 7),
                 (131, 9), (114, 3), (126, 3), (110, 11), (133, 11)]:
        dot(x, y, "smoke_warm" if (x + y) % 2 else "flame_orange")

    # Scattered debris on the ground below the road.
    for dx, dy in [(70, 44), (76, 45), (150, 44), (158, 46), (60, 42),
                   (170, 42), (84, 46), (140, 46)]:
        dot(dx, dy, "debris")
        dot(dx + 1, dy, "debris")

    big = canvas.resize((W * SCALE, H * SCALE), Image.NEAREST)
    big.save("scene.png", format="PNG", optimize=True)
    print("wrote scene.png", big.size)


if __name__ == "__main__":
    build()
