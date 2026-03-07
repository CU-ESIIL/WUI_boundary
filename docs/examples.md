# Project Patterns

This page captures reusable documentation patterns used in the `WUI_boundary` site.

## Navigation CTA pattern

Use this for concise internal calls-to-action.

[Back to Home](index.md){ .md-button .oasis-hover-button }

```md
[Back to Home](index.md){ .md-button .oasis-hover-button }
```

## Responsive iframe embed for UI drafts

Use this wrapper to keep embedded conceptual prototypes responsive.

<div class="oasis-embed">
  <iframe
    title="WUI Boundary Story Lab Draft 1"
    src="../ui-drafts/draft-1/story-lab.html"
    loading="lazy"
    allowfullscreen>
  </iframe>
</div>

```html
<div class="oasis-embed">
  <iframe
    title="WUI Boundary Story Lab Draft 1"
    src="../ui-drafts/draft-1/story-lab.html"
    loading="lazy"
    allowfullscreen>
  </iframe>
</div>
```

## Card grid

Use card grids to present top-level project sections.

<div class="grid cards" markdown>

- **UI Drafts**

  ---

  Link conceptual interfaces and transition plans.

- **Analytics**

  ---

  Link scaffold package docs and reproducible run steps.

- **Documentation**

  ---

  Link onboarding, conventions, and project history.

</div>

## Admonition

Use callouts for status and scope boundaries.

!!! tip
    Keep examples short and project-focused so contributors can reuse them without template cleanup.

---

For the current conceptual prototype, see [Draft 1 — WUI Boundary Story Lab](ui-drafts/draft-1.md).
