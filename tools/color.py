#!/usr/bin/env python3
"""Color math for the design system.

Computes WCAG contrast ratios and OKLCH conversions from real math
(no guessing). Used to generate the contrast tables in research/ and
proposals/.

Usage:
    python3 tools/color.py convert "hsl(40 30% 98%)"
    python3 tools/color.py contrast "#1c1b1a" "#fffcf0"
    python3 tools/color.py table <colors.json>   # batch contrast matrix
"""

from __future__ import annotations

import json
import math
import re
import sys


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse(color: str) -> tuple[float, float, float]:
    """Parse a color string to sRGB floats in [0, 1]."""
    color = color.strip()
    if color.startswith("#"):
        return hex_to_rgb(color)
    m = re.match(r"hsla?\(\s*([\d.]+)[ ,]+([\d.]+)%[ ,]+([\d.]+)%", color)
    if m:
        h, s, l = float(m[1]), float(m[2]) / 100, float(m[3]) / 100
        return hsl_to_rgb(h, s, l)
    raise ValueError(f"cannot parse color: {color!r}")


def hex_to_rgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore


def hsl_to_rgb(h: float, s: float, l: float) -> tuple[float, float, float]:
    h = h % 360
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return (r + m, g + m, b + m)


# ---------------------------------------------------------------------------
# Output formats
# ---------------------------------------------------------------------------


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb)


def rgb_to_hsl(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    l = (mx + mn) / 2
    if mx == mn:
        return (0.0, 0.0, round(l * 100, 1))
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = (g - b) / d + (6 if g < b else 0)
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return (round(h * 60, 1), round(s * 100, 1), round(l * 100, 1))


# ---------------------------------------------------------------------------
# OKLCH (Björn Ottosson's OKLab)
# ---------------------------------------------------------------------------


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgb_to_oklch(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (_srgb_to_linear(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    C = math.hypot(a, bb)
    H = math.degrees(math.atan2(bb, a)) % 360
    return (round(L * 100, 1), round(C, 3), round(H, 1))


def oklch_str(rgb: tuple[float, float, float]) -> str:
    L, C, H = rgb_to_oklch(rgb)
    return f"oklch({L}% {C} {H})"


# ---------------------------------------------------------------------------
# WCAG contrast
# ---------------------------------------------------------------------------


def relative_luminance(rgb: tuple[float, float, float]) -> float:
    r, g, b = (_srgb_to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(c1: str, c2: str) -> float:
    l1 = relative_luminance(parse(c1))
    l2 = relative_luminance(parse(c2))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def wcag_grade(ratio: float, large: bool = False) -> str:
    """Return the highest WCAG grade a ratio passes for normal/large text."""
    if large:
        if ratio >= 4.5:
            return "AAA"
        if ratio >= 3.0:
            return "AA"
        return "fail"
    if ratio >= 7.0:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3.0:
        return "AA-large"
    return "fail"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def cmd_convert(color: str) -> None:
    rgb = parse(color)
    h, s, l = rgb_to_hsl(rgb)
    print(f"input : {color}")
    print(f"hex   : {rgb_to_hex(rgb)}")
    print(f"hsl   : hsl({h} {s}% {l}%)")
    print(f"oklch : {oklch_str(rgb)}")
    print(f"lum   : {relative_luminance(rgb):.4f}")


def cmd_contrast(c1: str, c2: str) -> None:
    r = contrast(c1, c2)
    print(f"{c1} on {c2}")
    print(f"ratio : {r:.2f}:1")
    print(f"normal: {wcag_grade(r)}")
    print(f"large : {wcag_grade(r, large=True)}")


def cmd_table(path: str) -> None:
    """colors.json: {"fg": {...}, "bg": {...}} -> contrast matrix (markdown)."""
    data = json.load(open(path))
    fgs, bgs = data["fg"], data["bg"]
    header = "| fg \\ bg | " + " | ".join(bgs) + " |"
    sep = "|---|" + "|".join("---" for _ in bgs) + "|"
    print(header)
    print(sep)
    for fname, fval in fgs.items():
        cells = []
        for bval in bgs.values():
            r = contrast(fval, bval)
            cells.append(f"{r:.2f} {wcag_grade(r)}")
        print(f"| {fname} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd, *rest = args
    if cmd == "convert":
        cmd_convert(rest[0])
    elif cmd == "contrast":
        cmd_contrast(rest[0], rest[1])
    elif cmd == "table":
        cmd_table(rest[0])
    else:
        print(f"unknown command: {cmd}")
        sys.exit(1)
