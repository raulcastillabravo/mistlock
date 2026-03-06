# GCP Cloud SQL (PostgreSQL) + Local Emulator Firebase

Ejemplo mínimo viable (MVE) para trabajar con **Google Cloud SQL (PostgreSQL)** emulado localmente mediante **Docker Compose**, y **Funciones de nube Firebase** activadas por **Cloud Storage**. Este ejemplo demuestra un flujo completo de datos: Carga de CSV -> Activador de almacenamiento -> Procesamiento de función -> Inserción en Postgres.

## Estructura del proyecto

```
gcp-cloud-sql/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── functions/
│   ├── main.py              # Lógica de la función nubosa (V2)
│   └── requirements.txt     # Dependencias de la función
├── scripts/
│   └── setup-mve.sh         # Script de configuración estandarizado
├── docker-compose.yml       # Contenedor PostgreSQL
├── .env                     # Cadenas de conexión locales
├── firebase.json            # Configuración del emulador
├── mise.toml                # Configuración de herramientas
├── main.py                  # Script principal de demostración
├── pyproject.toml           # Dependencias del proyecto
└── README.md
```

## Requisitos previos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional)

## Opción 1: Uso del contenedor de desarrollo (Recomendado)

### Paso 1: Abrir el proyecto en el contenedor de desarrollo

1. Abre VS Code en la carpeta del proyecto.
2. Pulsa `F1` o `Ctrl+Shift+P`.
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el entorno se cree. Se instalarán automáticamente todas las herramientas necesarias (**Node.js**, **Java**, **Firebase Tools**, **mise**, **uv**) y todas las dependencias de Python.

### Paso 2: Iniciar servicios

Abre un terminal dentro del contenedor de desarrollo y ejecuta:

```bash
# Iniciar PostgreSQL
docker compose up -d

# Iniciar los emuladores de Firebase
firebase emulators:start
```

### Paso 3: Ejecutar el ejemplo

Abre un segundo terminal y ejecuta:

```bash
python main.py
```

Deberías ver una salida como esta:
```
🚀 Iniciando demostración...
✅ CSV cargado en el emulador de almacenamiento.
⏳ Esperando a la función nubosa... (1s)
📊 Se han encontrado 2 registros en Postgres:
 - Antigravity (anti@gravity.ai)
 - Usuario (user@example.com)
```

## Opción 2: Configuración local (sin contenedor de desarrollo)

### Paso 1: Iniciar infraestructura

```bash
docker compose up -d
```

### Paso 2: Configurar el entorno

En lugar de una configuración manual, utiliza nuestro script de configuración estandarizado. Este script instala automáticamente **mise** y **uv**, las versiones de herramientas necesarias (**Python**, **Node.js**, **Java**), instala **firebase-tools** y sincroniza todas las dependencias.

```bash
scripts/setup-mve.sh
```

### Paso 3: Iniciar emuladores

```bash
firebase emulators:start
```

### Paso 4: Ejecutar el ejemplo

```bash
python main.py
```

## Componentes del proyecto

### Función nubosa (`functions/main.py`)

Una función activada por almacenamiento que:
- Activador: `on_object_finalized` (carga de archivos).
- Mecanismo: Descarga el CSV, lo analiza y utiliza **SQLAlchemy ORM** para guardarlo en PostgreSQL.

### Script principal (`main.py`)

- Carga un `users.csv` de ejemplo en el emulador de almacenamiento.
- Consulta la base de datos PostgreSQL mediante **SQLAlchemy** hasta que se detectan los nuevos registros.

## Variables de entorno

El archivo `.env` contiene:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mve_db
STORAGE_BUCKET=mve-gcp-cloud-sql.appspot.com
FIREBASE_STORAGE_EMULATOR_HOST="localhost:9199"
GCP_PROJECT=mve-gcp-cloud-sql
```

## Limpieza

Para eliminar completamente la infraestructura local (contenedores y volúmenes):

```bash
docker compose down -v
```

## Próximos Pasos

- Integrar más servicios de GCP.
- Añadir pruebas unitarias para la Cloud Function.

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
