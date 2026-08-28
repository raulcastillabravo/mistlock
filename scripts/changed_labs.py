"""Emit the JSON matrix of Lab keys affected by a set of changed files.

Reads changed file paths from stdin (one per line) and prints a JSON array
of Lab keys (``provider/category/name``) to stdout, ready to feed a GitHub
Actions matrix. If any shared file changed, every Lab is emitted.

Only Labs that actually have tests are emitted. A Lab without a
``tests/<lab>/test_*.py`` is skipped instead of producing a matrix job that
fails on ``file or directory not found``.
"""

import json
import re
import sys
from pathlib import Path

LAB_RE = re.compile(r"^(?:src|tests)/([^/]+/(?:mves|projects)/[^/]+)/")

SHARED = {
    "tests/conftest.py",
    "pyproject.toml",
    "uv.lock",
    ".github/workflows/run-tests.yml",
    "scripts/setup-tests.sh",
    "scripts/changed_labs.py",
}


def all_labs() -> list[str]:
    root = Path("tests")
    labs = {
        str(path.parent.relative_to(root))
        for path in root.glob("*/*/*/test_*.py")
    }
    return sorted(labs)


def changed_labs(files: list[str]) -> list[str]:
    testable = all_labs()

    if any(file in SHARED for file in files):
        return testable

    labs = {
        match.group(1)
        for file in files
        if (match := LAB_RE.match(file))
    }
    return sorted(labs.intersection(testable))


def main() -> None:
    if "--all" in sys.argv[1:]:
        print(json.dumps(all_labs()))
        return

    files = [line.strip() for line in sys.stdin if line.strip()]
    print(json.dumps(changed_labs(files)))


if __name__ == "__main__":
    main()
