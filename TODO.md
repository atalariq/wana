# Wana — porting roadmap (palette → apps)

The Wana palette (Light / Dark) currently lives only as web tokens in
`tokens/base.css`. Goal: **one source-of-truth palette → many app themes**,
following the base16/base24 (tinted-theming) standard wherever an app supports
it, hand-written templates where it doesn't.

Source colors today: `tools/proposals.json` (`D-light` / `D-dark`) and
`tokens/base.css` — 10 semantic roles. Verify every generated color with
`python3 tools/color.py contrast <fg> <bg>`.

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
      common plugins. Author directly or via a base16/base24 nvim builder. Ship as
      its own repo (`wana.nvim`). Namespace confirmed free.
- [ ] **kitty** — `wana-dark.conf` / `wana-light.conf`: `foreground`,
      `background`, `cursor`, `selection_*`, `color0`–`color15`. Generate straight
      from the base24 ANSI set.
- [ ] **Noctalia v5** — `~/.config/noctalia/palettes/Wana.json` (JSON). Needs **16
      Material Design 3 roles** (`mPrimary`/`mOnPrimary`, `mSecondary`,
      `mTertiary`, `mError`, `mSurface`, `mSurfaceVariant`, `mOutline`, `mShadow`,
      `mHover`/`mOnHover` …) **+ a `terminal` block** (bg/fg/cursor/selection +
      normal & bright ANSI), `dark` required / `light` optional. Map Wana roles →
      M3 roles. Ref: <https://docs.noctalia.dev/v5/theming/palette/>
- [ ] **Herdr** — `~/.config/herdr/config.toml`, `[theme.custom]`: `panel_bg`,
      `accent`, `green`, `blue`, `red`, `yellow` (subset — quick win). Ref:
      <https://herdr.dev/docs/configuration/#theme>

## Phase 2 — Dev tools / CLIs I use

- [ ] **Alacritty** — `colors.primary` / `colors.normal` / `colors.bright` TOML;
      generate from the base24 ANSI set (same data as kitty).
- [ ] **OpenCode** — custom theme (JSON theme file). Verify the exact schema &
      path before generating.
- [ ] **Claude Code** — verify theming mechanism (terminal-ANSI driven vs a
      settings theme) before deciding what to ship.
- [ ] **Codex** — CLI, terminal-color driven; likely covered by the kitty/
      alacritty ANSI palette. Confirm.
- [ ] **Hermes** — apply Wana to its site/styles (it can `@import` `tokens/
base.css` or consume the generated CSS).
- [ ] **Others** (`dsb.`) — bat, delta, fzf, btop, starship, zsh/prompt: mostly
      free via tinted-theming base16/base24 templates once Phase 0 lands.

---

## Notes

- **Leverage:** Phase 0's base24 scheme is the unlock — most Phase 2 apps fall
  out of `tinty` for near-zero extra effort. Do Phase 0 before hand-rolling
  anything per-app.
- **Distribution:** publish the design system to npm under a scope
  (`@atalariq/wana`) — the bare `wana` package name is taken. Colorscheme repos
  (`wana.nvim`, etc.) and tinted-theming submission are unaffected.
- **Loose end:** `proposals/proposal-D.md` is still titled "Forest" (the working
  codename). Reconcile to Wana later if desired — it's historical, not load-bearing.
