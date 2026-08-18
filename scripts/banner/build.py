"""Layout constants, ratified palette, and crop for the animated banner pair."""

CANVAS = (1000.0, 560.0)

GRID_W = 96
GRID_H = 100
DOT = 4.0
PAD = 6.0

FRAME = (44.0, 60.0, 444.0, 500.0)
FRAME_W = FRAME[2] - FRAME[0]
FRAME_H = FRAME[3] - FRAME[1]
PXO = FRAME[0] + PAD + (FRAME_W - 2 * PAD - GRID_W * DOT) / 2
PYO = FRAME[1] + PAD + (FRAME_H - 2 * PAD - GRID_H * DOT) / 2
FRAME_CENTER = (FRAME[0] + FRAME_W / 2, FRAME[1] + FRAME_H / 2)

CROP = (0.24, 0.10, 0.76, 0.72)

DARK = {
    "bg": "#0A101F",
    "portrait": "#A78BFA",
    "cyan": "#22D3EE",
    "green": "#10B981",
    "text": "#CBD5E1",
    "border": "#1E293B",
    "panel": "#111A2E",
}

LIGHT = {
    "bg": "#F4F6FB",
    "portrait": "#7C3AED",
    "cyan": "#0891B2",
    "green": "#10B981",
    "text": "#334155",
    "border": "#1E293B",
    "panel": "#FFFFFF",
}

THEMES = {"dark": DARK, "light": LIGHT}
TIMELINE = 19.5
LUM_THRESHOLD = 115.0
