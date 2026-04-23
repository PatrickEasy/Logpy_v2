# Logpy_v2

A small Python utilities library for scripts and tools. What started as a timestamped logger plus a simple timer has grown into a general-purpose toolbox I reach for whenever I'm writing a script: structured logging, flexible timing, coloured CLI output, file-format conversion, and a project scaffolder.

## Overview

Logpy_v2 ships five small, independent modules that compose nicely together. The logging module timestamps and persists everything to JSON. The timer works as a decorator, context manager, or manual stopwatch. The print-utils module makes CLI output readable. The convert module handles markdown↔docx and csv↔json without pandoc. And the scaffold module spins up a fresh Python project with a .venv and git repo.

## Features

- **Timestamped logging** – every entry carries the wall-clock time and session-elapsed time, persisted as JSON.
- **Flexible timing** – `Timer` can be used as a context manager, decorator, or manual stopwatch, with zero overhead while running.
- **Coloured CLI helpers** – `smart_print`, `ok`, `info`, `err`, `ask`, `title`, `msg` — the same vocabulary across every script.
- **File-format conversion** – `.md → .docx`, `.csv ↔ .json`, plus matching test-file generators.
- **Batch conversion** – point at a directory and convert everything with a given extension in one call.
- **File discovery and log cleanup** – `find_files_with_extension`, `delete_log_files`.
- **Project scaffolder** – `scaffold_project()` creates a new project with `main.py`, `README.md`, `.gitignore`, a `.venv`, and an initial git commit. Every step is timed and logged.
- **Consistent integration** – every module uses the shared print/logging/timing helpers, so output looks the same whichever script you run.

## Installation

### From Private GitHub Repository (Recommended)

Add to your project's `requirements.txt`:

```
# Using SSH (recommended for private repos)
git+ssh://git@github.com/PatrickEasy/Logpy_v2.git

# Or using HTTPS with a personal access token
git+https://github.com/PatrickEasy/Logpy_v2.git
```

Then install:

```bash
pip install -r requirements.txt
```

### From Source

```bash
git clone https://github.com/PatrickEasy/Logpy_v2.git
cd Logpy_v2
pip install -e .
```

Installing the package also gives you two CLI entry points on your `PATH`:

```bash
logpy-convert data.csv               # data.csv -> data.json
logpy-scaffold                       # interactive project scaffolder
```

### Dependencies

- Python 3.9+
- `markdown`, `python-docx`, `beautifulsoup4` — used only by the convert module.

The logging, timing, print-utils, and scaffold modules use only the Python standard library; if you never touch `convert`, the three runtime dependencies never get used at runtime either.

## Quick Start

```python
from Logpy import (
    printtime, Timer, timed, get_session_elapsed,
    ok, info, err, ask, smart_print,
    convert, batch_convert, generate,
    find_files_with_extension, delete_log_files,
)
import time

# Timestamped output — every entry is persisted as JSON with elapsed time.
printtime("Application started")           # elapsed: 0s
time.sleep(1)
printtime("1 second later")                # elapsed: 1.0s

# Time a function with a decorator.
@timed("process_data")
def process_data(items):
    time.sleep(0.5)
    return len(items)

result = process_data([1, 2, 3])           # logs: Timer 'process_data' completed: 500ms

# Time a block of code with a context manager.
with Timer("database_query"):
    time.sleep(0.3)

# Coloured CLI output — same look across every Logpy-powered script.
ok("Build succeeded")
info("Deploying to staging")
name = ask("Project name", "my_project")

# File-format conversion.
out = convert("notes.md")                  # notes.md -> notes.docx
batch_convert("docs", ".md")               # convert every .md under docs/

# Generate a fixture file for testing.
generate("sample.csv")                     # writes tfiles/sample.csv

# File discovery + log cleanup.
py_files = find_files_with_extension("src", ".py")
delete_log_files("logs")

# Total session time.
printtime(f"Session time: {get_session_elapsed():.2f}s")
```

### Log File Output

Each log entry automatically includes elapsed time since the session started:

```json
[
    {
        "time": "2025-12-10 14:30:45",
        "message": "Application started",
        "elapsed": 0.0,
        "elapsed_formatted": "0ms"
    },
    {
        "time": "2025-12-10 14:30:46",
        "message": "Converted notes.md -> notes.docx",
        "elapsed": 1.503,
        "elapsed_formatted": "1.50s"
    }
]
```

## Modules

### `printtime` — Logging

Timestamped console output plus an automatic JSON log file per session. Every entry carries session-elapsed time. Strings, lists, sets, and dicts are all accepted and formatted recursively.

Exports: `printtime`, `log_message`, `get_session_elapsed`, `reset_session_timer`, `find_files_with_extension`, `delete_log_files`.

### `timer` — Timing

A `Timer` class plus a `timed` decorator. Zero overhead while running; check elapsed time any time without stopping the timer; registry for tracking multiple simultaneous timers. See [TIMER.md](TIMER.md) for the full guide.

### `print_utils` — Coloured CLI output

`smart_print(message, msg_type=...)` dispatches to `ok`, `info`, `err`, `ask`, `title`, or `msg`. Colour constants live on the `C` class. See [PRINT_UTILS.md](PRINT_UTILS.md).

### `convert` — File-format conversion

Converts `.md → .docx` and `.csv ↔ .json` without pandoc. Includes a `--batch` mode powered by `find_files_with_extension`, and matching `generate_*` functions to emit test fixtures into `tfiles/`. Every conversion is timed and logged. See [CONVERT.md](CONVERT.md).

### `scaffold` — Project scaffolding

`scaffold_project()` (a.k.a. `python -m Logpy.scaffold` or `logpy-scaffold`) prompts for a name, description, and parent folder, then creates the project directory, initial files, `.venv`, and a git repo with an initial commit. Each step is timed with `Timer` and logged with `printtime`. See [SCAFFOLD.md](SCAFFOLD.md).

## API Reference

### Logging

#### `printtime(message, indent=0, log_to_file=True, include_elapsed=True, msg_type=False)`

Print timestamped messages with automatic session-elapsed tracking. Supports strings, lists, sets, and dicts (recursively). If `msg_type` is set (`"ok"`, `"info"`, `"err"`, `"title"`, `"msg"`), output is routed through the matching `print_utils` helper.

#### `log_message(time, message, folder="logs", elapsed=None)`

Append an entry directly to the session's JSON log file.

#### `get_session_elapsed()` / `reset_session_timer()`

Query or reset the session-elapsed clock (starts when `Logpy` is imported).

#### `find_files_with_extension(directory, extension, recursive=True)`

Return a list of paths matching `extension` in `directory`. Used internally by `delete_log_files` and `batch_convert`.

#### `delete_log_files(directory=None, recursive=False)`

Delete files matching `log_*.json` in `directory` (defaults to the current working directory). Returns the number of files deleted.

### Timing

#### `Timer(name=None, auto_log=True, log_to_file=True)`

Context manager / manual stopwatch / decorator source. Methods: `start()`, `stop()`, `elapsed()`, `is_running()`, `reset()`. Class methods: `Timer.decorator(...)`, `Timer.get/register/unregister/clear_registry`. See [TIMER.md](TIMER.md).

#### `timed(name=None, auto_log=True, log_to_file=True)`

Shorter alias for `Timer.decorator(...)`.

### Coloured output

#### `smart_print(message, msg_type=None)`

Dispatches to the right helper based on `msg_type`. With no `msg_type`, falls back to plain `print`.

#### `ok(msg)` / `info(msg)` / `err(msg)` / `ask(prompt, default="")` / `title(msg)` / `msg(msg)`

Direct helpers. `err` exits the program with status 1. `ask` prompts for input and returns the value (or `default` if the user pressed enter).

#### `C`

Colour constants (`C.GREEN`, `C.RED`, `C.CYAN`, `C.BOLD`, `C.RESET`, ...).

### Conversion

#### `convert(src_path, dst_path=None)`

Convert a single file. If `dst_path` is omitted the output extension is inferred from the input. Supported: `.md → .docx`, `.csv ↔ .json`.

#### `batch_convert(directory, extension, recursive=True)`

Convert every file under `directory` with the given extension. Uses `find_files_with_extension` to discover inputs.

#### `generate(path)`

Write a fixture file to `tfiles/` — type is chosen from the file extension (`.md`, `.docx`, `.csv`, `.json`). Per-format helpers (`generate_md`, `generate_docx`, `generate_csv`, `generate_json`) are also exported.

### Scaffolding

#### `scaffold_project()`

Interactive project scaffolder. Prompts for name, description, and parent folder; creates the directory, initial files, `.venv`, and git repo; logs every step and times the overall run.

## Running the Demos

Every module has a `__main__` block you can run directly:

```bash
python -m Logpy.printtime       # logging + elapsed-time demo
python -m Logpy.timer           # Timer demo
python -m Logpy.print_utils     # coloured-output demo
python -m Logpy.convert         # prints CLI usage; add args to actually convert
python -m Logpy.scaffold        # interactive scaffolder
```

Running any of them also creates a log file in `logs/` so you can inspect the JSON output.

## Project Structure

```
Logpy_v2/
├── README.md              # This file
├── USAGE.md               # Installation guide for downstream projects
├── TIMER.md               # Timer guide
├── CONVERT.md             # Convert module guide
├── SCAFFOLD.md            # Scaffold module guide
├── PRINT_UTILS.md         # Print utils guide
├── requirements.txt       # Runtime dependencies (only needed for convert)
├── pyproject.toml         # Package configuration
├── .gitignore
├── .gitattributes
├── logs/                  # Generated log files (git-ignored)
├── tfiles/                # Generated test files (git-ignored)
└── Logpy/
    ├── __init__.py        # Public API exports
    ├── printtime.py       # Logging and session timing
    ├── timer.py           # Timer class and @timed decorator
    ├── print_utils.py     # Coloured CLI helpers (smart_print, ok, info, err, ...)
    ├── convert.py         # md↔docx, csv↔json, batch conversion, generators
    └── scaffold.py        # Python project scaffolder
```

## Contributing

This is a personal project, but suggestions and improvements are welcome. Feel free to open issues or submit pull requests.

## License

MIT License — use freely in personal projects.

## Changelog

### Version 2.2.0 (Current)
- **New module**: `print_utils` — coloured CLI helpers (`smart_print`, `ok`, `info`, `err`, `ask`, `title`, `msg`, `C`) now exported from the top-level package.
- **New module**: `convert` — `.md → .docx` and `.csv ↔ .json` conversion, with matching `generate_*` test-fixture helpers and a `batch_convert` mode powered by `find_files_with_extension`.
- **New module**: `scaffold` — interactive project scaffolder, exposed as `scaffold_project` and the `logpy-scaffold` CLI entry point. Every step is timed with `Timer` and logged with `printtime`.
- **New CLI entry points**: `logpy-convert` and `logpy-scaffold` installed on the `PATH` when the package is pip-installed.
- **Consistency**: every script now uses the shared `print_utils`, `printtime`, and `Timer` helpers; all intra-package imports are relative with a script-mode fallback.
- **Convert CLI**: added `--batch <dir> <ext>` and a `cli()` function so the entry point works.
- **Packaging**: declared runtime dependencies (`markdown`, `python-docx`, `beautifulsoup4`) in `pyproject.toml` and `requirements.txt`; bumped minimum Python to 3.9.

### Version 2.1.0
- `Timer` class with decorator, context manager, and manual control.
- Automatic session-elapsed tracking for all log entries.
- `get_session_elapsed()` and `reset_session_timer()` helpers.
- Human-readable time formatting (ms, seconds, minutes, hours).
- `printtime()` gained `include_elapsed` parameter; `log_message()` gained `elapsed`.
- Log files gained `elapsed` and `elapsed_formatted` fields.
- File-search utilities with recursive/non-recursive options.
- Improved log cleanup.
- Package became installable via pip from GitHub.

## Author

Patrick Easy

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/PatrickEasy/Logpy_v2/issues).

## Additional Documentation

- [USAGE.md](USAGE.md) — installation guide for downstream projects
- [TIMER.md](TIMER.md) — complete Timer documentation with advanced examples
- [CONVERT.md](CONVERT.md) — convert module guide
- [SCAFFOLD.md](SCAFFOLD.md) — scaffold module guide
- [PRINT_UTILS.md](PRINT_UTILS.md) — coloured-output helpers guide
