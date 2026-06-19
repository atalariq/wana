# Research Prompt — Design System Colorscheme

## Context

You're building a personal design system for a developer/student (Indonesian, UGM). The system will be used across multiple sites: a digital garden (journey.atalariq.dev), portfolio (atalariq.github.io), and research site (research.atalariq.dev).

The existing Journey tokens use:
- Light: warm white `hsl(40 30% 98%)`, surface `hsl(40 25% 95%)`
- Dark: cool blue-black `hsl(225 18% 11%)`, surface `hsl(225 16% 15%)`
- Accent: purple `hsl(255 70% 55%)`

## Task 1: Color Theory Research

Write `research/color-theory.md` covering:
- HSL vs OKLCH vs HEX — why perceptual uniformity matters for design tokens
- The 60-30-10 rule and how it maps to semantic color roles
- Contrast ratios: what WCAG AA/AAA actually means numerically
- Color temperature in UI: warm vs cool backgrounds, readability research
- How to build a palette that works in both light and dark mode (not just inverted)

## Task 2: Colorscheme Analysis

Write `research/colorscheme-analysis.md` — deep analysis of these schemes:
- **Gruvbox** — warm, retro, high contrast
- **Catppuccin** — pastel, modern, very popular
- **Flexoki** — by Steph Ango (Obsidian CEO), ink-on-paper feel
- **Everforest** — green-based, comfortable reading
- **Tokyo Night** — cool, VS Code favorite
- **Solarized** — Ethan Schoonover's scientifically-grounded scheme

For each:
- Core palette (bg, fg, accent, secondary accents)
- What makes it distinctive
- Light/dark mode approach
- Strengths and weaknesses for long-form reading
- WCAG contrast ratios (calculate them)

## Task 3: Accessibility Research

Write `research/accessibility.md`:
- WCAG 2.1 contrast requirements (AA vs AAA, text vs large text vs UI components)
- How to test contrast programmatically
- Common pitfalls in dark mode accessibility
- Color blindness considerations (deuteranopia, protanopia, tritanopia)
- Tools and methodology for ongoing a11y testing

## Task 4: Proposals (3 variants)

Create 3 full colorscheme proposals in `proposals/`. Each must include:
- Design philosophy (2-3 sentences)
- Full light + dark palette with semantic roles: bg, surface, overlay, muted, text, accent, success, warning, error, info
- All colors as HSL with OKLCH equivalent
- Contrast ratio table (every fg/bg combination)
- CSS custom properties ready to copy-paste
- Preview: what a blog post + code block would look like (ASCII mockup)

### Proposal A: "Warm Ink" (based on Flexoki/Everforest research)
Warm, paper-like light mode. Comfortable for long reading. Natural, not sterile.

### Proposal B: "Night Scholar" (based on Gruvbox/Tokyo Night research)
Dark-first palette. Rich, not just gray. Good for late-night coding and reading.

### Proposal C: "Balanced" (synthesis of best ideas)
Light + dark with shared accent. Maximum versatility. The "safe default" that still has personality.

## Output Format

All files as Markdown. Use tables for color specs. Include hex, HSL, and OKLCH for every color. Calculate actual contrast ratios (don't guess). Be opinionated — this is a personal system, not a framework.
