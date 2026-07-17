#!/usr/bin/env python3
"""
Turns a photo of yourself into the ascii portrait shown on the left side of
the profile card.

Run this only when you want to change the photo. It is never run by the
GitHub Actions workflows, so it is kept in this setup folder on its own and
the daily automation stays free of these extra dependencies.

    pip install pillow numpy rembg onnxruntime
    python setup/photo_to_ascii.py your_photo.jpg

It writes portrait.txt into the root of the repository, which is the file
generate_profile.py reads every time it builds the card.

Tuning knobs:
  COLS      characters across (more means more detail, but widens the card)
  BUST      how far down the body to keep, as a fraction of the subject height
  DETAIL    local contrast gain, raise it if the shirt looks like a solid blob
  WEIGHT    how much of the overall light and dark shape to keep, 0 is pure edges
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps
from rembg import remove

# The photo to convert is passed in as a command line argument, and falls
# back to photo.jpg in the current folder if nothing is given.
SRC = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
COLS = 96
ASPECT = 1.72        # svg line-height / char-width
BUST = 0.62
DETAIL = 2.3
WEIGHT = 0.45
RAMP = "@%#*+=-:. "  # darkest -> lightest


def main():
    # Step one is to remove the background entirely, so only the actual
    # person is left with a transparent alpha channel around them.
    cut = remove(Image.open(SRC))                       # cut the subject out of the background
    rgba = np.asarray(cut)
    alpha = rgba[:, :, 3]

    # Now we find the actual bounding box of the visible subject and crop
    # down to head and torso only, using BUST to decide how far down the
    # body to keep, then add a small pixel of padding around the edges.
    ys, xs = np.nonzero(alpha > 60)
    x0, x1 = xs.min(), xs.max()
    y0 = ys.min()
    y1 = int(y0 + (ys.max() - y0) * BUST)               # head + torso only
    pad = 8
    box = (max(0, x0 - pad), max(0, y0 - pad),
           min(rgba.shape[1], x1 + pad), min(rgba.shape[0], y1))

    cut = cut.crop(box)
    a = np.asarray(cut)[:, :, 3].astype(float) / 255.0
    g = np.asarray(ImageOps.autocontrast(cut.convert("L"), cutoff=1), dtype=np.int16)
    h, w = g.shape

    # This next part pulls local contrast out of the image, which is what
    # lets folds and edges in something like a plain dark shirt still show
    # up as ascii detail instead of turning into one flat blob of characters.
    blur = np.asarray(Image.fromarray(g.astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(max(2, w // 55))), dtype=np.int16)
    ink = np.clip(150 + (g - blur) * DETAIL + (g - 128) * WEIGHT, 0, 255)

    # We only care about the brightness range that actually appears inside
    # the subject, not the background, so the contrast stretch below is
    # measured only over the pixels where the alpha mask says something is
    # actually there.
    inside = a > 0.5
    lo, hi = np.percentile(ink[inside], 2), np.percentile(ink[inside], 98)
    ink = np.clip((ink - lo) * 255.0 / max(1, hi - lo), 0, 255)

    # Finally we shrink the whole image down to a small grid of characters,
    # one character per resulting pixel, and pick a symbol from RAMP for
    # each one based on how dark or light that spot ended up being. Any
    # pixel that falls outside the alpha mask is simply left blank.
    rows = max(1, int(COLS * (h / w) / ASPECT))
    small = np.asarray(Image.fromarray(ink.astype(np.uint8))
                       .resize((COLS, rows), Image.LANCZOS), dtype=float)
    mask = np.asarray(Image.fromarray((a * 255).astype(np.uint8))
                      .resize((COLS, rows), Image.LANCZOS), dtype=float)

    n = len(RAMP) - 1
    lines = []
    for y in range(rows):
        line = "".join(
            RAMP[round(small[y, x] / 255 * n)] if mask[y, x] > 110 else " "
            for x in range(COLS)
        )
        lines.append(line.rstrip())

    # portrait.txt always lives in the repository root, one level up from
    # this setup folder, since that is where generate_profile.py expects
    # to find it.
    out_path = Path(__file__).parent.parent / "portrait.txt"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nwrote {out_path.name}  ({COLS} cols x {rows} rows)")


if __name__ == "__main__":
    main()
