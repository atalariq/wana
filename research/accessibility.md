# Accessibility — Contrast, Dark Mode, and Color Vision

Research notes for Atalariq's personal design system. Target: **WCAG 2.1 AA
minimum, AAA where it's free**. Stack is Astro + plain CSS custom properties.
All ratios below are real numbers from `tools/color.py`, not eyeballed.

The palette this system uses is Flexoki-derived (warm off-black ink on warm
paper). The opinionated takeaway is at the bottom: **a token-level contrast
gate in CI + one manual keyboard/screen-reader pass per site.** Everything
else is the reasoning.

---

## 1. WCAG 2.1 contrast requirements

Contrast is the ratio between the relative luminance of foreground and
background, expressed as `N:1`. White on black is the maximum, `21:1`. Same
color on itself is the minimum, `1:1`.

| Content                                 | AA        | AAA              | WCAG SC       |
| --------------------------------------- | --------- | ---------------- | ------------- |
| Normal text                             | **4.5:1** | **7:1**          | 1.4.3 / 1.4.6 |
| Large text                              | **3:1**   | **4.5:1**        | 1.4.3 / 1.4.6 |
| UI components & graphical objects       | **3:1**   | (no AAA defined) | 1.4.11        |
| Incidental / disabled / decorative      | exempt    | exempt           | 1.4.3 note    |
| Logotypes (text that is part of a logo) | exempt    | exempt           | 1.4.3 note    |

### What "large text" actually means

The 3:1 threshold only applies to genuinely large text. WCAG defines it as:

- **≥ 18pt** regular weight, **or**
- **≥ 14pt bold**.

The trap: WCAG's "pt" is the CSS reference pixel, where **1pt = 1.333px**. So:

| WCAG term    | px                   | rem (16px root) |
| ------------ | -------------------- | --------------- |
| 18pt regular | **24px**             | 1.5rem          |
| 14pt bold    | **18.66px ≈ 18.5px** | ~1.16rem        |

So body copy at 16px / 1rem is **always "normal text"** and needs 4.5:1. Don't
talk yourself into the 3:1 lane for paragraphs. Only headings, large display
type, and bold lead-ins qualify. In this system, treat **everything except
explicit display/heading tokens as normal text** and hold the 4.5:1 line.

### Non-text contrast (1.4.11) is the one people forget

3:1 applies to the _visual boundary_ of UI components and meaningful graphics:
input borders, focus rings, toggle states, button outlines, chart strokes,
icon glyphs that carry meaning. A 1px hairline border at `#e6e4d9` on `#fffcf0`
is invisible to 1.4.11 even though it "looks fine" to you. Borders that _only_
decorate are exempt; borders that _communicate_ (this is the editable field,
this is selected) must hit 3:1.

---

## 2. Testing contrast programmatically

### The math

WCAG contrast is a two-step calculation. First, **relative luminance** of an
sRGB color — linearize each channel, then weight by human luminance
sensitivity (we see green far more than blue):

```
channel_linear = c/12.92                    if c <= 0.04045
                 ((c+0.055)/1.055) ** 2.4   otherwise
L = 0.2126*R + 0.7152*G + 0.0722*B
```

Then the **ratio**:

```
contrast = (L_lighter + 0.05) / (L_darker + 0.05)
```

The `0.05` is the flare term modeling ambient screen reflection — it's why the
scale tops out at 21 instead of infinity.

This is implemented verbatim in **`tools/color.py`** — see
`_srgb_to_linear`, `relative_luminance`, and `contrast`. That file is the
project's source of truth; trust its numbers over any online checker, because
they should agree to the same formula but the tool is reproducible in CI.

```bash
python3 tools/color.py contrast "#100F0F" "#FFFCF0"
# ratio : 18.62:1   normal: AAA   large: AAA
```

### Batch-checking a palette

`tools/color.py table <colors.json>` renders a full foreground×background
contrast matrix as Markdown. The JSON is two maps:

```json
{
  "fg": { "tx": "#100F0F", "tx-muted": "#6F6E69", "red": "#AF3029" },
  "bg": { "paper": "#FFFCF0", "bg-2": "#F2F0E5" }
}
```

Each cell prints `ratio grade` (e.g. `18.62 AAA`). This is how you regenerate
the contrast tables in `research/` and `proposals/` whenever a token moves —
one command, every pair, no manual transcription.

### Real numbers for this palette (text on backgrounds)

| Pair                               | Ratio       | Normal | Note                          |
| ---------------------------------- | ----------- | ------ | ----------------------------- |
| `tx #100F0F` on `paper #FFFCF0`    | **18.62:1** | AAA    | primary light-mode body       |
| `tx #FFFCF0` on `bg #1C1B1A`       | **16.73:1** | AAA    | primary dark-mode body        |
| `tx-muted #6F6E69` on `paper`      | **4.97:1**  | AA     | passes, but barely            |
| `tx-muted #878580` on `bg #1C1B1A` | **4.67:1**  | AA     | passes, but barely            |
| pure `#000` on pure `#fff`         | 21.00:1     | AAA    | the thing to _avoid_ (see §3) |

### CI integration

Make contrast a build gate, not a vibe. The minimal version is a Python
wrapper around `tools/color.py` that asserts every declared (fg, bg, min-grade)
triple and exits non-zero on failure:

```python
# tools/contrast_gate.py  (sketch)
from color import contrast, wcag_grade
PAIRS = [
    ("#100F0F", "#FFFCF0", 4.5),   # body / paper
    ("#6F6E69", "#FFFCF0", 4.5),   # muted / paper
    ("#FFFCF0", "#1C1B1A", 4.5),   # body / dark
    ("#878580", "#1C1B1A", 4.5),   # muted / dark
]
fails = [(f,b,r) for f,b,min_ in PAIRS
         if (r := contrast(f,b)) < min_]
if fails:
    for f,b,r in fails: print(f"FAIL {f} on {b}: {r:.2f}")
    raise SystemExit(1)
```

Wire it into the Astro repo's `package.json` (`"a11y:contrast"`) and run it in
the same CI job as the build. The point is that **a token edit that breaks
contrast fails the PR**, before it ships to journey/portfolio/research.

---

## 3. Dark mode pitfalls

Dark mode is where personal design systems quietly fail AA. Concrete traps,
each with a fix:

### Pure black + pure white → halation

`#000` background with `#fff` text scores a perfect 21:1 and is the _wrong_
choice. On OLED especially, max-luminance white text on max-black bleeds
("halation"), the text appears to vibrate, and astigmatic readers get
afterimages. This system already does the right thing:

- **Background: off-black `#1C1B1A`** (warm, ~10% lightness), not `#000`.
- **Text: off-white `#FFFCF0`** (warm paper), not `#fff`.
- Result `16.73:1` — still solid AAA, far gentler on the eye.

Rule: in dark mode keep the bg in the **`#11`–`#1a`** range and the text a hair
below pure white. You lose nothing on contrast and gain readability.

### Over-saturated accents vibrate on dark

`#00FFFF` cyan on black is 16.75:1 — passes everything, looks terrible. High
chroma against near-black causes chromatic aberration / a glowing edge. Dark
mode wants accents that are **lighter and less saturated** than their light-mode
twins. Because OKLCH separates lightness from chroma, the move is: raise L,
drop C. This palette's dark-mode accents (e.g. red shifts `#AF3029` → `#D14D41`,
green `#66800B` → `#879A39`) do exactly this — lighter steps for dark surfaces.

### Muted text is the #1 real-world AA failure

"Secondary" / "muted" text is where almost every system breaks AA, because it's
designed by eye to look subordinate, and "subordinate enough" usually lands
below 4.5:1. This palette's muted tokens are deliberately tuned to _just_ clear
it:

| Token              | On             | Ratio  | Margin over 4.5 |
| ------------------ | -------------- | ------ | --------------- |
| `tx-muted #6F6E69` | paper          | 4.97:1 | +0.47           |
| `tx-muted #878580` | dark `#1C1B1A` | 4.67:1 | +0.17           |

Both pass — but the dark one has only **0.17 of headroom**. Any future darkening
of the muted token, or use on a slightly lighter surface (`bg-2`), can tip it
to fail. **Lock these in the CI gate** (§2) so they can't drift. Don't push
muted text any dimmer to chase aesthetics.

### Focus indicators disappear

A dark-blue focus ring on a dark surface fails 1.4.11 (needs 3:1 against its
background) and strands keyboard users. Fixes: use a **light/high-contrast ring
color in dark mode** (often the accent's light step, or the text color), give it
real thickness (`outline: 2px` + `outline-offset: 2px`), and never
`outline: none` without a visible replacement.

### Don't rely on elevation/shadow on dark

`box-shadow` is the light-mode way to separate cards from background; on near
black it's nearly invisible. In dark mode, separate surfaces with **a lighter
background step** (`bg` → `bg-2`) and/or a **1px border that itself meets 3:1**
against the surface, not with shadow.

---

## 4. Color-vision considerations

Roughly 8% of men and 0.5% of women have some color-vision deficiency. Designing
for it is mostly _not_ about exotic palettes — it's about never letting color be
the only signal.

| Type                        | What's confused            | Prevalence   | Notes                                       |
| --------------------------- | -------------------------- | ------------ | ------------------------------------------- |
| **Deuteranopia / -anomaly** | red ↔ green                | ~6% of men   | most common; the default case to design for |
| **Protanopia / -anomaly**   | red ↔ green (red darkened) | ~2% of men   | red appears dimmer, can drop below contrast |
| **Tritanopia**              | blue ↔ yellow              | <0.01%, rare | still worth a sanity check                  |

### Non-negotiable rules

1. **Never encode meaning by hue alone.** Add a second channel: icon, text
   label, shape, underline, position, or pattern.
2. **Links:** don't rely on "blue = link". Underline links in body copy, or
   give them a clearly distinct weight/decoration. A deuteranope reading a
   blue link in a wall of dark text may not register it as a link at all.
3. **Status (success/warning/error):** the red/green pair is the _worst_
   possible choice for the most common deficiency. Always attach an icon and/or
   text — ✓ / ⚠ / ✕, or "Success" / "Error". Shape carries the meaning; color
   reinforces it.
4. **Charts/legends:** label series directly or use distinct line styles, not a
   color-only legend.

### How this palette's semantic colors actually fare

The Flexoki semantic colors are distinguishable to most CVD types because they
differ in _lightness_, not just hue — but contrast is uneven, which matters more
than CVD here:

| Semantic                    | On             | Ratio      | Normal grade      | Verdict                    |
| --------------------------- | -------------- | ---------- | ----------------- | -------------------------- |
| error `red #AF3029`         | paper          | 6.23:1     | AA                | good                       |
| success `green #66800B`     | paper          | **4.39:1** | **AA-large only** | ⚠ fails AA for normal text |
| info `blue #205EA6`         | paper          | 6.36:1     | AA                | good                       |
| error `red-400 #D14D41`     | dark `#1C1B1A` | **3.97:1** | **AA-large only** | ⚠ fails AA for normal text |
| success `green-400 #879A39` | dark           | 5.50:1     | AA                | good                       |

Two real failures to fix, not theoretical ones:

- **Light-mode green success text fails AA (4.39:1).** Don't render success
  _messages_ in `#66800B` on paper. Either darken the text token, or restrict
  this green to ≥18pt / icons / fills and put the message text in `tx`.
- **Dark-mode red error text fails AA (3.97:1).** Same remedy: darker surface
  pairing or use `red-400` only for icons/borders (where 1.4.11's 3:1 applies),
  with the actual error sentence in `tx`.

Both reinforce rule #3: lean on **icon + label**, and don't make the at-risk
color carry small body text.

### Simulation tools

- Chrome DevTools → Rendering → "Emulate vision deficiencies"
  (protanopia/deuteranopia/tritanopia/achromatopsia).
- Sim Daltonism (macOS), Color Oracle (cross-platform).
- Figma plugins: Stark, "A11y - Color Contrast Checker".

Run at least the **deuteranopia** simulation on every page that uses color to
convey state.

---

## 5. Tools & ongoing methodology

### The toolbox

| Tool                                    | What it's for                                  | When                 |
| --------------------------------------- | ---------------------------------------------- | -------------------- |
| **`tools/color.py`**                    | exact WCAG ratios + OKLCH; CI contrast gate    | token design, CI     |
| **axe DevTools**                        | DOM-aware a11y audit (roles, labels, contrast) | per-site dev pass    |
| **Lighthouse**                          | quick a11y score in CI/Chrome                  | smoke test per build |
| **WAVE**                                | visual annotated audit in the page             | manual review        |
| **Browser contrast picker**             | eyedropper ratio on live pixels                | spot checks          |
| **Polypane / contrast-grid**            | many-pair matrix, multi-viewport               | palette review       |
| **Screen reader (VoiceOver/NVDA/Orca)** | real semantics & focus order                   | manual pass          |

Automated tools catch ~30–40% of issues. Color contrast, alt text presence,
and ARIA misuse are automatable; _meaningful_ alt text, logical focus order, and
"does this actually make sense to a screen reader" are not. You need both lanes.

### APCA — the WCAG 3 contrast algorithm (not yet normative)

APCA (Accessible Perceptual Contrast Algorithm) is the contrast model slated for
WCAG 3. It's **perceptually better** than WCAG 2's ratio: it accounts for text
size _and weight_ in the threshold, models polarity (dark-on-light vs
light-on-dark behave differently), and uses a perceptual lightness curve instead
of the crude 0.05-flare ratio. In practice WCAG 2 is known to be too lenient on
some dark-on-light pairs and too strict on some light-on-dark ones; APCA fixes
both.

**But:** WCAG 3 is years from recommendation, APCA's thresholds are still
shifting, and no law or audit references it yet. So: **conform to WCAG 2.1 AA as
the binding requirement** (that's what `tools/color.py` and the CI gate
enforce), and optionally consult APCA (e.g. apcacontrast.com) as a tie-breaker
when a pair _passes_ 2.1 but still looks weak — like the 4.67:1 dark muted text.
Treat APCA as advisory, not as the gate.

### Recommended workflow for this system

Two layers. Keep it cheap so it actually gets done.

**1. Automated, per-commit (the gate):**

- `tools/color.py table` regenerates the contrast matrix whenever a token
  changes; commit the output so diffs are reviewable.
- `tools/contrast_gate.py` (§2) runs in CI and **fails the build** if any
  declared token pair drops below its required grade. Seed it with every pair
  in the tables above — including the two known semantic failures, set to their
  _intended_ fixed values so a regression is caught.
- Lighthouse a11y in CI as a coarse backstop.

**2. Manual, per-site, occasionally (the human pass):**

For each of journey / portfolio / research, once per significant redesign:

- **Keyboard only:** tab through everything. Every interactive element must show
  a visible focus ring (3:1, §3) and reach in a sane order. No keyboard traps.
- **Screen reader:** one read-through with Orca/VoiceOver/NVDA. Headings nest
  correctly, links make sense out of context, images have real alt text.
- **Vision sim:** deuteranopia emulation on any page using color for state.
- **Zoom:** 200% browser zoom, no clipping or horizontal scroll.

The split is the whole point: **machines guard the numbers (contrast tokens),
you guard the experience (focus, semantics, meaning).** Don't try to automate
the second or eyeball the first.
