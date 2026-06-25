#!/usr/bin/env python3
"""gen.py contract: --check is clean after a build; each target carries its colors."""

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

    def test_tty_has_16_sequences(self):
        files = gen.build()
        dark = files["themes/tty/wana-dark.sh"]
        self.assertEqual(dark.count(r"\e]P"), 16)
        seq = next(ln for ln in dark.splitlines() if r"\e]P" in ln)
        self.assertNotIn("#", seq)  # TTY hex must be bare (no leading '#')

    def test_pywal_is_valid_json_16_colors(self):
        import json

        files = gen.build()
        data = json.loads(files["themes/pywal/wana-dark.json"])
        self.assertEqual(len(data["colors"]), 16)
        self.assertIn("background", data["special"])
        self.assertTrue(data["colors"]["color0"].startswith("#"))

    def test_fzf_opts_color_string(self):
        files = gen.build()
        dark = files["themes/fzf/wana-dark.opts"]
        self.assertTrue(dark.startswith("--color="))
        self.assertIn("prompt:#", dark)
        self.assertIn("pointer:#", dark)

    def test_bat_tmtheme_is_valid_xml(self):
        import xml.etree.ElementTree as ET

        files = gen.build()
        dark = files["themes/bat/wana-dark.tmTheme"]
        ET.fromstring(dark)  # raises if malformed
        self.assertIn("wana-dark", dark)
        self.assertIn("#", dark)

    def test_starship_palette_block(self):
        files = gen.build()
        out = files["themes/starship/wana.toml"]
        self.assertIn("[palettes.wana]", out)
        self.assertIn("blue", out)
        self.assertIn("surface0", out)
        self.assertEqual(out.count(' = "#'), 30)

    def test_btop_has_37_keys(self):
        files = gen.build()
        dark = files["themes/btop/wana-dark.theme"]
        self.assertEqual(dark.count("theme["), 37)
        self.assertIn('theme[main_bg]="#', dark)

    def test_lazygit_theme_block(self):
        files = gen.build()
        out = files["themes/lazygit/wana.yml"]
        self.assertIn("activeBorderColor", out)
        self.assertIn("defaultFgColor", out)
        self.assertIn('"#', out)

    def test_opencode_is_valid_json(self):
        import json

        files = gen.build()
        data = json.loads(files["themes/opencode/wana.json"])
        self.assertEqual(len(data["defs"]), 16)
        self.assertIn("dark", data["theme"]["primary"])
        self.assertIn("light", data["theme"]["text"])

    def test_generated_header_present(self):
        for rel, content in gen.build().items():
            if rel.endswith(".opts"):
                continue  # single-line opts file has no comment syntax
            self.assertIn("GENERATED", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
