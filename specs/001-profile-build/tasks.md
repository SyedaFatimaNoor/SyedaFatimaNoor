---

description: "Task list for the animated GitHub profile build"
---

# Tasks: Animated GitHub Profile Build

**Input**: Design documents from `/specs/001-profile-build/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths below assume single project per plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure: `assets/photo/`, `scripts/banner/`, `.github/workflows/`
- [x] T002 Create `requirements.txt` (Pillow) and `.gitignore` (Python + universal + `.env*`)
- [x] T003 Create `assets/photo/placeholder.jpg` placeholder portrait and document the swap in README

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core banner pipeline that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Banner Build Modules (User Story 1)

- [x] T004 [P] [US1] Implement `scripts/banner/build.py` (layout constants: GRID_W, frame box, PXO/PYO, CROP tuple, dark/light palette, band logic `range(int(band.max())+1)`)
- [x] T005 [P] [US1] Implement `scripts/banner/portrait.py` (load, crop head-and-shoulders, subject_mask with thr_scale, luminance<115 → light paints ~ink & masks, dither to dot runs)
- [x] T006 [P] [US1] Implement `scripts/banner/anim.py` (SMIL `<animate>`/`<animateTransform>`: materialize, drift, glow, hue shift; 19.5 s loop)
- [x] T007 [P] [US1] Implement `scripts/banner/logos.py` (tech logo grid morphing with the portrait)
- [x] T008 [P] [US1] Implement `scripts/banner/premium.py` (rounded terminal-style frame, animated info panel decorations)
- [x] T009 [P] [US1] Implement `scripts/banner/verify.py` (SVG XML parse, SMIL presence, dot centroid vs frame center, band evenness, URL 200 checks with browser UA)
- [x] T010 [US1] Implement `scripts/build_banner.py` entry point (one command → dark.svg + light.svg + divider-dark.svg + divider-light.svg)

**Checkpoint**: `python scripts/build_banner.py assets/photo/placeholder.jpg` exits 0; `verify.py` passes on both themes; centroid ≈ frame center.

---

## Phase 3: User Story 1 - Scriptable Asset Pipeline (Priority: P1) 🎯 MVP

**Goal**: Regenerable animated banner pair + themed dividers

**Independent Test**: build_banner.py regenerates identical SVGs that parse and animate

### Tests for User Story 1

- [x] T011 [P] [US1] Verify `dark.svg`/`light.svg` parse as XML and contain `<animate>`/`<animateTransform>` via `scripts/banner/verify.py`
- [x] T012 [P] [US1] Verify divider SVGs exist and contain the cyan→violet→green gradient

### Implementation for User Story 1

- [x] T013 [US1] Generate `dark.svg` + `light.svg` from the placeholder photo (identical layout, ratified palette, 19.5 s loop)
- [x] T014 [US1] Generate `divider-dark.svg` + `divider-light.svg` with the ratified gradient

**Checkpoint**: MVP delivered — repository contains regenerable animated banners.

---

## Phase 4: User Story 2 - Self-Contained Profile Page (Priority: P1)

**Goal**: Theme-aware README with all sections, badges, cards

**Independent Test**: Every README image URL returns HTTP 200; sections in ratified order

### Tests for User Story 2

- [x] T015 [P] [US2] Run URL 200 scan over all README image URLs (browser User-Agent for shields.io)

### Implementation for User Story 2

- [x] T016 [P] [US2] Create `README.md` banner + typing line using `<picture>` media queries (dark/light srcset)
- [x] T017 [P] [US2] Add About Me, Currently Working On (+ Now Learning collapsible), More About Me sections
- [x] T018 [US2] Add ~130 Languages & Tools badges in 8 groups (Languages/Frontend/Backend/Mobile/Databases/Cloud & DevOps/AI-ML/Tools & IDEs); fix or remove any 404 slug
- [x] T019 [P] [US2] Add GitHub Stats + Streak + Activity Graph cards (self-hosted URL base `https://grs-XXXX.vercel.app`, dark params bg=0A101F&title_color=22D3EE&icon_color=10B981&text_color=CBD5E1&border_color=1E293B)
- [x] T020 [P] [US2] Add Featured Projects pin cards (`/api/pin`) + Random Dev Quote (quotes-github-readme, theme=radical) + visitor badge
- [x] T021 [P] [US2] Add Connect With Me links section (uses ratified profile details)

**Checkpoint**: README complete and theme-aware; no broken images.

---

## Phase 5: User Story 3 - Daily Contribution Snake (Priority: P2)

**Goal**: Auto-updating contribution snake via GitHub Actions

**Independent Test**: Workflow has a daily cron; README uses raw snake URLs

- [x] T022 [US3] Create `.github/workflows/contribution-snake.yml` (schedule daily + push to main; Platane/snk@v3; github_token: secrets.GITHUB_TOKEN; outputs `github-contribution-grid-snake.svg` + `-dark.svg` to output branch)
- [x] T023 [US3] Reference both snake SVGs in README via raw.githubusercontent URLs

**Checkpoint**: Workflow file valid; snake URLs resolve after first run.

---

## Phase 6: User Story 4 - Self-Hosted Stats Service (Priority: P3)

**Goal**: Own Vercel instance of github-readme-stats with PAT

**Independent Test**: `/api?username=SyedaFatimaNoor` returns real stats

> **⚠️ BLOCKED on user action**: requires Vercel account, CLI, and a
> fine-grained read-only PAT. Deploy steps are documented in spec US4.

- [ ] T024 [P] [US4] Clone and configure `github-readme-stats`; add `PAT_1` secret in Vercel; deploy
- [ ] T025 [US4] Replace `grs-XXXX` placeholders in README with the real instance URL; verify `/api` returns real stats

**Checkpoint**: Cards render real stats from the project's own instance.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Verification, hardening, and delivery

- [x] T026 [P] Re-run `scripts/banner/verify.py` on both themes (XML, SMIL, centroid, band evenness)
- [x] T027 [P] Run final URL 200 scan over every README image; confirm no public stats/trophy references (Principle II)
- [x] T028 Confirm `build_banner.py` regenerates identical SVGs (deterministic, Principle VI)
- [x] T029 Provide exact `git push` instructions to the user

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup; BLOCKS US1–US4
- **US1 assets (Phase 3)**: Depends on Phase 2 pipeline
- **US2 README (Phase 4)**: Depends on Phase 3 generated assets; may reference grs-XXXX placeholder until US4
- **US3 snake (Phase 5)**: Independent of Phases 3–4
- **US4 Vercel (Phase 6)**: BLOCKED on user credentials
- **Polish (Phase 7)**: Depends on all in-scope stories

### Parallel Opportunities

- All [P] tasks in Phase 2 run in parallel (different files)
- Phases 4 and 5 can proceed in parallel once Phase 3 completes
- Phase 6 is independent but credential-blocked

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational pipeline
3. Complete Phase 3: Generate + verify banner assets
4. **STOP and VALIDATE**: banner SVGs parse, animate, and are centered

### Incremental Delivery

1. Setup + Foundational → pipeline ready
2. US1 → generated animated banners (MVP!)
3. US2 → full theme-aware README
4. US3 → live contribution snake
5. US4 → self-hosted stats (after user provides Vercel/PAT)

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify assets before committing (Principle IV gate)
- Commit after each task or logical group
- Do NOT create the snake output branch manually; the workflow handles it
