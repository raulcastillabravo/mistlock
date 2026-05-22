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

## Global Integration Tests (mve-collection/tests/)
- **Folder Structure**: `mve-collection/tests/[cloud-provider]/[mves|projects]/[example-name]/test_[example_name].py`.
- **Pattern**:
    ```python
    def test_[example_name](run_tests, run_main):
        """Integration test description."""
        pass
    ```
