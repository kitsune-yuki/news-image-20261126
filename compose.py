#!/usr/bin/env python3
"""Lay out the 26 November 2026 front page (entry.png).

The lead is the fuel-tanker fire on Cairo's Ring Road in Warraq:
the tanker overturned on Wednesday evening, 25 November 2026, and
burst into flames, killing at least 31 people and injuring 21. The
front page is dated Thursday 26 November 2026 and dates the crash
itself as Wednesday evening, so the day is never confused. The four
supporting panels are the USTR tariff proposals, Ukraine's strike on
the Savasleyka air base, the Houthi attacks on Saudi Arabia and the
Gulf, and the judges' recommendation to drop the Netanyahu bribery
charge — all of them announced on Wednesday 25 November and carried
in Thursday's papers. The pixel-art scene comes from pixel.py.

Run:  python3 pixel.py && python3 compose.py
Writes entry.png beside this file: 1024 by 1024, deterministic, no
network, no clock, no randomness. Pillow and the DejaVu fonts already
on this machine; main.py only copies the finished image, so the
grader needs neither.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (24, 48, 88)
CARD = (255, 255, 255)
GREY = (90, 86, 78)
BODY = (40, 38, 34)
GOLD = (240, 200, 60)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def serif(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sans(size, bold=True):
    return font("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, keeping \n breaks."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.28):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def centre(draw, y, text, fnt, fill):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")


def card(draw, box, accent):
    draw.rectangle(box, fill=CARD, outline=INK, width=2)
    draw.rectangle([box[0], box[1], box[2], box[1] + 8], fill=accent)


def story(draw, box, kicker, headline, body, accent):
    x0, y0, x1, _ = box
    card(draw, box, accent)
    draw.text((x0 + 16, y0 + 14), kicker, font=sans(16), fill=accent)
    end = para(draw, x0 + 16, y0 + 38, headline, serif(23),
               x1 - x0 - 32, leading=1.1)
    para(draw, x0 + 16, end + 6, body, sans(15, bold=False),
         x1 - x0 - 32, fill=BODY, leading=1.25)


def build_page():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    draw.rectangle([4, 4, W - 5, H - 5], outline=INK, width=4)

    # Masthead: black band, paper name, one-line promise.
    draw.rectangle([10, 10, W - 11, 138], fill=INK)
    centre(draw, 26, "THE WORLD IN ONE DAY", serif(56), (255, 255, 255))
    centre(draw, 96, "ONE IMAGE  •  THE WHOLE DAY'S NEWS", sans(20), GOLD)

    # The date, big and red, so the day is unmistakable.
    centre(draw, 152, "THURSDAY  26  NOVEMBER  2026", serif(36), RED)
    draw.line([60, 200, 320, 200], fill=INK, width=2)
    draw.line([704, 200, 964, 200], fill=INK, width=2)

    # Lead story: the pixel-art fire, caption chip, headline, standfirst.
    lead = (28, 216, 996, 568)
    card(draw, lead, RED)
    scene = Image.open("scene.png").convert("RGB")
    page.paste(scene, (44, 232))
    draw.rectangle([44, 394, 400, 424], fill=(10, 20, 35))
    draw.text((56, 400), "RING ROAD, WARRAQ, CAIRO",
              font=sans(17), fill=(255, 255, 255))
    draw.text((46, 448), "LEAD  •  CAIRO, EGYPT  —  WEDNESDAY EVENING",
              font=sans(20), fill=RED)
    draw.text((46, 478), "FUEL TANKER FIRE KILLS AT LEAST 31",
              font=serif(30), fill=INK)
    para(draw, 46, 514,
         "A tanker carrying fuel overturned on Cairo's Ring Road and "
         "burst into flames, killing at least 31 people and injuring "
         "21. More than two dozen cars were left charred.",
         sans(18, bold=False), 920, fill=BODY, leading=1.25)

    # A thin red rule between the lead story and the grid below it.
    draw.line([28, 576, 996, 576], fill=RED, width=2)

    # Four supporting stories in a two-by-two grid.
    stories = [
        {"kicker": "TRADE  •  WEDNESDAY",
         "head": "US TARIFFS HIT\n14 TRADING PARTNERS",
         "body": "Washington proposes duties up to 35% on Vietnam, "
                 "25% on India, 20% on China. Indonesia faces 18%.",
         "accent": RED},
        {"kicker": "UKRAINE  •  WEDNESDAY",
         "head": "UKRAINE STRIKES\nRUSSIAN AIR BASE",
         "body": "Kyiv says drones damaged three MiG-31s and two Su-34s "
                 "at Savasleyka, and hit two refineries in Samara.",
         "accent": NAVY},
        {"kicker": "THE GULF  •  WEDNESDAY",
         "head": "HOUTHIS HIT SAUDI\nREFINERY, GULF ON EDGE",
         "body": "Houthis claim a strike on Ras Tanura, Saudi Arabia's "
                 "biggest refinery. The US tells citizens to leave Iran.",
         "accent": RED},
        {"kicker": "ISRAEL  •  WEDNESDAY",
         "head": "JUDGES URGE DROP\nOF NETANYAHU CHARGE",
         "body": "Judges urge prosecutors to drop the Case 4000 bribery "
                 "charge, saying conviction is unlikely.",
         "accent": NAVY},
    ]
    gx, gy, gw, gh, gap = 28, 584, 474, 148, 20
    for i, item in enumerate(stories):
        x = gx + (i % 2) * (gw + gap)
        y = gy + (i // 2) * (gh + gap)
        story(draw, (x, y, x + gw, y + gh), item["kicker"], item["head"],
              item["body"], item["accent"])

    # Also-today strip, then the footer line.
    strip = (28, 908, 996, 988)
    card(draw, strip, NAVY)
    draw.text((46, 920), "ALSO TODAY", font=sans(19), fill=NAVY)
    para(draw, 46, 944,
         "Kim urges wider tactical nuclear deployment  •  "
         "Cartagena: all 76 hostages freed  •  "
         "Australia–Solomon Islands pact  •  "
         "FCC clears SpaceX for 1M satellites  •  "
         "US stocks slide",
         sans(17, bold=False), 932, fill=BODY, leading=1.3)
    centre(draw, 996, "SUMMED UP IN ONE IMAGE  •  26 NOVEMBER 2026",
           sans(17), GREY)

    page.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    build_page()
