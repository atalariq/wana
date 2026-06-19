# Proposal C — "Balanced" ★ recommended default

> **Philosophy.** Warm where warmth helps, cool where coolness helps: a warm
> parchment light mode and a cool blue-black dark mode, sharing one purple accent
> with a single hue identity re-lit per mode. It's the direct, accessibility-hardened
> evolution of the _existing Journey tokens_ — same warm-light/cool-dark instinct,
> same purple, now with every pair measured and tuned. The "safe default" that
> still has a point of view.

This is the one to ship unless there's a strong reason to favor reading-comfort
(→ A) or night-first richness (→ B). It is the most _versatile_ across the three
sites — prose, portfolio, and research all sit comfortably on it — and it's the
smallest leap from what Journey already uses.

All numbers computed by `tools/color.py`. Regenerate with
`python3 tools/proposal_matrix.py C`.

---

## Light palette (warm paper — the Journey warm white, hardened)

| Role              | Hex       | HSL                    | OKLCH                      | Contrast vs `bg` |
| ----------------- | --------- | ---------------------- | -------------------------- | ---------------- |
| `bg`              | `#fbfaf8` | `hsl(40 27.3% 97.8%)`  | `oklch(98.5% 0.003 84.6)`  | —                |
| `surface`         | `#f2f0ea` | `hsl(45 23.5% 93.3%)`  | `oklch(95.5% 0.008 91.5)`  | —                |
| `overlay`         | `#e7e4db` | `hsl(45 20% 88.2%)`    | `oklch(91.9% 0.012 91.5)`  | —                |
| `muted` (text)    | `#5d6170` | `hsl(227 9.3% 40.2%)`  | `oklch(49.5% 0.024 273.7)` | 5.90:1 AA        |
| `text`            | `#1a1c22` | `hsl(225 13.3% 11.8%)` | `oklch(22.7% 0.012 270.8)` | 16.33:1 AAA      |
| `accent` (purple) | `#5a3cc4` | `hsl(253 53.5% 50.2%)` | `oklch(47.5% 0.199 286.2)` | 6.99:1 AA        |
| `success`         | `#3f7320` | `hsl(98 56.5% 28.8%)`  | `oklch(50.1% 0.127 136.1)` | 5.46:1 AA        |
| `warning`         | `#9a6500` | `hsl(39 100% 30.2%)`   | `oklch(55.0% 0.117 73.3)`  | 4.75:1 AA        |
| `error`           | `#bb2533` | `hsl(354 67% 43.9%)`   | `oklch(51.8% 0.184 22.3)`  | 5.88:1 AA        |
| `info`            | `#2660a8` | `hsl(213 63.1% 40.4%)` | `oklch(49.0% 0.130 255.6)` | 6.06:1 AA        |

## Dark palette (cool blue-black — the Journey dark, hardened)

| Role              | Hex       | HSL                    | OKLCH                      | Contrast vs `bg` |
| ----------------- | --------- | ---------------------- | -------------------------- | ---------------- |
| `bg`              | `#171a21` | `hsl(222 17.9% 11%)`   | `oklch(21.8% 0.015 266.9)` | —                |
| `surface`         | `#20232c` | `hsl(225 15.8% 14.9%)` | `oklch(25.7% 0.018 270.6)` | —                |
| `overlay`         | `#2b2f3a` | `hsl(224 14.9% 19.8%)` | `oklch(30.6% 0.021 269.4)` | —                |
| `muted` (text)    | `#a7adbc` | `hsl(223 13.5% 69.6%)` | `oklch(74.8% 0.023 268.4)` | 7.75:1 AAA       |
| `text`            | `#e6e8ef` | `hsl(227 22% 92%)`     | `oklch(93.1% 0.010 273.4)` | 14.22:1 AAA      |
| `accent` (purple) | `#9b86f0` | `hsl(252 77.9% 73.3%)` | `oklch(68.4% 0.153 290.9)` | 5.85:1 AA        |
| `success`         | `#94c46a` | `hsl(92 43.3% 59.2%)`  | `oklch(76.6% 0.130 131.8)` | 8.59:1 AAA       |
| `warning`         | `#e0b15a` | `hsl(39 68.4% 61.6%)`  | `oklch(78.6% 0.118 81.0)`  | 8.79:1 AAA       |
| `error`           | `#ef8090` | `hsl(351 77.6% 72%)`   | `oklch(72.7% 0.137 11.9)`  | 6.77:1 AA        |
| `info`            | `#79b0e6` | `hsl(210 68.6% 68.8%)` | `oklch(74.0% 0.098 248.8)` | 7.60:1 AAA       |

### The shared accent — one identity, two weights

This is the proposal's defining move. The purple keeps a **single hue identity**
across modes and only changes lightness/chroma:

| Mode  | Hex       | OKLCH                      | Δ                           |
| ----- | --------- | -------------------------- | --------------------------- |
| Light | `#5a3cc4` | `oklch(47.5% 0.199 286.2)` | deep violet, full chroma    |
| Dark  | `#9b86f0` | `oklch(68.4% 0.153 290.9)` | +20.9 L, −0.046 C, hue held |

Hue moves only 286→291 (≈5°, imperceptible — still "the purple"). Lightness does
all the work: +21 L for the dark surface. This is the Solarized "shared accent"
_idea_ done right — Solarized failed because it reused the _same_ values on both
bg (and cyan/green dropped below AA on light); here the hue is shared but the
value is retuned, so both modes clear AA. See `research/colorscheme-analysis.md`
§2 and the cross-scheme lessons.

---

## Contrast matrix — every fg × bg

WCAG: **AAA** ≥7 · **AA** ≥4.5 · **AA-large** ≥3 (≥18px/UI only) · **fail** <3.

### Light

| fg \ bg   | `bg` #fbfaf8 | `surface` #f2f0ea | `overlay` #e7e4db |
| --------- | ------------ | ----------------- | ----------------- |
| `text`    | 16.33 AAA    | 14.94 AAA         | 13.40 AAA         |
| `muted`   | 5.90 AA      | 5.41 AA           | 4.85 AA           |
| `accent`  | 6.99 AA      | 6.40 AA           | 5.74 AA           |
| `success` | 5.46 AA      | 5.00 AA           | 4.48 AA-large     |
| `warning` | 4.75 AA      | 4.35 AA-large     | 3.90 AA-large     |
| `error`   | 5.88 AA      | 5.38 AA           | 4.82 AA           |
| `info`    | 6.06 AA      | 5.55 AA           | 4.97 AA           |

### Dark

| fg \ bg   | `bg` #171a21 | `surface` #20232c | `overlay` #2b2f3a |
| --------- | ------------ | ----------------- | ----------------- |
| `text`    | 14.22 AAA    | 12.82 AAA         | 10.92 AAA         |
| `muted`   | 7.75 AAA     | 6.98 AA           | 5.95 AA           |
| `accent`  | 5.85 AA      | 5.28 AA           | 4.50 AA-large     |
| `success` | 8.59 AAA     | 7.74 AAA          | 6.60 AA           |
| `warning` | 8.79 AAA     | 7.93 AAA          | 6.75 AA           |
| `error`   | 6.77 AA      | 6.10 AA           | 5.20 AA           |
| `info`    | 7.60 AAA     | 6.85 AA           | 5.84 AA           |

**Reading the table.** `text`/`muted`/`accent` clear AA on every background in
both modes (only accent-on-`overlay` in dark is AA-large — and accent is rarely
set on the third-level bg). Dark `muted` is a standout 7.75:1 (AAA) — the muted
failure that plagues most schemes (`research/colorscheme-analysis.md` lesson #3)
is solved here. Semantic AA-large cells are again confined to `overlay`; use them
as icons/borders, message text in `--text`.

---

## CSS custom properties (copy-paste)

Light default (matches Journey today), dark via OS preference and `[data-theme]`.
Drop-in compatible with the existing `tokens.css` variable names.

```css
:root {
  /* ── Balanced — light (warm paper) ────────────────────────── */
  --bg: oklch(98.5% 0.003 84.6); /* #fbfaf8 */
  --surface: oklch(95.5% 0.008 91.5); /* #f2f0ea */
  --overlay: oklch(91.9% 0.012 91.5); /* #e7e4db */
  --muted: oklch(49.5% 0.024 273.7); /* #5d6170 */
  --text: oklch(22.7% 0.012 270.8); /* #1a1c22 */
  --accent: oklch(47.5% 0.199 286.2); /* #5a3cc4 */
  --success: oklch(50.1% 0.127 136.1); /* #3f7320 */
  --warning: oklch(55% 0.117 73.3); /* #9a6500 */
  --error: oklch(51.8% 0.184 22.3); /* #bb2533 */
  --info: oklch(49% 0.13 255.6); /* #2660a8 */
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* ── Balanced — dark (cool blue-black) ────────────────── */
    --bg: oklch(21.8% 0.015 266.9); /* #171a21 */
    --surface: oklch(25.7% 0.018 270.6); /* #20232c */
    --overlay: oklch(30.6% 0.021 269.4); /* #2b2f3a */
    --muted: oklch(74.8% 0.023 268.4); /* #a7adbc */
    --text: oklch(93.1% 0.01 273.4); /* #e6e8ef */
    --accent: oklch(68.4% 0.153 290.9); /* #9b86f0 */
    --success: oklch(76.6% 0.13 131.8); /* #94c46a */
    --warning: oklch(78.6% 0.118 81); /* #e0b15a */
    --error: oklch(72.7% 0.137 11.9); /* #ef8090 */
    --info: oklch(74% 0.098 248.8); /* #79b0e6 */
  }
}

/* Explicit user choice wins over OS preference. */
[data-theme="dark"] {
  --bg: oklch(21.8% 0.015 266.9);
  --surface: oklch(25.7% 0.018 270.6);
  --overlay: oklch(30.6% 0.021 269.4);
  --muted: oklch(74.8% 0.023 268.4);
  --text: oklch(93.1% 0.01 273.4);
  --accent: oklch(68.4% 0.153 290.9);
  --success: oklch(76.6% 0.13 131.8);
  --warning: oklch(78.6% 0.118 81);
  --error: oklch(72.7% 0.137 11.9);
  --info: oklch(74% 0.098 248.8);
}
```

---

## Preview — blog post + code block

### Light (warm paper)

```
┌──────────────────────────────────────────────────────────────┐
│  ░░ #fbfaf8 warm white ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│                                                                │
│   Notes on Type Scales            ← #1a1c22 text, AAA 16.3:1   │
│   ──────────────────                                           │
│   Posted 2026-06-19 · 5 min read  ← #5d6170 muted, AA 5.9:1    │
│                                                                │
│   A minor-third ratio (1.25) gives a calm, readable scale.     │
│   The purple [modular scale] link is the shared accent —       │
│   deep violet here, the very same hue you'll see glow in       │
│   dark mode.                                                    │
│                  └─ #5a3cc4 accent, AA 7.0:1                   │
│                                                                │
│   ┌── #f2f0ea surface ──────────────────────────────────┐     │
│   │  :root {                            /* comment */     │    │
│   │    --step-0: 1rem;                  /* success 5.5 */ │    │
│   │    --step-1: 1.25rem;               /* info 6.1   */  │    │
│   │    --ratio:  1.25;                  /* warning 4.8 */ │    │
│   │  }                                                    │    │
│   └──────────────────────────────────────────────────────┘     │
│                                                                │
│   ⚠ warning #9a6500   ✓ success #3f7320   ✕ error #bb2533      │
└──────────────────────────────────────────────────────────────┘
```

### Dark (cool blue-black)

```
┌──────────────────────────────────────────────────────────────┐
│  ▓▓ #171a21 cool blue-black ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│                                                                │
│   Notes on Type Scales            ← #e6e8ef text, AAA 14.2:1   │
│   ──────────────────                                           │
│   Posted 2026-06-19 · 5 min read  ← #a7adbc muted, AAA 7.8:1   │
│                                                                │
│   Same article, same shared purple [modular scale] link —      │
│   now a soft lavender, re-lit (+21 L) so it glows on the       │
│   cool dark field instead of sinking. One hue, two weights.    │
│                  └─ #9b86f0 accent, AA 5.9:1                   │
│                                                                │
│   ┌── #20232c surface (elevation by lightness) ───────┐       │
│   │  :root {                            /* comment */    │     │
│   │    --step-0: 1rem;                  /* success 8.6 */│     │
│   │    --step-1: 1.25rem;               /* info 6.9   */ │     │
│   │    --ratio:  1.25;                  /* warning 7.9 */│     │
│   │  }                                                   │     │
│   └──────────────────────────────────────────────────────┘     │
│                                                                │
│   ⚠ warning #e0b15a   ✓ success #94c46a   ✕ error #ef8090      │
└──────────────────────────────────────────────────────────────┘
```

---

## Honest trade-offs

- **+** Most versatile; works for prose, portfolio, and research equally. The "safe" choice that still has personality.
- **+** Smallest migration from the current Journey tokens — same warm-light/cool-dark/purple DNA, now measured and AA-clean. Variable names are drop-in compatible.
- **+** Solves the muted-text problem in dark mode (7.75:1 AAA) and keeps a genuinely shared accent identity across modes.
- **−** By splitting the difference (warm light + cool dark), it commits less hard than A (all-warm) or B (rich dark). If you want a _strong_ singular mood, a focused proposal beats the synthesis.
- **−** Light `warning` (4.75:1) and the AA-large semantic-on-`overlay` cells are the structural yellow/green-on-light limit; lean on icons for status.
- **−** Two different background _temperatures_ between modes means screenshots/branding shift feel slightly between light and dark — a deliberate trade for per-mode comfort.

> **Deviation from the general research, on purpose.** The reusable Hermes color
> synthesis (`~/Works/Hermes/.../personal-color-palette.md`) recommends a
> "warm everywhere" default — Flexoki-light + Everforest-_dark_ with an accent
> that shifts hue per mode (blue on light, green on dark). C goes the other way:
> cool blue-black dark and one re-lit purple. This isn't drift — it's continuity
> with the existing Journey tokens and a preference for temperature contrast over
> warmth consistency. See `research/colorscheme-analysis.md` →
> "Where this diverges from the general research."

---

## My recommendation

**Ship C as the baseline (`tokens/base.css`).** It's the lowest-risk, highest-
versatility option and the most faithful continuation of the existing system.
Keep **A "Warm Ink"** in your back pocket as an alternate _theme_ for the most
reading-heavy surface (the digital garden could opt into it), since both share
the OKLCH authoring model and the same token names — switching is just swapping
the variable block. **B "Night Scholar"** is the choice only if you decide the
system should be dark-first; it's the most opinionated and the least like what
Journey is today.
