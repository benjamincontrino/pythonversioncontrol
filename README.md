# pyenvdemo

A tutorial Python package demonstrating how VS Code projects, virtual environments, Poetry, and `.env` files work together — with demo functions showing the pattern used for connecting to cloud databases.

---

## Python vs R — Concept Mapping

| R Concept | Python / VS Code Equivalent |
|---|---|
| `.Rproj` | `.code-workspace` (VS Code workspace file) |
| `renv` | `venv` (built-in) or **Poetry** (recommended) |
| `renv.lock` | `poetry.lock` |
| `renv::init()` | `poetry new` / `poetry init` |
| `renv::snapshot()` | `poetry add` / `poetry lock` |
| `renv::restore()` | `poetry install` |
| `DESCRIPTION` | `pyproject.toml` |
| `NAMESPACE` + `roxygen2` | `__init__.py` + docstrings |
| `devtools::document()` | `sphinx-apidoc` (generates docs from docstrings) |
| `devtools::install_github()` | `pip install git+https://github.com/...` |
| `.env` + `dotenv` package | `.env` + `python-dotenv` package (identical pattern) |

---

## Concepts Covered

### 1. VS Code Workspace (`.code-workspace`)

A `.code-workspace` file is the VS Code equivalent of an `.Rproj` file. It sets the **root folder**, stores editor settings (formatter, linter, test runner), and lists recommended extensions for the project. Open it with **File → Open Workspace from File** to activate all settings automatically.

```json
{
  "folders": [{ "path": "." }],
  "settings": {
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
  }
}
```

### 2. Poetry — Virtual Environments + Package Management

Poetry is the Python equivalent of `renv` + `devtools` combined. It:
- Creates an **isolated virtual environment** (`.venv/`) per project so packages don't conflict across projects
- Manages a **lockfile** (`poetry.lock`) recording exact package versions
- Handles **building and publishing** your package (like `devtools::build()`)

> **Key mental model:** Poetry manages *which packages are available* → `import` loads them *into your script*. Always set up Poetry before writing `import` statements in a new project.

#### Core Poetry Commands

**`poetry new pyenvdemo`** — scaffold a new project (run once)
```bash
poetry new pyenvdemo
cd pyenvdemo
```
Creates the folder structure, `pyproject.toml`, and initial `src/` layout. Equivalent to `usethis::create_package()` in R.

**`poetry install`** — install all dependencies from `poetry.lock` (equivalent to `renv::restore()`)
```bash
poetry install
```
- Run this when you **clone a repo** or onboard to a teammate's project
- Reads `poetry.lock` and installs the exact versions recorded
- Creates `.venv/` if it doesn't exist

**`poetry add`** — add a new package (equivalent to `install.packages()` + `renv::snapshot()`)
```bash
poetry add python-dotenv          # add a runtime dependency
poetry add --group dev pytest     # add a dev-only dependency
```
Installs the package AND immediately updates `pyproject.toml` and `poetry.lock`. No separate snapshot step needed.

**`poetry lock`** — regenerate the lockfile without installing (equivalent to `renv::snapshot()`)
```bash
poetry lock
```
Use this after manually editing `pyproject.toml`.

**`poetry show --outdated`** — check for outdated packages (equivalent to `renv::status()`)
```bash
poetry show --outdated
```

**`poetry update`** — upgrade packages (equivalent to `renv::update()`)
```bash
poetry update python-dotenv   # update one package
poetry update                 # update everything
```
Always commits the updated `poetry.lock` to Git afterward.

**`poetry run`** — run a command inside the virtual environment
```bash
poetry run python my_script.py
poetry run pytest
```

**`poetry shell`** — activate the virtual environment in your terminal
```bash
poetry shell
# now you can run: python my_script.py, pytest, etc. directly
```

#### Full Poetry Lifecycle

```
New project                         Teammate clones your repo
───────────                         ─────────────────────────
poetry new pyenvdemo                poetry install
  ↓                                   ↓
poetry add python-dotenv            import pyenvdemo
poetry add --group dev pytest       # exact same versions guaranteed
  ↓
git push poetry.lock
```

#### What Gets Committed to GitHub

```
✅ commit:    poetry.lock        ← the version recipe
✅ commit:    pyproject.toml     ← package metadata + dependency declarations
❌ gitignore: .venv/             ← actual installed files (too large, teammates rebuild)
```

### 3. `pyproject.toml` — Package Manifest

`pyproject.toml` is the Python equivalent of R's `DESCRIPTION` file. It declares package metadata, dependencies, and build settings in one place.

```toml
[tool.poetry]
name = "pyenvdemo"
version = "0.1.0"
description = "My package"
authors = ["Benjamin Contrino <benjamin.contrino@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.11"
python-dotenv = "^1.0.0"
```

Bump the `version` field whenever you make changes so consumers know something changed.

### 4. `__init__.py` — Package Exports

`__init__.py` is the Python equivalent of R's `NAMESPACE` file. It marks a directory as a Python package and controls what is publicly available when someone imports it.

```python
# src/pyenvdemo/__init__.py
from .env_utils import get_env_var, list_env_connections

__all__ = ["get_env_var", "list_env_connections"]
```

Without `__init__.py`, the folder is just a folder. With it, Python treats it as an importable package.

### 5. Docstrings — Inline Documentation

Python uses **docstrings** instead of `roxygen2` comments. They live inside the function body and are accessible via `help()` at runtime.

```python
def get_env_var(key: str, default=None):
    """
    Retrieve an environment variable safely.

    Parameters
    ----------
    key : str
        The name of the variable to retrieve (e.g. "DB_SERVER").
    default : str, optional
        Fallback value if the variable is not set.

    Returns
    -------
    str or None
    """
```

To auto-generate HTML docs from docstrings (like `devtools::document()` generates `.Rd` files):
```bash
pip install sphinx
sphinx-apidoc -o docs/source src/pyenvdemo
sphinx-build docs/source docs/_build
```

### 6. `.env` Files — Credential Management

Identical pattern to R. A `.env` file stores secrets that must never be committed to GitHub.

```bash
# .env (never commit this)
DB_SERVER=my-server.database.windows.net
DB_PASSWORD=supersecret
```

In Python, load and access with `python-dotenv`:

```python
from dotenv import load_dotenv
from pyenvdemo import get_env_var

load_dotenv(".env")               # load once at the top of your script
server = get_env_var("DB_SERVER") # access anywhere after
```

Always commit `.env.example` (keys only, no values) so teammates know what to fill in.

### 7. Using This Package in Another Project

To use `pyenvdemo` in a different project, install it there — it is not a live link. If the original package changes, you must reinstall to get the updates.

**Install from GitHub:**
```bash
pip install git+https://github.com/benjamincontrino/pyenvdemo.git

# Or with Poetry in the consuming project:
poetry add git+https://github.com/benjamincontrino/pyenvdemo.git
```

**Install from a local path:**
```bash
pip install -e /path/to/pyenvdemo    # -e = editable mode (live link, dev only)
poetry add --editable /path/to/pyenvdemo
```

> **Editable mode (`-e`)** is a Python-only concept with no R equivalent. It symlinks the package into your environment so local changes are reflected immediately — useful during active development of both packages at once. Remove `-e` for production.

**When the original package changes:**
```bash
# In the original package — after making changes:
# bump version in pyproject.toml (e.g. 0.1.0 → 0.2.0), then:
git push

# In the consuming project — to pull the new version:
pip install --upgrade git+https://github.com/benjamincontrino/pyenvdemo.git
# or with Poetry:
poetry update pyenvdemo
poetry lock    # update the lockfile
```

---

## Cloud Platforms Covered

| Platform | Variables | Python Library | Use Case |
|----------|-----------|----------------|----------|
| SQL Server | `DB_*` | `pyodbc` + `sqlalchemy` | Relational queries |
| Azure Blob Storage | `AZURE_*` | `azure-storage-blob` | File storage (CSV, Parquet) |
| Microsoft Fabric | `FABRIC_*` | `pyodbc` + `sqlalchemy` | Lakehouse / warehouse |
| Databricks | `DATABRICKS_*` | `databricks-sql-connector` | Spark + Delta Lake |
| Snowflake | `SNOWFLAKE_*` | `snowflake-sqlalchemy` | Cloud data warehouse |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/benjamincontrino/pyenvdemo.git
cd pyenvdemo

# 2. Copy .env.example and fill in your credentials
cp .env.example .env

# 3. Install dependencies (recreates the exact environment)
poetry install

# 4. Open in VS Code
code pyenvdemo.code-workspace

# 5. Run the demo
poetry run python -c "
from dotenv import load_dotenv
from pyenvdemo import get_env_var, list_env_connections
load_dotenv('.env')
for row in list_env_connections():
    print(row)
"

# 6. Run tests
poetry run pytest
```

---

## Example Connection Patterns

### SQL Server
```python
import pyodbc
from dotenv import load_dotenv
from pyenvdemo import get_env_var

load_dotenv(".env")

conn = pyodbc.connect(
    f"DRIVER={{{get_env_var('DB_DRIVER')}}};"
    f"SERVER={get_env_var('DB_SERVER')};"
    f"DATABASE={get_env_var('DB_NAME')};"
    f"UID={get_env_var('DB_USER')};"
    f"PWD={get_env_var('DB_PASSWORD')};"
    f"PORT={get_env_var('DB_PORT', default='1433')};"
)
```

### Azure Blob Storage
```python
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from pyenvdemo import get_env_var

load_dotenv(".env")

client = BlobServiceClient(
    account_url=f"https://{get_env_var('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net",
    credential=get_env_var("AZURE_STORAGE_KEY")
)
container = client.get_container_client(get_env_var("AZURE_CONTAINER"))
```

### Databricks
```python
from databricks import sql
from dotenv import load_dotenv
from pyenvdemo import get_env_var

load_dotenv(".env")

conn = sql.connect(
    server_hostname=get_env_var("DATABRICKS_HOST"),
    http_path=get_env_var("DATABRICKS_HTTP_PATH"),
    access_token=get_env_var("DATABRICKS_TOKEN")
)
```

### Snowflake
```python
import snowflake.connector
from dotenv import load_dotenv
from pyenvdemo import get_env_var

load_dotenv(".env")

conn = snowflake.connector.connect(
    account=get_env_var("SNOWFLAKE_ACCOUNT"),
    user=get_env_var("SNOWFLAKE_USER"),
    password=get_env_var("SNOWFLAKE_PASSWORD"),
    warehouse=get_env_var("SNOWFLAKE_WAREHOUSE"),
    database=get_env_var("SNOWFLAKE_DATABASE"),
    schema=get_env_var("SNOWFLAKE_SCHEMA"),
    role=get_env_var("SNOWFLAKE_ROLE")
)
```

---

## Package Development Workflow

```bash
# After editing src/pyenvdemo/ files:

# Run tests
poetry run pytest

# Build a distributable package (like devtools::build())
poetry build        # creates dist/pyenvdemo-0.1.0.tar.gz

# Publish to PyPI (like submitting to CRAN)
poetry publish

# Push to GitHub
git add .
git commit -m "your message"
git push
```

---

## Project Structure

```
pyenvdemo/
├── src/
│   └── pyenvdemo/
│       ├── __init__.py       ← exports (like R's NAMESPACE)
│       └── env_utils.py      ← functions with docstrings
├── tests/
│   └── test_env_utils.py     ← pytest tests
├── .env                      ← credentials (never commit)
├── .env.example              ← keys only (safe to commit)
├── .gitignore
├── pyproject.toml            ← package manifest (like DESCRIPTION)
├── poetry.lock               ← exact version lockfile (like renv.lock)
├── pyenvdemo.code-workspace  ← VS Code settings (like .Rproj)
└── README.md
```

---

## Author
Benjamin Contrino — benjamin.contrino@gmail.com
