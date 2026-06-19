# Design System — Agent Guide

Personal design system for atalariq. Used across:
- **Journey** (digital garden, Astro) — `journey.atalariq.dev`
- **Portfolio** (atalariq.github.io)
- **Research site** (research.atalariq.dev)
- **Future projects**

## Goals

1. **Consistency** — one token system, many sites
2. **Accessibility** — WCAG AA minimum, AAA where possible
3. **Personality** — warm, readable, not generic Bootstrap-feel
4. **Simplicity** — CSS custom properties, no build-time token transformers (for now)

## Existing Tokens (Journey)

Journey already has a preliminary token system at `~/Repos/journey/src/styles/tokens.css`:
- Typography: minor-third scale (1.25), clamp() fluid
- Spacing: 2xs → 2xl
- Colors: warm light (hsl 40 30% 98%), cool dark (hsl 225 18% 11%), purple accent
- Measure: 65ch, radius: 0.5rem

## Research Structure

```
research/
  color-theory.md          # Fundamentals: HSL, perceptual uniformity, contrast
  colorscheme-analysis.md  # Deep analysis of reference schemes
  accessibility.md         # WCAG guidelines, testing methodology
  typography.md            # Type scale, font pairing, readability
proposals/
  proposal-A.md            # Full colorscheme proposal with tokens
  proposal-B.md
  proposal-C.md
tokens/
  base.css                 # The chosen baseline token file
```

## Commit Conventions

Conventional Commits: `<type>(<scope>): <description>`
Scope: `research`, `tokens`, `proposals`, `docs`
