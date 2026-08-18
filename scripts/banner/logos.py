"""Tech logo grid: monogram tiles that materialize beneath the info panel."""

from .build import TIMELINE

LOGO_SET = [
    ("PY", "#3776AB"), ("JS", "#F7DF1E"), ("TS", "#3178C6"), ("RD", "#FF2D20"),
    ("RE", "#61DAFB"), ("NX", "#000000"), ("TW", "#06B6D4"), ("GI", "#F05032"),
    ("GH", "#181717"), ("AW", "#FF9900"), ("PG", "#4169E1"), ("GO", "#00ADD8"),
    ("RU", "#DEA584"), ("DK", "#2496ED"), ("PG", "#336791"), ("NM", "#000000"),
]


def logo_grid(theme, origin_x, origin_y, tiles=12, cols=6, size=34, gap=14):
    lines = []
    for i in range(tiles):
        col = i % cols
        row = i // cols
        cx = origin_x + col * (size + gap) + size / 2
        cy = origin_y + row * (size + gap) + size / 2
        label, color = LOGO_SET[i % len(LOGO_SET)]
        begin = round(i * 1.6, 3)
        loop = round(begin + TIMELINE, 3)
        half = size / 2
        lines.append(
            f'<g transform="translate({cx:g} {cy:g})" opacity="0">'
            f'<rect x="-{half:g}" y="-{half:g}" width="{size:g}" height="{size:g}" '
            f'rx="8" fill="{theme["panel"]}" stroke="{color}" stroke-width="1.5"/>'
            f'<text y="5" text-anchor="middle" font-family="monospace" '
            f'font-size="{size * 0.42:g}" fill="{color}">{label}</text>'
            f'<animate attributeName="opacity" values="0;0.85" begin="{begin}s" '
            f'dur="0.8s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'additive="sum" values="0 0; 0 -4; 0 0" begin="{begin}s; {loop}s" '
            f'dur="{TIMELINE}s" repeatCount="indefinite"/>'
            f'</g>'
        )
    return "\n".join(lines)
