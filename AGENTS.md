# Wana — Agent Guide

Wana — a personal design system for atalariq. Used across:

- **Journey** (digital garden, Astro) — `journey.atalariq.dev`
- **Portfolio** (atalariq.github.io)
- **Research site** (research.atalariq.dev)
- **Future projects**

## Goals

1. **Consistency** — one token system, many sites
2. **Accessibility** — WCAG AA minimum, AAA where possible
3. **Personality** — warm, readable, not generic Bootstrap-feel
4. **Simplicity** — CSS custom properties, no build-time token transformers (for now)

## Tokens

The ratified token file is `tokens/base.css` — **Wana (Light / Dark)**, the palette that grew from the Proposal D "Forest" direction.

| Category   | Key tokens                                                                                                       |
| ---------- | ---------------------------------------------------------------------------------------------------------------- |
| Color      | `--bg`, `--surface`, `--overlay`, `--muted`, `--text`, `--accent`, `--success`, `--warning`, `--error`, `--info` |
| Typography | `--font-sans`, `--font-serif`, `--font-mono`, `--step--1` → `--step-3`, `--measure`                              |
| Spacing    | `--space-2xs` → `--space-2xl`                                                                                    |
| Radius     | `--radius: 0.25rem`                                                                                              |
| Shadow     | `--shadow`, `--ring`                                                                                             |
| Motion     | `--duration-fast`, `--duration-base`, `--easing`                                                                 |

Colors: Flexoki warm paper light (`#fffcf0`) + Gruvbox dark (`#282828`), forest-green accent hue 150.
All fg/bg pairs WCAG AA+. Verify with: `python3 tools/color.py contrast <fg> <bg>`

The playground (`site/index.html`) imports `tokens/base.css` as its source of truth.

## Research Structure

```
research/
  color-theory.md          # Fundamentals: HSL, perceptual uniformity, contrast
  colorscheme-analysis.md  # Deep analysis of reference schemes
  accessibility.md         # WCAG guidelines, testing methodology
  typography.md            # Type scale, font pairing, readability
proposals/
  proposal-D.md            # "Forest" — the chosen direction
tokens/
  base.css                 # The chosen baseline token file
schemes/
  wana-light.yaml          # canonical base24 palette (light)
  wana-dark.yaml           # canonical base24 palette (dark)
tools/
  gen.py                   # schemes -> themes/
  scheme.py                # base24 loader + ANSI-16 mapping
themes/                    # GENERATED app themes (do not hand-edit)
  kitty/
  yazi/                    # GENERATED yazi flavors -> atalariq/wana.yazi (private)
    wana-dark.yazi/
    wana-light.yazi/
```

## Commit Conventions

Conventional Commits: `<type>(<scope>): <description>`
Scope: `research`, `tokens`, `proposals`, `docs`
