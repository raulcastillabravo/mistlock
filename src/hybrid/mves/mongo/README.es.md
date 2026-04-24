# MongoDB

MVE (Minimal Viable Example) para MongoDB usando Docker Compose, MongoEngine ODM y MongoDB Compass para validación.

## Arquitectura

```mermaid
architecture-beta
    group api(cloud)[API Layer]
    group db(database)[Database Layer]

    service python(server)[Python App] in api
    service mongo(database)[MongoDB] in db

    python:R -- L:mongo
```
[![Ver Diagrama](https://img.shields.io/badge/Ver_Diagrama-Instalar-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

## Índice

- [Prerrequisitos](#prerrequisitos)
- [Quickstart](#quickstart)
- [Configurar Entorno](#configurar-entorno)
- [Iniciar Infraestructura](#iniciar-infraestructura)
- [Cómo ejecutar](#cómo-ejecutar)
- [Cómo depurar](#cómo-depurar)
- [Cómo testear](#cómo-testear)
- [Validar resultados](#validar-resultados)
- [Limpieza](#limpieza)

## Prerrequisitos

- [Docker](https://www.docker.com/get-started)
- [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) (Recomendado)
- [MongoDB Compass](https://www.mongodb.com/try/download/compass) (Opcional, para validación)

## Quickstart

1. Abrir en el Contenedor.
2. Ejecutar `python main.py`.

## Configurar Entorno

Si no usas Dev Containers, ejecuta el script de configuración:

```bash
bash scripts/setup.sh
```

## Iniciar Infraestructura

Lanza el servicio de MongoDB:

```bash
docker compose up -d
```

## Cómo ejecutar

### Usando python

Ejecuta el script de ejemplo:

```bash
bash scripts/run_main.sh
```

## Cómo depurar

### El cliente main.py

1. Abre `main.py`.
2. Presiona `F5` y selecciona **Python: Main**.

## Cómo testear

### Individualmente

Usa la barra lateral de Testing de VS Code para ejecutar tests.

### Todos los tests

Ejecuta el script de tests automatizados:

```bash
bash scripts/run_tests.sh
```

## Validar resultados

### Usando MongoDB Compass (Recomendado)

1. [Descarga e instala MongoDB Compass](https://www.mongodb.com/try/download/compass).
2. Crea una nueva conexión con esta cadena:
   ```
   mongodb://admin:admin123@localhost:27017/testdb?authSource=admin
   ```
3. Navega a `testdb` -> `users` para ver los documentos.

### Usando la extensión de VS Code

El Dev Container incluye la extensión **MongoDB for VS Code**.
1. Abre el icono de MongoDB en la barra de actividad.
2. Añade una nueva conexión usando la misma cadena de conexión.

## Limpieza

Detén los servicios y elimina los volúmenes:

```bash
docker compose down -v
```
