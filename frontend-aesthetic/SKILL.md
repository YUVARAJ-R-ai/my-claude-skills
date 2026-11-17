---
name: frontend-aesthetic
description: Build polished, human-crafted web interfaces with restrained visual systems, strong hierarchy, authentic product UI, and deliberate responsive behavior. Use for marketing sites, SaaS products, and dashboards. Prevent generic AI-generated aesthetics.
---

# Frontend Aesthetic Skill

## Mission

Build interfaces that feel intentional, product-specific, premium, calm, and human-designed—not like a generic AI-generated SaaS template.

Primary references for principles:
- Stitch: authentic product UI and product storytelling
- Stripe: technical credibility and hierarchy
- Linear: restraint, spacing, typography, motion
- Vercel: engineered minimalism and system consistency
- Mercury: editorial calm and premium composition
- Ramp/Brex: product-led fintech presentation

Do not copy layouts, branding, or assets from references. Extract principles.

## Operating Rules

1. Inspect the existing repository before changing UI.
2. Reuse the existing design system, tokens, primitives, and components when they exist.
3. Establish visual tokens before creating many components.
4. Build the hierarchy before decorating.
5. Prefer authentic product UI over decorative illustrations.
6. Use one coherent visual language across the product.
7. Make every visual element earn its place.
8. Design all important states: default, hover, focus, loading, empty, error, disabled, success, sparse and dense.
9. Treat mobile/responsive behavior as part of the design, not a final patch.
10. Finish with the audit in `audit.md`.

## Core Principle

When forced to choose:
- hierarchy over visual effects
- clarity over novelty
- authentic product UI over decorative graphics
- consistency over variety
- whitespace over unnecessary content
- one strong accent over many colors
- meaningful motion over animation for animation's sake

## Visual Balance

Aim for roughly 80% quiet visual surface and 20% visual emphasis. Do not make every section colorful, animated, rounded, glowing, or oversized.

## Before Coding

Answer:
- Who uses this?
- What is the primary task?
- What information matters most?
- What action matters most?
- What should the eye see first?
- What should be ignored?
- Is this a marketing page, application UI, dashboard, or hybrid?
- What visual personality fits the product?

## Anti-AI-Smell Rules

Avoid unless explicitly justified by the brand:
- purple/pink/blue gradient overload
- gradient text
- glassmorphism everywhere
- giant glowing blobs
- excessive 3D decoration
- identical rounded cards
- giant shadows
- excessive pills
- meaningless icons
- every section centered
- every section using the same composition
- excessive fade/slide animations
- fake statistics
- fake testimonials
- unrealistic product data
- random font sizes
- random spacing
- too many colors
- too many typefaces
- decorative UI with no semantic purpose

If several of these appear together, redesign instead of polishing.

## Human-Eye Test

Before shipping, inspect the rendered page and ask:
1. What do I see first?
2. What do I see second?
3. Is anything competing with the primary element?
4. Does each element have a reason?
5. Does the interface look like a template?
6. Does the UI communicate what the product actually does?
7. Could this screenshot belong to hundreds of unrelated startups?

If the answer to the last two questions is yes, introduce product-specific UI and composition.

## 5-Second Test

A screenshot should communicate the product's purpose or primary task within approximately five seconds.

## Implementation Workflow

1. Inspect repo and existing tokens/components.
2. Identify product and user goals.
3. Choose visual direction.
4. Define or extend tokens.
5. Define component vocabulary.
6. Design one representative section/screen.
7. Check hierarchy and density.
8. Build remaining UI.
9. Add responsive behavior.
10. Add interaction states.
11. Add restrained motion.
12. Run accessibility checks.
13. Run `audit.md`.
14. Remove anything unnecessary.

Never generate an entire large product blindly in one pass.

## Technology Guidance

Use the project's existing framework and component system.

For React/Next/Tailwind projects:
- prefer CSS variables/design tokens
- use semantic component names
- avoid one-off arbitrary values when a token exists
- keep reusable primitives canonical
- avoid duplicate Button/Card/Input variants created only because of visual tweaking

## Quality Bar

The final result should look like a product with a coherent design system, not a collection of individually attractive components.
