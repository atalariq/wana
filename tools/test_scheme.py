#!/usr/bin/env python3
"""Tests for tools/scheme.py — base24 loading + ANSI-16 mapping."""

import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scheme import Scheme, ANSI16_SLOTS

FIXTURE = {  # minimal valid base24 palette (base00..base17)
    "base00": "282828",
    "base01": "32302f",
    "base02": "3c3836",
    "base03": "a89984",
    "base04": "bdae93",
    "base05": "ebdbb2",
    "base06": "f2e5bc",
    "base07": "fbf1c7",
    "base08": "fe8b89",
    "base09": "eeb562",
    "base0A": "fabd2f",
    "base0B": "7abb87",
    "base0C": "8ec07c",
    "base0D": "80b7f0",
    "base0E": "d3869b",
    "base0F": "bb8e6e",
    "base10": "1d2021",
    "base11": "161616",
    "base12": "ffa09d",
    "base13": "ffcd70",
    "base14": "8dd69c",
    "base15": "a3dc8f",
    "base16": "93d1ff",
    "base17": "f39bb3",
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
        self.assertEqual(a[0], "#32302f")  # color0 = base01
        self.assertEqual(a[1], "#fe8b89")  # color1 = base08 (red)
        self.assertEqual(a[7], "#ebdbb2")  # color7 = base05 (fg/white)
        self.assertEqual(a[9], "#ffa09d")  # color9 = base12 (br-red)
        self.assertEqual(a[15], "#fbf1c7")  # color15 = base07

    def test_validate_rejects_missing_slot(self):
        bad = dict(FIXTURE)
        del bad["base17"]
        with self.assertRaises(ValueError):
            Scheme(name="x", variant="dark", palette=bad).validate()

    def test_validate_rejects_non_hex(self):
        bad = dict(FIXTURE)
        bad["base08"] = "gggggg"  # right length, not hex
        with self.assertRaises(ValueError):
            Scheme(name="x", variant="dark", palette=bad).validate()


class TestWanaDarkContrast(unittest.TestCase):
    def test_all_ansi_pass_aa(self):
        from scheme import load
        from color import contrast

        s = load(
            os.path.join(os.path.dirname(__file__), "..", "schemes", "wana-dark.yaml")
        )
        bg = s.hex("base00")
        for i, c in enumerate(s.ansi16()):
            # color0 = base01 (surface, intentionally low contrast);
            # color8 = base03 (muted/comments, AA optional). Both exempt.
            if i in (0, 8):
                continue
            self.assertGreaterEqual(contrast(c, bg), 4.5, f"color{i} {c} fails AA")


class TestWanaLightContrast(unittest.TestCase):
    def test_all_ansi_pass_aa(self):
        from scheme import load
        from color import contrast

        s = load(
            os.path.join(os.path.dirname(__file__), "..", "schemes", "wana-light.yaml")
        )
        bg = s.hex("base00")
        for i, c in enumerate(s.ansi16()):
            # color0 = base01 (surface); color8 = base03 (muted). Both exempt.
            if i in (0, 8):
                continue
            self.assertGreaterEqual(contrast(c, bg), 4.5, f"color{i} {c} fails AA")


class TestBrightInvariant(unittest.TestCase):
    """Each chromatic bright must equal bright_variant(its normal) — the rule
    the scheme comments claim. Guards against editing a normal but not its bright."""

    PAIRS = [
        ("base08", "base12"),
        ("base0A", "base13"),
        ("base0B", "base14"),
        ("base0C", "base15"),
        ("base0D", "base16"),
        ("base0E", "base17"),
    ]

    def _check(self, fname, fg_is_light):
        from scheme import load
        from color import bright_variant

        s = load(os.path.join(os.path.dirname(__file__), "..", "schemes", fname))
        for normal, bright in self.PAIRS:
            self.assertEqual(
                s.hex(bright),
                bright_variant(s.hex(normal), fg_is_light),
                f"{fname}:{bright} != bright_variant({normal})",
            )

    def test_dark(self):
        self._check("wana-dark.yaml", True)

    def test_light(self):
        self._check("wana-light.yaml", False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
