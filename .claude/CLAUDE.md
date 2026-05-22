This repository aimed at teaching how to emulate the Cloud locally (AWS, Azure, Google Cloud, Open Source services, etc.).

## Main concepts

It is structured into **Labs**. A Lab is either an **MVE** or a **Project**:

* **MVE (Minimal Viable Example)**: Focus on one specific Cloud service, how to emulate it and which tools are required to develop with it locally. There can be more than one MVE per service if there are several tools to emulate it.
* **Project**: Combine different Cloud services in the same local development environment.

Each Lab (MVE or Project) is independent and isolated from the others.

## Main rules

- **Free and Account-less**: All technologies must be free and not require creating an account anywhere (no credit cards, no cloud logins).
- **Service-Focused**: Centered on a specific cloud service, even if other supporting services are involved.
- **100% Compatible**: The code developed locally must be 100% compatible with the real Cloud services.
- **Ready to Run**: Examples must be dockerized and self-contained, including all necessary configuration to run immediately.
- **Environment Agnostic**: Infrastructure must work both inside and outside a Dev Container.
- **Mise Integration**: Tools must be installed via `mise` in both the Dev Container and host machine.
- **Cross-Platform**: Full compatibility with Windows, Linux, and MacOS.
- **Standardized Execution**: Single entry point via `main.py`, with support for debugger and automated tests.
- **Full Visibility**: Direct terminal access and recommended GUIs/VS Code extensions for all involved services.

## Project structure

- src/ folder contains MVEs and Projects structured by Cloud provider. The folder structure is src/[cloud-provider]/[mves|projects]/[cloud-service]-[emulator]/. Currently, these cloud providers are considered:
  - AWS.
  - Azure.
  - Google Cloud (GCP).
  - Hybrid: which is a mixture of different Open Source services such as Postgres, Redis, Mongo...
- docs/ is an Astro + Starlight site (package manager: `pnpm`). Each Lab (MVE/Project) has a matching doc page at `docs/src/content/docs/[provider]/[mves|projects]/[name].mdx` (English) and `docs/src/content/docs/es/[provider]/[mves|projects]/[name].mdx` (Spanish). Lab pages are identified by `isLab: true` in their frontmatter. Sidebar autogenerates from directory structure. Run with `pnpm dev` from `docs/`.
- tests/ is the test folder and follows the exact same structure as src/.

## References

Read specific rule files for more information about these topics:

- Python: .claude/rules/python-style-guide.md.
- README: .claude/rules/readme-style-guide.md.
- Testing: .claude/rules/tests-style-guide.md.
- MVE / Project structure: .claude/rules/example-structure.md

