#!/usr/bin/env python3
"""
Generates the small pill shaped badges that sit under the main profile card,
things like the LinkedIn, GitHub and project links.

Each badge gets a dark.svg and light.svg pair that are identical in shape
and size, only the theme colours and the icon differ. Icons are always
recoloured to the card's accent colour through the fill attribute, so it
does not matter what colour the source logo originally was, every badge
stays perfectly on theme.

Two icon types:
  "icon": an inline SVG path (viewBox + path data), recoloured to accent.
          Use this once you have a real logo, trace or export it as a
          single path (see the setup guide for notes on this) and drop
          the (viewBox, d) pair in below.
  "mono": a plain letter in a circle, used as a placeholder until a real
          icon is supplied.

Run:
    python generate_badges.py
Writes into assets/badge_<key>_dark.svg and assets/badge_<key>_light.svg
"""

from html import escape
from pathlib import Path

from generate_profile import THEMES  # reuse the same palette as the main card

OUT_DIR = Path(__file__).parent / "assets"

# Each of these dictionaries holds the raw SVG path data for one icon, along
# with the size of the viewBox that path was originally drawn in. The path
# itself is just traced vector artwork exported from the source logo, and
# since it gets recoloured with fill later on, the original colours here do
# not matter at all.
LINKEDIN_ICON = dict(
    view_box=(24, 24),
    d="M20.45 20.45h-3.55v-5.57c0-1.33-.02-3.03-1.85-3.03-1.86 0-2.14 1.45-2.14 2.94v5.66H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.38-1.85 3.61 0 4.28 2.38 4.28 5.47zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56z",
)

GITHUB_ICON = dict(
    view_box=(16, 16),
    d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z",
)

GPIFY_ICON = dict(
    view_box=(478.9, 309.2),
    d="M 132.519392492,1.2 c -65.3333333333,6.13333333333 -116.266666667,54.2666666667 -129.466666667,122.266666667 c -9.86666666666,51.2 4.26666666667,97.8666666666 41.2,136 c 20.4,21.0666666667 45.4666666667,35.8666666667 73.6,43.2 c 10.6666666667,2.8 14.8,3.2 37.3333333333,3.06666666667 c 23.0666666667,0 26.5333333333,-0.4 38.4,-3.6 c 55.0666666667,-14.8 96.8,-59.2 107.066666667,-113.733333333 c 1.6,-8.8 2,-17.3333333333 1.6,-33.7333333333 c -0.133333333333,-12.2666666667 -0.933333333333,-22.9333333333 -1.46666666667,-23.8666666667 c -0.8,-1.2 -15.3333333333,-1.6 -64.6666666667,-1.6 l -63.6,0 l -28.4,28.4 c -15.4666666667,15.6 -28.2666666667,28.8 -28.2666666667,29.3333333333 c 0,0.533333333333 27.8666666667,0.933333333333 62,0.933333333333 l 62,0 l -1.86666666667,4.53333333333 c -3.06666666667,7.2 -11.0666666667,19.2 -17.8666666667,26.4 c -24.1333333333,25.8666666667 -59.4666666667,35.2 -92.9333333333,24.5333333333 c -15.2,-4.8 -26.4,-11.8666666667 -38.6666666667,-24.1333333333 c -16.1333333333,-16.1333333333 -24.6666666667,-33.8666666667 -27.3333333333,-57.4666666667 c -4.4,-39.3333333333 16.2666666667,-79.0666666666 49.6,-95.0666666666 c 14.2666666667,-6.8 24,-8.66666666666 42,-7.86666666666 c 17.7333333333,0.8 31.7333333333,5.2 46.8,14.5333333333 l 10.2666666667,6.4 l 19.7333333333,-19.6 c 10.8,-10.8 19.6,-20 19.6,-20.5333333333 c 0,-2 -18,-14.4 -29.3333333333,-20.2666666667 c -21.2,-11.0666666667 -37.4666666667,-15.8666666667 -60.6666666667,-18.1333333333 c -8,-0.666666666667 -14.9333333333,-1.2 -15.3333333333,-1.2 c -0.4,0.133333333333 -5.46666666667,0.666666666666 -11.3333333333,1.2 z M 351.186059159,1.33333333333 c -22.6666666667,1.86666666667 -42.8,10.1333333333 -62.1333333333,25.3333333333 c -2.66666666667,2.13333333333 -19.0666666667,18.5333333333 -36.5333333333,36.5333333333 l -31.7333333333,32.8 l 6.4,6.53333333333 l 6.53333333333,6.66666666667 l 28.1333333333,-0.133333333333 l 28,0 l 7.33333333333,-8.66666666666 c 14.8,-17.4666666667 29.6,-30.5333333333 40.6666666667,-36 c 10.4,-5.2 10.6666666667,-5.2 25.8666666667,-5.2 c 14,0 16.2666666667,0.4 23.2,3.6 c 4.26666666667,2 11.2,7.06666666666 15.6,11.2 c 18.8,18 23.4666666667,44.5333333333 11.8666666667,67.4666666666 c -10.8,21.4666666667 -36.8,34 -60.1333333333,29.2 c -9.86666666666,-2.13333333333 -21.8666666667,-8.13333333333 -29.4666666667,-14.8 c -3.33333333333,-2.93333333333 -6.26666666667,-5.33333333333 -6.53333333333,-5.33333333333 c -0.133333333333,0 -0.533333333333,5.6 -0.666666666667,12.4 c -0.933333333333,40.6666666667 -16.2666666667,77.4666666666 -44.6666666667,106.8 l -10.4,10.5333333333 l 0,14.5333333333 l 0,14.4 l 29.3333333333,0 l 29.3333333333,0 l 0,-45.2 l 0,-45.2 l 9.06666666666,3.73333333333 c 25.3333333333,10.6666666667 57.3333333333,10.4 82.5333333333,-0.666666666666 c 24.2666666667,-10.8 47.6,-34.5333333333 57.3333333333,-58.2666666667 c 11.8666666667,-29.2 11.7333333333,-63.2 -0.4,-92 c -8.4,-19.8666666667 -26,-41.0666666667 -44.2666666667,-52.8 c -21.0666666667,-13.6 -47.3333333333,-19.7333333333 -74.2666666666,-17.4666666667 z",
)

VIGILX_ICON = dict(
    view_box=(604.4, 284.8),
    d="M 276.4,0.978907962638 c -51.6,4.13333333333 -108.933333333,22.6666666667 -156.933333333,50.8 c -32.8,19.3333333333 -75.7333333333,52.1333333333 -109.6,83.4666666666 l -9.86666666666,9.2 l 19.8666666667,17.3333333333 c 33.6,29.3333333333 55.2,45.6 85.2,63.6 c 48.9333333333,29.3333333333 93.3333333333,46.4 145.333333333,55.8666666667 c 18.9333333333,3.33333333333 59.4666666667,4.66666666667 81.3333333333,2.53333333333 c 76,-7.33333333333 154.4,-41.0666666667 223.066666667,-95.8666666666 c 12.5333333333,-10 49.6,-42.5333333333 49.6,-43.4666666667 c 0,-2 -39.3333333333,-36.6666666667 -61.3333333333,-54 c -82.5333333333,-65.2 -176,-96.5333333333 -266.666666667,-89.4666666666 z m 74,22 c 34.5333333333,5.46666666667 66.5333333333,16.2666666667 102.666666667,34.6666666667 c 28.1333333333,14.2666666667 44.2666666667,24.2666666667 68,42 c 22.1333333333,16.6666666667 52,42.1333333333 52,44.5333333333 c 0,3.73333333333 -38,33.8666666667 -65.3333333333,51.7333333333 c -54.5333333333,35.8666666667 -112.133333333,58.6666666667 -168,66.6666666666 c -17.6,2.53333333333 -60.6666666667,2.13333333333 -78.6666666666,-0.666666666667 c -70.9333333333,-10.9333333333 -140.133333333,-43.8666666667 -208.666666667,-99.0666666666 c -8.4,-6.66666666666 -16.6666666667,-13.7333333333 -18.4,-15.4666666667 l -2.93333333333,-3.33333333333 l 20.1333333333,-17.2 c 24.1333333333,-20.5333333333 35.2,-29.0666666667 53.4666666667,-41.4666666667 c 50.6666666667,-34.4 108,-56.9333333333 161.6,-63.7333333333 c 19.0666666667,-2.4 65.4666666667,-1.73333333333 84.1333333333,1.33333333333 z M 290.4,63.7789079626 c -11.6,1.73333333333 -19.7333333333,4.8 -28.4,10.5333333333 c -15.2,10.2666666667 -25.8666666667,24.5333333333 -31.3333333333,42 c -4,13.2 -4,33.8666666667 0.266666666667,45.7333333333 c 15.2,43.6 64.4,64.1333333333 105.466666667,44 c 11.0666666667,-5.33333333333 27.0666666667,-21.0666666667 33.0666666667,-32.5333333333 c 10.9333333333,-20.9333333333 11.2,-48.1333333333 0.8,-68.9333333333 c -9.73333333333,-19.2 -27.8666666667,-33.8666666667 -47.8666666667,-38.8 c -11.0666666667,-2.66666666667 -22.5333333333,-3.46666666667 -32,-2 z m 23.6,21.3333333333 c 20.2666666667,4.26666666667 36.6666666667,20.6666666667 41.8666666667,41.4666666667 c 6.8,28.1333333333 -12.4,58 -41.7333333333,64.5333333333 c -8.26666666666,1.86666666667 -11.6,2 -18.8,0.8 c -36.8,-6.13333333333 -56.9333333333,-43.7333333333 -41.3333333333,-77.2 c 3.6,-7.73333333333 17.0666666667,-21.6 24.4,-25.0666666667 c 12.2666666667,-5.73333333333 23.0666666667,-7.2 35.6,-4.53333333333 z",
)

EMAIL_ICON = dict(
    view_box=(24, 24),
    d="M2 5.5C2 4.67 2.67 4 3.5 4h17c.83 0 1.5.67 1.5 1.5v13c0 .83-.67 1.5-1.5 1.5h-17C2.67 20 2 19.33 2 18.5v-13zm2.2.5 7.8 6.2L19.8 6H4.2zM3.5 7.6v10.9h17V7.6l-8.5 6.75c-.29.23-.71.23-1 0L3.5 7.6z",
)

SKEPTIX_ICON = dict(
    view_box=(233.1, 278.7),
    d="M 61.7333333333,2 c -5.46666666667,2.4 -10,7.33333333333 -40.4,44 c -2.53333333333,3.2 -7.46666666666,8.93333333333 -10.9333333333,12.9333333333 c -10.1333333333,11.6 -10.4,12.9333333333 -10.4,46 c 0,26.4 0.266666666667,29.4666666667 2.66666666667,33.3333333333 c 3.46666666667,5.86666666667 22.2666666667,20.4 26.1333333333,20.4 c 3.2,0 3.2,-0.133333333333 3.2,-15.7333333333 c 0,-18.1333333333 0.133333333333,-18.5333333333 16.5333333333,-37.2 c 5.06666666667,-5.73333333333 15.4666666667,-17.7333333333 23.2,-26.6666666667 c 11.0666666667,-12.9333333333 14.9333333333,-16.6666666667 18.8,-17.7333333333 c 2.66666666667,-0.8 21.8666666667,-1.33333333333 43.8666666667,-1.33333333333 c 29.7333333333,0 40,-0.4 43.3333333333,-1.86666666667 c 6,-2.4 52.1333333333,-50.8 51.0666666667,-53.4666666667 c -0.4,-1.06666666667 -2.26666666667,-2.66666666667 -4.13333333333,-3.33333333333 c -2.13333333333,-0.8 -33.2,-1.33333333333 -81.0666666666,-1.33333333333 c -62.9333333333,0.133333333333 -78.4,0.4 -81.8666666666,2 z M 213.733333333,85.7333333333 c -3.06666666667,2.26666666667 -8.26666666666,6.13333333333 -11.3333333333,8.4 c -5.46666666667,3.86666666667 -23.3333333333,17.0666666667 -57.0666666667,42.1333333333 c -28.2666666667,20.9333333333 -36.4,26.4 -39.2,26.4 c -1.6,0 -13.6,-6.93333333333 -26.8,-15.3333333333 c -17.7333333333,-11.2 -25.2,-15.2 -28.2666666667,-15.3333333333 c -6.93333333333,0 -5.6,4.13333333333 6,18.2666666667 c 5.6,7.06666666666 13.3333333333,16.5333333333 16.9333333333,21.0666666667 c 10.6666666667,13.3333333333 16.9333333333,20.9333333333 22,26.8 c 2.53333333333,2.93333333333 6.26666666667,7.2 8.4,9.6 c 2,2.4 4.66666666667,4.26666666667 6,4.26666666667 c 2.53333333333,0 9.86666666666,-7.6 41.7333333333,-42.6666666667 c 21.8666666667,-24.1333333333 38.6666666667,-42.4 62.2666666667,-68 c 14.5333333333,-15.6 16.1333333333,-19.0666666667 8.93333333333,-19.6 c -2.8,-0.266666666667 -5.73333333333,0.933333333333 -9.6,4 z M 198.933333333,142.933333333 c -1.06666666667,1.06666666667 -1.6,6.53333333333 -1.6,14.5333333333 c 0,7.2 -0.533333333333,14.5333333333 -1.33333333333,16.4 c -0.666666666667,1.86666666667 -5.86666666667,8.93333333333 -11.6,15.6 c -5.73333333333,6.66666666666 -14.1333333333,16.6666666667 -18.8,22.2666666667 c -11.0666666667,13.2 -18,20.8 -21.7333333333,23.4666666667 c -2.66666666667,1.86666666667 -8.53333333333,2.13333333333 -44.4,2.13333333333 c -27.7333333333,0 -42.9333333333,0.533333333333 -46.4,1.6 c -4.26666666667,1.2 -8.66666666666,5.2 -22.5333333333,20.6666666667 l -17.3333333333,19.0666666667 l 89.2,0 l 89.2,0 l 8,-9.06666666666 c 23.2,-26 31.0666666667,-36.2666666667 32.5333333333,-42 c 0.8,-3.6 1.2,-15.8666666667 0.933333333333,-32 c -0.533333333333,-30.5333333333 0.4,-28.4 -17.2,-42.6666666667 c -13.6,-11.2 -15.0666666667,-11.8666666667 -16.9333333333,-10 z",
)

# This is the actual list of badges that get rendered. Each entry needs a
# short key used in the output filename, the visible label text, the link
# it should point to, and either an icon dictionary from above or a mono
# letter placeholder if no real icon has been traced yet.
# key, label, url, and either icon=(view_box, d) for a real path or mono="X" for a placeholder letter
BADGES = [
    dict(key="linkedin", label="LinkedIn", url="https://www.linkedin.com/in/rana-zaid26194", icon=LINKEDIN_ICON, mono=None),
    dict(key="github",   label="GitHub",   url="https://github.com/RanaZaid26194",           icon=GITHUB_ICON,   mono=None),
    dict(key="email",    label="Email",    url="mailto:ranazaide288@gmail.com",              icon=EMAIL_ICON,    mono=None),
    dict(key="skeptix",  label="Skeptix",  url="https://skeptix.netlify.app",                icon=SKEPTIX_ICON, mono=None),
    dict(key="vigilx",   label="Vigil-X",  url="https://vigil-x.netlify.app",                icon=VIGILX_ICON, mono=None),
    dict(key="gpify",    label="Gpify",    url="https://gpify.vercel.app",                   icon=GPIFY_ICON, mono=None),
]

# These constants control the shared geometry of every badge, so they all
# line up neatly no matter how long each label text is.
H = 32          # fixed badge height, same across every badge
PAD_X = 12      # left/right padding
LOGO_R = 9      # icon/monogram circle radius
GAP = 8         # gap between icon and label
CHAR_W = 7.6    # approx label char width at 13px semi bold

FONT = ("ui-monospace, SFMono-Regular, 'JetBrains Mono', "
        "'Cascadia Code', Menlo, Consolas, monospace")


def icon_markup(icon, cx, cy, r, color):
    # Takes whatever native size the icon's path was originally drawn at
    # and scales it down so it fits neatly inside the little circle behind
    # it, then centres it on that circle's midpoint.
    vb_w, vb_h = icon["view_box"]
    scale = (r * 1.15 * 2) / max(vb_w, vb_h)
    tx = cx - (vb_w * scale) / 2
    ty = cy - (vb_h * scale) / 2
    return (f'<g transform="translate({tx:.2f},{ty:.2f}) scale({scale:.4f})">'
            f'<path d="{icon["d"]}" fill="{color}"/></g>')


def render(colors, label, icon, mono):
    # The badge width is not fixed, it is worked out from how long the
    # label text is, so short labels like Email get a tighter pill and
    # longer labels like Vigil-X get a wider one automatically.
    label_w = len(label) * CHAR_W
    logo_x = PAD_X + LOGO_R
    text_x = PAD_X + LOGO_R * 2 + GAP
    width = text_x + label_w + PAD_X

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.1f}" height="{H}" '
        f'viewBox="0 0 {width:.1f} {H}" font-family="{FONT}">',

        # The rounded pill background itself, with the theme's panel colour
        # as its fill and a subtle border to separate it from the page.
        f'<rect x="0.75" y="0.75" width="{width - 1.5:.1f}" height="{H - 1.5}" rx="{H / 2:.1f}" '
        f'fill="{colors["panel"]}" stroke="{colors["border"]}" stroke-width="1.5"/>',

        # A soft, low opacity accent coloured circle sitting behind the
        # icon, giving it a little glow without overpowering the label.
        f'<circle cx="{logo_x:.1f}" cy="{H / 2}" r="{LOGO_R}" fill="{colors["accent"]}" opacity="0.15"/>',
    ]

    # icon (or letter) is always painted in the theme accent colour, never
    # the source logo's own colours, so every badge matches the card
    if icon:
        parts.append(icon_markup(icon, logo_x, H / 2, LOGO_R, colors["accent"]))
    else:
        # No traced icon yet for this badge, so fall back to a single
        # bold letter centred inside the circle as a placeholder.
        parts.append(
            f'<text x="{logo_x:.1f}" y="{H / 2 + 4.5}" text-anchor="middle" '
            f'font-size="11" font-weight="700" fill="{colors["accent"]}">{escape(mono)}</text>'
        )

    # Finally the label text itself, sitting to the right of the icon.
    parts.append(
        f'<text x="{text_x:.1f}" y="{H / 2 + 4.5}" font-size="13" font-weight="600" '
        f'fill="{colors["text"]}">{escape(label)}</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    # Runs once for every badge, and within that once for every theme, so
    # each badge ends up with both a dark and a light svg file sitting
    # side by side inside the assets folder.
    OUT_DIR.mkdir(exist_ok=True)
    for badge in BADGES:
        for theme_name, colors in THEMES.items():
            svg = render(colors, badge["label"], badge["icon"], badge["mono"])
            out = OUT_DIR / f'badge_{badge["key"]}_{theme_name}.svg'
            out.write_text(svg, encoding="utf-8")
            print(f"wrote {out.relative_to(Path(__file__).parent)}")


if __name__ == "__main__":
    main()
