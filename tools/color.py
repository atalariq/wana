#!/usr/bin/env python3
"""Color math for Wana.

Computes WCAG contrast ratios and OKLCH conversions from real math
(no guessing). Used to generate the contrast tables in research/ and
proposals/.

Usage:
    python3 tools/color.py convert "hsl(40 30% 98%)"
    python3 tools/color.py contrast "#1c1b1a" "#fffcf0"
    python3 tools/color.py oklch "48.3% 0.10 150" "#fffcf0"  # oklch -> hex (+contrast)
    python3 tools/color.py fit 0.10 150 "#fffcf0" 6.0 light  # find lightness for target
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


def _linear_to_srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))  # clamp out-of-gamut, matching the browser canvas
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def oklch_to_rgb(L: float, C: float, H: float) -> tuple[float, float, float]:
    """OKLCH (L in [0,1]) → gamut-clamped sRGB floats in [0,1]."""
    h = math.radians(H)
    a, b = C * math.cos(h), C * math.sin(h)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_**3, m_**3, s_**3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return tuple(_linear_to_srgb(c) for c in (r, g, bb))  # type: ignore


def parse_oklch(spec: str) -> tuple[float, float, float]:
    """Parse 'oklch(50% 0.1 150)' or '50 0.1 150' → (L[0,1], C, H)."""
    s = spec.strip().lower().replace("oklch(", "").replace(")", "").replace("%", "")
    parts = re.split(r"[ ,/]+", s.strip())
    L, C, H = float(parts[0]), float(parts[1]), float(parts[2])
    if L > 1:  # accept percent form
        L /= 100
    return L, C, H


def fit_lightness(
    C: float, H: float, bg: str, target: float, mode: str
) -> tuple[float, tuple[float, float, float], float]:
    """Binary-search OKLCH lightness (fixed C/H) to hit `target` contrast vs bg.

    mode='light' → dark accent on a light bg; 'dark' → light accent on dark bg.
    Returns (L[0,1], rgb, ratio).
    """
    lo, hi = (0.15, 0.75) if mode == "light" else (0.5, 0.97)
    bg_lum = relative_luminance(parse(bg))
    best = (0.0, (0.0, 0.0, 0.0), 0.0)
    for _ in range(28):
        L = (lo + hi) / 2
        rgb = oklch_to_rgb(L, C, H)
        fg_lum = relative_luminance(rgb)
        ph, pl = max(fg_lum, bg_lum), min(fg_lum, bg_lum)
        ratio = (ph + 0.05) / (pl + 0.05)
        best = (L, rgb, ratio)
        too_much = ratio > target
        if mode == "light":
            lo, hi = (L, hi) if too_much else (lo, L)
        else:
            lo, hi = (lo, L) if too_much else (L, hi)
    return best


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


def cmd_oklch(spec: str, bg: str | None = None) -> None:
    """oklch '50% 0.1 150' [bg] → hex + (optional) contrast vs bg."""
    L, C, H = parse_oklch(spec)
    rgb = oklch_to_rgb(L, C, H)
    print(f"oklch : oklch({L * 100:.1f}% {C} {H})")
    print(f"hex   : {rgb_to_hex(rgb)}")
    if bg:
        r = contrast(rgb_to_hex(rgb), bg)
        print(f"vs {bg}: {r:.2f}:1  normal {wcag_grade(r)}")


def cmd_fit(C: str, H: str, bg: str, target: str, mode: str) -> None:
    """fit <C> <H> <bg> <target> <light|dark> → lightness hitting target contrast."""
    L, rgb, ratio = fit_lightness(float(C), float(H), bg, float(target), mode)
    print(f"oklch : oklch({L * 100:.1f}% {C} {H})")
    print(f"hex   : {rgb_to_hex(rgb)}")
    print(f"vs {bg}: {ratio:.2f}:1  normal {wcag_grade(ratio)}")


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
    elif cmd == "oklch":
        cmd_oklch(rest[0], rest[1] if len(rest) > 1 else None)
    elif cmd == "fit":
        cmd_fit(*rest)
    elif cmd == "table":
        cmd_table(rest[0])
    else:
        print(f"unknown command: {cmd}")
        sys.exit(1)
