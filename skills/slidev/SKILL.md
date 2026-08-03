---
name: slidev-skill
description: Slidev markdown presentation work — creating projects, authoring slides, configuring themes and animations, exporting to PDF/PPTX/PNG, and building for deploy.
license: MIT
metadata:
  author: Vincent-the-gamer
  version: 1.0.1
  created: 2026-05-03
  last_reviewed: 2026-08-03
  review_interval_days: 90
  dependencies:
    - url: https://sli.dev/guide/
      name: Slidev Documentation
      type: docs
---

# Slidev

Slidev turns markdown into slide decks: every slide is a `---`-separated section in `slides.md`. Use `scripts/slidev_manager.py` for project operations, and edit `slides.md` directly for content. The full syntax, frontmatter, and CLI reference is in [`references/slidev-syntax.md`](references/slidev-syntax.md).

Slidev requires Node.js ≥ 22.0 and pnpm. Export to PDF/PPTX/PNG also needs `pnpm add -D playwright-chromium`.

## Create

Scaffold a new project:

```bash
python scripts/slidev_manager.py create <name> --theme <theme>
```

This writes `package.json`, `slides.md` (starter deck), and `README.md` into `<name>/`.

**Done when** `pnpm install && pnpm dev` runs without error.

## Author

All slide content lives in `slides.md`. Slides are separated by `---` on its own line. Global frontmatter (theme, title) goes in the first frontmatter block; per-slide frontmatter (layout, class, transition) goes between a `---` separator and the slide content.

To add or edit slides, modify `slides.md` directly. Run `slidev format` (or `python scripts/slidev_manager.py format`) to auto-format.

For the full syntax — code blocks, diagrams, math, layouts, presenter notes — see [`references/slidev-syntax.md`](references/slidev-syntax.md).

**Done when** the slide content matches the user's request and `slidev` dev server renders it.

## Style

Set the theme in the global frontmatter:

```yaml
---
theme: seriph
colorSchema: dark
---
```

Built-in themes: `default`, `seriph`. Install additional themes with `pnpm add @slidev/theme-<name>`. For custom styles per slide, use scoped `<style>` blocks. See [`references/slidev-syntax.md`](references/slidev-syntax.md) for the styling reference.

**Done when** the theme is set in frontmatter (and installed if external), and renders correctly in the dev server.

## Animate

Click animations use Vue directives in `slides.md`:

- `<v-click>` — content appears on the next click
- `<v-after>` — appears with the previous click
- `<v-clicks>` — each child appears on a successive click
- `v-motion` — motion effects (fade, slide, zoom)

Line-by-line code highlighting uses `{1|2|3}` after the language tag. See [`references/slidev-syntax.md`](references/slidev-syntax.md) for the full animation syntax.

**Done when** each requested animation triggers correctly in the dev server.

## Export

```bash
python scripts/slidev_manager.py export                          # PDF (default)
python scripts/slidev_manager.py export --format pptx             # PPTX
python scripts/slidev_manager.py export --format png              # PNG images
python scripts/slidev_manager.py export --with-clicks             # render click steps as pages
python scripts/slidev_manager.py export --dark                    # dark mode
python scripts/slidev_manager.py export --range 1,3-5,7           # specific slides
```

PDF and PPTX output is static — use `--with-clicks` to render each click step as a separate page. For full interactivity, build the SPA instead.

**Done when** the output file exists and the command exits with code 0.

## Build

```bash
python scripts/slidev_manager.py build [--base /subpath/]
```

Outputs to `dist/` — a static SPA that retains full interactivity. Host on any static host (Netlify, Vercel, GitHub Pages).

**Done when** `dist/` contains `index.html` and the command exits with code 0.

## Script

`scripts/slidev_manager.py` handles all Slidev operations:

| Command | Purpose |
|---|---|
| `create <name> [--theme]` | Scaffold a new project |
| `dev [--port]` | Start dev server |
| `export [--format] [--output] [--with-clicks] [--dark] [--range]` | Export slides |
| `build [--base]` | Build static SPA |
| `format` | Format `slides.md` |
| `info` | Show slide count and metadata |
