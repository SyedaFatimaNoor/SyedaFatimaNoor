---
id: 0001
title: Amend constitution for GitHub profile
stage: constitution
date: 2026-08-18
surface: agent
model: opencode/deepseek-v4-flash-free
feature: none
branch: master
user: architext
command: amend constitution
labels: ["constitution", "governance", "github-profile"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

GitHub Profile — Master Prompt + Step-by-Step Build Guide

This file contains everything you need to recreate the exact same animated GitHub profile (photo → dithered SVG banner, dark/light themes, self-hosted stats cards, snake animation, badges, featured projects, dev quote).

Two ways to use it:

Give the MASTER PROMPT below to any AI agent (Claude, opencode, ChatGPT, etc.) together with your profile details, and let the agent build it from scratch.
Or follow the STEP-BY-STEP GUIDE yourself.
What You Will Get
Animated dark/light banner (dark.svg + light.svg) built from YOUR photo as thousands of dots
Divider SVGs matching your theme
Self-hosted GitHub stats cards (your own Vercel instance — no public limits)
Contribution streak card + activity graph
Animated contribution snake (auto-updates daily via GitHub Actions)
~130 Languages & Tools badges grouped by category
Featured Projects repo cards
Random dev quote + fun facts section
Prerequisites
Item	Why	Where
GitHub account	Hosts the profile repo	github.com
Git installed	Push/pull	https://git-scm.com
Python 3.11+	Builds the SVG banners	https://python.org
Node.js 20+	GitHub Actions workflow	https://nodejs.org
Vercel account (CLI)	Self-host the stats service	https://vercel.com
A personal photo	Becomes the banner portrait (portrait orientation best)	—
⭐ MASTER PROMPT
Copy everything between the --- markers. Replace the [...] placeholders with your details before handing it to the agent.

You are an expert GitHub profile designer. Build me a complete, production-ready GitHub profile
repository from scratch, matching the spec below. Work autonomously: scaffold files, write
scripts, generate assets, verify everything, and give me push commands at the end.

== MY PROFILE DETAILS ==
- GitHub username: SyedaFatimaNoor
- Display name: Syeda Noor Fatima
- Email (for git commits): syedanoorfatima610@gmail.com
- Title / roles: [e.g. Full-Stack Developer · Agentic AI Developer · DevOps]
- Location: Karachi, PAkistan
- Education: Bachlors in CS ongoing
- Current focus: Freelancing and Office
- Toolchain: [tools you use]
- LinkedIn: [full URL]
- Other socials: [Instagram/Facebook/X URLs]
- Portfolio site: [URL]
- Tech stack: [list everything you actually use]
- Photo: I will provide [photo.jpg]. Design the banner around it.

== BRANDING (use exactly these colors) ==
- Dark theme:  bg=#0A101F  portrait=#A78BFA  cyan=#22D3EE  green=#10B981
- Light theme: bg=#F4F6FB  portrait=#7C3AED  cyan=#0891B2  green=#10B981
- Text dark=#CBD5E1  text light=#334155  border=#1E293B
- Timeline: 19.5 seconds loop

== DELIVERABLES ==
1. Animated SVG banner pair (dark.svg + light.svg):
   - Dithered/stippled portrait of my photo inside a rounded terminal-style frame on the left,
     animated dots + SMIL <animate> (dots materialize, drift, glow, hue shift).
   - On the right: animated info panel (name, roles, contact line) and tech logos that morph
     between the portrait and the logo grid.
   - Same layout in both files, only colors differ. Use <picture> media query in README so
     GitHub auto-switches on theme.
   - Portrait must be CROPPED head-and-shoulders and CENTERED in the frame (check centroid).
2. Divider SVG pair (divider-dark.svg + divider-light.svg) matching the theme.
3. README.md (premium, dark/light aware) with these sections in order:
   - Banner + typing line
   - About Me
   - Currently Working On (+ collapsible "Now Learning")
   - Languages & Tools (~130 badges grouped: Languages / Frontend / Backend / Mobile /
     Databases / Cloud & DevOps / AI-ML / Tools & IDEs)
   - GitHub Stats + Streak + Activity Graph
   - Featured Projects (repo pin cards for [your 4-6 repos])
   - Random Dev Quote (quotes-github-readme)
   - Contribution Snake (animated)
   - More About Me
   - Connect With Me + visitor badge
4. GitHub Actions workflow (github-contribution-grid-snake) that renders the snake daily
   and pushes SVGs to the output branch.
5. Verification: run every image URL, confirm 200s; validate both SVGs parse and SMIL animates;
   check portrait centered in frame; confirm no broken badges.

== CONSTRAINTS ==
- No comments in code unless necessary. Clean, consistent style.
- Self-host the stats cards on Vercel (github-readme-stats fork) with a PAT secret; use your
  OWN instance URL in the README, never the public one.
- Do NOT use github-profile-trophy (public endpoint is broken / 402).
- If any badge logo slug 404s, fix or remove it. Shields.io returns 403 without a browser
  User-Agent — retry with one.
- Communicate progress, then finish with the exact git push commands.

Build it now, step by step, and verify each artifact before moving on.
🛠️ STEP-BY-STEP GUIDE
Phase 0 — Scaffold
# Create the repo on github.com (public), then clone locally
git clone https://github.com/YOUR_USERNAME/YOUR_USERNAME.git
cd YOUR_USERNAME
git config user.name "Your Name"
git config user.email "you@email.com"
Create folders:

YOUR_USERNAME/
├── README.md
├── dark.svg / light.svg
├── divider-dark.svg / divider-light.svg
├── assets/photo/placeholder.jpg   ← YOUR photo here
├── scripts/
│   ├── build_banner.py            ← one-command banner builder
│   └── banner/
│       ├── portrait.py            ← photo → dot runs (crop, mask, threshold)
│       ├── build.py               ← layout constants + CROP
│       ├── verify.py              ← SVGs + metrics checks
│       └── ...
└── .github/workflows/
    └── contribution-snake.yml
Phase 1 — Banner Scripts
Write the pipeline that turns photo.jpg into animated dot-art:

portrait.py — load photo, crop to head-and-shoulders, convert to dithered dot runs. Key: a subject_mask() with thr_scale so the face is detected even in dark photos; and light-mode adaptation: if the photo's mean luminance < 115, the light-theme portrait must paint (~ink) & mask (the lit subject) instead of ink, or the face disappears.
build.py — layout constants (GRID_W, frame box, PXO/PYO), the CROP tuple, band logic (for b in range(int(band.max())+1) — a cropped photo may fill fewer bands than the grid).
anim.py / logos.py / premium.py — SMIL <animate> (materialize, drift, glow, hue), logo grid.
build_banner.py — entry point: python scripts/build_banner.py assets/photo/placeholder.jpg → writes dark.svg + light.svg.
verify.py — checks: SVG parses, SMIL OK, dots centered, band evenness, organic boundaries.
Centering rule: after building, compute the dot centroid vs. the frame center and adjust CROP until centroid ≈ center.

Phase 2 — Dividers
Generate two slim gradient divider SVGs (divider-dark.svg, divider-light.svg) with your cyan→violet→green gradient. They sit between every README section.

Phase 3 — Self-Hosted Stats (Vercel)
The public github-readme-stats.vercel.app rate-limits. Host your own:

# 1. Clone the stats service
git clone https://github.com/anuraghazra/github-readme-stats.git
cd github-readme-stats
npm install

# 2. Create a Personal Access Token (fine-grained, read-only) on GitHub:
#    Settings → Developer settings → Personal access tokens
#    Permissions: metadata:read (and public repos read).

# 3. Add the token to Vercel
vercel link                    # attach to a new project, e.g. "grs"
vercel env add PAT_1 production   # paste token
vercel deploy --prod

# 4. You now have https://grs-XXXX.vercel.app — THIS is the base URL
Verify: https://grs-XXXX.vercel.app/api?username=YOUR_USERNAME returns your real stats. Important: the token must be on the SAME project your deploy went to — check the Vercel project dashboard if cards say "Something went wrong".

Phase 4 — Snake Workflow
Create .github/workflows/contribution-snake.yml:

Trigger: schedule daily + push to main.
Uses Platane/snk@v3, runs on the latest commit, github_token: ${{ secrets.GITHUB_TOKEN }}.
Outputs github-contribution-grid-snake.svg + -dark.svg to the output branch.
Then in Settings → Pages, publish the output branch (or just use the raw.githubusercontent URLs in the README — no Pages needed).

Phase 5 — README Assembly
Assemble sections from the master-prompt deliverable list. Rules:

Use <picture><source media="(prefers-color-scheme: dark|light)" srcset=...> for every themed image (banner, dividers).
Stats/streak/graph cards: bg_color=0A101F&title_color=22D3EE&icon_color=10B981&text_color=CBD5E1&border_color=1E293B (dark) — the two modes via <picture> too if you want them theme-aware.
Featured Projects use the self-hosted pin endpoint: https://grs-XXXX.vercel.app/api/pin?username=YOU&repo=REPO&...
Quote: https://quotes-github-readme.vercel.app/api?type=horizontal&theme=radical
Phase 6 — Verify Everything
Every image URL returns 200 (use curl / a script with a browser User-Agent).
SVG check: parse both files; confirm <animate>/<animateTransform> exist.
Centering: dot centroid ≈ frame center in both themes.
Visual: open preview PNGs (render SVG → screenshot via headless Chrome) and eyeball them.
Commit + push, then hard-refresh your profile (Ctrl+F5).
🎨 Quick Customization
Thing	Where to change
Photo	Replace assets/photo/placeholder.jpg, re-run build_banner.py, adjust CROP
Colors	build.py constants + README card params
Roles / typing lines	README typing-svg lines + banner text
Featured repos	README /api/pin?repo=... entries
Languages & Tools	README badge groups
Snake speed/colors	workflow + snake service options
🔧 Troubleshooting
Problem	Fix
Stats card: "Something went wrong"	PAT missing on the deployed project in Vercel
Badge shows 403 / missing logo	Retry with browser User-Agent; replace the slug
Face not visible in light theme	Photo too dark → light-mode paints ~ink & mask automatically
Portrait off-center	Shift CROP (x) until dot centroid ≈ frame center
Snake not updating	Check Actions ran; output branch has SVGs; README uses raw URLs
Trophy card broken	Known upstream issue — drop it

You MUST consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

Filled the constitution template at `.specify/memory/constitution.md` from the GitHub
profile master prompt. Established v1.0.0 (initial ratification, 2026-08-18) with six
principles (Branding Discipline, Self-Hosted Services Only, Theme-Aware Rendering,
Verified Artifacts Gate, Automated Refresh, One-Command Rebuild), two governing sections
(Constraints & Non-Goals, Development Workflow), and a Governance section covering
semver amendment policy, compliance gates, and runtime guidance. Ran the consistency
propagation check across all `.specify/templates` and `opencode.md`; no stale or
conflicting references found (plan-template "Constitution Check" remains generic and
aligned; commands/ directory does not exist in this repo — N/A). Prepended a Sync
Impact Report. Created this PHR (0001, constitution stage).

## Outcome

- ✅ Impact: Initial project constitution ratified from the template; versioned 1.0.0.
- 🧪 Tests: none required (documentation change; validated via grep for bracket tokens).
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: /sp.spec for the profile build feature (fills role/link/tech placeholders).
- 🧠 Reflection: RATIFICATION_DATE set to today (initial adoption) rather than deferred;
  unknown personal-profile fields belong to the feature spec, not the constitution.

## Evaluation notes (flywheel)

- Failure modes observed: none.
- Graders run and results (PASS/FAIL): bracket-token scan PASS; version/date coherence PASS.
- Prompt variant (if applicable): constitution-amend
- Next experiment (smallest change to try): none.
