#!/usr/bin/env python3
"""Per-scheme contrast + OKLCH report for tools/schemes.json.

For each scheme, computes the contrast ratio of every foreground/accent
color against that scheme's primary background, plus OKLCH for each color.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from color import contrast, oklch_str, parse, wcag_grade  # noqa: E402

# Primary background key per scheme (first listed bg-like key).
BG_KEY = {
    "Gruvbox Dark (medium)": "bg",
    "Gruvbox Light (medium)": "bg",
    "Catppuccin Mocha": "base",
    "Catppuccin Latte": "base",
    "Flexoki Light": "paper",
    "Flexoki Dark": "black",
    "Everforest Dark (medium)": "bg0",
    "Everforest Light (medium)": "bg0",
    "Tokyo Night (Night)": "bg",
    "Tokyo Night Day (light)": "bg",
    "Solarized Dark": "base03",
    "Solarized Light": "base3",
}


def main() -> None:
    schemes = json.load(open(os.path.join(os.path.dirname(__file__), "schemes.json")))
    for name, colors in schemes.items():
        bg_key = BG_KEY[name]
        bg = colors[bg_key]
        print(f"\n### {name}  (bg = {bg_key} {bg})\n")
        print("| role | hex | oklch | contrast vs bg | grade |")
        print("|---|---|---|---|---|")
        for role, hexv in colors.items():
            ok = oklch_str(parse(hexv))
            if role == bg_key:
                print(f"| {role} (bg) | `{hexv}` | {ok} | — | — |")
                continue
            r = contrast(hexv, bg)
            print(f"| {role} | `{hexv}` | {ok} | {r:.2f}:1 | {wcag_grade(r)} |")


if __name__ == "__main__":
    main()
