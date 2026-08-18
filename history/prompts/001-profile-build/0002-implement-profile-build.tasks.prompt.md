---
id: 0002
title: Implement tasks for the animated GitHub profile build
stage: tasks
date: 2026-08-18
surface: opencode (CLI)
model: deepseek-v4-flash-free
feature: 001-profile-build
branch: 001-profile-build
user: Fatima
command: (tasks implementation outline pasted by user)
labels: [tasks, implementation, us1, us2, us3, us4]
links:
  spec: specs/001-profile-build/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - scripts/banner/__init__.py
  - scripts/banner/build.py
  - scripts/banner/portrait.py
  - scripts/banner/anim.py
  - scripts/banner/logos.py
  - scripts/banner/premium.py
  - scripts/banner/verify.py
  - scripts/build_banner.py
  - scripts/gen_badges.py
  - dark.svg
  - light.svg
  - divider-dark.svg
  - divider-light.svg
  - README.md
  - .github/workflows/contribution-snake.yml
  - .gitignore
  - requirements.txt
  - assets/photo/placeholder.jpg
  - specs/001-profile-build/tasks.md
tests:
  - python scripts/build_banner.py assets/photo/placeholder.jpg (exit 0)
  - verify gate: XML parse, SMIL 19.5s, centroid offset <1%/<3%, band_ratio <2.2 (dark 0.03/0.62/1.94, light 0.08/1.20/1.84 — GATE PASS)
  - determinism: rebuild hashes identical (Principle VI)
  - URL 200 scan over README (142 remote urls; 128 resolve 200; 14 expected placeholders grs-XXXX + snake pre-deploy)
  - badges: 123 shields URLs all 200; 4 slugs text-only (React Native, Godot, Cassandra, Windows)
---

## Prompt

Implement the tasks defined in `specs/001-profile-build/tasks.md` for feature
`001-profile-build` (animated GitHub profile). User pasted the "Tasks
Implementation" outline from the master prompt's build guide and asked to
continue with the build.

## Response snapshot

1. Phase 1 (Setup): created `assets/photo/`, `scripts/banner/`, `.github/workflows/`; wrote `.gitignore`, `requirements.txt` (Pillow); generated synthetic `assets/photo/placeholder.jpg` (mean luminance 60.9 — deliberately dark to exercise the light-theme paint+mask branch).
2. Phase 2 (Foundational): implemented the full `banner` package (build/portrait/anim/logos/premium/verify) + `scripts/build_banner.py` entry point. Fixed a relative-import bug in build_banner (sys.path insert) and a `dot_runs` bug that operated on the full-size photo instead of the cropped grid (`crop_to_grid` inside `dot_runs`). Set `CROP=(0.24,0.10,0.76,0.72)` for head-and-shoulders centering.
3. Phase 3 (US1): generated `dark.svg`, `light.svg`, `divider-dark.svg`, `divider-light.svg`. Verification GATE PASS (SMIL + 19.5s present, centroid offsets <1%/3%, band evenness <2.2).
4. Phase 4 (US2): validated simple-icons slugs against `unpkg simple-icons@16.28.0` (list-of-dicts format); mapped renamed slugs (bash→gnubash, css3→css, vue→vuedotjs, nuxtdotjs→nuxt, airflow→apacheairflow, rails→rubyonrails, kali→kalilinux) and text-only badges for pruned logos (java, csharp, linkedin, azure, aws, slack, heroku, oracle, canva, matplotlib, openai, powershell, vscode, visualstudiocode, reactnative, godot, cassandra, windows). Wrote `scripts/gen_badges.py` (123 badges, 8 groups, %20-encoded labels, all URLs 200). Wrote full theme-aware `README.md` (`<picture>` media queries, About/Working-On/Learning, Languages & Tools, self-hosted stats/streak/activity graph with `grs-XXXX` base, pin cards, dev quote, snake raw URLs, More About Me, Connect + visitor badge).
5. Phase 5 (US3): created `.github/workflows/contribution-snake.yml` (daily cron + workflow_dispatch, Platane/snk@v3, GITHUB_TOKEN, output branch via crazy-max/ghaction-github-pages).
6. Phase 7 (Polish): determinism check passed (identical SHA-256 on rebuild); final URL scan — 128/142 resolve 200, the 14 non-200 are expected (12 `grs-XXXX` placeholders pending US4 deploy, 2 snake raw URLs pending first workflow run). No public github-readme-stats/trophy references (Principle II).
7. Updated `tasks.md` checkboxes: T001–T023, T026–T029 complete; T024/T025 (US4 self-hosted stats) remain blocked on user credentials.
8. Deleted temp helpers `scripts/_si_lookup.py`, `scripts/_badges_out.md`.

## Outcome

- ✅ Impact: MVP (US1 banners) delivered and gate-passed; US2 theme-aware README complete with 123 verified badges; US3 snake workflow created; US4 blocked pending user's Vercel account + fine-grained read-only PAT (steps in spec US4).
- 🧪 Tests: build exit 0; verify GATE PASS; determinism PASS; badge URLs all 200; README scan 128/142 (14 expected placeholders); only 4 logos text-only.
- 📁 Files: 7 banner modules + build_banner.py + gen_badges.py + README.md + snake workflow + 4 generated SVGs + .gitignore + requirements.txt + placeholder photo + updated tasks.md.
- 🔁 Next prompts: US4 self-host stats (after user provides Vercel + PAT), swap real photo (`python scripts/build_banner.py assets/photo/<real>`) and re-run build, finalize LinkedIn/portfolio/socials URLs + real repo names for pin cards.
- 🧠 Reflection: PowerShell 5.1 mangled inline `python -c` with quotes — use temp .py files for multi-line checks; `verify.py` is a library, run the gate via inline import; gen_badges needed %20 label encoding for shields.io; keep self-hosted `grs-XXXX` base visible as a TODO so US4 completion is one search away.

## Evaluation notes (flywheel)

- Failure modes observed: Join-Path 2-arg limit and positional param binding in `create-new-feature.ps1`; shields 404 on removed simple-icons slugs; raw spaces in badge labels rejected; unencoded `python -c` under PowerShell.
- Graders run and results (PASS/FAIL): build/verify/determinism/URL-scan — all PASS; US4 not graded (blocked).
- Prompt variant (if applicable): tasks outline pasted by user (stage tasks).
- Next experiment (smallest change to try): run the snake workflow once after the profile repo is live to confirm raw URLs resolve, then complete US4.