# Token System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ratify `tokens/base.css` with the full Forest token set (color + typography + spacing + radius + shadow + motion) and wire the playground to import it as the single source of truth.

**Architecture:** Three-file split — `tokens/base.css` owns all custom properties, `site/style.css` owns component rules only, `site/index.html` links both. Two non-trivial changes from the playground's current state: `--radius` drops from `0.5rem` to `0.25rem`, and motion durations become CSS custom properties with `prefers-reduced-motion` support.

**Tech Stack:** CSS custom properties, OKLCH colors, `color-mix()`, `clamp()` fluid type, no build step.

---

## File Map

| File              | Action      | What changes                                                                                  |
| ----------------- | ----------- | --------------------------------------------------------------------------------------------- |
| `tokens/base.css` | **Rewrite** | Replace Proposal C stub with full Forest token set                                            |
| `site/index.html` | **Modify**  | Add `<link>` for `tokens/base.css` before `style.css`                                         |
| `site/style.css`  | **Modify**  | Remove `:root` token block + `[data-theme="dark"]` block; replace hardcoded transition values |
| `AGENTS.md`       | **Modify**  | Update token section to reflect Forest and ratified state                                     |

---

## Task 1: Rewrite `tokens/base.css`

**Files:**

- Modify: `tokens/base.css`

- [ ] **Step 1: Replace the file with the full Forest token set**

```css
/* ════════════════════════════════════════════════════════════════════
   Design System — base tokens
   Theme: Proposal D "Forest" (ratified 2026-06-20)

   Authoring model: OKLCH is canonical (perceptual lightness lets us
   re-light the accent per mode by arithmetic). Hex kept as a comment
   for eyeballing. See research/color-theory.md §1.

   Every fg/bg pair is WCAG AA+; verify with: python3 tools/color.py
   ════════════════════════════════════════════════════════════════════ */

:root {
  /* ── Color: light (Flexoki warm paper) ─────────────────────────── */
  --bg: oklch(99% 0.016 95.2); /* #fffcf0  */
  --surface: oklch(95.4% 0.015 98.3); /* #f2f0e5  */
  --overlay: oklch(91.7% 0.015 98.3); /* #e6e4d9  */
  --muted: oklch(53.8% 0.008 97.4); /* #6f6e69  — 4.97:1 AA  */
  --text: oklch(17% 0.002 17.3); /* #100f0f  — 18.62:1 AAA */
  --accent: oklch(48.3% 0.1 150.1); /* #2d6e3f  — 5.99:1 AA  */
  --success: oklch(53.9% 0.13 123.9); /* #5f7a0a  — 4.78:1 AA  */
  --warning: oklch(55.4% 0.121 68.5); /* #a06300  — 4.78:1 AA  */
  --error: oklch(54.6% 0.161 27); /* #bc4039  — 5.20:1 AA  */
  --info: oklch(51.4% 0.13 249.9); /* #1c6aae  — 5.49:1 AA  */

  /* ── Typography ─────────────────────────────────────────────────── */
  --font-sans:
    ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-serif: ui-serif, Georgia, Cambria, "Times New Roman", serif;
  --font-mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;

  /* Minor-third scale (×1.25), fluid via clamp() */
  --step--1: clamp(0.83rem, 0.8rem + 0.15vw, 0.9rem);
  --step-0: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --step-1: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --step-2: clamp(1.56rem, 1.4rem + 0.8vw, 2rem);
  --step-3: clamp(1.95rem, 1.7rem + 1.25vw, 2.75rem);

  --measure: 65ch;

  /* ── Spacing ─────────────────────────────────────────────────────── */
  --space-2xs: 0.25rem; /*  4px */
  --space-xs: 0.5rem; /*  8px */
  --space-s: 0.75rem; /* 12px */
  --space-m: 1rem; /* 16px */
  --space-l: 1.5rem; /* 24px */
  --space-xl: 2.5rem; /* 40px */
  --space-2xl: 4rem; /* 64px */

  /* ── Radius ──────────────────────────────────────────────────────── */
  --radius: 0.25rem;

  /* ── Shadow & Ring ───────────────────────────────────────────────── */
  --shadow:
    0 1px 2px color-mix(in oklch, var(--text) 8%, transparent),
    0 4px 12px color-mix(in oklch, var(--text) 6%, transparent);
  --ring: 0 0 0 3px color-mix(in oklch, var(--accent) 35%, transparent);

  /* ── Motion ──────────────────────────────────────────────────────── */
  --duration-fast: 0.15s; /* hover, micro-interactions */
  --duration-base: 0.25s; /* theme switch, larger transitions */
  --easing: ease;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* ── Color: dark (Gruvbox warm dark) ───────────────────────── */
    --bg: oklch(27.7% 0 89.9); /* #282828  */
    --surface: oklch(31.1% 0.003 48.6); /* #32302f  */
    --overlay: oklch(34.4% 0.007 48.5); /* #3c3836  */
    --muted: oklch(69% 0.035 76.3); /* #a89984  — 5.30:1 AA  */
    --text: oklch(89.4% 0.057 89.2); /* #ebdbb2  — 10.75:1 AAA */
    --accent: oklch(73.4% 0.1 149.7); /* #7abb87  — 6.52:1 AA  */
    --success: oklch(75.7% 0.13 124); /* #9fbe5c  — 7.02:1 AAA */
    --warning: oklch(80.9% 0.12 75); /* #eeb562  — 8.02:1 AAA */
    --error: oklch(76.2% 0.14 21.9); /* #fe8b89  — 6.51:1 AA  */
    --info: oklch(76.3% 0.101 250.1); /* #80b7f0  — 6.99:1 AA  */
  }
}

[data-theme="dark"] {
  --bg: oklch(27.7% 0 89.9);
  --surface: oklch(31.1% 0.003 48.6);
  --overlay: oklch(34.4% 0.007 48.5);
  --muted: oklch(69% 0.035 76.3);
  --text: oklch(89.4% 0.057 89.2);
  --accent: oklch(73.4% 0.1 149.7);
  --success: oklch(75.7% 0.13 124);
  --warning: oklch(80.9% 0.12 75);
  --error: oklch(76.2% 0.14 21.9);
  --info: oklch(76.3% 0.101 250.1);
}

[data-theme="light"] {
  --bg: oklch(99% 0.016 95.2);
  --surface: oklch(95.4% 0.015 98.3);
  --overlay: oklch(91.7% 0.015 98.3);
  --muted: oklch(53.8% 0.008 97.4);
  --text: oklch(17% 0.002 17.3);
  --accent: oklch(48.3% 0.1 150.1);
  --success: oklch(53.9% 0.13 123.9);
  --warning: oklch(55.4% 0.121 68.5);
  --error: oklch(54.6% 0.161 27);
  --info: oklch(51.4% 0.13 249.9);
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0;
    --duration-base: 0;
  }
}
```

- [ ] **Step 2: Verify the file looks right**

```bash
wc -l tokens/base.css
```

Expected: ~110 lines. Open the file and confirm four color blocks (`:root`, `@media (prefers-color-scheme: dark)`, `[data-theme="dark"]`, `[data-theme="light"]`) and the `prefers-reduced-motion` block are all present.

- [ ] **Step 3: Commit**

```bash
git add tokens/base.css
git commit -m "feat(tokens): ratify base.css — Forest color + full token set"
```

---

## Task 2: Wire the playground to import `tokens/base.css`

**Files:**

- Modify: `site/index.html` line 11
- Modify: `site/style.css` lines 1–65 (`:root` token block + `[data-theme="dark"]` block)

The current `site/style.css` opens with a `:root { ... }` block (lines 1–51) that duplicates what's now in `tokens/base.css`, followed by a `[data-theme="dark"] { ... }` block (lines 54–65). Both need to go.

Two playground-specific layout variables — `--header-h` and `--sidebar-w` — live inside the `:root` block and must be preserved. They are NOT general tokens; they stay in `site/style.css` in their own small `:root` block.

- [ ] **Step 1: Add the token link to `site/index.html`**

Replace line 11:

```html
<link rel="stylesheet" href="style.css" />
```

With:

```html
<link rel="stylesheet" href="../tokens/base.css" />
<link rel="stylesheet" href="style.css" />
```

- [ ] **Step 2: Remove the token block from `site/style.css`**

The file currently opens with:

```css
/* ── Tokens: colors ─────────────────────────────────────────────── */
:root {
  ...all token definitions...
  --header-h: 3.75rem;
  --sidebar-w: 15rem;
  --ring: ...;
  --shadow: ...;
}

/* Dark defaults (Proposal C). app.js keeps these in sync on theme/proposal change. */
[data-theme="dark"] {
  ...dark color overrides...
}
```

Replace that entire opening block (everything before `/* ── Reset / base ──`) with just the playground-specific layout variables:

```css
/* ── Playground layout variables ────────────────────────────────── */
:root {
  --header-h: 3.75rem;
  --sidebar-w: 15rem;
}
```

Everything from `/* ── Reset / base ──` onward stays untouched.

- [ ] **Step 3: Open the playground and verify visually**

```bash
# open site/index.html in browser (double-click or use a local server)
```

Checks:

- Forest light palette is active (warm paper background `#fffcf0`, forest green accent)
- Switching to dark mode shows Gruvbox dark (`#282828`)
- All proposals in the dropdown still switch colors correctly (app.js overrides still work)
- No console errors about undefined CSS variables

- [ ] **Step 4: Commit**

```bash
git add site/index.html site/style.css
git commit -m "refactor(site): import tokens/base.css; remove duplicated token block from style.css"
```

---

## Task 3: Replace hardcoded transition values in `site/style.css`

**Files:**

- Modify: `site/style.css`

All hardcoded `0.15s ease` and `0.25s ease` transition values in component rules need to use `var(--duration-fast)` and `var(--duration-base)` so `prefers-reduced-motion` takes effect. Circles (`50%`) and pill (`1em`) border-radius values are intentional — do not touch them.

- [ ] **Step 1: Replace the body theme-switch transition (was line ~90)**

Find:

```css
transition:
  background-color 0.25s ease,
  color 0.25s ease;
```

Replace with:

```css
transition:
  background-color var(--duration-base) var(--easing),
  color var(--duration-base) var(--easing);
```

- [ ] **Step 2: Replace `.proposal-mini-tabs button` hover transition (was line ~165)**

Find:

```css
transition: all 0.15s ease;
```

This selector is `.proposal-mini-tabs button`. Replace with:

```css
transition: all var(--duration-fast) var(--easing);
```

Note: there are multiple `transition: all 0.15s ease;` instances — use surrounding context to target the right one. They can all safely be replaced with the same value.

- [ ] **Step 3: Replace the remaining `0.15s ease` transitions**

Find all remaining instances (there are ~6 more — buttons, toggle-track, toggle-thumb, proposal-dot):

```
0.15s ease
```

Replace all with:

```
var(--duration-fast) var(--easing)
```

Use a global find-and-replace in your editor. Confirm the count before and after: there should be zero instances of `0.15s ease` remaining.

```bash
grep -c "0\.15s ease" site/style.css
```

Expected: `0`

- [ ] **Step 4: Confirm no `0.25s ease` instances remain**

```bash
grep -c "0\.25s ease" site/style.css
```

Expected: `0`

- [ ] **Step 5: Open the playground and verify transitions still work**

- Hover over buttons and nav elements — transitions should feel the same
- Toggle dark mode — background/color transition should animate
- Check with DevTools: set `prefers-reduced-motion: reduce` in the Rendering panel → transitions should be instant (0s)

- [ ] **Step 6: Commit**

```bash
git add site/style.css
git commit -m "refactor(site): use --duration-fast/base tokens for all transitions"
```

---

## Task 4: Update `AGENTS.md`

**Files:**

- Modify: `AGENTS.md`

- [ ] **Step 1: Update the token section**

The current `AGENTS.md` says:

```
tokens/
  base.css                 # The chosen baseline token file
```

And the "Existing Tokens (Journey)" section references Journey's old purple/cool token system.

Replace the entire "Existing Tokens (Journey)" section with:

```markdown
## Tokens

The ratified token file is `tokens/base.css` — **Proposal D "Forest"** (2026-06-20).

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
```

- [ ] **Step 2: Commit**

```bash
git add AGENTS.md
git commit -m "docs(agents): update token section to reflect ratified Forest system"
```
