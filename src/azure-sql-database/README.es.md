# Azure SQL Database con Dapr

Ejemplo mínimo viable (MVE) que demuestra un flujo orientado a eventos: procesamiento de un archivo CSV subido a Azurite (Azure Blob Storage) e inserción de los registros en Azure SQL Edge mediante dapr bindings.

## Arquitectura

```mermaid
architecture-beta
    service blob_sender(internet)[Subida CSV]
    group azurite_group(cloud)[Emulación Local]
        service azurite(disk)[Azurite Blob]
        service sql_edge(database)[Azure SQL Edge]
    group dapr_group(server)[Flujo de Eventos]
        service dapr(server)[Dapr Sidecar]
        service app(server)[FastAPI App]

    blob_sender:R -- L:azurite
    azurite:R -- L:daprd
    daprd:R -- L:app
    app:L -- R:daprd
    daprd:L -- R:sql_edge
```
[![Ver Diagrama](https://img.shields.io/badge/Ver_Diagrama-Instalar-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

## Índice
- [Inicio Rápido (Dev Container)](#inicio-rápido-dev-container)
- [Paso a Paso (Setup Local)](#paso-a-paso-setup-local)
- [Componentes del Proyecto](#componentes-del-proyecto)
- [Validación](#validación)
- [Limpieza](#limpieza)

---

## Inicio Rápido (Dev Container)

**Requisitos**: [Docker](https://www.docker.com/get-started) y [Extensión Dev Containers](vscode:extension/ms-vscode-remote.remote-containers).

1. Pulsa `F1` y selecciona: **Dev Containers: Reopen in Container**.
2. Ejecuta `docker compose up -d`.
3. Espera a la inicialización de SQL: `scripts/init-sql.sh`.
4. Sube un CSV a Azurite y comprueba la tabla de SQL.
5. Limpiar: `docker compose down -v`.

---

## Paso a Paso (Setup Local)

### 1. Iniciar Infraestructura
Arranca todos los servicios incluyendo Dapr y SQL:
```bash
docker compose up -d
```

### 2. Configurar Entorno
Instala dependencias y herramientas con el script de configuración estandarizado:
```bash
scripts/setup-mve.sh
```

### 3. Inicializar Tablas SQL
La tabla SQL debe crearse una vez que SQL Edge esté en funcionamiento:
```bash
scripts/init-sql.sh
```

### 4. Ejecutar el Ejemplo
La aplicación ya se está ejecutando dentro del contenedor `app` vía Docker Compose. Puedes monitorear los logs para verificar la conectividad:
```bash
docker compose logs -f app
```

### 5. Validación
Sube un CSV de ejemplo llamado `sample.csv`.

**Contenido de Ejemplo (`sample.csv`):**
```csv
name,email
Alice,alice@example.com
Bob,bob@example.com
```

**Subida a Azurite:**
Puedes usar cualquier explorador de almacenamiento o un comando curl estándar si el contenedor existe:
```bash
# Subir datos de ejemplo al contenedor 'inbound'
curl -X PUT -H "x-ms-blob-type: BlockBlob" \
     --data-binary @sample.csv \
     "http://localhost:10000/devstoreaccount1/inbound/sample.csv"
```

**Consultar SQL Edge:**
Verifica que los datos se insertaron:
```bash
docker exec -it sql_local /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U sa -P Password123! \
  -Q "SELECT * FROM users"
```

---

## Componentes del Proyecto

### Aplicación FastAPI (`main.py`)
- **`process_blob`**: Disparado por Dapr cuando llega un nuevo blob. Parsea las filas del CSV y usa el cliente de Dapr para llamar al SQL Binding.

### Componentes Dapr (`dapr/components/`)
- **`blob-input.yaml`**: Monitoriza el contenedor `inbound` en Azurite.
- **`sql-output.yaml`**: Se conecta a Azure SQL Edge para ejecutar sentencias `INSERT`.

---

## Limpieza
Elimina todos los servicios y volúmenes:
```bash
docker compose down -v
```

## Licencia
Este es un ejemplo mínimo para fines educativos. Siéntete libre de usarlo y modificarlo según necesites.
