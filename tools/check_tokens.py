#!/usr/bin/env python3
"""
Verify that dark color palettes in tokens/base.css remain identical.

The file defines dark colors twice: in @media (prefers-color-scheme: dark)
and in [data-theme="dark"]. Both must stay in sync per the CSS comment.
"""

import os
import re
import sys


def extract_tokens(block_text):
    """Extract {name: value} map from a CSS block."""
    tokens = {}
    # Match: --name: value;
    pattern = r"--([\w-]+)\s*:\s*([^;]+);"
    for match in re.finditer(pattern, block_text):
        name, value = match.groups()
        tokens[name] = value.strip()
    return tokens


def get_media_block(css_text):
    """Extract content of @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { ... } }"""
    # Match the entire @media block and extract the innermost { ... }
    media_match = re.search(
        r'@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{[^{}]*:root:not\(\[data-theme="light"\]\)\s*\{([^}]+)\}',
        css_text,
        re.DOTALL,
    )
    return media_match.group(1) if media_match else ""


def get_data_theme_dark_block(css_text):
    """Extract content of [data-theme="dark"] { ... }"""
    match = re.search(r'\[data-theme="dark"\]\s*\{([^}]+)\}', css_text, re.DOTALL)
    return match.group(1) if match else ""


def main():
    script_dir = os.path.dirname(__file__)
    css_path = os.path.join(script_dir, "..", "tokens", "base.css")

    try:
        with open(css_path, "r") as f:
            css_text = f.read()
    except FileNotFoundError:
        print(f"ERROR: Could not find {css_path}")
        return 1

    media_block = get_media_block(css_text)
    data_theme_block = get_data_theme_dark_block(css_text)

    if not media_block or not data_theme_block:
        print("ERROR: Could not find one or both dark palette blocks")
        return 1

    media_tokens = extract_tokens(media_block)
    data_theme_tokens = extract_tokens(data_theme_block)

    all_names = set(media_tokens.keys()) | set(data_theme_tokens.keys())
    all_names = sorted(all_names)

    mismatches = []
    for name in all_names:
        media_val = media_tokens.get(name)
        data_val = data_theme_tokens.get(name)

        if media_val != data_val:
            if media_val is None:
                mismatches.append(
                    f'  --{name}: missing in @media block, present in [data-theme="dark"] ({data_val})'
                )
            elif data_val is None:
                mismatches.append(
                    f'  --{name}: missing in [data-theme="dark"], present in @media block ({media_val})'
                )
            else:
                mismatches.append(
                    f"  --{name}: @media={media_val} vs data-theme={data_val}"
                )

    if mismatches:
        print("MISMATCH: Dark palettes differ:")
        for msg in mismatches:
            print(msg)
        return 1
    else:
        count = len(media_tokens)
        print(f"OK: dark palettes match ({count} tokens)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
