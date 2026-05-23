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

## Content Source

- **README is the source of truth**: Every Lab has a `README.md`. The content of the Starlight page must come exclusively from that README. Do not invent, add, or assume content that is not present in the README.
- **Migration goal**: The only objective is to reformat existing README content to use Starlight components (`<Steps>`, `<Tabs>`, callouts, etc.). Structure sections only if the corresponding content exists in the README.

## Style

- **Conciseness**: Direct and focused on "how-to". No filler text.
- **Intro wording**: Use "This guide shows you how to work with **X** using **Y**..." as the opening sentence pattern. Use "lab" not "example" when referring to the project.
- **No Architecture section**: Do not include the Mermaid architecture diagram or its badge. Starlight pages focus on execution, not architecture.
- **Callouts**: Use Starlight admonition syntax instead of emoji callouts. Place callouts **outside** of `<Steps>` — never nest them inside:
  - `:::note[Title]{icon="..."}` — important notes or background information.
  - `:::tip[Title]` — tips or best practices.
  - `:::caution[Title]` — warnings or potential pitfalls.
  - `:::danger[Title]` — critical warnings.
- **Callout placement**: Put post-execution notes (e.g., key refresh warnings) immediately **after** `</Steps>`, not inside it or in Prerequisites.
- **URLs as code blocks**: Render navigable URLs as `bash` code blocks, not inline text.
- **Dynamic Connection Details**: Never hardcode connection strings, ports, or passwords. Always refer to environment variables from the `.env` file.
- **Standardized Action Labels**: Bold action labels at the start of list items: `**Run**:`, `**Open**:`, `**Verify**:`, `**Install**:`, etc.
- **No manual index**: Starlight generates the Table of Contents from headings automatically. Do not add an index section.
- **No H1 title in body**: The frontmatter `title` field handles it.

## Structure

Every page must follow this exact sequence:

### 1. Intro Paragraph

One or two sentences after the imports. Use the pattern:
```
This guide shows you how to work with **Service** using **Emulator** and **Language**. This lab demonstrates [what it does].
```

### 2. Prerequisites

An H2 section listing requirements.
- Docker entry: `- [Docker](https://www.docker.com/get-started) installed and running.`
- Dev Containers entry (when supported): `- [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) installed (optional).`
- Add a `:::note[Dev Containers]` callout only for **incompatibility** warnings (e.g., SAM CLI not working inside a container). Do not add a tip here for the Dev Container happy path — that belongs as a Tab in "How to execute".

### 3. How to execute

An H2 section wrapping the full execution flow in a `<Steps>` component.

**When the lab supports Dev Containers**, consolidate setup and infrastructure into Step 1 using `<Tabs>` with two options — "Dev Container (recommended)" and "Manually". Then Step 2 is always "Run the Example":

```mdx
## How to execute

<Steps>

1. **Setup Environment**:
   <Tabs>
      <TabItem label="Dev Container (recommended)">
         Open **VS Code** in the project folder and execute this command in the **Command Palette**:
         ```bash
         > Dev Containers: Reopen in Container
         ```
      </TabItem>
      <TabItem label="Manually">
         1. **Run the setup** script to install tools and dependencies.
            ```bash
            scripts/setup.sh
            ```
         2. **Start Infrastructure**: Launch the required containers.
            ```bash
            docker compose up -d
            ```
      </TabItem>
   </Tabs>

2. **Run the Example**:
   ```bash
   python main.py
   ```

</Steps>
```

**When the lab does NOT support Dev Containers** (e.g., SAM/Lambda), use a flat 3-step flow without Tabs:

```mdx
## How to execute

<Steps>

1. **Setup Environment**: Run the setup script to install tools and dependencies.
   ```bash
   scripts/setup.sh
   ```
2. **Start Infrastructure**: Launch the required services.
   ```bash
   [command]
   ```
3. **Run the Example**:
   [Tabs for multiple interaction methods, or plain code block if only one]

</Steps>
```

**When "Run the Example" has multiple interaction methods** (Python, cURL, CLI, etc.), use `<Tabs>/<TabItem>` for that step in either flow.

### 4. How to debug

An H2 section using a numbered list for different debug scenarios.
- Each item is a scenario (e.g., `1. **Python Script (main.py)**:`, `2. **Service/Function**:`).
- Sub-bullets describe the steps with action labels.
- Only include if the README contains debug instructions.

### 5. How to test

An H2 section with:
- `- **All tests**: Run the automated script: scripts/run_tests.sh`
- `- **Individually**: Use the VS Code **Testing** tab to run or debug specific test cases.`

Only include if the README contains test instructions.

### 6. Validate results

An H2 section with a numbered list of validation methods.
- Each item is a tool or method with a bold label (e.g., `1. **Check Buckets**:`, `2. **Explore with [Tool] (GUI)**:`).
- Always reference `.env` variables for connection details.
- Render navigable URLs as `bash` code blocks.
- Provide example commands or queries.

### 7. Clean Up

An H2 section with the cleanup steps.
- Standard: `docker compose down -v`
- For non-Docker labs (e.g., SAM/Lambda): numbered steps to stop services and remove artifacts.

### 8. Troubleshooting (optional)

A Markdown table with two columns — Issue and Solution — if the README includes troubleshooting content.

```markdown
| Issue | Solution |
|-------|----------|
| Problem description | How to fix it. |
```
