#!/usr/bin/env python3
"""Convert a Jupyter Notebook (.ipynb) into an Astro Content Collection Markdown post.

Preserves Fastpages/Quarto cell directives (#collapse-hide, #collapse-show, #collapse-output),
streams/execute_result text outputs, and extracts embedded base64 PNG/SVG figures into public/images/.

Usage:
  python3 scripts/import_ipynb.py path/to/2026-11-04-my-note.ipynb --slug my-note
"""

import argparse
import base64
import html
import json
import re
from pathlib import Path


def normalize_display_math(md_text: str) -> str:
    """Ensure single-line $$...$$ outside code fences become multi-line display math for remark-math."""
    lines = md_text.splitlines()
    out = []
    in_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("````"):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence:
            m = re.match(r"^\s*\$\$(.+?)\$\$\s*$", line)
            if m:
                out.append("$$")
                out.append(m.group(1).strip())
                out.append("$$")
                continue
        out.append(line)
    return "\n".join(out)


def convert_notebook(
    nb_path: Path,
    project_root: Path,
    slug: str,
    pub_date: str,
    legacy_paths: list[str] | None = None,
    img_rewrite: tuple[str, str] | None = None,
) -> Path:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])

    title = slug.replace("-", " ").title()
    description = f"Technical notebook: {title}"
    categories = ["jupyter", "python"]
    toc = True

    start_idx = 0
    if cells and cells[0].get("cell_type") == "markdown":
        c0 = "".join(cells[0].get("source", []))
        lines = c0.splitlines()
        if lines and lines[0].startswith("# "):
            title = lines[0][2:].strip()
            start_idx = 1
            desc_parts = []
            for ln in lines[1:]:
                s = ln.strip()
                if s.startswith(">"):
                    desc_parts.append(s.lstrip(">").strip())
                elif s.startswith("- categories:"):
                    raw_cats = s.split(":", 1)[1].strip().strip("[]")
                    categories = [c.strip().strip("'\"") for c in raw_cats.split(",") if c.strip()]
                elif s.startswith("- toc:"):
                    toc = "true" in s.lower()
            if desc_parts:
                description = " ".join(desc_parts)

    img_out_dir = project_root / "public" / "images" / "notebooks" / slug
    body_chunks: list[str] = []

    for idx, cell in enumerate(cells[start_idx:], start=start_idx):
        ctype = cell.get("cell_type")
        src = "".join(cell.get("source", []))
        if not src.strip():
            continue

        if ctype == "markdown":
            if img_rewrite:
                src = src.replace(img_rewrite[0], img_rewrite[1])
            src = normalize_display_math(src)
            body_chunks.append(src.strip())
        elif ctype == "code":
            lines = src.splitlines()
            collapse_code = False
            collapse_output = False
            cleaned_lines = []
            for ln in lines:
                tag = ln.strip().lower()
                if tag.startswith("#collapse-hide") or tag.startswith("#| code-fold: true"):
                    collapse_code = True
                elif tag.startswith("#collapse-show"):
                    continue
                elif tag.startswith("#collapse-output"):
                    collapse_output = True
                else:
                    cleaned_lines.append(ln)

            code_str = "\n".join(cleaned_lines).strip()
            if code_str:
                fenced = f"```python\n{code_str}\n```"
                if collapse_code:
                    body_chunks.append(
                        f'<details class="nb-collapse">\n<summary>Show helper code</summary>\n\n{fenced}\n\n</details>'
                    )
                else:
                    body_chunks.append(fenced)

            # Collect outputs
            text_outputs: list[str] = []
            img_mds: list[str] = []
            for o_idx, out in enumerate(cell.get("outputs", [])):
                otype = out.get("output_type")
                if otype == "stream":
                    txt = "".join(out.get("text", []))
                    if txt.strip():
                        text_outputs.append(txt.rstrip())
                elif otype in ("execute_result", "display_data"):
                    data = out.get("data", {})
                    if "image/png" in data:
                        img_out_dir.mkdir(parents=True, exist_ok=True)
                        raw_b64 = "".join(data["image/png"]) if isinstance(data["image/png"], list) else data["image/png"]
                        img_file = img_out_dir / f"cell_{idx}_{o_idx}.png"
                        img_file.write_bytes(base64.b64decode(raw_b64))
                        img_mds.append(f"![Notebook output cell {idx}](/images/notebooks/{slug}/cell_{idx}_{o_idx}.png)")
                    elif "text/plain" in data:
                        txt = "".join(data["text/plain"]) if isinstance(data["text/plain"], list) else data["text/plain"]
                        if txt.strip():
                            text_outputs.append(txt.rstrip())

            if text_outputs:
                joined_out = html.escape("\n".join(text_outputs))
                if len(joined_out) > 650 or collapse_output:
                    body_chunks.append(
                        f'<details class="nb-collapse">\n<summary>Show cell output</summary>\n<pre class="nb-output"><code>{joined_out}</code></pre>\n</details>'
                    )
                else:
                    body_chunks.append(f'<pre class="nb-output"><code>{joined_out}</code></pre>')

            for imd in img_mds:
                body_chunks.append(imd)

    legacy_yaml = json.dumps(legacy_paths or [])
    cats_yaml = json.dumps(categories)
    safe_title = json.dumps(title)
    safe_desc = json.dumps(description)

    frontmatter = f"""---
title: {safe_title}
description: {safe_desc}
pubDate: {pub_date}
toc: {str(toc).lower()}
categories: {cats_yaml}
notebookSource: "{nb_path.name}"
legacyPaths: {legacy_yaml}
---
"""
    dest = project_root / "src" / "content" / "blog" / f"{slug}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(frontmatter + "\n" + "\n\n".join(body_chunks) + "\n", encoding="utf-8")
    return dest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--date", default="2026-11-04")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    out = convert_notebook(args.notebook, root, args.slug, args.date)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
