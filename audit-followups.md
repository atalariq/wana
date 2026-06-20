# Audit & Follow-up Proposals

_Pragmatic senior-engineer pass over the design-system repo (tokens, playground, tools, docs). Every claim traced to file:line. Audit only — nothing implemented._

## Map (what's here)

- **`tokens/base.css`** — the single ratified token file: Proposal D "Forest" colors (OKLCH-canonical, hex comments), type scale, spacing, radius, shadow/ring, motion. Light default + dark via both `@media (prefers-color-scheme)` and `[data-theme]`.
- **`site/`** — vanilla HTML/CSS/JS playground that dogfoods the tokens. `index.html` links `base.css`; `app.js` is a self-contained OKLCH↔hex↔HSL + WCAG engine driving a live token editor, contrast checker, and CSS/DTCG/Figma export-import. `accent-explorer.html` is a standalone hue-picking tool.
- **`tools/`** — `color.py` (the canonical color math + CLI), `proposal_matrix.py` (contrast tables from `proposals.json`), `proposals.json` (A–D palette data).
- **`research/`, `proposals/`** — design rationale (color theory, accessibility, A–D proposals). `AGENTS.md` is the agent-facing guide. No README, no tests.

Overall: clean, well-commented, correctly-scoped for a personal system. The math checks out — I verified every contrast claim in `base.css` with `tools/color.py` and they're all accurate. The problems are **drift between the ratified `base.css` and the playground/exports**, not broken fundamentals.

---

## Ranked follow-ups

### 1. Playground renders Proposal C, not the ratified Forest theme — and "D" has no tab

- **type:** bug · **priority:** P1 · **effort:** S
- **what & why:** `app.js:325` defaults `state.proposal = "C"`, and `init()` calls `applyTokens()` which overwrites every `--color` var inline — so the page that loads `base.css` (Forest D) immediately repaints as Proposal C. Worse, `renderProposalTabs` loops only `["A","B","C"]` (`app.js:367`), so the **D · Forest tab doesn't exist**. This directly contradicts `AGENTS.md:33` ("imports base.css as its source of truth") and `TODO.md:53` ("pick the D · Forest tab"). The dogfood currently showcases the wrong theme.
- **prompt:**
  > In `site/app.js`, make the playground default to and expose the ratified Forest theme. Change `state.proposal` from `"C"` to `"D"` (~line 325). In `renderProposalTabs` (~line 367), change both the main-tab and mini-tab loops from `["A", "B", "C"]` to `["A", "B", "C", "D"]` so all four proposals are selectable. Open `site/index.html` and confirm the page loads in Forest (matching `tokens/base.css`), the D tab is present and active, and switching A→B→C→D re-skins the whole UI. Don't touch the color math.

### 2. CSS/JSON/Figma export emits the wrong radius and drops half the tokens

- **type:** bug · **priority:** P1 · **effort:** S
- **what & why:** All three exporters hardcode `--radius: 0.5rem` (`app.js:652`, `:696`, `:723`), but the ratified token is `0.25rem` (`base.css:50`). The CSS export also omits `--shadow`, `--ring`, `--duration-fast/base`, and `--easing` entirely, and emits only a `[data-theme="dark"]` block (no `@media (prefers-color-scheme: dark)`), so anyone who "Export as CSS" to consume the system gets an incomplete, subtly-wrong token file. The stale `0.5rem` traces back to `site-spec.md:106` (predates Forest).
- **prompt:**
  > In `site/app.js`, fix the exporters to match `tokens/base.css`. (1) Change every hardcoded `--radius`/`radius` value from `0.5rem` to `0.25rem` in `exportCss` (~line 652), `exportJson` (~line 696), and `exportFigma` (~line 723). (2) In `exportCss`, add the missing `--shadow`, `--ring`, `--duration-fast`, `--duration-base`, and `--easing` declarations, copied verbatim from `tokens/base.css`. Verify the CSS export output is a valid superset of the static tokens in `base.css`. Leave the color tokens (which come from live state) alone.

### 3. README for consuming the design system _(your proposal #1 — keep, sharpened)_

- **type:** docs · **priority:** P1 · **effort:** M
- **verdict:** **Keep.** Real gap — `AGENTS.md` is agent-facing process notes, not a consumer guide, and there's no README at all. Sharpened scope so it's not a vague "write docs."
- **what & why:** The three target sites (Journey, Portfolio, Research per `AGENTS.md:5`) have no documented way to pull in tokens. A README should cover: (a) one-line consumption — `@import` / `<link>` `tokens/base.css`; (b) the token reference table (roles, type scale, spacing, radius, motion) — can lift from `AGENTS.md:21`; (c) theming: light default, `data-theme="dark"`/`"light"` to pin, auto OS-dark via `@media`; (d) the OKLCH-canonical authoring model + how to regenerate/verify with `tools/color.py`; (e) a one-line note that OKLCH needs a modern browser (no fallback shipped — state it honestly); (f) what the `site/` playground is for. Keep it short; link out to `research/` rather than restating it.
- **prompt:**
  > Write `README.md` at the repo root for **consumers** of this design system (the author's own sites: Journey, Portfolio, Research). Read `AGENTS.md`, `tokens/base.css`, and skim `proposals/proposal-D.md` first. Sections: (1) What this is + the Forest theme in one paragraph; (2) Quick start — how to `@import` or `<link>` `tokens/base.css` and start using `var(--token)`; (3) Token reference — adapt the table from `AGENTS.md`, listing color roles, `--step-*`, `--space-*`, `--radius`, shadow/ring, motion; (4) Theming — light is default, set `data-theme="dark"`/`"light"` to pin a mode, OS dark is honored automatically; (5) Authoring colors — OKLCH is canonical, verify contrast with `python3 tools/color.py contrast <fg> <bg>`; (6) Browser support — uses `oklch()` and `color-mix()`, modern browsers only, no fallback shipped; (7) The `site/` playground, one line. Match the terse, technical tone of the existing docs. Don't restate `research/` — link to it.

### 4. No tests for the color math, which exists in two hand-synced copies

- **type:** test · **priority:** P2 · **effort:** M
- **what & why:** `app.js:1` says the math is "ported verbatim from `tools/color.py`," and the spec demands real WCAG/OKLCH correctness. Two independent implementations of correctness-critical math with zero tests guarantees silent drift. Highest-leverage test: a handful of known-answer cases for `color.py` (contrast of a known pair, hex→OKLCH→hex round-trip stability, a `fit` result hitting its target) — cheap, catches real regressions. Testing the JS copy is secondary; a pragmatic option is a tiny script asserting `color.py` and `app.js` agree on a few conversions.
- **prompt:**
  > Add a minimal test file `tools/test_color.py` (stdlib `unittest`, no new deps) for `tools/color.py`. Cover: (1) `contrast("#100f0f", "#fffcf0")` ≈ 18.6 and `contrast("#2d6e3f", "#fffcf0")` ≈ 5.99 (the values asserted in `base.css` comments); (2) hex→OKLCH→hex round-trips back to the same hex (within rounding) for several Forest tokens; (3) `fit_lightness` returns a color whose contrast is within ~0.1 of the requested target. Run `python3 tools/test_color.py` and paste the passing output. Do not refactor `color.py`.

### 5. Dark palette is duplicated across two blocks in base.css

- **type:** improvement · **priority:** P2 · **effort:** S
- **what & why:** The 10 dark color values are written twice — once in `@media (prefers-color-scheme: dark)` (`base.css:64-77`) and once in `[data-theme="dark"]` (`base.css:82-93`) — with a comment admitting "both blocks must stay identical." That's a real edit-one-forget-the-other hazard. It's a genuine pure-CSS specificity constraint, so there's no free DRY fix; the cheap mitigation is the test/guard, not a rewrite.
- **prompt:**
  > Add a guard against the two dark-palette blocks in `tokens/base.css` drifting. Lowest-effort option: a tiny `tools/check_tokens.py` that parses `base.css`, extracts the custom-property declarations inside the `@media (prefers-color-scheme: dark)` block and the `[data-theme="dark"]` block, and exits non-zero if they differ — printing the mismatched roles. Run it against the current file (should pass) and paste the output. Do not restructure the CSS itself.

### 6. Name the design system _(your proposal #2 — keep, lower priority)_

- **type:** naming · **priority:** P2 · **effort:** S
- **verdict:** **Keep**, but it's polish, not a blocker — sequence it after the functional fixes. Options below; pick one, then it can become a token namespace / package name / the playground `<title>`.
- **options** (all evoke the warm-green Forest identity; the references are _Lily Chou-Chou_'s hazy green, Wong Kar-Wai warmth, Everforest):
  - **Grove** _(recommended)_ — short, forest-green-native, and ties to Journey being a "digital garden." Clean as a package name and an unobtrusive token prefix if you ever namespace (`--grove-accent`). Low collision risk in your personal scope.
  - **Understory** — the forest layer beneath the canopy; bookish, fits a research/writing-leaning author. Longer.
  - **Everwarm** — direct riff on Everforest + the "warm everywhere" thesis of Proposal D. A bit on-the-nose.
  - **Canopy** — green, structural ("a canopy over all my sites"); more common as a product name elsewhere.
- **prompt:**
  > Decide the design system's name (recommendation: **Grove**). Once chosen, apply it consistently: the `<title>` and `<h1>` in `site/index.html` (currently "atalariq design system"), the header comment in `tokens/base.css`, the export-file basename in `site/app.js` (`exportFilename`, currently `atalariq-tokens-…`), and `AGENTS.md`/`README.md`. Do not introduce a token prefix unless explicitly requested — keep `--accent` etc. unprefixed. Show a diff of every rename.

### 7. Delete or refresh the stale scratch docs

- **type:** chore · **priority:** P2 · **effort:** S
- **what & why:** `TODO.md` and `site-spec.md` are untracked (`git status`) and now actively misleading. `TODO.md:7` says "commit this session's work first (uncommitted)" and `:50` says base.css is "NOT yet ratified (still Proposal C)" — but git history shows it ratified (`7c2e0e2`) and everything committed; its `__pycache__` warning (`:33`) is also resolved (already in `.gitignore`). `site-spec.md` predates Forest (radius `0.5rem`, tabs A/B/C only). Keeping stale handoff notes around invites acting on them.
- **prompt:**
  > Review `TODO.md` and `site-spec.md` (both untracked). Confirm against git history that the work they describe is done (token ratification in commit `7c2e0e2`, `__pycache__` already gitignored). Then either delete both, or — if worth keeping — replace `TODO.md` with a fresh short status and update `site-spec.md`'s radius to `0.25rem` and proposal list to include D. Ask me which before deleting. Show what you changed.

---

## Explicitly skipped (not worth it)

- **Dedupe the proposal color data** (`PROPOSALS` in `app.js:30` vs `tools/proposals.json`). The inline copy is a deliberate choice so the playground works from `file://` without `fetch`/CORS (`app.js:15`). A build step to generate one from the other is overengineering for a 4-palette personal tool. Leave it; if anything, just a comment cross-link.
- **A token build pipeline (Style Dictionary / transformers).** `AGENTS.md:15` explicitly chooses "no build-time token transformers (for now)." The CSS-custom-properties approach is the right altitude here; don't add tooling the project deliberately declined.
- **Framework / componentization of the playground.** It's a single-purpose vanilla demo and fine as-is; the real component library is tracked as future work elsewhere (`TODO.md:82`).
