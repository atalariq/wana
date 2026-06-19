# Proposal B — "Night Scholar"

> **Philosophy.** Built dark-first, for the 1 a.m. session. The background is a
> deep, _rich_ blue-black — not flat gray — that gives the screen depth, the way
> Tokyo Night and Gruvbox feel alive rather than washed out. The accent is the
> existing Journey purple, kept as the brand thread. Light mode exists and is
> accessible, but it's the understudy: a cool, slightly blue paper for the rare
> daytime read.

Pick this if you spend most of your time in the dark and want it to feel
_designed_, not defaulted. The dark palette is the showpiece; every accent on it
clears AA, most hit AAA.

All numbers computed by `tools/color.py`. Regenerate with
`python3 tools/proposal_matrix.py B`.

---

## Dark palette (the hero)

| Role              | Hex       | HSL                    | OKLCH                      | Contrast vs `bg` |
| ----------------- | --------- | ---------------------- | -------------------------- | ---------------- |
| `bg`              | `#14151f` | `hsl(235 21.6% 10%)`   | `oklch(20.0% 0.020 280.0)` | —                |
| `surface`         | `#1d1f2c` | `hsl(232 20.5% 14.3%)` | `oklch(24.3% 0.025 277.6)` | —                |
| `overlay`         | `#282b3c` | `hsl(231 20% 19.6%)`   | `oklch(29.4% 0.031 276.5)` | —                |
| `muted` (text)    | `#9097ba` | `hsl(230 23.3% 64.7%)` | `oklch(68.3% 0.052 276.1)` | 6.33:1 AA        |
| `text`            | `#d7dbf2` | `hsl(231 50.9% 89.6%)` | `oklch(89.5% 0.032 277.9)` | 13.23:1 AAA      |
| `accent` (purple) | `#b49cf5` | `hsl(256 81.7% 78.6%)` | `oklch(74.8% 0.128 295.6)` | 7.79:1 AAA       |
| `success`         | `#9ed07a` | `hsl(95 47.8% 64.7%)`  | `oklch(80.2% 0.126 133.2)` | 10.16:1 AAA      |
| `warning`         | `#e6b860` | `hsl(39 72.8% 63.9%)`  | `oklch(80.6% 0.119 81.9)`  | 9.85:1 AAA       |
| `error`           | `#f08599` | `hsl(349 78.1% 73.1%)` | `oklch(73.8% 0.132 8.9)`   | 7.37:1 AAA       |
| `info`            | `#7fb8e8` | `hsl(207 69.5% 70.4%)` | `oklch(76.1% 0.091 244.8)` | 8.58:1 AAA       |

## Light palette (the understudy)

| Role              | Hex       | HSL                    | OKLCH                      | Contrast vs `bg` |
| ----------------- | --------- | ---------------------- | -------------------------- | ---------------- |
| `bg`              | `#e9eaf2` | `hsl(233 25.7% 93.1%)` | `oklch(93.9% 0.011 280.5)` | —                |
| `surface`         | `#dfe1ec` | `hsl(231 25.5% 90%)`   | `oklch(91.1% 0.015 277.8)` | —                |
| `overlay`         | `#d2d5e4` | `hsl(230 25% 85.9%)`   | `oklch(87.5% 0.021 276.9)` | —                |
| `muted` (text)    | `#565b76` | `hsl(231 15.7% 40%)`   | `oklch(47.7% 0.044 276.4)` | 5.55:1 AA        |
| `text`            | `#1c1f2e` | `hsl(230 24.3% 14.5%)` | `oklch(24.4% 0.029 275.3)` | 13.63:1 AAA      |
| `accent` (purple) | `#6a3fd0` | `hsl(258 60.7% 53.1%)` | `oklch(50.5% 0.209 290.5)` | 5.42:1 AA        |
| `success`         | `#357025` | `hsl(107 50.3% 29.2%)` | `oklch(48.8% 0.124 139.6)` | 5.01:1 AA        |
| `warning`         | `#855800` | `hsl(40 100% 26.1%)`   | `oklch(49.7% 0.105 74.7)`  | 5.16:1 AA        |
| `error`           | `#c02748` | `hsl(347 66.2% 45.3%)` | `oklch(53.2% 0.187 15.0)`  | 4.83:1 AA        |
| `info`            | `#2861b8` | `hsl(216 64.3% 43.9%)` | `oklch(50.3% 0.150 258.9)` | 5.02:1 AA        |

The purple accent holds hue identity (~290–296° OKLCH) across modes but flips
weight: a bright lavender L 74.8% on dark → a deep violet L 50.5% on light. This
is the Catppuccin-Mocha lesson applied — pastels _only_ work on dark, so the
light mode darkens and saturates instead of trying to reuse the lavender.

---

## Contrast matrix — every fg × bg

WCAG: **AAA** ≥7 · **AA** ≥4.5 · **AA-large** ≥3 (≥18px/UI only) · **fail** <3.

### Dark (hero)

| fg \ bg   | `bg` #14151f | `surface` #1d1f2c | `overlay` #282b3c |
| --------- | ------------ | ----------------- | ----------------- |
| `text`    | 13.23 AAA    | 11.91 AAA         | 10.20 AAA         |
| `muted`   | 6.33 AA      | 5.70 AA           | 4.88 AA           |
| `accent`  | 7.79 AAA     | 7.02 AAA          | 6.01 AA           |
| `success` | 10.16 AAA    | 9.15 AAA          | 7.83 AAA          |
| `warning` | 9.85 AAA     | 8.87 AAA          | 7.59 AAA          |
| `error`   | 7.37 AAA     | 6.63 AA           | 5.68 AA           |
| `info`    | 8.58 AAA     | 7.73 AAA          | 6.61 AA           |

### Light

| fg \ bg   | `bg` #e9eaf2 | `surface` #dfe1ec | `overlay` #d2d5e4 |
| --------- | ------------ | ----------------- | ----------------- |
| `text`    | 13.63 AAA    | 12.55 AAA         | 11.19 AAA         |
| `muted`   | 5.55 AA      | 5.11 AA           | 4.56 AA           |
| `accent`  | 5.42 AA      | 4.98 AA           | 4.45 AA-large     |
| `success` | 5.01 AA      | 4.61 AA           | 4.11 AA-large     |
| `warning` | 5.16 AA      | 4.75 AA           | 4.24 AA-large     |
| `error`   | 4.83 AA      | 4.45 AA-large     | 3.97 AA-large     |
| `info`    | 5.02 AA      | 4.62 AA           | 4.12 AA-large     |

**Reading the table.** The dark mode is exceptional — nearly all AAA. The light
mode clears AA for every fg on `bg` and `surface`; AA-large cells are confined to
`overlay` (semantic-on-third-bg), where these colors should be icons/borders
anyway. As always, status _messages_ use `--text` with a colored icon, not the
semantic color as body text.

---

## CSS custom properties (copy-paste)

Dark-first: dark is the `:root` default, light is the opt-in. This matches the
proposal's intent and means a no-JS, no-flash dark experience out of the box.

```css
:root {
  /* ── Night Scholar — dark (default) ───────────────────────── */
  --bg: oklch(20% 0.02 280); /* #14151f */
  --surface: oklch(24.3% 0.025 277.6); /* #1d1f2c */
  --overlay: oklch(29.4% 0.031 276.5); /* #282b3c */
  --muted: oklch(68.3% 0.052 276.1); /* #9097ba */
  --text: oklch(89.5% 0.032 277.9); /* #d7dbf2 */
  --accent: oklch(74.8% 0.128 295.6); /* #b49cf5 */
  --success: oklch(80.2% 0.126 133.2); /* #9ed07a */
  --warning: oklch(80.6% 0.119 81.9); /* #e6b860 */
  --error: oklch(73.8% 0.132 8.9); /* #f08599 */
  --info: oklch(76.1% 0.091 244.8); /* #7fb8e8 */
}

@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    /* ── Night Scholar — light (understudy) ───────────────── */
    --bg: oklch(93.9% 0.011 280.5); /* #e9eaf2 */
    --surface: oklch(91.1% 0.015 277.8); /* #dfe1ec */
    --overlay: oklch(87.5% 0.021 276.9); /* #d2d5e4 */
    --muted: oklch(47.7% 0.044 276.4); /* #565b76 */
    --text: oklch(24.4% 0.029 275.3); /* #1c1f2e */
    --accent: oklch(50.5% 0.209 290.5); /* #6a3fd0 */
    --success: oklch(48.8% 0.124 139.6); /* #357025 */
    --warning: oklch(49.7% 0.105 74.7); /* #855800 */
    --error: oklch(53.2% 0.187 15); /* #c02748 */
    --info: oklch(50.3% 0.15 258.9); /* #2861b8 */
  }
}

/* Explicit user choice wins over OS preference. */
[data-theme="light"] {
  --bg: oklch(93.9% 0.011 280.5);
  --surface: oklch(91.1% 0.015 277.8);
  --overlay: oklch(87.5% 0.021 276.9);
  --muted: oklch(47.7% 0.044 276.4);
  --text: oklch(24.4% 0.029 275.3);
  --accent: oklch(50.5% 0.209 290.5);
  --success: oklch(48.8% 0.124 139.6);
  --warning: oklch(49.7% 0.105 74.7);
  --error: oklch(53.2% 0.187 15);
  --info: oklch(50.3% 0.15 258.9);
}
```

---

## Preview — blog post + code block

### Dark (hero)

```
┌──────────────────────────────────────────────────────────────┐
│  ▓▓ #14151f rich blue-black ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│                                                                │
│   Compilers at Midnight           ← #d7dbf2 text, AAA 13.2:1   │
│   ──────────────────                                           │
│   Posted 2026-06-19 · 12 min read ← #9097ba muted, AA 6.3:1    │
│                                                                │
│   A parser is just a function that turns a flat stream of      │
│   tokens into a tree. The purple [recursive descent] link      │
│   is the same Journey purple, re-lit to glow on the dark       │
│   field instead of sinking into it.                            │
│                  └─ #b49cf5 accent, AAA 7.8:1                  │
│                                                                │
│   ┌── #1d1f2c surface (elevation by lightness) ────────┐      │
│   │  fn parse_expr(&mut self) -> Expr {  // comment     │      │
│   │      let lhs = self.parse_term();    // success 9.2 │      │
│   │      while self.eat(Plus) {          // warning 8.9 │      │
│   │          ...                         // error  6.6  │      │
│   │      }                                              │      │
│   └──────────────────────────────────────────────────────┘     │
│                                                                │
│   ⚠ warning #e6b860   ✓ success #9ed07a   ✕ error #f08599      │
└──────────────────────────────────────────────────────────────┘
```

### Light (understudy)

```
┌──────────────────────────────────────────────────────────────┐
│  ░░ #e9eaf2 cool paper ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│                                                                │
│   Compilers at Midnight           ← #1c1f2e text, AAA 13.6:1   │
│   ──────────────────                                           │
│   Posted 2026-06-19 · 12 min read ← #565b76 muted, AA 5.6:1    │
│                                                                │
│   The same purple [recursive descent] link, darkened and       │
│   saturated for the light background — pastels can't carry      │
│   contrast on paper, so light mode commits to a deep violet.   │
│                  └─ #6a3fd0 accent, AA 5.4:1                   │
│                                                                │
│   ┌── #dfe1ec surface ───────────────────────────────────┐    │
│   │  fn parse_expr(&mut self) -> Expr {  // comment muted │    │
│   │      let lhs = self.parse_term();    // success 5.0   │    │
│   │      while self.eat(Plus) { ... }    // warning 5.2   │    │
│   └──────────────────────────────────────────────────────┘     │
│                                                                │
│   ⚠ warning #855800   ✓ success #357025   ✕ error #c02748      │
└──────────────────────────────────────────────────────────────┘
```

---

## Honest trade-offs

- **+** Best dark mode of the three — rich, deep, every accent AA+, mostly AAA. Genuinely pleasant for long night sessions.
- **+** Keeps the existing Journey purple as the brand, so it's the least disruptive migration from current tokens.
- **+** Bright pastel accents on dark are vivid without being neon (chroma kept ≤0.13).
- **−** Light mode is deliberately secondary; it's accessible but cooler/flatter than Proposal A or C's warm light. If you read a lot in daylight, this is the weakest light mode of the three.
- **−** The cool blue-black bg has _less_ "warm personality" than the brief's stated direction — this proposal trades warmth for depth and night-comfort.
- **−** Light-mode `error` on `surface`/`overlay` dips to AA-large; keep error _text_ in `--text` with a red icon.
