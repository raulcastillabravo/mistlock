# Ejemplo MinIO + Boto3 + Docker

Ejemplo mínimo viable para trabajar con MinIO usando Docker Compose, Boto3 (AWS SDK para Python) y pandas para manipulación de datos.

## Estructura del Proyecto

```
project/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── minio_client.py
├── pyproject.toml
├── main.py
├── uv.lock
└── README.md
```

## Requisitos Previos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para configuración de dev container)
- Acceso a la Consola de MinIO (basada en navegador)

## Opción 1: Usando Dev Container (Recomendado)

### Paso 1: Abrir el Proyecto en Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y las dependencias se instalen

### Paso 2: Iniciar el Contenedor de MinIO

Dentro de la terminal del dev container:

```bash
docker compose up -d
```

Verifica que esté ejecutándose:

```bash
docker ps
```

### Paso 3: Crear Bucket

Antes de ejecutar el script, crea el bucket en la Consola de MinIO:
1. Abre [http://localhost:9001](http://localhost:9001) (Usuario/Contraseña: `minioadmin`).
2. Ve a **Buckets** > **Create Bucket** y nómbralo `test-bucket`.

### Paso 4: Ejecutar el Ejemplo

```bash
python main.py
```

Deberías ver una salida como:

```
Bucket 'test-bucket' created successfully.
Created dummy DataFrame:
   id  value category
0   1     10        A
1   2     20        B
2   3     30        A
3   4     40        B
4   5     50        C
Saved DataFrame to 'data.csv'.
File 'data.csv' uploaded to 'test-bucket/data.csv'.
File 'test-bucket/data.csv' downloaded to 'downloaded_data.csv'.
Downloaded DataFrame:
   id  value category
0   1     10        A
1   2     20        B
2   3     30        A
3   4     40        B
4   5     50        C
Local files cleaned up.
```

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Dependencias de Python

```bash
pip3 install uv && uv sync
```

### Paso 2: Iniciar el Contenedor de MinIO

```bash
docker compose up -d
```

### Paso 3: Crear Bucket

1. Abre [http://localhost:9001](http://localhost:9001) (Usuario/Contraseña: `minioadmin`).
2. Ve a **Buckets** > **Create Bucket** y nómbralo `test-bucket`.

### Paso 4: Ejecutar el Ejemplo

```bash
python main.py
```

## Accediendo a la Consola de MinIO

### Paso 1: Abrir la Consola en el Navegador

1. Navega a: [http://localhost:9001](http://localhost:9001)
2. Ingresa las credenciales:
   - **Usuario:** `minioadmin`
   - **Contraseña:** `minioadmin`

### Paso 2: Ver Buckets y Archivos

1. En la Consola de MinIO, haz clic en **Buckets** en la barra lateral izquierda
2. Deberías ver el bucket `test-bucket`
3. Haz clic en `test-bucket` para ver su contenido
4. Deberías ver el archivo `data.csv` subido por el script de Python
5. Puedes descargar, previsualizar o gestionar archivos a través de la consola

## API del Cliente MinIO

El módulo `minio_client.py` proporciona un wrapper simple alrededor de boto3 para operaciones comunes de MinIO:

### Métodos Disponibles

| Método           | Descripción                                      | Parámetros                                    |
|------------------|--------------------------------------------------|-----------------------------------------------|
| `create_bucket`  | Crea un nuevo bucket si no existe                | `bucket_name` (str)                           |
| `upload_file`    | Sube un archivo a un bucket                      | `file_name` (str), `bucket` (str), `object_name` (str, opcional) |
| `download_file`  | Descarga un archivo desde un bucket              | `bucket` (str), `object_name` (str), `file_name` (str) |
| `delete_file`    | Elimina un archivo de un bucket                  | `bucket` (str), `object_name` (str)           |

### Ejemplo de Uso

```python
from minio_client import MinioClient

# Initialize client
client = MinioClient()

# Create bucket
client.create_bucket("my-bucket")

# Upload file
client.upload_file("local_file.csv", "my-bucket", "remote_file.csv")

# Download file
client.download_file("my-bucket", "remote_file.csv", "downloaded_file.csv")

# Delete file
client.delete_file("my-bucket", "remote_file.csv")
```

## Variables de Entorno

El archivo `.env` contiene:

```
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=http://localhost:9000
BUCKET_NAME=test-bucket
```

Puedes modificar estos valores según sea necesario. Recuerda recrear los contenedores si cambias las credenciales de MinIO.

## Comandos Útiles

### Comandos de Docker

```bash
# Iniciar contenedores
docker compose up -d

# Detener contenedores
docker compose down

# Detener y eliminar volúmenes (elimina todos los datos)
docker compose down -v

# Ver logs
docker compose logs -f

# Ver solo logs de MinIO
docker compose logs -f minio
```

## Solución de Problemas

### Puerto Ya en Uso

Si los puertos 9000 o 9001 ya están en uso, modifica la sección de puertos en `docker-compose.yml`:

```yaml
ports:
  - "9002:9000"  # Puerto API
  - "9003:9001"  # Puerto Consola
```

Luego actualiza `MINIO_ENDPOINT` en `.env`:

```
MINIO_ENDPOINT=http://localhost:9002
```

Y reinicia:

```bash
docker compose down
docker compose up -d
```

### Conexión Rechazada

Asegúrate de que el contenedor de MinIO esté ejecutándose:

```bash
docker ps
```

Verifica los logs en busca de errores:

```bash
docker compose logs minio
```

### Módulo No Encontrado

Si obtienes errores de importación, instala las dependencias:

```bash
pip3 install uv && uv sync
```

### Permiso Denegado (Dev Container)

Si obtienes errores de permisos con Docker en el dev container, asegúrate de que la característica `docker-outside-of-docker` esté correctamente configurada en `devcontainer.json`.

### No se Puede Acceder a la Consola de MinIO

Si no puedes acceder a la consola en `http://localhost:9001`:

1. Verifica que el contenedor esté ejecutándose: `docker ps`
2. Verifica que el mapeo de puertos sea correcto: `docker compose ps`
3. Intenta acceder vía `http://127.0.0.1:9001`
4. Verifica la configuración del firewall

## Limpieza

Para eliminar todo completamente:

```bash
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar la imagen de MinIO (opcional)
docker rmi minio/minio
```

## Próximos Pasos

- Implementar políticas de bucket para control de acceso
- Añadir versionado a los buckets
- Implementar gestión del ciclo de vida de objetos
- Añadir cifrado para datos sensibles
- Crear endpoints API con FastAPI para exponer operaciones de MinIO
- Implementar streaming de archivos para archivos grandes
- Añadir pruebas unitarias para las operaciones del cliente MinIO

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usar y modificar según sea necesario.
