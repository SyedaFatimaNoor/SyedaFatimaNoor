#!/usr/bin/env python3
"""One-command banner builder: photo -> dark.svg + light.svg + dividers."""

import os
import sys

from banner import portrait, verify
from banner.anim import drift, materialize
from banner.build import CANVAS, DOT, FRAME, FRAME_H, FRAME_W, PXO, PYO, THEMES, TIMELINE
from banner.logos import logo_grid
from banner.premium import divider, info_panel, terminal_frame

NAME = "Syeda Noor Fatima"
ROLES = "Full-Stack Dev · Agentic AI · DevOps"
CONTACT = "syedanoorfatima610@gmail.com"


def _glow(theme):
    fx = FRAME[0] + FRAME_W / 2
    fy = FRAME[1] + FRAME_H / 2
    return (
        f'<radialGradient id="glow" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0" stop-color="{theme["portrait"]}" stop-opacity="0.25"/>'
        f'<stop offset="1" stop-color="{theme["bg"]}" stop-opacity="0"/>'
        f'</radialGradient>'
        f'<circle cx="{fx:g}" cy="{fy:g}" r="{FRAME_W * 0.62:g}" fill="url(#glow)">'
        f'<animate attributeName="opacity" values="0.6;1;0.6" dur="{TIMELINE}s" '
        f'repeatCount="indefinite"/></circle>'
    )


def banner_svg(theme_key, photo):
    theme = THEMES[theme_key]
    runs = portrait.dot_runs(photo, dark=(theme_key == "dark"))
    total = len(runs) or 1
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS[0]:g}" '
        f'height="{CANVAS[1]:g}" viewBox="0 0 {CANVAS[0]:g} {CANVAS[1]:g}" '
        f'font-family="monospace">',
        f'<defs>{_glow(theme)}</defs>',
        f'<rect width="{CANVAS[0]:g}" height="{CANVAS[1]:g}" fill="{theme["bg"]}"/>',
        terminal_frame(theme),
    ]
    for i, (band_y, row) in enumerate(runs):
        segs = []
        for x1, x2 in row:
            xa = PXO + x1 * DOT
            xb = PXO + (x2 + 1) * DOT
            y = PYO + band_y * DOT + DOT / 2
            segs.append(f'<line x1="{xa:.2f}" y1="{y:.2f}" x2="{xb:.2f}" y2="{y:.2f}"/>')
        parts.append(
            f'<g stroke="{theme["portrait"]}" stroke-width="{DOT}" stroke-linecap="round">'
            + "".join(segs)
            + materialize(i, total)
            + drift(i, total)
            + "</g>"
        )
    parts.append(info_panel(theme, NAME, ROLES, CONTACT))
    parts.append(logo_grid(theme, 620, 320))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/build_banner.py <photo>")
        return 1
    photo_path = sys.argv[1]
    if not os.path.exists(photo_path):
        print(f"error: photo not found: {photo_path}")
        return 1
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    photo = portrait.load_rgb(photo_path)
    for key in ("dark", "light"):
        out = os.path.join(root, f"{key}.svg")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(banner_svg(key, photo))
        print(f"wrote {out}")
    for key in ("dark", "light"):
        out = os.path.join(root, f"divider-{key}.svg")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(divider(THEMES[key]))
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main())
