#!/usr/bin/env python3
"""Minimal test suite for tools/color.py color math.

Run from the repo root:
    python3 tools/test_color.py
    python3 -m unittest tools.test_color -v
"""

import sys
import os
import unittest

# Make `import color` work when running as `python3 tools/test_color.py` from
# the repo root OR from inside the tools/ directory.
_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

from color import (
    contrast,
    fit_lightness,
    hex_to_rgb,
    oklch_to_rgb,
    parse_oklch,
    relative_luminance,
    rgb_to_hex,
    rgb_to_oklch,
)


class TestContrast(unittest.TestCase):
    """Known contrast values asserted in tokens/base.css comments."""

    BG = "#fffcf0"

    def test_text_on_bg(self):
        # --text: #100f0f — 18.62:1 AAA
        self.assertAlmostEqual(contrast("#100f0f", self.BG), 18.62, delta=0.05)

    def test_accent_on_bg(self):
        # --accent: #2d6e3f — 5.99:1 AA
        self.assertAlmostEqual(contrast("#2d6e3f", self.BG), 5.99, delta=0.05)

    def test_muted_on_bg(self):
        # --muted: #6f6e69 — 4.97:1 AA
        self.assertAlmostEqual(contrast("#6f6e69", self.BG), 4.97, delta=0.05)

    def test_symmetry(self):
        # Contrast ratio is symmetric.
        c1 = contrast("#100f0f", self.BG)
        c2 = contrast(self.BG, "#100f0f")
        self.assertAlmostEqual(c1, c2, places=10)

    def test_self_contrast(self):
        # A color against itself has ratio 1.0.
        self.assertAlmostEqual(contrast("#fffcf0", "#fffcf0"), 1.0, places=10)


class TestRoundTrip(unittest.TestCase):
    """hex -> OKLCH -> hex should be lossless within rounding.

    rgb_to_oklch returns L as a percentage (0–100); oklch_to_rgb expects L in
    [0, 1], so we divide by 100 before the inverse conversion.
    """

    FOREST_TOKENS = [
        "#fffcf0",  # bg / paper
        "#2d6e3f",  # accent green
        "#100f0f",  # text / near-black
        "#7abb87",  # light green
        "#282828",  # Gruvbox dark bg
    ]

    def _round_trip(self, hex_in: str) -> str:
        rgb = hex_to_rgb(hex_in)
        L_pct, C, H = rgb_to_oklch(rgb)
        rgb2 = oklch_to_rgb(L_pct / 100, C, H)  # scale L back to [0,1]
        return rgb_to_hex(rgb2)

    def test_paper(self):
        self.assertEqual(self._round_trip("#fffcf0"), "#fffcf0")

    def test_accent_green(self):
        self.assertEqual(self._round_trip("#2d6e3f"), "#2d6e3f")

    def test_near_black(self):
        self.assertEqual(self._round_trip("#100f0f"), "#100f0f")

    def test_light_green(self):
        self.assertEqual(self._round_trip("#7abb87"), "#7abb87")

    def test_gruvbox_dark(self):
        self.assertEqual(self._round_trip("#282828"), "#282828")


class TestFitLightness(unittest.TestCase):
    """fit_lightness should converge to within ~0.15 of the target ratio."""

    def test_light_mode_target_6(self):
        # C=0.1, H=150, bg=#fffcf0, target=6.0, mode=light
        L, rgb, ratio = fit_lightness(0.1, 150, "#fffcf0", 6.0, "light")
        self.assertAlmostEqual(ratio, 6.0, delta=0.15)

    def test_returns_valid_l(self):
        # Returned L should be in [0, 1].
        L, rgb, ratio = fit_lightness(0.1, 150, "#fffcf0", 6.0, "light")
        self.assertGreaterEqual(L, 0.0)
        self.assertLessEqual(L, 1.0)

    def test_rgb_in_range(self):
        # Returned RGB channels should all be in [0, 1].
        L, rgb, ratio = fit_lightness(0.1, 150, "#fffcf0", 6.0, "light")
        for ch in rgb:
            self.assertGreaterEqual(ch, 0.0)
            self.assertLessEqual(ch, 1.0)

    def test_dark_mode_target_4_5(self):
        # Dark mode: light accent on a dark bg.
        L, rgb, ratio = fit_lightness(0.1, 150, "#100f0f", 4.5, "dark")
        self.assertAlmostEqual(ratio, 4.5, delta=0.15)


class TestParsing(unittest.TestCase):
    """parse_oklch round-trips with oklch_to_rgb."""

    def test_percent_form(self):
        L, C, H = parse_oklch("oklch(48.3% 0.1 150.1)")
        self.assertAlmostEqual(L, 0.483, places=3)
        self.assertAlmostEqual(C, 0.1, places=4)
        self.assertAlmostEqual(H, 150.1, places=1)

    def test_bare_form(self):
        # Bare numbers: L > 1 is treated as percent.
        L, C, H = parse_oklch("48.3 0.1 150.1")
        self.assertAlmostEqual(L, 0.483, places=3)

    def test_fractional_l_unchanged(self):
        # L <= 1 should pass through unchanged.
        L, C, H = parse_oklch("0.483 0.1 150.1")
        self.assertAlmostEqual(L, 0.483, places=3)


class TestRelativeLuminance(unittest.TestCase):
    """Spot-check relative_luminance against known values."""

    def test_white(self):
        # Pure white has luminance 1.0.
        self.assertAlmostEqual(relative_luminance((1.0, 1.0, 1.0)), 1.0, places=6)

    def test_black(self):
        # Pure black has luminance 0.0.
        self.assertAlmostEqual(relative_luminance((0.0, 0.0, 0.0)), 0.0, places=10)

    def test_white_black_contrast(self):
        # White on black = 21:1 (WCAG maximum).
        lw = relative_luminance((1.0, 1.0, 1.0))
        lb = relative_luminance((0.0, 0.0, 0.0))
        ratio = (lw + 0.05) / (lb + 0.05)
        self.assertAlmostEqual(ratio, 21.0, places=6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
