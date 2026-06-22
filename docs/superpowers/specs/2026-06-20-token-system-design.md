# Token System Design — Forest

**Date:** 2026-06-20
**Status:** Approved, pending implementation
**Scope:** Typography, spacing, radius, shadow, motion tokens for `tokens/base.css`

---

## Context

The color layer is already decided: Proposal D "Forest" (Flexoki warm paper light + Gruvbox dark, hue-150 forest green signature). This spec covers the remaining token categories needed to ratify `tokens/base.css` in one complete pass.

The playground (`site/style.css`) already contains working definitions for all of these. The implementation task is to **extract them as the canonical source** — with two changes from the playground's current values: `--radius` drops from `0.5rem` to `0.25rem`, and motion tokens become first-class CSS custom properties with `prefers-reduced-motion` support.

---

## Typography

### Font stacks

```css
--font-sans:
  ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
--font-serif: ui-serif, Georgia, Cambria, "Times New Roman", serif;
--font-mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
```

System-only. No web font loading — zero network overhead, consistent with Gruvbox/Flexoki's "comfort over punch" ethos. `--font-sans` is the default body face; `--font-serif` available for long-form prose contexts; `--font-mono` for code.

### Type scale

Minor-third ratio (×1.25), fluid via `clamp()`. Five steps:

```css
--step--1: clamp(0.83rem, 0.8rem + 0.15vw, 0.9rem);
--step-0: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
--step-1: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
--step-2: clamp(1.56rem, 1.4rem + 0.8vw, 2rem);
--step-3: clamp(1.95rem, 1.7rem + 1.25vw, 2.75rem);
```

Intended mapping (not enforced at token level — components decide):

| Step        | Typical use                       |
| ----------- | --------------------------------- |
| `--step--1` | Caption, label, meta, code inline |
| `--step-0`  | Body text                         |
| `--step-1`  | h3, subheading                    |
| `--step-2`  | h2, section heading               |
| `--step-3`  | h1, hero                          |

### Prose measure

```css
--measure: 65ch;
```

Applied to any prose container to cap line length in the readable 45–75ch range.

### Base body defaults (in `body` rule, not tokens)

```css
font-family: var(--font-sans);
font-size: var(--step-0);
line-height: 1.6;
```

---

## Spacing

Seven-step scale, approximately ×1.5 progression:

```css
--space-2xs: 0.25rem; /*  4px */
--space-xs: 0.5rem; /*  8px */
--space-s: 0.75rem; /* 12px */
--space-m: 1rem; /* 16px */
--space-l: 1.5rem; /* 24px */
--space-xl: 2.5rem; /* 40px */
--space-2xl: 4rem; /* 64px */
```

No change from the playground.

---

## Radius

```css
--radius: 0.25rem;
```

Single token. Sharp/editorial — changed from playground's `0.5rem`. Consistent with filmic/print reference aesthetic (Lily Chou-Chou, Wong Kar-Wai). All components use this one value; no radius scale needed at this stage.

---

## Shadow & Ring

```css
--shadow:
  0 1px 2px color-mix(in oklch, var(--text) 8%, transparent),
  0 4px 12px color-mix(in oklch, var(--text) 6%, transparent);

--ring: 0 0 0 3px color-mix(in oklch, var(--accent) 35%, transparent);
```

Both are theme-aware — they reference `--text` and `--accent` so they automatically adapt between light and dark without separate dark-mode overrides.

- `--shadow`: for elevated surfaces (cards, dropdowns, modals)
- `--ring`: for focus states on interactive elements

---

## Motion

Currently hardcoded in `site/style.css`. Extracting as tokens and adding `prefers-reduced-motion` support, which the playground currently lacks.

```css
--duration-fast: 0.15s; /* hover, micro-interactions */
--duration-base: 0.25s; /* theme switch, larger transitions */
--easing: ease;
```

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0;
    --duration-base: 0;
  }
}
```

All `transition` declarations in components should use `var(--duration-fast)` or `var(--duration-base)` instead of hardcoded values.

---

## What this spec does NOT cover

- **Color tokens** — already in `proposals/proposal-D.md`; will be merged into `tokens/base.css` alongside these.
- **Component library** — post-token work; spec lives in Hermes `research/design-system/component-library-v0.md`.
- **The playground** (`site/style.css`) — it re-defines its own tokens inline. Once `tokens/base.css` is ratified, the playground should import it instead. That wiring is part of the implementation task.

---

## Implementation checklist

1. Update `tokens/base.css`:
   - Replace Proposal C color block with Proposal D "Forest"
   - Add typography, spacing, radius, shadow, ring, motion tokens
   - Add `prefers-reduced-motion` block
2. Update `site/index.html` to `<link>` `tokens/base.css` before `style.css`
3. Remove duplicate token declarations from `site/style.css` (keep component rules, remove `:root` token block)
4. Update `--radius` usages in `site/style.css` from hardcoded `0.5rem` to `var(--radius)` where not already done
5. Replace hardcoded `0.15s ease` / `0.25s ease` transition values with `var(--duration-fast)` / `var(--duration-base) var(--easing)`
6. Update `AGENTS.md` to reflect ratified token file
