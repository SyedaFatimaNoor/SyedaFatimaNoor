"""Verification gate: XML parse, SMIL presence, centroid, band evenness, URL checks."""

import urllib.request
import xml.etree.ElementTree as ET

from .build import CANVAS, DOT, FRAME_CENTER, PYO

NS = {"svg": "http://www.w3.org/2000/svg"}
UA = {"User-Agent": "Mozilla/5.0 (compatible; profile-verify/1.0)"}


def parse(path):
    return ET.parse(path)


def check_smil(root):
    anim = root.findall(".//svg:animate", NS)
    tr = root.findall(".//svg:animateTransform", NS)
    durs = [e.get("dur") or "" for e in anim + tr]
    return bool(anim) and bool(tr) and any("19.5" in d for d in durs)


def centroid(root):
    total = 0.0
    cx = cy = 0.0
    for line in root.findall(".//svg:line", NS):
        x1 = float(line.get("x1"))
        x2 = float(line.get("x2"))
        y = float(line.get("y1"))
        w = abs(x2 - x1)
        total += w
        cx += ((x1 + x2) / 2) * w
        cy += y * w
    if not total:
        return (None, None)
    return (cx / total, cy / total)


def offset_percent(root):
    cx, cy = centroid(root)
    if cx is None:
        return (100.0, 100.0)
    fcx, fcy = FRAME_CENTER
    dx = abs(cx - fcx) / CANVAS[0] * 100
    dy = abs(cy - fcy) / CANVAS[1] * 100
    return (dx, dy)


def band_evenness(root):
    counts = {}
    for line in root.findall(".//svg:line", NS):
        y = float(line.get("y1"))
        b = int(round((y - PYO) / DOT))
        counts[b] = counts.get(b, 0) + 1
    vals = list(counts.values())
    if not vals:
        return 0.0
    avg = sum(vals) / len(vals)
    return max(vals) / avg


def url_status(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except Exception as exc:
        return str(exc)
