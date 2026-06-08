#!/usr/bin/env python3
"""
Recolor the Raised & Rooted logo (a navy fabric patch photo) into a clean
two-tone mark: brand-green emblem on a cream background.

Strategy: the design (cream silhouette, sage tree, gold text/star) is LIGHT;
the navy background is DARK. So we separate by luminance (Otsu threshold),
build a smooth anti-aliased mask, paint the design brand-green over a cream
field, then auto-crop to the emblem and pad to a centered square.

Output: assets/logo-green.png  (cream bg)  +  assets/logo-green-transparent.png
"""
from PIL import Image, ImageFilter, ImageOps
import os, glob, sys

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

# Auto-detect the source logo (macOS screenshot filenames use a U+202F space
# that is painful to hardcode). Prefer an explicit argv path if given.
if len(sys.argv) > 1:
    SRC = sys.argv[1]
else:
    candidates = [p for p in glob.glob(os.path.join(ASSETS, "*.png"))
                  if "logo-green" not in os.path.basename(p)]
    candidates += glob.glob(os.path.join(ASSETS, "*.PNG"))
    if not candidates:
        sys.exit("No source logo .png found in assets/")
    SRC = max(candidates, key=os.path.getmtime)

OUT_CREAM = os.path.join(ASSETS, "logo-green.png")
OUT_TRANS = os.path.join(ASSETS, "logo-green-transparent.png")
print(f"Source: {os.path.basename(SRC)}")

GREEN = (47, 74, 50)      # --green-deep #2f4a32
CREAM = (247, 243, 234)   # --cream #f7f3ea
CANVAS = 640              # output square size
MARGIN_FRAC = 0.08        # padding around the emblem


def otsu_threshold(gray):
    """Compute Otsu's threshold from a 256-bin histogram (pure Python)."""
    hist = gray.histogram()[:256]
    total = sum(hist)
    sum_all = sum(i * h for i, h in enumerate(hist))
    sum_b = 0.0
    w_b = 0.0
    max_var = -1.0
    thresh = 127
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break
        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (sum_all - sum_b) / w_f
        var = w_b * w_f * (m_b - m_f) ** 2
        if var > max_var:
            max_var = var
            thresh = t
    return thresh


def main():
    im = Image.open(SRC).convert("RGBA")
    src_alpha = im.getchannel("A")
    amin, _ = src_alpha.getextrema()

    if amin < 250:
        # Source already has a transparent background (e.g. rr_no_bg.png):
        # every opaque pixel IS the design, so reuse its alpha directly. This
        # keeps the original clean anti-aliased edges.
        alpha = src_alpha
    else:
        # Opaque source (navy fabric photo): key out the navy background by
        # COLOR — it is the only region that is both dark AND blue-dominant.
        rgb = im.convert("RGB")

        def is_bg(r, g, b):
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            return lum < 108 and b >= r - 6

        mask = [0 if is_bg(r, g, b) else 255 for (r, g, b) in rgb.getdata()]
        alpha = Image.new("L", im.size)
        alpha.putdata(mask)
        alpha = alpha.filter(ImageFilter.MedianFilter(3))
        alpha = alpha.filter(ImageFilter.GaussianBlur(0.8))

    # Crop to the emblem
    bbox = alpha.getbbox()
    if bbox:
        alpha_c = alpha.crop(bbox)
    else:
        alpha_c = alpha

    w, h = alpha_c.size
    side = max(w, h)
    pad = int(side * MARGIN_FRAC)
    side_p = side + 2 * pad

    # Build green emblem on its own alpha, centered on square
    green_img = Image.new("RGBA", (side_p, side_p), (0, 0, 0, 0))
    solid_green = Image.new("RGBA", alpha_c.size, GREEN + (255,))
    ox = (side_p - w) // 2
    oy = (side_p - h) // 2
    green_img.paste(solid_green, (ox, oy), alpha_c)

    # Transparent version
    trans = green_img.resize((CANVAS, CANVAS), Image.LANCZOS)
    trans.save(OUT_TRANS)

    # Cream-background version
    cream_bg = Image.new("RGBA", (side_p, side_p), CREAM + (255,))
    cream_bg.alpha_composite(green_img)
    cream_bg.convert("RGB").resize((CANVAS, CANVAS), Image.LANCZOS).save(OUT_CREAM)

    print(f"Saved {OUT_CREAM}")
    print(f"Saved {OUT_TRANS}")


if __name__ == "__main__":
    main()
