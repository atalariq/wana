# Wana yazi Flavor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a Wana **yazi flavor** (dark + light) from the canonical base24 schemes, and publish it to a private standalone repo `atalariq/wana.yazi` via `git subtree` — keeping `schemes/` the single source of truth so the flavor can never drift from the palette.

**Architecture:** Two new renderers in `tools/gen.py` emit, per variant, a yazi flavor directory `themes/yazi/wana-<variant>.yazi/` containing `flavor.toml` (a TOML theme that mirrors yazi's `theme.toml`) and `tmtheme.xml` (the code-preview theme, reusing the existing `bat.tmTheme.tmpl`). Static per-flavor files (`README.md`, `LICENSE`, `LICENSE-tmtheme`) are committed by hand. A `tools/publish.sh` runs `git subtree split --prefix=themes/yazi` and pushes to the private `wana.yazi` remote — one-way, authored only in `wana`.

**Tech Stack:** Python 3.14 stdlib (`tomllib`, `xml.etree`), `unittest`, the existing `tools/scheme.py` loader, `git subtree`, `gh` CLI.

---

## Background facts (verified during planning)

- A yazi **flavor** is a kebab-case directory ending in `.yazi` containing: `flavor.toml`, `tmtheme.xml`, `README.md`, `LICENSE`, `LICENSE-tmtheme`, and (optional) `preview.png`. Source: yazi-rs.github.io/docs/flavors/overview.
- **One variant per flavor.** The user selects them in `theme.toml`:
  ```toml
  [flavor]
  dark  = "wana-dark"
  light = "wana-light"
  ```
  So we ship **two** flavor dirs.
- `flavor.toml` mirrors `theme.toml`. Verified top-level tables: `[mgr]`, `[tabs]`, `[mode]`, `[status]`, `[pick]`, `[input]`, `[cmp]`, `[tasks]`, `[which]`, `[help]`, `[spot]`, `[notify]`, `[filetype]`, `[icon]`. Color values are hex strings `"#rrggbb"` (or the literal `"reset"`) inside inline tables like `{ fg = "#...", bg = "#...", bold = true }`.
- Inside a flavor, **do not set `[mgr] syntect_theme`** — a flavor always uses its own bundled `tmtheme.xml` for code preview. (Documented behavior.)
- The structure below is adapted from the official `catppuccin-mocha.yazi/flavor.toml` (known-good), with every color swapped for a Wana base24 slot.

**`str.format` brace escaping:** `flavor.toml` is full of literal `{ … }` TOML inline tables. `gen.py` renders templates with `str.format`, so **every literal brace must be doubled** (`{{` and `}}`); only the `{baseNN}` field placeholders stay single. Task 2 Step 4 (parse with `tomllib`) catches any miss.

**Wana base24 → yazi role mapping** (used in `flavor.toml`):

```
cwd, tabs.active.bg, mode.normal, pick/input/cmp/tasks/spot border, status.perm_type → base0D (blue)
find_keyword, marker_selected, status.perm_read, mode.unset(alt only via base09) → base0A (yellow)
find_position, pick.active, tasks.hovered, which.desc, help.run, spot.tbl_cell.fg → base0E (magenta)
marker_copied, status.perm_exec/progress_normal, notify.title_info, filetype document → base0B (green)
marker_cut, status.perm_write, notify.title_error → base08 (red)
marker_marked, mode.select, which.cand, help.on, spot.tbl_col, filetype image → base0C (cyan)
count_* fg, tabs.active.fg, mode.*_main fg → base00 (bg)
border_style, perm_sep, which.rest(base04)/separator_style → base03 (muted) / base04
progress_label, help.footer.bg → base05 (text)
inactive tab/mode/which.mask bg, tbl_cell.bg, progress_normal.bg → base01 / base02
unset mode, notify.title_warn(base0A) → base09 (orange)
```

---

## File Structure

| Path                                                              | Responsibility                                                  | Status    |
| ----------------------------------------------------------------- | --------------------------------------------------------------- | --------- |
| `tools/templates/yazi.flavor.toml.tmpl`                           | yazi `flavor.toml` template (base24 placeholders)               | create    |
| `tools/gen.py`                                                    | Add `render_yazi_flavor` + `render_yazi_tmtheme`; register both | modify    |
| `themes/yazi/wana-dark.yazi/flavor.toml`                          | Generated dark flavor config                                    | generated |
| `themes/yazi/wana-dark.yazi/tmtheme.xml`                          | Generated dark code-preview theme                               | generated |
| `themes/yazi/wana-light.yazi/flavor.toml`                         | Generated light flavor config                                   | generated |
| `themes/yazi/wana-light.yazi/tmtheme.xml`                         | Generated light code-preview theme                              | generated |
| `themes/yazi/wana-dark.yazi/{README.md,LICENSE,LICENSE-tmtheme}`  | Static per-flavor files                                         | create    |
| `themes/yazi/wana-light.yazi/{README.md,LICENSE,LICENSE-tmtheme}` | Static per-flavor files                                         | create    |
| `tools/test_gen.py`                                               | Add yazi flavor assertions                                      | modify    |
| `tools/publish.sh`                                                | `git subtree split` + push to standalone private repos          | create    |
| `AGENTS.md`, `README.md`                                          | Document yazi target + publish flow                             | modify    |

---

## Task 1: yazi tmtheme renderer (reuse bat template)

The code-preview theme is identical in spirit to bat's tmTheme. Reuse `bat.tmTheme.tmpl` verbatim, just write it to the flavor dir.

**Files:**

- Modify: `tools/gen.py`
- Test: `tools/test_gen.py`

- [ ] **Step 1: Write the failing test**

Add to `tools/test_gen.py`:

```python
    def test_yazi_tmtheme_is_valid_xml(self):
        import xml.etree.ElementTree as ET

        files = gen.build()
        dark = files["themes/yazi/wana-dark.yazi/tmtheme.xml"]
        ET.fromstring(dark)  # raises if malformed
        self.assertIn("wana-dark", dark)
        self.assertIn("#", dark)
```

- [ ] **Step 2: Run test, verify it fails**

Run: `python3 tools/test_gen.py TestGen.test_yazi_tmtheme_is_valid_xml`
Expected: FAIL with `KeyError: 'themes/yazi/wana-dark.yazi/tmtheme.xml'`.

- [ ] **Step 3: Add `render_yazi_tmtheme` to `tools/gen.py`**

Add after `render_bat` (it reuses the same template):

```python
def render_yazi_tmtheme(s: Scheme) -> tuple[str, str]:
    with open(os.path.join(TPL, "bat.tmTheme.tmpl")) as f:
        tpl = f.read()
    fields = {"name": f"wana-{s.variant}"}
    fields.update({f"base{n:02X}": s.hex(f"base{n:02X}") for n in range(16)})
    out = tpl.format(**fields)
    rel = f"themes/yazi/wana-{s.variant}.yazi/tmtheme.xml"
    return rel, out
```

Register it in `RENDERERS` (add the line):

```python
    render_yazi_tmtheme,
```

- [ ] **Step 4: Generate and run test**

Run: `python3 tools/gen.py && python3 tools/test_gen.py TestGen.test_yazi_tmtheme_is_valid_xml`
Expected: prints `wrote themes/yazi/wana-dark.yazi/tmtheme.xml` (and light), test PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/gen.py tools/test_gen.py themes/yazi/
git commit -m "feat(gen): add yazi tmtheme renderer"
```

---

## Task 2: yazi flavor.toml renderer

The flavor config. Template is adapted from catppuccin-mocha's `flavor.toml`, recolored to Wana base24. **Remember: every literal `{`/`}` is doubled.**

**Files:**

- Create: `tools/templates/yazi.flavor.toml.tmpl`
- Modify: `tools/gen.py`
- Test: `tools/test_gen.py`

- [ ] **Step 1: Write the failing test**

Add to `tools/test_gen.py`:

```python
    def test_yazi_flavor_is_valid_toml(self):
        import tomllib

        files = gen.build()
        raw = files["themes/yazi/wana-dark.yazi/flavor.toml"]
        data = tomllib.loads(raw)  # raises if malformed
        for section in ("mgr", "mode", "status", "tabs", "which", "filetype"):
            self.assertIn(section, data, f"missing [{section}]")
        # flavor uses its own tmtheme -> must NOT set syntect_theme
        self.assertNotIn("syntect_theme", data["mgr"])
        # cwd is the dark blue (base0D)
        self.assertEqual(data["mgr"]["cwd"]["fg"].lower(), "#80b7f0")
```

- [ ] **Step 2: Run test, verify it fails**

Run: `python3 tools/test_gen.py TestGen.test_yazi_flavor_is_valid_toml`
Expected: FAIL with `KeyError: 'themes/yazi/wana-dark.yazi/flavor.toml'`.

- [ ] **Step 3: Write `tools/templates/yazi.flavor.toml.tmpl`**

```toml
# GENERATED by tools/gen.py from schemes/ — do not edit.
# Wana — yazi flavor

[mgr]
cwd = {{ fg = "{base0D}" }}

find_keyword  = {{ fg = "{base0A}", bold = true, italic = true, underline = true }}
find_position = {{ fg = "{base0E}", bg = "reset", bold = true, italic = true }}

marker_copied   = {{ fg = "{base0B}", bg = "{base0B}" }}
marker_cut      = {{ fg = "{base08}", bg = "{base08}" }}
marker_marked   = {{ fg = "{base0C}", bg = "{base0C}" }}
marker_selected = {{ fg = "{base0A}", bg = "{base0A}" }}

count_copied   = {{ fg = "{base00}", bg = "{base0B}" }}
count_cut      = {{ fg = "{base00}", bg = "{base08}" }}
count_selected = {{ fg = "{base00}", bg = "{base0A}" }}

border_symbol = "│"
border_style  = {{ fg = "{base03}" }}

[tabs]
active   = {{ fg = "{base00}", bg = "{base0D}", bold = true }}
inactive = {{ fg = "{base0D}", bg = "{base01}" }}

[mode]
normal_main = {{ fg = "{base00}", bg = "{base0D}", bold = true }}
normal_alt  = {{ fg = "{base0D}", bg = "{base01}" }}

select_main = {{ fg = "{base00}", bg = "{base0C}", bold = true }}
select_alt  = {{ fg = "{base0C}", bg = "{base01}" }}

unset_main = {{ fg = "{base00}", bg = "{base09}", bold = true }}
unset_alt  = {{ fg = "{base09}", bg = "{base01}" }}

[status]
perm_sep   = {{ fg = "{base03}" }}
perm_type  = {{ fg = "{base0D}" }}
perm_read  = {{ fg = "{base0A}" }}
perm_write = {{ fg = "{base08}" }}
perm_exec  = {{ fg = "{base0B}" }}

progress_label  = {{ fg = "{base05}", bold = true }}
progress_normal = {{ fg = "{base0B}", bg = "{base02}" }}
progress_error  = {{ fg = "{base0A}", bg = "{base08}" }}

[pick]
border   = {{ fg = "{base0D}" }}
active   = {{ fg = "{base0E}", bold = true }}
inactive = {{}}

[input]
border   = {{ fg = "{base0D}" }}
title    = {{}}
value    = {{}}
selected = {{ reversed = true }}

[cmp]
border = {{ fg = "{base0D}" }}

[tasks]
border  = {{ fg = "{base0D}" }}
title   = {{}}
hovered = {{ fg = "{base0E}", bold = true }}

[which]
mask            = {{ bg = "{base01}" }}
cand            = {{ fg = "{base0C}" }}
rest            = {{ fg = "{base04}" }}
desc            = {{ fg = "{base0E}" }}
separator       = "  "
separator_style = {{ fg = "{base03}" }}

[help]
on      = {{ fg = "{base0C}" }}
run     = {{ fg = "{base0E}" }}
hovered = {{ reversed = true, bold = true }}
footer  = {{ fg = "{base01}", bg = "{base05}" }}

[spot]
border   = {{ fg = "{base0D}" }}
title    = {{ fg = "{base0D}" }}
tbl_col  = {{ fg = "{base0C}" }}
tbl_cell = {{ fg = "{base0E}", bg = "{base02}" }}

[notify]
title_info  = {{ fg = "{base0B}" }}
title_warn  = {{ fg = "{base0A}" }}
title_error = {{ fg = "{base08}" }}

[filetype]
rules = [
	{{ mime = "image/*", fg = "{base0C}" }},
	{{ mime = "{{audio,video}}/*", fg = "{base0A}" }},
	{{ mime = "application/{{zip,rar,7z*,tar,gzip,xz,zstd,bzip*,lzma,compress,archive,cpio,arj,xar,ms-cab*}}", fg = "{base0E}" }},
	{{ mime = "application/{{pdf,doc,rtf}}", fg = "{base0B}" }},
	{{ mime = "vfs/{{absent,stale}}", fg = "{base04}" }},
	{{ url = "*", fg = "{base05}" }},
	{{ url = "*/", fg = "{base0D}" }},
]
```

Note the **triple-brace cases**: `{{audio,video}}` and the archive/pdf globs are literal yazi brace-globs, so each literal `{`/`}` is doubled — `{{audio,video}}` renders to `{audio,video}`.

- [ ] **Step 4: Add `render_yazi_flavor` to `tools/gen.py`**

Add after `render_yazi_tmtheme`:

```python
def render_yazi_flavor(s: Scheme) -> tuple[str, str]:
    with open(os.path.join(TPL, "yazi.flavor.toml.tmpl")) as f:
        tpl = f.read()
    fields = {f"base{n:02X}": s.hex(f"base{n:02X}") for n in range(24)}
    out = tpl.format(**fields)
    rel = f"themes/yazi/wana-{s.variant}.yazi/flavor.toml"
    return rel, out
```

Register in `RENDERERS`:

```python
    render_yazi_flavor,
```

- [ ] **Step 5: Generate and run test**

Run: `python3 tools/gen.py && python3 tools/test_gen.py TestGen.test_yazi_flavor_is_valid_toml`
Expected: writes both `flavor.toml` files; test PASS. If `tomllib.loads` raises, a literal brace was not doubled — find it in the `.tmpl` and double it.

- [ ] **Step 6: Commit**

```bash
git add tools/gen.py tools/templates/yazi.flavor.toml.tmpl themes/yazi/
git commit -m "feat(gen): add yazi flavor.toml renderer"
```

---

## Task 3: Static per-flavor files (README, LICENSE)

Each flavor dir needs `README.md`, `LICENSE`, `LICENSE-tmtheme`. These are static (not generated). `preview.png` is intentionally deferred — a flavor loads without it; capture screenshots after first install.

**Files:**

- Create: `themes/yazi/wana-dark.yazi/README.md`, `themes/yazi/wana-light.yazi/README.md`
- Create: `themes/yazi/wana-{dark,light}.yazi/LICENSE`, `…/LICENSE-tmtheme`

- [ ] **Step 1: Write `themes/yazi/wana-dark.yazi/README.md`**

````markdown
# Wana Dark — yazi flavor

A warm, bookish Gruvbox-leaning flavor for [yazi](https://github.com/sxyazi/yazi),
generated from the canonical [Wana](https://github.com/atalariq/wana) base24 palette.

## Install

```sh
ya pkg add atalariq/wana.yazi:wana-dark
```
````

Then in `~/.config/yazi/theme.toml`:

```toml
[flavor]
dark = "wana-dark"
```

> Generated — do not hand-edit. Source of truth: `schemes/wana-dark.yaml` in atalariq/wana.

````

- [ ] **Step 2: Write `themes/yazi/wana-light.yazi/README.md`**

Same as Step 1, replacing `dark` → `light` and `Dark` → `Light` throughout.

- [ ] **Step 3: Add LICENSE files**

Copy the repo's license intent (MIT, author atalariq). Run:

```bash
for d in themes/yazi/wana-dark.yazi themes/yazi/wana-light.yazi; do
  cat > "$d/LICENSE" <<'EOF'
MIT License

Copyright (c) 2026 atalariq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
  cp "$d/LICENSE" "$d/LICENSE-tmtheme"
done
````

- [ ] **Step 4: Commit**

```bash
git add themes/yazi/
git commit -m "docs(yazi): add per-flavor README and LICENSE files"
```

---

## Task 4: Lock freshness + count check

Make sure the four generated yazi files stay in sync and the suite is green.

**Files:**

- Modify: `tools/test_gen.py`

- [ ] **Step 1: Add a count assertion**

Add to `tools/test_gen.py`:

```python
    def test_yazi_emits_two_flavors(self):
        files = gen.build()
        yazi = [k for k in files if k.startswith("themes/yazi/")]
        # 2 variants x (flavor.toml + tmtheme.xml)
        self.assertEqual(len(yazi), 4, yazi)
```

- [ ] **Step 2: Run the whole suite**

Run: `python3 -m pytest tools/ -q`
Expected: all green (existing 49 + the new yazi tests). `test_check_is_clean` confirms generated files match committed.

- [ ] **Step 3: Commit**

```bash
git add tools/test_gen.py
git commit -m "test(gen): assert yazi emits two complete flavors"
```

---

## Task 5: `tools/publish.sh` — subtree publish to private standalone repo

One-way publish from `wana` to the private `atalariq/wana.yazi`. Authored only here; the standalone repo is a generated mirror.

**Files:**

- Create: `tools/publish.sh`

- [ ] **Step 1: Write `tools/publish.sh`**

```bash
#!/usr/bin/env bash
# Publish a generated subtree to its standalone private repo (one-way).
#
#   tools/publish.sh yazi      # push themes/yazi -> atalariq/wana.yazi
#   tools/publish.sh nvim      # push themes/nvim -> atalariq/wana.nvim
#   tools/publish.sh all
#
# We only ever author in this repo, so the split history is linear and pushes
# fast-forward. If a push is rejected, re-run with FORCE=1.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

publish() {
  local name="$1" prefix="$2" url="$3" branch="_dist_${1}"
  [ -d "$prefix" ] || { echo "skip $name: $prefix missing"; return 0; }
  git remote get-url "$name" >/dev/null 2>&1 || git remote add "$name" "$url"
  git subtree split --prefix="$prefix" -b "$branch"
  if [ "${FORCE:-0}" = "1" ]; then
    git push --force "$name" "$branch:main"
  else
    git push "$name" "$branch:main"
  fi
  git branch -D "$branch"
  echo "published $prefix -> $url (main)"
}

case "${1:-all}" in
  yazi) publish wana-yazi themes/yazi "git@github.com:atalariq/wana.yazi.git" ;;
  nvim) publish wana-nvim themes/nvim "git@github.com:atalariq/wana.nvim.git" ;;
  all)
    publish wana-yazi themes/yazi "git@github.com:atalariq/wana.yazi.git"
    publish wana-nvim themes/nvim "git@github.com:atalariq/wana.nvim.git"
    ;;
  *) echo "usage: tools/publish.sh [yazi|nvim|all]" >&2; exit 2 ;;
esac
```

- [ ] **Step 2: Make it executable + smoke-test the split (no push)**

```bash
chmod +x tools/publish.sh
git subtree split --prefix=themes/yazi -b _smoke && git branch -D _smoke
```

Expected: prints a commit SHA (the synthetic subtree root). The branch delete confirms the split works. No network yet.

- [ ] **Step 3: Commit**

```bash
git add tools/publish.sh
git commit -m "chore(tools): add subtree publish script for standalone repos"
```

---

## Task 6: Create the private repo + first publish (outward-facing — user-confirmed)

Repos are **private** (confirmed). These steps touch GitHub; run them deliberately.

- [ ] **Step 1: Create the private repo**

```bash
gh repo create atalariq/wana.yazi --private \
  --description "Wana flavor for yazi (generated from atalariq/wana)"
```

Expected: `✓ Created repository atalariq/wana.yazi`.

- [ ] **Step 2: Publish**

Run: `tools/publish.sh yazi`
Expected: `published themes/yazi -> git@github.com:atalariq/wana.yazi.git (main)`.

- [ ] **Step 3: Verify the mirror layout**

```bash
gh api repos/atalariq/wana.yazi/contents | python3 -c "import sys,json;print([x['name'] for x in json.load(sys.stdin)])"
```

Expected: `['wana-dark.yazi', 'wana-light.yazi']` — the flavor dirs are at the repo root (correct for `ya pkg add`).

---

## Task 7: Document the yazi target + publish flow

**Files:**

- Modify: `AGENTS.md` (tree listing), `README.md` (App themes section)

- [ ] **Step 1: Add yazi to the `AGENTS.md` tree**

Under `themes/`, add:

```
  yazi/                    # GENERATED yazi flavors -> atalariq/wana.yazi (private)
    wana-dark.yazi/
    wana-light.yazi/
```

- [ ] **Step 2: Note the publish flow in `README.md`**

In the App themes section add:

```markdown
### Standalone repos

Some targets ship as their own installable repos, generated from `schemes/`
and published one-way with `tools/publish.sh`:

- `themes/yazi/` → `atalariq/wana.yazi` (install: `ya pkg add atalariq/wana.yazi:wana-dark`)
```

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md README.md
git commit -m "docs: document yazi flavor target and subtree publish flow"
```

---

## Self-review notes

- **Spec coverage:** generated flavor (Tasks 1–2), static flavor files (3), freshness/drift via `gen --check` + count (4), subtree publish (5), private repo creation + first push (6), docs (7). Single source of truth preserved — every color comes from `schemes/` through `gen.py`, so the drift guarantee from `test_gen.py::test_check_is_clean` extends to yazi.
- **Brace escaping:** the one real footgun (literal TOML braces under `str.format`) is caught by `tomllib.loads` in Task 2 Step 5.
- **Out of scope:** nvim (separate plan `2026-06-26-wana-nvim-colorscheme.md`), `preview.png` screenshots (post-install follow-up), making the repo public.

```

```
