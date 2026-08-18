"""SMIL animation generators for the 19.5 s banner timeline."""

from .build import TIMELINE


def _begin(index, total):
    return round(index * TIMELINE / total, 3) if total else 0.0


def materialize(index, total):
    begin = _begin(index, total)
    dur = round(max(0.6, 1.8 - begin), 3)
    return (
        f'<animate attributeName="opacity" values="0;1" '
        f'begin="{begin}s" dur="{dur}s" fill="freeze"/>'
    )


def drift(index, total):
    begin = _begin(index, total)
    amp = -1.5 - (index % 3)
    loop = round(begin + TIMELINE, 3)
    return (
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 0; 0 {amp}; 0 0" begin="{begin}s; {loop}s" '
        f'dur="{TIMELINE}s" repeatCount="indefinite"/>'
    )
