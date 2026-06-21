#!/usr/bin/env python3
"""Drift guard: colors shared between tokens/base.css, proposals.json (D-*),
and schemes/*.yaml must agree."""

import json, os, re, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scheme import load

ROOT = os.path.join(os.path.dirname(__file__), "..")
SHARED = {  # web role -> base24 slot
    "bg": "base00",
    "surface": "base01",
    "overlay": "base02",
    "muted": "base03",
    "text": "base05",
    "error": "base08",
    "warning": "base09",
    "accent": "base0B",
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
        with open(os.path.join(ROOT, "tokens", "base.css")) as f:
            css = f.read()
        block = re.search(css_selector + r"\s*\{([^}]+)\}", css, re.DOTALL).group(1)
        css_roles = css_hex_comments(block)
        with open(os.path.join(ROOT, "tools", "proposals.json")) as f:
            prop = json.load(f)[proposal_key]
        s = load(os.path.join(ROOT, "schemes", scheme_file))
        for role, slot in SHARED.items():
            sv = s.hex(slot)
            self.assertEqual(
                sv,
                prop[role],
                f"{scheme_file}:{slot} vs proposals {proposal_key}:{role}",
            )
            if role in css_roles:  # not every role carries a hex comment
                self.assertEqual(
                    sv, css_roles[role], f"{scheme_file}:{slot} vs base.css {role}"
                )

    def test_light(self):
        self._check("wana-light.yaml", "D-light", r":root")

    def test_dark(self):
        self._check("wana-dark.yaml", "D-dark", r'\[data-theme="dark"\]')


if __name__ == "__main__":
    unittest.main(verbosity=2)
