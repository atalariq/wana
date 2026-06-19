#!/usr/bin/env python3
"""Full fg×bg contrast matrix + OKLCH for each proposal palette.

Reads tools/proposals.json. For each palette, prints every foreground role
against every background role (bg/surface/overlay), flags WCAG grade, and
emits an OKLCH/HSL column for token tables.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from color import contrast, oklch_str, parse, rgb_to_hsl, wcag_grade  # noqa: E402

FG_ROLES = ["text", "muted", "accent", "success", "warning", "error", "info"]


def main() -> None:
    data = json.load(open(os.path.join(os.path.dirname(__file__), "proposals.json")))
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for name, p in data.items():
        if only and only not in name:
            continue
        bgs = p["_bgs"]
        print(f"\n## {name}\n")
        print("token table:")
        print("| role | hex | hsl | oklch |")
        print("|---|---|---|---|")
        for role, hexv in p.items():
            if role == "_bgs":
                continue
            h, s, l = rgb_to_hsl(parse(hexv))
            print(
                f"| {role} | `{hexv}` | hsl({h} {s}% {l}%) | {oklch_str(parse(hexv))} |"
            )
        print(f"\ncontrast matrix (fg \\ bg):\n")
        print("| fg \\ bg | " + " | ".join(f"{b} `{p[b]}`" for b in bgs) + " |")
        print("|---|" + "|".join("---" for _ in bgs) + "|")
        worst = []
        for fg in FG_ROLES:
            if fg not in p:
                continue
            cells = []
            for b in bgs:
                r = contrast(p[fg], p[b])
                g = wcag_grade(r)
                cells.append(f"{r:.2f} {g}")
                if b == bgs[0] and fg in ("text", "muted", "accent") and r < 4.5:
                    worst.append(f"  !! {fg} on {b}: {r:.2f} ({g})")
            print(f"| {fg} | " + " | ".join(cells) + " |")
        if worst:
            print("\nFAILS (text/muted/accent must be >=4.5 on primary bg):")
            print("\n".join(worst))


if __name__ == "__main__":
    main()
