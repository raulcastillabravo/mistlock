# Azure Cosmos DB + Docker

Ejemplo mínimo viable para trabajar con Azure Cosmos DB localmente usando Docker. Este ejemplo demuestra cómo integrar una aplicación Python con el emulador de Azure Cosmos DB.

## Estructura del Proyecto

```
azure-cosmos-db/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── docker-compose.yml
├── .env
├── main.py
├── pyproject.toml
└── README.md
```

## Requisitos Previos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (opcional, para configuración de dev container)

## Opción 1: Uso de Dev Container (Recomendado)

### Paso 1: Abrir el Proyecto en Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Escribe y selecciona: **Dev Containers: Reopen in Container**
4. Espera a que el contenedor se construya y las dependencias se instalen

### Paso 2: Ejecutar el Ejemplo

Si ves el mensaje `PostgreSQL=FAIL` en los logs de la terminal, `main.py` fallará. Por favor, consulta la sección de **Solución de Problemas** para corregirlo.

```bash
python main.py
```

Deberías ver una salida como:

```
--- Cosmos DB Connection Test ---
Endpoint: http://localhost:8081
Connecting to database: TestDB...
Connecting to container: TestContainer...
Uploading test item with ID: ...
SUCCESS: Item uploaded successfully to Cosmos DB!
```

### Paso 3: Validar los resultados

Puedes verificar que los datos se han subido de dos formas:

1.  **Explorador Web**: Abre [http://localhost:1234/](http://localhost:1234/) en tu navegador.
2.  **Extensión de VS Code**: Instala la extensión [Azure Cosmos DB](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb) y conéctate usando la siguiente cadena de conexión (HTTP):
    ```
    AccountEndpoint=http://localhost:8081/;AccountKey=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==;
    ```

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Dependencias de Python

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv sync
```

### Paso 2: Iniciar el Emulador

```bash
docker compose up -d cosmos
```

**Espera entre 15 y 30 segundos** para asegurar que el emulador se haya inicializado completamente antes de ejecutar el script.

### Paso 3: Ejecutar el Ejemplo

Si ves el mensaje `PostgreSQL=FAIL` en los logs de la terminal, `main.py` fallará. Por favor, consulta la sección de **Solución de Problemas** para corregirlo.

```bash
python main.py
```

### Paso 4: Validar los resultados

Puedes verificar que los datos se han subido de dos formas:

1.  **Explorador Web**: Abre [http://localhost:1234/](http://localhost:1234/) en tu navegador.
2.  **Extensión de VS Code**: Instala la extensión [Azure Cosmos DB](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb) y conéctate usando la siguiente cadena de conexión (HTTP):
    ```
    AccountEndpoint=http://localhost:8081/;AccountKey=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==;
    ```

## Componentes del Proyecto

### Script Principal (`main.py`)

Script de Python que demuestra cómo conectar e interactuar con Cosmos DB:

- **CosmosClient**: Conecta al emulador usando variables de entorno.
- **`run()`**: Función principal que crea una base de datos, un contenedor e inserta un elemento de prueba.

## Variables de Entorno

El archivo `.env` contiene:

```
COSMOS_ENDPOINT=http://localhost:8081
COSMOS_KEY=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==
```

**Nota**: La clave es la clave maestra por defecto para el emulador de Cosmos DB.

## Comandos Útiles

### Comandos de Docker

```bash
# Iniciar emulador
docker compose up -d cosmos

# Detener emulador
docker compose down

# Ver logs
docker compose logs -f cosmos
```

## Solución de Problemas

### Conexión Rechazada

Asegúrate de que el emulador esté funcionando:
```bash
docker ps
```

### Aviso de PostgreSQL=FAIL

Si ves los mensajes `PostgreSQL=FAIL, Gateway=OK, Explorer=OK` o `pgcosmos readiness check still waiting` en los logs, significa que la capa de compatibilidad con PostgreSQL del emulador ha fallado al iniciar.

**Este aviso impedirá que `main.py` se ejecute correctamente**, ya que el SDK puede fallar al conectar mientras los servicios internos siguen en un bucle de reintento.

**Solución:**
Para solucionar esto y permitir que `main.py` funcione, debes borrar los volúmenes de datos para resetear el estado del emulador:
```bash
docker compose down -v
```
*(Nota: Esto eliminará cualquier base de datos existente en el emulador).*

### El periodo de evaluación ha expirado / Error 104 de PAL

Si ves el error `Error: The evaluation period has expired` o `PAL initialization failed. Error: 104`, significa que el periodo de evaluación de 180 días de la imagen del emulador ha terminado.

**Solución Oficial (Descargar imagen más reciente):**
1.  Detén todo: `docker compose down -v`
2.  Elimina la imagen antigua: `docker rmi mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator`
3.  Descarga la última versión: `docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest`
4.  Levanta de nuevo: `docker compose up -d cosmos`

**Solución Alternativa (Usar un tag específico):**
Si Microsoft aún no ha actualizado la imagen `latest` y la solución oficial no funciona, busca una etiqueta de versión específica y reciente en el repositorio oficial:
1. Ve a [Azure Cosmos DB Emulator Docker Releases](https://github.com/Azure/azure-cosmos-db-emulator-docker/releases).
2. Busca el tag más reciente (ej. `vnext-EN20251223`).
3. Actualiza la imagen en `docker-compose.yml` con ese tag.
4. Levanta de nuevo: `docker compose up -d cosmos`

## Limpieza

Para eliminar todo completamente:

```bash
docker compose down -v
```

## Licencia

Este es un ejemplo mínimo con fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
