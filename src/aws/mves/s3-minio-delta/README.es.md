# MinIO + Delta Lake + Docker: Ejemplo Mínimo Viable

Ejemplo mínimo viable (MVE) para trabajar con **MinIO** usando **Docker Compose** y **Delta Lake** (delta-rs) para transacciones ACID y capacidades de viaje en el tiempo.

## Estructura del Proyecto

```
project/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── minio_delta.py
├── pyproject.toml
├── main.py
├── uv.lock
└── README.md
```

## Requisitos Previos

- **Docker** y **Docker Compose** instalados
- **VS Code** con la extensión [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) (opcional)
- Acceso a la consola de MinIO (opcional)

-----

## Opción 1: Usando Contenedor de Desarrollo (Recomendado)

### Paso 1: Abrir el Proyecto en el Contenedor de Desarrollo

1. Abre VS Code en la carpeta del proyecto
2. Pulsa `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y se instalen las dependencias

### Paso 2: Iniciar el Servicio MinIO

Dentro de la terminal del contenedor de desarrollo:

```bash
docker compose up -d
```

Verifica que el servicio esté corriendo:

```bash
docker ps
```

Deberías ver el contenedor `minio_delta`.

### Paso 3: Crear Bucket en MinIO

1. Abre tu navegador y ve a: **http://localhost:9001**
2. Inicia sesión con:
   - **Usuario:** `minioadmin`
   - **Contraseña:** `minioadmin`
3. Haz clic en **Buckets** en la barra lateral izquierda
4. Haz clic en el botón **Create Bucket**
5. Ingresa el nombre del bucket: `delta-bucket`
6. Haz clic en **Create Bucket**

### Paso 4: Ejecutar el Script de Ejemplo

```bash
python main.py
```

Deberías ver una salida mostrando:
- Escritura de tabla Delta particionada por categoría
- Lectura de todos los datos de la tabla
- Sobrescritura solo de la partición Electronics usando predicate
- Lectura de todos los datos para verificar que la partición Accessories no cambió

### Paso 5: Ver Datos en la Consola de MinIO (Opcional)

1. Regresa a la consola de MinIO: **http://localhost:9001**
2. Navega a **Buckets** → `delta-bucket` → `sales_data/`
3. Verás la estructura de directorios de Delta Lake con archivos Parquet y logs de transacciones

-----

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Dependencias de Python

```bash
pip3 install uv && uv sync
```

### Paso 2: Iniciar el Servicio MinIO

```bash
docker compose up -d
```

### Paso 3: Crear Bucket en MinIO

Sigue el Paso 3 de la Opción 1.

### Paso 4: Ejecutar el Ejemplo

```bash
python main.py
```

### Paso 5: Ver Datos en la Consola de MinIO

Sigue el Paso 5 de la Opción 1.

-----

## ¿Qué es Delta Lake?

Delta Lake es una capa de almacenamiento de código abierto que aporta transacciones ACID a Apache Spark y cargas de trabajo de big data. Características clave:

- **Transacciones ACID**: Garantiza la integridad de los datos
- **Viaje en el Tiempo**: Acceso a versiones anteriores de los datos
- **Evolución de Esquema**: Modificar esquemas de tabla con el tiempo
- **Batch y Streaming Unificados**: Una sola tabla para ambas operaciones
- **Historial de Auditoría**: Historial completo de todos los cambios

## Cómo Funciona el Ejemplo

La clase `MinioDelta` proporciona dos métodos principales:

1. **`write(df, path, mode="overwrite", partition_by=None, predicate=None)`**: Escribir DataFrame de pandas como tabla Delta
   - `df`: DataFrame de pandas a escribir
   - `path`: Ruta de la tabla dentro del bucket
   - `mode`: Modo de escritura (`overwrite`, `append`, `error`, `ignore`)
   - `partition_by`: Lista opcional de columnas para particionar
   - `predicate`: Predicado SQL opcional para filtrar qué datos sobrescribir (ej. `"category = 'Electronics'"`)
   - Crea el log de transacciones de Delta Lake y almacena datos en formato Parquet

2. **`read(path, columns=None, filters=None)`**: Leer tabla Delta en DataFrame de pandas
   - `path`: Ruta de la tabla dentro del bucket
   - `columns`: Lista opcional de columnas a leer
   - `filters`: Lista opcional de filtros (ej. `[("category", "=", "Electronics")]`)
   - Devuelve la última versión como DataFrame de pandas

### Ejemplo de Uso

```python
client = MinioDelta()

# Escribir con particionado
client.write(df, "sales_data", partition_by=["category"])

# Leer con filtrado
electronics = client.read("sales_data", filters=[("category", "=", "Electronics")])

# Sobrescribir solo una partición específica usando predicate
client.write(
    updated_data, 
    "sales_data", 
    mode="overwrite",
    predicate="category = 'Electronics'"
)
```

### Opciones de Storage Importantes para MinIO

La clase `MinioDelta` usa las siguientes opciones críticas de storage para compatibilidad con MinIO:

```python
{
    "AWS_ALLOW_HTTP": "true",  # Habilitar conexiones HTTP (requerido para MinIO local)
    "aws_conditional_put": "etag",  # Habilitar operaciones atómicas usando ETags
}
```

Estas opciones son esenciales para que Delta Lake funcione correctamente con MinIO.

## Variables de Entorno

El archivo **`.env`** contiene:

```
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=http://localhost:9000
BUCKET_NAME=delta-bucket
```

**Nota:** Todas las variables de entorno son requeridas (sin valores por defecto). La clase `MinioDelta` lee el nombre del bucket del entorno, por lo que no necesitas especificarlo en cada llamada al método.

Puedes modificar estos valores según sea necesario. Recuerda **recrear los contenedores** si cambias las credenciales de MinIO.

## Estructura de Directorios de Delta Lake

Cuando creas una tabla Delta particionada, MinIO almacena:

```
delta-bucket/
└── sales_data/
    ├── _delta_log/
    │   ├── 00000000000000000000.json
    │   └── 00000000000000000001.json
    ├── category=Accessories/
    │   └── part-00000-xxxxx.parquet
    └── category=Electronics/
        └── part-00001-xxxxx.parquet
```

- **`_delta_log/`**: Log de transacciones (archivos JSON rastreando cada operación)
- **`category=*/`**: Directorios de partición (uno por cada valor único de categoría)
- **Archivos `.parquet`**: Datos reales en formato Apache Parquet

## Comandos Útiles

### Comandos de Docker

```bash
# Iniciar contenedor
docker compose up -d

# Detener contenedor
docker compose down

# Detener y eliminar volúmenes (elimina todos los datos)
docker compose down -v

# Ver logs
docker compose logs -f minio
```

### Consola de MinIO

```bash
# Acceder a la consola de MinIO
open http://localhost:9001
```

## Funcionalidades Avanzadas

### Viaje en el Tiempo

```python
# Leer versión específica
dt = DeltaTable(
    "s3://delta-bucket/sales_data",
    version=0,
    storage_options=client.storage_options
)
df_v0 = dt.to_pandas()
```

### Validación de Esquema

Delta Lake automáticamente valida la consistencia del esquema:
- Los nuevos datos deben coincidir con el esquema existente
- Evolución de esquema soportada con operaciones de merge

### Almacenamiento Optimizado

- Datos almacenados en formato columnar Parquet
- Compresión eficiente
- Predicate pushdown para consultas más rápidas

## Solución de Problemas

### Puerto ya en Uso

Si los puertos 9000 o 9001 ya están en uso, cambia los mapeos de puertos en `docker-compose.yml`:

```yaml
ports:
  - "9002:9000"  # Cambiar puerto del host
  - "9003:9001"
```

Actualiza `MINIO_ENDPOINT` en `.env` en consecuencia.

### Conexión Rechazada

Asegúrate de que el contenedor de MinIO esté corriendo:

```bash
docker ps
docker compose logs minio
```

### Errores de Permisos

Si obtienes errores de permisos de S3, verifica:
- El bucket existe (se crea automáticamente en la primera escritura)
- Las credenciales son correctas en `.env`
- `AWS_S3_ALLOW_UNSAFE_RENAME` está establecido en `"true"`

### Módulo No Encontrado

Si obtienes errores de importación, instala las dependencias:

```bash
pip3 install uv && uv sync
```

## Limpieza

Para eliminar completamente todo:

```bash
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar la imagen (opcional)
docker rmi minio/minio
```

## Comparación: Delta Lake vs. Archivos Regulares

| Característica | Archivos Regulares | Delta Lake |
|----------------|-------------------|------------|
| Transacciones ACID | ❌ | ✅ |
| Viaje en el Tiempo | ❌ | ✅ |
| Validación de Esquema | ❌ | ✅ |
| Escrituras Concurrentes | ⚠️ Riesgoso | ✅ Seguro |
| Historial de Auditoría | ❌ | ✅ |
| Protección contra Corrupción | ❌ | ✅ |

## Siguientes Pasos

- Implementar viaje en el tiempo para acceder a datos históricos
- Añadir ejemplos de evolución de esquema
- Integrar con Apache Spark para procesamiento a gran escala
- Implementar verificaciones de calidad de datos con restricciones de Delta Lake
- Configurar compactación y optimización automatizada (OPTIMIZE, VACUUM)
- Experimentar con particionado multinivel (ej. por año y mes)
- Añadir selección de columnas para leer solo campos específicos

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
