# Wana Foundation (Rename + Phase 0) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebrand the repo to **Wana** and build the Phase 0 generation pipeline — a full ANSI-16 palette in two canonical base24 YAML schemes, an in-repo Python generator, a drift guard, and working kitty themes as the end-to-end proof.

**Architecture:** Two `schemes/wana-{light,dark}.yaml` files (base24) are the source of truth for app-theme generation. `tools/scheme.py` loads a scheme and exposes its base24 palette + the standard base24→ANSI-16 terminal mapping. `tools/gen.py` renders every committed file under `themes/` from `tools/templates/` and has a `--check` mode for CI. `tokens/base.css` stays hand-authored; a drift-guard test keeps the colors shared between `base.css`, `proposals.json`, and the schemes in agreement.

**Tech Stack:** Python 3.14 (stdlib + `pyyaml` 6.0.3, already installed), `unittest`, the existing `tools/color.py` OKLCH/WCAG math.

> **Commit signing note:** this environment cannot sign commits (no TTY for the GPG passphrase). If `git commit` fails with `gpg failed to sign the data`, prepend `-c commit.gpgsign=false` to the commit command. All commit commands below assume you may need that prefix.

---

## File Structure

| Path                                                          | Responsibility                                                  | Status    |
| ------------------------------------------------------------- | --------------------------------------------------------------- | --------- |
| `schemes/wana-dark.yaml`                                      | Canonical base24 palette, dark flavor (24 colors)               | create    |
| `schemes/wana-light.yaml`                                     | Canonical base24 palette, light flavor (24 colors)              | create    |
| `tools/color.py`                                              | Add `bright_variant()` — the one OKLCH bright-shift rule        | modify    |
| `tools/scheme.py`                                             | Load a base24 YAML; expose `.palette` + `.ansi16()`             | create    |
| `tools/gen.py`                                                | Render `themes/**` from `schemes/` + `templates/`; `--check`    | create    |
| `tools/templates/kitty.conf.tmpl`                             | kitty template (the Phase 0 proof target)                       | create    |
| `themes/kitty/wana-dark.conf`                                 | Generated kitty dark theme                                      | generated |
| `themes/kitty/wana-light.conf`                                | Generated kitty light theme                                     | generated |
| `tools/test_bright.py`                                        | Tests for `bright_variant()`                                    | create    |
| `tools/test_scheme.py`                                        | Tests for scheme loading + ANSI-16 mapping + contrast of all 16 | create    |
| `tools/test_drift.py`                                         | Drift guard across base.css / proposals.json / schemes          | create    |
| `tools/test_gen.py`                                           | `gen.py --check` is clean; generated kitty has 16 colors        | create    |
| `site/index.html`, `site/accent-explorer.html`, `site/app.js` | Rebrand proper-name strings                                     | modify    |
| `README.md`, `AGENTS.md`, `tools/color.py` docstring          | Rebrand + document `schemes/`+`themes/`                         | modify    |
| `TODO.md`                                                     | Tick Phase 0 items                                              | modify    |

---

## Reference data (verified during planning)

These are the **verified candidate values**. The authoring tasks start from these
and re-run the verification commands; only adjust if a number drifts.

**base24 → ANSI-16 terminal mapping** (used by `scheme.py` and the kitty template):

```
color0  = base01    color8  = base03
color1  = base08    color9  = base12
color2  = base0B    color10 = base14
color3  = base0A    color11 = base13
color4  = base0D    color12 = base16
color5  = base0E    color13 = base17
color6  = base0C    color14 = base15
color7  = base05    color15 = base07
```

**Dark accents + brights, verified vs bg `#282828`** (`bright_variant` with `fg_is_light=True`, dL=0.08, dC=1.10):

| slot           | role           | hex         | contrast | bright slot | bright hex | contrast |
| -------------- | -------------- | ----------- | -------- | ----------- | ---------- | -------- |
| base08 red     | error          | `#fe8b89`   | 6.51 AA  | base12      | `#ffa09d`  | 7.56     |
| base0B green   | accent         | `#7abb87`   | 6.52 AA  | base14      | `#8dd69c`  | 8.59     |
| base09 orange  | warning        | `#eeb562`   | 8.02 AAA | —           | —          | —        |
| base0A yellow  | Gruvbox yellow | `#eeb562`\* | 8.02     | base13      | `#ffcd70`  | 9.98     |
| base0D blue    | info           | `#80b7f0`   | 6.99 AA  | base16      | `#93d1ff`  | 8.99     |
| base0E magenta | Gruvbox purple | `#d3869b`   | 5.37 AA  | base17      | `#f39bb3`  | 7.13     |
| base0C cyan    | Gruvbox aqua   | `#8ec07c`   | 7.01 AAA | base15      | `#a3dc8f`  | 9.26     |

\* On dark, `warning` and a distinct yellow nearly coincide; Task 4 keeps
`base09=#eeb562` (orange) and selects `base0A` yellow + `base0F` brown via the
verify step (candidates: yellow `#fabd2f`, brown derived) — see Task 4 Step 2.

**Light accents + brights, verified vs bg `#fffcf0`** (`bright_variant` with `fg_is_light=False`):

| slot           | role         | hex       | contrast | bright slot | bright hex | contrast |
| -------------- | ------------ | --------- | -------- | ----------- | ---------- | -------- |
| base08 red     | error        | `#bc4039` | 5.20 AA  | base12      | `#a61619`  | 7.43     |
| base0B green   | accent       | `#2d6e3f` | 5.99 AA  | base14      | `#015826`  | 8.43     |
| base09 orange  | warning      | `#a06300` | 4.78 AA  | —           | —          | —        |
| base0A yellow  | Flexoki, fit | `#956c00` | 4.62 AA  | base13      | `#805300`  | 6.48     |
| base0D blue    | info         | `#1c6aae` | 5.49 AA  | base16      | `#00529b`  | 7.62     |
| base0E magenta | Flexoki 600  | `#a02f6f` | 6.53 AA  | base17      | `#8a0059`  | 9.18     |
| base0C cyan    | Flexoki, fit | `#218078` | 4.62 AA  | base15      | `#006a62`  | 6.31     |

Greyscale slots come straight from existing Wana roles where they exist
(`base00=bg, base01=surface, base02=overlay, base03=muted, base05=text`); the
remaining ramp slots (`base04, base06, base07, base10, base11`) are derived and
finalized by the verify steps in Tasks 4–5.

---

## Task 1: Rebrand textual references

Renames the proper-name occurrences only. The physical directory move
(`~/Repos/design-system → ~/Repos/wana`) is deferred to the final task so it
doesn't break path-relative execution of the tasks in between.

**Files:**

- Modify: `README.md:1`
- Modify: `site/index.html:25` (and `<title>`)
- Modify: `site/accent-explorer.html:6`
- Modify: `site/app.js` (`exportFilename`)
- Modify: `AGENTS.md:1` (and any name string)
- Modify: `tools/color.py:2` (docstring)

- [ ] **Step 1: Find every proper-name occurrence**

Run: `grep -rni "design.system\|atalariq design\|atalariq-tokens" README.md AGENTS.md site/ tools/color.py`
Expected: the lines listed in Files above (README title, site title/h1, accent-explorer title, app.js export filename, AGENTS heading, color.py docstring).

- [ ] **Step 2: Rebrand `README.md`**

Change the H1 from `# design-system` to `# Wana`. Leave descriptive prose
("a personal CSS custom-property design system") unchanged.

- [ ] **Step 3: Rebrand `site/index.html`**

Set `<title>` to `Wana` and the `<h1 class="site-title">` to
`Wana <span>design system</span>` is already correct — verify the `<title>`
tag matches. If `<title>` still says "atalariq design system", change it to
`Wana — design system`.

- [ ] **Step 4: Rebrand `site/accent-explorer.html`**

Change `<title>Accent Explorer — design system</title>` to
`<title>Accent Explorer — Wana</title>`.

- [ ] **Step 5: Rebrand `site/app.js` export filename**

Find `exportFilename` (currently produces `atalariq-tokens-…`). Change the
basename to `wana-tokens`.

- [ ] **Step 6: Rebrand `AGENTS.md` + `tools/color.py` docstring**

`AGENTS.md` line 1 already reads `# Wana — Agent Guide`; verify. In
`tools/color.py`, change the docstring line `"""Color math for the design system.`
to `"""Color math for Wana.`.

- [ ] **Step 7: Verify nothing functional broke**

Run: `python3 tools/test_color.py`
Expected: all tests pass (rename touched only a docstring in `color.py`).

- [ ] **Step 8: Commit**

```bash
git add README.md site/index.html site/accent-explorer.html site/app.js AGENTS.md tools/color.py
git commit -m "refactor: rebrand proper-name references to Wana"
```

---

## Task 2: `bright_variant()` — the one bright-shift rule

The single rule that turns a normal ANSI color into its bright variant: shift
OKLCH lightness toward the foreground end by a fixed delta, nudge chroma, clamp.

**Files:**

- Modify: `tools/color.py` (add function near the OKLCH helpers)
- Test: `tools/test_bright.py`

- [ ] **Step 1: Write the failing test**

```python
#!/usr/bin/env python3
"""Tests for color.bright_variant — the ANSI bright-shift rule."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color import bright_variant, contrast

class TestBrightVariant(unittest.TestCase):
    def test_dark_red_brightens_and_passes(self):
        # fg_is_light=True (dark theme): bright is lighter, higher contrast on dark bg
        b = bright_variant("#fe8b89", fg_is_light=True)
        self.assertEqual(b, "#ffa09d")
        self.assertGreater(contrast(b, "#282828"), contrast("#fe8b89", "#282828"))

    def test_light_red_deepens_and_passes(self):
        # fg_is_light=False (light theme): bright is darker, higher contrast on light bg
        b = bright_variant("#bc4039", fg_is_light=False)
        self.assertEqual(b, "#a61619")
        self.assertGreater(contrast(b, "#fffcf0"), contrast("#bc4039", "#fffcf0"))

    def test_returns_valid_hex(self):
        b = bright_variant("#7abb87", fg_is_light=True)
        self.assertRegex(b, r"^#[0-9a-f]{6}$")

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

- [ ] **Step 2: Run the test, verify it fails**

Run: `python3 tools/test_bright.py`
Expected: FAIL with `ImportError: cannot import name 'bright_variant'`.

- [ ] **Step 3: Implement `bright_variant` in `tools/color.py`**

Add after `oklch_to_rgb` (uses helpers already in the file):

```python
def bright_variant(
    hex_color: str, fg_is_light: bool, dL: float = 0.08, dC: float = 1.10
) -> str:
    """ANSI 'bright' variant: shift OKLCH lightness toward the fg end.

    fg_is_light=True  (dark theme)  -> lighter bright (L += dL)
    fg_is_light=False (light theme) -> deeper bright  (L -= dL)
    Chroma is nudged by dC; result is gamut-clamped by oklch_to_rgb.
    """
    L, C, H = rgb_to_oklch(hex_to_rgb(hex_color))
    L /= 100  # rgb_to_oklch returns L as a percentage
    L = min(0.98, L + dL) if fg_is_light else max(0.10, L - dL)
    return rgb_to_hex(oklch_to_rgb(L, C * dC, H))
```

- [ ] **Step 4: Run the test, verify it passes**

Run: `python3 tools/test_bright.py`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add tools/color.py tools/test_bright.py
git commit -m "feat(tools): add bright_variant OKLCH shift for ANSI brights"
```

---

## Task 3: `scheme.py` — base24 loader + ANSI-16 mapping

Loads a base24 YAML and exposes the palette and the standard 16-color terminal
mapping. No file generation yet — this is the data layer the generator builds on.

**Files:**

- Create: `tools/scheme.py`
- Test: `tools/test_scheme.py`

- [ ] **Step 1: Write the failing test**

```python
#!/usr/bin/env python3
"""Tests for tools/scheme.py — base24 loading + ANSI-16 mapping."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scheme import Scheme, ANSI16_SLOTS

FIXTURE = {  # minimal valid base24 palette (base00..base17)
    "base00": "282828", "base01": "32302f", "base02": "3c3836", "base03": "a89984",
    "base04": "bdae93", "base05": "ebdbb2", "base06": "f2e5bc", "base07": "fbf1c7",
    "base08": "fe8b89", "base09": "eeb562", "base0A": "fabd2f", "base0B": "7abb87",
    "base0C": "8ec07c", "base0D": "80b7f0", "base0E": "d3869b", "base0F": "bb8e6e",
    "base10": "1d2021", "base11": "161616", "base12": "ffa09d", "base13": "ffcd70",
    "base14": "8dd69c", "base15": "a3dc8f", "base16": "93d1ff", "base17": "f39bb3",
}

class TestScheme(unittest.TestCase):
    def setUp(self):
        self.s = Scheme(name="Wana Dark", variant="dark", palette=dict(FIXTURE))

    def test_has_24_slots(self):
        self.assertEqual(len(self.s.palette), 24)

    def test_hex_lookup_adds_hash(self):
        self.assertEqual(self.s.hex("base00"), "#282828")

    def test_ansi16_has_16_entries(self):
        self.assertEqual(len(self.s.ansi16()), 16)

    def test_ansi16_mapping(self):
        a = self.s.ansi16()
        self.assertEqual(a[0], "#32302f")   # color0 = base01
        self.assertEqual(a[1], "#fe8b89")   # color1 = base08 (red)
        self.assertEqual(a[7], "#ebdbb2")   # color7 = base05 (fg/white)
        self.assertEqual(a[9], "#ffa09d")   # color9 = base12 (br-red)
        self.assertEqual(a[15], "#fbf1c7")  # color15 = base07

    def test_validate_rejects_missing_slot(self):
        bad = dict(FIXTURE); del bad["base17"]
        with self.assertRaises(ValueError):
            Scheme(name="x", variant="dark", palette=bad).validate()

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

- [ ] **Step 2: Run the test, verify it fails**

Run: `python3 tools/test_scheme.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'scheme'`.

- [ ] **Step 3: Implement `tools/scheme.py`**

```python
#!/usr/bin/env python3
"""Load a base24 YAML scheme and expose its palette + ANSI-16 mapping.

A base24 scheme has 24 colour slots base00..base17. The standard terminal
mapping (tinted-theming) turns those into 16 ANSI colours.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import yaml

SLOTS = [f"base{n:02X}" for n in range(24)]  # base00..base17 (hex-cased)

# Standard base24 -> 16-colour terminal mapping (index = ANSI colour number).
ANSI16_SLOTS = [
    "base01", "base08", "base0B", "base0A", "base0D", "base0E", "base0C", "base05",
    "base03", "base12", "base14", "base13", "base16", "base17", "base15", "base07",
]


@dataclass
class Scheme:
    name: str
    variant: str  # "light" | "dark"
    palette: dict  # slot -> 6-digit hex WITHOUT leading '#'

    def hex(self, slot: str) -> str:
        return "#" + self.palette[slot].lstrip("#").lower()

    def ansi16(self) -> list[str]:
        return [self.hex(s) for s in ANSI16_SLOTS]

    def validate(self) -> "Scheme":
        for slot in SLOTS:
            v = self.palette.get(slot)
            if v is None:
                raise ValueError(f"{self.name}: missing slot {slot}")
            if len(v.lstrip('#')) != 6:
                raise ValueError(f"{self.name}: {slot} not 6-digit hex: {v!r}")
        return self


def load(path: str) -> Scheme:
    with open(path) as f:
        data = yaml.safe_load(f)
    return Scheme(
        name=data["name"],
        variant=data.get("variant", "dark"),
        palette={k: v for k, v in data["palette"].items()},
    ).validate()
```

- [ ] **Step 4: Run the test, verify it passes**

Run: `python3 tools/test_scheme.py`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add tools/scheme.py tools/test_scheme.py
git commit -m "feat(tools): add base24 scheme loader and ANSI-16 mapping"
```

---

## Task 4: Author `schemes/wana-dark.yaml`

Write the 24-colour dark palette and prove every ANSI colour passes AA on the
dark bg, and that each bright equals `bright_variant(normal)`.

**Files:**

- Create: `schemes/wana-dark.yaml`
- Test: add to `tools/test_scheme.py`

- [ ] **Step 1: Write `schemes/wana-dark.yaml`**

```yaml
system: "base24"
name: "Wana Dark"
author: "atalariq"
variant: "dark"
# GENERATED-SOURCE: this file is the canonical palette. Brights (base12-17)
# are produced by tools/color.py bright_variant(normal, fg_is_light=True);
# the drift/scheme tests enforce that relationship.
palette:
  base00: "282828" # bg
  base01: "32302f" # surface
  base02: "3c3836" # overlay / selection
  base03: "a89984" # muted / comments
  base04: "bdae93" # dark fg (status bars)
  base05: "ebdbb2" # text
  base06: "f2e5bc" # light fg
  base07: "fbf1c7" # lightest
  base08: "fe8b89" # red     = error
  base09: "eeb562" # orange  = warning
  base0A: "fabd2f" # yellow  (Gruvbox)
  base0B: "7abb87" # green   = accent
  base0C: "8ec07c" # cyan    (Gruvbox aqua)
  base0D: "80b7f0" # blue    = info
  base0E: "d3869b" # magenta (Gruvbox purple)
  base0F: "bb8e6e" # brown
  base10: "1d2021" # darker bg
  base11: "161616" # darkest bg
  base12: "ffa09d" # br-red
  base13: "ffd479" # br-yellow  (= bright_variant base0A)
  base14: "8dd69c" # br-green
  base15: "a3dc8f" # br-cyan
  base16: "93d1ff" # br-blue
  base17: "f39bb3" # br-magenta
```

- [ ] **Step 2: Verify contrast of every ANSI colour and finalize the open slots**

Run:

```bash
python3 - <<'PY'
import sys; sys.path.insert(0,"tools")
from scheme import load, ANSI16_SLOTS
from color import contrast, wcag_grade, bright_variant
s = load("schemes/wana-dark.yaml")
bg = s.hex("base00")
for i, c in enumerate(s.ansi16()):
    print(f"color{i:<2} {c} {contrast(c,bg):.2f} {wcag_grade(contrast(c,bg))}")
# brights must equal bright_variant(normal, fg_is_light=True)
for nb, br in [("base0A","base13"),("base08","base12"),("base0B","base14"),
               ("base0C","base15"),("base0D","base16"),("base0E","base17")]:
    want = bright_variant(s.hex(nb), True)
    print(nb, "->", br, s.hex(br), "want", want, "OK" if s.hex(br)==want else "FIX")
PY
```

Expected: every `colorN` grades AA or better against `base00`; each bright line
prints `OK`. If any `colorN` is below AA, deepen/retune that slot's hex and
re-run. If a bright prints `FIX`, replace it with the `want` value shown
(this is how `base13 br-yellow` and `base0F brown` get their final values —
copy the verified output into the YAML).

- [ ] **Step 3: Add a contrast assertion to `tools/test_scheme.py`**

```python
class TestWanaDarkContrast(unittest.TestCase):
    def test_all_ansi_pass_aa(self):
        from scheme import load
        from color import contrast
        s = load(os.path.join(os.path.dirname(__file__), "..", "schemes", "wana-dark.yaml"))
        bg = s.hex("base00")
        for i, c in enumerate(s.ansi16()):
            if i in (0, 8):  # color0/8 are background-ish, not fg text
                continue
            self.assertGreaterEqual(contrast(c, bg), 4.5, f"color{i} {c} fails AA")
```

- [ ] **Step 4: Run the test, verify it passes**

Run: `python3 tools/test_scheme.py`
Expected: PASS (all tests, including `TestWanaDarkContrast`).

- [ ] **Step 5: Commit**

```bash
git add schemes/wana-dark.yaml tools/test_scheme.py
git commit -m "feat(schemes): add Wana Dark base24 palette (ANSI-16, AA-verified)"
```

---

## Task 5: Author `schemes/wana-light.yaml`

Same as Task 4 for the light flavor. Light normals for yellow/cyan use the
AA-fitted values (`#956c00`, `#218078`); brights deepen via `fg_is_light=False`.

**Files:**

- Create: `schemes/wana-light.yaml`
- Test: add to `tools/test_scheme.py`

- [ ] **Step 1: Write `schemes/wana-light.yaml`**

```yaml
system: "base24"
name: "Wana Light"
author: "atalariq"
variant: "light"
# Brights (base12-17) = tools/color.py bright_variant(normal, fg_is_light=False).
palette:
  base00: "fffcf0" # bg / paper
  base01: "f2f0e5" # surface
  base02: "e6e4d9" # overlay / selection
  base03: "6f6e69" # muted / comments
  base04: "878580" # dark fg
  base05: "100f0f" # text
  base06: "1c1b1a" # light fg (Flexoki convention: deeper than text)
  base07: "282726" # lightest fg
  base08: "bc4039" # red     = error
  base09: "a06300" # orange  = warning
  base0A: "956c00" # yellow  (Flexoki, AA-fitted)
  base0B: "2d6e3f" # green   = accent
  base0C: "218078" # cyan    (Flexoki, AA-fitted)
  base0D: "1c6aae" # blue    = info
  base0E: "a02f6f" # magenta (Flexoki 600)
  base0F: "8a6240" # brown
  base10: "e1ddc9" # darker bg
  base11: "d4cfb8" # darkest bg
  base12: "a61619" # br-red
  base13: "805300" # br-yellow
  base14: "015826" # br-green
  base15: "006a62" # br-cyan
  base16: "00529b" # br-blue
  base17: "8a0059" # br-magenta
```

- [ ] **Step 2: Verify contrast + bright relationship**

Run (same harness as Task 4 Step 2, light file + `fg_is_light=False`):

```bash
python3 - <<'PY'
import sys; sys.path.insert(0,"tools")
from scheme import load
from color import contrast, wcag_grade, bright_variant
s = load("schemes/wana-light.yaml")
bg = s.hex("base00")
for i, c in enumerate(s.ansi16()):
    print(f"color{i:<2} {c} {contrast(c,bg):.2f} {wcag_grade(contrast(c,bg))}")
for nb, br in [("base0A","base13"),("base08","base12"),("base0B","base14"),
               ("base0C","base15"),("base0D","base16"),("base0E","base17")]:
    want = bright_variant(s.hex(nb), False)
    print(nb, "->", br, s.hex(br), "want", want, "OK" if s.hex(br)==want else "FIX")
PY
```

Expected: every fg `colorN` grades AA+ against `base00`; brights print `OK`.
Fix any `FIX`/sub-AA slot as in Task 4 Step 2. Finalize `base0F brown` and the
`base04/06/07/10/11` ramp here (deepen until distinct and, for fg slots, AA).

- [ ] **Step 3: Add a contrast assertion to `tools/test_scheme.py`**

```python
class TestWanaLightContrast(unittest.TestCase):
    def test_all_ansi_pass_aa(self):
        from scheme import load
        from color import contrast
        s = load(os.path.join(os.path.dirname(__file__), "..", "schemes", "wana-light.yaml"))
        bg = s.hex("base00")
        for i, c in enumerate(s.ansi16()):
            if i in (0, 8):
                continue
            self.assertGreaterEqual(contrast(c, bg), 4.5, f"color{i} {c} fails AA")
```

- [ ] **Step 4: Run the test, verify it passes**

Run: `python3 tools/test_scheme.py`
Expected: PASS (all tests).

- [ ] **Step 5: Commit**

```bash
git add schemes/wana-light.yaml tools/test_scheme.py
git commit -m "feat(schemes): add Wana Light base24 palette (ANSI-16, AA-verified)"
```

---

## Task 6: Drift guard across base.css / proposals.json / schemes

Ensure the colors shared between the ratified web layer and the new schemes
never silently diverge.

**Files:**

- Create: `tools/test_drift.py`

The shared mapping (web role → base24 slot), values from `tokens/base.css`:

```
bg→base00, surface→base01, overlay→base02, muted→base03, text→base05,
error→base08, warning→base09, accent→base0B, info→base0D
```

- [ ] **Step 1: Write the failing test**

```python
#!/usr/bin/env python3
"""Drift guard: colors shared between tokens/base.css, proposals.json (D-*),
and schemes/*.yaml must agree."""
import json, os, re, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scheme import load

ROOT = os.path.join(os.path.dirname(__file__), "..")
SHARED = {  # web role -> base24 slot
    "bg": "base00", "surface": "base01", "overlay": "base02", "muted": "base03",
    "text": "base05", "error": "base08", "warning": "base09", "accent": "base0B",
    "info": "base0D",
}

def css_hex_comments(block):
    """role -> hex pulled from the '/* #rrggbb */' comments in a base.css block."""
    out = {}
    for role, hexv in re.findall(r"--(\w+):[^;]+;\s*/\*\s*(#[0-9a-fA-F]{6})", block):
        out[role] = hexv.lower()
    return out

class TestDrift(unittest.TestCase):
    def _check(self, scheme_file, proposal_key, css_selector):
        css = open(os.path.join(ROOT, "tokens", "base.css")).read()
        block = re.search(css_selector + r"\s*\{([^}]+)\}", css, re.DOTALL).group(1)
        css_roles = css_hex_comments(block)
        prop = json.load(open(os.path.join(ROOT, "tools", "proposals.json")))[proposal_key]
        s = load(os.path.join(ROOT, "schemes", scheme_file))
        for role, slot in SHARED.items():
            sv = s.hex(slot)
            self.assertEqual(sv, prop[role], f"{scheme_file}:{slot} vs proposals {proposal_key}:{role}")
            if role in css_roles:  # not every role carries a hex comment
                self.assertEqual(sv, css_roles[role], f"{scheme_file}:{slot} vs base.css {role}")

    def test_light(self):
        self._check("wana-light.yaml", "D-light", r":root")

    def test_dark(self):
        self._check("wana-dark.yaml", "D-dark", r'\[data-theme="dark"\]')

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

- [ ] **Step 2: Run the test, verify it fails OR passes meaningfully**

Run: `python3 tools/test_drift.py`
Expected: PASS if Tasks 4–5 used the canonical role hexes. If it FAILS, the
failure message names the exact slot/role mismatch — fix the YAML to match the
ratified `proposals.json` D-\* value (the web layer is authoritative for shared
roles), then re-run.

- [ ] **Step 3: Commit**

```bash
git add tools/test_drift.py
git commit -m "test(tools): add drift guard across base.css, proposals.json, schemes"
```

---

## Task 7: `gen.py` + kitty template + generated themes

The generator and the first real target. Proves YAML → ANSI-16 → a working
terminal config end to end.

**Files:**

- Create: `tools/templates/kitty.conf.tmpl`
- Create: `tools/gen.py`
- Create (generated): `themes/kitty/wana-dark.conf`, `themes/kitty/wana-light.conf`

- [ ] **Step 1: Write `tools/templates/kitty.conf.tmpl`**

Uses `str.format` field names that `gen.py` supplies (`{name}`, `{c0}`…`{c15}`,
`{bg}`, `{fg}`, `{cursor}`, `{sel_bg}`, `{sel_fg}`):

```
# GENERATED by tools/gen.py from schemes/ — do not edit.
# {name}

foreground            {fg}
background            {bg}
cursor                {cursor}
cursor_text_color     {bg}
selection_foreground  {sel_fg}
selection_background  {sel_bg}

color0  {c0}
color1  {c1}
color2  {c2}
color3  {c3}
color4  {c4}
color5  {c5}
color6  {c6}
color7  {c7}
color8  {c8}
color9  {c9}
color10 {c10}
color11 {c11}
color12 {c12}
color13 {c13}
color14 {c14}
color15 {c15}
```

- [ ] **Step 2: Write `tools/gen.py`**

```python
#!/usr/bin/env python3
"""Generate app themes from schemes/*.yaml into themes/.

    python3 tools/gen.py          # regenerate all themes
    python3 tools/gen.py --check  # exit 1 if any committed theme is stale

Add a new target by writing tools/templates/<x> and a render_<x>() below.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scheme import Scheme, load  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
TPL = os.path.join(os.path.dirname(__file__), "templates")
SCHEMES = {"dark": "wana-dark.yaml", "light": "wana-light.yaml"}


def _kitty_fields(s: Scheme) -> dict:
    a = s.ansi16()
    fields = {f"c{i}": a[i] for i in range(16)}
    fields.update(
        name=s.name,
        bg=s.hex("base00"),
        fg=s.hex("base05"),
        cursor=s.hex("base0B"),     # accent green caret
        sel_bg=s.hex("base02"),
        sel_fg=s.hex("base05"),
    )
    return fields


def render_kitty(s: Scheme) -> tuple[str, str]:
    tpl = open(os.path.join(TPL, "kitty.conf.tmpl")).read()
    out = tpl.format(**_kitty_fields(s))
    rel = f"themes/kitty/wana-{s.variant}.conf"
    return rel, out


RENDERERS = [render_kitty]


def build() -> dict:
    """Return {relative_path: content} for every target/flavor."""
    files = {}
    for variant, fname in SCHEMES.items():
        s = load(os.path.join(ROOT, "schemes", fname))
        for render in RENDERERS:
            rel, content = render(s)
            files[rel] = content
    return files


def main(argv: list[str]) -> int:
    check = "--check" in argv
    files = build()
    stale = []
    for rel, content in files.items():
        path = os.path.join(ROOT, rel)
        existing = open(path).read() if os.path.exists(path) else None
        if check:
            if existing != content:
                stale.append(rel)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            print(f"wrote {rel}")
    if check and stale:
        print("STALE (run tools/gen.py):")
        for rel in stale:
            print(f"  {rel}")
        return 1
    if check:
        print(f"OK: {len(files)} themes up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 3: Generate the themes**

Run: `python3 tools/gen.py`
Expected: prints `wrote themes/kitty/wana-dark.conf` and
`wrote themes/kitty/wana-light.conf`.

- [ ] **Step 4: Eyeball the output**

Run: `grep -c '^color' themes/kitty/wana-dark.conf`
Expected: `16`.

- [ ] **Step 5: Commit**

```bash
git add tools/gen.py tools/templates/kitty.conf.tmpl themes/kitty/
git commit -m "feat(gen): add theme generator and kitty target"
```

---

## Task 8: `gen.py --check` test + freshness wiring

Lock in that committed `themes/` always match the schemes.

**Files:**

- Create: `tools/test_gen.py`

- [ ] **Step 1: Write the test**

```python
#!/usr/bin/env python3
"""gen.py contract: --check is clean after a build, kitty has 16 colors."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen

class TestGen(unittest.TestCase):
    def test_check_is_clean(self):
        # If this fails, run `python3 tools/gen.py` and commit the result.
        self.assertEqual(gen.main(["--check"]), 0)

    def test_kitty_has_16_colors(self):
        files = gen.build()
        dark = files["themes/kitty/wana-dark.conf"]
        self.assertEqual(sum(1 for ln in dark.splitlines() if ln.startswith("color")), 16)

    def test_generated_header_present(self):
        for content in gen.build().values():
            self.assertIn("GENERATED", content)

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

- [ ] **Step 2: Run the test, verify it passes**

Run: `python3 tools/test_gen.py`
Expected: PASS (3 tests). If `test_check_is_clean` fails, run
`python3 tools/gen.py`, `git add themes/`, and re-run.

- [ ] **Step 3: Run the whole suite**

Run: `python3 -m unittest discover -s tools -p 'test_*.py' -v`
Expected: every test across `test_color`, `test_bright`, `test_scheme`,
`test_drift`, `test_gen` passes.

- [ ] **Step 4: Commit**

```bash
git add tools/test_gen.py
git commit -m "test(gen): verify themes stay in sync with schemes"
```

---

## Task 9: Documentation — schemes/themes + Phase 0 done

**Files:**

- Modify: `AGENTS.md` (Research Structure block)
- Modify: `README.md` (add a short "App themes" section)
- Modify: `TODO.md` (tick Phase 0)

- [ ] **Step 1: Update `AGENTS.md` Research Structure**

Add to the tree under the existing entries:

```
schemes/
  wana-light.yaml          # canonical base24 palette (light)
  wana-dark.yaml           # canonical base24 palette (dark)
tools/
  gen.py                   # schemes -> themes/
  scheme.py                # base24 loader + ANSI-16 mapping
themes/                    # GENERATED app themes (do not hand-edit)
  kitty/
```

- [ ] **Step 2: Add a README "App themes" section**

After the token reference, add:

```markdown
## App themes

Terminal/editor themes are generated from the canonical base24 schemes in
`schemes/` by `tools/gen.py`, into `themes/` (never hand-edited). Regenerate
with `python3 tools/gen.py`; CI checks freshness with `--check`.
```

- [ ] **Step 3: Tick Phase 0 in `TODO.md`**

Change the three Phase 0 checkboxes from `- [ ]` to `- [x]` (ANSI-16 set,
canonical base24 file, generation path). Leave Phase 1/2 unticked.

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md README.md TODO.md
git commit -m "docs: document schemes/themes pipeline, mark Phase 0 done"
```

---

## Task 10 (final, operational): physical directory rename

Run **last**, after every task above is committed — it changes the repo's path,
which would break the path-relative steps if done earlier. Best run by the user
in a shell with no agent session open inside the directory.

- [ ] **Step 1: Confirm a clean tree**

Run: `git status --porcelain`
Expected: empty (everything committed).

- [ ] **Step 2: Move the directory**

```bash
cd ~ && mv ~/Repos/design-system ~/Repos/wana && cd ~/Repos/wana
```

- [ ] **Step 3: Verify git still works from the new path**

Run: `git -C ~/Repos/wana log --oneline -3`
Expected: the recent Wana commits, history intact.

- [ ] **Step 4 (when ready to publish): add the remote and push**

```bash
git -C ~/Repos/wana remote add origin git@github.com:atalariq/wana.git
git -C ~/Repos/wana push -u origin dev
```

(Run only when you're ready — create the empty `atalariq/wana` repo on GitHub
first. This step is yours, not the implementer's.)

---

## Self-review notes

- **Spec coverage:** rename (Task 1, 10), ANSI-16 palette extension (Tasks 2,
  4, 5), base24 canonical schemes (4, 5), in-repo generator (3, 7), drift guard
  (6), generation freshness (8), kitty proof target (7), docs (9). Phase 1/2
  targets are intentionally deferred to their own plans per the agreed structure.
- **Verification:** every color slot is contrast-checked (Tasks 4–5), brights
  are tied to `bright_variant` by test, and `gen --check` guarantees freshness.
- **Out of scope here:** nvim/noctalia/herdr/alacritty/opencode/etc. (Phase 1–2
  plans), npm publish, standalone repo split, regenerating `base.css`.
