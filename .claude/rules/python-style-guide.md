---
trigger: glob
globs: "**/*.py"
description: Defines the mandatory style and structure that all python files in the repository must follow.
---

## Principles
- **All code, comments, docstrings, and variable names MUST be in English.**
- **Follow good practices**.
- **Minimalist and concise code**.
- **Avoid unnecessary abstractions**.
- **Simplicity over flexibility**.

## Classes vs Functions
- Prefer using classes to encapsulate code.
- Use functions when:
  - Encapsulating logic for `main.py`.
  - Intrinsic to the framework (e.g., Azure Functions, AWS Lambda).

## Imports
- Follow this order:
  1. Python standard library imports.
  2. Third-party imports.
  3. Local imports.
- Use double line breaks between groups.

## Environment Variables
- Load environment variables using `load_dotenv()`.
- Load them at the beginning of the module:
  - In classes: Load in `__init__`.
  - In functions: Load outside the function at the module level (after imports and `load_dotenv()`).
- **Do NOT use default values in `os.getenv`**. If a variable is required, ensure it is defined in the `.env` file or handle the missing case.

## Typing
- Add type hints to all declared variables:
  - Function and method arguments.
  - Public class attributes (declared at the start of the class, initialized to `None`).
  - Private class attributes (outside `__init__`, prefixed with `_`).
  - Function returns (except when the return is `None`).

## Attribute Declaration
- All class attributes must be declared at the top of the class, before `__init__`.
- Attributes must have a type hint and be initialized to `None` if their value is set in `__init__`.
- **Prefer using private attributes** (prefixed with `_`) unless the attribute explicitly needs to be public. Avoid public attributes where possible.

Example:
```python
class MyClass:
    name: str = None
    _private_attr: int = None

    def __init__(self, name: str):
        self.name = name
        self._private_attr = 10
```

## Docstrings
- If the function name is self-explanatory and has simple parameters, do not add a docstring.
- If added, they must be concise.
- If a parameter requires a specific format, provide an example.

## Error Handling
- Prefer letting exceptions bubble up to show the original error and stop the process rather than creating custom exception handling just for a custom message.
- Exception handling is only accepted when:
  - Strictly necessary for process logic (e.g., retrying a request N times).
  - Performing the operation and letting it fail is better than checking first (LEAP - Look Before You Leap vs EAFP - Easier to Ask for Forgiveness than Permission).

## Sizes
- Aim for files not to exceed 25 lines of code.
- If a file exceeds 40 lines, look for ways to modularize.
- Aim for lines of code not to exceed 79 characters.
