# SUN's Blog (Astro 7 + MDX)

Personal technical notebook built with **Astro 7**, **MDX**, **Shiki** (dual Day/Night themes), **KaTeX** (numbered IEEE-style equations), **Mermaid** (adaptive Day/Night SVG diagrams), and zero-dependency Vanilla CSS systems components.

## Quick Commands

```bash
# Start local dev server (http://127.0.0.1:4321/blog/)
npm run dev

# Build static production site into ./dist
npm run build

# Import a Jupyter Notebook (.ipynb) with preserved outputs & collapsible code cells
python3 scripts/import_ipynb.py path/to/notebook.ipynb --slug my-post-slug --date 2026-11-04
```

## Switching Between `/blog` Subpath and Root `sunbc0120.github.io`

- By default, `astro.config.mjs` sets `base: '/blog'` (matching `https://sunbc0120.github.io/blog/`).
- If you move the repository to `sunbc0120/sunbc0120.github.io`, set `ASTRO_BASE=/` in `.github/workflows/deploy.yml` (or default `BASE_PATH` to `'/'` in `astro.config.mjs`). All Markdown image and link paths adjust automatically via `rehypePrefixBase`.
