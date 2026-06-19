/* ════════════════════════════════════════════════════════════════════
   atalariq design system — playground logic

   - Color math (OKLCH ↔ hex ↔ HSL, WCAG contrast) ported verbatim from
     tools/color.py — no external libraries.
   - State drives the whole page: proposal + theme + editable tokens.
   - Tokens are applied via documentElement.style.setProperty() as oklch()
     strings, so the entire dogfooded UI re-skins in real time.
   ════════════════════════════════════════════════════════════════════ */

"use strict";

/* ─────────────────────────────────────────────────────────────────────
   Color data — the three proposals (mirrors tools/proposals.json).
   Embedded inline so the site works from file:// without fetch/CORS.
   ───────────────────────────────────────────────────────────────────── */
const ROLES = [
  "bg",
  "surface",
  "overlay",
  "muted",
  "text",
  "accent",
  "success",
  "warning",
  "error",
  "info",
];

const PROPOSALS = {
  A: {
    name: "Warm Ink",
    light: {
      bg: "#faf4e6",
      surface: "#f1e9d5",
      overlay: "#e7ddc4",
      text: "#211d17",
      muted: "#6b6557",
      accent: "#1d6b7a",
      success: "#5a7012",
      warning: "#8f5f00",
      error: "#b3261e",
      info: "#2a5ea8",
    },
    dark: {
      bg: "#1a1714",
      surface: "#242019",
      overlay: "#2f2a21",
      text: "#ece3cf",
      muted: "#a39a86",
      accent: "#5cb6c4",
      success: "#a7bd5a",
      warning: "#e0a83a",
      error: "#e07b6a",
      info: "#7fb0e0",
    },
  },
  B: {
    name: "Night Scholar",
    light: {
      bg: "#e9eaf2",
      surface: "#dfe1ec",
      overlay: "#d2d5e4",
      text: "#1c1f2e",
      muted: "#565b76",
      accent: "#6a3fd0",
      success: "#357025",
      warning: "#855800",
      error: "#c02748",
      info: "#2861b8",
    },
    dark: {
      bg: "#14151f",
      surface: "#1d1f2c",
      overlay: "#282b3c",
      text: "#d7dbf2",
      muted: "#9097ba",
      accent: "#b49cf5",
      success: "#9ed07a",
      warning: "#e6b860",
      error: "#f08599",
      info: "#7fb8e8",
    },
  },
  C: {
    name: "Balanced",
    light: {
      bg: "#fbfaf8",
      surface: "#f2f0ea",
      overlay: "#e7e4db",
      text: "#1a1c22",
      muted: "#5d6170",
      accent: "#5a3cc4",
      success: "#3f7320",
      warning: "#9a6500",
      error: "#bb2533",
      info: "#2660a8",
    },
    dark: {
      bg: "#171a21",
      surface: "#20232c",
      overlay: "#2b2f3a",
      text: "#e6e8ef",
      muted: "#a7adbc",
      accent: "#9b86f0",
      success: "#94c46a",
      warning: "#e0b15a",
      error: "#ef8090",
      info: "#79b0e6",
    },
  },
};

/* ═══════════════════════ COLOR MATH (port of color.py) ═══════════════ */

function clamp01(x) {
  return Math.min(1, Math.max(0, x));
}

function hexToRgb(h) {
  h = h.trim().replace(/^#/, "");
  if (h.length === 3)
    h = h
      .split("")
      .map((c) => c + c)
      .join("");
  return [
    parseInt(h.slice(0, 2), 16) / 255,
    parseInt(h.slice(2, 4), 16) / 255,
    parseInt(h.slice(4, 6), 16) / 255,
  ];
}

function rgbToHex(rgb) {
  return (
    "#" +
    rgb
      .map((c) =>
        Math.round(clamp01(c) * 255)
          .toString(16)
          .padStart(2, "0"),
      )
      .join("")
  );
}

function hslToRgb(h, s, l) {
  h = ((h % 360) + 360) % 360;
  s /= 100;
  l /= 100;
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = l - c / 2;
  let r, g, b;
  if (h < 60) [r, g, b] = [c, x, 0];
  else if (h < 120) [r, g, b] = [x, c, 0];
  else if (h < 180) [r, g, b] = [0, c, x];
  else if (h < 240) [r, g, b] = [0, x, c];
  else if (h < 300) [r, g, b] = [x, 0, c];
  else [r, g, b] = [c, 0, x];
  return [r + m, g + m, b + m];
}

function rgbToHsl(rgb) {
  const [r, g, b] = rgb;
  const mx = Math.max(r, g, b),
    mn = Math.min(r, g, b);
  const l = (mx + mn) / 2;
  if (mx === mn) return [0, 0, round(l * 100, 1)];
  const d = mx - mn;
  const s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn);
  let h;
  if (mx === r) h = (g - b) / d + (g < b ? 6 : 0);
  else if (mx === g) h = (b - r) / d + 2;
  else h = (r - g) / d + 4;
  return [round(h * 60, 1), round(s * 100, 1), round(l * 100, 1)];
}

function srgbToLinear(c) {
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}
function linearToSrgb(c) {
  return c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055;
}

/* sRGB[0,1] → OKLCH. L returned in percent (0–100), to match color.py. */
function rgbToOklch(rgb) {
  const [r, g, b] = rgb.map(srgbToLinear);
  const l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b;
  const m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b;
  const s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b;
  const cbrt = (v) => Math.sign(v) * Math.pow(Math.abs(v), 1 / 3);
  const l_ = cbrt(l),
    m_ = cbrt(m),
    s_ = cbrt(s);
  const L = 0.2104542553 * l_ + 0.793617785 * m_ - 0.0040720468 * s_;
  const a = 1.9779984951 * l_ - 2.428592205 * m_ + 0.4505937099 * s_;
  const bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.808675766 * s_;
  const C = Math.hypot(a, bb);
  let H = (Math.atan2(bb, a) * 180) / Math.PI;
  H = ((H % 360) + 360) % 360;
  return [round(L * 100, 1), round(C, 3), round(H, 1)];
}

/* OKLCH (L in percent) → sRGB[0,1], gamut-clamped. Inverse of rgbToOklch. */
function oklchToRgb(L, C, H) {
  L = L / 100;
  const hr = (H * Math.PI) / 180;
  const a = C * Math.cos(hr);
  const b = C * Math.sin(hr);
  const l_ = L + 0.3963377774 * a + 0.2158037573 * b;
  const m_ = L - 0.1055613458 * a - 0.0638541728 * b;
  const s_ = L - 0.0894841775 * a - 1.291485548 * b;
  const l = l_ ** 3,
    m = m_ ** 3,
    s = s_ ** 3;
  const r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s;
  const g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s;
  const bl = -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s;
  return [r, g, bl].map((c) => clamp01(linearToSrgb(c)));
}

function relativeLuminance(rgb) {
  const [r, g, b] = rgb.map(srgbToLinear);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrastRatio(hex1, hex2) {
  const l1 = relativeLuminance(hexToRgb(hex1));
  const l2 = relativeLuminance(hexToRgb(hex2));
  const hi = Math.max(l1, l2),
    lo = Math.min(l1, l2);
  return (hi + 0.05) / (lo + 0.05);
}

function wcagGrade(ratio, large = false) {
  if (large) {
    if (ratio >= 4.5) return "AAA";
    if (ratio >= 3.0) return "AA";
    return "fail";
  }
  if (ratio >= 7.0) return "AAA";
  if (ratio >= 4.5) return "AA";
  if (ratio >= 3.0) return "AA-large";
  return "fail";
}

function round(x, n) {
  const p = 10 ** n;
  return Math.round(x * p) / p;
}

/* Format helpers */
function hexToOklchStr(hex) {
  const [L, C, H] = rgbToOklch(hexToRgb(hex));
  return `oklch(${L}% ${C} ${H})`;
}
function hexToHslStr(hex) {
  const [h, s, l] = rgbToHsl(hexToRgb(hex));
  return `hsl(${h} ${s}% ${l}%)`;
}

/* Parse a CSS oklch() string → hex. Accepts "oklch(L% C H)" with optional %. */
function parseOklch(str) {
  const m = str.trim().match(/oklch\(\s*([\d.]+)%?\s+([\d.]+)\s+([\d.]+)/i);
  if (!m) return null;
  const L = parseFloat(m[1]),
    C = parseFloat(m[2]),
    H = parseFloat(m[3]);
  return rgbToHex(oklchToRgb(L, C, H));
}

/* Parse a CSS hsl() string → hex. */
function parseHsl(str) {
  const m = str.trim().match(/hsla?\(\s*([\d.]+)[ ,]+([\d.]+)%[ ,]+([\d.]+)%/i);
  if (!m) return null;
  return rgbToHex(
    hslToRgb(parseFloat(m[1]), parseFloat(m[2]), parseFloat(m[3])),
  );
}

function isHex(str) {
  return /^#?[0-9a-f]{3}([0-9a-f]{3})?$/i.test(str.trim());
}
function normalizeHex(str) {
  let h = str.trim().replace(/^#/, "");
  if (h.length === 3)
    h = h
      .split("")
      .map((c) => c + c)
      .join("");
  return "#" + h.toLowerCase();
}

/* ═══════════════════════ STATE ══════════════════════════════════════ */

const state = {
  proposal: "C",
  theme: "light",
  selectedRole: "accent",
  exportFmt: "css",
  // Working copy of tokens for the active proposal: { light: {...}, dark: {...} }
  tokens: { light: {}, dark: {} },
};

function loadProposal(key) {
  state.proposal = key;
  state.tokens.light = { ...PROPOSALS[key].light };
  state.tokens.dark = { ...PROPOSALS[key].dark };
}

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));
const el = (tag, cls, html) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html != null) n.innerHTML = html;
  return n;
};

/* ═══════════════════════ APPLYING TOKENS (dogfood) ══════════════════ */

function applyTokens() {
  const root = document.documentElement;
  root.setAttribute("data-theme", state.theme);
  const pal = state.tokens[state.theme];
  for (const role of ROLES) {
    // Apply as oklch() to satisfy the "use oklch() function" requirement.
    root.style.setProperty(`--${role}`, hexToOklchStr(pal[role]));
  }
}

/* ═══════════════════════ COLORS SECTION ═════════════════════════════ */

function renderProposalTabs() {
  const tabs = $("#proposalTabs");
  const mini = $("#proposalMiniTabs");
  tabs.innerHTML = "";
  mini.innerHTML = "";
  for (const key of ["A", "B", "C"]) {
    const t = el(
      "button",
      "proposal-tab" + (key === state.proposal ? " active" : ""),
    );
    t.setAttribute("role", "tab");
    t.innerHTML = `<span class="pt-key">${key}</span>${PROPOSALS[key].name}`;
    t.addEventListener("click", () => selectProposal(key));
    tabs.appendChild(t);

    const m = el("button", key === state.proposal ? "active" : "");
    m.textContent = key;
    m.title = PROPOSALS[key].name;
    m.addEventListener("click", () => selectProposal(key));
    mini.appendChild(m);
  }
}

function swatchCard(role, hex, bgHex) {
  const card = el("div", "swatch");
  const ratio = contrastRatio(hex, bgHex);
  const grade = wcagGrade(ratio);
  card.innerHTML = `
    <div class="swatch-preview" style="background:${hex}"></div>
    <div class="swatch-info">
      <div class="swatch-role">${role}</div>
      <div class="swatch-hex">${hex}</div>
      <div class="swatch-oklch">${hexToOklchStr(hex)}</div>
      <div class="swatch-contrast">
        ${ratio.toFixed(2)}:1
        <span class="contrast-pill grade-${grade}">${grade}</span>
      </div>
    </div>`;
  return card;
}

function renderPalettes() {
  const pal = PROPOSALS[state.proposal];
  $("#lightMeta").textContent = "contrast vs bg " + pal.light.bg;
  $("#darkMeta").textContent = "contrast vs bg " + pal.dark.bg;
  for (const [mode, gridId] of [
    ["light", "#swatchesLight"],
    ["dark", "#swatchesDark"],
  ]) {
    const grid = $(gridId);
    grid.innerHTML = "";
    for (const role of ROLES) {
      grid.appendChild(swatchCard(role, pal[mode][role], pal[mode].bg));
    }
  }
}

/* ═══════════════════════ TYPOGRAPHY SECTION ═════════════════════════ */

function renderTypeScale() {
  const steps = [
    ["--step-3", "Display heading"],
    ["--step-2", "Section heading"],
    ["--step-1", "Subheading"],
    ["--step-0", "Body text — the quick brown fox jumps over the lazy dog"],
    ["--step--1", "Small / caption text"],
  ];
  const wrap = $("#typeScale");
  wrap.innerHTML = "";
  for (const [token, sample] of steps) {
    const row = el("div", "type-row");
    row.innerHTML = `<span class="type-token">${token}</span><span class="type-sample" style="font-size:var(${token})">${sample}</span>`;
    wrap.appendChild(row);
  }
}

/* ═══════════════════════ SPACING SECTION ════════════════════════════ */

function renderSpacing() {
  const tokens = [
    ["--space-2xs", "0.25rem"],
    ["--space-xs", "0.5rem"],
    ["--space-s", "0.75rem"],
    ["--space-m", "1rem"],
    ["--space-l", "1.5rem"],
    ["--space-xl", "2.5rem"],
    ["--space-2xl", "4rem"],
  ];
  const wrap = $("#spaceScale");
  wrap.innerHTML = "";
  for (const [token, val] of tokens) {
    const row = el("div", "space-row");
    row.innerHTML = `<span class="space-token">${token}<small>${val}</small></span><div class="space-bar" style="width:var(${token})"></div>`;
    wrap.appendChild(row);
  }
}

/* ═══════════════════════ COMPONENTS: badges ═════════════════════════ */

function renderBadges() {
  const row = $("#badgeRow");
  row.innerHTML = "";
  for (const role of [
    "accent",
    "success",
    "warning",
    "error",
    "info",
    "muted",
  ]) {
    row.appendChild(el("span", `badge badge-${role}`, role));
  }
}

/* ═══════════════════════ TOKEN EDITOR ═══════════════════════════════ */

function renderRoleList() {
  const list = $("#roleList");
  list.innerHTML = "";
  const pal = state.tokens[state.theme];
  for (const role of ROLES) {
    const btn = el(
      "button",
      "role-btn" + (role === state.selectedRole ? " active" : ""),
    );
    btn.innerHTML = `<span class="role-swatch" style="background:${pal[role]}"></span><span class="role-name">${role}</span><span class="role-hex">${pal[role]}</span>`;
    btn.addEventListener("click", () => {
      state.selectedRole = role;
      refreshEditor();
    });
    list.appendChild(btn);
  }
}

/* Update every editor input to reflect the selected role's current value. */
function refreshEditor() {
  $("#editorThemeLabel").textContent = state.theme;
  $("#editingRole").textContent = state.selectedRole;
  renderRoleList();

  const hex = state.tokens[state.theme][state.selectedRole];
  const [L, C, H] = rgbToOklch(hexToRgb(hex));

  $("#editorPreview").style.background = hex;
  $("#slL").value = L;
  $("#outL").textContent = L + "%";
  $("#slC").value = C;
  $("#outC").textContent = C;
  $("#slH").value = H;
  $("#outH").textContent = H;

  $("#colorPicker").value = normalizeHex(hex);
  setInput($("#inHex"), hex);
  setInput($("#inOklch"), hexToOklchStr(hex));
  setInput($("#inHsl"), hexToHslStr(hex));
}

function setInput(node, val) {
  node.value = val;
  node.classList.remove("invalid");
}

/* Commit a new hex for the selected role, then re-skin + refresh everything. */
function setRoleColor(hex) {
  state.tokens[state.theme][state.selectedRole] = hex;
  applyTokens();
  refreshEditor();
  renderBadges();
  updateContrastResult();
  renderExport();
}

function wireEditor() {
  // OKLCH sliders → recompute hex from L/C/H.
  const sl = () => {
    const L = parseFloat($("#slL").value);
    const C = parseFloat($("#slC").value);
    const H = parseFloat($("#slH").value);
    $("#outL").textContent = L + "%";
    $("#outC").textContent = round(C, 3);
    $("#outH").textContent = round(H, 1);
    setRoleColor(rgbToHex(oklchToRgb(L, C, H)));
  };
  ["#slL", "#slC", "#slH"].forEach((s) => $(s).addEventListener("input", sl));

  // Native color picker.
  $("#colorPicker").addEventListener("input", (e) =>
    setRoleColor(e.target.value),
  );

  // Hex / OKLCH / HSL text fields — bidirectional, validated.
  $("#inHex").addEventListener("change", (e) => {
    if (isHex(e.target.value)) setRoleColor(normalizeHex(e.target.value));
    else e.target.classList.add("invalid");
  });
  $("#inOklch").addEventListener("change", (e) => {
    const hex = parseOklch(e.target.value);
    if (hex) setRoleColor(hex);
    else e.target.classList.add("invalid");
  });
  $("#inHsl").addEventListener("change", (e) => {
    const hex = parseHsl(e.target.value);
    if (hex) setRoleColor(hex);
    else e.target.classList.add("invalid");
  });

  // Reset to proposal defaults (active theme).
  $("#resetBtn").addEventListener("click", () => {
    state.tokens[state.theme] = { ...PROPOSALS[state.proposal][state.theme] };
    applyTokens();
    refreshEditor();
    renderBadges();
    updateContrastResult();
    renderExport();
  });
}

/* ─── Contrast checker ─── */
function fillContrastSelects() {
  const opts = ROLES.map((r) => `<option value="${r}">${r}</option>`).join("");
  const fg = $("#contrastFg"),
    bg = $("#contrastBg");
  fg.innerHTML = opts;
  bg.innerHTML = opts;
  fg.value = "text";
  bg.value = "bg";
  fg.addEventListener("change", updateContrastResult);
  bg.addEventListener("change", updateContrastResult);
}

function updateContrastResult() {
  const pal = state.tokens[state.theme];
  const fgHex = pal[$("#contrastFg").value];
  const bgHex = pal[$("#contrastBg").value];
  const ratio = contrastRatio(fgHex, bgHex);

  const sample = $("#contrastSample");
  sample.style.background = bgHex;
  sample.style.color = fgHex;

  $("#contrastRatio").textContent = ratio.toFixed(2) + ":1";

  const grades = $("#contrastGrades");
  grades.innerHTML = "";
  const checks = [
    ["Normal AA", ratio >= 4.5],
    ["Normal AAA", ratio >= 7.0],
    ["Large AA", ratio >= 3.0],
    ["Large AAA", ratio >= 4.5],
  ];
  for (const [label, pass] of checks) {
    grades.appendChild(
      el(
        "span",
        `grade-chip ${pass ? "pass" : "fail"}`,
        `${label} ${pass ? "✓" : "✕"}`,
      ),
    );
  }
}

/* ═══════════════════════ IMPORT / EXPORT ════════════════════════════ */

function exportCss() {
  const lines = [];
  lines.push(
    "/* atalariq design system — " + PROPOSALS[state.proposal].name + " */",
  );
  lines.push(":root {");
  for (const role of ROLES)
    lines.push(
      `  --${role}: ${hexToOklchStr(state.tokens.light[role])}; /* ${state.tokens.light[role]} */`,
    );
  // Typography + spacing tokens (static across proposals).
  lines.push("");
  lines.push(
    '  --font-sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;',
  );
  lines.push(
    '  --font-serif: ui-serif, Georgia, Cambria, "Times New Roman", serif;',
  );
  lines.push(
    '  --font-mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;',
  );
  lines.push("  --step--1: clamp(0.83rem, 0.8rem + 0.15vw, 0.9rem);");
  lines.push("  --step-0: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);");
  lines.push("  --step-1: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);");
  lines.push("  --step-2: clamp(1.56rem, 1.4rem + 0.8vw, 2rem);");
  lines.push("  --step-3: clamp(1.95rem, 1.7rem + 1.25vw, 2.75rem);");
  lines.push("  --measure: 65ch;");
  lines.push("  --radius: 0.5rem;");
  lines.push(
    "  --space-2xs: 0.25rem;  --space-xs: 0.5rem;  --space-s: 0.75rem;",
  );
  lines.push(
    "  --space-m: 1rem;  --space-l: 1.5rem;  --space-xl: 2.5rem;  --space-2xl: 4rem;",
  );
  lines.push("}");
  lines.push("");
  lines.push('[data-theme="dark"] {');
  for (const role of ROLES)
    lines.push(
      `  --${role}: ${hexToOklchStr(state.tokens.dark[role])}; /* ${state.tokens.dark[role]} */`,
    );
  lines.push("}");
  return lines.join("\n");
}

/* W3C Design Tokens Community Group (DTCG) format. */
function exportJson() {
  const colorGroup = (pal) => {
    const out = {};
    for (const role of ROLES) {
      out[role] = { $type: "color", $value: pal[role] };
    }
    return out;
  };
  const doc = {
    $schema: "https://design-tokens.github.io/community-group/format/",
    color: {
      $type: "color",
      light: colorGroup(state.tokens.light),
      dark: colorGroup(state.tokens.dark),
    },
    space: {
      $type: "dimension",
      "2xs": { $value: "0.25rem" },
      xs: { $value: "0.5rem" },
      s: { $value: "0.75rem" },
      m: { $value: "1rem" },
      l: { $value: "1.5rem" },
      xl: { $value: "2.5rem" },
      "2xl": { $value: "4rem" },
    },
    radius: { $type: "dimension", $value: "0.5rem" },
  };
  return JSON.stringify(doc, null, 2);
}

/* Tokens Studio (Figma Tokens plugin) schema: sets keyed by theme, each
   token { value, type }. */
function exportFigma() {
  const set = (pal) => {
    const colors = {};
    for (const role of ROLES)
      colors[role] = { value: pal[role], type: "color" };
    return { color: colors };
  };
  const doc = {
    light: set(state.tokens.light),
    dark: set(state.tokens.dark),
    global: {
      spacing: {
        "2xs": { value: "0.25rem", type: "spacing" },
        xs: { value: "0.5rem", type: "spacing" },
        s: { value: "0.75rem", type: "spacing" },
        m: { value: "1rem", type: "spacing" },
        l: { value: "1.5rem", type: "spacing" },
        xl: { value: "2.5rem", type: "spacing" },
        "2xl": { value: "4rem", type: "spacing" },
      },
      radius: { value: "0.5rem", type: "borderRadius" },
    },
    $themes: [],
    $metadata: { tokenSetOrder: ["global", "light", "dark"] },
  };
  return JSON.stringify(doc, null, 2);
}

function currentExport() {
  if (state.exportFmt === "json") return exportJson();
  if (state.exportFmt === "figma") return exportFigma();
  return exportCss();
}

function renderExport() {
  $("#exportOutput").textContent = currentExport();
}

function exportFilename() {
  const base =
    "atalariq-tokens-" +
    PROPOSALS[state.proposal].name.toLowerCase().replace(/\s+/g, "-");
  if (state.exportFmt === "css") return base + ".css";
  if (state.exportFmt === "figma") return base + ".figma.json";
  return base + ".json";
}

function wireExport() {
  $$(".export-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      state.exportFmt = tab.dataset.fmt;
      $$(".export-tab").forEach((t) => t.classList.toggle("active", t === tab));
      renderExport();
    });
  });

  $("#copyExport").addEventListener("click", async () => {
    const text = currentExport();
    try {
      await navigator.clipboard.writeText(text);
      flash("#exportStatus", "Copied to clipboard ✓");
    } catch {
      // Fallback for file:// / older browsers.
      const ta = el("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      ta.remove();
      flash("#exportStatus", "Copied ✓");
    }
  });

  $("#downloadExport").addEventListener("click", () => {
    const blob = new Blob([currentExport()], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = el("a");
    a.href = url;
    a.download = exportFilename();
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    flash("#exportStatus", "Downloaded " + exportFilename());
  });
}

function flash(sel, msg) {
  const node = $(sel);
  node.textContent = msg;
  setTimeout(() => {
    if (node.textContent === msg) node.textContent = "";
  }, 2500);
}

/* ─── Import ─── */
function importFromCss(text) {
  // Parse :root { ... } and [data-theme="dark"] { ... } custom properties.
  const result = { light: {}, dark: {} };
  const grab = (block, target) => {
    const re = /--([a-z]+)\s*:\s*([^;]+);/gi;
    let m;
    while ((m = re.exec(block))) {
      const role = m[1].trim();
      if (!ROLES.includes(role)) continue;
      const val = m[2].trim();
      let hex = null;
      if (isHex(val)) hex = normalizeHex(val);
      else if (/^oklch/i.test(val)) hex = parseOklch(val);
      else if (/^hsl/i.test(val)) hex = parseHsl(val);
      if (hex) target[role] = hex;
    }
  };
  const darkMatch = text.match(/\[data-theme=["']?dark["']?\]\s*\{([^}]*)\}/i);
  if (darkMatch) grab(darkMatch[1], result.dark);
  const rootMatch = text.match(/:root\s*\{([^}]*)\}/i);
  if (rootMatch) grab(rootMatch[1], result.light);
  else grab(text, result.light); // bare list of props → treat as light
  return result;
}

function importFromJson(text) {
  const data = JSON.parse(text);
  const result = { light: {}, dark: {} };

  const readColor = (v) => {
    if (v == null) return null;
    const raw = typeof v === "string" ? v : (v.$value ?? v.value);
    if (typeof raw !== "string") return null;
    if (isHex(raw)) return normalizeHex(raw);
    if (/^oklch/i.test(raw)) return parseOklch(raw);
    if (/^hsl/i.test(raw)) return parseHsl(raw);
    return null;
  };

  // DTCG: color.light.<role>, color.dark.<role>
  if (data.color && (data.color.light || data.color.dark)) {
    for (const mode of ["light", "dark"]) {
      const grp = data.color[mode] || {};
      for (const role of ROLES) {
        const c = readColor(grp[role]);
        if (c) result[mode][role] = c;
      }
    }
  }
  // Tokens Studio: light.color.<role>, dark.color.<role>
  if (data.light?.color || data.dark?.color) {
    for (const mode of ["light", "dark"]) {
      const grp = data[mode]?.color || {};
      for (const role of ROLES) {
        const c = readColor(grp[role]);
        if (c) result[mode][role] = c;
      }
    }
  }
  // Flat fallback: { light: {role:hex}, dark: {role:hex} }
  for (const mode of ["light", "dark"]) {
    if (data[mode] && !data[mode].color) {
      for (const role of ROLES) {
        const c = readColor(data[mode][role]);
        if (c) result[mode][role] = c;
      }
    }
  }
  return result;
}

function applyImported(parsed) {
  let count = 0;
  for (const mode of ["light", "dark"]) {
    for (const role of ROLES) {
      if (parsed[mode][role]) {
        state.tokens[mode][role] = parsed[mode][role];
        count++;
      }
    }
  }
  if (count === 0) throw new Error("no recognizable color tokens found");
  applyTokens();
  refreshEditor();
  renderBadges();
  updateContrastResult();
  renderExport();
  return count;
}

function wireImport() {
  $("#importFile").addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      $("#importArea").value = reader.result;
      $("#importFmt").value = /\.css$/i.test(file.name) ? "css" : "json";
    };
    reader.readAsText(file);
  });

  $("#importBtn").addEventListener("click", () => {
    const text = $("#importArea").value.trim();
    if (!text) {
      flash("#importStatus", "Paste or upload tokens first");
      return;
    }
    try {
      const parsed = state.importFmtIsCss()
        ? importFromCss(text)
        : importFromJson(text);
      const n = applyImported(parsed);
      const status = $("#importStatus");
      status.style.color = "var(--success)";
      flash("#importStatus", `Imported ${n} token${n === 1 ? "" : "s"} ✓`);
    } catch (err) {
      const status = $("#importStatus");
      status.style.color = "var(--error)";
      flash("#importStatus", "Import failed: " + err.message);
    }
  });
}
state.importFmtIsCss = () => $("#importFmt").value === "css";

/* ═══════════════════════ NAV / THEME / PROPOSAL ═════════════════════ */

function selectProposal(key) {
  loadProposal(key);
  applyTokens();
  renderProposalTabs();
  renderPalettes();
  renderBadges();
  fillContrastSelects();
  refreshEditor();
  updateContrastResult();
  renderExport();
}

function toggleTheme() {
  state.theme = state.theme === "light" ? "dark" : "light";
  applyTokens();
  renderPalettes();
  refreshEditor();
  fillContrastSelects();
  updateContrastResult();
}

function wireNav() {
  $("#themeToggle").addEventListener("click", toggleTheme);

  const sidebar = $("#sidebar");
  $("#navToggle").addEventListener("click", () => {
    const open = sidebar.classList.toggle("open");
    $("#navToggle").setAttribute("aria-expanded", String(open));
  });

  // Close mobile nav after picking a section.
  $$(".nav-link").forEach((link) => {
    link.addEventListener("click", () => {
      if (window.innerWidth <= 768) sidebar.classList.remove("open");
    });
  });

  // Scroll-spy to highlight the active section.
  const links = $$(".nav-link");
  const byId = new Map(links.map((l) => [l.dataset.section, l]));
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          links.forEach((l) => l.classList.remove("active"));
          byId.get(entry.target.id)?.classList.add("active");
        }
      }
    },
    { rootMargin: "-45% 0px -50% 0px", threshold: 0 },
  );
  $$("section.section").forEach((s) => observer.observe(s));
}

/* ═══════════════════════ INIT ═══════════════════════════════════════ */

function init() {
  // Honour OS dark preference on first load.
  if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  ) {
    state.theme = "dark";
  }
  loadProposal(state.proposal);
  applyTokens();

  renderProposalTabs();
  renderPalettes();
  renderTypeScale();
  renderSpacing();
  renderBadges();

  fillContrastSelects();
  refreshEditor();
  updateContrastResult();
  wireEditor();

  renderExport();
  wireExport();
  wireImport();

  wireNav();
}

document.addEventListener("DOMContentLoaded", init);
