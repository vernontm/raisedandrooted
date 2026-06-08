#!/usr/bin/env python3
"""
Composite the real Raised & Rooted logo onto the kie.ai-generated cover
background, then export the finished cover as PNG + PDF.
"""
from PIL import Image
import os

A = os.path.join(os.path.dirname(__file__), "..", "assets")
BG = os.path.join(A, "cover-bg.jpg")
LOGO = os.path.join(A, "rr_no_bg.png")           # full-color logo pops on deep green
OUT_PNG = os.path.join(A, "guide-cover-ebook.png")
OUT_PDF = os.path.join(A, "raised-and-rooted-free-guide.pdf")

cover = Image.open(BG).convert("RGBA")
W, H = cover.size

logo = Image.open(LOGO).convert("RGBA")
target_w = int(W * 0.33)
target_h = round(logo.height * target_w / logo.width)
logo = logo.resize((target_w, target_h), Image.LANCZOS)

x = (W - target_w) // 2
y = int(H * 0.055)
cover.alpha_composite(logo, (x, y))

final = cover.convert("RGB")
final.save(OUT_PNG)
final.save(OUT_PDF, "PDF", resolution=150.0)

print(f"Cover size: {W}x{H}")
print(f"Logo placed at ({x},{y}) size {target_w}x{target_h}")
print(f"Saved {OUT_PNG}")
print(f"Saved {OUT_PDF}")
