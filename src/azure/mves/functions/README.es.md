# Azure Functions

Azure Functions permite ejecutar pequeñas piezas de código (llamadas "funciones") sin preocuparse por la infraestructura de la aplicación. Este MVE demuestra cómo desarrollar y probar Azure Functions localmente utilizando **Azure Functions Core Tools**.

## Architecture

```mermaid
architecture-beta
    group cloud(cloud)[Azure]

    service func(server)[Functions Emulator] in cloud
    service client(internet)[Python Client]

    client -- "HTTP GET/POST" --> func
```

[![View Diagram](https://img.shields.io/badge/View_Diagram-Install-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

- **Client Python**: Un script sencillo que envía peticiones HTTP a la función.
- **Emulador de Functions**: Entorno de ejecución local proporcionado por Azure Functions Core Tools.

## Index

- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Setup Environment](#setup-environment)
- [Start Infrastructure](#start-infrastructure)
- [How to execute](#how-to-execute)
- [How to debug](#how-to-debug)
- [How to test](#how-to-test)
- [Validate results](#validate-results)
- [Clean Up](#clean-up)

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Extension Dev Containers](vscode:extension/ms-vscode-remote.remote-containers)

## Quickstart

1. **Abrir en Contenedor**: Abre VS Code en esta carpeta y selecciona **Dev Containers: Reopen in Container**.
2. **Ejecutar el Ejemplo**: `python main.py`.

## Setup Environment

Si no estás usando un Dev Container, puedes configurar el entorno manualmente: `scripts/setup.sh`

## Start Infrastructure

Si no estás usando un Dev Container, inicia los servicios requeridos: `docker compose up -d`

## How to execute

1. **Usando python**:
    - **Interactivo**: `python main.py`
    - **Script**: `scripts/run_main.sh`
2. **Usando curl**:
    - **Ejecutar**: `curl "http://localhost:7071/api/get_secret?username=admin"`
3. **Usando REST Client**:
    - **Abrir**: `app.http` (si se crea) o usa cualquier cliente REST.

## How to debug

1. **main.py**:
    - **Abrir**: `main.py`
    - **Breakpoints**: Establece un breakpoint en la función `main`.
    - **Ejecutar**: Presiona `F5` o usa la pestaña "Run and Debug".
2. **Functions**:
    - **Abrir**: `function_app.py`
    - **Breakpoints**: Establece un breakpoint dentro de `get_secret`.
    - **Ejecutar**: Usa la extensión de VS Code para Azure Functions o adjunta el debugger al proceso `func host start`.

## How to test

1. **Individualmente**: A través de la pestaña Testing de VS Code.
2. **Todos los tests**: A través del script automatizado (`scripts/run_tests.sh`).

## Validate results

1. **Verificar usando la Terminal**:
    - **Validar**: La salida de `main.py` debe mostrar el secreto para 'admin' y 403 para otros usuarios.
2. **Verificar usando Logs**:
    - **Inspeccionar**: Revisa la salida de la terminal donde se ejecuta `func start` para ver los logs de ejecución de la función.

## Clean Up

`docker compose down -v`
