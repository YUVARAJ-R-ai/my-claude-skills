---
name: gamma-ui-style
description: Use this skill whenever the user wants a UI, landing page, or dashboard built in the "Gamma.app style" — warm cream backgrounds, soft pastel gradient blobs, big rounded pill buttons, generous whitespace, sparkle/badge accents, and clean rounded-sans typography. Trigger on phrases like "gamma style", "like gamma.app", "soft/cream/pastel SaaS UI", or any request to build a marketing site AND a companion dashboard/app with multiple routes that should share one consistent design system. Covers both marketing-page patterns (hero, feature grid, testimonials, FAQ) and app-shell/dashboard patterns (sidebar nav, multi-route layout, tables, empty states) in the same visual language.
---

# Gamma.app-style UI System

A design system that mimics gamma.app's aesthetic: warm, soft, confident, slightly playful SaaS design — and extends it into a proper multi-route dashboard/app shell so a marketing site and its app feel like one product.

Read this whole file before generating code. It's organized as: **1) Design tokens**, **2) Marketing-page patterns**, **3) Dashboard/app-shell patterns**, **4) Build rules**.

## 1. Design tokens

Use these as CSS custom properties (or Tailwind config extensions) in every build. Don't invent a different palette mid-project.

```css
:root {
  /* Backgrounds — warm, never stark white or cool gray */
  --bg-canvas: #FBF7F1;        /* main page background, warm cream */
  --bg-surface: #FFFFFF;       /* cards, panels */
  --bg-sunken: #F3EDE4;        /* subtle recessed areas, table stripes */

  /* Text */
  --text-primary: #1F1B16;     /* near-black, warm not pure black */
  --text-secondary: #6B6459;   /* muted warm gray for body copy */
  --text-tertiary: #A39C8E;    /* captions, placeholders */

  /* Accent palette — soft pastels used for gradient blobs, badges, illustrations */
  --accent-purple: #B9A6F5;
  --accent-pink:   #F6B9CE;
  --accent-peach:  #FAD4B0;
  --accent-yellow: #F5E28C;
  --accent-mint:   #B7E8D0;
  --accent-blue:   #AFCBF0;

  /* Primary brand action — deep, confident, NOT the pastel accents */
  --brand-primary: #2E2A26;    /* near-black pill buttons, like gamma's CTA */
  --brand-on-primary: #FFFFFF;
  --brand-gradient: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));

  /* Borders / shadows — soft, never harsh */
  --border-subtle: #EFE7DA;
  --shadow-soft: 0 8px 24px -8px rgba(31,27,22,0.12);
  --shadow-card: 0 2px 8px rgba(31,27,22,0.06);

  /* Radii — everything is rounded, this is core to the look */
  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-pill: 999px;

  /* Spacing scale */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-6: 24px; --space-8: 32px; --space-12: 48px; --space-16: 64px; --space-24: 96px;
}
```

**Typography**
- Headings: a rounded/geometric grotesque — `"Inter", "General Sans", -apple-system, sans-serif`. Weight 600–700. Headlines are large (clamp(2.5rem, 5vw, 4rem)) and tight line-height (1.05–1.1), often with one word or phrase in an accent color or italic serif for personality.
- Body: same family, weight 400, `--text-secondary`, line-height 1.6, comfortable size (16–18px).
- Never use a default system serif or a harsh monospace for UI chrome.

**Signature visual motifs (use these, they ARE the Gamma look)**
- Soft irregular gradient "blob" shapes bleeding off-canvas behind hero sections — low-opacity, large, blurred.
- Pill-shaped buttons and badges everywhere (`border-radius: var(--radius-pill)`), never sharp-cornered buttons.
- Small sparkle/star accent glyphs (✦ or a 4-point star SVG) near AI/generate-related CTAs.
- Cards with large radius (16–24px), thin 1px warm-gray border OR soft shadow — not both heavy.
- Generous negative space; sections breathe with 64–96px vertical padding.
- Product screenshots/illustrations shown inside soft rounded frames, often slightly overlapping the section above.
- Logo strips in muted grayscale, low opacity, evenly spaced.

## 2. Marketing-page patterns

Standard section order for a Gamma-style landing page:
1. **Nav** — logo left, text links center/right, ghost "Login" + solid dark pill "Start for free" button. Nav bar transparent over hero, background blurs in on scroll.
2. **Hero** — huge headline (mixed weight/color emphasis on key phrase), one-line subhead in `--text-secondary`, two CTAs (solid pill + ghost/text link), gradient blob behind, product screenshot or looping video below fold-line, slightly overlapping the hero.
3. **Logo cloud** — "trusted by" strip, grayscale logos, low opacity.
4. **Feature grid** — 3–6 cards, each: small icon/illustration on soft accent-colored rounded square, bold short title, one-sentence description. NOT dense paragraphs.
5. **Alternating feature showcase** — image/video left, text right, then flip; repeat 2–3 times, each block on its own subtle background tint.
6. **Social proof / testimonials** — grid or masonry of quote cards, bold the key phrase inside each quote, name + role + small avatar.
7. **FAQ** — accordion, warm surface background, one question open by default.
8. **Closing CTA** — centered, big headline, single pill button, often on a full-bleed gradient or dark section for contrast.
9. **Footer** — multi-column link groups on `--bg-sunken`, social icons, app store badges if relevant.

## 3. Dashboard / multi-route app-shell patterns

When the user wants "the same style but for a dashboard/app with multiple routes," carry the same tokens but shift density — dashboards need more information density than marketing pages while keeping the warm, rounded, soft-shadow language.

**App shell layout**
- Persistent left sidebar (240–280px), `--bg-surface` on `--bg-canvas` page background, rounded selection pill behind the active nav item (not just a text color change — Gamma-style relies on soft filled pills for active state).
- Sidebar sections: workspace/brand switcher at top, primary nav items with icon + label, secondary/settings nav pinned to bottom, user avatar + account menu at very bottom.
- Top bar (56–64px) inside main content area: breadcrumb or page title left, search + primary action pill button + avatar right. Keep it on `--bg-canvas`, not a hard white bar — avoid a harsh line between topbar and sidebar.
- Main content area: max-width container with `--space-8` to `--space-12` padding, cards use `--radius-lg` and `--shadow-card`.

**Routing structure (React Router / Next.js App Router — pick to match stack)**
```
/                → marketing site (patterns from section 2)
/app             → dashboard shell (layout route wrapping all authenticated pages)
  /app/overview  → summary cards + charts (default landing after login)
  /app/[resource]         → list/table view
  /app/[resource]/[id]    → detail/edit view
  /app/[resource]/new     → create flow
  /app/settings           → account, billing, team — nested tabs
```
Use a shared layout component (`AppShell`) that renders sidebar + topbar once and an `<Outlet />`/`{children}` for the route content, so every route inherits the same chrome automatically — don't re-implement the shell per page.

**Core dashboard components, in the same visual language**
- **Stat cards**: rounded-lg surface, small label in `--text-tertiary`, large number in heading weight, small colored delta badge (pill, mint for positive / pink for negative).
- **Tables**: no heavy grid lines — row separation via `--bg-sunken` zebra striping or 1px `--border-subtle`, row hover = soft `--bg-sunken` tint, actions revealed as icon buttons on hover, pagination as pill buttons.
- **Empty states**: centered illustration in accent pastel colors, short friendly headline, single pill CTA — never a bare "No data" text.
- **Forms**: labels above inputs, inputs with `--radius-md`, soft focus ring in `--accent-purple` at 40% opacity, primary submit as solid dark pill, destructive actions as text-only red, not a filled red button.
- **Modals/drawers**: `--radius-lg`, soft shadow, blurred scrim behind (backdrop-filter: blur(4px) over rgba(31,27,22,0.2)).
- **Toasts/notifications**: pill-shaped, `--bg-surface` with colored left accent bar, auto-dismiss.

**UX rules to actually make multi-route navigation good, not just pretty**
- Active route always has a visible state in the sidebar (filled pill), not just bold text — accessibility and glanceability both need this.
- Breadcrumbs on any route nested more than one level deep (`/app/customers/42/invoices`).
- Persist scroll position and filters when navigating away and back to a list route (don't reset table state on every mount).
- Loading state per-route uses skeleton cards matching the real card shapes (rounded rectangles in `--bg-sunken` with shimmer), not a full-page spinner, so layout doesn't jump.
- 404/empty-permission routes reuse the "empty state" component, not a generic browser-style error page.
- Mobile: sidebar collapses to a bottom tab bar or slide-over drawer, never a squished mini-sidebar.

## 4. Build rules

- Always define the CSS variables from section 1 at the top of the stylesheet/config, even if only a subset is used — keeps follow-up requests in this conversation visually consistent.
- If building in React, prefer Tailwind with the tokens mapped into `tailwind.config` (`theme.extend.colors`, `borderRadius`) over inline styles, so the design system is reusable across routes.
- If asked for "just the landing page," still set up the token file — it makes it trivial to extend into the dashboard later, which is a common follow-up.
- Don't mix in sharp corners, pure black (#000), or pure white (#FFF) backgrounds anywhere — that immediately breaks the warm Gamma feel.
- When in doubt about a component not covered above, default to: rounded corners, soft shadow over hard border, pill buttons, warm cream base with one pastel accent per section.
