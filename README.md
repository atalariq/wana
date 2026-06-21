# Wana

A personal CSS custom-property design system used across atalariq's sites — Journey, Portfolio, and Research. No build step, no framework, no preprocessor. Drop in one CSS file and use `var(--token)`. The ratified palette is **Wana** (Proposal D), with two flavors: **Wana Light** (warm Flexoki paper) and **Wana Dark** (Gruvbox warm-dark), tied together by a forest-green accent (OKLCH hue 150).

---

## Quick start

**CSS import**

```css
@import "tokens/base.css";
```

**HTML link**

```html
<link rel="stylesheet" href="tokens/base.css" />
```

**Usage**

```css
.button {
  background: var(--accent);
  color: var(--bg);
  border-radius: var(--radius);
  padding: var(--space-2xs) var(--space-m);
  transition: opacity var(--duration-fast) var(--easing);
}
```

---

## Token reference

### Color

| Token       | Light hex | Dark hex  | Role                             |
| ----------- | --------- | --------- | -------------------------------- |
| `--bg`      | `#fffcf0` | `#282828` | Page background                  |
| `--surface` | `#f2f0e5` | `#32302f` | Cards, panels                    |
| `--overlay` | `#e6e4d9` | `#3c3836` | Dropdowns, tooltips              |
| `--muted`   | `#6f6e69` | `#a89984` | Placeholder, secondary text (AA) |
| `--text`    | `#100f0f` | `#ebdbb2` | Body text (AAA)                  |
| `--accent`  | `#2d6e3f` | `#7abb87` | Forest green — links, focus, CTA |
| `--success` | `#5f7a0a` | `#9fbe5c` | Positive feedback                |
| `--warning` | `#a06300` | `#eeb562` | Caution                          |
| `--error`   | `#bc4039` | `#fe8b89` | Destructive, invalid             |
| `--info`    | `#1c6aae` | `#80b7f0` | Informational                    |

All fg/bg pairs are WCAG AA at minimum. See `proposals/proposal-D.md` for full contrast ratios.

### Typography

| Token          | Value                                                                     |
| -------------- | ------------------------------------------------------------------------- |
| `--font-sans`  | `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif` |
| `--font-serif` | `ui-serif, Georgia, Cambria, "Times New Roman", serif`                    |
| `--font-mono`  | `ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace`              |
| `--step--1`    | `clamp(0.83rem, 0.8rem + 0.15vw, 0.9rem)`                                 |
| `--step-0`     | `clamp(1rem, 0.95rem + 0.25vw, 1.125rem)`                                 |
| `--step-1`     | `clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)`                                 |
| `--step-2`     | `clamp(1.56rem, 1.4rem + 0.8vw, 2rem)`                                    |
| `--step-3`     | `clamp(1.95rem, 1.7rem + 1.25vw, 2.75rem)`                                |
| `--measure`    | `65ch`                                                                    |

Minor-third scale (×1.25), fluid via `clamp()`.

### Spacing

| Token         | Value            |
| ------------- | ---------------- |
| `--space-2xs` | `0.25rem` (4px)  |
| `--space-xs`  | `0.5rem` (8px)   |
| `--space-s`   | `0.75rem` (12px) |
| `--space-m`   | `1rem` (16px)    |
| `--space-l`   | `1.5rem` (24px)  |
| `--space-xl`  | `2.5rem` (40px)  |
| `--space-2xl` | `4rem` (64px)    |

### Misc

| Token             | Value                | Notes                                                 |
| ----------------- | -------------------- | ----------------------------------------------------- |
| `--radius`        | `0.25rem`            | Applied uniformly                                     |
| `--shadow`        | two-layer box-shadow | Via `color-mix(in oklch, var(--text) …)`              |
| `--ring`          | focus ring           | `color-mix(in oklch, var(--accent) 35%, transparent)` |
| `--duration-fast` | `0.15s`              | Hover, micro-interactions                             |
| `--duration-base` | `0.25s`              | Theme switch, larger transitions                      |
| `--easing`        | `ease`               |                                                       |

---

## Theming

Light mode is the default. To pin a mode explicitly, set `data-theme` on `<html>`:

```html
<html data-theme="dark">
  <!-- force dark -->
  <html data-theme="light">
    <!-- force light, even on dark-OS -->
  </html>
</html>
```

Without `data-theme`, OS preference is honored automatically via `@media (prefers-color-scheme: dark)`. Reduced motion is also respected — `--duration-fast` and `--duration-base` collapse to `0s` when `prefers-reduced-motion: reduce` is active.

---

## Authoring colors

OKLCH is the canonical format. Hex values are kept as comments for eyeballing only. To verify contrast for any new pair:

```bash
python3 tools/color.py contrast <fg> <bg>
```

To generate a new semantic color fitted to a contrast target:

```bash
python3 tools/color.py fit <C> <H> <bg> <target> <light|dark>
```

Every shipped fg/bg pair is WCAG AA or better. See `research/accessibility.md` and `research/color-theory.md` for methodology.

---

## Browser support

This system uses `oklch()` and `color-mix()`. Modern evergreen browsers only (Chrome 111+, Firefox 113+, Safari 16.4+). No fallback hex values are shipped — if you need IE or older support, this is the wrong tool.

---

## App themes

Terminal/editor themes are generated from the canonical base24 schemes in
`schemes/` by `tools/gen.py`, into `themes/` (never hand-edited). Regenerate
with `python3 tools/gen.py`; freshness is checked with `python3 tools/gen.py --check`.

---

## Playground

`site/index.html` is a live, no-build token playground with an editor, contrast checker, and import/export. It dogfoods `tokens/base.css` directly as its source of truth.
