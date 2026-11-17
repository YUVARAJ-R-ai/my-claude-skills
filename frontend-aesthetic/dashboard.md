# Dashboard / Product UI Mode

The core aesthetic principles apply to dashboards, but the priorities change.

Marketing page priority:
hierarchy → storytelling → persuasion → whitespace

Dashboard priority:
scanability → information hierarchy → speed → interaction → density

## Dashboard Principles

1. Users should find the primary information immediately.
2. Navigation should be predictable.
3. Related data should be grouped.
4. Density should increase where users perform detailed work.
5. Decorative elements must never compete with data.
6. Use color primarily for semantic meaning.
7. Prefer quiet surfaces and strong typography.
8. Tables should be calm and scannable.
9. Charts must communicate actual information.
10. Every state must be designed.

## Typical Structure

APP SHELL
- sidebar/top navigation
- contextual header
- search/actions
- content area

CONTENT
- page title
- primary metric/action
- supporting metrics
- visualization
- detailed table/list
- secondary modules

Do not force every dashboard into this exact structure.

## Cards

Cards are useful for grouping information, but avoid twelve identical cards.

Use different compositions for:
- KPI
- chart
- table
- activity
- status
- task
- detail

## Data Hierarchy

Example:

Revenue
$2.48M
↑ 14.2%
vs previous period

Then detailed chart/table.

Do not bury the important value inside paragraphs.

## Tables

Prefer:
- compact typography
- clear column alignment
- subtle row separation
- sticky headers where appropriate
- semantic status indicators
- tabular numerals for comparable numbers

Avoid:
- rainbow rows
- giant borders
- oversized icons
- excessive rounded cells

## Color Semantics

Reserve colors for meaning:
- success
- warning
- destructive/error
- information
- interaction/accent

Do not assign random colors to metrics merely to make cards colorful.

## Density

Suggested:
- overview: low/medium density
- analytics: medium/high
- tables: high
- settings: medium
- forms: medium
- detail views: medium/high

## States

Design:
- loading
- skeleton
- empty
- first-use
- populated
- sparse
- dense
- error
- offline where relevant
- permission denied
- disabled
- success

Skeletons should preserve final geometry and prevent layout shift.

## Interaction

Hover, focus, selection, filtering, sorting, pagination, dialogs, drawers and menus should have clear states.

Do not use animation as decoration.

## Responsive Dashboard

On smaller screens:
- collapse navigation intelligently
- preserve primary actions
- turn wide tables into useful mobile representations rather than simply shrinking text
- prioritize important columns
- allow horizontal scrolling where appropriate
- maintain touch targets
- preserve information hierarchy
