# Scaffold Usage Guide

`scaffold` spins up a fresh Python project with a minimal set of files, a virtual environment, and an initialised git repo. Every step is wrapped in a `Timer` and logged through `printtime`, so each scaffold run produces a JSON log describing what happened and how long each step took.

## What It Creates

```
<name>/
├── main.py        # Simple module with a main() function
├── README.md      # Project name + description + setup instructions
├── .gitignore     # Minimal Python .gitignore
└── .venv/         # Virtual environment (python3 -m venv)
```

It also runs `git init -b main`, stages the new files, and creates an initial commit.

## Running It

```bash
# As an installed entry point (after pip install -e . or a git+ install):
logpy-scaffold

# As a module:
python -m Logpy.scaffold

# From the Logpy/ folder:
python scaffold.py
```

You'll be prompted for three values:

| Prompt            | Default                 |
| ----------------- | ----------------------- |
| Project name      | `my_project`            |
| Description       | `A Python project`      |
| Where to create it| `~/documents/github`    |

Pressing enter accepts the default.

## Using It From Python

```python
from Logpy import scaffold_project

scaffold_project()   # same interactive flow as the CLI
```

`scaffold_project` is re-exported from the top level of the package; internally it's `Logpy.scaffold.main`.

## What Gets Logged

Running the scaffolder produces log entries along the way:

```json
[
    { "time": "...", "message": "Scaffold session started",              "elapsed": 0.0,  "elapsed_formatted": "0ms"    },
    { "time": "...", "message": "name:",                                  "elapsed": 2.10, "elapsed_formatted": "2.10s"  },
    { "time": "...", "message": "    my_project",                         "elapsed": 2.11, "elapsed_formatted": "2.11s"  },
    { "time": "...", "message": "description:",                          "elapsed": 2.11, "elapsed_formatted": "2.11s"  },
    { "time": "...", "message": "    A Python project",                   "elapsed": 2.12, "elapsed_formatted": "2.12s"  },
    { "time": "...", "message": "Created project files in /path/to/my_project", "elapsed": 2.13, "elapsed_formatted": "2.13s"  },
    { "time": "...", "message": "Timer 'scaffold.write_files' completed: 12.4ms", "elapsed": 2.14, "elapsed_formatted": "2.14s"  },
    { "time": "...", "message": "Virtual environment created at /path/to/my_project/.venv", "elapsed": 4.90, "elapsed_formatted": "4.90s" },
    { "time": "...", "message": "Timer 'scaffold.create_venv' completed: 2.76s", "elapsed": 4.91, "elapsed_formatted": "4.91s" },
    { "time": "...", "message": "Git repository initialised in /path/to/my_project", "elapsed": 5.00, "elapsed_formatted": "5.00s" },
    { "time": "...", "message": "Scaffold completed in 5.01s",            "elapsed": 5.01, "elapsed_formatted": "5.01s"  }
]
```

Named timers like `scaffold.write_files`, `scaffold.create_venv`, and `scaffold.git_init` let you break down exactly where the scaffold spent its time.

## Customising

The generators are small and intentionally simple. If you want to change what gets written, edit these three in `Logpy/scaffold.py`:

- `make_main(name)` — contents of `main.py`
- `make_readme(name, description)` — contents of `README.md`
- `GITIGNORE` — a plain string constant for `.gitignore`

If you want to skip the `.venv` or git-init steps, the relevant helpers (`_create_venv`, `_git_init`) are clearly separated at the top of the module — call `_write_project_files` on its own if that's all you need.

## Safety

If the target directory already exists, the scaffolder aborts via `err()`. Nothing is ever overwritten.

## Troubleshooting

**"Directory already exists"** — pick a different name or parent folder, or delete the existing directory first.

**venv creation is slow** — that's Python's own `python3 -m venv` doing its thing. The `scaffold.create_venv` timer in the log confirms this is where the time is going.

**Nothing in `logs/`** — the log file is written to the current working directory's `logs/` folder, not the scaffolded project's. Check where you ran the command from.
