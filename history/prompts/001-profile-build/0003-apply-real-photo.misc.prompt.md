---
id: 0003
title: Apply real profile photo to the banner pipeline
stage: misc
date: 2026-08-18
surface: opencode (CLI)
model: deepseek-v4-flash-free
feature: 001-profile-build
branch: 001-profile-build
user: Fatima
command: (image upload + "mainay ya image update kr di hy is ko lagao")
labels: [misc, assets, portrait, auto-center, us1]
links:
  spec: specs/001-profile-build/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - assets/photo/placeholder.jpg
  - scripts/banner/portrait.py
  - scripts/banner/build.py
  - dark.svg
  - light.svg
  - divider-dark.svg
  - divider-light.svg
tests:
  - python scripts/build_banner.py assets/photo/placeholder.jpg (exit 0)
  - verify gate: SMIL 19.5s, offset x<1%, y<3%, band_ratio<2.2
  - determinism: identical SHA-256 on rebuild
---

## Prompt

User replaced `assets/photo/placeholder.jpg` with their real photo (1023×1537,
portrait, mean luminance 87.8) and asked to apply it ("mainay ya image update
kr di hy is ko lagao"). Model cannot ingest image pixels directly, so work was
done from the file.

## Response snapshot

1. Confirmed the file was swapped (dimensions/size changed) and noted the image
   itself is not viewable by the model — processed it as a file.
2. Rebuilt banners: verification gate FAILED — horizontal centroid offset 7.66%
   (fixed CROP assumed a centered subject; the real photo's face sits right of
   the crop window).
3. Measured the skin-mask centroid: grid col 71.1 vs center 48.0 → tried a
   hand-tuned CROP shift; gate improved to 3.1% but still failed, proving a
   static CROP is not robust across photos.
4. Added `auto_center_crop()` in `scripts/banner/portrait.py` (6-iteration
   fixpoint: fit crop → skin-mask centroid → shift window horizontally until
   centroid within ±1 grid col; clamps at photo edges; no-op if mask empty).
   `dot_runs` now crops via `crop_to_grid(img, auto_center_crop(img))`;
   `crop_to_grid` takes an optional crop tuple.
5. Reverted `CROP` to its original base `(0.24, 0.10, 0.76, 0.72)` — position is
   now auto-derived, so the constant stays photo-agnostic (Principle VI: one
   command rebuild with any photo).
6. Result: GATE PASS both themes (2447 lines each, offset 0.44%/0.16%, band
   ratio 1.48); determinism confirmed (identical SHA-256 on rebuild).

## Outcome

- ✅ Impact: real photo applied; pipeline now auto-centers any portrait so the
  crop constant never needs retuning per photo.
- 🧪 Tests: build exit 0; GATE PASS; determinism PASS.
- 📁 Files: `portrait.py` (+auto_center_crop, crop param), `build.py` (CROP
  restored), 4 regenerated SVGs.
- 🔁 Next prompts: commit + push regenerated assets; US4 self-hosted stats once
  user provides Vercel + PAT.
- 🧠 Reflection: fixed-CROP constants are a fragile assumption for user-supplied
  photos — centering on the subject mask is the robust design and keeps the
  verified-artifacts gate meaningful.

## Evaluation notes (flywheel)

- Failure modes observed: static CROP → 7.66% horizontal offset; single-step
  linear shift undershot (3.1%) because re-masking shifts the blob; iteration
  fixes it.
- Graders run and results (PASS/FAIL): build/verify/determinism — PASS.
- Prompt variant (if applicable): asset swap (misc stage).
- Next experiment (smallest change to try): none — gate converged; consider
  auto vertical centering only if a future photo crops oddly.