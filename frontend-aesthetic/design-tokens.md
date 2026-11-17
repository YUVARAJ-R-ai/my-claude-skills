# Design Tokens

Use this as a starting framework. Adapt it to the product and existing repository.

## Color

Prefer:
- 1 main background
- 1 surface
- 1 elevated surface
- primary text
- secondary text
- muted text
- subtle border
- 1 brand accent
- semantic success/warning/error/info

Example light values:
background: #FAFAFA
surface: #FFFFFF
subtle: #F5F5F5
text: #171717
secondary: #525252
muted: #8A8A8A
border: rgba(0,0,0,0.08)

Example dark values:
background: #08090A
surface: #111214
elevated: #181A1D
text: #F7F8F8
secondary: #A1A1AA
muted: #71717A
border: rgba(255,255,255,0.08)

These are examples, not mandatory brand colors.

## Typography

Use one primary family and optionally one monospace family.

Starting scale:
- display: 64–96px
- H1: 48–64px
- H2: 32–48px
- H3: 20–28px
- body: 15–18px
- metadata: 12–14px

Adjust based on viewport and product.

Avoid arbitrary sizes throughout the UI.

## Spacing

Prefer a coherent scale such as:
4, 8, 12, 16, 24, 32, 48, 64, 80, 96, 128

## Radius

Example hierarchy:
- inputs/buttons: 8–12px
- cards: 12–18px
- large panels: 16–24px
- pills: full radius

Do not make everything a pill or giant rounded rectangle.

## Shadows

Use shadows sparingly.
Prefer subtle elevation and borders.
Do not give every card a large shadow.

## Motion

Starting durations:
- micro: 120–200ms
- component: 180–300ms
- large: 300–500ms

Respect prefers-reduced-motion.

## Container

Typical marketing max-width:
1200–1400px

Text blocks:
approximately 600–750px where appropriate.

Do not stretch paragraphs across the entire viewport.
