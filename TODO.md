# Wana — porting roadmap (palette → apps)

The Wana palette (Light / Dark) lives as canonical **base24 schemes** in
`schemes/wana-{light,dark}.yaml`. Goal: **one source-of-truth palette → many app
themes**, following the base16/base24 (tinted-theming) standard wherever an app
supports it, hand-written templates where it doesn't.

Generation: `python3 tools/gen.py` renders every committed file under `themes/`
from `schemes/`; `python3 tools/gen.py --check` (and the `tools/` test suite)
guards freshness/drift. Add a target by writing `tools/templates/<x>` + a
`render_<x>()` in `tools/gen.py`. Verify colors with
`python3 tools/color.py contrast <fg> <bg>`.

---

## Current status & resume point (updated 2026-06-26)

**Shipped — 13 generated targets** in `themes/` (all from `schemes/`, 52 tests green):
alacritty, bat, btop, fzf, herdr, kitty, lazygit, opencode, pywal, starship,
tmux, tty, **yazi**.

**Standalone repos** (generated here, published one-way via `tools/publish.sh`
with `git subtree`; palette stays canonical in `schemes/` → no drift):

- ✅ **wana.yazi** — LIVE at private `atalariq/wana.yazi`. Install:
  `ya pkg add atalariq/wana.yazi:wana-dark`.
- ⏸️ **wana.nvim** — plan written & ready, execution paused at Task 1.

**▶️ Resume here (wana.nvim):** execute
`docs/superpowers/plans/2026-06-26-wana-nvim-colorscheme.md` (subagent-driven).
Architecture: palette `lua/wana/palette.lua` is GENERATED from `schemes/`
(`render_nvim_palette`); highlight groups are HAND-AUTHORED in
`lua/wana/highlights.lua`. Prerequisites: Neovim installed (Task 4 headless load
gate) + green light to create private `atalariq/wana.nvim`. The publish script
`tools/publish.sh nvim` already exists. Companion: the shipped yazi plan
`docs/superpowers/plans/2026-06-26-wana-yazi-flavor.md` is the proven template
for the subtree/publish flow.

---

## Phase 0 — Prerequisites (do these first)

- [x] **Extend the palette to a full ANSI-16 set.** Wana currently has no
      dedicated **magenta** or **cyan**, and no **bright** variants — terminals
      (kitty/alacritty), Neovim, and Noctalia all need the full 16. Define
      `normal` + `bright` for black/red/green/yellow/blue/magenta/cyan/white in
      both flavors, fit for legibility, verify contrast.
- [x] **Adopt a canonical palette file.** Author a **base24** scheme
      (`wana-light.yaml` / `wana-dark.yaml`, tinted-theming/schemes style) as the
      single source of truth — base24 carries the ANSI brights terminals need.
      Everything below generates from it. (Alt: extend `tools/proposals.json`.)
- [x] **Pick the generation path.** Use **tinted-theming (`tinty`)** templates
      for supported apps (kitty, alacritty, bat, fzf, btop, starship, delta… come
      almost for free once the base24 scheme exists); hand-write the rest.
      _(Chosen: in-repo Python generator `tools/gen.py`; tinty not adopted.)_

## Phase 1 — Core targets

- [ ] **wana.nvim** — Neovim colorscheme (Lua), light + dark, treesitter + LSP +
      common plugins. Ship as its own repo (`wana.nvim`). _Plan written & ready:_
      `docs/superpowers/plans/2026-06-26-wana-nvim-colorscheme.md` (palette
      generated, highlights hand-authored). **Paused at Task 1 — resume here.**
- [x] **kitty** — `wana-dark.conf` / `wana-light.conf`: `foreground`,
      `background`, `cursor`, `selection_*`, `color0`–`color15`. Generated from
      the base24 ANSI set. (`themes/kitty/`)
- [ ] **Noctalia v5** — `~/.config/noctalia/palettes/Wana.json` (JSON). Needs **16
      Material Design 3 roles** (`mPrimary`/`mOnPrimary`, `mSecondary`,
      `mTertiary`, `mError`, `mSurface`, `mSurfaceVariant`, `mOutline`, `mShadow`,
      `mHover`/`mOnHover` …) **+ a `terminal` block** (bg/fg/cursor/selection +
      normal & bright ANSI), `dark` required / `light` optional. Map Wana roles →
      M3 roles. Ref: <https://docs.noctalia.dev/v5/theming/palette/>
- [x] **Herdr** — `[theme.custom]`: `panel_bg`, `accent`, `green`, `blue`, `red`,
      `yellow`. Generated. (`themes/herdr/wana.toml`) Ref:
      <https://herdr.dev/docs/configuration/#theme>

## Phase 2 — Dev tools / CLIs I use

- [x] **Alacritty** — `colors.primary` / `colors.normal` / `colors.bright` TOML;
      generated from the base24 ANSI set. (`themes/alacritty/`)
- [x] **OpenCode** — custom JSON theme. Generated. (`themes/opencode/wana.json`)
- [ ] **Claude Code** — verify theming mechanism (terminal-ANSI driven vs a
      settings theme) before deciding what to ship.
- [ ] **Codex** — CLI, terminal-color driven; likely covered by the kitty/
      alacritty ANSI palette. Confirm.
- [ ] **Hermes** — apply Wana to its site/styles (it can `@import` `tokens/
base.css` or consume the generated CSS).
- [x] **Shipped via base24 templates** — bat, fzf, btop, starship, tmux, tty,
      pywal, lazygit. (`themes/<app>/`)
- [ ] **Still free / quick wins** — delta, zsh/prompt: add a template +
      `render_<x>()` when wanted.

---

## Notes

- **Leverage:** Phase 0's base24 scheme is the unlock — most ANSI-driven apps
  are near-zero effort: add a `tools/templates/<x>` + `render_<x>()` and they
  generate from `schemes/`. Reach for hand-authoring only where an app needs
  opinionated, non-palette-dump design (e.g. the nvim highlight groups).
- **Distribution:** publish the design system to npm under a scope
  (`@atalariq/wana`) — the bare `wana` package name is taken. Colorscheme repos
  (`wana.nvim`, etc.) and tinted-theming submission are unaffected.
- **Loose end:** `proposals/proposal-D.md` is still titled "Forest" (the working
  codename). Reconcile to Wana later if desired — it's historical, not load-bearing.
