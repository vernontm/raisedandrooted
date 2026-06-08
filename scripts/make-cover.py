#!/usr/bin/env python3
"""
Build a premium ebook-style cover for the free guide:
full-bleed photo background + green gradient + real logo + elegant type.
Exports PNG + PDF. No call-to-action button — it reads like a book cover.
"""
import os
from PIL import Image, ImageDraw, ImageFont

A = os.path.join(os.path.dirname(__file__), "..", "assets")
F = os.path.join(os.path.dirname(__file__), "fonts")

PHOTO = os.path.join(A, "hero.jpg")          # kie.ai classroom scene (teacher + kids)
LOGO = os.path.join(A, "rr_no_bg.png")
OUT_PNG = os.path.join(A, "guide-cover-ebook.png")
OUT_PDF = os.path.join(A, "raised-and-rooted-free-guide.pdf")

W, H = 1536, 2048
GREEN = (26, 44, 29)         # deep rich green for the gradient
CREAM = (247, 243, 234)
CREAM_SOFT = (228, 226, 210)
GOLD = (216, 176, 92)
LOGO_TINT = (244, 237, 217)  # warm cream — pops on photo/green

fr_title = ImageFont.truetype(os.path.join(F, "Fraunces-SemiBold.ttf"), 120)
fr_title_it = ImageFont.truetype(os.path.join(F, "Fraunces-Italic.ttf"), 120)
ns_sub = ImageFont.truetype(os.path.join(F, "NunitoSans-SemiBold.ttf"), 41)
ns_eye = ImageFont.truetype(os.path.join(F, "NunitoSans-ExtraBold.ttf"), 30)
ns_foot = ImageFont.truetype(os.path.join(F, "NunitoSans-ExtraBold.ttf"), 27)


def cover_fill(img, w, h):
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    img = img.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def vgrad(w, h, stops):
    """Vertical alpha ramp from (fraction, alpha) stops."""
    stops = sorted(stops)
    col = Image.new("L", (1, h))
    data = []
    for yy in range(h):
        f = yy / (h - 1)
        a = stops[0][1]
        for i in range(len(stops) - 1):
            f0, a0 = stops[i]
            f1, a1 = stops[i + 1]
            if f0 <= f <= f1:
                t = 0 if f1 == f0 else (f - f0) / (f1 - f0)
                a = a0 + (a1 - a0) * t
                break
            if f > f1:
                a = a1
        data.append(int(a))
    col.putdata(data)
    return col.resize((w, h))


def tint(path, color):
    im = Image.open(path).convert("RGBA")
    a = im.getchannel("A")
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", im.size, color + (255,)), (0, 0), a)
    return out


def tracked_width(draw, text, font, track):
    return sum(draw.textlength(c, font=font) + track for c in text) - track


def draw_tracked_centered(draw, cx, y, text, font, fill, track):
    w = tracked_width(draw, text, font, track)
    x = cx - w / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    # Background photo, full-bleed
    base = cover_fill(Image.open(PHOTO).convert("RGB"), W, H).convert("RGBA")

    # Overall mood tint
    base.alpha_composite(Image.new("RGBA", (W, H), GREEN + (95,)))
    # Top band (logo + title legibility) — stays dark through the text block
    top = Image.new("RGBA", (W, H), GREEN + (255,))
    top.putalpha(vgrad(W, H, [(0.0, 252), (0.30, 238), (0.60, 70), (0.74, 0)]))
    base.alpha_composite(top)
    # Bottom grounding
    bot = Image.new("RGBA", (W, H), GREEN + (255,))
    bot.putalpha(vgrad(W, H, [(0.64, 0), (1.0, 245)]))
    base.alpha_composite(bot)

    draw = ImageDraw.Draw(base)
    cx = W / 2

    def shadow_text(x, y, text, font, fill):
        draw.text((x + 2, y + 3), text, font=font, fill=(8, 16, 10, 170))
        draw.text((x, y), text, font=font, fill=fill)

    # Thin gold border frame
    m = 40
    draw.rectangle([(m, m), (W - m, H - m)], outline=GOLD, width=3)

    # Logo (cream tint) centered near the top
    logo = tint(LOGO, LOGO_TINT)
    lw = int(W * 0.29)
    lh = round(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    base.alpha_composite(logo, ((W - lw) // 2, int(H * 0.065)))

    # Eyebrow
    y = int(H * 0.315)
    draw_tracked_centered(draw, cx, y, "THE PARENT'S GUIDE", ns_eye, GOLD, 8)
    y += 80

    # Title (wrapped, centered, with soft shadow)
    title = "The Real Numbers Behind Your Child's Future"
    lines = wrap(draw, title, fr_title, W * 0.80)
    for ln in lines:
        w = draw.textlength(ln, font=fr_title)
        shadow_text(cx - w / 2, y, ln, fr_title, CREAM)
        y += 128
    y += 16

    # Gold divider
    draw.line([(cx - 70, y), (cx + 70, y)], fill=GOLD, width=4)
    y += 48

    # Subtitle (wrapped, with soft shadow)
    sub = ("What the data really says about the school you choose, and 10 "
           "simple routines to raise a confident, capable child.")
    for ln in wrap(draw, sub, ns_sub, W * 0.72):
        w = draw.textlength(ln, font=ns_sub)
        shadow_text(cx - w / 2, y, ln, ns_sub, CREAM_SOFT)
        y += 56

    # Footer brand line
    draw_tracked_centered(draw, cx, H - 132,
                          "RAISED & ROOTED ACADEMY  ·  KATY, TX",
                          ns_foot, CREAM, 6)

    final = base.convert("RGB")
    final.save(OUT_PNG)
    final.save(OUT_PDF, "PDF", resolution=150.0)
    print(f"Saved {OUT_PNG}")
    print(f"Saved {OUT_PDF}")


if __name__ == "__main__":
    main()
