# Feature Specification: Animated GitHub Profile Build

**Feature Branch**: `001-profile-build`
**Created**: 2026-08-18
**Status**: Draft
**Input**: User description: "Build animated GitHub profile from master prompt"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Scriptable Asset Pipeline (Priority: P1)

As a maintainer, I can run one command to regenerate the animated dark/light
banner SVGs and themed dividers from my photo, so the repository is
self-contained and rebuildable without external services.

**Why this priority**: Every other deliverable (README, cards, snake) depends
on generated assets. It is fully scriptable and verifiable without accounts
or credentials, making it the MVP slice.

**Independent Test**: `python scripts/build_banner.py assets/photo/placeholder.jpg`
exits 0 and writes `dark.svg`, `light.svg`, `divider-dark.svg`,
`divider-light.svg` that parse as XML and contain SMIL animation.

**Acceptance Scenarios**:

1. **Given** a source photo in `assets/photo/`, **When** `build_banner.py` runs,
   **Then** both theme SVGs are written with identical layout and the exact
   ratified palette.
2. **Given** the generated SVGs, **When** parsed, **Then** they are valid XML
   containing `<animate>`/`<animateTransform>` with a 19.5 s loop.
3. **Given** the portrait in the banner, **When** the dot centroid is computed,
   **Then** it is within tolerance of the frame center in both themes.
4. **Given** a photo with mean luminance < 115, **When** the light theme is
   built, **Then** the portrait paints (~ink) and masks the lit subject so the
   face stays visible.

---

### User Story 2 - Self-Contained Profile Page (Priority: P1)

As a visitor of the GitHub profile, I see a premium, theme-aware README with
the banner, stats cards, badges, featured projects, and a dev quote, so the
profile presents a complete professional identity.

**Why this priority**: This is the visible deliverable that makes the profile
useful; it can be assembled and verified purely from repository content plus
hosted image URLs.

**Independent Test**: The README renders every image URL with HTTP 200 (browser
User-Agent), all sections appear in the ratified order, and themed images use
`<picture>` media queries.

**Acceptance Scenarios**:

1. **Given** the assembled README, **When** every remote URL is requested,
   **Then** each returns HTTP 200 with no broken badge slugs.
2. **Given** the README on GitHub, **When** the viewer toggles theme,
   **Then** themed assets switch via `prefers-color-scheme`.
3. **Given** the stats section, **When** cards are requested, **Then** they
   come from the project's own Vercel instance, never the public endpoint.

---

### User Story 3 - Daily Contribution Snake (Priority: P2)

As a visitor, I see an up-to-date animated contribution grid so the profile
reflects activity without manual updates.

**Why this priority**: Adds live value but depends on GitHub Actions and the
output branch; secondary to the static profile content.

**Independent Test**: The workflow `contribution-snake.yml` schedules daily,
and the README references the snake SVGs via raw.githubusercontent URLs.

**Acceptance Scenarios**:

1. **Given** the workflow on the default branch, **When** the schedule fires,
   **Then** `github-contribution-grid-snake.svg` and `-dark.svg` are pushed to
   the output branch.
2. **Given** the output branch exists, **When** the README is viewed,
   **Then** both snake variants render from raw URLs.

---

### User Story 4 - Self-Hosted Stats Service (Priority: P3)

As a maintainer, I deploy my own github-readme-stats instance with a PAT so
cards are reliable and never rate-limited.

**Why this priority**: Requires a Vercel account, PAT, and manual deploy —
blocked on user credentials and external services.

**Independent Test**: `https://grs-<project>.vercel.app/api?username=SyedaFatimaNoor`
returns real stats.

**Acceptance Scenarios**:

1. **Given** a deployed Vercel project with the `PAT_1` secret, **When** the
   API is called, **Then** real stats return for the profile user.
2. **Given** a missing or mis-placed token, **When** cards are requested,
   **Then** the README troubleshooting entry explains the fix.

---

### Edge Cases

- Very dark photo: face must remain visible in the light theme
  (luminance < 115 → paint ~ink & mask).
- Portrait off-center: `CROP` must be shifted until the dot centroid ≈ frame
  center in both themes.
- Shields.io returns 403 without a browser User-Agent: retry with one;
  a 404 logo slug must be fixed or the badge removed.
- A cropped photo may fill fewer bands than the grid: band logic must derive
  from `int(band.max())+1`.
- Public stats endpoint rate-limits: never referenced in the README.
- Snake not updating: workflow must have run and the output branch must
  contain the SVGs; README must use raw URLs.
- Missing source photo: `build_banner.py` must exit non-zero with a clear
  message.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `python scripts/build_banner.py assets/photo/<photo>` MUST
  generate `dark.svg` and `light.svg` in one run.
- **FR-002**: Both SVGs MUST use identical layout; only the ratified theme
  colors differ (dark: bg #0A101F, portrait #A78BFA, cyan #22D3EE, green
  #10B981, text #CBD5E1, border #1E293B; light: bg #F4F6FB, portrait #7C3AED,
  cyan #0891B2, green #10B981, text #334155, border #1E293B).
- **FR-003**: Both SVGs MUST contain SMIL `<animate>`/`<animateTransform>` with
  a 19.5 s looping timeline (materialize, drift, glow, hue shift).
- **FR-004**: The portrait MUST be cropped head-and-shoulders and centered;
  the dot centroid MUST approximate the frame center in both themes.
- **FR-005**: If the photo's mean luminance < 115, the light-theme portrait
  MUST paint (~ink) and mask the lit subject.
- **FR-006**: `divider-dark.svg` and `divider-light.svg` MUST be generated with
  the cyan→violet→green gradient.
- **FR-007**: Every themed image in the README MUST use `<picture>` with
  `(prefers-color-scheme: dark|light)` srcset.
- **FR-008**: Stats/streak/graph/pin cards MUST reference the project's own
  Vercel instance; the public `github-readme-stats` endpoint MUST NOT be used.
- **FR-009**: The `github-profile-trophy` badge MUST NOT be used (broken / 402).
- **FR-010**: `.github/workflows/contribution-snake.yml` MUST schedule daily,
  use `Platane/snk@v3` with `secrets.GITHUB_TOKEN`, and push snake SVGs to the
  output branch.
- **FR-011**: The README MUST contain the ratified sections in order: banner +
  typing, About Me, Currently Working On (+ Now Learning), Languages & Tools
  (~130 badges in 8 groups), Stats + Streak + Activity Graph, Featured
  Projects, Dev Quote, Contribution Snake, More About Me, Connect + visitor
  badge.
- **FR-012**: Verification MUST run URL 200 checks (browser User-Agent for
  shields.io), SVG parse, SMIL presence, and centroid checks before commit.
- **FR-013**: Secrets MUST NOT be committed; the PAT lives only in Vercel
  environment variables or a gitignored `.env`.
- **FR-014**: Any badge slug that 404s MUST be fixed or removed.
- **FR-015**: Code MUST contain no comments unless necessary for correctness.

### Key Entities *(include if feature involves data)*

None — this feature is a static content repository. Profile identity data
(username `SyedaFatimaNoor`, display name, email, roles, links, tech stack)
is configuration in the README, banner text, and build script constants.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `build_banner.py` exits 0 and writes all four SVGs.
- **SC-002**: Both banner SVGs parse as XML and contain SMIL elements.
- **SC-003**: Dot centroid is within 2% of frame center in both themes.
- **SC-004**: Every README image URL returns HTTP 200 with a browser
  User-Agent.
- **SC-005**: The snake workflow exists with a daily schedule and pushes both
  snake variants to the output branch.
- **SC-006**: Self-hosted stats API returns real stats for
  `SyedaFatimaNoor`.
- **SC-007**: README themed images switch with viewer theme via `<picture>`.
- **SC-008**: No `github-profile-trophy` reference and no public stats URL in
  the README.
