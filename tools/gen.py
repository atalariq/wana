#!/usr/bin/env python3
"""Generate app themes from schemes/*.yaml into themes/.

    python3 tools/gen.py          # regenerate all themes
    python3 tools/gen.py --check  # exit 1 if any committed theme is stale

Add a new target by writing tools/templates/<x> and a render_<x>() below.
Templates are str.format strings: any LITERAL brace in a target's config
(e.g. JSON for noctalia) must be escaped as {{ }} or it will break rendering.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scheme import Scheme, load  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
TPL = os.path.join(os.path.dirname(__file__), "templates")
SCHEMES = {"dark": "wana-dark.yaml", "light": "wana-light.yaml"}


def _scheme(variant: str) -> Scheme:
    return load(os.path.join(ROOT, "schemes", SCHEMES[variant]))


def _term_fields(s: Scheme) -> dict:
    a = s.ansi16()
    fields = {f"c{i}": a[i] for i in range(16)}
    fields.update(
        name=s.name,
        bg=s.hex("base00"),
        fg=s.hex("base05"),
        cursor=s.hex("base0B"),  # accent green caret
        sel_bg=s.hex("base02"),
        sel_fg=s.hex("base05"),
    )
    return fields


def render_kitty(s: Scheme) -> tuple[str, str]:
    with open(os.path.join(TPL, "kitty.conf.tmpl")) as f:
        tpl = f.read()
    out = tpl.format(**_term_fields(s))
    rel = f"themes/kitty/wana-{s.variant}.conf"
    return rel, out


def render_alacritty(s: Scheme) -> tuple[str, str]:
    with open(os.path.join(TPL, "alacritty.toml.tmpl")) as f:
        tpl = f.read()
    out = tpl.format(**_term_fields(s))
    rel = f"themes/alacritty/wana-{s.variant}.toml"
    return rel, out


def render_tty(s: Scheme) -> tuple[str, str]:
    with open(os.path.join(TPL, "tty.sh.tmpl")) as f:
        tpl = f.read()
    a = s.ansi16()
    fields = {"name": s.name}
    fields.update({f"c{i}s": a[i].lstrip("#") for i in range(16)})
    out = tpl.format(**fields)
    rel = f"themes/tty/wana-{s.variant}.sh"
    return rel, out


def render_pywal(s: Scheme) -> tuple[str, str]:
    with open(os.path.join(TPL, "pywal.json.tmpl")) as f:
        tpl = f.read()
    out = tpl.format(**_term_fields(s))
    rel = f"themes/pywal/wana-{s.variant}.json"
    return rel, out


def render_fzf(s: Scheme) -> tuple[str, str]:
    with open(os.path.join(TPL, "fzf.opts.tmpl")) as f:
        tpl = f.read()
    out = tpl.format(**_term_fields(s))
    rel = f"themes/fzf/wana-{s.variant}.opts"
    return rel, out


def render_bat(s: Scheme) -> tuple[str, str]:
    with open(os.path.join(TPL, "bat.tmTheme.tmpl")) as f:
        tpl = f.read()
    fields = {"name": f"wana-{s.variant}"}
    fields.update({f"base{n:02X}": s.hex(f"base{n:02X}") for n in range(16)})
    out = tpl.format(**fields)
    rel = f"themes/bat/wana-{s.variant}.tmTheme"
    return rel, out


def render_starship(s: Scheme) -> tuple[str, str]:
    d = _scheme("dark")
    with open(os.path.join(TPL, "starship.toml.tmpl")) as f:
        tpl = f.read()
    fields = {f"base{n:02X}": d.hex(f"base{n:02X}") for n in range(24)}
    out = tpl.format(**fields)
    return "themes/starship/wana.toml", out


def render_btop(s: Scheme) -> tuple[str, str]:
    with open(os.path.join(TPL, "btop.theme.tmpl")) as f:
        tpl = f.read()
    out = tpl.format(**_term_fields(s))
    rel = f"themes/btop/wana-{s.variant}.theme"
    return rel, out


RENDERERS = [
    render_kitty,
    render_alacritty,
    render_tty,
    render_pywal,
    render_fzf,
    render_bat,
    render_starship,
    render_btop,
]


def build() -> dict:
    """Return {relative_path: content} for every target/flavor."""
    files = {}
    for variant, fname in SCHEMES.items():
        s = load(os.path.join(ROOT, "schemes", fname))
        for render in RENDERERS:
            rel, content = render(s)
            files[rel] = content
    return files


def main(argv: list[str]) -> int:
    check = "--check" in argv
    files = build()
    stale = []
    for rel, content in files.items():
        path = os.path.join(ROOT, rel)
        if os.path.exists(path):
            with open(path) as f:
                existing = f.read()
        else:
            existing = None
        if check:
            if existing != content:
                stale.append(rel)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            print(f"wrote {rel}")
    if check and stale:
        print("STALE (run tools/gen.py):")
        for rel in stale:
            print(f"  {rel}")
        return 1
    if check:
        print(f"OK: {len(files)} themes up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
