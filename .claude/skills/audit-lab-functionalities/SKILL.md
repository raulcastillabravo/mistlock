---
name: audit-lab-functionalities
description: >-
  Audit a Lab (MVE or Project) to identify missing user-facing functionalities —
  setup, infrastructure, execution methods, debugging, testing, validation and
  clean up. Use when asked to find what a Lab is missing, check Lab completeness,
  or compare a Lab against the functionality matrix. Produces a status matrix,
  a prioritized gap list and an actionable task list.
---

# Audit Lab Functionalities

Identify which user-facing **functionalities** a Lab is missing and report them in a
consumable format (status matrix + gaps + task list).

A "functionality" is an option the user has to: bring up infrastructure, auto-install
tools/deps via `setup.sh`, **execute** the Lab (multiple methods), **debug** it (multiple
scenarios), **test** every part, **validate** results (multiple tools), and **clean up**.

## Inputs

- Lab path: `src/[provider]/[mves|projects]/[name]`.
- Its docs: `docs/src/content/docs/[provider]/[mves|projects]/[name].mdx` (EN) and the
  `es/` counterpart.
- Its global integration test dir: `tests/[provider]/[mves|projects]/[name]/`.

## References to read first

- `.claude/rules/example-structure.md` — required files/scripts per Lab.
- `.claude/rules/docs-style-guide.md` — required doc sections and their order.
- `.claude/rules/tests-style-guide.md` — local and global test conventions.

## The Functionality Matrix (primary guide)

This matrix — **not** a twin Lab — is the source of truth for completeness. A twin Lab
(same service, e.g. `s3-minio` for `s3-garage`) is only a convenience for near-1:1 copying
**when one exists**; most Labs have no twin, so audit against the matrix directly.

The matrix is **extensible**: when a new common functionality is identified across Labs,
add a row here.

| # | Functionality | Signal in `src/` | Signal in `docs/` |
|---|---------------|------------------|-------------------|
| 1 | Setup — Dev Container | `.devcontainer/devcontainer.json` with `dockerComposeFile` + `postCreateCommand: scripts/setup.sh` | Tab "Dev Container (recommended)" in How to execute |
| 2 | Setup — Manual (mise) | `scripts/setup.sh` installing mise + `mise.toml` with a complete `setup` task | Tab "Manually" |
| 3 | Infrastructure | `docker-compose.yml` (or SAM/firebase equivalent) | Step "Start Infrastructure"/"Start Host" |
| 4 | Execution — multiple methods | `scripts/run_main.sh`; `main.py`; optional `http/*.http`, CLI scripts | Step "Run the Example" using `<Tabs>` (Python / cURL / REST Client / CLI) |
| 5 | Debug | `.vscode/launch.json` with configs (main.py, function/service, tests) | Section "How to debug" |
| 6 | Test — local | `tests/` mirroring `src/`, `tests/conftest.py`, `.env.test`, `scripts/run_tests.sh` | Section "How to test" |
| 7 | Test — global integration | `tests/[provider]/[mves\|projects]/[name]/test_[name].py` using `run_tests`/`run_main` fixtures | — |
| 8 | Validate results — multiple tools | CLI/GUI scripts (`*_cli.sh`, `*-gui.sh`), VS Code extensions | Section "Validate results" using `<Tabs>` (≥2 tools) |
| 9 | Clean Up | `docker compose down -v` (or service-specific teardown) | Section "Clean Up" |
| 10 | Docs parity EN/ES | — | `es/` page exists with the same sections as the EN page |

Notes:
- Some functionalities are **not applicable** to every Lab (e.g. SAM Labs are incompatible
  with Dev Containers; a pure CLI Lab may have a single execution method). Mark these
  `N/A` with a one-line reason rather than as a gap.
- Reference "complete" Labs to consult as benchmarks: `aws/mves/lambda-sam`,
  `aws/mves/s3-minio`, `azure/mves/functions`, `google-cloud/mves/firebase-cloud-functions`,
  `hybrid/mves/mongo`, `hybrid/mves/redis`.

## Procedure

1. **Inventory** the Lab: list files in `src/[lab]`, read its EN+ES docs pages, and check
   for `tests/[provider]/[mves|projects]/[name]/`.
2. **Score each matrix row** as `✅` (present), `⚠️` (partial), `❌` (missing) or `N/A`
   (with reason) — checking **both** the `src/` signal and the `docs/` signal. A row is
   only `✅` when both code and docs are present.
3. **Cite evidence**: the exact file path that satisfies (or the absence that fails) each row.
4. **Twin compare (optional)**: if a same-service twin exists, diff structure to surface
   anything the twin offers that this Lab lacks; otherwise rely on the matrix.
5. **Check EN/ES parity**: same sections in both doc pages.

## Output format

Produce Markdown with three parts:

### 1. Status matrix

Reproduce the matrix table with a Status column and an Evidence column per row.

### 2. Prioritized gaps

- **Critical**: an entire functionality dimension absent (e.g. no tests at all, no debug).
- **Improvement**: partial coverage (e.g. a single execution method where more apply,
  missing optional validation tool).

### 3. Task list

Concrete, ordered, actionable items to close every gap — each naming the file(s) to create
or edit and, when a twin exists, the file to copy from (adjusting service-specific values
such as ports, endpoints, profiles, and dynamic credentials).
