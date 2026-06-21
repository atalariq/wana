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
    def _check(self, scheme_file, proposal_key, block_pattern):
        with open(os.path.join(ROOT, "tokens", "base.css")) as f:
            css = f.read()
        block = re.search(block_pattern, css, re.DOTALL).group(1)
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
            # Every shared role carries a /* #hex */ comment in both blocks, so
            # the CSS check is mandatory — a missing comment is itself drift.
            self.assertIn(role, css_roles, f"{scheme_file}: no base.css hex for {role}")
            self.assertEqual(
                sv, css_roles[role], f"{scheme_file}:{slot} vs base.css {role}"
            )

    def test_light(self):
        # First ':root { ... }' block = the light token defaults.
        self._check("wana-light.yaml", "D-light", r":root\s*\{([^}]+)\}")

    def test_dark(self):
        # The @media dark block carries the hex comments; the bare
        # [data-theme="dark"] block does not, so parse the @media one.
        self._check(
            "wana-dark.yaml",
            "D-dark",
            r'prefers-color-scheme:\s*dark\)\s*\{\s*:root:not\(\[data-theme="light"\]\)\s*\{([^}]+)\}',
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
