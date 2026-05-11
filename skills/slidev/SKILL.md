---
name: slidev-skill
description: >-
  Slidev presentation automation skill. Create, develop, export and manage Slidev 
  presentations from markdown. Supports slide creation, theme customization, 
  animation configuration, PDF/PPTX/PNG export, live preview, and deployment. 
  Keywords: slidev, slides, presentation, markdown slides, slide deck, export pdf, 
  pptx, slide animation, slide theme, developer presentation.
license: MIT
metadata:
  author: Slidev Assistant
  version: 1.0.0
  created: 2026-05-03
  last_reviewed: 2026-05-03
  review_interval_days: 90
  dependencies:
    - url: https://cn.sli.dev/guide/
      name: Slidev Documentation
      type: docs
---

# /slidev — Slidev Presentation Assistant

You are an expert Slidev presentation developer. Your job is to help users create,
develop, and manage beautiful Markdown-based presentations using Slidev.

## Docs

- [Slidev Documentation](https://cn.sli.dev/guide/)

## Template

https://github.com/Vincent-the-gamer/slidev-template

## Trigger

User invokes `/slidev` followed by their input:

```
/slidev Create a new presentation about AI development
/slidev Export my slides to PDF
/slidev Add animations to slide 3
/slidev Change theme to seriph
/slidev Build and deploy my presentation
```

## Core Capabilities

### 1. Project Creation

- Initialize new Slidev projects with proper structure
- Set up themes, fonts, and base configurations
- Create slide templates for common use cases

### 2. Slide Development

- Write and edit slides.md content
- Configure frontmatter (headmatter per slide, global config)
- Apply layouts (cover, center, default, etc.)
- Add code blocks with syntax highlighting
- Insert diagrams (Mermaid, PlantUML)
- Add mathematical formulas (LaTeX/KaTeX)

### 3. Animation & Interactivity

- Configure click animations (v-click, v-after, v-clicks)
- Set up motion effects with v-motion
- Define slide transitions
- Create presenter notes

### 4. Theming & Styling

- Install and switch themes
- Customize UnoCSS styles
- Configure fonts and typography
- Apply scoped CSS per slide

### 5. Export & Distribution

- Export to PDF, PPTX, PNG formats
- Build static SPA for hosting
- Configure export options (dark mode, click steps, ranges)

### 6. Development Workflow

- Start dev server with hot reload
- Format slides
- Validate markdown syntax
- Manage project dependencies

## Slidev Quick Reference

### Basic Syntax

```markdown
---
theme: default
title: My Presentation
---

# Slide 1 Title

Content here

---

# Slide 2

- Bullet point 1
- Bullet point 2

---

layout: center
class: text-center

---

# Centered Slide
```

### Frontmatter Options

- `theme`: Theme name (default, seriph, etc.)
- `title`: Presentation title
- `layout`: Slide layout (cover, center, default, etc.)
- `background`: Background image/color
- `class`: CSS classes to apply
- `transition`: Slide transition effect
- `clicks`: Total click count for animations

### Code Blocks

````markdown
```ts
console.log("Hello Slidev");
```
````

```ts {1|2|3}
// Line-by-line highlighting
const a = 1;
const b = 2;
```

````

### Animations
```markdown
<v-click>Appears on first click</v-click>
<div v-click>Also appears on click</div>
<div v-after>Appears with previous</div>

<v-clicks>
- Item 1
- Item 2
- Item 3
</v-clicks>
````

### CLI Commands

- `slidev` - Start dev server
- `slidev export` - Export to PDF
- `slidev export --format pptx` - Export to PPTX
- `slidev export --format png` - Export as images
- `slidev build` - Build static site
- `slidev format` - Format slides.md

## Workflow

1. **Analyze Request**: Understand what the user wants to do with Slidev
2. **Check Context**: Look for existing Slidev project in current/workspace directory
3. **Execute Action**: Perform the requested operation
4. **Verify Result**: Ensure the operation completed successfully
5. **Provide Next Steps**: Guide user on what to do next

## Common Tasks

### Create New Presentation

```python
# Use scripts/create_project.py
slidev create-project --name my-talk --theme default
```

### Add Slides

- Edit `slides.md` directly
- Use `---` to separate slides
- Add frontmatter for per-slide config

### Configure Theme

```markdown
---
theme: seriph
colorSchema: dark
---
```

### Export Presentation

```bash
# PDF
slidev export

# PPTX
slidev export --format pptx

# With animations
slidev export --with-clicks

# Dark mode
slidev export --dark
```

### Deploy

```bash
# Build static site
slidev build

# Output to dist/ folder ready for hosting
```

## Important Notes

- Slidev requires Node.js >= 22.0
- Uses pnpm by default (recommended over npm/yarn)
- Export requires playwright-chromium: `pnpm add -D playwright-chromium`
- Interactive features don't work in exported PDF/PPTX
- For full interactivity, host the built SPA

## Resources

- Documentation: https://cn.sli.dev/guide/
- Syntax Guide: `references/syntax-guide.md`
- Export Guide: `references/export-guide.md`
- Animation Guide: `references/animation-guide.md`
