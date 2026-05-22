---
trigger: glob
globs: "**/README*.md"
description: Defines the mandatory style, structure, and content that all README files in the repository must follow.
---

## Style

- **Dual Language**: Every example must have an English version (`README.md`) and a Spanish version (`README.es.md`).
- **Translation Quality**: The Spanish version must be a high-quality, complete translation of the English content, maintaining the same structure and code blocks.
- **Conciseness**: Explanations must be direct and focused on "how-to" and "why".
- **Emojis**: Use emojis sparingly and only for specific callouts:
    - 💡: Tips or best practices.
    - ℹ️: Important notes or background information.
    - ⚠️: Warnings or potential pitfalls.
    - ✓: Success markers or validation steps.
- **Dynamic Connection Details**: Never hardcode connection strings, ports, or passwords. Always refer to the environment variables defined in the `.env` file.
    - Example: `Connect using the MONGO_URI defined in your .env.`
- **Standardized Action Labels**: Use bolded action labels at the start of list items for quick scanning:
    - `**Connect**:`, `**Open**:`, `**Run**:`, `**Verify**:`, `**Interactive**:`, etc.

## Structure

Every README must follow this exact sequence of headers:

### 1. Title
A short, descriptive title containing the main technology (e.g., `# Azure SQL Database`).

### 2. Architecture
A simple Mermaid diagram demonstrating the technology flow.
- **Format**: Always use `mermaid` with the `architecture-beta` type.
- **Group Label**: Use `cloud` as the group label for cloud services (e.g., `group cloud(cloud)[Cloud]`).
- **Visualizer Badge**: Immediately follow the diagram with the "View Diagram Install" badge:
  ```markdown
  [![View Diagram](https://img.shields.io/badge/View_Diagram-Install-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)
  ```

### 3. Index
A bulleted list of anchor links to all main H2 sections. Avoid linking to sub-items if the section uses the numbered list format.

### 4. Prerequisites
An H2 section detailing the requirements to run the MVE in any mode.
- Bulleted list with links to [Docker](https://www.docker.com/get-started) and the [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers).

### 5. Quickstart
An H2 section with the minimal, numbered steps to run the MVE.
- Standard steps:
  1. **Open in Container**: Open VS Code in the project folder and select **Dev Containers: Reopen in Container**.
  2. **Run the Example**: `python main.py`.

### 6. Setup Environment
An H2 section explaining how to prepare the environment manually (without Dev Container).
- Content: `If you are not using a Dev Container, you can set up the environment manually: scripts/setup.sh`

### 7. Start Infrastructure
An H2 section with the command to launch the required services.
- Always include the message: `If you are not using a Dev Container, launch the required containers: docker compose up -d`

### 8. How to execute
An H2 section using a **numbered list** for different interaction methods.
- Each item should be a tool or method (e.g., `1. **Using python**:`, `2. **Using [Tool Name](link)**:`).
- Use sub-bullets with bolded action labels for the steps.

### 9. How to debug
An H2 section using a **numbered list** for different debugging scenarios (e.g., `1. **main.py**:`, `2. **Tests**:`).
- Use sub-bullets for the steps (`- **Open**:`, `- **Breakpoints**:`, `- **Run**:`).

### 10. How to test
An H2 section using a **numbered list** for running tests:
- `1. **Individually**: Via VS Code Testing tab.`
- `2. **All tests**: Via automated script (scripts/run_tests.sh).`

### 11. Validate results
An H2 section using a **numbered list** to verify success.
- Each item should be a tool (e.g., `1. **Check using [Tool Name](link)**:`).
- Always refer to `.env` variables for connection details.
- Provide example queries or commands (SQL, CLI, or Python) to verify the state.

### 12. Clean Up
An H2 section with the command to stop services and remove volumes: `docker compose down -v`.
