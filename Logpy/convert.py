"""
Convert a Markdown file to .docx without pandoc.

Usage:
    python convert.py test1.md            # writes test1.docx next to it
    python convert.py test1.md out.docx   # explicit output path

Install once:
    pip install markdown python-docx beautifulsoup4
"""

import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt


def _add_runs(paragraph, node):
    """Walk an HTML node and append runs to a docx paragraph, preserving bold/italic/code."""
    for child in node.children:
        if getattr(child, "name", None) is None:
            # plain text node
            paragraph.add_run(str(child))
        elif child.name in ("strong", "b"):
            run = paragraph.add_run(child.get_text())
            run.bold = True
        elif child.name in ("em", "i"):
            run = paragraph.add_run(child.get_text())
            run.italic = True
        elif child.name == "code":
            run = paragraph.add_run(child.get_text())
            run.font.name = "Consolas"
        elif child.name == "a":
            run = paragraph.add_run(child.get_text())
            run.underline = True
        else:
            _add_runs(paragraph, child)


def convert(md_path: str, docx_path: str | None = None) -> Path:
    src = Path(md_path)
    if not src.exists():
        raise FileNotFoundError(src)
    dst = Path(docx_path) if docx_path else src.with_suffix(".docx")

    html = markdown.markdown(
        src.read_text(encoding="utf-8"),
        extensions=["fenced_code", "tables"],
    )
    soup = BeautifulSoup(html, "html.parser")

    doc = Document()

    for el in soup.children:
        name = getattr(el, "name", None)
        if name is None:
            continue
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            doc.add_heading(el.get_text(), level=int(name[1]))
        elif name == "p":
            p = doc.add_paragraph()
            _add_runs(p, el)
        elif name in ("ul", "ol"):
            style = "List Bullet" if name == "ul" else "List Number"
            for li in el.find_all("li", recursive=False):
                p = doc.add_paragraph(style=style)
                _add_runs(p, li)
        elif name == "pre":
            # fenced code block
            code_text = el.get_text()
            p = doc.add_paragraph()
            run = p.add_run(code_text)
            run.font.name = "Consolas"
            run.font.size = Pt(10)
        elif name == "blockquote":
            p = doc.add_paragraph(style="Intense Quote")
            _add_runs(p, el)
        elif name == "hr":
            doc.add_paragraph("_" * 40)
        elif name == "table":
            rows = el.find_all("tr")
            if not rows:
                continue
            cols = max(len(r.find_all(["td", "th"])) for r in rows)
            table = doc.add_table(rows=len(rows), cols=cols)
            table.style = "Light Grid Accent 1"
            for r_idx, row in enumerate(rows):
                for c_idx, cell in enumerate(row.find_all(["td", "th"])):
                    table.cell(r_idx, c_idx).text = cell.get_text()

    doc.save(dst)
    return dst


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <input.md> [output.docx]")
        sys.exit(1)
    filename = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    out = convert(filename, output)
    print(f"Wrote {out}")