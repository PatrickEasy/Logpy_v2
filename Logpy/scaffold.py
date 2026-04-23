#!/usr/bin/env python3
"""
Simple Python project scaffolder.

Creates a new Python project directory with a main module, a README, a
.gitignore, a virtual environment, and an initialised git repo.

Usage:
    python -m Logpy.scaffold          # when installed as a package
    python scaffold.py                # when run from the Logpy/ folder

Every step is timed with :class:`Logpy.Timer` and logged through
:func:`Logpy.printtime`, so each scaffold run produces a JSON log file in
``logs/`` describing what happened and how long each step took.
"""

import sys
import subprocess
from pathlib import Path

# Import printing utilities from the sibling module.
# Relative import when running as part of the package, absolute fallback
# when executing this file directly as a script.
try:
    from .print_utils import ok, info, err, ask, C, title
    from .printtime import printtime
    from .timer import Timer
except ImportError:
    from print_utils import ok, info, err, ask, C, title
    from printtime import printtime
    from timer import Timer


# ── File contents ─────────────────────────────────────────────────────────────
GITIGNORE = """.venv/
__pycache__/
*.pyc
.env
.DS_Store
"""


def make_main(name):
    """Return the source for the generated ``main.py``."""
    return (
        f'"""{name}"""\n\n\n'
        f'def main():\n'
        f'    print("Hello from {name}!")\n\n\n'
        f'if __name__ == "__main__":\n'
        f'    main()\n'
    )


def make_readme(name, description):
    """Return a minimal README.md body for the new project."""
    return f"""# {name}

{description}

## Setup

```bash
source .venv/bin/activate
python main.py
```
"""


# ── Scaffolding steps ─────────────────────────────────────────────────────────

def _write_project_files(root: Path, name: str, description: str) -> None:
    """Create the initial project files inside ``root``."""
    with Timer("scaffold.write_files"):
        root.mkdir(parents=True)
        (root / "main.py").write_text(make_main(name))
        (root / "README.md").write_text(make_readme(name, description))
        (root / ".gitignore").write_text(GITIGNORE)
    printtime(f"Created project files in {root}")
    ok("Files created  (main.py, README.md, .gitignore)")


def _create_venv(root: Path) -> None:
    """Create a ``.venv`` inside ``root``."""
    info("Creating .venv ...")
    with Timer("scaffold.create_venv"):
        subprocess.run("python3 -m venv .venv", shell=True, cwd=root)
    printtime(f"Virtual environment created at {root / '.venv'}")
    ok(".venv ready")


def _git_init(root: Path) -> None:
    """Initialise a git repo in ``root`` with a single initial commit."""
    with Timer("scaffold.git_init"):
        subprocess.run("git init -b main", shell=True, cwd=root, capture_output=True)
        subprocess.run("git add .", shell=True, cwd=root, capture_output=True)
        subprocess.run(
            'git commit -m "initial commit"',
            shell=True, cwd=root, capture_output=True,
        )
    printtime(f"Git repository initialised in {root}")
    ok("Git initialised")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"\n{C.CYAN}{C.BOLD}  🐍  Python Scaffolder{C.RESET}\n")
    printtime("Scaffold session started")

    # Time the whole run so we can report total time at the end.
    overall = Timer("scaffold.total", auto_log=False).start()

    name        = ask("Project name", "my_project")
    description = ask("Description",  "A Python project")
    parent      = Path(ask("Where to create it", "~/documents/github")).expanduser()

    root = parent / name
    if root.exists():
        printtime(f"Scaffold aborted: {root} already exists")
        err(f"Directory already exists: {root}")

    printtime({
        "name": name,
        "description": description,
        "root": str(root),
    })

    _write_project_files(root, name, description)
    _create_venv(root)
    _git_init(root)

    total = overall.stop()
    printtime(f"Scaffold completed in {Timer._format_time(total)}")

    print(f"\n  {C.WHITE}Done! Get started:{C.RESET}\n\n"
          f"    cd {root}\n"
          f"    source .venv/bin/activate\n"
          f"    python main.py\n")

    print(f"""
  {C.WHITE}{C.BOLD}Done! Useful commands:{C.RESET}

  Navigate to your project:
    cd {root}

  Activate virtual environment:
    source .venv/bin/activate

  Run your project:
    python main.py

  Install a package:
    pip install <package>

  Save dependencies:
    pip freeze > requirements.txt

  Deactivate virtual environment:
    deactivate
""")


if __name__ == "__main__":
    main()
