# Ejemplo de Azurite + Azure Blob Storage

Ejemplo mínimo viable para trabajar con Azure Blob Storage localmente usando Azurite, Docker Compose y Python. Este ejemplo demuestra cómo crear contenedores y subir/descargar blobs.

## Estructura del Proyecto

```
azurite-docker/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── docker-compose.yml
├── .env
├── azurite_client.py
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Prerrequisitos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para configuración con dev container)

## Opción 1: Usando Dev Container (Recomendado)

### Paso 1: Abrir el Proyecto en Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y se instalen las dependencias

El dev container incluye la **extensión de Azure Storage** para explorar y administrar recursos de Azure Storage.

### Paso 2: Iniciar Azurite

Dentro de la terminal del dev container:

```bash
docker compose up -d
```

Verifica que esté ejecutándose:

```bash
docker ps
```

### Paso 3: Ejecutar el Ejemplo

```bash
python main.py
```

Deberías ver una salida como:

```
Connecting to Azurite...
Container 'test-container' created.

Uploading blob...
Uploaded 'hello.txt' to container 'test-container'.

Listing blobs in container:
  - hello.txt

Downloading blob...
Content: Hello from Azurite!
```

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Dependencias de Python

```bash
pip3 install uv && uv sync
```

### Paso 2: Iniciar Azurite

Usando Docker Compose:

```bash
docker compose up -d
```

### Paso 3: Ejecutar el Ejemplo

```bash
python main.py
```

## Componentes del Proyecto

### AzuriteClient (`azurite_client.py`)

Clase cliente para operaciones de Azure Blob Storage:

- **Constructor**: Lee la cadena de conexión de las variables de entorno y crea BlobServiceClient
- **`create_container(container_name)`**: Crea un contenedor si no existe
- **`upload_blob(container_name, blob_name, data)`**: Sube datos a un blob
- **`download_blob(container_name, blob_name)`**: Descarga y retorna el contenido del blob
- **`list_blobs(container_name)`**: Lista todos los blobs en un contenedor

### Script Principal (`main.py`)

Demuestra operaciones de Azurite Blob Storage:

- Crea un contenedor
- Sube un blob
- Lista todos los blobs en el contenedor
- Descarga y muestra el contenido del blob

## Variables de Entorno

El archivo `.env` contiene:

```
# Cadena de conexión por defecto de Azurite
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;

# Nombre del contenedor
CONTAINER_NAME=test-container
```

**Nota**: La cadena de conexión usa las credenciales por defecto de Azurite para desarrollo local.

## Extensión de Azure Storage

La extensión de **Azure Storage** para VS Code (incluida en el dev container) proporciona:

- **Explorador de Cuentas de Almacenamiento**: Explora contenedores, blobs, colas y tablas
- **Administración Visual**: Crea, elimina y administra recursos de almacenamiento desde VS Code
- **Operaciones con Blobs**: Sube, descarga y elimina blobs directamente desde la interfaz
- **Funciona con Azurite**: Conéctate a tu instancia local de Azurite para pruebas fáciles

### Usando la Extensión

1. Abre la vista de Azure en VS Code (icono de Azure en la barra lateral)
2. En "Storage Accounts", haz clic en "Attach Storage Account"
3. Selecciona "Attach to a local emulator"
4. Usa la configuración de conexión por defecto de Azurite
5. Explora tus contenedores y blobs visualmente

## Comandos Útiles

### Comandos de Docker

```bash
# Iniciar contenedor de Azurite
docker compose up -d

# Detener contenedor
docker compose down

# Detener y eliminar volúmenes (eliminar todos los datos)
docker compose down -v

# Ver logs
docker compose logs -f

# Ver solo logs de Azurite
docker compose logs -f azurite
```

### Azure Storage Explorer

También puedes usar [Azure Storage Explorer](https://azure.microsoft.com/es-es/products/storage/storage-explorer/) para explorar el almacenamiento de Azurite:

1. Descarga e instala Azure Storage Explorer
2. Conéctate al Emulador de Almacenamiento Local
3. Usa la cadena de conexión por defecto de Azurite

## Solución de Problemas

### Puerto Ya en Uso

Si el puerto 10000 ya está en uso, modifica la sección de puertos en `docker-compose.yml`:

```yaml
ports:
  - "10010:10000"
```

Luego actualiza la cadena de conexión en `.env`:

```
BlobEndpoint=http://127.0.0.1:10010/devstoreaccount1
```

### Conexión Rechazada

Asegúrate de que Azurite esté ejecutándose:

```bash
docker ps
```



### Módulo No Encontrado

Si obtienes errores de importación, instala las dependencias:

```bash
pip3 install uv && uv sync
```

## Limpieza

Para eliminar todo completamente:

```bash
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar la imagen de Azurite (opcional)
docker rmi mcr.microsoft.com/azure-storage/azurite
```

## Próximos Pasos

- Agregar ejemplos de Queue storage
- Agregar ejemplos de Table storage
- Implementar Azure Functions con Azurite
- Agregar pruebas unitarias para operaciones de almacenamiento

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usar y modificar según sea necesario.
