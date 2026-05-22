---
trigger: glob
globs: "docs/src/content/docs/**/*.mdx"
description: Defines the mandatory style, structure, and content that all Starlight documentation pages must follow.
---

## File Conventions

- **Extension**: Always `.mdx` (not `.md`) to support JSX component imports.
- **Location**: `docs/src/content/docs/[provider]/[mves|projects]/[name].mdx` (English), `docs/src/content/docs/es/[provider]/[mves|projects]/[name].mdx` (Spanish).
- **Dual Language**: Every page must have an English version and a Spanish version. The Spanish version is a complete, high-quality translation maintaining identical structure and code blocks.

## Frontmatter

Every page must begin with this frontmatter (each field must appear in this specific order, if not, reorder):

```yaml
---
title: Service Name (Emulator)
description: One or two sentences describing what the lab demonstrates and how it works.
isLab: true
---
```

- `title` replaces the `# H1` heading — Starlight renders it automatically. Do not add a `# Title` in the body.
- `description` is shown in metadata and page previews.
- `isLab: true` is mandatory on all Lab (MVE/Project) pages. It must appear after `title` and `description`.

## Imports

Declare all Starlight component imports immediately after the frontmatter, before any content:

```mdx
import { Steps } from '@astrojs/starlight/components';
import { Tabs, TabItem } from '@astrojs/starlight/components';
```

Only import components that are actually used in the page.

## Style

- **Conciseness**: Direct and focused on "how-to". No filler text.
- **Callouts**: Use Starlight admonition syntax instead of emoji callouts:
  - `:::note[Title]{icon="..."}` — important notes or background information.
  - `:::tip[Title]` — tips or best practices.
  - `:::caution[Title]` — warnings or potential pitfalls.
  - `:::danger[Title]` — critical warnings.
- **Dynamic Connection Details**: Never hardcode connection strings, ports, or passwords. Always refer to environment variables from the `.env` file.
- **Standardized Action Labels**: Bold action labels at the start of list items: `**Run**:`, `**Open**:`, `**Verify**:`, `**Install**:`, etc.
- **No manual index**: Starlight generates the Table of Contents from headings automatically. Do not add an index section.
- **No H1 title in body**: The frontmatter `title` field handles it.

## Structure

Every page must follow this exact sequence:

### 1. Intro Paragraph

One or two sentences after the imports that expand on the frontmatter description. Bold the key technologies.

Example:
```
This guide shows you how to work with **Azure SQL Database** using **pyodbc** and **Python**.
```

### 2. Prerequisites

An H2 section listing requirements to run the example.
- Bulleted list with links.
- Include [Docker](https://www.docker.com/get-started) when Docker is required.
- Add a `:::note[Dev Containers]` callout for any Dev Container compatibility warnings.

### 3. How to execute

An H2 section wrapping the full execution flow in a `<Steps>` component.

- **Step 1 — Setup Environment**: Run `scripts/setup.sh`.
- **Step 2 — Start Infrastructure**: Launch required services (e.g., `docker compose up -d` or service-specific commands). Use sub-bullets for multiple services/terminals.
- **Step 3 — Run the Example**: Use a `<Tabs>/<TabItem>` block to show all interaction methods (Python, cURL, REST Client, CLI, etc.).

Template:
```mdx
## How to execute

<Steps>

1. **Setup Environment**: Run the setup script to install tools and dependencies.
   ```bash
   scripts/setup.sh
   ```
2. **Start Infrastructure**: Launch the required containers.
   ```bash
   docker compose up -d
   ```
3. **Run the Example**:
   <Tabs>
      <TabItem label="Python">
         ```bash
         python main.py
         ```
      </TabItem>
      <TabItem label="cURL">
         ```bash
         curl "http://localhost:PORT/endpoint"
         ```
      </TabItem>
   </Tabs>

</Steps>
```

### 4. How to debug

An H2 section using a numbered list for different debug scenarios.
- Each item is a scenario (e.g., `1. **Python Script (main.py)**:`, `2. **Service/Function**:`).
- Sub-bullets describe the steps with action labels.

### 5. How to test

An H2 section with:
- `- **All tests**: Run the automated script: scripts/run_tests.sh`
- `- **Individually**: Use the VS Code **Testing** tab to run or debug specific test cases.`

### 6. Validate results

An H2 section with a bulleted list of validation methods.
- Each item is a validation tool or method with a bold label (e.g., `- **Logs**:`, `- **CLI Output**:`).
- Always reference `.env` variables for connection details.
- Provide example commands or queries.

### 7. Clean Up

An H2 section with the cleanup steps.
- Standard: `docker compose down -v`
- For non-Docker examples (e.g., SAM/Lambda): numbered steps to stop services and remove artifacts.
