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
    - [docs-style-guide.md](../rules/docs-style-guide.md)
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

## 4. Lab READMEs

Create two files in `src/[provider]/[mves|projects]/[example-name]/`:

**`README.md`**:
```markdown
# [Title]

[description from the English Starlight doc page]

> 📖 Full documentation for this lab is available at:
> https://mistlock.dev/[provider]/[mves|projects]/[name]/
```

**`README.es.md`**:
```markdown
# [Title]

[description from the Spanish Starlight doc page]

> 📖 La documentación completa de este lab está disponible en:
> https://mistlock.dev/[provider]/[mves|projects]/[name]/
```

- Use the `title` and `description` from the Starlight doc pages (step 5). The overview must match the doc `description` exactly — they must stay in sync.
- The URL must match the doc page path, not necessarily the `src/` folder name.
- For redirect labs (labs that point to another lab), use the destination lab URL directly — not the wrapper lab's own URL.

## 5. Documentation Site

Create the doc pages for the new example in the Starlight site following [docs-style-guide.md](../rules/docs-style-guide.md):

1. **English page**: `docs/src/content/docs/[provider]/[mves|projects]/[name].mdx`
2. **Spanish page**: `docs/src/content/docs/es/[provider]/[mves|projects]/[name].mdx`

Both pages must begin with this frontmatter:
```yaml
---
title: [Example Title]
description: [Brief description]
isLab: true
---
```

Also update `docs/public/llm.txt` — add the entry under the correct provider and type section.

## 6. Repository Documentation

Update the main tables in the root directory of `mve-collection` for every technology involved in the MVE:
- Add an entry to the table in `README.md`.
- Add a matching entry to the table in `README.es.md`.
