# Azure SQL Database + Azure Functions

Ejemplo mínimo viable para trabajar con **Azure SQL Edge** usando **Azure Functions** y **SQLAlchemy**. Este ejemplo demuestra cómo procesar peticiones HTTP POST y persistir datos en una base de datos SQL.

## Estructura del Proyecto

```
azure-sql-database/
├── .devcontainer/
│   └── devcontainer.json
├── functions/
│   └── register_user.py    # Lógica de la función (Blueprint)
├── shared/
│   └── database.py         # Modelos SQLAlchemy
├── sql/
│   └── init.sql            # Script de inicialización de DB
├── scripts/
│   ├── setup-mve.sh        # Configuración del entorno
│   └── init-sql.sh         # Inicialización de tablas SQL
├── .funcignore
├── function_app.py         # Punto de entrada de la Azure Function
├── host.json
├── local.settings.json
├── docker-compose.yml      # Infraestructura de SQL Edge
├── main.py                 # Script de prueba (envío de POST)
├── pyproject.toml
└── README.md
```

## Prerrequisitos

- Docker y Docker Compose instalados
- VS Code con la extensión Dev Containers (Recomendado)
- Azure Functions Core Tools (Se instalan automáticamente en el Dev Container)

## Opción 1: Usando Dev Container (Recomendado)

### Paso 1: Abrir el Proyecto en el Dev Container

1. Abre VS Code en la carpeta del proyecto
2. Presiona `F1` o `Ctrl+Shift+P` y selecciona: **Dev Containers: Reopen in Container**
3. Espera a que el contenedor se construya y las dependencias se instalen

### Paso 2: Ejecutar la Azure Function

Inicia el runtime local de Azure Functions:

```bash
func start
```

### Paso 3: Ejecutar el Ejemplo

En una nueva terminal, ejecuta el script de prueba:

```bash
python main.py
```

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Levantar Infraestructura

Inicia el contenedor de SQL Edge:

```bash
docker compose up -d
```

### Paso 2: Configurar Entorno

Ejecuta el script de configuración estandarizado:

```bash
scripts/setup-mve.sh
```

### Paso 3: Ejecutar la Función y Probar

```bash
func start
# En otra terminal
python main.py
```

## Validación

### Opción A: Extensión SQL Server para VS Code

1. Instala la extensión **SQL Server (mssql)**.
2. Haz clic en el **icono de SQL Server** en la barra de actividad.
3. Haz clic en **Add Connection (+)**.
4. Usa los siguientes detalles:
   - **Server name**: `azure-sql-edge`
   - **Authentication Type**: `SQL Login`
   - **User name**: `sa`
   - **Password**: `Password123!`
   - **Trust Server Certificate**: `True` (Esencial para conexión local)
   - **Database**: `UserDB` (Creada automáticamente durante el setup)

### Opción B: Terminal (CURL)

Puedes verificar la función directamente usando `curl`:

```bash
curl -X POST http://localhost:7071/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Jane Smith", "email": "jane@example.com"}'
```

## Componentes del Proyecto

### Azure Function App (`function_app.py`)

- **Root Entrypoint**: Configura la FunctionApp y registra los blueprints del directorio `functions/`.

### Lógica de la Función (`functions/register_user.py`)

- **`register_user`**: Trigger HTTP (vía Blueprint) que recibe un payload JSON y utiliza la capa de base de datos compartida para persistirlo.

### Capa de Base de Datos (`shared/database.py`)

- **SQLAlchemy**: Módulo centralizado para modelos de base de datos y lógica de conexión usando SQLAlchemy ORM.

## Limpieza

Para eliminar contenedores y volúmenes:

```bash
docker compose down -v
```

## Licencia

Este es un ejemplo mínimo para fines educativos. Siéntete libre de usarlo y modificarlo según sea necesario.
