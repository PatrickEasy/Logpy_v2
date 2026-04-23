# Convert Usage Guide

The `convert` module converts between a small set of file formats without relying on pandoc, and ships matching generators for producing test-fixture files. Every conversion is timed with `Timer` and recorded through `printtime`, so running a conversion also produces a structured JSON log in `logs/`.

## Supported Conversions

| From    | To       | Function        |
| ------- | -------- | --------------- |
| `.md`   | `.docx`  | `md_to_docx`    |
| `.csv`  | `.json`  | `csv_to_json`   |
| `.json` | `.csv`   | `json_to_csv`   |

Default output extensions are defined in `DEFAULT_OUTPUT`, so calling `convert("notes.md")` writes `notes.docx` automatically.

## Dependencies

`convert` is the only Logpy module with third-party dependencies:

```bash
pip install markdown python-docx beautifulsoup4
```

These are declared in `pyproject.toml` and `requirements.txt`, so `pip install -r requirements.txt` (or `pip install -e .`) covers them.

## Quick Examples

### Convert a Single File

```python
from Logpy import convert

out = convert("notes.md")              # writes notes.docx
out = convert("data.csv")              # writes data.json
out = convert("data.json", "out.csv")  # explicit destination
```

### Batch Convert a Directory

```python
from Logpy import batch_convert

outputs = batch_convert("docs", ".md")                # recursive by default
outputs = batch_convert("data", ".csv", recursive=False)
```

`batch_convert` uses `find_files_with_extension` under the hood, so it honours the same recursive/non-recursive semantics as the rest of Logpy.

### Generate Test Fixtures

```python
from Logpy import generate, generate_md, generate_csv

generate("sample.md")      # -> tfiles/sample.md
generate("sample.docx")    # -> tfiles/sample.docx
generate("sample.csv")     # -> tfiles/sample.csv
generate("sample.json")    # -> tfiles/sample.json

# Format-specific helpers accept explicit paths and keyword args.
generate_md("my.md", sections=6)
generate_csv("big.csv", rows=1000, cols=10)
```

All generated fixtures land in the `tfiles/` folder (created if missing).

## CLI Usage

```bash
# Run as a module (when the package is installed):
python -m Logpy.convert <input> [output]
python -m Logpy.convert --gen <path>
python -m Logpy.convert --batch <dir> <ext>

# Or using the installed entry point:
logpy-convert notes.md
logpy-convert --gen sample.csv
logpy-convert --batch ./docs .md
```

Without arguments, `logpy-convert` prints usage and exits with status 1. Any `FileNotFoundError` or `ValueError` is routed through `err()`, so failures print a red `✗` line and exit with status 1.

## API Reference

### Single-file conversion

**`convert(src_path, dst_path=None) -> Path`**

Convert one file. Infers the destination extension from `DEFAULT_OUTPUT` when `dst_path` is omitted. Raises `FileNotFoundError` if the source is missing, or `ValueError` for unsupported conversions.

**`md_to_docx(src, dst)`** — markdown → Word. Handles headings, paragraphs, `ul`/`ol` lists, fenced code, blockquotes, horizontal rules, and tables.

**`csv_to_json(src, dst)`** — reads with `utf-8-sig` to handle BOM'd CSVs; writes a list of dictionaries.

**`json_to_csv(src, dst)`** — accepts a list of flat objects or a single object. Nested dict/list values are JSON-stringified on output rather than flattened.

### Batch conversion

**`batch_convert(directory, extension, recursive=True) -> list[Path]`**

Convert every matching file under `directory`. Reports per-file success via `ok()`, failures via `smart_print(..., "info")`, and a summary line via `printtime`.

### Generators

**`generate(path) -> Path`**

Dispatch on extension. Writes to `tfiles/<filename>` (only the basename is honoured).

**`generate_md(dst, sections=4)`** — exercises every element `md_to_docx` handles (headings, paragraphs, bullet + numbered lists with inline formatting, blockquotes, code blocks, tables).

**`generate_docx(dst, sections=4)`** — direct python-docx output, useful for round-trip testing.

**`generate_csv(dst, rows=20, cols=5)`** — random header row and mixed word/number cells.

**`generate_json(dst, rows=20, cols=5)`** — list of flat objects; every 5th row sneaks in a nested value so `json_to_csv`'s stringify-fallback is exercised.

### Constants

**`CONVERTERS`** — `{(src_ext, dst_ext): fn}` lookup for the dispatcher.

**`DEFAULT_OUTPUT`** — `{src_ext: dst_ext}` used when the caller omits `dst_path`.

**`GENERATORS`** — `{ext: fn}` used by `generate`.

**`TFILES_DIR`** — `Path("tfiles")`, the fixture output folder.

## Integration with the Rest of Logpy

- Every call to `convert()`, `batch_convert()`, and `generate()` is wrapped in a named `Timer`, so the session log ends up with entries like `Timer 'convert[.md->.docx]' completed: 142.7ms`.
- `batch_convert` uses `find_files_with_extension` for input discovery.
- CLI feedback uses `ok`, `info`, and `err` from `print_utils`, so successes show a green `✓` and errors show a red `✗` and exit.
- Every successful conversion produces a `printtime` entry with the source and destination paths, so `logs/log_*.json` records exactly what was written and when.

## Troubleshooting

**`ModuleNotFoundError: No module named 'docx'`** — install the runtime deps: `pip install -r requirements.txt` or `pip install python-docx markdown beautifulsoup4`.

**`ValueError: Unsupported conversion ...`** — check `CONVERTERS` for the supported pairs. Only `.md → .docx` and `.csv ↔ .json` are wired up.

**`ValueError: JSON must be a list of flat objects ...`** — `json_to_csv` requires either a list of dicts or a single dict. Nested-by-default JSON has to be flattened first.

**Tables look wrong in the output .docx** — `md_to_docx` reads with `fenced_code` + `tables` extensions. Make sure your markdown table has a delimiter row (`| --- | --- |`).
