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
│   ├── settings.json
│   └── extensions.json
├── scripts/
│   ├── setup.sh
│   └── [other install tools sh]
├── docker-compose.yml
├── .env
├── .env.test
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
- **Never copy `.env` values into `containerEnv`.** Every value lives only in `.env`. When processes that do not load `.env` themselves need it (e.g. a VS Code extension such as AWS Toolkit), pass it from the `dev` service in `docker-compose.yml`: `env_file: .env` for the values as they are, plus `environment` entries built with `${VAR}` interpolation (Compose reads `.env`) when a value must be transformed, e.g. a relative path made absolute:
  ```yaml
  dev:
    env_file: .env
    environment:
      - AWS_CA_BUNDLE=/app/${AWS_CA_BUNDLE}
  ```
  `environment` overrides `env_file`. Reference Lab: `src/aws/projects/simple-etl-aws-emulator`.
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
name: mistlock-[provider]-[lab-name]

services:
  service:
    image: official/image
    ports:
      - "port:port"
    environment:
      - VARIABLE=value
    volumes:
      - name_data:/data
    command: optional command

  dev:
    image: mcr.microsoft.com/devcontainers/python:3.12-bookworm
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

- **name** (mandatory): Every `docker-compose.yml` must declare a top-level
  `name: mistlock-[provider]-[lab-name]`, using the short provider slug (`aws`,
  `azure`, `gcp`, `hybrid`) and the Lab directory name — e.g.
  `mistlock-aws-s3-garage`, `mistlock-gcp-simple-etl`, `mistlock-hybrid-redis`.
  It pins the Compose project name, which namespaces every container, volume and
  network the Lab creates. Two reasons it is required:
  - Without it Compose derives the project from the **working directory**, so
    several Labs running at once share names and collide. The provider slug is
    mandatory even when the Lab name looks unique, because names repeat across
    providers (`simple-etl`, `sql-writer`, `storage-writer`, `no-sql-writer`).
  - Inside the Dev Container the working directory is `/app`, not the Lab
    folder, so without `name` a `docker compose` call from within the container
    would target a *different* project than the same call from the host.
- **Do NOT use `container_name`.** It writes into Docker's flat, machine-global
  namespace, so any fixed value collides across Labs. Let Compose derive the
  name (`[project]-[service]-1`) and address containers through the Compose
  project instead — see below.
- **Address containers by service, never by name**: use
  `docker compose exec [service] …`, `docker compose logs [service]`, etc., in
  scripts and docs. Add `-T` when the command is non-interactive or pipes stdin
  (e.g. `docker compose exec -T db psql … < init.sql`). Plain
  `docker exec [name] …` is forbidden: the name it relies on no longer exists.
- **Service names**: Simple and representative (e.g., `azurite`, `localstack`),
  since they are now the identifier users type. They must be valid DNS labels
  (lowercase, hyphens — not underscores), as Compose publishes them as network
  hostnames.
- **volumes**: Name as `[service]_data`.

## Environment Variables

```
# Descriptive group comment
VARIABLE_ONE=value
VARIABLE_TWO=another-value

# Another group
OTHER_VARIABLE=value
```

Each Lab also has a `.env.test` at its root containing **only** the variables
that tests must override (e.g. a dedicated container/table name), never a full
copy of `.env`. Tests load `.env` first and then `.env.test` with
`override=True`. See the tests style guide for details.

## VS Code Settings

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python"
}
```

## VS Code Extensions

Every Lab must include a `.vscode/extensions.json` listing the recommended
extensions, so users get the same prompts whether or not they open the Dev
Container.

- The `recommendations` array must **mirror the `extensions` list** in
  `.devcontainer/devcontainer.json` (`customizations.vscode.extensions`). When
  you add or remove an extension in one, update the other.

```json
{
  "recommendations": [
    "ms-python.python"
  ]
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
- Every task needed to set up the environment must be referenced in the **setup** task to ensure a complete environment setup in one command. Only setup tasks hang from `setup`.
- **Every script in `scripts/` must be a mise task**, except `setup.sh` (it installs mise itself). The code stays in the script and the task only points to it (`run = "scripts/..."`). Users, docs, Dev Container and tests always run scripts through `mise run <task>`, never by calling the `.sh` directly. `mise run` loads `.env`, puts the mise tools on `PATH` (the real binaries, not the shims) and runs from the Lab root, so scripts never load `.env` or tweak `PATH` themselves.
- A task whose work is a single command runs it inline (`run = "..."`) instead of a one-line script. Scripts in `scripts/` are only for multi-command logic.
- Task names: `main` (inline: `.venv/bin/python main.py`), `test` (inline: `.venv/bin/python -m pytest tests/`), `deploy:<method>` and `destroy:<method>` (`scripts/<method>/deploy.sh` / `destroy.sh`), `install-<tool>` (`scripts/install-<tool>.sh`). Other scripts use a short kebab-case name matching the script.
- Tasks that are not setup (`main`, `test`, `destroy:*`, …) do not hang from `setup`. Exception: the default deployment method's `deploy:<method>` hangs from `setup`, and it must be idempotent (skip if already deployed) so `setup.sh` can run more than once.
- Manual commands in the docs that need `.env` (e.g. the AWS CLI) use `mise exec -- <tool> ...` from the Lab root.
- Reference Lab: `src/aws/projects/simple-etl-aws-emulator`.

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

[tasks.main]
description = "Run main.py"
run = ".venv/bin/python main.py"

[tasks.test]
description = "Run the Lab tests"
run = ".venv/bin/python -m pytest tests/"
```

- If an MVE requires a tool not available in **mise** that needs multiple bash commands, the installation of each tool must be in a separate script at `scripts/install-[tool].sh` and executed as a **mise** task.

Example:
```toml
[tasks.install-odbc]
description = "Install Microsoft ODBC driver for SQL Server"
run = "scripts/install-odbc.sh"
```

## Standardized Scripts Rule

The scripts in `scripts/` MUST be the **Single Source of Truth** for deployment and management. Each one is exposed and run as a **mise task** (see `mise.toml`); `setup.sh` is the only script called directly.
- **setup.sh**: Responsible for installing `mise`, installing tools, and running the `setup` task.
- **.devcontainer/postCreateCommand.sh**: Dev Container entry point. Runs `setup.sh` and appends the `mise` shims path to the shell rc files (idempotently).
- `main.py` and the tests are run by the inline mise tasks `main` and `test`, so there are no `run_main.sh` / `run_tests.sh` scripts.
- **[method]/deploy.sh** and **[method]/destroy.sh** (`mise run deploy:[method]` / `destroy:[method]`): One folder per deployment method, when the Lab has several.
- Scripts should use `.venv/bin/python` for Python-based tasks to avoid PATH issues.
- Scripts should handle clean up (deleting temporary files or state) where applicable.

## pyproject.toml

The chosen method for dependency management is **Python + uv** with `pyproject.toml`.

### Essential Fields
- **name**: Name of the example directory.
- **requires-python**: Should always be `">=3.12"`.
- **dependencies**: List all required libraries. Always include `python-dotenv`.
- **versions**: Do not specify version constraints unless strictly necessary.

### Structure Template
```toml
[project]
name = "example-name"
version = "0.1.0"
description = "Brief example description"
readme = "README.md"
requires-python = ">=3.12"
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
- `docs/src/content/docs/start-here/catalog.mdx` **and** `docs/src/content/docs/es/start-here/catalog.mdx` — the catalog is **hand-written, not autogenerated**. Add the Lab to the `<CatalogCard>` of its service under the right `##` provider section (`mves={[...]}` or `projects={[...]}`), or add a whole new `<CatalogCard>` when the service has no card yet. Insert it following the section's existing ordering (the AWS and Open Source sections are alphabetical by `title`).
- `docs/src/content/docs/index.mdx` **and** `docs/src/content/docs/es/index.mdx` — landing page. Add the service to the `<Grid>` of its provider section when no Lab for that service is listed there yet.
- `llms.txt`, `llms-full.txt`, and `llms-small.txt` are generated automatically at build time by the `starlight-llms-txt` plugin (configured in `docs/astro.config.mjs`) — no manual update needed.

Notes on both catalog and landing entries:

- `CatalogCard` hrefs are written **without** the `/es/` prefix in the Spanish page too — the component prepends the locale itself.
- Icon names come from the Iconify sets installed in `docs/package.json` (`@iconify-json/logos`, `@iconify-json/gcp`). Check the name exists before using it, e.g. `node -e "console.log(Object.keys(require('./node_modules/@iconify-json/logos/icons.json').icons).filter(n => n.includes('kafka')))"` — an unknown name fails the build.
- Run `pnpm build` in `docs/` and confirm the Lab shows up in `dist/start-here/catalog/index.html` and `dist/es/start-here/catalog/index.html`.