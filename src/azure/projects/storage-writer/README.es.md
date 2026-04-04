# Ejemplo de Azure Functions + Azurite

Ejemplo mínimo viable para trabajar con Azure Functions localmente usando Azurite, Docker Compose y Python. Este ejemplo demuestra cómo crear una función activada por HTTP que sube archivos al almacenamiento de blobs local.

## Estructura del Proyecto

```
azure-functions/
├── upload-function/
│   ├── azurite_client.py
│   ├── function_app.py
│   ├── host.json
│   ├── local.settings.json
│   └── requirements.txt
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── docker-compose.yml
├── .env
├── main.py
├── pyproject.toml
├── README.es.md
└── README.md
```

## Requisitos Previos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para configuración de dev container)
- Azure Functions Core Tools (se instala automáticamente en el dev container)

## Opción 1: Usar Dev Container (Recomendado)

### Paso 1: Abrir Proyecto en Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y las dependencias se instalen

El dev container incluye:

- **Extensión de Azure Functions** para desarrollo y depuración local
- **Extensión de Azure Storage** para explorar el almacenamiento de blobs
- **Azure CLI** para operaciones adicionales de Azure

### Paso 2: Iniciar Azurite

Dentro del terminal del dev container:

```bash
docker compose up -d
```

Verifica que esté ejecutándose:

```bash
docker ps
```

### Paso 3: Iniciar Azure Functions

```bash
source .venv/bin/activate
func start --prefix ./upload-function/
```

Deberías ver una salida como:

```
Azure Functions Core Tools
Core Tools Version:       4.x.x
Function Runtime Version: 4.x.x

Functions:

        UploadFile: [POST] http://localhost:7071/api/upload

For detailed output, run func with --verbose flag.
```

### Paso 4: Probar la Función

Abre una nueva terminal y ejecuta:

```bash
python main.py
```

Deberías ver:

```
Testing Azure Function upload endpoint...

Uploading 'test.txt'...
Status: 200
Response: File 'test.txt' uploaded to 'uploads'.
```

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Azure Functions Core Tools

Sigue la guía de instalación oficial:

- **Windows**: `npm install -g azure-functions-core-tools@4 --unsafe-perm true`
- **macOS**: `brew tap azure/functions && brew install azure-functions-core-tools@4`
- **Linux**: Sigue la [documentación oficial](https://learn.microsoft.com/es-es/azure/azure-functions/functions-run-local)

### Paso 2: Instalar Dependencias de Python

```bash
pip3 install uv && uv sync
```

### Paso 3: Iniciar Azurite

Usando Docker Compose:

```bash
docker compose up -d
```

### Paso 4: Iniciar Azure Functions

```bash
source .venv/bin/activate
func start --prefix ./upload-function/
```

### Paso 5: Probar la Función

```bash
python main.py
```

## Componentes del Proyecto

### AzuriteClient (`upload-function/azurite_client.py`)

Cliente reutilizable para operaciones de almacenamiento de blobs de Azurite:

- **`create_container(container_name)`**: Crea el contenedor si no existe
- **`upload_blob(container_name, blob_name, data)`**: Sube datos a un blob

### Function App (`upload-function/function_app.py`)

Aplicación de Azure Functions con activador HTTP:

- **`@app.route`**: Define el endpoint HTTP `/api/upload` que acepta peticiones POST
- **`upload_file(req)`**: Maneja la subida de archivos usando AzuriteClient
- **Manejo de Errores**: Devuelve códigos de estado HTTP apropiados

### Configuración del Host (`upload-function/host.json`)

Configuración global para el host de Functions:

- Configuración de logging
- Configuración del bundle de extensiones

### Ajustes Locales (`upload-function/local.settings.json`)

Ajustes de desarrollo local:

- **AzureWebJobsStorage**: Conexión a Azurite para el runtime de Functions
- **AZURE_STORAGE_CONNECTION_STRING**: Conexión para operaciones de blobs
- **BLOB_CONTAINER_NAME**: Contenedor destino para las subidas

### Dependencias de la Función (`upload-function/requirements.txt`)

Dependencias de Python para el runtime de Azure Functions.

### Script Principal (`main.py`)

Script de demostración que invoca la Azure Function desplegada:

- Hace una petición HTTP POST al endpoint de la función
- Sube un archivo de prueba
- Muestra la respuesta

### Docker Compose (`docker-compose.yml`)

Configuración del servicio Azurite:

- Servicio de blobs en el puerto 10000
- Servicio de colas en el puerto 10001
- Servicio de tablas en el puerto 10002

## Variables de Entorno

El archivo `.env` contiene:

```
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;

BLOB_CONTAINER_NAME=uploads
```

**Nota**: La cadena de conexión usa las credenciales predeterminadas de Azurite para desarrollo local.

## Extensión de Azure Functions

La extensión de **Azure Functions** para VS Code (incluida en el dev container) proporciona:

- **Depuración Local**: Establece puntos de interrupción y depura funciones localmente
- **Gestión de Funciones**: Crea, elimina y gestiona funciones desde VS Code
- **Despliegue**: Despliega funciones a Azure directamente desde el editor
- **Transmisión de Logs**: Visualiza logs en tiempo real de tus funciones

### Usar la Extensión

1. Abre la vista de Azure en VS Code (icono de Azure en la barra lateral)
2. En "Workspace", verás tus funciones locales
3. Haz clic derecho en una función para depurar, probar o ver logs
4. Usa la opción "Execute Function Now" para probar sin llamadas externas

## Comandos Útiles

### Comandos de Azure Functions

```bash
# Iniciar runtime de Functions
cd upload-function
func start

# Iniciar con logging detallado
func start --verbose

# Crear una nueva función
func new

# Instalar extensiones
func extensions install
```

### Comandos de Docker

```bash
# Iniciar contenedor de Azurite
docker compose up -d

# Detener contenedor
docker compose down

# Detener y eliminar volúmenes (eliminar todos los datos)
docker compose down -v

# Ver logs
docker compose logs -f azurite
```

### Comandos de Prueba

```bash
# Ejecutar el script de prueba
python main.py

# O usar curl directamente
curl -X POST "http://localhost:7071/api/upload?filename=test.txt" \
  -H "Content-Type: text/plain" \
  -d "Hello from Azure Functions!"
```

## Solución de Problemas

### Puerto Ya en Uso

Si el puerto 7071 (Functions) o 10000 (Azurite) ya está en uso:

**Para Azurite**, modifica `docker-compose.yml`:

```yaml
ports:
  - "10010:10000"
```

Luego actualiza las cadenas de conexión en `.env` y `upload-function/local.settings.json`:

```
BlobEndpoint=http://127.0.0.1:10010/devstoreaccount1
```

**Para Functions**, establece un puerto diferente:

```bash
func start --port 7072
```

### Conexión Rechazada

Asegúrate de que Azurite esté ejecutándose:

```bash
docker ps
```

Verifica que la cadena de conexión en `upload-function/local.settings.json` coincida con tu configuración de Azurite.

### Módulo No Encontrado

Si obtienes errores de importación en la función:

```bash
cd upload-function
pip install -r requirements.txt
```

### Función No Encontrada

Si la función no aparece al ejecutar `func start`:

1. Verifica que estés en el directorio `upload-function`
2. Comprueba que `function_app.py` existe
3. Verifica que `host.json` tenga el bundle de extensiones correcto
4. Intenta eliminar `.venv` y reinstalar las dependencias

## Limpieza

Para eliminar completamente todo:

```bash
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar la imagen de Azurite (opcional)
docker rmi mcr.microsoft.com/azure-storage/azurite
```

## Próximos Pasos

- Añadir más tipos de activadores (Timer, Queue, Blob)
- Implementar bindings de funciones para operaciones automáticas de blobs
- Añadir pruebas unitarias para las funciones
- Desplegar a Azure Functions en la nube
- Añadir autenticación y autorización

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usar y modificar según sea necesario.
