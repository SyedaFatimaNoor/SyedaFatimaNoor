"""Premium decorations: terminal frame, info panel, section divider."""

from .build import CANVAS, FRAME, TIMELINE


def terminal_frame(theme):
    x0, y0, x1, y1 = FRAME
    rx = 18
    return (
        f'<rect x="{x0:g}" y="{y0:g}" width="{x1 - x0:g}" height="{y1 - y0:g}" '
        f'rx="{rx:g}" fill="{theme["panel"]}" stroke="{theme["border"]}" '
        f'stroke-width="2"/>'
        f'<circle cx="{x0 + 24:g}" cy="{y0 + 24:g}" r="6" fill="#EF4444"/>'
        f'<circle cx="{x0 + 46:g}" cy="{y0 + 24:g}" r="6" fill="#F59E0B"/>'
        f'<circle cx="{x0 + 68:g}" cy="{y0 + 24:g}" r="6" fill="{theme["green"]}"/>'
        f'<circle cx="{x0 + 180:g}" cy="{y0 + 30:g}" r="1.5" fill="{theme["cyan"]}">'
        f'<animate attributeName="r" values="1.5;3;1.5" dur="4s" repeatCount="indefinite"/>'
        f'</circle>'
    )


def info_panel(theme, name, roles, contact):
    cx = CANVAS[0] / 2 + 260
    return (
        f'<g>'
        f'<text x="{cx:g}" y="150" text-anchor="middle" font-family="monospace" '
        f'font-size="44" font-weight="700" fill="{theme["portrait"]}">{name}'
        f'<animate attributeName="fill" values="{theme["portrait"]};{theme["cyan"]};'
        f'{theme["green"]};{theme["portrait"]}" dur="{TIMELINE}s" '
        f'repeatCount="indefinite"/></text>'
        f'<text x="{cx:g}" y="200" text-anchor="middle" font-family="monospace" '
        f'font-size="20" fill="{theme["text"]}">{roles}<tspan fill="{theme["cyan"]}">|</tspan>'
        f'<animate attributeName="opacity" values="1;0.4;1" dur="2s" '
        f'repeatCount="indefinite"/></text>'
        f'<text x="{cx:g}" y="248" text-anchor="middle" font-family="monospace" '
        f'font-size="16" fill="{theme["cyan"]}">{contact}</text>'
        f'</g>'
    )


def divider(theme):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="24" '
        f'viewBox="0 0 1000 24">'
        f'<defs><linearGradient id="g" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{theme["cyan"]}"/>'
        f'<stop offset="0.5" stop-color="{theme["portrait"]}"/>'
        f'<stop offset="1" stop-color="{theme["green"]}"/>'
        f'</linearGradient></defs>'
        f'<rect x="0" y="8" width="1000" height="8" rx="4" fill="url(#g)">'
        f'<animate attributeName="opacity" values="0.4;1;0.4" dur="6s" '
        f'repeatCount="indefinite"/></rect>'
        f'</svg>'
    )
