# Wana — Palette → App Themes Design

**Date:** 2026-06-21
**Status:** Approved, pending implementation plan
**Scope:** Phase 0–2 of `TODO.md` (palette → many app themes), plus the
`design-system → wana` rebrand. All work lands in **this repo**.

---

## Context

The Wana palette (Light / Dark) currently exists only as web tokens in
`tokens/base.css` (10 semantic roles) and as `D-light` / `D-dark` in
`tools/proposals.json`. The goal is **one source-of-truth palette → many app
themes**: terminals, Neovim, Noctalia, Herdr, and a long tail of CLI tools.

The repo is Python-first (`tools/color.py` does OKLCH↔sRGB + WCAG math). It has
no JS build step and no external theming toolchain. The design keeps it that
way: generation is a small in-repo Python program, not external `tinty`.

This spec covers the architecture and the decisions that shape it. Exact hex
values for newly-invented colors (magenta, cyan, brights) are produced during
implementation and reviewed on the playground before they are final.

---

## Decisions (locked during brainstorming)

1. **Generation path:** an **in-repo Python generator** (`tools/gen.py` +
   `tools/templates/`) reads the canonical palette and emits every app's config
   into `themes/`. Zero external dependencies, fully reproducible, one command.
   _(Not external `tinty`.)_
2. **Rename scope:** full rebrand — move the working directory
   `~/Repos/design-system → ~/Repos/wana` (git history preserved) **and** update
   every proper-name reference. Generic descriptive phrases ("a personal design
   system") stay as descriptions.
3. **ANSI-16 derivation:** the **8 normal** ANSI colors anchor on the parent
   schemes (Flexoki for Light, Gruvbox for Dark) — proven and recognizable; the
   **8 bright** colors are generated algorithmically via a single OKLCH
   lightness-shift rule, contrast-verified. No per-color guessing for brights.

---

## Architecture

### Source of truth & data flow

A new **base24 YAML scheme** per flavor becomes the canonical palette for theme
generation:

```
schemes/wana-light.yaml    # system: base24, variant: light
schemes/wana-dark.yaml     # system: base24, variant: dark
```

base24 (tinted-theming standard) is chosen because it carries the ANSI brights
terminals need and maps cleanly to 16 terminal colors.

`tokens/base.css` (the 10 ratified web roles) **stays hand-authored** — it is
**not** regenerated from the YAML. Instead a **drift guard** asserts that the
colors shared between `base.css`, `proposals.json` (`D-*`), and the YAML schemes
agree. So:

- **YAML schemes** = source of truth for _app theme generation_.
- **`tokens/base.css`** = source of truth for _the web layer_ (unchanged).
- **Drift guard test** = keeps the shared subset honest in both directions.

```
schemes/*.yaml ──► tools/gen.py ──► themes/**          (app themes)
       ▲
       └── drift guard ◄── tokens/base.css, proposals.json (D-*)
```

### base24 slot mapping

The 24 base24 slots are filled from the existing 10 roles plus derived/new
colors:

| Slot           | Meaning                                           | Source                                              |
| -------------- | ------------------------------------------------- | --------------------------------------------------- |
| base00–02      | bg / surface / overlay (selection)                | existing roles                                      |
| base03         | muted (comments)                                  | existing                                            |
| base04         | dark foreground                                   | derived (between muted & text)                      |
| base05         | text (default fg)                                 | existing                                            |
| base06–07      | light / lightest fg                               | derived (OKLCH L-shift)                             |
| base08 red     | red                                               | = `error` (existing)                                |
| base09 orange  | orange                                            | = `warning` (existing)                              |
| base0A yellow  | yellow                                            | **new** — parent (Flexoki/Gruvbox yellow)           |
| base0B green   | green                                             | = `accent` (signature forest, hue 150)              |
| base0C cyan    | cyan                                              | **new** — parent                                    |
| base0D blue    | blue                                              | = `info` (existing)                                 |
| base0E magenta | magenta/purple                                    | **new** — parent                                    |
| base0F brown   | brown                                             | **new** — parent or derived                         |
| base10–11      | darker / darkest bg                               | derived (OKLCH L-shift of bg)                       |
| base12–17      | brights (red, yellow, green, cyan, blue, magenta) | **OKLCH L-shift of the normals**, contrast-verified |

ANSI-16 falls out via the standard base24→terminal mapping:

```
0  black   = base01      8  br-black   = base03
1  red     = base08      9  br-red     = base12
2  green   = base0B     10  br-green   = base14
3  yellow  = base0A     11  br-yellow  = base13
4  blue    = base0D     12  br-blue    = base16
5  magenta = base0E     13  br-magenta = base17
6  cyan    = base0C     14  br-cyan    = base15
7  white   = base05     15  br-white   = base07
```

### Bright-color rule

Each bright is its normal counterpart shifted in OKLCH lightness by a fixed
delta (direction depends on flavor: brighten on dark, deepen/saturate on light),
then gamut-clamped and contrast-checked against the flavor bg. One rule, applied
uniformly — implemented via `tools/color.py` (`fit` / `oklch` already exist; add
a helper if needed). The exact delta is tuned once on the playground.

### Generator

```
tools/gen.py              # reads schemes/*.yaml → writes themes/**
tools/templates/          # one template per target (plain str.format, no jinja)
themes/                   # generated outputs, committed, never hand-edited
  kitty/  alacritty/  nvim/  noctalia/  herdr/  opencode/  …
```

- Pure-stdlib Python where possible. YAML loaded via `pyyaml` if already
  available, else a tiny vendored loader — confirmed during implementation.
- `python3 tools/gen.py` regenerates everything.
- `python3 tools/gen.py --check` regenerates to a temp location and diffs
  against committed `themes/`; nonzero exit on drift (for the test suite).
- Every generated file carries a `GENERATED — do not edit` header pointing back
  to `schemes/` and `gen.py`.

---

## Targets

All targets from `TODO.md`, generated into `themes/` in this repo.

### Phase 0 — pipeline + palette (the unlock)

- Extend the palette to a full ANSI-16 set (normal 8 anchored on parents, bright
  8 via the OKLCH rule), both flavors, contrast-verified.
- Author `schemes/wana-light.yaml` + `schemes/wana-dark.yaml` (base24).
- Build `tools/gen.py` + the **kitty** template to prove the pipeline
  end-to-end (YAML → ANSI-16 → working config).
- Add the drift-guard test.

### Phase 1 — core targets

- **wana.nvim** — Lua colorscheme, light + dark, treesitter + LSP + common
  plugins. Generated into `themes/nvim/`. _Note:_ TODO envisions a standalone
  `wana.nvim` repo; per "di repo ini saja" it is generated here. Splitting it
  out is a later, separate step, out of scope for this spec.
- **kitty** — `wana-dark.conf` / `wana-light.conf` (done as the Phase 0 proof).
- **Noctalia v5** — `Wana.json`: 16 Material Design 3 roles + a `terminal`
  block (bg/fg/cursor/selection + normal & bright ANSI). Map Wana roles → M3
  roles. `dark` required, `light` optional.
- **Herdr** — `config.toml` `[theme.custom]` subset (`panel_bg`, `accent`,
  `green`, `blue`, `red`, `yellow`). Quick win.

### Phase 2 — dev tools / CLIs

- **Alacritty** — `primary` / `normal` / `bright` TOML (same ANSI data as kitty).
- **OpenCode** — JSON theme file (verify schema/path during impl).
- **Claude Code** — verify theming mechanism (terminal-ANSI vs settings theme)
  before deciding what to ship.
- **Codex** — terminal-color driven; confirm it's covered by kitty/alacritty.
- **bat, delta, fzf, btop, starship** — one template each, base16/base24-shaped,
  generated locally (no external `tinty`).
- **Hermes** — apply Wana to its site (consumes `tokens/base.css` or generated
  CSS). Cross-repo; flagged but lower priority.

---

## Rename (design-system → wana)

Lands **first**, as its own commit, so everything else builds on the new name.

- Move working dir `~/Repos/design-system → ~/Repos/wana` (preserve git history).
- Rename the branch to `dev` (done).
- Update proper-name occurrences only:
  - `README.md` title (`# design-system` → `# Wana`)
  - `site/index.html` `<title>` / `<h1>`
  - `site/accent-explorer.html` `<title>`
  - `site/app.js` `exportFilename`
  - `AGENTS.md`, `tools/color.py` docstring
- Leave generic descriptive phrases ("a personal design system") intact.
- Remote: the user will push to a new repo `atalariq/wana` once complete.

---

## Verification

- **Contrast:** every generated fg/bg color pair checked with
  `python3 tools/color.py contrast <fg> <bg>` — WCAG AA minimum, AAA where the
  parent allowed.
- **Drift guard:** new test (extending `tools/check_tokens.py` /
  `tools/test_color.py`) asserts shared colors agree across `base.css`,
  `proposals.json` (`D-*`), and `schemes/*.yaml`.
- **Generation freshness:** `tools/gen.py --check` confirms committed `themes/`
  match the YAML — stale outputs fail.
- **Per-target sanity:** where a target has a known schema (Noctalia M3 roles,
  OpenCode JSON), validate against it before committing.

---

## Out of scope

- Splitting `wana.nvim` (or any theme) into its own standalone repo.
- Publishing to npm (`@atalariq/wana`) or submitting to tinted-theming.
- Regenerating `tokens/base.css` from the YAML (it stays hand-authored).
- Restyling Hermes beyond pointing it at the tokens (cross-repo).
- Reconciling the historical "Forest" codename in `proposals/proposal-D.md`.

---

## Open implementation questions (resolved during impl, not blocking)

- Exact OKLCH lightness delta for brights (tuned on the playground).
- Whether `pyyaml` is available or a vendored loader is needed.
- Noctalia Wana-role → M3-role mapping table (needs the M3 role list verified
  against the v5 docs).
- OpenCode / Claude Code / Codex exact theming mechanism and file paths.
