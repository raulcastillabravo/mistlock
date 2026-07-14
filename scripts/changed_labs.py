"""Emit the JSON matrix of Lab keys affected by a set of changed files.

Reads changed file paths from stdin (one per line) and prints a JSON array
of Lab keys (``provider/category/name``) to stdout, ready to feed a GitHub
Actions matrix. If any shared file changed, every Lab is emitted.
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
    if any(file in SHARED for file in files):
        return all_labs()

    labs = {
        match.group(1)
        for file in files
        if (match := LAB_RE.match(file))
    }
    return sorted(labs)


def main() -> None:
    if "--all" in sys.argv[1:]:
        print(json.dumps(all_labs()))
        return

    files = [line.strip() for line in sys.stdin if line.strip()]
    print(json.dumps(changed_labs(files)))


if __name__ == "__main__":
    main()
