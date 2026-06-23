---
trigger: glob
globs: "src/**"
description: Defines the mandatory structure that all MVE projects in the repository must follow.
---

## Standard Structure

Each example should follow this structure:

```
src/[cloud-provider]/[mves|projects]/[example-name]/
├── .devcontainer/
│   ├── devcontainer.json
│   └── postCreateCommand.sh
├── .vscode/
│   └── settings.json
├── scripts/
│   ├── setup.sh
│   ├── run_main.sh
│   ├── run_tests.sh
│   └── [other install tools sh]
├── docker-compose.yml
├── .env
├── main.py
├── [Other Python code files]
├── mise.toml
├── pyproject.toml
├── uv.lock
├── README.md
└── README.es.md
```

## Dev Container

- The `dev` service defined in `docker-compose.yml` must be used as the Dev Container.
- **Do NOT override `PATH` in `containerEnv`.** Setting `PATH` there fully replaces the variable, forcing you to re-list every default path. Instead, append the `mise` shims path from `postCreateCommand.sh` (see below). Use `containerEnv` only for additive variables (e.g., `AWS_PROFILE`).
- The `postCreateCommand` must call `.devcontainer/postCreateCommand.sh` (relative to `workspaceFolder`, which is `/app`). This script runs `scripts/setup.sh` and appends the `mise` shims path to `~/.bashrc` and `~/.zshrc` so every new shell session inside the container has it on `PATH`.
- It must always include the feature `"ghcr.io/devcontainers/features/docker-outside-of-docker:1": {}`.
- It must install mandatory VS Code extensions: **Python**, and any other specific to the MVE services.

```json
{
  "name": "[MVE Name]",
  "dockerComposeFile": [
    "../docker-compose.yml"
  ],
  "service": "dev",
  "workspaceFolder": "/app",
  "features": {
    "ghcr.io/devcontainers/features/docker-outside-of-docker:1": {
      "moby": false
    }
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "tamasfe.even-better-toml"
      ]
    }
  },
  "containerEnv": {
    "AWS_PROFILE": "example"
  },
  "postCreateCommand": ".devcontainer/postCreateCommand.sh"
}
```

### postCreateCommand.sh

Lives in `.devcontainer/`. Runs `setup.sh`, then appends the `mise` shims path to the shell rc files (guarded so it is not duplicated on re-creation). Derive the path from `$HOME` — never hardcode `/home/vscode`, so it survives a different container user.

```bash
#!/bin/bash
set -e

scripts/setup.sh

# Add mise to PATH
MISE_SHIMS="$HOME/.local/share/mise/shims"
EXPORT_LINE="export PATH=\$PATH:$MISE_SHIMS"

for RC in "$HOME/.bashrc" "$HOME/.zshrc"; do
  if [ -f "$RC" ] && ! grep -qF "$MISE_SHIMS" "$RC"; then
    echo "$EXPORT_LINE" >> "$RC"
  fi
done
```

## Docker Compose

### Preferred Structure

```yaml
services:
  service:
    image: official/image
    container_name: name
    ports:
      - "port:port"
    environment:
      - VARIABLE=value
    volumes:
      - name_data:/data
    command: optional command

  dev:
    image: mcr.microsoft.com/devcontainers/python:3.12-bookworm
    container_name: dev
    network_mode: host
    depends_on:
      - service
    volumes:
      - .:/app:cached
    working_dir: /app
    command: sleep infinity

volumes:
  name_data:
```

### Conventions

- **container_name**: Simple and representative name (e.g., `azurite`, `localstack`).
- **volumes**: Name as `[service]_data`.

## Environment Variables

```
# Descriptive group comment
VARIABLE_ONE=value
VARIABLE_TWO=another-value

# Another group
OTHER_VARIABLE=value
```

## VS Code Settings

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python"
}
```

## setup.sh

- It must install **mise** using curl, guarded so it is not reinstalled if already present (idempotent — `setup.sh` may run more than once).
- It must install the tools specified in `mise.toml`.
- It must execute the tasks defined in `mise.toml`.

Example:
```bash
#!/bin/bash
set -e

command -v mise >/dev/null 2>&1 || (curl https://mise.run | sh)
export PATH="$HOME/.local/bin:$PATH"

mise install -y
mise run setup
# ... Other tasks
```

## mise.toml

- It must always install **Python 3.12** and **uv**.
- It must load the `.env` file.
- Every task defined must be eventually referenced in the **setup** task to ensure a complete environment setup in one command.

Example:
```toml
[tools]
python = "3.12"
uv = "latest"

[settings]
env_file = ".env"

[tasks.sync]
description = "Sync python dependencies"
run = "uv sync"

[tasks.setup]
description = "Full environment setup"
run = [
  { task = "sync" },
  { task = "other-task" },
]
```

- If an MVE requires a tool not available in **mise** that needs multiple bash commands, the installation of each tool must be in a separate script at `scripts/install-[tool].sh` and executed as a **mise** task.

Example:
```toml
[tasks.install-odbc]
description = "Install Microsoft ODBC driver for SQL Server"
run = "scripts/install-odbc.sh"
```

## Standardized Scripts Rule

The scripts in `scripts/` MUST be the **Single Source of Truth** for deployment and management. 
- **setup.sh**: Responsible for installing `mise`, installing tools, and running the `setup` task.
- **.devcontainer/postCreateCommand.sh**: Dev Container entry point. Runs `setup.sh` and appends the `mise` shims path to the shell rc files (idempotently).
- **run_main.sh**: Responsible for executing the `main.py` entry point with the correct environment.
- **run_tests.sh**: Responsible for launching all tests for the MVE.
- Scripts should use `.venv/bin/python` for Python-based tasks to avoid PATH issues.
- Scripts should handle clean up (deleting temporary files or state) where applicable.

## pyproject.toml

The chosen method for dependency management is **Python + uv** with `pyproject.toml`.

### Essential Fields
- **name**: Name of the example directory.
- **requires-python**: Should always be `">=3.9"`.
- **dependencies**: List all required libraries. Always include `python-dotenv`.
- **versions**: Do not specify version constraints unless strictly necessary.

### Structure Template
```toml
[project]
name = "example-name"
version = "0.1.0"
description = "Brief example description"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "library1",
    "python-dotenv",
]
```

## Lab READMEs

Each Lab has a `README.md` and `README.es.md` with a one-paragraph overview and a redirect link to the full Starlight doc page:

```markdown
# Title

One-sentence overview of the lab.

> 📖 Full documentation for this lab is available at:
> https://mistlock.dev/[provider]/[mves|projects]/[name]/
```

**Sync rule**: The overview paragraph must match the `description` field of the corresponding Starlight doc page. When updating a doc page's `description`, update the README overviews too. The `description` must stay under ~160 characters (SEO meta description limit); the doc page's intro paragraph in the body may keep a longer, two-sentence version.

**Redirect rule**: Some Labs (e.g., ElastiCache, RDS, Cache for Redis) are wrappers that point users to another lab. For these, the README redirect link must point directly to the destination lab URL — not to the wrapper lab's own doc page. Avoid double redirects (README → wrapper page → destination).

## Docs site checklist

When adding or removing an example, update these files in `docs/`:

- `docs/src/content/docs/[provider]/[mves|projects]/[name].mdx` — English doc page (must include `isLab: true` in frontmatter).
- `docs/src/content/docs/es/[provider]/[mves|projects]/[name].mdx` — Spanish doc page (must include `isLab: true` in frontmatter).
- `llms.txt`, `llms-full.txt`, and `llms-small.txt` are generated automatically at build time by the `starlight-llms-txt` plugin (configured in `docs/astro.config.mjs`) — no manual update needed.