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
