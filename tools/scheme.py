#!/usr/bin/env python3
"""Load a base24 YAML scheme and expose its palette + ANSI-16 mapping.

A base24 scheme has 24 colour slots base00..base17. The standard terminal
mapping (tinted-theming) turns those into 16 ANSI colours.
"""

from __future__ import annotations

from dataclasses import dataclass

import yaml

SLOTS = [f"base{n:02X}" for n in range(24)]  # base00..base17 (hex-cased)

# Standard base24 -> 16-colour terminal mapping (index = ANSI colour number).
ANSI16_SLOTS = [
    "base01",
    "base08",
    "base0B",
    "base0A",
    "base0D",
    "base0E",
    "base0C",
    "base05",
    "base03",
    "base12",
    "base14",
    "base13",
    "base16",
    "base17",
    "base15",
    "base07",
]


@dataclass
class Scheme:
    name: str
    variant: str  # "light" | "dark"
    palette: dict[str, str]  # slot -> 6-digit hex WITHOUT leading '#'

    def hex(self, slot: str) -> str:
        return "#" + self.palette[slot].lstrip("#").lower()

    def ansi16(self) -> list[str]:
        return [self.hex(s) for s in ANSI16_SLOTS]

    def validate(self) -> "Scheme":
        for slot in SLOTS:
            v = self.palette.get(slot)
            if v is None:
                raise ValueError(f"{self.name}: missing slot {slot}")
            digits = v.lstrip("#")
            if len(digits) != 6 or any(
                c not in "0123456789abcdefABCDEF" for c in digits
            ):
                raise ValueError(f"{self.name}: {slot} not 6-digit hex: {v!r}")
        return self


def load(path: str) -> Scheme:
    with open(path) as f:
        data = yaml.safe_load(f)
    return Scheme(
        name=data["name"],
        variant=data.get("variant", "dark"),
        palette={k: v for k, v in data["palette"].items()},
    ).validate()
