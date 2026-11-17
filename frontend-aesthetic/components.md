# Component Design Rules

## Component Vocabulary

Prefer semantic, product-specific components:
Transaction
AccountSummary
PaymentCard
LoanStatus
UsageChart
ProductPreview
Integration
ActivityFeed
CustomerTable

Avoid visual-only naming:
FancyCard
BlueBox
GradientContainer
BigCard
ModernButton

## Canonical Components

Maintain one canonical implementation for each primitive:
- Button
- Input
- Select
- Dialog
- Card
- Badge
- Table
- Tabs
- Tooltip

Extend variants through tokens/props instead of cloning components.

## Buttons

Use a clear hierarchy:
- primary
- secondary
- tertiary/ghost
- destructive when necessary

Avoid gradient buttons by default.

## Icons

Use one icon family consistently.
Keep stroke weight and optical sizing consistent.
Do not add icons merely to fill empty space.

## Cards

A card must group meaningful information.
If removing the card improves the design, remove it.

## Product Mockups

Use believable:
- labels
- numbers
- statuses
- timestamps
- table rows
- user flows

Never use fake data to imply real customers, revenue, security certifications, awards, or performance claims.

## Forms

Forms should prioritize:
label → field → helper → validation → action

Design:
- focus
- error
- disabled
- loading
- success

## Charts

Charts must answer a question.
Every axis, legend, tooltip and annotation should have purpose.
Avoid decorative charts with invented trends.

## Navigation

Keep navigation stable and predictable.
Do not add menus simply because other SaaS sites have them.

## Accessibility

Use semantic HTML.
Ensure keyboard navigation.
Provide visible focus.
Use sufficient contrast.
Use accessible names for controls.
Keep touch targets usable.
Support reduced motion.
