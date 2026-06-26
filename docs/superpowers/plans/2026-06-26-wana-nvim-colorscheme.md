# Wana nvim Colorscheme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a real Neovim colorscheme `wana.nvim` (dark + light) as a Lua plugin in a private standalone repo `atalariq/wana.nvim`, where the **palette is generated** from the canonical base24 schemes (anti-drift) and the **highlight groups are hand-authored** (quality) — avoiding the flat look of a pure base16 dump.

**Architecture:** `tools/gen.py` gains `render_nvim_palette`, emitting `themes/nvim/lua/wana/palette.lua` — a Lua table `{ dark = {...}, light = {...} }` with named roles mapped from base24. The rest of the plugin is hand-authored and lives under `themes/nvim/`: `lua/wana/highlights.lua` (the design work — a `function(palette) -> {group = spec}` table), `lua/wana/init.lua` (load logic), and `colors/wana.lua` (the `:colorscheme wana` entry point). `tools/publish.sh nvim` subtree-splits `themes/nvim/` to the private repo. Only the palette is generated, so it never drifts; highlights are authored once and extended over time.

**Tech Stack:** Python 3.14 stdlib + `tools/scheme.py` (palette generation), Lua 5.1/LuaJIT (the plugin), Neovim ≥ 0.9 (`nvim_set_hl`, treesitter `@`-captures), `git subtree`, `gh`.

---

## Background facts (verified during planning)

- A modern Neovim colorscheme is a plugin: `colors/wana.lua` is what `:colorscheme wana` runs; it calls into `lua/wana/`. Plugin managers install it from a git repo (`{ "atalariq/wana.nvim" }`) — hence a standalone repo, not a file in `themes/`.
- `vim.o.background` (`"dark"`/`"light"`) selects the variant at load time; `nvim_set_hl(0, group, spec)` sets each highlight where `spec` is `{ fg = "#rrggbb", bg = ..., bold = ..., italic = ..., sp = ..., undercurl = ..., link = "Other" }`.
- The split: **palette is data** (generate it, single source of truth) — **highlights are design** (hand-author the base24-role → highlight-group mapping). This is how quality "generated" themes stay both correct and good.

**base24 → nvim role mapping** (used by `render_nvim_palette`):

```
bg=base00  bg_dim=base10  bg_alt=base01  surface=base01  sel=base02  overlay=base02
muted=base03  fg_dim=base04  fg=base05  fg_bright=base07
red=base08  orange=base09  yellow=base0A  green=base0B  cyan=base0C
blue=base0D  magenta=base0E  brown=base0F
br_red=base12  br_yellow=base13  br_green=base14  br_cyan=base15  br_blue=base16  br_magenta=base17
```

---

## File Structure

| Path                                           | Responsibility                                                  | Status    |
| ---------------------------------------------- | --------------------------------------------------------------- | --------- |
| `tools/gen.py`                                 | Add `render_nvim_palette` (emits Lua palette from both schemes) | modify    |
| `themes/nvim/lua/wana/palette.lua`             | GENERATED `{ dark=…, light=… }` color table                     | generated |
| `themes/nvim/lua/wana/highlights.lua`          | Hand-authored `function(p) -> groups`                           | create    |
| `themes/nvim/lua/wana/init.lua`                | `M.load()` / `M.setup()` — apply highlights                     | create    |
| `themes/nvim/colors/wana.lua`                  | `:colorscheme wana` entry point                                 | create    |
| `themes/nvim/README.md`, `themes/nvim/LICENSE` | Plugin docs + license                                           | create    |
| `tools/test_gen.py`                            | Assert palette.lua generated + both variants + hex shape        | modify    |
| `tools/publish.sh`                             | (from yazi plan) already supports `nvim`                        | reuse     |
| `AGENTS.md`, `README.md`                       | Document nvim target                                            | modify    |

> **Dependency:** Task 5 (publish) reuses `tools/publish.sh` created in the yazi plan (`2026-06-26-wana-yazi-flavor.md`, Task 5). If that script doesn't exist yet, create it from that plan first.

---

## Task 1: `render_nvim_palette` — generate the Lua palette

Emit a Lua module holding both variants, derived from `schemes/`. This is the only generated file in the plugin.

**Files:**

- Modify: `tools/gen.py`
- Test: `tools/test_gen.py`

- [ ] **Step 1: Write the failing test**

Add to `tools/test_gen.py`:

```python
    def test_nvim_palette_has_both_variants(self):
        import re

        files = gen.build()
        lua = files["themes/nvim/lua/wana/palette.lua"]
        self.assertIn("dark = {", lua)
        self.assertIn("light = {", lua)
        # named roles present, mapped to 6-digit hex
        self.assertRegex(lua, r'green\s*=\s*"#7abb87"')
        hexes = re.findall(r'"(#[0-9a-fA-F]{6})"', lua)
        self.assertGreaterEqual(len(hexes), 2 * 20)  # ~20 roles x 2 variants
```

- [ ] **Step 2: Run test, verify it fails**

Run: `python3 tools/test_gen.py TestGen.test_nvim_palette_has_both_variants`
Expected: FAIL with `KeyError: 'themes/nvim/lua/wana/palette.lua'`.

- [ ] **Step 3: Add `render_nvim_palette` to `tools/gen.py`**

Add (it reads both schemes, ignores the passed `s`, like `render_starship`):

```python
# nvim role -> base24 slot
NVIM_ROLES = {
    "bg": "base00", "bg_dim": "base10", "bg_alt": "base01", "surface": "base01",
    "sel": "base02", "overlay": "base02", "muted": "base03", "fg_dim": "base04",
    "fg": "base05", "fg_bright": "base07",
    "red": "base08", "orange": "base09", "yellow": "base0A", "green": "base0B",
    "cyan": "base0C", "blue": "base0D", "magenta": "base0E", "brown": "base0F",
    "br_red": "base12", "br_yellow": "base13", "br_green": "base14",
    "br_cyan": "base15", "br_blue": "base16", "br_magenta": "base17",
}


def _lua_palette(s: Scheme) -> str:
    lines = []
    for role, slot in NVIM_ROLES.items():
        lines.append(f'    {role} = "{s.hex(slot)}",')
    return "\n".join(lines)


def render_nvim_palette(s: Scheme) -> tuple[str, str]:
    dark, light = _scheme("dark"), _scheme("light")
    out = (
        "-- GENERATED by tools/gen.py from schemes/ — do not edit.\n"
        "return {\n"
        "  dark = {\n" + _lua_palette(dark) + "\n  },\n"
        "  light = {\n" + _lua_palette(light) + "\n  },\n"
        "}\n"
    )
    return "themes/nvim/lua/wana/palette.lua", out
```

Register in `RENDERERS`:

```python
    render_nvim_palette,
```

- [ ] **Step 4: Generate and run test**

Run: `python3 tools/gen.py && python3 tools/test_gen.py TestGen.test_nvim_palette_has_both_variants`
Expected: writes `themes/nvim/lua/wana/palette.lua`; test PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/gen.py tools/test_gen.py themes/nvim/lua/wana/palette.lua
git commit -m "feat(gen): generate nvim palette.lua from schemes"
```

---

## Task 2: Hand-authored highlights (the design work)

A `function(p)` returning the v1 highlight table: editor UI + syntax + treesitter captures + diagnostics + diff. This is intentionally hand-tuned, not a flat base16 dump. Extend plugin integrations in Task 6.

**Files:**

- Create: `themes/nvim/lua/wana/highlights.lua`

- [ ] **Step 1: Write `themes/nvim/lua/wana/highlights.lua`**

```lua
-- Hand-authored highlight map. Input: a palette variant table from palette.lua.
return function(p)
  return {
    -- Editor UI
    Normal       = { fg = p.fg, bg = p.bg },
    NormalFloat  = { fg = p.fg, bg = p.bg_alt },
    FloatBorder  = { fg = p.muted, bg = p.bg_alt },
    Cursor       = { fg = p.bg, bg = p.green },
    CursorLine   = { bg = p.bg_alt },
    CursorLineNr = { fg = p.yellow, bold = true },
    LineNr       = { fg = p.muted },
    SignColumn   = { bg = p.bg },
    ColorColumn  = { bg = p.bg_alt },
    Visual       = { bg = p.sel },
    Search       = { fg = p.bg, bg = p.yellow },
    IncSearch    = { fg = p.bg, bg = p.orange },
    MatchParen   = { fg = p.cyan, bold = true },
    Pmenu        = { fg = p.fg, bg = p.bg_alt },
    PmenuSel     = { fg = p.bg, bg = p.blue, bold = true },
    PmenuSbar    = { bg = p.surface },
    PmenuThumb   = { bg = p.muted },
    StatusLine   = { fg = p.fg, bg = p.surface },
    StatusLineNC = { fg = p.muted, bg = p.bg_alt },
    TabLine      = { fg = p.muted, bg = p.bg_alt },
    TabLineSel   = { fg = p.bg, bg = p.blue, bold = true },
    WinSeparator = { fg = p.surface },
    Folded       = { fg = p.muted, bg = p.bg_alt },
    NonText      = { fg = p.surface },
    Whitespace   = { fg = p.surface },
    Directory    = { fg = p.blue },
    Title        = { fg = p.green, bold = true },
    ErrorMsg     = { fg = p.red },
    WarningMsg   = { fg = p.orange },

    -- Legacy syntax
    Comment      = { fg = p.muted, italic = true },
    Constant     = { fg = p.orange },
    String       = { fg = p.green },
    Character    = { fg = p.green },
    Number       = { fg = p.orange },
    Boolean      = { fg = p.orange },
    Identifier   = { fg = p.fg },
    Function     = { fg = p.blue },
    Statement    = { fg = p.magenta },
    Keyword      = { fg = p.magenta },
    Conditional  = { fg = p.magenta },
    Repeat       = { fg = p.magenta },
    Operator     = { fg = p.cyan },
    PreProc      = { fg = p.cyan },
    Type         = { fg = p.yellow },
    StorageClass = { fg = p.yellow },
    Special      = { fg = p.cyan },
    Underlined   = { fg = p.blue, underline = true },
    Todo         = { fg = p.bg, bg = p.yellow, bold = true },
    Error        = { fg = p.red },

    -- Treesitter captures
    ["@variable"]          = { fg = p.fg },
    ["@variable.builtin"]  = { fg = p.red },
    ["@variable.member"]   = { fg = p.fg },
    ["@property"]          = { fg = p.fg },
    ["@parameter"]         = { fg = p.fg, italic = true },
    ["@function"]          = { fg = p.blue },
    ["@function.builtin"]  = { fg = p.cyan },
    ["@function.call"]     = { fg = p.blue },
    ["@constructor"]       = { fg = p.yellow },
    ["@keyword"]           = { fg = p.magenta },
    ["@keyword.function"]  = { fg = p.magenta },
    ["@keyword.return"]    = { fg = p.magenta },
    ["@conditional"]       = { fg = p.magenta },
    ["@string"]            = { fg = p.green },
    ["@string.escape"]     = { fg = p.cyan },
    ["@number"]            = { fg = p.orange },
    ["@boolean"]           = { fg = p.orange },
    ["@type"]              = { fg = p.yellow },
    ["@type.builtin"]      = { fg = p.yellow, italic = true },
    ["@comment"]           = { fg = p.muted, italic = true },
    ["@punctuation"]       = { fg = p.fg_dim },
    ["@punctuation.bracket"] = { fg = p.fg_dim },
    ["@tag"]               = { fg = p.red },
    ["@tag.attribute"]     = { fg = p.yellow },
    ["@constant"]          = { fg = p.orange },
    ["@constant.builtin"]  = { fg = p.orange },

    -- LSP / diagnostics
    DiagnosticError = { fg = p.red },
    DiagnosticWarn  = { fg = p.orange },
    DiagnosticInfo  = { fg = p.blue },
    DiagnosticHint  = { fg = p.cyan },
    DiagnosticUnderlineError = { undercurl = true, sp = p.red },
    DiagnosticUnderlineWarn  = { undercurl = true, sp = p.orange },
    DiagnosticUnderlineInfo  = { undercurl = true, sp = p.blue },
    DiagnosticUnderlineHint  = { undercurl = true, sp = p.cyan },
    LspReferenceText  = { bg = p.sel },
    LspReferenceRead  = { bg = p.sel },
    LspReferenceWrite = { bg = p.sel },

    -- Diff / git
    DiffAdd    = { fg = p.green, bg = p.bg_alt },
    DiffChange = { fg = p.yellow, bg = p.bg_alt },
    DiffDelete = { fg = p.red, bg = p.bg_alt },
    DiffText   = { fg = p.bg, bg = p.yellow },
    Added      = { fg = p.green },
    Changed    = { fg = p.yellow },
    Removed    = { fg = p.red },
  }
end
```

- [ ] **Step 2: Lua-parse sanity check**

Run: `luajit -e 'assert(loadfile("themes/nvim/lua/wana/highlights.lua"))' 2>/dev/null || lua5.1 -e 'assert(loadfile("themes/nvim/lua/wana/highlights.lua"))'`
Expected: no output, exit 0 (file is syntactically valid Lua). If neither `luajit` nor `lua5.1` is installed, skip — Task 4 (headless nvim load) covers it.

- [ ] **Step 3: Commit**

```bash
git add themes/nvim/lua/wana/highlights.lua
git commit -m "feat(nvim): add hand-authored highlight map (editor, treesitter, lsp, diff)"
```

---

## Task 3: Plugin entry points — `init.lua` + `colors/wana.lua`

Wire palette + highlights into a loadable colorscheme.

**Files:**

- Create: `themes/nvim/lua/wana/init.lua`
- Create: `themes/nvim/colors/wana.lua`

- [ ] **Step 1: Write `themes/nvim/lua/wana/init.lua`**

```lua
local M = {}

function M.load()
  local variant = (vim.o.background == "light") and "light" or "dark"
  local p = require("wana.palette")[variant]

  if vim.g.colors_name then
    vim.cmd("highlight clear")
    if vim.fn.exists("syntax_on") == 1 then
      vim.cmd("syntax reset")
    end
  end
  vim.o.termguicolors = true
  vim.g.colors_name = "wana"

  local groups = require("wana.highlights")(p)
  for group, spec in pairs(groups) do
    vim.api.nvim_set_hl(0, group, spec)
  end
end

-- Allow require("wana").setup() as an alias for symmetry with other plugins.
M.setup = M.load

return M
```

- [ ] **Step 2: Write `themes/nvim/colors/wana.lua`**

```lua
-- Entry point for `:colorscheme wana`.
require("wana").load()
```

- [ ] **Step 3: Commit**

```bash
git add themes/nvim/lua/wana/init.lua themes/nvim/colors/wana.lua
git commit -m "feat(nvim): add colorscheme entry point and loader"
```

---

## Task 4: Headless load verification

Prove the colorscheme actually loads in Neovim with no errors, in both backgrounds.

**Files:** none (verification only)

- [ ] **Step 1: Load dark, assert it applies**

```bash
nvim --headless --clean \
  --cmd "set rtp+=themes/nvim" \
  -c "set background=dark" \
  -c "colorscheme wana" \
  -c "lua local h=vim.api.nvim_get_hl(0,{name='Function'}); assert(h.fg, 'Function has no fg'); print('dark OK')" \
  -c "qa" 2>&1
```

Expected: prints `dark OK`, exit 0. Any Lua error (bad group spec, missing palette key) prints a traceback and fails here.

- [ ] **Step 2: Load light, assert it applies**

```bash
nvim --headless --clean \
  --cmd "set rtp+=themes/nvim" \
  -c "set background=light" \
  -c "colorscheme wana" \
  -c "lua local n=vim.api.nvim_get_hl(0,{name='Normal'}); assert(n.bg, 'Normal has no bg'); print('light OK')" \
  -c "qa" 2>&1
```

Expected: prints `light OK`, exit 0.

> If `nvim` isn't installed in the execution environment, this task is the user's manual gate — note it in the handoff and do not mark the plan complete without it.

- [ ] **Step 3: Add a freshness assertion + run the suite**

Add to `tools/test_gen.py`:

```python
    def test_nvim_palette_is_generated_only_file(self):
        files = gen.build()
        nvim = [k for k in files if k.startswith("themes/nvim/")]
        # only palette.lua is generated; highlights/init/colors are hand-authored
        self.assertEqual(nvim, ["themes/nvim/lua/wana/palette.lua"])
```

Run: `python3 -m pytest tools/ -q`
Expected: all green (`test_check_is_clean` confirms palette.lua matches committed).

- [ ] **Step 4: Commit**

```bash
git add tools/test_gen.py
git commit -m "test(gen): assert palette.lua is the only generated nvim file"
```

---

## Task 5: README + LICENSE, then publish to private repo

**Files:**

- Create: `themes/nvim/README.md`, `themes/nvim/LICENSE`

- [ ] **Step 1: Write `themes/nvim/README.md`**

````markdown
# wana.nvim

A warm, bookish Gruvbox-leaning Neovim colorscheme with dark + light variants.
The palette is generated from the canonical [Wana](https://github.com/atalariq/wana)
base24 schemes; highlights are hand-authored.

## Install (lazy.nvim)

```lua
{ "atalariq/wana.nvim", priority = 1000, config = function()
  vim.o.background = "dark" -- or "light"
  vim.cmd.colorscheme("wana")
end }
```
````

## Variants

`set background=dark` / `set background=light` selects the variant, then
`:colorscheme wana`.

> `lua/wana/palette.lua` is generated — do not hand-edit. Edit highlights in
> `lua/wana/highlights.lua`. Source of truth: `schemes/` in atalariq/wana.

````

- [ ] **Step 2: Add LICENSE (MIT, author atalariq)**

```bash
cp themes/yazi/wana-dark.yazi/LICENSE themes/nvim/LICENSE 2>/dev/null \
  || echo "create themes/nvim/LICENSE (MIT, copyright 2026 atalariq)"
````

(If the yazi plan hasn't run, paste the same MIT text used there.)

- [ ] **Step 3: Commit**

```bash
git add themes/nvim/README.md themes/nvim/LICENSE
git commit -m "docs(nvim): add README and LICENSE"
```

- [ ] **Step 4: Create the private repo + publish (outward-facing — user-confirmed private)**

```bash
gh repo create atalariq/wana.nvim --private \
  --description "Wana Neovim colorscheme (palette generated from atalariq/wana)"
tools/publish.sh nvim
```

Expected: `✓ Created repository atalariq/wana.nvim`, then
`published themes/nvim -> git@github.com:atalariq/wana.nvim.git (main)`.

- [ ] **Step 5: Verify the mirror is installable**

```bash
gh api repos/atalariq/wana.nvim/contents | python3 -c "import sys,json;print([x['name'] for x in json.load(sys.stdin)])"
```

Expected: includes `colors`, `lua`, `README.md`, `LICENSE` at repo root (so plugin managers find `colors/wana.lua`).

---

## Task 6: Document + (optional) extend plugin integrations

**Files:**

- Modify: `AGENTS.md`, `README.md`
- Optional: `themes/nvim/lua/wana/highlights.lua`

- [ ] **Step 1: Add nvim to `AGENTS.md` tree**

Under `themes/`:

```
  nvim/                    # palette GENERATED, highlights hand-authored -> atalariq/wana.nvim (private)
    lua/wana/palette.lua   # generated
    lua/wana/highlights.lua
```

- [ ] **Step 2: Add nvim to the README "Standalone repos" list**

```markdown
- `themes/nvim/` → `atalariq/wana.nvim` (palette generated; highlights hand-authored)
```

- [ ] **Step 3 (optional, iterative): add plugin-specific groups**

Extend `highlights.lua` with integrations as needed, e.g. gitsigns + telescope:

```lua
    -- gitsigns
    GitSignsAdd    = { fg = p.green },
    GitSignsChange = { fg = p.yellow },
    GitSignsDelete = { fg = p.red },
    -- telescope
    TelescopeBorderColor   = { fg = p.muted },
    TelescopeSelection     = { bg = p.sel },
    TelescopeMatching      = { fg = p.yellow, bold = true },
    TelescopePromptPrefix  = { fg = p.green },
```

Re-run Task 4 Step 1 after each addition. Commit per integration:

```bash
git commit -m "feat(nvim): add gitsigns + telescope highlights"
```

- [ ] **Step 4: Commit docs**

```bash
git add AGENTS.md README.md
git commit -m "docs: document nvim colorscheme target"
```

---

## Self-review notes

- **Spec coverage:** generated palette (Task 1), hand-authored highlights (2), loadable plugin (3), headless verification both variants (4), publish to private repo (5), docs + extensibility (6). The generated/hand-authored split is enforced by `test_nvim_palette_is_generated_only_file` (Task 4) — only `palette.lua` is under `gen.py`, so the anti-drift guarantee holds while highlights stay free for design.
- **Type consistency:** `init.lua` indexes `require("wana.palette")[variant]` and passes it to `require("wana.highlights")(p)`; every `p.<role>` used in `highlights.lua` is a key emitted by `NVIM_ROLES` in `render_nvim_palette`. (Check: `bg, bg_dim, bg_alt, surface, sel, overlay, muted, fg_dim, fg, fg_bright, red, orange, yellow, green, cyan, blue, magenta, brown, br_*` — all present in both.)
- **Out of scope:** exhaustive plugin coverage (iterative, Task 6), lualine/heirline theme module, `:Wana` user commands, making the repo public, `preview.png`.

```

```
