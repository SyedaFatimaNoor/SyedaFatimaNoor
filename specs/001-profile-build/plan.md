# Implementation Plan: Animated GitHub Profile Build

**Branch**: `001-profile-build` | **Date**: 2026-08-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-profile-build/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a production-ready animated GitHub profile for `SyedaFatimaNoor` from a
master prompt: a Python pipeline turns a personal photo into two animated
dithered SVG banners (dark/light) plus themed dividers, a GitHub Actions
workflow regenerates the contribution snake daily, and a theme-aware README
assembles the profile with self-hosted stats cards (own Vercel instance),
~130 tech badges, featured projects, and a dev quote. Every artifact passes a
verification gate (URL 200, SVG parse, SMIL, centroid) before commit.

## Technical Context

**Language/Version**: Python 3.11+ (asset pipeline: `scripts/`), YAML (workflow), Markdown + SVG (rendered output)  
**Primary Dependencies**: Pillow (image loading/dithering; single pip dependency), Python stdlib (SVG generation, XML verification)  
**Storage**: none — static repository; generated SVGs are committed, stats served from Vercel  
**Testing**: `scripts/banner/verify.py` gate (SVG parse, SMIL presence, centroid check, band evenness); URL checks with browser User-Agent  
**Target Platform**: GitHub profile rendering (dark/light via `prefers-color-scheme`), Vercel (stats)  
**Project Type**: single — deliverables live at repository root  
**Performance Goals**: banner build < 60 s; SVG file size < 500 KB per theme; README renders with no broken images  
**Constraints**: no JS runtime in rendered profile; SMIL-only animation; 19.5 s loop; exact ratified palette; no comments in code unless necessary  
**Scale/Scope**: 1 repo, ~130 badges, 2 animated banners, 2 dividers, 1 workflow, 1 README

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate |
|-----------|------|
| I. Branding Discipline | Every color literal in generated SVGs must be from the ratified dark/light palette |
| II. Self-Hosted Services Only | README must contain zero references to public stats or trophy endpoints |
| III. Theme-Aware Rendering | Every themed image uses `<picture>`; animation is SMIL with a 19.5 s loop |
| IV. Verified Artifacts Gate | `verify.py` passes: XML parse, SMIL present, centroid ≈ center, all URLs 200 |
| V. Automated Refresh | `contribution-snake.yml` exists with a daily cron and output-branch push |
| VI. One-Command Rebuild | `python scripts/build_banner.py assets/photo/<photo>` regenerates both banners deterministically |

**Compliance**: all gates satisfiable within scope; no violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-profile-build/
├── plan.md              # This file
├── spec.md              # Feature specification
└── tasks.md             # Task breakdown (/sp.tasks output)
```

### Source Code (repository root)

```text
README.md                    # Theme-aware profile page (final deliverable)
dark.svg                     # Animated banner, dark theme (generated)
light.svg                    # Animated banner, light theme (generated)
divider-dark.svg             # Section divider, dark theme (generated)
divider-light.svg            # Section divider, light theme (generated)
assets/
├── photo/placeholder.jpg    # Source portrait (user-provided; placeholder until then)
└── logos/                   # (optional) local tech logos if a badge slug 404s
scripts/
├── build_banner.py          # Entry point: photo → dark.svg + light.svg + dividers
└── banner/
    ├── portrait.py          # photo → crop → mask → dither → dot runs
    ├── build.py             # layout constants, GRID_W, frame box, PXO/PYO, CROP, palette
    ├── anim.py              # SMIL <animate>/<animateTransform> generators
    ├── logos.py             # logo grid (tech logos morphing in/out)
    ├── premium.py           # premium frame/info-panel decorations
    └── verify.py            # SVG parse, SMIL, centroid, band-evenness, URL checks
.github/
└── workflows/
    └── contribution-snake.yml  # daily snake render + output-branch push
```

**Structure Decision**: Single project at repository root because the
deliverable *is* the repository itself. Build tooling lives under `scripts/`,
generated assets at the root (needed for relative GitHub rendering), and CI
under `.github/workflows/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations — the six constitution gates are met by the planned design
without complexity trade-offs.
