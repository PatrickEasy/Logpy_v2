# Print Utilities Usage Guide

`print_utils` is Logpy's vocabulary for coloured CLI output. Every other module in the package routes its console output through these helpers, so anything you write using them will look consistent with `convert`, `scaffold`, and `printtime`.

## The Helpers

| Helper           | Looks like                     | Use for                                  |
| ---------------- | ------------------------------ | ---------------------------------------- |
| `title(msg)`     | bold, surrounded by blank lines| Section headers                          |
| `msg(msg)`       | plain indented text            | General messages                         |
| `ok(msg)`        | green `✓` + message            | Success                                  |
| `info(msg)`      | blue `→` + message             | Informational / progress                 |
| `err(msg)`       | red `✗` + message, then `sys.exit(1)` | Fatal errors                       |
| `ask(prompt, default="")` | cyan `?` + prompt, returns user input | Interactive questions             |
| `smart_print(message, msg_type=None)` | Dispatches to one of the above | Generic pipe for arbitrary messages |

All of them live in `Logpy.print_utils` and are also re-exported at the top level:

```python
from Logpy import ok, info, err, ask, title, msg, smart_print, C
```

## Quick Examples

```python
from Logpy import title, ok, info, err, ask, smart_print

title("Deployment")
info("Uploading artefacts...")
ok("Upload complete")

name = ask("Project name", "my_project")

smart_print("Build finished", "ok")
smart_print("Nothing to do", "info")

# err() exits the process — use it at the top-level of a CLI when you
# want to abort with status 1.
if not config_valid:
    err("Config is invalid")
```

## The `C` Class — Raw Colour Codes

If you need the raw ANSI codes (e.g. to build a coloured string that will be handed to another function), use `C`:

```python
from Logpy import C

print(f"{C.BOLD}{C.CYAN}  🐍  Python Scaffolder{C.RESET}")
```

Available attributes: `RESET`, `BOLD`, `DIM`, `GREEN`, `BLUE`, `CYAN`, `WHITE`, `RED`.

## `smart_print` Dispatch

`smart_print(message, msg_type=...)` is the one-stop entry point other modules use when they want to conditionally format output. Valid `msg_type` values:

```
"ok"    -> ok(message)
"info"  -> info(message)
"err"   -> err(message)         # exits
"ask"   -> ask(message)         # returns input
"title" -> title(message)
"msg"   -> msg(message)
None    -> plain print(message)
```

An unknown `msg_type` is itself reported as an error (red `✗`).

`printtime()` accepts a `msg_type` argument and forwards it here, so the same vocabulary applies whether you're logging or just printing.

## When to Reach for Which

- **Interactive scripts**: `ask` for prompts, `ok`/`info`/`err` for feedback.
- **Inside another Logpy module**: prefer `smart_print(..., "info")` so the dispatch is consistent and future-proof.
- **Wrapping status output from a long-running process**: combine `info` for progress with `ok` at completion.
- **Short, bold section breaks**: `title`.
- **Fatal failure**: `err` — but only from top-level CLI code, since it exits the process.

## Running the Demo

```bash
python -m Logpy.print_utils
```

The demo prints every helper, demonstrates `smart_print` dispatch, and shows what an `ask` call would look like.

## Cross-Reference

- `printtime()` can route output through these helpers via its `msg_type` argument.
- `convert` uses `ok`, `info`, `err`, `smart_print`, and `title` for its CLI feedback.
- `scaffold` uses `ask`, `ok`, `info`, `err`, `title`, and the `C` colour constants.
