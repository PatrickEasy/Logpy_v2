"""
Convert between file formats without pandoc.

Supported:
    .md   -> .docx
    .csv  -> .json
    .json -> .csv

Usage:
    python convert.py test1.md               # writes test1.docx
    python convert.py data.csv               # writes data.json
    python convert.py data.json              # writes data.csv
    python convert.py data.csv out.json      # explicit output path

Install once:
    pip install markdown python-docx beautifulsoup4
"""

import csv
import json
import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt


# ---------------------------------------------------------------------------
# Markdown -> DOCX
# ---------------------------------------------------------------------------

def _add_runs(paragraph, node):
    """Walk an HTML node and append runs to a docx paragraph, preserving bold/italic/code."""
    for child in node.children:
        if getattr(child, "name", None) is None:
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


def md_to_docx(src: Path, dst: Path) -> None:
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


# ---------------------------------------------------------------------------
# CSV <-> JSON
# ---------------------------------------------------------------------------

def csv_to_json(src: Path, dst: Path) -> None:
    with src.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    with dst.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)


def json_to_csv(src: Path, dst: Path) -> None:
    data = json.loads(src.read_text(encoding="utf-8"))

    # Accept either a list of dicts, or a single dict (wrap it).
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise ValueError(
            "JSON must be a list of flat objects (or a single object). "
            "Nested structures aren't supported — flatten first."
        )

    # Union of keys across all rows, preserving first-seen order.
    fieldnames: list[str] = []
    seen = set()
    for row in data:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with dst.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            # Stringify nested values so csv doesn't choke.
            writer.writerow({
                k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                for k, v in row.items()
            })


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

# Map (input_ext, output_ext) -> converter function.
CONVERTERS = {
    (".md", ".docx"): md_to_docx,
    (".csv", ".json"): csv_to_json,
    (".json", ".csv"): json_to_csv,
}

# If only input is given, pick the default output extension.
DEFAULT_OUTPUT = {
    ".md": ".docx",
    ".csv": ".json",
    ".json": ".csv",
}


def convert(src_path: str, dst_path: str | None = None) -> Path:
    src = Path(src_path)
    if not src.exists():
        raise FileNotFoundError(src)

    src_ext = src.suffix.lower()
    if dst_path:
        dst = Path(dst_path)
    else:
        if src_ext not in DEFAULT_OUTPUT:
            raise ValueError(f"No default output format for {src_ext!r}")
        dst = src.with_suffix(DEFAULT_OUTPUT[src_ext])

    dst_ext = dst.suffix.lower()
    key = (src_ext, dst_ext)
    if key not in CONVERTERS:
        supported = ", ".join(f"{a}->{b}" for a, b in CONVERTERS)
        raise ValueError(f"Unsupported conversion {src_ext}->{dst_ext}. Supported: {supported}")

    CONVERTERS[key](src, dst)
    return dst


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <input> [output]")
        print("Supported: .md -> .docx, .csv -> .json, .json -> .csv")
        sys.exit(1)
    filename = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    out = convert(filename, output)
    print(f"Wrote {out}")