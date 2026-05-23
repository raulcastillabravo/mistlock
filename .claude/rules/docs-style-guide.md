---
trigger: glob
globs: "docs/src/content/docs/**/*.mdx"
description: Defines the mandatory style, structure, and content that all docs site pages must follow.
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
  - `:::note[Title]{icon="..."}` — informational notices, procedural reminders (e.g., "switch methods → clean up first").
  - `:::tip[Title]` — tips or best practices.
  - `:::caution[Title]` — reserve for genuinely risky actions (data loss, irreversible operations). Do not use for simple procedural reminders.
  - `:::danger[Title]` — critical warnings.
- **Callout placement**: Put post-execution notes (e.g., key refresh warnings) immediately **after** `</Steps>`, not inside it or in Prerequisites.
- **URLs as code blocks**: Render navigable URLs as `bash` code blocks, not inline text.
- **Dynamic Connection Details**: Never hardcode connection strings, ports, or passwords. Always refer to environment variables from the `.env` file.
- **Standardized Action Labels**: Bold action labels at the start of list items: `**Run**:`, `**Open**:`, `**Verify**:`, `**Install**:`, etc.
- **No manual index**: Starlight generates the Table of Contents from headings automatically. Do not add an index section.
- **No H1 title in body**: The frontmatter `title` field handles it.
- **Tab sync**: Use `syncKey="<key>"` on related `<Tabs>` components to keep them in sync (e.g., deployment method selection synced between "Deployment methods" and "Clean Up" sections). Tab labels must match exactly.

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
- Add a `:::note[Dev Containers]` callout only for **incompatibility** warnings (e.g., SAM CLI not working inside a container). Do not add tips or explanations for the Dev Container happy path here — that belongs as a Tab in "How to execute".

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

### 6. Deployment methods (optional)

An H2 section with a `<Tabs syncKey="deploy-method">` component when the lab supports multiple deployment methods (Terraform, CloudFormation, Boto3, AWS CLI, etc.).

- The **default method** (typically Boto3) goes inside the Manually tab of Step 1 in "How to execute". This section lists all alternatives.
- Immediately follow with a `:::note[Switching deployment methods]` reminding users to clean up before switching.

```mdx
## Deployment methods

There are other **deployment methods** you can use in this lab.

<Tabs syncKey="deploy-method">
   <TabItem label="Terraform">
      ```bash
      scripts/terraform/deploy.sh
      ```
   </TabItem>
   <TabItem label="CloudFormation">
      ```bash
      scripts/cloudformation/deploy.sh
      ```
   </TabItem>
   <TabItem label="Boto3">
      ```bash
      scripts/boto3/deploy.sh
      ```
   </TabItem>
</Tabs>

:::note[Switching deployment methods]
If you switch between methods, run **Clean Up** first to avoid resource name conflicts.
:::
```

### 7. Validate results

An H2 section. When there are multiple validation tools, use `<Tabs>` instead of a numbered list — one tab per tool (e.g., AWS CLI, AWS Toolkit, MinIO GUI, NoSQL Workbench).
- Always reference `.env` variables for connection details.
- Render navigable URLs as `bash` code blocks.
- Provide example commands or queries per tab.

### 8. Clean Up

An H2 section with the cleanup steps.
- Standard single method: `docker compose down -v`
- For non-Docker labs (e.g., SAM/Lambda): numbered steps to stop services and remove artifacts.
- **When the lab has multiple deployment methods**: use `<Tabs syncKey="deploy-method">` (same syncKey as "Deployment methods" section) for the per-method destroy script, then a separate code block for `docker compose down -v` with explanatory text distinguishing "remove resources only" vs "remove everything".

### 9. Troubleshooting (optional)

A Markdown table with two columns — Issue and Solution — if the README includes troubleshooting content.

```markdown
| Issue | Solution |
|-------|----------|
| Problem description | How to fix it. |
```

## Spanish Translation

Every English page must have a corresponding Spanish version at `docs/src/content/docs/es/[provider]/[mves|projects]/[name].mdx`. The Spanish version maintains identical structure, MDX components, `syncKey` values, and code blocks.

### What to translate

- All prose text: introductory sentences, descriptions, explanations
- Frontmatter `description` (and `title` only if it is not a brand/technical name)
- Section headings (see table below)
- Tab labels that are not technical proper nouns
- Callout titles unless they are technical terms or proper nouns
- Troubleshooting table content

### What to keep in English

- All code blocks, commands, scripts, file paths, and URLs
- Technical proper nouns: VS Code, Docker, Python, AWS CLI, Firebase, etc.
- The word "Testing" when referring to the VS Code Testing tab — never translate as "Pruebas"
- Use "tests" instead of "pruebas" for technical test references
- All `<TabItem label="...">` values that are technical names (Python, cURL, AWS CLI, REST Client, etc.)
- All `syncKey` attribute values

### Section heading translations

| English | Spanish |
|---------|---------|
| Prerequisites | Prerrequisitos |
| How to execute | Cómo ejecutar |
| How to debug | Cómo depurar |
| How to test | Cómo testear |
| Validate results | Validar resultados |
| Clean Up | Limpieza |
| Troubleshooting | Solución de problemas |
| Deployment methods | Métodos de despliegue |

### Tab label translations

| English | Spanish |
|---------|---------|
| `Dev Container (recommended)` | `Dev Container (recomendado)` |
| `Manually` | `Manual` |

All other tab labels that are technical names remain in English.

### Action labels

Bold action labels at the start of list items must use the **imperative (tú)** form — never infinitive:

| English | Spanish |
|---------|---------|
| **Open** | **Abre** |
| **Run** | **Ejecuta** |
| **Install** | **Instala** |
| **Verify** | **Verifica** |
| **Connect** | **Conecta** |
| **Navigate** | **Navega** |
| **Browse** | **Navega** |
| **Select** | **Selecciona** |
| **Enter Shell** | **Accede al shell** |
| **Enable** | **Activa** |
| **Monitor** | **Monitoriza** |
| **Expand** | **Despliega** |
| **Click** | **Haz clic en** |

### Intro pattern

```
Esta guía te muestra cómo trabajar con **Service** usando **Emulator** y **Language**. Este lab demuestra [what it does].
```

### Troubleshooting table

```markdown
| Problema | Solución |
|----------|----------|
| Description in Spanish | Solution in Spanish |
```
