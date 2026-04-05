# Metabase + PostgreSQL + Docker: Ejemplo Mínimo Viable

Ejemplo mínimo viable (MVE) para trabajar con **Metabase** usando **Docker Compose**, **PostgreSQL** como fuente de datos y el ORM **SQLAlchemy**.

## Estructura del Proyecto

```
project/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── db.py
├── models.py
├── pyproject.toml
├── main.py
├── uv.lock
└── README.md
```

## Requisitos Previos

  * **Docker** y **Docker Compose** instalados.
  * **VS Code** con la extensión [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) (opcional, para la configuración del contenedor de desarrollo).
  * **DBeaver** o cualquier cliente PostgreSQL (opcional).

-----

## Opción 1: Usando Contenedor de Desarrollo (Recomendado)

### Paso 1: Abrir el Proyecto en el Contenedor de Desarrollo

1.  Abre VS Code en la carpeta del proyecto.
2.  Pulsa `F1` o `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac).
3.  Escribe y selecciona: **Dev Containers: Reopen in Container** (Contenedores de Desarrollo: Reabrir en Contenedor).
4.  Espera a que el contenedor se construya y se instalen las dependencias.

### Paso 2: Iniciar los Servicios

Dentro de la terminal del contenedor de desarrollo:

```bash
docker compose up -d
```

Verifica que los servicios estén corriendo:

```bash
docker ps
```

Deberías ver dos contenedores: `metabase` y `postgres_metabase`.

### Paso 3: Crear Tablas e Insertar Datos de Ejemplo

Ejecuta el script de Python:

```bash
python main.py
```

Deberías ver una salida similar a esta:

```
Inserted 25 products into the database
```

Esto creará la tabla `products` en la base de datos `metabaseappdb` e insertará 25 productos de ejemplo con datos pre-calculados.

### Paso 4: Acceder a Metabase

1. Abre tu navegador y ve a: **http://localhost:3000**
2. Completa la configuración inicial:
   - Crea tu cuenta de administrador
   - Haz clic en "Agregar tus datos" o "Add your data"
   - Selecciona **PostgreSQL**
   - Introduce los detalles de conexión:
     - **Host:** `postgres`
     - **Port:** `5432`
     - **Database name:** `metabaseappdb`
     - **Username:** `metabase`
     - **Password:** `metabase123`
3. Haz clic en **Save** (Guardar)
4. ¡Comienza a explorar tus datos y crear visualizaciones!

-----

## Opción 2: Configuración Local (Sin Dev Container)

### Paso 1: Instalar Dependencias de Python

```bash
pip3 install uv && uv sync
```

### Paso 2: Iniciar los Servicios

```bash
docker compose up -d
```

### Paso 3: Crear Tablas e Insertar Datos

```bash
python main.py
```

### Paso 4: Acceder a Metabase

Sigue el Paso 4 de la Opción 1 anterior.

-----

## Esquema de la Base de Datos

La tabla **`products`** tiene la siguiente estructura:

| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | `INTEGER` (Clave Primaria) | ID de producto autoincremental. |
| `name` | `VARCHAR(200)` | Nombre del producto. |
| `category` | `VARCHAR(100)` | Categoría del producto. |
| `price` | `FLOAT` | Precio unitario. |
| `quantity_sold` | `INTEGER` | Número de unidades vendidas. |
| `revenue` | `FLOAT` | Ingresos totales (precio × cantidad). |
| `sale_date` | `TIMESTAMP` | Fecha de venta. |

## Datos de Ejemplo

El script inserta 25 productos de ejemplo distribuidos en 5 categorías:
- **Electronics** (5 productos): Laptops, teléfonos, TVs, auriculares, smartwatches
- **Clothing** (5 productos): Zapatillas, jeans, chaquetas, camisetas, abrigos
- **Home & Kitchen** (5 productos): Batidoras, cafeteras, aspiradoras, freidoras de aire, utensilios de cocina
- **Books** (5 productos): Literatura clásica y libros de negocios
- **Sports & Outdoors** (5 productos): Esterillas de yoga, mancuernas, bicicletas, tiendas de campaña, zapatillas para correr

-----

## Variables de Entorno

El archivo **`.env`** contiene lo siguiente:

```
METABASE_USER=metabase
METABASE_PASSWORD=metabase123
METABASE_DB=metabaseappdb
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

Puedes modificar estos valores según sea necesario. Recuerda **recrear los contenedores** si cambias las credenciales de la base de datos.

-----

## 🔗 Conexión con DBeaver (Opcional)

### Paso 1: Crear Nueva Conexión

1.  Abre DBeaver.
2.  Haz clic en **New Database Connection** (icono del enchufe con un +).
3.  Selecciona **PostgreSQL**.
4.  Haz clic en **Siguiente**.

### Paso 2: Configurar la Conexión

Introduce los siguientes detalles:

  * **Host:** `localhost`
  * **Port:** `5432`
  * **Database:** `metabaseappdb`
  * **Username:** `metabase`
  * **Password:** `metabase123`

### Paso 3: Probar y Guardar

1.  Haz clic en **Test Connection** para verificar.
2.  Si es exitoso, haz clic en **Finish**.

### Paso 4: Ver los Datos

1.  En el **Database Navigator**, expande tu conexión.
2.  Navega a: `metabaseappdb` → `Schemas` → `public` → `Tables` → **`products`**.
3.  Haz clic derecho sobre la tabla **`products`** → **View Data** (Ver Datos).
4.  Deberías ver los 25 productos insertados por el script de Python.

-----

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

# Ver solo los logs de Metabase
docker compose logs -f metabase

# Ver solo los logs de PostgreSQL
docker compose logs -f postgres
```

### Comandos de Metabase

```bash
# Verificar si Metabase está listo
curl http://localhost:3000/api/health
```

-----

## Creando Visualizaciones en Metabase

Una vez que hayas conectado Metabase a PostgreSQL, puedes crear varias visualizaciones:

### Ejemplos de Preguntas para Hacer:

1. **Ingresos Totales por Categoría**
   - Visualización: Gráfico de barras o gráfico circular
   - Agrupar por: `category`
   - Resumir: Suma de `revenue`

2. **Unidades Vendidas a lo Largo del Tiempo**
   - Visualización: Gráfico de líneas
   - Eje X: `sale_date`
   - Eje Y: Suma de `quantity_sold`

3. **Top 10 Productos por Ingresos**
   - Visualización: Gráfico de barras
   - Ordenar por: `revenue` (descendente)
   - Límite: 10

4. **Precio Promedio por Categoría**
   - Visualización: Gráfico de barras
   - Agrupar por: `category`
   - Resumir: Promedio de `price`

-----

## Solución de Problemas (Troubleshooting)

### Puerto ya en uso

Si el puerto 3000 o 5432 ya está en uso, cambia los mapeos de puertos en `docker-compose.yml` y reinicia:

```bash
docker compose down
docker compose up -d
```

### Metabase no Carga

Espera un minuto para que Metabase se inicie completamente. Verifica el estado:

```bash
docker compose logs -f metabase
```

Busca el mensaje: "Metabase Initialization COMPLETE"

### Conexión Rechazada

Asegúrate de que ambos contenedores estén corriendo:

```bash
docker ps
```

Comprueba los logs en busca de errores:

```bash
docker compose logs postgres
docker compose logs metabase
```

### Módulo No Encontrado

Si obtienes errores de importación, instala las dependencias:

```bash
pip3 install uv && uv sync
```

### Permiso Denegado (Dev Container)

Si obtienes errores de permisos con Docker dentro del contenedor de desarrollo, asegúrate de que la *feature* `docker-outside-of-docker` esté configurada correctamente en tu `devcontainer.json`.

-----

## Limpieza

Para eliminar completamente todos los contenedores y datos asociados:

```bash
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar las imágenes (opcional)
docker rmi metabase/metabase:latest postgres:15-alpine
```

-----

## Siguientes Pasos

  * Crear consultas y dashboards más complejos en Metabase
  * Añadir más datos de productos con diferentes rangos de fechas
  * Implementar relaciones de datos (ej., clientes, pedidos)
  * Configurar informes automáticos por correo electrónico en Metabase
  * Configurar permisos de usuario y compartir en Metabase
  * Añadir más tablas para crear una base de datos de comercio electrónico completa

