---
trigger: glob
globs: "tests/**"
description: Defines the mandatory structure and conventions for all tests in the repository.
---

# Tests Style Guide

## Local Tests (Inside MVE or Project)
- **Folder Structure**: Follow the same structure as `src/`. For example:
  - Code: `src/providers/redis_client.py`
  - Test: `tests/providers/test_redis_client.py`
- **Naming**: Tests must named `test_[module_name].py`.
- **No Mocking**: Do not mock calls to services (e.g., Redis, SQL) that are expected to be running in the local infrastructure.
- **Isolation & Cleanup**: Use fixtures to create the resources a test needs
  (containers, tables, queues…) and tear them down afterwards, so tests do not
  pollute the resources used by `main.py`.

## Test Environment Variables (`.env.test`)
- Each Lab keeps a `.env.test` at its root holding **only** the variables that
  must be overridden for tests (e.g. a separate container/table name). Do not
  duplicate the full `.env`.
- Tests load `.env` first, then `.env.test` on top with `override=True`, so only
  the variables present in `.env.test` are replaced:
  ```python
  from dotenv import load_dotenv

  load_dotenv()
  load_dotenv(".env.test", override=True)
  ```
- This guarantees tests act on dedicated resources (e.g. `bronze-test`) instead
  of the ones `main.py` uses (e.g. `bronze`).

## Global Integration Tests (mistlock/tests/)
- **Folder Structure**: `mistlock/tests/[cloud-provider]/[mves|projects]/[example-name]/test_[example_name].py`.
- **Pattern**: run the Lab through its mise tasks (see example-structure) with
  the `mise_run` fixture from `tests/conftest.py`:
    ```python
    def test_[example_name](mise_run):
        """Integration test description."""
        assert mise_run("test").returncode == 0
        assert mise_run("main").returncode == 0
    ```
- **Deployment methods**: use the `mise_deploy` fixture with indirect
  parametrization, which runs `deploy:<method>` and `destroy:<method>`:
    ```python
    @pytest.mark.parametrize("mise_deploy", ["terraform"], indirect=True)
    def test_deployment_method(mise_deploy, mise_run):
        assert mise_run("main").returncode == 0
    ```
- **Legacy**: the `run_tests`, `run_main` and `deploy` fixtures call the `.sh`
  scripts directly. They remain only for Labs not yet migrated to mise tasks;
  new and audited Labs use `mise_run` / `mise_deploy`.
