---
description: Workflow to create a new example (MVE or Project)
---

# Example Creation Workflow

This workflow ensures all new examples (Minimal Viable Examples or Projects) follow the repository's professional standards and architecture.

## 1. Requirements & Branching

1.  **Request Details**: Ask the user if they want to create an **MVE** or a **project**. Then, ask for the **example name** and its **technical specification** (technologies, architecture, and goals).
2.  **Ensure Up-to-Date**: Run `git checkout main` and `git pull` in the `mve-collection` repository to ensure you are on the correct and updated branch.
3.  **Create Branch**: Create a new feature branch in the `mve-collection` repository following the format `feature/[example-name]`.

## 2. Planning Phase (STOP AND PLAN)

Before writing any code, the agent must present a plan to the user for approval:
1.  **Review Rules**: Carefully read and apply the following project rules:
    - [example-structure.md](../rules/example-structure.md)
    - [python-style-guide.md](../rules/python-style-guide.md)
    - [readme-style-guide.md](../rules/readme-style-guide.md)
2.  **Define Architecture**: Outline the components, services (Docker Compose), and the Python script's logic.
3.  **File Structure Plan**: List all files to be created/modified.
4.  **Wait for Approval**: Do not proceed to implementation until the user approves the plan.

## 3. Implementation

1.  **Develop**: Implement the MVE following the approved plan and project rules.
3.  **Tests**: Create an integration test in `mve-collection/tests/[cloud-provider]/[mves|projects]/[example-name]/test_[example_name].py`. Use the following pattern:
    ```python
    def test_[example_name](run_tests, run_main):
        pass
    ```
    This test ensures the MVE can be initialized and executed correctly in CI.

## 4. Documentation Site

Create the doc pages for the new example in the Starlight site:
1. **English page**: `docs/src/content/docs/[provider]/[mves|projects]/[name].md`
2. **Spanish page**: `docs/src/content/docs/es/[provider]/[mves|projects]/[name].md`

Both pages must use this frontmatter:
```markdown
---
isExample: true
title: [Example Title]
description: [Brief description]
---
```

Content must follow the same structure as the example's `README.md` / `README.es.md`.

## 5. Repository Documentation

Update the main tables in the root directory of `mve-collection` for every technology involved in the MVE:
- Add an entry to the table in `README.md`.
- Add a matching entry to the table in `README.es.md`.