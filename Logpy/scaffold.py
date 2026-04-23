#!/usr/bin/env python3
"""
Simple Python project scaffolder.

Usage:
    python scaffold.py
    This will prompt you for a project name, description, and where to create it. It will then create a directory with that name, containing:
    - main.py: a simple Python script with a main() function
    - README.md: a markdown file with the project name and description
    - .gitignore: a basic gitignore file for Python projects
    It will also create a virtual environment in .venv and initialise a git repository with an initial commit.
"""

import sys
import subprocess
from pathlib import Path


# ── Colours ──────────────────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    GREEN  = "\033[92m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    RED    = "\033[91m"

def ok(msg):   print(f"  {C.GREEN}✓{C.RESET}  {msg}")

def info(msg): print(f"  {C.BLUE}→{C.RESET}  {msg}")

def err(msg):  print(f"  {C.RED}✗{C.RESET}  {msg}"); sys.exit(1)

def ask(prompt, default=""):
    hint = f" [{C.DIM}{default}{C.RESET}]" if default else ""
    return input(f"  {C.CYAN}?{C.RESET}  {prompt}{hint}: ").strip() or default


# ── File contents ─────────────────────────────────────────────────────────────
GITIGNORE = """.venv/
__pycache__/
*.pyc
.env
.DS_Store
"""

def make_main(name):
    return f'"""{name}"""\n\n\ndef main():\n    print("Hello from {name}!")\n\n\nif __name__ == "__main__":\n    main()\n'

def make_readme(name, description):
    return f"""# {name}

{description}

## Setup

```bash
source .venv/bin/activate
python main.py
```
"""


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"\n\033[96m\033[1m  🐍  Python Scaffolder\033[0m\n")

    name        = ask("Project name", "my_project")
    description = ask("Description",  "A Python project")
    parent      = Path(ask("Where to create it", "~/documents/github")).expanduser()

    root = parent / name
    if root.exists():
        err(f"Directory already exists: {root}")

    # Create files
    root.mkdir(parents=True)
    (root / "main.py").write_text(make_main(name))
    (root / "README.md").write_text(make_readme(name, description))
    (root / ".gitignore").write_text(GITIGNORE)
    ok("Files created  (main.py, README.md, .gitignore)")

    # Create .venv
    info("Creating .venv ...")
    subprocess.run("python3 -m venv .venv", shell=True, cwd=root)
    ok(".venv ready")

    # Git init
    subprocess.run("git init -b main", shell=True, cwd=root, capture_output=True)
    subprocess.run("git add .", shell=True, cwd=root, capture_output=True)
    subprocess.run('git commit -m "initial commit"', shell=True, cwd=root, capture_output=True)
    ok("Git initialised")

    print(f"\n  \033[97mDone! Get started:\033[0m\n\n    cd {root}\n    source .venv/bin/activate\n    python main.py\n")

    print(f"""
  \033[97m\033[1mDone! Useful commands:\033[0m
 
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