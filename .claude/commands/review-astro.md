---
description: Audit Astro components and Starlight docs for usability, accessibility, performance, componentization, best practices, security, maintainability, and design. Pass scope as argument (e.g. "components in this branch", "docs/src/components/Grid.astro", "all landing components").
---

# Astro/Starlight Component Review Workflow

Act as an expert in **Astro**, **Starlight**, and **UX/UI**. Audit the specified components and/or Starlight pages with zero tolerance for design, performance, and accessibility issues.

## 1. Understand Scope

The user has specified: **$ARGUMENTS**

If no argument is provided, ask the user what to review before proceeding.

Resolve scope to a concrete list of files:
- "components in this branch" → `git diff --name-only origin/main...HEAD` filtered to `docs/src/components/` and `docs/src/content/docs/`
- "landing components" → all files in `docs/src/components/` + `docs/src/content/docs/index.mdx`
- A specific file path → that file only
- Any other description → infer the most reasonable set of files and confirm with the user

## 2. Read Context

Before auditing, always read:
- `docs/astro.config.mjs` — integrations, plugins, Starlight config
- `docs/package.json` — dependencies and versions in use

Then read every file in scope fully. For each component, also read the pages that use it to understand real usage.

## 3. Audit Dimensions

Analyze every file against all of the following. Be strict.

### 3.1 Usability
- Interactive elements have clear, descriptive labels
- User flow is obvious without explanation
- No confusing or ambiguous UI states

### 3.2 Accessibility (WCAG 2.1 AA minimum)
- Images have meaningful `alt` (empty only when purely decorative)
- Interactive elements keyboard-navigable and focus-visible
- Color contrast: 4.5:1 text, 3:1 large text / UI components
- ARIA roles, labels, landmarks correct and not redundant
- No `div`/`span` used as interactive without `role` + `tabindex`
- Semantic HTML: heading order, landmark elements (`<nav>`, `<main>`, `<section>`, `<article>`)
- Animation respects `prefers-reduced-motion`

### 3.3 Performance
- No `client:*` directives unless JavaScript is genuinely required at runtime
- Images use `<Image>` from `astro:assets`, not raw `<img>`
- No render-blocking patterns
- No large inline SVGs that should be externalized
- Icons loaded efficiently (no per-icon HTTP request if using an icon set)
- No runtime style calculations where static CSS suffices

### 3.4 Componentization
- Single responsibility per component
- Props typed with a `Props` TypeScript interface in the `---` frontmatter
- No logic duplicated across components
- Granularity appropriate: not monolithic, not over-fragmented
- Slots used correctly for content projection

### 3.5 Astro/Starlight Best Practices
- Starlight built-in components used where available instead of custom reimplementations
- `astro:content` collections used for data-driven content, not hardcoded arrays in `.mdx`
- No anti-patterns: `document.querySelector` in Astro component scripts, incorrect SSR/CSR mixing
- CSS scoped to component via `<style>` tag, not global where avoidable
- No `!important` abuse
- Starlight CSS custom properties used (`var(--sl-color-accent)`, etc.) for theming, not hardcoded colors

### 3.6 Security
- No `set:html` with unsanitized content
- External scripts have `integrity` attribute (SRI)
- External links use `rel="noopener noreferrer"`
- No secrets or tokens in component source

### 3.7 Long-term Maintainability
- No magic strings or hardcoded values that belong in config/constants
- Component and prop names self-documenting
- No deeply nested conditional rendering
- No dead code (unused props, unreachable branches, commented-out blocks)

### 3.8 Hidden Bugs
- Props that can be `undefined` used without guards
- Missing keys in list rendering (`.map()` expressions)
- CSS class name typos or missing styles
- Broken or context-dependent URL paths

### 3.9 Code Repetition
- Identical markup blocks that should be extracted into a sub-component
- Copy-paste styles that should be a shared CSS class or custom property

### 3.10 Code Readability
- Clear and consistent variable/prop names
- Complex conditionals extracted into named variables
- Files that are too long and should be split

### 3.11 Industry Patterns
- Composition over inheritance: slot-based composition preferred
- Data via props, not implicit global state, for reusable components
- Container/Presentational separation where applicable

### 3.12 Design
- Spacing, typography, and color follow a coherent system
- Starlight CSS custom properties used instead of hardcoded brand values
- Components responsive at mobile/tablet/desktop breakpoints
- Dark mode works via CSS variables — no hardcoded light-only colors
- No fixed pixel widths that break at non-standard viewports

## 4. Findings Report

Categorize every finding:

1. **Critical** — broken functionality, security issue, WCAG failure, render-blocking problem. Fix immediately.
2. **Improvement** — performance, maintainability, or pattern issues. Explain why and how.
3. **Style** — readability, naming, minor design inconsistency.

Each finding must include:
- **Location**: `file:line`
- **Problem**: what is wrong and why it matters
- **Fix**: concrete change to apply

## 5. Execution

After the report, ask the user which findings to fix. Then:

1. Apply approved fixes
2. Verify affected pages still render correctly
3. Confirm no Starlight built-in behavior broken (sidebar, TOC, search, i18n, dark mode)
4. Present a summary of all changes made
