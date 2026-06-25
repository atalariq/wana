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
        self.assertEqual(
            sum(1 for ln in dark.splitlines() if ln.startswith("color")), 16
        )

    def test_alacritty_has_16_colors(self):
        files = gen.build()
        dark = files["themes/alacritty/wana-dark.toml"]
        names = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
        for name in names:
            self.assertIn(name, dark)
        # 8 normal + 8 bright assignments
        self.assertEqual(
            dark.count(' = "'), 8 + 8 + 2 + 2 + 2
        )  # +primary/cursor/selection

    def test_generated_header_present(self):
        for content in gen.build().values():
            self.assertIn("GENERATED", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
