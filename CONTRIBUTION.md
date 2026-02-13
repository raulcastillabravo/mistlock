# Contributing Guide 🚀

First of all, thank you so much for being here! If you are reading this, it's because you are interested in participating in this project, and that makes me very excited.

## Project Vision

This project was born with the idea of creating a resource for the community to be able to **develop for the Cloud without having to pay**.

It is not a replacement for the Cloud, but a complement to avoid costs during development, testing, and debugging.

Therefore, there are three key points you should know if you want to collaborate:
* **100% free and no accounts**: All technologies and examples must be completely free or use a **Free Tier**. Furthermore, no example should require an account for any tool.
* **MVE (Minimal Viable Examples)**: Examples should be as simple as possible. We don't intend to teach how to develop in the Cloud; we only want to show how to emulate it locally.
* **One-click execution**: Examples must be executable with as few steps as possible, which is why we use **Dev Containers** to automate the entire environment.

The examples in the repository will be used in the future to create **YouTube videos, talks, workshops, and courses**, and all contributors who have participated in the code development will be mentioned.

## How to contribute 🛠️

To keep the workflow organized and simple, I suggest following these steps:

### 1. Set up your environment

- **Fork the repository**: Create a "fork" of the project to your GitHub account to have your own copy. You can do this with the "Fork" button at the top right.
- **Clone your fork**: Download the code to your local machine:
  ```bash
  git clone <YOUR_FORK_URL>
  ```
- **Add the original repository as a remote**: To keep your copy updated:
  ```bash
  git remote add upstream https://github.com/raulcastillabravo/mve-collection.git
  ```
- **Prerequisites**: Make sure you have Python >= 3.9, Docker, and **uv** installed for dependency management (`pip install uv`).

### 2. Work on your changes

- **Sync your fork**: Make sure you are up to date with `main`:
  ```bash
  git switch main && git fetch upstream && git merge upstream/main
  ```
- **Create a new branch**: Use a descriptive name: `git switch -c feature/your-example-name`.
- **Develop your MVE**: Implement your example following the project standards (see section below).
- **Test your changes**: Ensure the example works perfectly both in the Dev Container and locally.

### 3. Submit your changes

- **Commit your changes**: Use clear messages following the convention: `feat: add [service] example`.
- **Push to your fork**: Upload your changes to GitHub:
  ```bash
  git push origin feature/your-example-name
  ```
- **Create a Pull Request (PR)**: Go to your fork on GitHub and click on "Pull request." Describe what you've added and why it's useful.

## MVE Structure 🏗️

The repository consists of **independent examples** that teach how to emulate one or several Cloud services, and all of them maintain consistency in terms of structure and documentation.

The minimum requirements that an MVE must meet are:

### 1. Development Environment
* **Dev Container**: It must include a `.devcontainer/` folder that allowing you to run the entire MVE with a single click (Reopen in Container).
* **Local Environment**: It must also be executable without a Dev Container by following the documented steps.

### 2. Documentation (README.md & README.es.md)
Documentation must be bilingual (English and Spanish) and follow this section structure:

1. **Title and Description**: What the MVE does and what technologies it uses.
2. **Architecture (Optional)**: Mermaid diagram of the involved services.
3. **Index**: Quick links to sections.
4. **Quickstart (Dev Container)**: Steps to run it quickly using the development container.
5. **Step by Step (without Dev Container)**: Detailed section for manual execution that must contain:
    * **Start infrastructure**: How to spin up services (e.g., Docker Compose).
    * **Configure CLI/Tools**: Configuration of AWS CLI, Azure CLI, etc.
    * **Install Python/Dependencies**: Python installation and synchronization with `uv`.
    * **Deploy resources**: Steps to deploy infrastructure (e.g., Terraform, CloudFormation, Boto3).
    * **Run the example**: How to run the main script (`main.py`).
    * **Validation**: How to verify that everything worked correctly.
    * **Clean up**: Commands to clean and stop services.
6. **Troubleshooting**: Solutions to common issues.
7. **License**: License of the example.

### 3. Code
* **Language**: All code, variables, functions, and comments must be in **English**.
* **Simplicity**: Direct, minimalist code without unnecessary abstractions.
* **Dependencies**: Always managed with `pyproject.toml` and `uv`.

## Happy coding!

That being said, I hope you enjoy this repository as much as I do and that it is of great help in your projects. Don't hesitate to open an issue, propose improvements, or open a PR to add changes, I'll be happy to read from you.

Best regards,
Raúl.
