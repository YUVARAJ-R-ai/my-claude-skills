# Frontend Aesthetic Audit

Run this after implementation.

## A. Hierarchy

- [ ] Is there one clear primary element per screen/section?
- [ ] Is the reading/scanning order obvious?
- [ ] Are secondary elements visually subordinate?
- [ ] Are important actions easy to find?

## B. AI-Smell Audit

Count violations:
- [ ] unnecessary gradients
- [ ] gradient text
- [ ] glassmorphism overload
- [ ] glowing blobs
- [ ] excessive rounded cards
- [ ] excessive shadows
- [ ] excessive pills
- [ ] meaningless icons
- [ ] repetitive section composition
- [ ] excessive animation
- [ ] giant headings everywhere
- [ ] too many colors
- [ ] inconsistent typography
- [ ] inconsistent spacing
- [ ] fake-looking product data
- [ ] decorative UI with no purpose

If 3 or more are present in the same area, redesign it.

## C. Human-Eye Audit

Ask:
1. What do I notice first?
2. What do I notice second?
3. Where does my eye stop?
4. Is anything fighting for attention?
5. Does the page feel calm or noisy?
6. Does it feel like a coherent product?
7. Does it feel specific to this company?
8. Could I replace the logo with another startup and nothing would feel different?

If #8 is yes, improve product specificity.

## D. Consistency

- [ ] Same spacing scale
- [ ] Same radius system
- [ ] Same border treatment
- [ ] Same icon family
- [ ] Same typography system
- [ ] Same interaction language
- [ ] Same semantic color usage

## E. Content Authenticity

- [ ] No invented testimonials
- [ ] No invented statistics
- [ ] No fake customer logos
- [ ] No fake certifications
- [ ] No meaningless dashboard numbers
- [ ] Product UI uses believable domain-specific data

## F. Responsive

Check:
- desktop
- tablet
- mobile

Verify:
- no horizontal overflow
- hierarchy remains intact
- navigation remains usable
- tables remain usable
- touch targets remain practical
- text does not become cramped
- important actions remain visible

## G. Accessibility

- [ ] keyboard navigation
- [ ] visible focus
- [ ] semantic HTML
- [ ] labels
- [ ] contrast
- [ ] reduced motion
- [ ] accessible control names
- [ ] sensible touch targets

## H. Motion

- [ ] Motion communicates state or hierarchy
- [ ] No animation exists solely because it looks cool
- [ ] No excessive simultaneous animations
- [ ] Reduced-motion behavior exists

## I. Final Removal Pass

Remove 10% of decorative elements if the interface can survive without them.

A polished interface often becomes better by subtraction.

## Final Gate

Do not declare the UI complete if:
- the hierarchy is unclear
- the design system is inconsistent
- the page looks interchangeable with a generic SaaS template
- major states are missing
- responsive behavior is broken
- product UI is decorative rather than meaningful
