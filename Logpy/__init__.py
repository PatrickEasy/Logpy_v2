"""
Logpy - A small Python utilities library for scripts and tools.

What started as a timestamped-logger (``printtime``) and a small timer
helper (``Timer``) has grown into a general-purpose toolbox for the
kinds of things scripts end up needing:

* **Timestamped logging** with a JSON log file per session and automatic
  session-elapsed tracking (``printtime``, ``log_message``,
  ``get_session_elapsed``, ``reset_session_timer``).
* **Flexible timing** with decorator, context-manager and manual
  interfaces (``Timer``, ``timed``).
* **Coloured console helpers** for readable CLI output
  (``smart_print``, ``ok``, ``info``, ``err``, ``ask``, ``title``,
  ``msg``, and the ``C`` colour constants).
* **File format conversion** between markdown/docx and csv/json, plus
  matching test-file generators (``convert``, ``batch_convert``,
  ``md_to_docx``, ``csv_to_json``, ``json_to_csv``, ``generate_md``,
  ``generate_docx``, ``generate_csv``, ``generate_json``, ``generate``).
* **File discovery + cleanup** (``find_files_with_extension``,
  ``delete_log_files``).
* **Project scaffolding** for spinning up a fresh Python project with a
  .venv and git repo (``scaffold_project``).

Example usage::

    from Logpy import printtime, Timer, timed, convert, ok, info

    printtime("Application started")          # logs: elapsed 0s
    with Timer("build_report"):
        out = convert("data.csv")             # data.csv -> data.json
    ok(f"Wrote {out}")

    @timed("process_data")
    def process_data(items):
        return len(items)
"""

from .print_utils import (
    C,
    title,
    msg,
    ok,
    info,
    err,
    ask,
    smart_print,
)

from .printtime import (
    printtime,
    log_message,
    delete_log_files,
    find_files_with_extension,
    get_session_elapsed,
    reset_session_timer,
)

from .timer import (
    Timer,
    timed,
)

from .convert import (
    convert,
    batch_convert,
    cli as convert_cli,
    md_to_docx,
    csv_to_json,
    json_to_csv,
    generate,
    generate_md,
    generate_docx,
    generate_csv,
    generate_json,
    CONVERTERS,
    DEFAULT_OUTPUT,
    GENERATORS,
    TFILES_DIR,
)

# ``scaffold.main`` is re-exported under a more descriptive name so that
# ``from Logpy import scaffold_project`` reads naturally.
from .scaffold import main as scaffold_project

__version__ = "2.2.0"
__author__ = "Patrick Easy"

__all__ = [
    # print_utils
    "C",
    "title",
    "msg",
    "ok",
    "info",
    "err",
    "ask",
    "smart_print",
    # printtime
    "printtime",
    "log_message",
    "delete_log_files",
    "find_files_with_extension",
    "get_session_elapsed",
    "reset_session_timer",
    # timer
    "Timer",
    "timed",
    # convert
    "convert",
    "batch_convert",
    "convert_cli",
    "md_to_docx",
    "csv_to_json",
    "json_to_csv",
    "generate",
    "generate_md",
    "generate_docx",
    "generate_csv",
    "generate_json",
    "CONVERTERS",
    "DEFAULT_OUTPUT",
    "GENERATORS",
    "TFILES_DIR",
    # scaffold
    "scaffold_project",
]
