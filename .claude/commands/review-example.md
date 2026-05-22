---
description: Workflow for analyzing and improving an example (MVE or Project) by applying professional best practices and coding standards
---

# Best Practices Review Workflow (review-best-practices)

This workflow focuses on auditing a single example to identify technical debt, bad practices, and opportunities for professional-grade improvements.

## 1. Initialization

1.  **Select example**: Ask the user for the name of the example to review (e.g., `aws-lambda`).
2.  **Read Rules**: Review the following standards:
    - [python-style-guide.md](../rules/python-style-guide.md)
    - [example-structure.md](../rules/example-structure.md)
    - [readme-style-guide.md](../rules/readme-style-guide.md)

## 2. Technical Audit

Analyze all Python files, configuration files, and scripts within the example to check for:

1.  **Code Quality & Redundancy**:
    - **Duplication**: Identify and consolidate duplicated code blocks or logic.
    - **Boilerplate**: Remove code that adds no value (e.g., redundant try-except blocks that just re-raise).
    - **Abstraction**: Ensure code is direct; avoid unnecessary wrappers or complex inheritance for simple examples.
2.  **Naming & Inefficiency**:
    - **Conventions**: Enforce snake_case for Python and kebab-case for Cloud resources (buckets, tables).
    - **Efficiency**: Check for sub-optimal use of built-in functions or inefficient algorithms.
3.  **Resource & Context Management**:
    - **Context Managers**: Ensure files, database connections, and network sessions use `with` statements to guarantee proper closure.
    - **Leaks**: Identify manual `open()` or `.close()` calls that are prone to resource leaks.
    - **Queries**: Find "N+1" patterns or redundant API calls inside loops.
4.  **Security & Secret Management**:
    - **Hardcoded Secrets**: Search for API keys, passwords, or tokens directly in the code.
    - **Env Variables**: Verify that all configuration is loaded via `.env` files and `os.getenv()`.
    - **Profiles**: Ensure use of named profiles (like `localstack`) instead of relying on default credentials.
5.  **Professional Patterns & Industry Standards**:
    - **Idempotency**: Ensure deployment logic can be run multiple times safely (checking existence before creating).
    - **Feedback**: Ensure informative prints with standardized status indicators (e.g., `✓`, `!`, `...`).
    - **Language**: **MANDATORY**: All code, comments, docstrings, and English documentation MUST be in English.
6.  **Dependency, Environment & Tooling**:
    - **Templates**: Check if the example follows the [example template](../../templates/mve/) structure.
    - **Mise & UV**: Verify the existence and correct configuration of `mise.toml` and `pyproject.toml`. Remove any legacy dependency managers.
    - **Scripts**: Ensure `scripts/setup.sh` is the single source of truth and uses `.venv/bin/python` to avoid PATH issues.
7.  **Documentation Standards**:
    - **README Structure**: Enforce all mandatory H1/H2 headers from [readme-style-guide.md](../rules/readme-style-guide.md).
    - **Architecture**: Verify the use of `mermaid` with `architecture-beta` and the inclusion of the Mermaid chart badge.
    - **Translation**: Ensure `README.es.md` is a complete and high-quality translation of `README.md`.

## 3. Findings & Recommendations

1.  **Categorized List of Issues**:
    - **Critical**: Security risks, resource leaks, or broken logic.
    - **Improvement**: Refactoring for better performance, idempotency, or professional patterns.
    - **Style**: Naming inconsistencies or feedback/logging clarity.
2.  **Refactoring Plan**: Explain the "why" and "how" for each change, citing professional standards or project rules.

## 4. Execution & Validation

1.  **Apply Improvements**: Refactor the codebase to address the identified issues.
2.  **Run & Verify**: Execute the example to ensure functionality is preserved.
3.  **Documentation Sync**: Update `README.md` or `README.es.md` if code changes (renames, paths) affected the steps.
4.  **Finalize**: Present a summary of all improvements made to the user.
