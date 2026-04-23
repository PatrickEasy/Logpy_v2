# Using Logpy in Other Projects

This guide explains how to use the Logpy package in your other Python projects.

## Setup for Private GitHub Repository

### Step 1: Add to requirements.txt

In your other project, add one of these lines to your `requirements.txt`:

**Option 1: Using SSH (Recommended for private repos)**
```
git+ssh://git@github.com/PatrickEasy/Logpy_v2.git
```

**Option 2: Using HTTPS**
```
git+https://github.com/PatrickEasy/Logpy_v2.git
```

**Option 3: Using a specific version/tag**
```
git+ssh://git@github.com/PatrickEasy/Logpy_v2.git@v2.2.0
```

**Option 4: Using a specific branch**
```
git+ssh://git@github.com/PatrickEasy/Logpy_v2.git@main
```

**Option 5: Using a specific commit**
```
git+ssh://git@github.com/PatrickEasy/Logpy_v2.git@abc123def456
```

Installing the package also installs the three runtime dependencies (`markdown`, `python-docx`, `beautifulsoup4`) that the `convert` module needs. If you don't use `convert`, they're still installed but never imported at runtime.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Use in Your Code

```python
from Logpy import (
    # Logging
    printtime, log_message, get_session_elapsed, reset_session_timer,
    find_files_with_extension, delete_log_files,
    # Timing
    Timer, timed,
    # Coloured CLI output
    smart_print, ok, info, err, ask, title, msg, C,
    # File-format conversion + fixture generators
    convert, batch_convert, md_to_docx, csv_to_json, json_to_csv,
    generate, generate_md, generate_docx, generate_csv, generate_json,
    # Project scaffolder
    scaffold_project,
)

printtime("Your application is running!")
```

### Step 4 (optional): Use the installed CLI entry points

Installing the package also puts two scripts on your `PATH`:

```bash
logpy-convert data.csv              # data.csv -> data.json
logpy-convert --batch ./docs .md    # batch-convert every .md under ./docs
logpy-scaffold                      # interactive project scaffolder
```

## Authentication for Private Repositories

### Using SSH (Recommended)

1. Make sure you have SSH keys set up with GitHub.
2. Test your connection: `ssh -T git@github.com`
3. Use the SSH URL format in requirements.txt.

### Using HTTPS with Personal Access Token

If you need to use HTTPS (e.g., in CI/CD):

1. Create a Personal Access Token in GitHub:
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` scope

2. Use the token in requirements.txt:
   ```
   git+https://<YOUR_TOKEN>@github.com/PatrickEasy/Logpy_v2.git
   ```

3. **Security Note**: Never commit tokens to git! Use environment variables:
   ```
   git+https://${GITHUB_TOKEN}@github.com/PatrickEasy/Logpy_v2.git
   ```

### Using Git Credential Helper

Configure git to remember credentials:
```bash
git config --global credential.helper cache
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Install dependencies
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    pip install -r requirements.txt
```

### Docker Example

```dockerfile
FROM python:3.11-slim

# Add SSH key for private repo access
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

# Install dependencies
COPY requirements.txt .
RUN --mount=type=ssh pip install -r requirements.txt
```

## Updating the Package

To update Logpy to the latest version:

```bash
pip install --upgrade --force-reinstall git+ssh://git@github.com/PatrickEasy/Logpy_v2.git
```

## Development Setup

For local development where you want to make changes to Logpy:

```bash
# Clone both repositories
git clone https://github.com/PatrickEasy/Logpy_v2.git
git clone https://github.com/YourUsername/your-other-project.git

# Install Logpy in editable mode
cd Logpy_v2
pip install -e .

# Now changes to Logpy will be reflected immediately in your other project
cd ../your-other-project
python your_script.py
```

## Running the Module Demos

Every Logpy module ships a `__main__` demo you can run straight from the installed package:

```bash
python -m Logpy.printtime       # logging + elapsed-time demo
python -m Logpy.timer           # Timer demo
python -m Logpy.print_utils     # coloured-output demo
python -m Logpy.convert         # CLI usage
python -m Logpy.scaffold        # interactive scaffolder
```

## Troubleshooting

### "Could not find a version that satisfies the requirement"
- Verify your GitHub authentication is working
- Check that the repository URL is correct

### "Permission denied (publickey)"
- Set up SSH keys with GitHub
- Or use HTTPS with a personal access token

### "fatal: could not read Username for 'https://github.com'"
- Use SSH instead of HTTPS
- Or provide authentication credentials

### Package not found after installation
- Make sure you're importing from `Logpy` (capital L)
- Verify installation: `pip show logpy`

### ImportError for `markdown`, `docx`, or `bs4`
- These are required by the `convert` module. Re-run `pip install -r requirements.txt`, or install them directly: `pip install markdown python-docx beautifulsoup4`.

## Example Project Structure

```
your-project/
├── requirements.txt        # Contains git+ssh://git@github.com/PatrickEasy/Logpy_v2.git
├── main.py
├── tfiles/                 # Created automatically by convert generators
│   └── sample.md
└── logs/                   # Created automatically by Logpy
    └── log_20231210_143045.json
```

## Complete Example

**requirements.txt:**
```
git+ssh://git@github.com/PatrickEasy/Logpy_v2.git
requests==2.31.0
```

**main.py:**
```python
from Logpy import (
    printtime, Timer, timed, convert,
    ok, info, err, delete_log_files,
)
import requests

@timed("fetch_github_status")
def fetch_github_status():
    return requests.get("https://api.github.com")

def main():
    printtime("Starting application...")
    info("Checking GitHub status")

    response = fetch_github_status()
    printtime(f"API Status: {response.status_code}")

    # Convert a local CSV to JSON — timed and logged automatically.
    with Timer("write_report"):
        convert("data.csv")

    ok("Done")

    # Clean up old logs.
    deleted = delete_log_files("logs")
    printtime(f"Cleaned up {deleted} old log files")

if __name__ == "__main__":
    main()
```

**Run it:**
```bash
pip install -r requirements.txt
python main.py
```
