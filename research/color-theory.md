# Color Theory for This Design System

A working reference for the personal design system behind `journey.atalariq.dev`,
the portfolio, and the research site. Opinionated on purpose. Every number here
was computed with `tools/color.py`, not guessed.

The three base tokens this whole document orbits around:

| Token                     | HSL                | Hex       | OKLCH                      | Relative luminance |
| ------------------------- | ------------------ | --------- | -------------------------- | ------------------ |
| Light bg (warm white)     | `hsl(40 30% 98%)`  | `#fbfaf8` | `oklch(98.7% 0.003 84.6)`  | 0.9602             |
| Dark bg (cool blue-black) | `hsl(225 18% 11%)` | `#171a21` | `oklch(21.7% 0.015 270.6)` | 0.0101             |
| Accent (purple)           | `hsl(255 70% 55%)` | `#643cdd` | `oklch(50.6% 0.227 286.6)` | 0.1114             |

---

## 1. HSL vs OKLCH vs HEX

### What each one is

**HEX** (`#643cdd`) is just three 8-bit sRGB channels (R, G, B) written in
hexadecimal. It is a storage format, not a thinking format. You cannot look at
`#643cdd` and predict what `#7a52e0` does to it. Fine as a final output; useless
for reasoning about relationships.

**HSL** (`hsl(255 70% 55%)`) is a cylindrical re-projection of _the same_ sRGB
cube: Hue (angle 0–360), Saturation (0–100%), Lightness (0–100%). It is
intuitive — "more saturated", "lighter" — which is why it is everywhere. Its
fatal flaw is that none of its axes are perceptual. "Lightness" in HSL is a
geometric midpoint of the RGB cube, **not** how bright the color looks to a human
eye.

**OKLCH** (`oklch(50.6% 0.227 286.6)`) is the cylindrical form of Björn
Ottosson's OKLab (2020), a color space engineered so that equal numeric steps
correspond to _equal perceived_ steps. L = perceptual Lightness (0–1 or 0–100%),
C = Chroma (colorfulness, unbounded but practically ~0–0.37), H = Hue angle.
Same idea as HSL's cylinder, but the axes mean what they say.

### Why perceptual uniformity matters: the worked example

Take four maximally-saturated hues, all at HSL lightness 50%. By HSL's logic they
should be equally bright. They are not even close:

| Color  | HSL                 | OKLCH (real perceived L)   | Relative luminance |
| ------ | ------------------- | -------------------------- | ------------------ |
| Yellow | `hsl(60 100% 50%)`  | `oklch(96.8% 0.211 109.8)` | 0.9278             |
| Green  | `hsl(120 100% 50%)` | `oklch(86.6% 0.295 142.5)` | 0.7152             |
| Red    | `hsl(0 100% 50%)`   | `oklch(62.8% 0.258 29.2)`  | 0.2126             |
| Blue   | `hsl(240 100% 50%)` | `oklch(45.2% 0.313 264.1)` | 0.0722             |

Read the middle column. HSL swears these are all "50% light." OKLCH (which models
the eye) says yellow is **96.8%** light and blue is **45.2%** light — a perceptual
gap of more than 2x. The relative-luminance column confirms it physically: yellow
reflects ~13x more light energy than blue. HSL lightness is a lie that happens to
be self-consistent.

### Practical consequences for tokens

This is not academic. It breaks three things you do constantly:

1. **Generating tints/shades.** Step HSL lightness in even increments and your
   ramp will look bunched in the lights and starved in the darks (or vice versa),
   differently _per hue_. Step OKLCH L in even increments and every step looks
   evenly spaced, on any hue. A 9-step gray ramp built in OKLCH just works; in
   HSL you hand-tune it.

2. **Accent ramps.** If you want `accent-400 … accent-700` to feel like a smooth
   gradient, OKLCH gives it to you by moving L while holding C and H. In HSL the
   "same" hue darkens unevenly and often muddies.

3. **Hue shifting without lightness drift.** Want a warm and a cool variant of the
   accent at the _same apparent brightness_? In OKLCH you change H and keep L
   fixed — done. In HSL, rotating hue silently changes how light the swatch looks
   (the table above is proof), so your "same-weight" accents won't match.

### Recommendation for THIS system: author in OKLCH

Take the stance. **Define the canonical palette in OKLCH custom properties.**

Reasons specific to this system:

- The system explicitly values "warm/readable, not generic Bootstrap" and uses
  _plain CSS custom properties, no build-time token transformer_. OKLCH is native
  CSS — `oklch()` shipped in all major browsers in 2023 (Chrome/Edge 111, Safari
  15.4, Firefox 113). There is nothing to transpile. This is the one place where
  the "no build step" constraint actually _favors_ the more correct space, because
  you no longer need a Sass/Style-Dictionary pipeline to fake perceptual ramps.
- Light/dark parity (Section 5) is dramatically easier when L means perceived
  lightness, because "make the accent readable on dark" becomes "raise L," full
  stop, instead of a guess-and-check on HSL.
- The author is a developer/student building a _personal, long-lived_ system.
  Learning OKLCH once pays off across the digital garden, portfolio, and research
  site forever. This is exactly the audience that should invest in the right tool.

Concession to familiarity: keep an HSL (and hex) column in the token table as
_documentation_, the way this very file does. Read in HSL, ship in OKLCH. If you
ever need an IE-era fallback (you don't, for a personal 2026 site), `@supports`
the OKLCH and let hex be the fallback — but I would not bother.

```css
:root {
  /* canonical: OKLCH. hex kept as comment for eyeballing. */
  --bg: oklch(98.7% 0.003 84.6); /* #fbfaf8 warm white */
  --text: oklch(21.7% 0.015 270.6); /* #171a21 cool blue-black */
  --accent: oklch(50.6% 0.227 286.6); /* #643cdd purple */
}
```

---

## 2. The 60-30-10 Rule

### Origin

It comes from interior design, where a room reads as harmonious when one color
dominates ~60% of the space (walls), a secondary covers ~30% (furniture,
upholstery), and an accent punctuates ~10% (cushions, art, a lamp). The ratios
aren't magic; they encode a hierarchy — one thing leads, one supports, one points.
It transfers to UI because screens have the same problem: too many co-equal colors
and the eye finds no anchor.

### Mapping to semantic UI roles

| Bucket    | ~Share | Interior origin | UI role               | What lives here                                                                |
| --------- | ------ | --------------- | --------------------- | ------------------------------------------------------------------------------ |
| Dominant  | 60%    | Walls           | Background / surfaces | page bg, card/panel surfaces, large empty regions                              |
| Secondary | 30%    | Furniture       | Text & structure      | body text, headings, muted text, borders, dividers, icons                      |
| Accent    | 10%    | Cushions/art    | Highlights            | links, primary buttons, focus rings, active states, selection, code highlights |

The ratios are a _budget_, not a measurement. On a reading-focused site the 60%
and 30% are doing almost all the work and that is correct — text plus background
is the product.

### Concrete buckets for a reading-focused site

**Dominant (~60%) — the warm white / cool blue-black.**
This is `--bg` and its near-neighbors (one or two surface levels). On a digital
garden the background _is_ most of the screen. Keep it boring and warm; it should
disappear.

**Secondary (~30%) — the text scale.**
The blue-black `--text` for body, plus a muted variant for metadata, captions,
and "less important" prose, plus borders. Suggested members, with real contrast
on the warm light bg:

| Role       | HSL                | Hex       | OKLCH                      | Contrast on `#fbfaf8`  |
| ---------- | ------------------ | --------- | -------------------------- | ---------------------- |
| Body text  | `hsl(225 18% 11%)` | `#171a21` | `oklch(21.7% 0.015 270.6)` | 16.81:1 (AAA)          |
| Muted text | `hsl(225 12% 40%)` | `#5a6072` | `oklch(49.0% 0.030 270.7)` | 6.04:1 (AA)            |
| Border     | `hsl(40 15% 90%)`  | `#e9e7e2` | `oklch(92.8% 0.007 84.6)`  | (non-text, decorative) |

Note muted text is still 6.04:1 — comfortably AA. Resist the urge to make "muted"
mean "illegible gray."

**Accent (~10%) — the purple, used sparingly.**
`--accent` is for links, the focus ring, primary CTA, selection highlight. The
whole point is scarcity: if everything is purple, nothing is. On a reading site
you might spend most of your 10% budget just on inline links.

---

## 3. Contrast Ratios

### The actual formula

WCAG 2.x contrast is a ratio of _relative luminance_, not of HSL lightness or hue.
Two steps:

**Step 1 — linearize each sRGB channel** (undo the gamma curve), per channel
value `c` in [0,1]:

```
c_lin = c / 12.92                     if c <= 0.04045
c_lin = ((c + 0.055) / 1.055) ^ 2.4   otherwise
```

**Step 2 — relative luminance** is the weighted sum (the weights are the eye's
sensitivity: green dominates, blue barely registers):

```
L = 0.2126·R_lin + 0.7152·G_lin + 0.0722·B_lin
```

**Contrast ratio** between two colors, where `L1` is the lighter:

```
ratio = (L1 + 0.05) / (L2 + 0.05)
```

The `+0.05` models ambient flare; it caps the scale so pure black on pure white is
**21:1**, never infinity, and a color against itself is 1:1.

### What WCAG AA / AAA mean numerically

| Threshold | Normal text | Large text (≥18pt or ≥14pt bold) | UI components / graphics |
| --------- | ----------- | -------------------------------- | ------------------------ |
| AA        | 4.5:1       | 3:1                              | 3:1                      |
| AAA       | 7:1         | 4.5:1                            | (no AAA tier defined)    |

This system's stated floor is **WCAG AA**, i.e. 4.5:1 for body text. Aim for AAA
(7:1) on the primary text pair, which costs nothing here since it already clears 16:1.

### Worked example (real numbers)

Body text on the warm light background:

- `L_bg` (`#fbfaf8`) = 0.9602
- `L_text` (`#171a21`) = 0.0101
- ratio = (0.9602 + 0.05) / (0.0101 + 0.05) = 1.0102 / 0.0601 = **16.81:1**

That is AAA with enormous headroom — exactly what you want for a reading-first
site. The accent tells a more interesting story:

| Pair                           | Ratio      | Normal-text grade   |
| ------------------------------ | ---------- | ------------------- |
| `--text` on `--bg` (light)     | 16.81:1    | AAA                 |
| `--accent` on `--bg` (light)   | 6.26:1     | AA (just under AAA) |
| `--text`/`--bg` swapped (dark) | 16.81:1    | AAA                 |
| `--accent` on `--bg` (dark)    | **2.68:1** | **fail**            |

The last row is the cliff: the _same_ purple that reads fine on light
(6.26:1) fails outright on dark (2.68:1). That is the entire argument for
Section 5. Note also that accent-on-light at 6.26:1 passes AA for body but misses
AAA — fine for links/buttons, but do not set long body copy in accent purple.

---

## 4. Color Temperature in UI

### Warm vs cool, and what the evidence actually says

Be honest here, because this area is thick with marketing folklore.

**What is reasonably evidence-based:**

- **Glare and harsh-contrast fatigue are real.** A pure-white (`#ffffff`) page is
  a maximal-luminance light source pointed at the reader's eyes. Dropping
  luminance slightly and warming it (toward paper) reduces the raw light energy
  and softens the black-on-white contrast edge. Our warm white sits at luminance
  0.9602 vs pure white's 1.0 — a small, deliberate step off the maximum, plus a
  warm hue that reads as "paper" rather than "lightbox."
- **Pure black text on pure white maxes out at 21:1.** More contrast is not always
  more comfortable for sustained reading; very high contrast can cause visual
  buzzing/halation, especially for some readers. The warm pairing here still hits
  16.81:1 — far past AA, but off the 21:1 extreme.

**What is weaker than marketed (folklore territory):**

- **Blue-light / f.lux "saves your eyes / sleep" claims.** The strong versions
  ("blue light damages your retina from screens," "warm screens fix your sleep")
  are not well supported. The melatonin/circadian literature is real but the
  _effect size from screen color temperature at typical brightness_ is modest and
  contested; recent controlled work has failed to find that screen warming
  meaningfully improves sleep. Treat warmth as an **aesthetic and glare-comfort**
  choice, not a medical one. Don't sell it as health.
- **"Warm = friendly, cool = professional" psychology.** Directionally plausible,
  culturally loaded, not a law. Use it as taste, not science.

### Why this system chose warm-light + cool-dark

This pairing is deliberate and defensible _on the honest grounds_:

- **Warm light bg** (`hsl(40 30% 98%)`, that 40° hue) reads as paper/parchment.
  It supports the "warm/readable, not generic Bootstrap" personality and trims a
  sliver of glare off pure white — comfort + identity, not a health claim.
- **Cool dark bg** (`hsl(225 18% 11%)`, blue-black at 225°) is the right call for
  dark mode for a perceptual reason, not vibes: warm _dark_ colors tend to look
  muddy/brown, while a slight blue cast reads as a clean, deep "night" and keeps
  the surface feeling like a void the text floats on. It is also _not_ pure black
  (Section 5 explains why that matters).

So the system isn't symmetric (warm light / warm dark) — it's warm where warmth
helps (paper feel in light mode) and cool where coolness helps (clean depth in
dark mode). That asymmetry is the correct instinct.

---

## 5. One Palette, Two Modes (Not Just Inverted)

Naive dark mode = "flip the colors." It always looks cheap, and here is exactly
why, with this system's real numbers.

### Why naive inversion fails

1. **Saturated accents go neon on dark.** Color looks more intense against a dark
   field. Worse, the _contrast_ math turns on you: `--accent` purple is 6.26:1 on
   light but only **2.68:1** on the dark bg — it simultaneously looks louder _and_
   reads worse. Inversion gives you the worst of both.

2. **Pure-black background causes halation/smearing.** On `#000000`, white text at
   the full 21:1 ratio "blooms" — the glyphs smear, especially on OLED and for
   astigmatic/light-sensitive readers. That is why the dark bg here is
   `#171a21` (luminance 0.0101), not `#000`. The text pair still lands at 16.81:1
   — plenty — without sitting at the harsh 21:1 extreme.

3. **Shadows don't invert.** In light mode, depth = darker shadow. Invert that and
   you get glowing white shadows, which read as nonsense. Dark mode needs a
   _different_ depth mechanic entirely (next point).

### Elevation by lightness (the dark-mode depth trick)

In light mode, things "rise" by casting shadow. In dark mode, **things rise by
getting lighter** — closer surfaces catch more light. Build a small ramp off the
cool dark base, raising OKLCH L (~+4% per level) while letting chroma ease down:

| Level | Use              | HSL                | Hex       | OKLCH                      |
| ----- | ---------------- | ------------------ | --------- | -------------------------- |
| L0    | page background  | `hsl(225 18% 11%)` | `#171a21` | `oklch(21.7% 0.015 270.6)` |
| L1    | card / surface   | `hsl(225 16% 15%)` | `#20232c` | `oklch(25.8% 0.018 270.6)` |
| L2    | raised / popover | `hsl(225 14% 19%)` | `#2a2d37` | `oklch(29.8% 0.019 270.7)` |
| L3    | overlay / modal  | `hsl(225 12% 24%)` | `#363a45` | `oklch(34.8% 0.020 270.8)` |

Notice the OKLCH L marches in clean ~4% steps — that even spacing is _why_ you
author in OKLCH (Section 1). The same ramp eyeballed in HSL would need fudging.

### Desaturate + re-light the accent per mode

The accent must be a different _value_ in each mode while staying the _same color
identity_ (same hue family). The fix is to raise lightness (and usually nudge
chroma down) for dark mode:

| Mode  | Accent    | HSL                | Hex       | OKLCH                      | Contrast on its bg |
| ----- | --------- | ------------------ | --------- | -------------------------- | ------------------ |
| Light | base      | `hsl(255 70% 55%)` | `#643cdd` | `oklch(50.6% 0.227 286.6)` | 6.26:1 (AA)        |
| Dark  | lightened | `hsl(255 80% 70%)` | `#9475f0` | `oklch(64.9% 0.177 292.3)` | 5.05:1 (AA)        |

Same hue family (~286–292° in OKLCH, ~255° in HSL — recognizably "the purple"),
but the dark-mode version is raised from L 50.6% to 64.9% and chroma trimmed
0.227 → 0.177. Result: it clears AA on dark (5.05:1) instead of failing (2.68:1),
and it reads as a calm accent rather than a neon stripe. **This single move is the
difference between a designed dark mode and an inverted one.**

### Keep hue identity across modes

The thing that must stay constant is _which color it is_. Across both accent rows
the hue barely moves (OKLCH H ~286–292). Lightness and chroma are the knobs;
**hue is the brand.** If the purple becomes blue or magenta when you switch modes,
you've lost identity. Lock H, move L and C.

### Opinionated dark-mode guidance for this system

- **Never `#000`.** Base dark on `#171a21` (the cool blue-black). Halation matters
  more than the bragging rights of 21:1.
- **Depth = lightness, not shadow.** Use the L0–L3 ramp above. Shadows in dark
  mode, if any, should be subtle and combined with a lighter surface, never used
  alone.
- **Two accent tokens, not one.** Ship `--accent` (light) and `--accent-dark`
  (raised L, trimmed C), swapped under the `prefers-color-scheme` / `[data-theme]`
  query. Don't reuse one accent across both modes — the 2.68:1 failure is proof
  it can't.
- **Muted text gets lighter on dark, and that's fine.** For reference, a dark-mode
  muted token `hsl(220 12% 70%)` / `#a9afbc` / `oklch(75.4% 0.019 264.5)` lands at
  **7.97:1** on the dark bg (AAA) — you have room to make "muted" genuinely
  readable.
- **Author every token in OKLCH so cross-mode adjustments are arithmetic, not
  vibes.** "Make it work on dark" should mean "+~14% L, −~0.05 C," a thing you can
  reason about — which is the whole reason Section 1 picked OKLCH.
