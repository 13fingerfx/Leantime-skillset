# Native UI, Dashboards, Widgets, And Visual Functions

Use this reference for Leantime UI tweaks, visual plugin screens, dashboards, widgets, modals, buttons, tables, forms, charts, and frontend assets.

## Inspect Before Designing

Before editing or creating UI:

1. Find two existing Leantime views that solve a similar layout.
2. Identify wrappers, headings, spacing, buttons, forms, table/list patterns, icons, and translation style.
3. Reuse those conventions before adding CSS.
4. Keep custom CSS small and local to the plugin.

## Native UI Rules

- Use Leantime's layout, page header, content wrapper, icon system, and form/table/button classes from the target version.
- Use translation keys for visible strings.
- Match existing density. Leantime is a working app, not a marketing page.
- Prefer familiar controls: icon buttons for commands, toggles/checkboxes for binary settings, selects for option sets, tabs for view switching.
- Keep dashboard widgets scannable and responsive.
- Do not hard-code brand colors unless the target version already exposes that value and nearby UI uses it.
- Avoid decorative gradients, oversized hero sections, and floating card stacks for operational screens.

## Accessibility And Responsiveness

Check:

- text contrast against backgrounds
- keyboard-accessible buttons and links
- labels for form controls
- mobile layout for dashboards and tables
- no text overlap or clipped controls
- dynamic content cannot resize fixed-format controls unexpectedly

## Visual Validation

For significant UI work, run the local Leantime app and inspect screenshots at desktop and mobile widths. If a dev server is unavailable, still inspect generated Blade/CSS against nearby templates and explain the validation gap.

## Red Flags

- New CSS file with many colors, shadows, radii, or spacing tokens.
- UI passes backend tests but "does not feel like Leantime."
- Dashboard tables overflow mobile screens.
- Plugin uses raw English text in templates.
- Modal or workflow controls do not match nearby app behavior.
