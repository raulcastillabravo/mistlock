# Entorno Local de Databricks con Docker

Ejemplo mínimo viable para simular un entorno de Databricks localmente usando Docker, **MinIO como almacenamiento compatible con S3 y PostgreSQL como Hive Metastore persistente**. Este ejemplo muestra cómo desarrollar y probar ETLs de Spark/Delta Lake de forma local con una alta fidelidad respecto al entorno de la nube utilizando el **Databricks Runtime 15.4 LTS (Spark 3.5.0)**.

## Estructura del Proyecto

```
databricks-docker/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── src/
│   ├── databricks_shim/
│   │   ├── connect.py
│   │   └── utils.py
│   └── notebooks/
│       └── analysis.ipynb
├── Dockerfile
├── docker-compose.yml
├── .env
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Prerrequisitos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para configuración en contenedor)

## Opción 1: Usando Dev Container (Recomendado)

### Paso 1: Abrir el proyecto en el Dev Container

1. Abre VS Code en la carpeta del proyecto.
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac).
3. Escribe y selecciona: **Dev Containers: Reopen in Container**.
4. Espera a que el contenedor se construya y las dependencias se instalen.

### Paso 2: Ejecutar el ejemplo

```bash
python main.py
```

Deberías ver una salida que indica la transformación de las capas Bronze a Silver y una consulta de verificación final.

### Paso 3: Análisis Interactivo

Abre `src/notebooks/analysis.ipynb` y ejecuta las celdas para analizar los datos registrados en el Hive Metastore y **probar el DBUtils Shim** (secrets y widgets).
> **Nota**: Esta funcionalidad interactiva solo está disponible al usar el **Dev Container**, ya que este proporciona el entorno de Jupyter ya configurado.

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Levantar la Infraestructura

```bash
docker compose up -d
```

Esto iniciará:
- **Spark**: Instancia de Spark Standalone.
- **MinIO**: Almacenamiento compatible con S3.
- **Postgres**: Backend para el Hive Metastore.
- **mc**: Utilidad para crear automáticamente el `BUCKET_NAME` definido en el `.env`.

### Paso 2: Ejecutar el ejemplo

Ejecuta el script directamente dentro del contenedor de Spark:

```bash
docker compose exec spark python3 main.py
```

## Componentes del Proyecto

### Spark Client (`src/databricks_shim/connect.py`)

Función `get_spark_session(app_name)`:

- **Detección de Entorno**: Usa la variable `APP_ENV` para alternar entre los modos Local y Cloud.
- **Emulación**: Configura los conectores S3A, extensiones de Delta Lake y la conexión JDBC al Hive Metastore cuando `APP_ENV=local`.

### Databricks Shim (`src/databricks_shim/utils.py`)

Mock parcial para `dbutils`:

- **Secrets**: `dbutils.secrets.get()` se mapea a variables de entorno.
- **Widgets**: `dbutils.widgets.get()` se mapea a variables de entorno.
- **Pruebas**: El notebook `analysis.ipynb` incluye una sección para verificar estos mocks.
- **Extensibilidad**: Diseñado para ampliarse con más métodos de `fs` o `notebook` según sea necesario.

### Script Principal (`main.py`)

Demostración de ETL:

- 1. Genera datos raw con un esquema explícito.
- 2. Guarda los datos en la capa **Bronze** (Delta Lake en MinIO).
- 3. Lee de Bronze, transforma los datos y los guarda en la capa **Silver** como una **Tabla Gestionada** en el Hive Metastore.

## Variables de Entorno

El archivo `.env` contiene configuraciones críticas:

```
BUCKET_NAME=demo-bucket
STORAGE_PREFIX=s3a
AWS_ENDPOINT_URL=http://minio:9000
POSTGRES_HOST=postgres
```

**Nota**: `STORAGE_PREFIX` permite una alta portabilidad. Puedes cambiarlo a `abfss` al moverte a Azure sin cambiar la lógica del código.

## Comandos Útiles

### Comandos de Docker

```bash
# Levantar el entorno
docker compose up -d

# Ver logs de Spark/Metastore
docker compose logs -f

# Parar y limpiar todo completamente
docker compose down -v
```

## Solución de Problemas

### Connection Refused

Asegúrate de que todos los servicios estén corriendo:

```bash
docker compose ps
```

### La tabla ya existe

Si ejecutas la ETL varias veces con diferentes esquemas, podrías encontrar conflictos en el Metastore. Usa `spark.sql("DROP TABLE IF EXISTS sales.products_silver")` o limpia los volúmenes.

## Limpieza

Para eliminar contenedores y datos persistentes:

```bash
docker compose down -v
```

## Siguientes Pasos

- Implementar pruebas de Delta Lake Time Travel.
- Añadir más métodos mock de `dbutils.fs`.
- Integrar con herramientas de BI locales conectando al Hive Metastore.

## Licencia

Este es un ejemplo mínimo para fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
