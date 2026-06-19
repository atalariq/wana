# Proposal A — "Warm Ink"

> **Philosophy.** Ink on warm paper. The light mode is the hero: a parchment
> background and warm near-black ink, the way a good book or a Flexoki/Everforest
> editor feels — calm, low-glare, made for staring at prose for an hour. The dark
> mode is a _warm_ dark (brown-black, not blue-black), so the personality survives
> the switch instead of turning generic-cool. Accent is a muted teal — the color
> of old fountain-pen ink that has dried slightly green.

This is the proposal to pick if **reading comfort** is the top priority and the
sites lean prose-heavy (the digital garden, the research write-ups). It is the
warmest, softest, most "analog" of the three.

All numbers computed by `tools/color.py`. Regenerate with
`python3 tools/proposal_matrix.py A`.

---

## Light palette (the hero)

| Role            | Hex       | HSL                    | OKLCH                      | Contrast vs `bg` |
| --------------- | --------- | ---------------------- | -------------------------- | ---------------- |
| `bg` (paper)    | `#faf4e6` | `hsl(42 66.7% 94.1%)`  | `oklch(96.8% 0.020 87.5)`  | —                |
| `surface`       | `#f1e9d5` | `hsl(43 50% 89%)`      | `oklch(93.5% 0.028 88.8)`  | —                |
| `overlay`       | `#e7ddc4` | `hsl(43 42.2% 83.7%)`  | `oklch(89.9% 0.035 88.8)`  | —                |
| `muted` (text)  | `#6b6557` | `hsl(42 10.3% 38%)`    | `oklch(50.8% 0.023 87.6)`  | 5.28:1 AA        |
| `text` (ink)    | `#211d17` | `hsl(36 17.9% 11%)`    | `oklch(23.3% 0.013 78.0)`  | 15.28:1 AAA      |
| `accent` (teal) | `#1d6b7a` | `hsl(190 61.6% 29.6%)` | `oklch(48.9% 0.076 213.5)` | 5.57:1 AA        |
| `success`       | `#5a7012` | `hsl(74 72.3% 25.5%)`  | `oklch(51.0% 0.117 122.7)` | 5.09:1 AA        |
| `warning`       | `#8f5f00` | `hsl(40 100% 28%)`     | `oklch(52.4% 0.111 74.7)`  | 5.03:1 AA        |
| `error`         | `#b3261e` | `hsl(3 71.3% 41%)`     | `oklch(50.1% 0.178 28.7)`  | 5.96:1 AA        |
| `info`          | `#2a5ea8` | `hsl(215 60% 41.2%)`   | `oklch(48.6% 0.131 257.7)` | 5.86:1 AA        |

## Dark palette (warm dark, not blue-black)

| Role            | Hex       | HSL                    | OKLCH                      | Contrast vs `bg` |
| --------------- | --------- | ---------------------- | -------------------------- | ---------------- |
| `bg`            | `#1a1714` | `hsl(30 13% 9%)`       | `oklch(20.7% 0.008 67.4)`  | —                |
| `surface`       | `#242019` | `hsl(38 18% 12%)`      | `oklch(24.6% 0.014 81.6)`  | —                |
| `overlay`       | `#2f2a21` | `hsl(39 17.5% 15.7%)`  | `oklch(28.7% 0.017 82.2)`  | —                |
| `muted` (text)  | `#a39a86` | `hsl(41 13.6% 58.2%)`  | `oklch(68.8% 0.030 86.7)`  | 6.39:1 AA        |
| `text`          | `#ece3cf` | `hsl(41 43.3% 86.9%)`  | `oklch(91.8% 0.028 86.6)`  | 13.99:1 AAA      |
| `accent` (teal) | `#5cb6c4` | `hsl(188 46.8% 56.5%)` | `oklch(72.6% 0.088 208.7)` | 7.60:1 AAA       |
| `success`       | `#a7bd5a` | `hsl(73 42.9% 54.7%)`  | `oklch(76.1% 0.128 119.9)` | 8.56:1 AAA       |
| `warning`       | `#e0a83a` | `hsl(40 72.8% 55.3%)`  | `oklch(76.5% 0.138 80.4)`  | 8.36:1 AAA       |
| `error`         | `#e07b6a` | `hsl(9 65.6% 64.7%)`   | `oklch(69.1% 0.129 30.7)`  | 6.13:1 AA        |
| `info`          | `#7fb0e0` | `hsl(210 61% 68.8%)`   | `oklch(74.1% 0.087 248.6)` | 7.81:1 AAA       |

The accent keeps its **hue identity** (~209–214° OKLCH teal) across modes but is
re-lit: L 48.9% on light → 72.6% on dark, chroma nudged up to stay visible. Same
move Flexoki uses; this is "designed dark mode," not inversion.

---

## Contrast matrix — every fg × bg

WCAG: **AAA** ≥7 · **AA** ≥4.5 · **AA-large** ≥3 (≥18px/UI only) · **fail** <3.

### Light

| fg \ bg   | `bg` #faf4e6 | `surface` #f1e9d5 | `overlay` #e7ddc4 |
| --------- | ------------ | ----------------- | ----------------- |
| `text`    | 15.28 AAA    | 13.85 AAA         | 12.40 AAA         |
| `muted`   | 5.28 AA      | 4.79 AA           | 4.29 AA-large     |
| `accent`  | 5.57 AA      | 5.05 AA           | 4.52 AA           |
| `success` | 5.09 AA      | 4.61 AA           | 4.13 AA-large     |
| `warning` | 5.03 AA      | 4.56 AA           | 4.08 AA-large     |
| `error`   | 5.96 AA      | 5.40 AA           | 4.84 AA           |
| `info`    | 5.86 AA      | 5.32 AA           | 4.76 AA           |

### Dark

| fg \ bg   | `bg` #1a1714 | `surface` #242019 | `overlay` #2f2a21 |
| --------- | ------------ | ----------------- | ----------------- |
| `text`    | 13.99 AAA    | 12.70 AAA         | 11.16 AAA         |
| `muted`   | 6.39 AA      | 5.81 AA           | 5.10 AA           |
| `accent`  | 7.60 AAA     | 6.90 AA           | 6.07 AA           |
| `success` | 8.56 AAA     | 7.77 AAA          | 6.83 AA           |
| `warning` | 8.36 AAA     | 7.59 AAA          | 6.67 AA           |
| `error`   | 6.13 AA      | 5.57 AA           | 4.89 AA           |
| `info`    | 7.81 AAA     | 7.09 AAA          | 6.23 AA           |

**Reading the table.** Every text/muted/accent pair clears AA on `bg` and
`surface`. The handful of AA-large cells are semantic colors on `overlay` (a
rare third-level background) — fine, because semantic colors should carry
**icons, borders, and large labels**, with message _body_ text always set in
`--text` (see `research/accessibility.md` §4). Don't set a 14px success
sentence in `--success`; set it in `--text` and put a ✓ in `--success`.

---

## CSS custom properties (copy-paste)

Authored in OKLCH (canonical), hex kept as a comment for eyeballing — per
`research/color-theory.md`'s recommendation. Light is the default; dark applies
under both the OS preference and an explicit `[data-theme]` override.

```css
:root {
  /* ── Warm Ink — light (paper) ───────────────────────────── */
  --bg: oklch(96.8% 0.02 87.5); /* #faf4e6 */
  --surface: oklch(93.5% 0.028 88.8); /* #f1e9d5 */
  --overlay: oklch(89.9% 0.035 88.8); /* #e7ddc4 */
  --muted: oklch(50.8% 0.023 87.6); /* #6b6557 */
  --text: oklch(23.3% 0.013 78); /* #211d17 */
  --accent: oklch(48.9% 0.076 213.5); /* #1d6b7a */
  --success: oklch(51% 0.117 122.7); /* #5a7012 */
  --warning: oklch(52.4% 0.111 74.7); /* #8f5f00 */
  --error: oklch(50.1% 0.178 28.7); /* #b3261e */
  --info: oklch(48.6% 0.131 257.7); /* #2a5ea8 */
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* ── Warm Ink — dark (warm brown-black) ───────────────── */
    --bg: oklch(20.7% 0.008 67.4); /* #1a1714 */
    --surface: oklch(24.6% 0.014 81.6); /* #242019 */
    --overlay: oklch(28.7% 0.017 82.2); /* #2f2a21 */
    --muted: oklch(68.8% 0.03 86.7); /* #a39a86 */
    --text: oklch(91.8% 0.028 86.6); /* #ece3cf */
    --accent: oklch(72.6% 0.088 208.7); /* #5cb6c4 */
    --success: oklch(76.1% 0.128 119.9); /* #a7bd5a */
    --warning: oklch(76.5% 0.138 80.4); /* #e0a83a */
    --error: oklch(69.1% 0.129 30.7); /* #e07b6a */
    --info: oklch(74.1% 0.087 248.6); /* #7fb0e0 */
  }
}

/* Explicit user choice wins over OS preference. */
[data-theme="dark"] {
  --bg: oklch(20.7% 0.008 67.4);
  --surface: oklch(24.6% 0.014 81.6);
  --overlay: oklch(28.7% 0.017 82.2);
  --muted: oklch(68.8% 0.03 86.7);
  --text: oklch(91.8% 0.028 86.6);
  --accent: oklch(72.6% 0.088 208.7);
  --success: oklch(76.1% 0.128 119.9);
  --warning: oklch(76.5% 0.138 80.4);
  --error: oklch(69.1% 0.129 30.7);
  --info: oklch(74.1% 0.087 248.6);
}
```

---

## Preview — blog post + code block

### Light (paper)

```
┌──────────────────────────────────────────────────────────────┐
│  ░░ #faf4e6 warm paper ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│                                                                │
│   On Spaced Repetition            ← #211d17 ink, AAA 15.3:1    │
│   ─────────────────                                            │
│   Posted 2026-06-19 · 7 min read  ← #6b6557 muted, AA 5.3:1    │
│                                                                │
│   Memory is not a bucket you fill. It is a muscle that         │
│   strengthens against forgetting. The trick is to revisit      │
│   a fact just as it begins to fade — a teal link like          │
│   [the forgetting curve] punctuates the prose.                 │
│                  └─ #1d6b7a accent, underlined, AA 5.6:1       │
│                                                                │
│   ┌── #f1e9d5 surface ──────────────────────────────────┐     │
│   │  def review(card, grade):           # comment muted  │     │
│   │      if grade >= 3:                                   │     │
│   │          card.interval *= card.ease  # success 5.1:1 │     │
│   │      else:                                            │     │
│   │          card.interval = 1           # error 6.0:1   │     │
│   └──────────────────────────────────────────────────────┘     │
│                                                                │
│   ⚠ warning #8f5f00   ✓ success #5a7012   ✕ error #b3261e      │
└──────────────────────────────────────────────────────────────┘
```

### Dark (warm)

```
┌──────────────────────────────────────────────────────────────┐
│  ▓▓ #1a1714 warm brown-black ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│                                                                │
│   On Spaced Repetition            ← #ece3cf text, AAA 14.0:1   │
│   ─────────────────                                            │
│   Posted 2026-06-19 · 7 min read  ← #a39a86 muted, AA 6.4:1    │
│                                                                │
│   Memory is not a bucket you fill. The same teal accent        │
│   [the forgetting curve] now glows softly instead of           │
│   sinking — re-lit for the dark surface.                       │
│                  └─ #5cb6c4 accent, AAA 7.6:1                  │
│                                                                │
│   ┌── #242019 surface (elevation by lightness) ─────────┐     │
│   │  def review(card, grade):           # comment muted  │     │
│   │      if grade >= 3:                                   │     │
│   │          card.interval *= card.ease  # success 8.6:1 │     │
│   │      else:                                            │     │
│   │          card.interval = 1           # error 6.1:1   │     │
│   └──────────────────────────────────────────────────────┘     │
│                                                                │
│   ⚠ warning #e0a83a   ✓ success #a7bd5a   ✕ error #e07b6a      │
└──────────────────────────────────────────────────────────────┘
```

---

## Honest trade-offs

- **+** Warmest, most paper-like of the three; best for sustained prose. Both modes keep a distinct personality (warm light _and_ warm dark).
- **+** Teal accent is calm and reads as "ink," not "brand color" — pairs well with serious writing.
- **−** The warm dark mode is unusual; if you're used to cool dark editors it can feel slightly "sepia." Some will love it, some won't.
- **−** Teal accent is close in hue to `info` blue — keep `info` for system messages only so they don't muddle.
- **−** Light-mode semantic colors sit in the 5:1 range (AA, not AAA) — intentional (high-chroma earth tones), but lean on icons for status, never color alone.
